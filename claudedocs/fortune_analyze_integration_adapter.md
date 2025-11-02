# Fortune-Analyze Integration Adapter

**Version**: 1.0
**Purpose**: Integration layer between Django web platform and existing `/fortune-analyze` command
**Last Updated**: 2025-11-02

---

## Overview

This document defines the integration adapter that converts web platform Order/Profile data into the existing `/fortune-analyze` command format without modifying the command itself. The adapter acts as a bridge between the Django models and the Claude Code CLI command.

---

## Integration Architecture

```
┌─────────────────────┐
│  Django Web App     │
│  (User Interface)   │
└──────────┬──────────┘
           │ Order Creation
           ▼
┌─────────────────────┐
│  Order Model        │
│  Profile Model      │
└──────────┬──────────┘
           │ Celery Task Triggered
           ▼
┌─────────────────────┐
│  Integration Adapter│ ← THIS DOCUMENT
│  (fortune_adapter)  │
└──────────┬──────────┘
           │ Command Invocation
           ▼
┌─────────────────────┐
│  Claude Code CLI    │
│  /fortune-analyze   │
└──────────┬──────────┘
           │ File Creation
           ▼
┌─────────────────────┐
│  Person Directory   │
│  {YYYYMMDD_HHMM}/   │
│  ├── calculations   │
│  ├── report.html    │
│  ├── synthesis.md   │
│  └── 8 expert .md   │
└──────────┬──────────┘
           │ File Retrieval
           ▼
┌─────────────────────┐
│  AnalysisReport     │
│  Model (DB Storage) │
└─────────────────────┘
```

---

## Data Model Mapping

### Django Models (Web Platform)

```python
# apps/orders/models.py

class Profile(models.Model):
    """Birth data profile"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    birth_date = models.DateField()  # YYYY-MM-DD
    birth_time = models.TimeField()  # HH:MM:SS
    birth_location = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    """Purchase order for analysis"""
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('paid', 'Payment Confirmed'),
        ('processing', 'Analysis In Progress'),
        ('completed', 'Analysis Complete'),
        ('failed', 'Analysis Failed'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    selected_experts = models.JSONField()  # ['bazi', 'ziwei', 'astrology', ...]
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_intent_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AnalysisJob(models.Model):
    """Background job tracking"""
    STATUS_CHOICES = [
        ('queued', 'Queued'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('retry', 'Retrying'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='queued')
    celery_task_id = models.CharField(max_length=100, blank=True)
    retry_count = models.IntegerField(default=0)
    max_retries = models.IntegerField(default=3)
    error_message = models.TextField(blank=True)
    current_phase = models.IntegerField(default=0)  # 0=not started, 1-3=phases
    person_directory = models.CharField(max_length=500, blank=True)  # e.g., "19940414_2140_陈洁玲"
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

class AnalysisReport(models.Model):
    """Generated analysis report"""
    job = models.OneToOneField(AnalysisJob, on_delete=models.CASCADE)
    report_html = models.TextField()  # Full HTML content
    synthesis_markdown = models.TextField(blank=True)  # synthesis_report.md
    calculations_json = models.JSONField()  # calculations.json

    # Individual expert reports (MD format)
    bazi_report = models.TextField(blank=True)
    ziwei_report = models.TextField(blank=True)
    astrology_report = models.TextField(blank=True)
    plum_blossom_report = models.TextField(blank=True)
    qimen_report = models.TextField(blank=True)
    liuyao_report = models.TextField(blank=True)
    numerology_report = models.TextField(blank=True)
    name_analysis_report = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
```

### Command Arguments Mapping

```python
# /fortune-analyze <name> <birth_date> <birth_time> <location> <gender> [--methods ...]

# From Django Profile to Command Arguments:
profile = {
    'name': '陈洁玲',
    'birth_date': date(1994, 4, 14),
    'birth_time': time(21, 40, 0),
    'birth_location': '汕頭, 廣東',
    'gender': 'female'
}

selected_experts = ['bazi', 'ziwei', 'astrology', 'numerology']

# Command Construction:
command_args = [
    profile.name,                               # 陈洁玲
    profile.birth_date.strftime('%Y-%m-%d'),   # 1994-04-14
    profile.birth_time.strftime('%I:%M%p').lower(),  # 09:40pm
    profile.birth_location,                     # 汕頭, 廣東
    profile.gender,                            # female
    '--methods'
] + selected_experts  # bazi ziwei astrology numerology

# Final command:
# /fortune-analyze 陈洁玲 1994-04-14 09:40pm "汕頭, 廣東" female --methods bazi ziwei astrology numerology
```

---

## Integration Adapter Implementation

### 1. Adapter Module Structure

```python
# apps/analysis/fortune_adapter.py

import os
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from django.conf import settings
from apps.orders.models import Profile, Order, AnalysisJob, AnalysisReport


class FortuneAnalyzeAdapter:
    """
    Adapter for integrating Django web platform with /fortune-analyze command.
    Converts Django models to command arguments and manages file I/O.
    """

    # Directory where fortune-telling results are stored
    BASE_OUTPUT_DIR = Path(settings.BASE_DIR) / 'data' / 'fortune-telling'

    # Expected output files from /fortune-analyze command
    EXPECTED_FILES = [
        'calculations.json',
        'report.html',  # or index.html
        'synthesis_report.md',
        'bazi_analysis.md',
        'ziwei_analysis.md',
        'astrology_analysis.md',
        'plum_analysis_analysis.md',
        'qimen_analysis.md',
        'liuyao_analysis.md',
        'numerology_analysis.md',
        'name_analysis_analysis.md',
    ]

    def __init__(self, job: AnalysisJob):
        """Initialize adapter with AnalysisJob"""
        self.job = job
        self.order = job.order
        self.profile = self.order.profile

    def build_command_arguments(self) -> List[str]:
        """
        Convert Profile model to /fortune-analyze command arguments.

        Returns:
            List of command arguments ready for subprocess execution
        """
        # Format birth time: 06:00am or 09:40pm
        birth_time_str = self.profile.birth_time.strftime('%I:%M%p').lower()

        # Map selected_experts to method names
        # Note: Command expects method names without '_analysis' suffix
        method_names = []
        for expert in self.order.selected_experts:
            # Map web platform expert names to command method names
            method_map = {
                'bazi': 'bazi',
                'ziwei': 'ziwei',
                'astrology': 'astrology',
                'plum_blossom': 'plum',
                'qimen': 'qimen',
                'liuyao': 'liuyao',
                'numerology': 'numerology',
                'name_analysis': 'name',
            }
            method_names.append(method_map.get(expert, expert))

        # Build argument list
        args = [
            self.profile.name,
            self.profile.birth_date.strftime('%Y-%m-%d'),
            birth_time_str,
            self.profile.birth_location,
            self.profile.gender,
        ]

        # Add methods if specific experts selected (otherwise defaults to 'all')
        if method_names and set(method_names) != {'bazi', 'ziwei', 'astrology', 'plum', 'qimen', 'liuyao', 'numerology', 'name'}:
            args.extend(['--methods'] + method_names)

        return args

    def predict_person_directory(self) -> str:
        """
        Predict the person directory name that /fortune-analyze will create.
        Format: {YYYYMMDD_HHMM_name}

        Returns:
            Directory name (e.g., "19940414_2140_陈洁玲")
        """
        birth_datetime = datetime.combine(
            self.profile.birth_date,
            self.profile.birth_time
        )

        # Format: YYYYMMDD_HHMM
        date_prefix = birth_datetime.strftime('%Y%m%d_%H%M')

        # Combine with name
        person_dir = f"{date_prefix}_{self.profile.name}"

        return person_dir

    def get_person_directory_path(self) -> Path:
        """Get full path to person directory"""
        person_dir = self.predict_person_directory()
        return self.BASE_OUTPUT_DIR / person_dir

    def execute_analysis(self) -> Tuple[bool, str]:
        """
        Execute /fortune-analyze command via Claude Code CLI.

        Returns:
            Tuple of (success: bool, error_message: str)
        """
        try:
            # Build command prompt for Claude Code CLI
            cmd_args = self.build_command_arguments()
            prompt = f"/fortune-analyze {' '.join(cmd_args)}"

            # Predict person directory for tracking
            person_dir = self.predict_person_directory()
            self.job.person_directory = person_dir
            self.job.save(update_fields=['person_directory'])

            # Execute via Claude Code CLI with print mode
            # Using subprocess to call: claude -p "<prompt>"
            result = subprocess.run(
                [
                    'claude',
                    '-p', prompt,
                    '--output-format', 'json',
                    '--max-turns', '15',  # Allow sufficient turns for 3-phase execution
                    '--dangerously-skip-permissions',  # Auto-approve file operations
                ],
                capture_output=True,
                text=True,
                timeout=600,  # 10 minute timeout (command takes ~5-6 minutes)
                cwd=str(settings.BASE_DIR),  # Execute from project root
            )

            # Check execution result
            if result.returncode != 0:
                error_msg = f"Claude CLI failed with exit code {result.returncode}\nStderr: {result.stderr}"
                return False, error_msg

            # Parse JSON output (optional - for debugging)
            try:
                output_data = json.loads(result.stdout)
                # Claude CLI output format may vary - adapt as needed
            except json.JSONDecodeError:
                # Non-JSON output is acceptable - command uses file output
                pass

            # Verify person directory was created
            person_path = self.get_person_directory_path()
            if not person_path.exists():
                return False, f"Person directory not created: {person_path}"

            return True, ""

        except subprocess.TimeoutExpired:
            return False, "Analysis command timed out after 10 minutes"
        except Exception as e:
            return False, f"Execution error: {str(e)}"

    def monitor_file_creation(self, timeout: int = 600) -> Tuple[bool, List[str]]:
        """
        Monitor person directory for expected file creation.

        Args:
            timeout: Maximum seconds to wait for files

        Returns:
            Tuple of (all_files_created: bool, missing_files: List[str])
        """
        person_path = self.get_person_directory_path()
        start_time = time.time()

        while time.time() - start_time < timeout:
            if not person_path.exists():
                time.sleep(5)
                continue

            # Check for files
            missing = []
            for expected_file in self.EXPECTED_FILES:
                file_path = person_path / expected_file

                # Handle report.html OR index.html
                if expected_file == 'report.html':
                    if not file_path.exists():
                        alt_path = person_path / 'index.html'
                        if not alt_path.exists():
                            missing.append(expected_file)
                elif not file_path.exists():
                    # Skip method-specific files if method not selected
                    method_name = expected_file.replace('_analysis.md', '').replace('_analysis_analysis.md', '')
                    if method_name in ['bazi', 'ziwei', 'astrology', 'plum', 'qimen', 'liuyao', 'numerology', 'name']:
                        # Check if this method was selected
                        method_map_reverse = {
                            'bazi': 'bazi',
                            'ziwei': 'ziwei',
                            'astrology': 'astrology',
                            'plum': 'plum_blossom',
                            'qimen': 'qimen',
                            'liuyao': 'liuyao',
                            'numerology': 'numerology',
                            'name': 'name_analysis',
                        }
                        expert_name = method_map_reverse.get(method_name, method_name)
                        if expert_name not in self.order.selected_experts:
                            continue  # Skip this file

                    missing.append(expected_file)

            if not missing:
                return True, []

            time.sleep(10)  # Check every 10 seconds

        return False, missing

    def extract_report_files(self) -> Dict[str, any]:
        """
        Extract all generated files from person directory.

        Returns:
            Dictionary with file contents
        """
        person_path = self.get_person_directory_path()

        data = {
            'calculations_json': {},
            'report_html': '',
            'synthesis_markdown': '',
            'bazi_report': '',
            'ziwei_report': '',
            'astrology_report': '',
            'plum_blossom_report': '',
            'qimen_report': '',
            'liuyao_report': '',
            'numerology_report': '',
            'name_analysis_report': '',
        }

        # Read calculations.json
        calc_path = person_path / 'calculations.json'
        if calc_path.exists():
            with open(calc_path, 'r', encoding='utf-8') as f:
                data['calculations_json'] = json.load(f)

        # Read HTML report (report.html or index.html)
        html_path = person_path / 'report.html'
        if not html_path.exists():
            html_path = person_path / 'index.html'
        if html_path.exists():
            with open(html_path, 'r', encoding='utf-8') as f:
                data['report_html'] = f.read()

        # Read synthesis report
        synthesis_path = person_path / 'synthesis_report.md'
        if synthesis_path.exists():
            with open(synthesis_path, 'r', encoding='utf-8') as f:
                data['synthesis_markdown'] = f.read()

        # Read individual expert reports
        expert_file_map = {
            'bazi_analysis.md': 'bazi_report',
            'ziwei_analysis.md': 'ziwei_report',
            'astrology_analysis.md': 'astrology_report',
            'plum_analysis_analysis.md': 'plum_blossom_report',
            'qimen_analysis.md': 'qimen_report',
            'liuyao_analysis.md': 'liuyao_report',
            'numerology_analysis.md': 'numerology_report',
            'name_analysis_analysis.md': 'name_analysis_report',
        }

        for filename, field_name in expert_file_map.items():
            file_path = person_path / filename
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    data[field_name] = f.read()

        return data

    def save_to_database(self, report_data: Dict[str, any]) -> AnalysisReport:
        """
        Save extracted report data to AnalysisReport model.

        Args:
            report_data: Dictionary from extract_report_files()

        Returns:
            Created AnalysisReport instance
        """
        report, created = AnalysisReport.objects.update_or_create(
            job=self.job,
            defaults={
                'report_html': report_data['report_html'],
                'synthesis_markdown': report_data['synthesis_markdown'],
                'calculations_json': report_data['calculations_json'],
                'bazi_report': report_data['bazi_report'],
                'ziwei_report': report_data['ziwei_report'],
                'astrology_report': report_data['astrology_report'],
                'plum_blossom_report': report_data['plum_blossom_report'],
                'qimen_report': report_data['qimen_report'],
                'liuyao_report': report_data['liuyao_report'],
                'numerology_report': report_data['numerology_report'],
                'name_analysis_report': report_data['name_analysis_report'],
            }
        )

        return report

    def cleanup_files(self, keep_files: bool = True):
        """
        Optionally cleanup person directory after successful DB save.

        Args:
            keep_files: If True, keep files on disk; if False, delete them
        """
        if not keep_files:
            person_path = self.get_person_directory_path()
            if person_path.exists():
                import shutil
                shutil.rmtree(person_path)
```

---

## Celery Task Integration

### 2. Celery Task Wrapper

```python
# apps/analysis/tasks.py

import logging
from datetime import datetime
from celery import shared_task
from django.utils import timezone

from apps.orders.models import AnalysisJob, Order
from .fortune_adapter import FortuneAnalyzeAdapter

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def execute_fortune_analysis(self, job_id: int):
    """
    Celery task to execute /fortune-analyze command and save results.

    Args:
        job_id: AnalysisJob.id
    """
    try:
        # Get job and update status
        job = AnalysisJob.objects.select_related('order', 'order__profile').get(id=job_id)
        job.status = 'processing'
        job.started_at = timezone.now()
        job.celery_task_id = self.request.id
        job.save()

        # Update order status
        job.order.status = 'processing'
        job.order.save()

        # Initialize adapter
        adapter = FortuneAnalyzeAdapter(job)

        logger.info(f"Starting fortune analysis for job {job_id}, order {job.order.id}")

        # Execute analysis command
        success, error_msg = adapter.execute_analysis()

        if not success:
            logger.error(f"Analysis execution failed for job {job_id}: {error_msg}")
            raise Exception(error_msg)

        logger.info(f"Analysis command completed for job {job_id}, monitoring file creation...")

        # Monitor file creation (with 10 minute timeout)
        files_created, missing_files = adapter.monitor_file_creation(timeout=600)

        if not files_created:
            error_msg = f"Not all files were created. Missing: {missing_files}"
            logger.error(f"File creation incomplete for job {job_id}: {error_msg}")
            raise Exception(error_msg)

        logger.info(f"All files created for job {job_id}, extracting report data...")

        # Extract report files
        report_data = adapter.extract_report_files()

        # Save to database
        report = adapter.save_to_database(report_data)

        logger.info(f"Report saved to database for job {job_id}, report ID {report.id}")

        # Update job status
        job.status = 'completed'
        job.completed_at = timezone.now()
        job.current_phase = 3  # All phases complete
        job.save()

        # Update order status
        job.order.status = 'completed'
        job.order.save()

        # Optional: cleanup files from disk (keep by default)
        # adapter.cleanup_files(keep_files=True)

        logger.info(f"Fortune analysis completed successfully for job {job_id}")

        # Send notification email
        from .notifications import send_analysis_ready_email
        send_analysis_ready_email(job.order)

        return {
            'success': True,
            'job_id': job_id,
            'report_id': report.id,
            'person_directory': job.person_directory,
        }

    except AnalysisJob.DoesNotExist:
        logger.error(f"AnalysisJob {job_id} not found")
        return {'success': False, 'error': 'Job not found'}

    except Exception as e:
        logger.exception(f"Error in execute_fortune_analysis for job {job_id}: {str(e)}")

        # Update job status to failed
        try:
            job = AnalysisJob.objects.get(id=job_id)
            job.status = 'failed'
            job.error_message = str(e)
            job.retry_count += 1
            job.save()

            # Update order status
            job.order.status = 'failed'
            job.order.save()
        except:
            pass

        # Retry if not exceeded max retries
        if self.request.retries < self.max_retries:
            logger.info(f"Retrying fortune analysis for job {job_id}, attempt {self.request.retries + 1}")
            raise self.retry(exc=e, countdown=60 * (self.request.retries + 1))  # Exponential backoff

        return {'success': False, 'error': str(e)}
```

---

## Progress Tracking Enhancement

### 3. Phase Monitoring (Optional Enhancement)

Since `/fortune-analyze` executes in 3 phases, we can enhance the adapter to monitor phase progress:

```python
# apps/analysis/fortune_adapter.py (enhancement)

class FortuneAnalyzeAdapter:
    # ... existing code ...

    def monitor_phase_progress(self, callback=None):
        """
        Monitor the 3-phase execution progress by checking file creation.

        Args:
            callback: Optional function to call on phase completion
                     Signature: callback(phase: int, job: AnalysisJob)
        """
        person_path = self.get_person_directory_path()

        # Phase 1 completion indicators: bazi, ziwei, astrology .md files
        phase1_files = ['bazi_analysis.md', 'ziwei_analysis.md', 'astrology_analysis.md']

        # Phase 2 completion indicators: plum, qimen, liuyao .md files
        phase2_files = ['plum_analysis_analysis.md', 'qimen_analysis.md', 'liuyao_analysis.md']

        # Phase 3 completion indicators: numerology, name, synthesis .md files
        phase3_files = ['numerology_analysis.md', 'name_analysis_analysis.md', 'synthesis_report.md']

        current_phase = 0

        while current_phase < 3:
            time.sleep(15)  # Check every 15 seconds

            if not person_path.exists():
                continue

            # Check phase 1
            if current_phase == 0:
                if all((person_path / f).exists() for f in phase1_files if self._should_check_file(f)):
                    current_phase = 1
                    self.job.current_phase = 1
                    self.job.save(update_fields=['current_phase'])
                    if callback:
                        callback(1, self.job)
                    logger.info(f"Job {self.job.id} completed phase 1")

            # Check phase 2
            if current_phase == 1:
                if all((person_path / f).exists() for f in phase2_files if self._should_check_file(f)):
                    current_phase = 2
                    self.job.current_phase = 2
                    self.job.save(update_fields=['current_phase'])
                    if callback:
                        callback(2, self.job)
                    logger.info(f"Job {self.job.id} completed phase 2")

            # Check phase 3
            if current_phase == 2:
                if all((person_path / f).exists() for f in phase3_files if self._should_check_file(f)):
                    current_phase = 3
                    self.job.current_phase = 3
                    self.job.save(update_fields=['current_phase'])
                    if callback:
                        callback(3, self.job)
                    logger.info(f"Job {self.job.id} completed phase 3")
                    break

    def _should_check_file(self, filename: str) -> bool:
        """Check if file should be expected based on selected experts"""
        method_name = filename.replace('_analysis.md', '').replace('_analysis_analysis.md', '')

        if method_name == 'synthesis_report':
            return True  # Always expect synthesis

        method_map_reverse = {
            'bazi': 'bazi',
            'ziwei': 'ziwei',
            'astrology': 'astrology',
            'plum': 'plum_blossom',
            'qimen': 'qimen',
            'liuyao': 'liuyao',
            'numerology': 'numerology',
            'name': 'name_analysis',
        }

        expert_name = method_map_reverse.get(method_name, method_name)
        return expert_name in self.order.selected_experts
```

---

## User-Facing Status Display

### 4. API Endpoint for Progress

```python
# apps/analysis/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.orders.models import AnalysisJob


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def job_status(request, job_id):
    """
    Get current status of analysis job.

    Returns:
        {
            'status': 'processing',
            'current_phase': 2,
            'total_phases': 3,
            'progress_percentage': 66,
            'estimated_remaining_seconds': 120,
            'error_message': null
        }
    """
    try:
        job = AnalysisJob.objects.select_related('order').get(
            id=job_id,
            order__user=request.user
        )

        # Calculate progress
        progress_map = {
            'queued': 0,
            'processing': (job.current_phase / 3) * 100 if job.current_phase > 0 else 10,
            'completed': 100,
            'failed': 0,
        }

        progress = progress_map.get(job.status, 0)

        # Estimate remaining time (rough estimate: ~2 minutes per phase)
        remaining_phases = 3 - job.current_phase
        estimated_remaining = remaining_phases * 120  # 120 seconds per phase

        return Response({
            'status': job.status,
            'current_phase': job.current_phase,
            'total_phases': 3,
            'progress_percentage': int(progress),
            'estimated_remaining_seconds': estimated_remaining if job.status == 'processing' else 0,
            'error_message': job.error_message if job.status == 'failed' else None,
            'started_at': job.started_at.isoformat() if job.started_at else None,
            'completed_at': job.completed_at.isoformat() if job.completed_at else None,
        })

    except AnalysisJob.DoesNotExist:
        return Response({'error': 'Job not found'}, status=404)
```

---

## Testing Strategy

### 5. Manual Testing Procedure

```bash
# 1. Create test profile and order in Django shell
python manage.py shell

from apps.orders.models import Profile, Order, AnalysisJob
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.first()

# Create test profile
profile = Profile.objects.create(
    user=user,
    name='TestUser',
    birth_date='1990-01-15',
    birth_time='14:30:00',
    birth_location='Taipei, Taiwan',
    gender='male'
)

# Create test order
order = Order.objects.create(
    user=user,
    profile=profile,
    selected_experts=['bazi', 'ziwei', 'astrology'],
    total_price=24.99,
    status='paid'
)

# Create analysis job
job = AnalysisJob.objects.create(
    order=order,
    status='queued'
)

print(f"Created job ID: {job.id}")
exit()

# 2. Trigger Celery task manually
python manage.py shell

from apps.analysis.tasks import execute_fortune_analysis
from apps.orders.models import AnalysisJob

job = AnalysisJob.objects.last()
result = execute_fortune_analysis.delay(job.id)

print(f"Task ID: {result.id}")
print(f"Task state: {result.state}")
exit()

# 3. Monitor progress
python manage.py shell

from apps.orders.models import AnalysisJob

job = AnalysisJob.objects.last()
print(f"Status: {job.status}")
print(f"Current phase: {job.current_phase}")
print(f"Person directory: {job.person_directory}")

# Check if files exist
from pathlib import Path
person_path = Path(settings.BASE_DIR) / 'data' / 'fortune-telling' / job.person_directory
if person_path.exists():
    files = list(person_path.glob('*'))
    print(f"Files created: {[f.name for f in files]}")
exit()

# 4. Verify report in database
python manage.py shell

from apps.orders.models import AnalysisJob, AnalysisReport

job = AnalysisJob.objects.last()
report = AnalysisReport.objects.get(job=job)

print(f"HTML report length: {len(report.report_html)}")
print(f"Calculations: {report.calculations_json.keys()}")
print(f"Bazi report length: {len(report.bazi_report)}")
exit()
```

---

## Configuration

### 6. Django Settings

```python
# settings.py

# Fortune-telling configuration
FORTUNE_ANALYSIS_BASE_DIR = BASE_DIR / 'data' / 'fortune-telling'

# Celery configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 900  # 15 minutes max per task
CELERY_TASK_SOFT_TIME_LIMIT = 600  # 10 minutes soft limit

# Create fortune-telling directory if not exists
FORTUNE_ANALYSIS_BASE_DIR.mkdir(parents=True, exist_ok=True)
```

---

## Error Handling & Recovery

### 7. Failure Scenarios

| Scenario | Detection | Recovery Strategy |
|----------|-----------|-------------------|
| Claude CLI timeout | `subprocess.TimeoutExpired` | Retry with increased timeout |
| Command execution failure | `returncode != 0` | Log stderr, retry up to 3 times |
| Person directory not created | `person_path.exists() == False` | Mark as failed, notify support |
| Incomplete file generation | `missing_files != []` | Wait longer, then retry |
| File read errors | `OSError` exceptions | Retry file read, check permissions |
| Database save errors | `IntegrityError` | Log error, mark job as failed |
| Celery worker crash | Task stuck in processing | Monitoring system detects, restarts task |

### 8. Monitoring & Alerts

```python
# apps/analysis/monitoring.py

from django.utils import timezone
from datetime import timedelta
from apps.orders.models import AnalysisJob


def check_stuck_jobs():
    """
    Find jobs stuck in 'processing' state for >15 minutes.
    Should be run via cron or Celery beat.
    """
    threshold = timezone.now() - timedelta(minutes=15)

    stuck_jobs = AnalysisJob.objects.filter(
        status='processing',
        started_at__lt=threshold
    )

    for job in stuck_jobs:
        # Alert admins
        logger.error(f"Job {job.id} stuck in processing for >15 minutes")

        # Optionally retry
        from .tasks import execute_fortune_analysis
        execute_fortune_analysis.apply_async(args=[job.id], countdown=60)
```

---

## Summary

This integration adapter provides:

✅ **Zero Changes to `/fortune-analyze` Command**: Command remains unchanged
✅ **Clean Abstraction**: `FortuneAnalyzeAdapter` handles all integration logic
✅ **Robust Error Handling**: Retry logic, timeout management, file monitoring
✅ **Progress Tracking**: 3-phase progress updates for user visibility
✅ **Database Persistence**: All reports stored in Django models
✅ **Async Processing**: Celery task queue for background execution
✅ **Monitoring**: Health checks and stuck job detection

**Next Steps**:
1. Implement `FortuneAnalyzeAdapter` class
2. Create Celery task `execute_fortune_analysis`
3. Build API endpoint for progress tracking
4. Test end-to-end flow with sample data
5. Deploy monitoring and alerting system

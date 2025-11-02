# Batch Job Queue Architecture for Fortune-Telling Analysis

**Purpose**: Process fortune-telling analysis requests offline using Claude Code CLI with job queue system

**Approach**: Users submit requests → queued → background workers process via CLI → notify when complete

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Request Flow                        │
└─────────────────────────────────────────────────────────────┘

User Form Submit
      ↓
Django View (create order + job)
      ↓
Save to PostgreSQL (order, job record)
      ↓
Enqueue Celery Task → Redis Queue
      ↓
Return "Processing..." page to user
      ↓
Email: "Your analysis has been queued"


┌─────────────────────────────────────────────────────────────┐
│                  Background Processing                       │
└─────────────────────────────────────────────────────────────┘

Celery Worker picks up job
      ↓
Update job status: "processing"
      ↓
Prepare input data file (birth info, selected experts)
      ↓
Execute: claude /fortune-analyze @input.json
      ↓
Wait for Claude Code to complete (30-120 sec)
      ↓
Parse output, save HTML report
      ↓
Update job status: "completed"
      ↓
Email: "Your analysis is ready!"


┌─────────────────────────────────────────────────────────────┐
│                     Error Handling                           │
└─────────────────────────────────────────────────────────────┘

Claude Code CLI fails
      ↓
Retry logic (max 3 attempts)
      ↓
Still fails?
      ↓
Update job status: "failed"
      ↓
Email: "We're reviewing your request"
      ↓
Admin notification for manual intervention
```

---

## Database Schema

```python
# models.py

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """User birth profile"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    birth_time = models.TimeField(null=True, blank=True)
    birth_location = models.CharField(max_length=200)
    timezone = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class Package(models.Model):
    """Pre-defined analysis packages"""
    name = models.CharField(max_length=100)  # e.g., "Popular Trio"
    slug = models.SlugField(unique=True)
    description = models.TextField()
    experts = models.JSONField()  # List of expert systems
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=True)

class Order(models.Model):
    """Purchase order"""
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('paid', 'Payment Confirmed'),
        ('processing', 'Analysis in Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True)
    selected_experts = models.JSONField()  # List of expert systems
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Payment info
    payment_method = models.CharField(max_length=50)
    payment_id = models.CharField(max_length=200, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.email} - {self.status}"

class AnalysisJob(models.Model):
    """Background job for analysis generation"""
    STATUS_CHOICES = [
        ('queued', 'Queued'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('retry', 'Retrying'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='analysis_job')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='queued')

    # Job execution details
    celery_task_id = models.CharField(max_length=255, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Retry management
    retry_count = models.IntegerField(default=0)
    max_retries = models.IntegerField(default=3)

    # Output data
    input_data = models.JSONField()  # Birth info + selected experts
    output_path = models.CharField(max_length=500, blank=True)  # Path to generated report
    error_message = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Job {self.id} - Order {self.order.id} - {self.status}"

class AnalysisReport(models.Model):
    """Completed analysis report"""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='report')

    # Report content
    html_content = models.TextField()
    pdf_path = models.CharField(max_length=500, blank=True)

    # Metadata
    experts_included = models.JSONField()
    generation_time = models.DurationField()  # How long it took to generate

    # Access tracking
    view_count = models.IntegerField(default=0)
    last_viewed = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for Order {self.order.id}"
```

---

## Celery Task Implementation

```python
# tasks.py

import subprocess
import json
import os
from datetime import datetime, timedelta
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from .models import AnalysisJob, AnalysisReport, Order

@shared_task(bind=True, max_retries=3)
def generate_fortune_analysis(self, job_id):
    """
    Background task to generate fortune analysis using Claude Code CLI

    Args:
        job_id: AnalysisJob instance ID
    """
    job = AnalysisJob.objects.get(id=job_id)
    order = job.order

    try:
        # Update job status
        job.status = 'processing'
        job.started_at = datetime.now()
        job.celery_task_id = self.request.id
        job.save()

        # Update order status
        order.status = 'processing'
        order.save()

        # Prepare input data file
        input_file_path = prepare_input_file(job)

        # Execute Claude Code CLI command
        output_path = execute_claude_analysis(input_file_path, job)

        # Parse and save results
        report = save_analysis_report(output_path, job, order)

        # Update job status
        job.status = 'completed'
        job.completed_at = datetime.now()
        job.output_path = output_path
        job.save()

        # Update order status
        order.status = 'completed'
        order.save()

        # Send completion email
        send_completion_email(order, report)

        return {'status': 'success', 'job_id': job_id, 'order_id': order.id}

    except Exception as e:
        # Handle failure
        job.retry_count += 1
        job.error_message = str(e)

        if job.retry_count < job.max_retries:
            # Retry with exponential backoff
            job.status = 'retry'
            job.save()

            countdown = 60 * (2 ** job.retry_count)  # 60s, 120s, 240s
            raise self.retry(exc=e, countdown=countdown)
        else:
            # Max retries exceeded
            job.status = 'failed'
            job.save()

            order.status = 'failed'
            order.save()

            # Send failure notification
            send_failure_email(order, str(e))
            notify_admin_of_failure(job)

            return {'status': 'failed', 'job_id': job_id, 'error': str(e)}


def prepare_input_file(job):
    """
    Create input JSON file for Claude Code CLI

    Returns:
        str: Path to input file
    """
    profile = job.order.profile

    # Create input data structure
    input_data = {
        'name': profile.name,
        'birth_date': profile.birth_date.isoformat(),
        'birth_time': profile.birth_time.isoformat() if profile.birth_time else None,
        'birth_location': profile.birth_location,
        'timezone': profile.timezone,
        'selected_experts': job.input_data['selected_experts'],
        'order_id': job.order.id,
        'job_id': job.id
    }

    # Create temp directory if needed
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_jobs')
    os.makedirs(temp_dir, exist_ok=True)

    # Write input file
    input_file_path = os.path.join(temp_dir, f'job_{job.id}_input.json')
    with open(input_file_path, 'w') as f:
        json.dump(input_data, f, indent=2)

    return input_file_path


def execute_claude_analysis(input_file_path, job):
    """
    Execute Claude Code CLI to generate analysis

    Args:
        input_file_path: Path to input JSON
        job: AnalysisJob instance

    Returns:
        str: Path to output HTML file
    """
    output_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, f'report_{job.order.id}.html')

    # Construct Claude Code CLI command
    # Assuming you have a /fortune-analyze command that accepts input file
    cmd = [
        'claude',
        '/fortune-analyze',
        f'--input={input_file_path}',
        f'--output={output_file}',
        '--format=html'
    ]

    # Execute with timeout
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minutes max
            cwd=settings.BASE_DIR,
            env=os.environ.copy()
        )

        if result.returncode != 0:
            raise Exception(f"Claude Code failed: {result.stderr}")

        # Verify output file exists
        if not os.path.exists(output_file):
            raise Exception(f"Output file not generated: {output_file}")

        return output_file

    except subprocess.TimeoutExpired:
        raise Exception("Analysis generation timed out after 5 minutes")
    except Exception as e:
        raise Exception(f"Failed to execute Claude Code: {str(e)}")


def save_analysis_report(output_path, job, order):
    """
    Save generated report to database

    Args:
        output_path: Path to HTML report
        job: AnalysisJob instance
        order: Order instance

    Returns:
        AnalysisReport instance
    """
    # Read HTML content
    with open(output_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Calculate generation time
    generation_time = job.completed_at - job.started_at if job.completed_at else timedelta(0)

    # Create report record
    report = AnalysisReport.objects.create(
        order=order,
        html_content=html_content,
        pdf_path='',  # Optional: convert to PDF later
        experts_included=job.input_data['selected_experts'],
        generation_time=generation_time
    )

    return report


def send_completion_email(order, report):
    """Send email notification when analysis is ready"""
    subject = f"Your Fortune Analysis is Ready! (Order #{order.id})"
    message = f"""
    Hello {order.user.first_name or order.user.email},

    Great news! Your fortune analysis has been completed and is ready to view.

    Order Details:
    - Order ID: #{order.id}
    - Analysis Type: {', '.join(order.selected_experts)}
    - Generated: {report.created_at.strftime('%Y-%m-%d %H:%M')}

    View Your Analysis:
    {settings.SITE_URL}/dashboard/orders/{order.id}/

    Thank you for using our service!

    Best regards,
    Fortune Analysis Team
    """

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.user.email],
        fail_silently=True
    )


def send_failure_email(order, error):
    """Notify user of analysis failure"""
    subject = f"Issue with Your Analysis (Order #{order.id})"
    message = f"""
    Hello {order.user.first_name or order.user.email},

    We encountered an issue while generating your fortune analysis.

    Order ID: #{order.id}

    Our team has been notified and is working to resolve this.
    We'll have your analysis ready within 24 hours.

    If you have any questions, please reply to this email.

    We apologize for the inconvenience.

    Best regards,
    Fortune Analysis Team
    """

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.user.email],
        fail_silently=True
    )


def notify_admin_of_failure(job):
    """Send admin notification for failed jobs"""
    subject = f"[ALERT] Analysis Job Failed - Job #{job.id}"
    message = f"""
    Analysis job failed after {job.retry_count} retries.

    Job ID: {job.id}
    Order ID: {job.order.id}
    User: {job.order.user.email}
    Error: {job.error_message}

    Please review and process manually.
    """

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMIN_EMAIL],
        fail_silently=True
    )
```

---

## Django Views

```python
# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, Package, Profile, AnalysisJob
from .tasks import generate_fortune_analysis
from .forms import ProfileForm, CheckoutForm

def marketplace(request):
    """Display available packages and individual experts"""
    packages = Package.objects.filter(is_active=True)

    context = {
        'packages': packages,
        'individual_experts': [
            {'name': 'Bazi (八字)', 'price': 9.99, 'slug': 'bazi'},
            {'name': 'Ziwei (紫微)', 'price': 9.99, 'slug': 'ziwei'},
            {'name': 'Astrology (占星)', 'price': 9.99, 'slug': 'astrology'},
            {'name': 'Numerology (生命靈數)', 'price': 9.99, 'slug': 'numerology'},
            {'name': 'Name Analysis (姓名學)', 'price': 9.99, 'slug': 'name'},
            {'name': 'Plum Blossom (梅花易數)', 'price': 9.99, 'slug': 'plum'},
            {'name': 'Qimen (奇門遁甲)', 'price': 9.99, 'slug': 'qimen'},
            {'name': 'Liuyao (六爻)', 'price': 9.99, 'slug': 'liuyao'},
        ]
    }

    return render(request, 'marketplace.html', context)


@login_required
def checkout(request, package_slug=None):
    """Checkout flow - collect profile data and process payment"""

    if package_slug:
        package = get_object_or_404(Package, slug=package_slug)
        selected_experts = package.experts
        total_price = package.price
    else:
        # Custom selection from session cart
        selected_experts = request.session.get('cart_experts', [])
        total_price = len(selected_experts) * 9.99  # Simple pricing

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST)

        if profile_form.is_valid():
            # Save profile
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()

            # Create order
            order = Order.objects.create(
                user=request.user,
                profile=profile,
                package=package if package_slug else None,
                selected_experts=selected_experts,
                total_price=total_price,
                status='pending'
            )

            # For now, skip actual payment (internal testing)
            # In production, integrate Stripe here

            # Simulate payment confirmation
            order.status = 'paid'
            order.payment_method = 'test'
            order.save()

            # Create analysis job
            job = AnalysisJob.objects.create(
                order=order,
                input_data={
                    'selected_experts': selected_experts,
                    'profile_id': profile.id
                }
            )

            # Queue background job
            task = generate_fortune_analysis.delay(job.id)
            job.celery_task_id = task.id
            job.save()

            messages.success(request, 'Order placed! Your analysis is being generated.')
            return redirect('order_status', order_id=order.id)
    else:
        profile_form = ProfileForm()

    context = {
        'profile_form': profile_form,
        'selected_experts': selected_experts,
        'total_price': total_price,
        'package': package if package_slug else None
    }

    return render(request, 'checkout.html', context)


@login_required
def order_status(request, order_id):
    """Display order and job status"""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    try:
        job = order.analysis_job
    except AnalysisJob.DoesNotExist:
        job = None

    context = {
        'order': order,
        'job': job
    }

    return render(request, 'order_status.html', context)


@login_required
def view_report(request, order_id):
    """View completed analysis report"""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status != 'completed':
        messages.warning(request, 'Your analysis is still being generated.')
        return redirect('order_status', order_id=order.id)

    try:
        report = order.report

        # Track view count
        report.view_count += 1
        report.last_viewed = datetime.now()
        report.save()

        context = {
            'order': order,
            'report': report
        }

        return render(request, 'report_view.html', context)

    except AnalysisReport.DoesNotExist:
        messages.error(request, 'Report not found.')
        return redirect('dashboard')


@login_required
def dashboard(request):
    """User dashboard showing all orders and analyses"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'orders': orders
    }

    return render(request, 'dashboard.html', context)
```

---

## Configuration

```python
# settings.py

import os
from pathlib import Path

# ... existing settings ...

# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Task routing
CELERY_TASK_ROUTES = {
    'fortune.tasks.generate_fortune_analysis': {'queue': 'analysis'},
}

# Media files (for reports)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Site URL for email links
SITE_URL = 'http://localhost:8000'  # Change in production

# Admin email for alerts
ADMIN_EMAIL = 'admin@example.com'

# Email configuration (use SendGrid, Mailgun, etc in production)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # For testing
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # For production
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'Fortune Analysis <noreply@fortune-analysis.com>'
```

```python
# celery.py (in project root)

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fortune_saas.settings')

app = Celery('fortune_saas')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
```

```python
# __init__.py (in project root)

from .celery import app as celery_app

__all__ = ('celery_app',)
```

---

## Deployment on Linode

```bash
# 1. Install dependencies on Linode server
sudo apt update
sudo apt install -y python3-pip python3-venv postgresql redis-server nginx

# 2. Create project directory
mkdir -p /var/www/fortune-saas
cd /var/www/fortune-saas

# 3. Set up Python virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Install Python packages
pip install django djangorestframework celery redis psycopg2-binary gunicorn

# 5. Install Claude Code CLI (if not already)
npm install -g @anthropic-ai/claude-code

# 6. Set up PostgreSQL database
sudo -u postgres createdb fortune_saas
sudo -u postgres createuser fortune_user -P

# 7. Configure Django
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic

# 8. Start services

# Redis (should auto-start)
sudo systemctl enable redis-server
sudo systemctl start redis-server

# Celery worker (create systemd service)
sudo nano /etc/systemd/system/celery-worker.service
```

```ini
# /etc/systemd/system/celery-worker.service
[Unit]
Description=Celery Worker for Fortune Analysis
After=network.target redis.target

[Service]
Type=forking
User=www-data
Group=www-data
WorkingDirectory=/var/www/fortune-saas
Environment="PATH=/var/www/fortune-saas/venv/bin"
ExecStart=/var/www/fortune-saas/venv/bin/celery -A fortune_saas worker \
    -Q analysis \
    --loglevel=info \
    --logfile=/var/log/celery/worker.log \
    --pidfile=/var/run/celery/worker.pid

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start Celery
sudo systemctl enable celery-worker
sudo systemctl start celery-worker

# Check status
sudo systemctl status celery-worker
sudo tail -f /var/log/celery/worker.log
```

---

## Monitoring & Management

```python
# admin.py

from django.contrib import admin
from .models import Profile, Package, Order, AnalysisJob, AnalysisReport

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__email', 'id']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(AnalysisJob)
class AnalysisJobAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'status', 'retry_count', 'created_at', 'completed_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order__id', 'celery_task_id']
    readonly_fields = ['created_at', 'updated_at']

    actions = ['retry_failed_jobs']

    def retry_failed_jobs(self, request, queryset):
        """Admin action to retry failed jobs"""
        for job in queryset.filter(status='failed'):
            job.retry_count = 0
            job.status = 'queued'
            job.save()

            from .tasks import generate_fortune_analysis
            generate_fortune_analysis.delay(job.id)

        self.message_user(request, f'{queryset.count()} jobs queued for retry')

    retry_failed_jobs.short_description = 'Retry selected failed jobs'

@admin.register(AnalysisReport)
class AnalysisReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'generation_time', 'view_count', 'created_at']
    search_fields = ['order__id', 'order__user__email']
    readonly_fields = ['created_at']
```

---

## Testing the System

```bash
# 1. Start Django development server
python manage.py runserver

# 2. Start Celery worker (separate terminal)
celery -A fortune_saas worker -Q analysis --loglevel=info

# 3. Monitor Redis queue (optional - separate terminal)
redis-cli monitor

# 4. Test the flow:
# - Register a user
# - Browse marketplace
# - Select package and checkout
# - Fill birth profile data
# - Submit order
# - Check job status page (should show "processing")
# - Wait for completion email
# - View completed report

# 5. Monitor Celery tasks
celery -A fortune_saas inspect active  # See active tasks
celery -A fortune_saas inspect stats   # Worker stats
```

---

## Next Steps

1. **Test with sample data**
   - Create test order via Django admin
   - Manually trigger Celery task
   - Verify Claude Code CLI execution

2. **Refine `/fortune-analyze` command**
   - Ensure it accepts JSON input file
   - Returns HTML output to specified path
   - Handles errors gracefully

3. **Add monitoring dashboard**
   - Real-time job status updates via AJAX
   - Progress indicator
   - Queue length visibility

4. **Implement payment integration**
   - Stripe test mode first
   - Webhook handlers for payment confirmation
   - Queue job ONLY after payment verified

5. **Production deployment**
   - Nginx reverse proxy
   - Gunicorn WSGI server
   - SSL certificate
   - Monitoring (Sentry, New Relic)

---

## Cost & Performance Estimates

```yaml
Processing Capacity:
  Single Worker: 2-3 analyses per minute
  Multiple Workers: Scale linearly (3 workers = 6-9/min)

Queue Management:
  Redis: Can handle thousands of queued jobs
  PostgreSQL: Efficiently stores job metadata

Peak Load Handling:
  10 orders/hour: Single worker handles easily
  100 orders/hour: Need 3-5 workers

Resource Usage:
  Per Worker: ~200MB RAM, 0.5 CPU cores
  Redis: ~50MB RAM
  PostgreSQL: ~100MB RAM base

Linode Sizing:
  Shared CPU 2GB: Handles 1-2 workers (10-20 orders/hour)
  Dedicated 4GB: Handles 4-6 workers (50+ orders/hour)
```

This architecture gives you a solid foundation for batch processing with Claude Code CLI while keeping the system maintainable and scalable for internal testing!

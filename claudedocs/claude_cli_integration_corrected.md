# Claude Code CLI Integration - Corrected Implementation

**Based on**: Official Claude Code CLI documentation and real-world usage patterns

**Key Finding**: Claude Code CLI does **NOT** have `--input` or `--output` flags. Instead, it uses:
- **Input**: stdin piping or inline prompts
- **Output**: stdout (can be redirected to files)
- **Print mode**: `-p` flag for non-interactive execution
- **Output format**: `--output-format json` for structured data

---

## Corrected Architecture

### How Claude Code CLI Actually Works

```bash
# ❌ WRONG (doesn't exist)
claude /fortune-analyze --input=data.json --output=report.html

# ✅ CORRECT (actual Claude Code CLI syntax)
cat data.json | claude -p "Analyze this birth data and generate fortune-telling report" --output-format json > output.json
```

### Three Approaches for Integration

#### **Approach 1: Custom Slash Command (Recommended for Testing)**

Create `.claude/commands/fortune-analyze.md`:

```markdown
---
command: /fortune-analyze
category: Fortune Telling
---

# Fortune Analysis Command

Read birth data from the provided JSON and generate comprehensive fortune-telling analysis.

## Input Format Expected

The $ARGUMENTS should contain a path to JSON file with:
```json
{
  "name": "User Name",
  "birth_date": "1972-01-17",
  "birth_time": "06:00:00",
  "birth_location": "Taipei, Taiwan",
  "timezone": "Asia/Taipei",
  "selected_experts": ["bazi", "ziwei", "astrology"]
}
```

## Analysis Process

1. Read the input file: `@$ARGUMENTS`
2. Extract birth data and selected expert systems
3. For each selected expert:
   - Run calculation scripts from `scripts/fortune_telling/`
   - Generate interpretation using expert system
4. Create comprehensive HTML report combining all analyses
5. Save the report to the output path specified

## Expected Output

Generate a complete HTML report with:
- Professional styling
- Charts and visualizations for each system
- Synthesis section combining insights
- Personalized narrative based on birth data

Save the report to: `data/fortune-telling/reports/report_ORDER_ID.html`

Return JSON summary:
```json
{
  "status": "success",
  "report_path": "data/fortune-telling/reports/report_123.html",
  "experts_analyzed": ["bazi", "ziwei", "astrology"],
  "generation_time": "45 seconds"
}
```
```

**Usage**:
```bash
# Interactive mode (for testing)
claude /fortune-analyze input.json

# Print mode (for automation)
claude -p "/fortune-analyze input.json" --output-format json > result.json
```

#### **Approach 2: Piped Input with Prompt (Simple Integration)**

```python
# tasks.py - Updated Celery task

def execute_claude_analysis(input_data, job):
    """
    Execute Claude Code via stdin piping
    """
    import subprocess
    import json

    # Prepare input JSON
    input_json = json.dumps(input_data, indent=2)

    # Construct prompt
    prompt = f"""
    Analyze this fortune-telling request and generate a comprehensive HTML report.

    Birth Data: {input_json}

    Requirements:
    1. Run analysis for these expert systems: {input_data['selected_experts']}
    2. Use existing Python calculation scripts in scripts/fortune_telling/
    3. Generate professional HTML report with visualizations
    4. Save to: data/fortune-telling/reports/report_{job.order.id}.html

    Return JSON summary with status, report_path, and generation_time.
    """

    # Execute Claude Code CLI
    try:
        result = subprocess.run(
            ['claude', '-p', prompt, '--output-format', 'json'],
            input=input_json,
            capture_output=True,
            text=True,
            timeout=300,
            cwd=settings.BASE_DIR
        )

        if result.returncode != 0:
            raise Exception(f"Claude Code failed: {result.stderr}")

        # Parse JSON response
        response = json.loads(result.stdout)

        if response.get('status') != 'success':
            raise Exception(f"Analysis failed: {response.get('error')}")

        return response.get('report_path')

    except subprocess.TimeoutExpired:
        raise Exception("Analysis timed out after 5 minutes")
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse Claude response: {e}")
    except Exception as e:
        raise Exception(f"Claude Code execution failed: {str(e)}")
```

#### **Approach 3: File-Based with Redirection (Most Robust)**

```python
# tasks.py - File-based approach

def execute_claude_analysis_file_based(input_file_path, job):
    """
    Execute Claude Code with file input and output redirection
    """
    import subprocess
    import os

    output_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, f'report_{job.order.id}.html')
    json_output_file = os.path.join(output_dir, f'report_{job.order.id}.json')

    # Construct comprehensive prompt
    prompt = f"""
    Generate fortune-telling analysis report from the input file.

    Instructions:
    1. Read birth data from: {input_file_path}
    2. Use Python scripts in scripts/fortune_telling/ for calculations
    3. Generate HTML report with all visualizations
    4. Save HTML to: {output_file}
    5. Return JSON summary

    The input file contains birth data and selected expert systems.
    """

    try:
        # Method 1: Cat file into Claude
        with open(input_file_path, 'r') as f:
            input_content = f.read()

        result = subprocess.run(
            ['claude', '-p', prompt, '--output-format', 'json'],
            input=input_content,
            capture_output=True,
            text=True,
            timeout=300,
            cwd=settings.BASE_DIR,
            env=os.environ.copy()
        )

        if result.returncode != 0:
            raise Exception(f"Claude failed: {result.stderr}")

        # Save JSON response
        with open(json_output_file, 'w') as f:
            f.write(result.stdout)

        # Parse response
        response = json.loads(result.stdout)

        # Verify HTML report was created
        if not os.path.exists(output_file):
            raise Exception(f"HTML report not generated at: {output_file}")

        return output_file

    except Exception as e:
        raise Exception(f"Analysis generation failed: {str(e)}")
```

---

## Updated Celery Task Implementation

```python
# tasks.py - Complete updated implementation

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
    Background task using Claude Code CLI for analysis generation

    Updated to use correct Claude CLI syntax:
    - Print mode (-p) for non-interactive execution
    - JSON output format (--output-format json)
    - Stdin piping or file-based input
    """
    job = AnalysisJob.objects.get(id=job_id)
    order = job.order

    try:
        # Update job status
        job.status = 'processing'
        job.started_at = datetime.now()
        job.celery_task_id = self.request.id
        job.save()

        order.status = 'processing'
        order.save()

        # Prepare input data
        input_data = prepare_analysis_input(job)

        # Execute Claude Code CLI
        report_path = execute_claude_cli_analysis(input_data, job)

        # Save report to database
        report = save_analysis_report(report_path, job, order)

        # Update job status
        job.status = 'completed'
        job.completed_at = datetime.now()
        job.output_path = report_path
        job.save()

        order.status = 'completed'
        order.save()

        # Send completion email
        send_completion_email(order, report)

        return {
            'status': 'success',
            'job_id': job_id,
            'order_id': order.id,
            'report_path': report_path
        }

    except Exception as e:
        # Handle failure with retry logic
        job.retry_count += 1
        job.error_message = str(e)

        if job.retry_count < job.max_retries:
            job.status = 'retry'
            job.save()

            countdown = 60 * (2 ** job.retry_count)
            raise self.retry(exc=e, countdown=countdown)
        else:
            job.status = 'failed'
            job.save()

            order.status = 'failed'
            order.save()

            send_failure_email(order, str(e))
            notify_admin_of_failure(job)

            return {'status': 'failed', 'job_id': job_id, 'error': str(e)}


def prepare_analysis_input(job):
    """Prepare input data for Claude Code"""
    profile = job.order.profile

    return {
        'name': profile.name,
        'birth_date': profile.birth_date.isoformat(),
        'birth_time': profile.birth_time.isoformat() if profile.birth_time else None,
        'birth_location': profile.birth_location,
        'timezone': profile.timezone,
        'selected_experts': job.input_data['selected_experts'],
        'order_id': job.order.id,
        'job_id': job.id
    }


def execute_claude_cli_analysis(input_data, job):
    """
    Execute Claude Code CLI using correct syntax

    Returns:
        str: Path to generated HTML report
    """
    # Prepare output paths
    output_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
    os.makedirs(output_dir, exist_ok=True)

    html_report_path = os.path.join(output_dir, f'report_{job.order.id}.html')
    json_result_path = os.path.join(output_dir, f'result_{job.order.id}.json')

    # Convert input to JSON string
    input_json = json.dumps(input_data, indent=2)

    # Construct Claude prompt
    prompt = f"""
You are a fortune-telling analysis system. Generate a comprehensive HTML report based on the following birth data.

**Birth Information:**
```json
{input_json}
```

**Task Requirements:**

1. **Calculate Charts**: Use the Python calculation scripts in `scripts/fortune_telling/`:
   - For "bazi": Use `bazi_calculator.py` and `bazi_interpretation.py`
   - For "ziwei": Use `ziwei_calculator.py` and `ziwei_interpretation.py`
   - For "astrology": Use `astrology_calculator.py` and `astrology_interpretation.py`
   - And so on for other expert systems in the selected_experts list

2. **Generate HTML Report**:
   - Create a professional, beautifully formatted HTML document
   - Include charts and visualizations for each expert system
   - Add personalized narrative based on birth data
   - Synthesize insights across all selected expert systems
   - Use the existing `html_report_generator.py` as reference

3. **Save Output**:
   - Save the complete HTML report to: `{html_report_path}`
   - Ensure the file is created and contains valid HTML

4. **Return Result**:
   Respond with JSON in this exact format:
   ```json
   {{
     "status": "success",
     "report_path": "{html_report_path}",
     "experts_analyzed": {input_data['selected_experts']},
     "generation_time_seconds": <actual time taken>
   }}
   ```

**Important**: Actually execute the Python scripts and generate the real analysis. Do not create placeholder content.
"""

    try:
        # Execute Claude Code in print mode
        result = subprocess.run(
            [
                'claude',
                '-p',
                prompt,
                '--output-format', 'json',
                '--max-turns', '10',  # Allow multi-step execution
                '--dangerously-skip-permissions'  # Auto-approve file operations
            ],
            input=input_json,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minutes
            cwd=settings.BASE_DIR,
            env=os.environ.copy()
        )

        if result.returncode != 0:
            raise Exception(f"Claude Code failed: {result.stderr}")

        # Save raw JSON response
        with open(json_result_path, 'w') as f:
            f.write(result.stdout)

        # Parse Claude's response
        try:
            response = json.loads(result.stdout)
        except json.JSONDecodeError:
            # If response isn't pure JSON, try to extract JSON from output
            import re
            json_match = re.search(r'\{[^}]+\}', result.stdout, re.DOTALL)
            if json_match:
                response = json.loads(json_match.group())
            else:
                raise Exception(f"Failed to parse Claude response as JSON: {result.stdout[:500]}")

        # Verify report was generated
        if not os.path.exists(html_report_path):
            raise Exception(f"HTML report was not created at: {html_report_path}")

        # Validate it's actually HTML
        with open(html_report_path, 'r') as f:
            content = f.read()
            if not content.strip().startswith('<!DOCTYPE') and not content.strip().startswith('<html'):
                raise Exception("Generated file is not valid HTML")

        return html_report_path

    except subprocess.TimeoutExpired:
        raise Exception("Claude Code analysis timed out after 5 minutes")
    except Exception as e:
        raise Exception(f"Claude CLI execution failed: {str(e)}")


def save_analysis_report(report_path, job, order):
    """Save HTML report to database"""
    with open(report_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    generation_time = job.completed_at - job.started_at if job.completed_at else timedelta(0)

    report = AnalysisReport.objects.create(
        order=order,
        html_content=html_content,
        pdf_path='',
        experts_included=job.input_data['selected_experts'],
        generation_time=generation_time
    )

    return report


def send_completion_email(order, report):
    """Send completion notification"""
    subject = f"Your Fortune Analysis is Ready! (Order #{order.id})"
    message = f"""
Hello {order.user.first_name or order.user.email},

Your fortune analysis has been completed!

Order ID: #{order.id}
Experts: {', '.join(order.selected_experts)}

View your analysis: {settings.SITE_URL}/dashboard/orders/{order.id}/

Best regards,
Fortune Analysis Team
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.user.email],
        fail_silently=False
    )


def send_failure_email(order, error):
    """Notify user of failure"""
    subject = f"Issue with Your Analysis (Order #{order.id})"
    message = f"""
Hello,

We encountered an issue generating your analysis.
Our team has been notified and will resolve this within 24 hours.

Order ID: #{order.id}

Best regards,
Fortune Analysis Team
"""

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [order.user.email])


def notify_admin_of_failure(job):
    """Alert admin of failure"""
    subject = f"[ALERT] Analysis Job Failed - Job #{job.id}"
    message = f"""
Job ID: {job.id}
Order ID: {job.order.id}
User: {job.order.user.email}
Retries: {job.retry_count}
Error: {job.error_message}
"""

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL])
```

---

## Testing the Integration

### 1. **Test Claude Code CLI Manually**

```bash
# Create test input
cat > test_input.json << 'EOF'
{
  "name": "Test User",
  "birth_date": "1990-01-01",
  "birth_time": "12:00:00",
  "birth_location": "Taipei, Taiwan",
  "timezone": "Asia/Taipei",
  "selected_experts": ["bazi"]
}
EOF

# Test with print mode
cat test_input.json | claude -p "Generate a simple fortune analysis report for this birth data. Save as test_report.html" --output-format json

# Check if report was created
ls -la test_report.html
```

### 2. **Test Custom Slash Command**

First, create the command file:

```bash
mkdir -p .claude/commands
cat > .claude/commands/fortune-analyze.md << 'EOF'
---
command: /fortune-analyze
category: Fortune Telling
---

Generate fortune-telling analysis from birth data in $ARGUMENTS file.

Read the JSON file, run Python calculation scripts, and generate HTML report.
EOF

# Test it
claude /fortune-analyze test_input.json
```

### 3. **Test from Python**

```python
# test_claude_cli.py

import subprocess
import json

input_data = {
    "name": "Test User",
    "birth_date": "1990-01-01",
    "selected_experts": ["bazi"]
}

prompt = "Generate a simple fortune analysis and save as test.html"

result = subprocess.run(
    ['claude', '-p', prompt, '--output-format', 'json'],
    input=json.dumps(input_data),
    capture_output=True,
    text=True,
    timeout=60
)

print("Return code:", result.returncode)
print("Output:", result.stdout)
print("Errors:", result.stderr)
```

---

## Key Differences from Original Design

| Original (Incorrect) | Corrected |
|---------------------|-----------|
| `claude /fortune-analyze --input=file.json` | `cat file.json \| claude -p "prompt"` |
| `--output=report.html` | Shell redirection `> report.html` or Claude saves file via tools |
| `--format=html` | Specify in prompt, not as flag |
| Custom CLI flags | Use standard `-p` and `--output-format` |

---

## Recommended Approach: Custom Slash Command

**Why**: Most maintainable and aligned with Claude Code's design

**Setup**:

1. Create `.claude/commands/fortune-analyze.md`:
```markdown
Generate fortune-telling analysis from JSON file: $ARGUMENTS

1. Read birth data from the file
2. Run Python scripts in scripts/fortune_telling/
3. Generate HTML report
4. Save to data/fortune-telling/reports/
```

2. Use in Celery task:
```python
subprocess.run(
    ['claude', '-p', f'/fortune-analyze {input_file}', '--output-format', 'json'],
    capture_output=True,
    timeout=300
)
```

This gives you:
- ✅ Clean command interface
- ✅ Testable in interactive mode
- ✅ Works in automation with `-p`
- ✅ JSON output for parsing
- ✅ File operations handled by Claude's tools

---

## Production Considerations

### Security
- Use `--max-turns` to limit iterations
- Validate Claude's file operations
- Sandbox execution if possible

### Monitoring
```python
# Log Claude CLI output for debugging
import logging
logger = logging.getLogger(__name__)

result = subprocess.run([...], capture_output=True)
logger.info(f"Claude stdout: {result.stdout}")
logger.error(f"Claude stderr: {result.stderr}")
```

### Cost Control
- Each Claude CLI invocation uses Anthropic API
- Monitor API usage via Anthropic console
- Set budget alerts

### Error Recovery
- Parse JSON output for success/failure
- Check file existence after execution
- Retry with exponential backoff
- Manual intervention for persistent failures

This corrected implementation uses Claude Code CLI as it's actually designed to work!

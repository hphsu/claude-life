---
name: fortune-analyze
description: 綜合命理分析系統 - 整合八字、紫微、占星三大體系並生成HTML報告
category: fortune-telling
---

# Fortune-Telling Comprehensive Analysis System

## Purpose
Execute a comprehensive fortune-telling analysis using three expert systems (BaZi, Zi Wei Dou Shu, Psychological Astrology), synthesize the results, and generate a beautiful HTML report.

## Usage
```bash
/fortune-analyze <name> <birth_date> <birth_time> <location> <gender>
```

**Arguments:**
- `name`: Person's name (Chinese or English)
- `birth_date`: YYYY-MM-DD format (e.g., 1972-01-17)
- `birth_time`: HH:MM format with am/pm (e.g., 06:00am)
- `location`: City, Region/Country (e.g., "Miaoli, Taiwan")
- `gender`: male or female

**Example:**
```bash
/fortune-analyze Frank 1972-01-17 06:00am "Miaoli, Taiwan" male
```

## Execution Workflow

You must execute the following steps in order:

### Step 1: Validate Arguments
Verify that all required arguments are provided and in correct format.

### Step 2: Run Python Calculation Script
Execute the fortune-telling calculation script:

```bash
cd /Users/frank/src/life/scripts/fortune_telling
python3 run_fortune_analysis.py "$NAME" "$BIRTH_DATE" "$BIRTH_TIME" "$LOCATION" "$GENDER"
```

This will generate a JSON file at:
```
/Users/frank/src/life/data/fortune-telling/fortune_tell_{name}_{timestamp}.json
```

### Step 3: Read Calculation Results
Use the Read tool to load the generated JSON file. The file contains:
- BaZi (八字) calculation results
- Zi Wei Dou Shu (紫微斗數) calculation results
- Psychological Astrology calculation results
- Basic birth data metadata

### Step 4: Spawn Expert Agents in Parallel
Launch 3 expert agents **in parallel** using the Task tool. Each agent receives the pre-calculated data for their specialty.

**Agent 1: BaZi Expert**
```
Subagent: bazi-expert
Task: Analyze the provided BaZi data and generate a comprehensive Traditional Chinese analysis

Input Data:
{Extract BaZi section from JSON and format according to agent's input requirements}

Requirements:
- Output in Traditional Chinese (繁體中文)
- Minimum 300 characters per major domain
- Pure markdown format
- Include confidence levels
```

**Agent 2: Zi Wei Expert**
```
Subagent: ziwei-expert
Task: Analyze the provided Zi Wei Dou Shu data and generate a comprehensive Traditional Chinese analysis

Input Data:
{Extract Ziwei section from JSON and format according to agent's input requirements}

Requirements:
- Output in Traditional Chinese (繁體中文)
- Major palaces ≥250 characters, secondary ≥150 characters
- Pure markdown format
- Include confidence levels
```

**Agent 3: Astrology Expert**
```
Subagent: astrology-expert
Task: Analyze the provided psychological astrology data and generate a comprehensive Traditional Chinese analysis

Input Data:
{Extract Astrology section from JSON and format according to agent's input requirements}

Requirements:
- Output in Traditional Chinese (繁體中文)
- Major portraits ≥300 characters, development domains ≥200 characters
- Pure markdown format
- Include confidence levels
- Warm, empowering, non-judgmental tone
```

**IMPORTANT**: Use a **single Task tool invocation with 3 sub-tasks** to run all 3 agents in parallel for maximum efficiency.

### Step 5: Wait for Agent Completion
All 3 expert agents must complete before proceeding. Store their outputs:
- `bazi_analysis` = BaZi expert markdown output
- `ziwei_analysis` = Zi Wei expert markdown output
- `astrology_analysis` = Astrology expert markdown output

### Step 6: Spawn Synthesis Agent
Launch the synthesis agent **sequentially** (after Step 5 completes):

```
Subagent: synthesis-expert
Task: Synthesize the three expert analyses into a comprehensive, cross-validated report

Input Data:
**BaZi Expert Analysis:**
{bazi_analysis}

**Zi Wei Expert Analysis:**
{ziwei_analysis}

**Astrology Expert Analysis:**
{astrology_analysis}

**Basic Birth Data:**
- 姓名: {name}
- 出生時間: {birth_date} {birth_time}
- 出生地點: {location}
- 性別: {gender}

Requirements:
- Output in Traditional Chinese (繁體中文)
- Major domains ≥400 characters each
- Total report ≥2500 characters
- Pure markdown format
- Include detailed confidence scoring
- Acknowledge contradictions transparently
- Professional, balanced, insightful tone
```

### Step 7: Convert Markdown to HTML
For each of the 4 markdown outputs (BaZi, Zi Wei, Astrology, Synthesis):

1. Use a markdown-to-HTML converter (Python `markdown` library or similar)
2. Preserve formatting, headings, lists, emphasis
3. Ensure proper UTF-8 encoding for Traditional Chinese

You can use this Python snippet for conversion:
```python
import markdown

# Convert each markdown section to HTML
bazi_html = markdown.markdown(bazi_analysis, extensions=['extra', 'nl2br'])
ziwei_html = markdown.markdown(ziwei_analysis, extensions=['extra', 'nl2br'])
astrology_html = markdown.markdown(astrology_analysis, extensions=['extra', 'nl2br'])
synthesis_html = markdown.markdown(synthesis_analysis, extensions=['extra', 'nl2br'])
```

### Step 8: Generate HTML Report
Read the HTML template:
```
/Users/frank/src/life/scripts/fortune_telling/templates/agent_report_template.html
```

Replace all placeholders:
- `{{NAME}}` → person's name
- `{{BIRTH_DATE}}` → birth date
- `{{BIRTH_TIME}}` → birth time
- `{{LOCATION}}` → location
- `{{GENDER}}` → gender (男性/女性)
- `{{TIMESTAMP}}` → current timestamp
- `{{BAZI_CONTENT}}` → bazi_html
- `{{ZIWEI_CONTENT}}` → ziwei_html
- `{{ASTROLOGY_CONTENT}}` → astrology_html
- `{{SYNTHESIS_CONTENT}}` → synthesis_html

### Step 9: Save HTML Report
Save the final HTML to:
```
/Users/frank/src/life/data/fortune-telling/fortune_tell_{name}_{timestamp}.html
```

Use the same timestamp as the JSON file for consistency.

### Step 10: Display Success Message
Inform the user:
```
✅ 綜合命理分析完成！

📊 分析報告已生成:
- JSON數據: /Users/frank/src/life/data/fortune-telling/fortune_tell_{name}_{timestamp}.json
- HTML報告: /Users/frank/src/life/data/fortune-telling/fortune_tell_{name}_{timestamp}.html

📖 報告包含:
- 🧩 三方法綜合分析 (最高信心度)
- 📿 八字命理深度解析
- ⭐ 紫微斗數完整分析
- 🌟 心理占星全面解讀

⏱️ 總計分析時間: ~2-3分鐘
```

## Implementation Notes

1. **Parallel Execution**: Steps 4 (3 expert agents) must run in parallel for efficiency
2. **Sequential Synthesis**: Step 6 (synthesis agent) must run after Step 5 completes
3. **Error Handling**: If any agent fails, provide error details and partial results if available
4. **Data Validation**: Ensure JSON file exists and contains all required sections before spawning agents
5. **Character Encoding**: All markdown and HTML must use UTF-8 encoding for Traditional Chinese
6. **Timestamp Consistency**: Use the same timestamp for JSON and HTML filenames

## Quality Standards

- **Completeness**: All 4 analyses (3 experts + synthesis) must complete successfully
- **Language**: All outputs must be in Traditional Chinese (繁體中文)
- **Length**: Meet minimum character requirements for each domain
- **Formatting**: Proper HTML rendering with all markdown formatting preserved
- **Professional**: Executive-level quality suitable for serious life guidance

## Expected Execution Time
- Python calculations: ~30 seconds
- 3 expert agents (parallel): ~60-90 seconds
- Synthesis agent: ~30-45 seconds
- HTML generation: ~5 seconds
- **Total**: ~2-3 minutes

## Progress Tracking
The system now includes real-time progress tracking with:
- **Stage Progress**: Shows progress through calculation stages (parse → prepare → bazi → ziwei → astrology → assemble → save)
- **Agent Progress**: Displays status of all 4 agents (3 experts + synthesis) during analysis phase
- **Time Tracking**: Reports elapsed time for each stage
- **Summary Report**: Shows final completion statistics and total time

Progress indicators appear automatically during execution with color-coded status emojis:
- ⏳ Pending/Waiting
- 🔄 In Progress
- ✅ Completed
- ❌ Failed

## Files Created
1. JSON data file with all calculations
2. HTML report with beautiful formatting and navigation

---

**Note**: This command requires:
- Python environment with required libraries installed
- All 4 agent definitions in `.claude/agents/`
- HTML template in `scripts/fortune_telling/templates/`
- Calculation script at `scripts/fortune_telling/run_fortune_analysis.py`

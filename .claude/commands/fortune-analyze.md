---
name: fortune-analyze
description: 綜合命理分析系統 - 整合八字、紫微、占星、姓名學、梅花易數、生命靈數、奇門遁甲、六爻八大體系並生成HTML報告
category: fortune-telling
---

# Fortune-Telling Comprehensive Analysis System

## Purpose
Execute a comprehensive fortune-telling analysis using up to EIGHT expert systems, synthesize the results, and generate a beautiful HTML report.

## Usage
```bash
/fortune-analyze <name> <birth_date> <birth_time> <location> <gender> [--methods method1 method2 ...]
```

**Arguments:**
- `name`: Person's name (Chinese or English)
- `birth_date`: YYYY-MM-DD format (e.g., 1972-01-17)
- `birth_time`: HH:MM format with am/pm (e.g., 06:00am)
- `location`: City, Region/Country (e.g., "Miaoli, Taiwan")
- `gender`: male or female
- `--methods`: (Optional) Space-separated list of methods to use
  - Available: bazi, ziwei, astrology, name, plum, numerology, qimen, liuyao, all
  - Default: all

**Example:**
```bash
/fortune-analyze Frank 1972-01-17 06:00am "Miaoli, Taiwan" male
/fortune-analyze Frank 1972-01-17 06:00am "Miaoli, Taiwan" male --methods bazi ziwei astrology
/fortune-analyze Frank 1972-01-17 06:00am "Miaoli, Taiwan" male --methods all
```

## Execution Workflow

You must execute the following steps in order:

### Step 1: Validate Arguments
Verify that all required arguments are provided and in correct format.

### Step 2: Run Python Calculation Script
Execute the fortune-telling calculation script with the appropriate --methods flag:

```bash
cd /home/user/claude-life/scripts/fortune_telling
python3 run_fortune_analysis.py "$NAME" "$BIRTH_DATE" "$BIRTH_TIME" "$LOCATION" "$GENDER" --methods $METHODS
```

This will generate a JSON file at:
```
/home/user/claude-life/data/fortune-telling/fortune_tell_{name}_{timestamp}.json
```

### Step 3: Read Calculation Results
Use the Read tool to load the generated JSON file. The file contains calculation results for the selected methods:
- BaZi (八字) - if 'bazi' or 'all' selected
- Zi Wei Dou Shu (紫微斗數) - if 'ziwei' or 'all' selected
- Psychological Astrology - if 'astrology' or 'all' selected
- Name Analysis (姓名學) - if 'name' or 'all' selected
- Plum Blossom (梅花易數) - if 'plum' or 'all' selected
- Numerology (生命靈數) - if 'numerology' or 'all' selected
- Qi Men Dun Jia (奇門遁甲) - if 'qimen' or 'all' selected
- Liu Yao (六爻) - if 'liuyao' or 'all' selected
- Basic birth data metadata

### Step 4: Spawn Expert Agents in Parallel
Launch expert agents **in parallel** using the Task tool for each selected method. Each agent receives the pre-calculated data for their specialty.

**Agent 1: BaZi Expert** (if 'bazi' in methods)
```
Subagent: general-purpose
Task: Analyze the provided BaZi (八字) data and generate a comprehensive Traditional Chinese analysis

Input Data:
{Extract BaZi section from JSON}

Requirements:
- Output in Traditional Chinese (繁體中文)
- Minimum 300 characters per major domain
- Pure markdown format
- Include confidence levels
- Analyze四柱八字、五行強弱、十神配置、格局高低、用神喜忌、大運流年、事業財運健康等

Output Format:
## 📿 八字命理深度解析

### 一、基本命盤
[四柱八字配置、五行統計、日主強弱]

### 二、格局分析
[格局判斷與成敗分析]

### 三、十神配置
[十神分佈與特性解讀]

### 四、命運特徵
#### 💼 事業運勢
[官星印星食傷配置分析]

#### 💰 財富運勢
[財星強弱分析]

#### 💕 感情婚姻
[配偶宮桃花星分析]

#### 🏥 健康狀況
[五行偏枯分析]

### 五、大運流年
[運勢走向分析]

### 六、開運建議
[五行補救、方位顏色、職業方向]
```

**Agent 2: Zi Wei Expert** (if 'ziwei' in methods)
```
Subagent: general-purpose
Task: Analyze the provided Zi Wei Dou Shu (紫微斗數) data and generate a comprehensive Traditional Chinese analysis

Input Data:
{Extract Ziwei section from JSON}

Requirements:
- Output in Traditional Chinese (繁體中文)
- Major palaces ≥250 characters, secondary ≥150 characters
- Pure markdown format
- Include confidence levels
- Analyze十二宮星曜配置、主星輔星組合、四化飛星、格局判斷、大限流年等

Output Format:
## ⭐ 紫微斗數完整分析

### 一、命盤概況
[命宮主星、身宮位置、命主身主]

### 二、命宮分析
[命宮主星組合與格局]

### 三、十二宮詳解
[逐宮分析：命宮、兄弟、夫妻、子女、財帛、疾厄、遷移、僕役、官祿、田宅、福德、父母]

### 四、四化分析
[生年四化及其影響]

### 五、大限流年
[運勢走向分析]

### 六、人生建議
[發展方向與注意事項]
```

**Agent 3: Astrology Expert** (if 'astrology' in methods)
```
Subagent: general-purpose
Task: Analyze the provided psychological astrology data and generate a comprehensive Traditional Chinese analysis

Input Data:
{Extract Astrology section from JSON}

Requirements:
- Output in Traditional Chinese (繁體中文)
- Major portraits ≥300 characters, development domains ≥200 characters
- Pure markdown format
- Include confidence levels
- Warm, empowering, non-judgmental tone
- Analyze行星星座宮位、相位配置、主導元素、星盤格局等

Output Format:
## 🌟 心理占星全面解讀

### 一、星盤概覽
[太陽月亮上升MC、主導元素、星盤格局]

### 二、行星配置
[逐個行星分析：太陽、月亮、水星、金星、火星、木星、土星、天王星、海王星、冥王星]

### 三、宮位重點
[有行星落入的宮位詳細解讀]

### 四、相位分析
[主要相位及其意義]

### 五、生命主題
[事業、財富、愛情、靈性]

### 六、流年行運
[當前重要行運]

### 七、天賦與挑戰
[天賦領域、挑戰領域、整合建議]
```

**Agent 4: Name Analysis Expert** (if 'name' in methods)
```
Subagent: general-purpose
Task: Analyze the provided Name Analysis (姓名學) data and generate a comprehensive Traditional Chinese analysis

Input Data:
{Extract name_analysis section from JSON}

Requirements:
- Output in Traditional Chinese (繁體中文)
- Minimum 250 characters
- Pure markdown format
- Include confidence levels
- Analyze五格配置、三才組合、數理吉凶、五行屬性等

Output Format:
## ✍️ 姓名學專業分析

### 一、基本資訊
[姓名、性別、筆畫統計]

### 二、五格配置
[天格、人格、地格、外格、總格的數值、五行、吉凶]

### 三、三才配置
[天格人格地格的五行組合與吉凶]

### 四、數理分析
[各格數理含義詳解]

### 五、綜合評價
[整體評分、吉凶判斷、優劣勢分析]

### 六、改名建議
[如需改名的建議方向]
```

**Agent 5: Plum Blossom Expert** (if 'plum' in methods)
```
Subagent: general-purpose
Task: Analyze the provided Plum Blossom Numerology (梅花易數) data and generate a comprehensive Traditional Chinese analysis

Input Data:
{Extract plum_blossom section from JSON}

Requirements:
- Output in Traditional Chinese (繁體中文)
- Minimum 250 characters
- Pure markdown format
- Include confidence levels
- Analyze本卦變卦、上下卦組合、動爻意義、五行生剋等

Output Format:
## 🌸 梅花易數占測分析

### 一、起卦資訊
[起卦時間、起卦方法]

### 二、本卦分析
[本卦卦名、上下卦、卦辭、卦義]

### 三、動爻解析
[動爻位置與含義]

### 四、變卦分析
[變卦卦名、卦義、與本卦的關係]

### 五、五行生剋
[上下卦五行關係分析]

### 六、綜合斷卦
[吉凶判斷、事態發展預測、行動建議]
```

**Agent 6: Numerology Expert** (if 'numerology' in methods)
```
Subagent: general-purpose
Task: Analyze the provided Western Numerology (生命靈數) data and generate a comprehensive Traditional Chinese analysis

Input Data:
{Extract numerology section from JSON}

Requirements:
- Output in Traditional Chinese (繁體中文)
- Minimum 250 characters
- Pure markdown format
- Include confidence levels
- Analyze生命靈數、命運數、靈魂數、人格數、生日數及大師數等

Output Format:
## 🔢 生命靈數深度分析

### 一、核心數字
[生命靈數、命運數、靈魂數、人格數、生日數]

### 二、生命靈數解讀
[主要靈數的含義、類型、關鍵字]

### 三、性格特質
[正面特質、負面特質、核心驅動力]

### 四、人生課題
[生命目標、主要挑戰、成長方向]

### 五、天賦才能
[天賦領域、適合職業]

### 六、大師數分析
[如有大師數11/22/33的特殊意義]

### 七、整合建議
[如何發揮優勢、克服挑戰]
```

**Agent 7: Qi Men Expert** (if 'qimen' in methods)
```
Subagent: general-purpose
Task: Analyze the provided Qi Men Dun Jia (奇門遁甲) data and generate a comprehensive Traditional Chinese analysis

Input Data:
{Extract qimen section from JSON}

Requirements:
- Output in Traditional Chinese (繁體中文)
- Minimum 300 characters
- Pure markdown format
- Include confidence levels
- Analyze局數、九星八門八神配置、九宮方位、吉凶判斷等

Output Format:
## 🧭 奇門遁甲盤象分析

### 一、起局資訊
[起局時間、時辰干支、局數、陰遁陽遁]

### 二、盤面概況
[九宮配置總覽]

### 三、各宮分析
[逐宮分析：九星、八門、八神配置及吉凶]

### 四、用神分析
[根據占測事項判斷用神]

### 五、最佳方位
[吉利方位推薦]

### 六、時機判斷
[適合行動的時機]

### 七、綜合建議
[整體吉凶、行動策略、注意事項]
```

**Agent 8: Liu Yao Expert** (if 'liuyao' in methods)
```
Subagent: general-purpose
Task: Analyze the provided Liu Yao (六爻) divination data and generate a comprehensive Traditional Chinese analysis

Input Data:
{Extract liuyao section from JSON}

Requirements:
- Output in Traditional Chinese (繁體中文)
- Minimum 250 characters
- Pure markdown format
- Include confidence levels
- Analyze本卦變卦、六爻配置、六親六獸、動爻意義等

Output Format:
## 🎲 六爻占卜詳解

### 一、起卦資訊
[起卦時間、起卦方法]

### 二、本卦分析
[本卦卦名、上下卦、卦辭、判斷]

### 三、六爻配置
[逐爻分析：六親、六獸配置]

### 四、動爻解析
[動爻數量、位置、意義]

### 五、變卦分析
[變卦卦名、卦義]

### 六、用神分析
[確定用神及其旺衰]

### 七、綜合斷卦
[吉凶判斷、事態走向、應期推斷、行動建議]
```

**IMPORTANT**: Use a **single Task tool invocation with multiple sub-tasks** to run all selected expert agents in parallel for maximum efficiency. Only spawn agents for methods that were selected by the user.

### Step 5: Wait for Agent Completion
All selected expert agents must complete before proceeding. Store their outputs:
- `bazi_analysis` = BaZi expert markdown output (if selected)
- `ziwei_analysis` = Zi Wei expert markdown output (if selected)
- `astrology_analysis` = Astrology expert markdown output (if selected)
- `name_analysis` = Name Analysis expert markdown output (if selected)
- `plum_analysis` = Plum Blossom expert markdown output (if selected)
- `numerology_analysis` = Numerology expert markdown output (if selected)
- `qimen_analysis` = Qi Men expert markdown output (if selected)
- `liuyao_analysis` = Liu Yao expert markdown output (if selected)

### Step 6: Spawn Synthesis Agent
Launch the synthesis agent **sequentially** (after Step 5 completes):

```
Subagent: general-purpose
Task: Synthesize ALL available expert analyses into a comprehensive, cross-validated report

Input Data:
**Selected Methods**: {list of methods that were analyzed}

**BaZi Expert Analysis** (if available):
{bazi_analysis}

**Zi Wei Expert Analysis** (if available):
{ziwei_analysis}

**Astrology Expert Analysis** (if available):
{astrology_analysis}

**Name Analysis Expert Analysis** (if available):
{name_analysis}

**Plum Blossom Expert Analysis** (if available):
{plum_analysis}

**Numerology Expert Analysis** (if available):
{numerology_analysis}

**Qi Men Expert Analysis** (if available):
{qimen_analysis}

**Liu Yao Expert Analysis** (if available):
{liuyao_analysis}

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
- Include detailed confidence scoring for convergent findings
- Acknowledge contradictions transparently
- Professional, balanced, insightful tone
- ONLY synthesize methods that were actually analyzed (check selected methods list)

Output Format:
## 🧩 跨方法綜合分析

### 一、分析方法概覽
[列出本次使用的分析方法]

### 二、核心命運特徵

#### 🎯 多方法一致的強力指標
[列出三個或以上方法都指向的特質]

**1. [特質名稱]**
- ✅ **[方法1]**: [評分 ⭐⭐⭐⭐⭐ X/10]
- ✅ **[方法2]**: [評分 ⭐⭐⭐⭐⭐ X/10]
- ✅ **[方法3]**: [評分 ⭐⭐⭐⭐⭐ X/10]
- 🌟 **綜合解讀**: [三者一致的結論與建議]

#### ⚖️ 不同觀點的平衡說明
[當不同方法有分歧時的分析]

### 三、人生階段運勢
[如果有八字、紫微、占星等時間性方法，整合分析不同階段]

### 四、重要人生主題

#### 💼 事業發展路徑
[整合所有方法對事業的分析]

#### 💰 財富累積模式
[整合所有方法對財運的分析]

#### 💕 感情婚姻狀態
[整合所有方法對感情的分析]

#### 🏥 健康養生重點
[整合所有方法對健康的分析]

### 五、個人化建議

#### 🎯 優勢發揮
[基於多方法一致的強項]

#### ⚠️ 風險規避
[基於多方法一致的弱項]

#### 🛤️ 發展路線
[整合性的人生規劃建議]

#### 🔮 關鍵時機
[重要的轉折年份與把握時機的建議]

### 六、信心度評估
[對各項分析的信心度評分與說明]
```

### Step 7: Convert Markdown to HTML
For each of the available markdown outputs:

1. Use a markdown-to-HTML converter (Python `markdown` library or similar)
2. Preserve formatting, headings, lists, emphasis
3. Ensure proper UTF-8 encoding for Traditional Chinese

You can use this Python snippet for conversion:
```python
import markdown

# Convert each markdown section to HTML
# Only convert analyses that were actually generated
if bazi_analysis:
    bazi_html = markdown.markdown(bazi_analysis, extensions=['extra', 'nl2br'])
if ziwei_analysis:
    ziwei_html = markdown.markdown(ziwei_analysis, extensions=['extra', 'nl2br'])
# ... repeat for all available analyses
synthesis_html = markdown.markdown(synthesis_analysis, extensions=['extra', 'nl2br'])
```

### Step 8: Generate HTML Report
Read the HTML template:
```
/home/user/claude-life/scripts/fortune_telling/templates/agent_report_template.html
```

Replace all placeholders:
- `{{NAME}}` → person's name
- `{{BIRTH_DATE}}` → birth date
- `{{BIRTH_TIME}}` → birth time
- `{{LOCATION}}` → location
- `{{GENDER}}` → gender (男性/女性)
- `{{TIMESTAMP}}` → current timestamp
- `{{METHODS}}` → comma-separated list of methods used
- `{{SYNTHESIS_CONTENT}}` → synthesis_html
- `{{BAZI_CONTENT}}` → bazi_html (if available, else hide section)
- `{{ZIWEI_CONTENT}}` → ziwei_html (if available, else hide section)
- `{{ASTROLOGY_CONTENT}}` → astrology_html (if available, else hide section)
- `{{NAME_ANALYSIS_CONTENT}}` → name_html (if available, else hide section)
- `{{PLUM_CONTENT}}` → plum_html (if available, else hide section)
- `{{NUMEROLOGY_CONTENT}}` → numerology_html (if available, else hide section)
- `{{QIMEN_CONTENT}}` → qimen_html (if available, else hide section)
- `{{LIUYAO_CONTENT}}` → liuyao_html (if available, else hide section)

**IMPORTANT**: For sections that weren't analyzed, either:
- Hide the section entirely (preferred)
- Show a message like "本次分析未包含此方法"

### Step 9: Save HTML Report
Save the final HTML to:
```
/home/user/claude-life/data/fortune-telling/fortune_tell_{name}_{timestamp}.html
```

Use the same timestamp as the JSON file for consistency.

### Step 10: Display Success Message
Inform the user:
```
✅ 綜合命理分析完成！

📊 分析報告已生成:
- JSON數據: /home/user/claude-life/data/fortune-telling/fortune_tell_{name}_{timestamp}.json
- HTML報告: /home/user/claude-life/data/fortune-telling/fortune_tell_{name}_{timestamp}.html

📖 報告包含:
- 🧩 {N}方法綜合分析 (最高信心度)
[list all methods that were used with their emojis]

⏱️ 總計分析時間: ~{N}-{N+1}分鐘
```

## Implementation Notes

1. **Parallel Execution**: Step 4 (expert agents) must run in parallel for efficiency
2. **Sequential Synthesis**: Step 6 (synthesis agent) must run after Step 5 completes
3. **Method Selection**: Only spawn agents and generate sections for selected methods
4. **Error Handling**: If any agent fails, provide error details and partial results if available
5. **Data Validation**: Ensure JSON file exists and contains all required sections before spawning agents
6. **Character Encoding**: All markdown and HTML must use UTF-8 encoding for Traditional Chinese
7. **Timestamp Consistency**: Use the same timestamp for JSON and HTML filenames
8. **Dynamic Sections**: HTML template should handle variable number of methods gracefully

## Quality Standards

- **Completeness**: All selected analyses must complete successfully
- **Language**: All outputs must be in Traditional Chinese (繁體中文)
- **Length**: Meet minimum character requirements for each domain
- **Formatting**: Proper HTML rendering with all markdown formatting preserved
- **Professional**: Executive-level quality suitable for serious life guidance
- **Synthesis**: Must intelligently integrate only the methods that were analyzed

## Expected Execution Time
- Python calculations: ~30 seconds (for all 8 methods)
- Expert agents (parallel): ~60-120 seconds (varies by number of methods)
- Synthesis agent: ~30-60 seconds
- HTML generation: ~5 seconds
- **Total**: ~2-4 minutes (varies by number of methods selected)

## Progress Tracking
The system now includes real-time progress tracking with:
- **Stage Progress**: Shows progress through calculation stages
- **Agent Progress**: Displays status of all active agents during analysis phase
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
- Calculation script at `scripts/fortune_telling/run_fortune_analysis.py`
- HTML template in `scripts/fortune_telling/templates/`
- All calculator modules for the 8 methods

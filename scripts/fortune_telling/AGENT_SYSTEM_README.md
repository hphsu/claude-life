# Fortune-Telling AI Agent System

## 🎯 System Overview

A comprehensive fortune-telling analysis system that integrates **three expert AI agents** using:
- **八字命理 (BaZi)** - Chinese Four Pillars astrology
- **紫微斗數 (Zi Wei Dou Shu)** - Purple Star Astrology
- **心理占星 (Psychological Astrology)** - Western astrology with Jungian psychology

The system generates a **synthesis report** that cross-validates insights across all three methods, providing the highest confidence analysis.

## 📁 File Structure

```
/Users/frank/src/life/
├── .claude/
│   ├── agents/                              # AI expert agent definitions
│   │   ├── bazi-expert.md                   # 八字 expert (160 lines)
│   │   ├── ziwei-expert.md                  # 紫微 expert (240 lines)
│   │   ├── astrology-expert.md              # 占星 expert (290 lines)
│   │   └── synthesis-expert.md              # 綜合 expert (410 lines)
│   └── commands/
│       └── fortune-analyze.md               # Main orchestration command
├── scripts/fortune_telling/
│   ├── run_fortune_analysis.py              # Parameterized calculation script
│   └── templates/
│       └── agent_report_template.html       # Beautiful HTML report template
└── data/fortune-telling/                    # Output directory
    ├── fortune_tell_{name}_{timestamp}.json # Calculation data
    └── fortune_tell_{name}_{timestamp}.html # Final report
```

## 🚀 Quick Start

### Method 1: Using the Slash Command (Recommended)

```bash
/fortune-analyze <name> <birth_date> <birth_time> <location> <gender>
```

**Example:**
```bash
/fortune-analyze Frank 1972-01-17 06:00am "Miaoli, Taiwan" male
```

This single command will:
1. ✅ Run Python calculations (八字, 紫微, 占星)
2. ✅ Spawn 3 expert agents in parallel
3. ✅ Generate synthesis analysis
4. ✅ Create beautiful HTML report
5. ✅ Save everything to `data/fortune-telling/`

**Expected Time:** ~2-3 minutes

### Method 2: Manual Step-by-Step

#### Step 1: Run Calculations
```bash
cd /Users/frank/src/life/scripts/fortune_telling
python3 run_fortune_analysis.py Frank 1972-01-17 06:00am "Miaoli, Taiwan" male
```

This generates:
```
/Users/frank/src/life/data/fortune-telling/fortune_tell_Frank_20251029_104804.json
```

#### Step 2: Use the Slash Command with JSON File
```bash
/fortune-analyze --json-file /path/to/fortune_tell_Frank_20251029_104804.json
```

## 📋 Agent Definitions

### 1. BaZi Expert (bazi-expert.md)
- **Role**: 資深八字命理大師，專精四柱分析與人生指引
- **Analysis Domains**: 性格特質, 事業發展, 財富運勢, 感情婚姻, 健康狀況
- **Output**: ≥300 characters per domain in Traditional Chinese
- **Confidence**: Based on pillar alignment (極高 >95%, 高 80-95%, 中等 60-80%)

### 2. Zi Wei Expert (ziwei-expert.md)
- **Role**: 精通紫微斗數的資深命理大師，深諳星曜宮位與四化飛星
- **Analysis Domains**: 12 palaces (命/兄/夫/子/財/疾/遷/交/官/田/福/父)
- **Output**: Major palaces ≥250 chars, secondary ≥150 chars
- **Confidence**: Based on star clarity and transformations

### 3. Astrology Expert (astrology-expert.md)
- **Role**: 精通心理占星學的資深占星師，深諳榮格心理學與星盤解讀
- **Analysis Domains**: 6 psychological portraits + 3 development domains
- **Output**: Major ≥300 chars, development ≥200 chars
- **Confidence**: Based on planetary alignments and aspect patterns

### 4. Synthesis Expert (synthesis-expert.md)
- **Role**: 綜合分析大師，融會貫通八字、紫微、占星三大系統
- **Integration Methods**:
  - 共振法 (Resonance): Find common insights (highest confidence)
  - 互補法 (Complementarity): Use methods to fill each other's blind spots
  - 驗證法 (Verification): Cross-validate conclusions
  - 層次法 (Layering): Different methods for different levels
  - 時空法 (Spacetime): BaZi for time, Ziwei for space, Astrology for psychology
- **Output**: ≥2500 characters total, ≥400 chars per major domain
- **Confidence Formula**: (Consistency×0.5) + (Data Quality×0.3) + (Theory Support×0.2)

## 🎨 HTML Report Features

The generated HTML report includes:

- **📋 Metadata Header**: Name, birth date/time, location, gender
- **🧭 Navigation**: Quick links to all sections
- **🧩 Synthesis Section**: Cross-validated insights (highest confidence)
- **📿 BaZi Section**: Four Pillars analysis with color-coded visualization
- **⭐ Zi Wei Section**: 12 Palaces with star positions
- **🌟 Astrology Section**: Natal chart interpretation
- **💫 Beautiful Styling**:
  - Professional gradient header
  - Color-coded sections for each method
  - Confidence badges
  - Responsive design (mobile-friendly)
  - Print-friendly layout
  - Perfect Traditional Chinese typography

## 📊 Output Examples

### JSON Output Structure
```json
{
  "basic_info": {
    "name": "Frank",
    "birth_gregorian": "1972-01-17 06:00",
    "birth_lunar": "1971年12月2日",
    "location": "miaoli",
    "gender": "男"
  },
  "calendar_data": { ... },
  "bazi": {
    "calculation": {
      "four_pillars": {
        "year": "辛亥",
        "month": "辛卯",
        "day": "己未",
        "hour": "丁卯"
      },
      ...
    }
  },
  "ziwei": { ... },
  "astrology": { ... }
}
```

### Agent Output Example
Each agent returns markdown in Traditional Chinese:

```markdown
# 八字命理深度分析

## 性格特質

**日主特性**: 己土日主，溫和穩重...

**十神配置**: 命中食神當令，具有...

**信心度**: 極高（95%+）- 三柱明確指向
```

## ⚙️ Command Arguments

### Required Arguments:
- `name`: Person's name (Chinese or English)
- `birth_date`: Format: YYYY-MM-DD
- `birth_time`: Format: HH:MMam/pm (e.g., 06:00am, 11:30pm)
- `location`: City name (e.g., "Miaoli, Taiwan" or just "miaoli")
- `gender`: male or female

### Optional Flags:
- `--true-solar-time`: Use true solar time correction (default: false)

## 🔍 Validation & Quality

### Quality Gates:
- ✅ All agents must complete successfully
- ✅ Minimum character requirements enforced
- ✅ Traditional Chinese (繁體中文) only
- ✅ Confidence levels required for each section
- ✅ Markdown formatting preserved in HTML
- ✅ UTF-8 encoding verified

### Confidence Levels:
- **極高 (95%+)**: All 3 methods agree
- **高 (80-95%)**: 2 methods agree, 1 doesn't contradict
- **中等 (60-80%)**: 2 methods agree, 1 differs
- **較低 (40-60%)**: Methods show different aspects
- **待確認 (<40%)**: Significant contradictions detected

## 🎯 Use Cases

1. **Personal Life Guidance**: Comprehensive self-understanding across multiple systems
2. **Career Planning**: Cross-validated career recommendations
3. **Relationship Insight**: Multi-method compatibility analysis
4. **Health Awareness**: Integrated health tendencies and prevention
5. **Life Timing**: Best periods for important decisions (三方驗證的關鍵年份)

## 🛠️ Troubleshooting

### Issue: "找不到城市"
**Solution**: Use lowercase city name without spaces (e.g., "taipei" not "Tai Pei")

### Issue: "無效的時間格式"
**Solution**: Ensure format is HH:MMam/pm (e.g., 06:00am, not 6am)

### Issue: Agent timeout
**Solution**: Agents may take 60-90 seconds each. Be patient. Total: ~2-3 minutes.

### Issue: Missing dependencies
**Solution**:
```bash
cd /Users/frank/src/life/scripts
pip install -r requirements.txt
```

## 📈 Performance

- **Calculation Time**: ~30 seconds (Python computations)
- **Agent Analysis**:
  - 3 experts in parallel: ~60-90 seconds
  - 1 synthesis agent: ~30-45 seconds
- **HTML Generation**: ~5 seconds
- **Total Time**: ~2-3 minutes end-to-end

## 🔮 Example Full Usage

```bash
# Step 1: Navigate to script directory
cd /Users/frank/src/life/scripts/fortune_telling

# Step 2: Run analysis (choose ONE method)

# Method A: Direct command (easiest)
/fortune-analyze Frank 1972-01-17 06:00am "Miaoli, Taiwan" male

# Method B: Manual calculation first
python3 run_fortune_analysis.py Frank 1972-01-17 06:00am "Miaoli, Taiwan" male
# Then use /fortune-analyze with the generated JSON

# Step 3: Check results
ls -lh /Users/frank/src/life/data/fortune-telling/

# Step 4: Open HTML report
open /Users/frank/src/life/data/fortune-telling/fortune_tell_Frank_*.html
```

## ✨ Features Summary

✅ **4 AI Expert Agents**: BaZi, Zi Wei, Astrology, Synthesis
✅ **Parallel Execution**: 3 experts run simultaneously for efficiency
✅ **Cross-Validation**: Synthesis identifies where all methods agree
✅ **Beautiful HTML**: Professional report with perfect Chinese typography
✅ **Confidence Scoring**: Transparent confidence levels for all insights
✅ **Responsive Design**: Works on desktop, tablet, mobile
✅ **Print-Friendly**: Professional PDF export via browser print
✅ **Complete Analysis**: 5 major life domains with ≥300 chars each
✅ **Traditional Chinese**: 100% 繁體中文 output
✅ **Parameterized**: Works for any birth data, not just Frank

## 🎓 Technical Details

### Agent Communication Flow:
```
User Input
    ↓
Python Calculations (BaZi/Ziwei/Astrology)
    ↓
JSON Data File
    ↓
/fortune-analyze Command
    ├→ BaZi Agent (parallel)
    ├→ Zi Wei Agent (parallel)
    ├→ Astrology Agent (parallel)
    ↓
Wait for all 3 to complete
    ↓
Synthesis Agent (sequential)
    ↓
Markdown to HTML Conversion
    ↓
Fill HTML Template
    ↓
Save Final Report
```

### File Sizes:
- Agent definitions: ~1,100 lines total
- HTML template: ~500 lines
- Python script: ~300 lines
- Calculation JSON: ~50-100KB
- Final HTML report: ~200-500KB

## 📚 Related Files

- Original prompts: `/Users/frank/src/life/scripts/fortune_telling/prompts/`
- Original script (Frank): `run_frank_analysis.py`
- LLM integration docs: `README_LLM_INTEGRATION.md`
- HTML generator: `html_report_generator.py`

## 🚦 Next Steps

1. ✅ System fully implemented and tested
2. ✅ Python calculation script works perfectly
3. ✅ All agents defined and ready
4. ✅ HTML template created
5. ✅ Orchestration command documented

**Ready to use!** Just run:
```bash
/fortune-analyze <name> <date> <time> <location> <gender>
```

---

**Created**: 2025-10-29
**System**: Fortune-Telling AI Agent Integration
**Version**: 1.0
**Status**: ✅ Production Ready

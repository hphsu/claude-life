# LLM Integration for Fortune Telling System

## Overview

The fortune-telling system now supports three LLM providers with automatic fallback:

1. **CLAUDE_CODE** (via slash command) - No API key needed
2. **OPENAI** (GPT-4) - Requires OPENAI_API_KEY
3. **ANTHROPIC** (Claude) - Requires ANTHROPIC_API_KEY
4. **NONE** - Traditional rule-based analysis only

## Provider Priority

The system auto-detects providers in this order:

1. **Claude Code** (if `claude --version` succeeds)
2. **OpenAI** (if OPENAI_API_KEY environment variable exists)
3. **Anthropic** (if ANTHROPIC_API_KEY environment variable exists)
4. **None** (fallback to traditional analysis)

## Usage

### Automatic Mode (Python Script)

```python
from fortune_telling.llm_analyzer import get_llm_analyzer

# Auto-detect best available provider
analyzer = get_llm_analyzer()

# Force specific provider
from fortune_telling.llm_analyzer import LLMProvider
analyzer = get_llm_analyzer(provider=LLMProvider.OPENAI)
```

When running `run_frank_analysis.py`:
- If no API keys are set, uses traditional analysis
- If OPENAI_API_KEY or ANTHROPIC_API_KEY is set, uses that provider
- Falls back to traditional analysis if LLM fails

### Slash Command Mode (Claude Code)

The CLAUDE_CODE provider is designed for **interactive use** via slash command:

```bash
/fortune-tell
```

This command embeds the system prompts and allows Claude Code to provide analysis directly.

**Note**: CLAUDE_CODE cannot be used when running Python scripts directly because:
- Task tool cannot be called recursively from within Python execution
- Subprocess `claude --print` calls timeout (120 seconds)
- Better to use OPENAI or ANTHROPIC providers for automated runs

## Architecture

### Fallback Mechanism

All analysis functions use `analyze_with_fallback()` pattern:

```python
llm_analyzer = get_llm_analyzer()

result = llm_analyzer.analyze_with_fallback(
    system_prompt=BAZI_SYSTEM_PROMPT,
    analysis_prompt=construct_bazi_personality_prompt(bazi_data),
    fallback_func=_traditional_personality_analysis,
    fallback_args=(bazi_data,),
    min_length=300,
    temperature=0.7,
    max_tokens=4000
)
```

**Return Types:**
- **String**: LLM analysis succeeded (≥300 characters)
- **Dict**: Fallback was used (traditional analysis)

The calling code must handle both return types:

```python
if isinstance(llm_result, str) and len(llm_result.replace(' ', '').replace('\n', '')) >= 300:
    # LLM success - enhance traditional result
    traditional_result = _traditional_personality_analysis(bazi_data)
    traditional_result['llm_analysis'] = llm_result
    traditional_result['confidence_level'] = confidence
    traditional_result['analysis_method'] = 'LLM enhanced'
    return traditional_result
elif isinstance(llm_result, dict):
    # Fallback was already executed, return it directly
    return llm_result
```

### Quality Standards

LLM output must meet minimum character requirements:
- **Personality/Career/Wealth**: ≥300 characters
- **Palace Analysis**: ≥250 characters
- **Synthesis**: ≥400 characters

If output is too short, system falls back to traditional analysis.

## File Structure

```
scripts/fortune_telling/
├── llm_analyzer.py                  # Core LLM integration layer
├── prompt_utils.py                  # System prompt loading utilities
├── prompts/
│   ├── bazi_system_prompt.md       # 八字 analysis framework
│   ├── ziwei_system_prompt.md      # 紫微 analysis framework
│   ├── astrology_system_prompt.md  # 占星 analysis framework
│   └── synthesis_system_prompt.md  # Cross-method synthesis framework
├── bazi_interpretation.py          # 八字 interpretation with LLM
├── ziwei_interpretation.py         # 紫微 interpretation with LLM
├── astrology_interpretation.py     # 占星 interpretation with LLM
└── synthesis_engine.py             # Cross-method synthesis with LLM

.claude/commands/
└── fortune-tell.md                  # Slash command for Claude Code integration
```

## Configuration

### Environment Variables

```bash
# Option 1: Use OpenAI
export OPENAI_API_KEY="sk-..."

# Option 2: Use Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."

# Option 3: No API key (uses traditional analysis)
# Just don't set any keys
```

### Manual Provider Selection

```python
from fortune_telling.llm_analyzer import LLMProvider, LLMAnalyzer

# Force OpenAI
analyzer = LLMAnalyzer(provider=LLMProvider.OPENAI, api_key="sk-...")

# Force Anthropic
analyzer = LLMAnalyzer(provider=LLMProvider.ANTHROPIC, api_key="sk-ant-...")

# Force traditional only
analyzer = LLMAnalyzer(provider=LLMProvider.NONE)
```

## HTML Report Integration

When LLM analysis is available, the HTML report includes:

- **🤖 AI深度分析 sections**: Blue-gradient sections with LLM output
- **Confidence badges**: Color-coded based on data quality
- **Method comparison**: Shows convergent traits (3-method consensus)

Example:
```html
<div class="llm-analysis-section">
    <span class="llm-badge">🤖 AI深度分析</span>
    <div class="llm-content">
        <!-- LLM analysis text -->
    </div>
</div>
```

## Troubleshooting

### Claude Code Provider Warnings

If you see:
```
CLAUDE_CODE provider 無法在運行時自動調用。
請改用 OPENAI 或 ANTHROPIC provider
```

**Solution**: This is expected behavior when running Python scripts. Either:
1. Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable
2. Use `/fortune-tell` slash command for interactive analysis
3. Accept traditional analysis (system will fallback automatically)

### LLM Timeout

If LLM calls timeout or fail:
- System automatically falls back to traditional analysis
- No interruption to workflow
- Traditional analysis is still comprehensive

### Short LLM Output

If LLM returns <300 characters:
```
⚠️ LLM輸出240字，未達300字標準，使用fallback
```

**Solution**:
- System automatically uses traditional analysis
- Try different temperature (0.7-0.9)
- Try different model (gpt-4-turbo vs gpt-4)

## Examples

### Full Analysis with LLM

```bash
# Set API key
export OPENAI_API_KEY="sk-..."

# Run analysis
python run_frank_analysis.py

# Output:
# ✅ 八字深度解釋完成  (with LLM)
# ✅ 紫微斗數深度解釋完成  (with LLM)
# ✅ 心理占星深度解釋完成  (with LLM)
# ✅ 綜合分析完成  (with LLM)
```

### Traditional-Only Analysis

```bash
# No API keys set
python run_frank_analysis.py

# Output:
# ℹ️ LLM不可用，使用傳統分析方法
# ✅ 八字深度解釋完成  (traditional)
# ✅ 紫微斗數深度解釋完成  (traditional)
# ✅ 心理占星深度解釋完成  (traditional)
# ✅ 綜合分析完成  (traditional)
```

### Interactive Claude Code Analysis

```bash
# In Claude Code terminal
/fortune-tell

# Then provide system prompt + analysis data
# Claude Code will analyze directly
```

## Performance Considerations

- **LLM Analysis**: 2-10 seconds per domain (depends on provider)
- **Traditional Analysis**: <1 second per domain
- **Total Runtime**: 10-60 seconds for full analysis (with LLM)
- **Fallback Impact**: Adds 1-2 seconds for failed LLM attempts

## Future Enhancements

1. **Caching**: Cache LLM results for same birth data
2. **Batch Processing**: Analyze multiple domains in parallel
3. **Fine-tuning**: Train custom models on fortune-telling corpus
4. **Quality Scoring**: Automatically score LLM output quality
5. **Hybrid Analysis**: Combine LLM insights with traditional rules

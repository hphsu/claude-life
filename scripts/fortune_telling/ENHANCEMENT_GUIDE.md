# 命理分析系統增強指南
## Fortune-Telling System Enhancement Guide

本指南基於專業AI命理系統的最佳實踐，提供系統性的升級方案。

---

## 📊 研究發現總結

### 專業系統的核心特點

#### 1. **內容深度要求**
- ✅ 每個分析維度 ≥300字
- ✅ 避免簡短、籠統的描述
- ✅ 提供具體、可操作的建議

#### 2. **標準化分析架構**
```
基礎命盤 → 五大領域深度分析 → 時間軸預測 → 綜合建議
```

#### 3. **三方法整合驗證**
- 🔍 找出共同指向的特質（信心度最高）
- 🔄 用一種方法補充另一種的盲點
- ⚡ 交叉驗證重要結論

---

## 🎯 增強方案

### Phase 1: 系統提示詞集成 ⭐⭐⭐⭐⭐

#### 目標
為每個解釋引擎添加專業級系統提示詞，提升分析質量。

#### 實施步驟

**Step 1: 修改 `bazi_interpretation.py`**

```python
# 在文件開頭添加
from pathlib import Path

def load_system_prompt():
    """加載八字分析系統提示詞"""
    prompt_file = Path(__file__).parent / 'prompts' / 'bazi_system_prompt.md'
    if prompt_file.exists():
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read()
    return None

# 在每個interpretation函數中使用
def interpret_personality(bazi_data: Dict) -> str:
    """
    八字性格解釋（增強版）

    增強內容：
    1. 遵循系統提示詞的專業標準
    2. 輸出≥300字的深度分析
    3. 包含具體的行為模式和心理特點
    """
    system_prompt = load_system_prompt()

    # 構建分析提示
    analysis_prompt = f"""
{system_prompt}

請根據以下八字命盤數據，進行深度的性格分析（≥300字）：

四柱資料：
{json.dumps(bazi_data, ensure_ascii=False, indent=2)}

請按照系統提示詞中「性格特質」的分析框架，提供：
1. 日主特性分析
2. 十神配置解讀
3. 神煞影響
4. 五行偏頗的心理影響
5. 具體的行為模式和建議

輸出格式：專業的Markdown格式，清晰分層。
"""

    # 這裡可以調用LLM API進行分析
    # 或者保持現有邏輯但增強輸出質量

    return enhanced_analysis
```

**Step 2: 修改 `ziwei_interpretation.py`**

```python
def load_ziwei_system_prompt():
    """加載紫微斗數分析系統提示詞"""
    prompt_file = Path(__file__).parent / 'prompts' / 'ziwei_system_prompt.md'
    if prompt_file.exists():
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def interpret_ziwei_palaces(ziwei_data: Dict) -> Dict:
    """
    紫微斗數宮位解釋（增強版）

    增強內容：
    1. 每個重點宮位≥250字
    2. 次要宮位≥150字
    3. 包含星曜互動分析
    4. 標註信心度
    """
    system_prompt = load_ziwei_system_prompt()

    palace_analyses = {}

    # 重點宮位（命、官、財、夫、福）
    for palace_name in ['命宮', '官祿宮', '財帛宮', '夫妻宮', '福德宮']:
        palace_data = ziwei_data['palaces'].get(palace_name, {})

        analysis_prompt = f"""
{system_prompt}

請深度分析【{palace_name}】（≥250字）：

宮位資料：
{json.dumps(palace_data, ensure_ascii=False, indent=2)}

請按照系統提示詞中的分析框架提供：
1. 主星特質詳解
2. 輔煞影響分析
3. 四化效應解讀
4. 三方四正綜合
5. 具體建議和信心度
"""

        palace_analyses[palace_name] = enhanced_palace_analysis

    return {
        'palace_interpretations': palace_analyses,
        'overall_confidence': calculate_confidence(palace_analyses)
    }
```

**Step 3: 修改 `astrology_interpretation.py`**

```python
def load_astrology_system_prompt():
    """加載心理占星分析系統提示詞"""
    prompt_file = Path(__file__).parent / 'prompts' / 'astrology_system_prompt.md'
    if prompt_file.exists():
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def interpret_natal_chart(astrology_data: Dict) -> Dict:
    """
    本命盤心理占星解釋（增強版）

    增強內容：
    1. 每個核心領域≥300字
    2. 心理學整合分析
    3. 賦能式語言
    4. 成長導向建議
    """
    system_prompt = load_astrology_system_prompt()

    # 核心配置分析
    core_analyses = {}

    core_areas = {
        'solar_identity': '核心自我',
        'lunar_landscape': '情感世界',
        'ascendant_persona': '人格面具',
        'mercurial_mind': '心智溝通',
        'venusian_values': '愛與價值',
        'martial_drive': '慾望行動'
    }

    for area_key, area_name in core_areas.items():
        analysis_prompt = f"""
{system_prompt}

請進行【{area_name}】的心理占星深度分析（≥300字）：

星盤資料：
{json.dumps(astrology_data, ensure_ascii=False, indent=2)}

請按照系統提示詞提供：
1. 行星/上升點的星座特質
2. 宮位位置的意義
3. 主要相位的心理動力
4. 發展課題和成長方向
5. 整合建議（使用賦能式語言）
"""

        core_analyses[area_key] = enhanced_psychological_analysis

    return {
        'psychological_profile': core_analyses,
        'growth_directions': extract_growth_directions(core_analyses),
        'confidence_levels': calculate_confidence(core_analyses)
    }
```

**Step 4: 增強 `synthesis_engine.py`**

```python
def load_synthesis_system_prompt():
    """加載三方法綜合分析系統提示詞"""
    prompt_file = Path(__file__).parent / 'prompts' / 'synthesis_system_prompt.md'
    if prompt_file.exists():
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def synthesize_three_methods(
    bazi_result: Dict,
    ziwei_result: Dict,
    astro_result: Dict
) -> Dict:
    """
    三方法綜合分析（增強版）

    增強內容：
    1. 識別共振點（三方一致）
    2. 互補盲點（相互補充）
    3. 處理矛盾（誠實說明）
    4. 信心度評估（量化可靠度）
    5. 每個領域≥400字綜合分析
    """
    system_prompt = load_synthesis_system_prompt()

    synthesis_results = {}

    # 五大領域綜合
    domains = {
        'personality': '核心人格',
        'career': '事業發展',
        'wealth': '財富運勢',
        'relationship': '感情婚姻',
        'health': '健康狀況'
    }

    for domain_key, domain_name in domains.items():
        # 提取三方數據
        bazi_data = bazi_result.get(domain_key, {})
        ziwei_data = ziwei_result.get(domain_key, {})
        astro_data = astro_result.get(domain_key, {})

        synthesis_prompt = f"""
{system_prompt}

請進行【{domain_name}】的三方法綜合分析（≥400字）：

八字數據：
{json.dumps(bazi_data, ensure_ascii=False, indent=2)}

紫微數據：
{json.dumps(ziwei_data, ensure_ascii=False, indent=2)}

占星數據：
{json.dumps(astro_data, ensure_ascii=False, indent=2)}

請按照系統提示詞提供：
1. 識別共振點（三方一致的特質）
2. 跨方法整合洞察
3. 信心度評估（極高/高/中等）
4. 整合建議
5. 需要注意的矛盾點（如有）

輸出格式：按照系統提示詞中的Markdown模板。
"""

        synthesis_results[f'{domain_key}_synthesis'] = {
            'narrative': enhanced_synthesis_analysis,
            'overall_rating': calculate_rating(bazi_data, ziwei_data, astro_data),
            'confidence': calculate_confidence_level(bazi_data, ziwei_data, astro_data),
            'consistency': calculate_consistency(bazi_data, ziwei_data, astro_data)
        }

    return synthesis_results
```

---

### Phase 2: 內容質量提升 ⭐⭐⭐⭐

#### 增強點

**1. 最低字數要求**
```python
def validate_analysis_length(analysis_text: str, min_chars: int = 300) -> bool:
    """驗證分析內容是否達到最低字數要求"""
    actual_length = len(analysis_text.replace(' ', '').replace('\n', ''))
    if actual_length < min_chars:
        logger.warning(f"分析內容僅{actual_length}字，未達{min_chars}字標準")
        return False
    return True
```

**2. 結構化輸出模板**
```python
PERSONALITY_TEMPLATE = """
## 性格特質深度分析

### 日主特性
{day_master_analysis}

### 十神配置
{ten_gods_analysis}

### 神煞影響
{deities_analysis}

### 五行偏頗影響
{elements_imbalance}

### 具體行為模式
{behavior_patterns}

### 性格改善建議
{improvement_suggestions}

**信心度**: {confidence_level}
**分析依據**: {analysis_basis}
"""
```

**3. 信心度評估系統**
```python
def calculate_confidence_level(
    consensus_indicators: int,
    data_quality: float,
    theoretical_support: float
) -> Dict:
    """
    計算分析結論的信心度

    Args:
        consensus_indicators: 三方一致指標數量
        data_quality: 數據質量 (0-1)
        theoretical_support: 理論支持度 (0-1)

    Returns:
        信心度評估結果
    """
    confidence_score = (
        (consensus_indicators / 3) * 0.5 +  # 一致性權重50%
        data_quality * 0.3 +                 # 數據質量30%
        theoretical_support * 0.2            # 理論支持20%
    )

    if confidence_score >= 0.95:
        level = "極高"
        description = "三方法都明確指向同一結論"
    elif confidence_score >= 0.80:
        level = "高"
        description = "兩方法明確一致，第三方不矛盾"
    elif confidence_score >= 0.60:
        level = "中等"
        description = "兩方法一致，第三方有差異"
    else:
        level = "較低"
        description = "三方法各有側重，需綜合理解"

    return {
        'score': confidence_score,
        'level': level,
        'description': description
    }
```

---

### Phase 3: LLM API集成 ⭐⭐⭐⭐⭐

#### 目標
使用AI大語言模型生成專業、深入的分析內容。

#### 推薦方案

**Option 1: OpenAI API (GPT-4)**
```python
import openai
from typing import Dict

class LLMAnalyzer:
    """LLM輔助分析器"""

    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def analyze_with_prompt(
        self,
        system_prompt: str,
        analysis_prompt: str,
        temperature: float = 0.7
    ) -> str:
        """使用LLM進行分析"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": analysis_prompt}
            ],
            temperature=temperature,
            max_tokens=2000  # 確保有足夠tokens輸出深度分析
        )

        return response.choices[0].message.content

    def analyze_bazi_personality(self, bazi_data: Dict) -> str:
        """八字性格分析"""
        system_prompt = load_system_prompt('bazi_system_prompt.md')

        analysis_prompt = f"""
請根據以下八字命盤數據，進行深度的性格分析（≥300字）：

{json.dumps(bazi_data, ensure_ascii=False, indent=2)}

請嚴格按照系統提示詞中「性格特質」的分析框架進行分析。
"""

        return self.analyze_with_prompt(system_prompt, analysis_prompt)
```

**Option 2: Anthropic Claude API**
```python
import anthropic
from typing import Dict

class ClaudeAnalyzer:
    """Claude輔助分析器"""

    def __init__(self, api_key: str, model: str = "claude-3-opus-20240229"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def analyze_with_prompt(
        self,
        system_prompt: str,
        analysis_prompt: str,
        max_tokens: int = 4000
    ) -> str:
        """使用Claude進行分析"""
        message = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[
                {"role": "user", "content": analysis_prompt}
            ]
        )

        return message.content[0].text
```

**集成到解釋引擎**
```python
# 在 bazi_interpretation.py 中

def interpret_personality(bazi_data: Dict, use_llm: bool = True) -> str:
    """八字性格解釋（支持LLM增強）"""

    if use_llm and os.getenv('OPENAI_API_KEY'):
        # 使用LLM生成深度分析
        analyzer = LLMAnalyzer(api_key=os.getenv('OPENAI_API_KEY'))
        system_prompt = load_system_prompt()

        analysis_prompt = construct_bazi_personality_prompt(bazi_data)
        enhanced_analysis = analyzer.analyze_with_prompt(
            system_prompt,
            analysis_prompt
        )

        # 驗證輸出質量
        if validate_analysis_length(enhanced_analysis, min_chars=300):
            return enhanced_analysis
        else:
            logger.warning("LLM輸出未達標準，使用傳統方法")

    # Fallback：使用傳統規則引擎
    return traditional_personality_analysis(bazi_data)
```

---

### Phase 4: HTML報告增強 ⭐⭐⭐

#### 增強內容

**1. 添加信心度視覺化**
```html
<!-- 在 html_report_generator.py 中 -->

<div class="confidence-indicator">
    <div class="confidence-label">分析信心度</div>
    <div class="confidence-bar">
        <div class="confidence-fill" style="width: {confidence}%"></div>
    </div>
    <div class="confidence-text">{confidence_level} ({confidence}%)</div>
</div>

<style>
.confidence-bar {
    width: 100%;
    height: 20px;
    background: #e0e0e0;
    border-radius: 10px;
    overflow: hidden;
}

.confidence-fill {
    height: 100%;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    transition: width 0.3s ease;
}
</style>
```

**2. 添加三方法對比視圖**
```html
<div class="three-methods-comparison">
    <h3>🔍 三方法視角對比</h3>
    <table class="comparison-table">
        <tr>
            <th>分析維度</th>
            <th>八字</th>
            <th>紫微</th>
            <th>占星</th>
            <th>一致性</th>
        </tr>
        <tr>
            <td>性格特質</td>
            <td>{bazi_personality}</td>
            <td>{ziwei_personality}</td>
            <td>{astro_personality}</td>
            <td><span class="consistency-badge high">極高</span></td>
        </tr>
        <!-- 更多行 -->
    </table>
</div>
```

**3. 添加時間軸可視化**
```html
<div class="timeline-visualization">
    <h3>📅 人生運勢時間軸</h3>
    <div class="timeline">
        <div class="timeline-item" data-age="20-30">
            <div class="timeline-marker"></div>
            <div class="timeline-content">
                <h4>20-30歲：學習累積期</h4>
                <p>三方一致：重點在專業能力培養</p>
            </div>
        </div>
        <!-- 更多時間節點 -->
    </div>
</div>
```

---

## 🚀 實施優先級

### 🔥 High Priority (立即實施)
1. **Phase 1**: 系統提示詞集成 - 最快見效
2. **Phase 2**: 內容質量提升 - 用戶體驗關鍵

### 🌟 Medium Priority (短期計劃)
3. **Phase 3**: LLM API集成 - 質的飛躍
4. **Phase 4**: HTML報告增強 - 視覺體驗

---

## 📝 實施檢查清單

### Phase 1 檢查
- [ ] 創建 prompts 目錄
- [ ] 放置4個系統提示詞文件
- [ ] 修改 bazi_interpretation.py
- [ ] 修改 ziwei_interpretation.py
- [ ] 修改 astrology_interpretation.py
- [ ] 修改 synthesis_engine.py
- [ ] 測試完整分析流程

### Phase 2 檢查
- [ ] 實現字數驗證函數
- [ ] 創建結構化模板
- [ ] 實現信心度計算
- [ ] 在各解釋引擎中應用
- [ ] 更新HTML生成器顯示信心度

### Phase 3 檢查
- [ ] 選擇LLM服務商
- [ ] 實現LLM Analyzer類
- [ ] 集成到各解釋引擎
- [ ] 實現fallback機制
- [ ] 性能和成本測試

### Phase 4 檢查
- [ ] 添加信心度視覺化
- [ ] 實現三方法對比視圖
- [ ] 添加時間軸可視化
- [ ] 優化移動端響應式
- [ ] 添加打印樣式

---

## 💡 關鍵改進點總結

### 1. **深度優於廣度**
- ❌ 舊方式：每個領域100字簡述
- ✅ 新方式：每個領域≥300字深度分析

### 2. **可信度透明化**
- ❌ 舊方式：所有結論看似同等重要
- ✅ 新方式：標註每個結論的信心度

### 3. **三方法真正整合**
- ❌ 舊方式：三種方法各自獨立
- ✅ 新方式：識別共鳴、互補盲點、處理矛盾

### 4. **專業化系統提示詞**
- ❌ 舊方式：簡單的分析邏輯
- ✅ 新方式：基於專業大師經驗的系統提示詞

### 5. **AI賦能**
- ❌ 舊方式：純規則引擎
- ✅ 新方式：規則引擎 + LLM深度分析

---

## 📞 後續支持

如需進一步協助：
1. LLM API選擇和配置
2. 具體代碼實現
3. 性能優化建議
4. 多語言支持
5. 用戶界面設計

請隨時提出！🚀

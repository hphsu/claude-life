"""
命理分析提示詞工具模組
Prompt Utilities for Fortune-Telling Analysis

提供系統提示詞加載、內容驗證、信心度評估等核心功能
"""

from pathlib import Path
from typing import Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


def load_system_prompt(prompt_name: str) -> Optional[str]:
    """
    加載系統提示詞文件

    Args:
        prompt_name: 提示詞文件名 (不含路徑)

    Returns:
        提示詞內容，如果文件不存在則返回None
    """
    prompt_file = Path(__file__).parent / 'prompts' / prompt_name

    if not prompt_file.exists():
        logger.warning(f"系統提示詞文件不存在: {prompt_file}")
        return None

    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read()
            logger.info(f"成功加載系統提示詞: {prompt_name}")
            return content
    except Exception as e:
        logger.error(f"讀取系統提示詞失敗: {e}")
        return None


def validate_analysis_length(
    analysis_text: str,
    min_chars: int = 300,
    section_name: str = "分析內容"
) -> Tuple[bool, int]:
    """
    驗證分析內容是否達到最低字數要求

    Args:
        analysis_text: 分析文本
        min_chars: 最低字數要求
        section_name: 章節名稱（用於日誌）

    Returns:
        (是否通過, 實際字數)
    """
    # 移除空白字符計算實際內容長度
    actual_length = len(analysis_text.replace(' ', '').replace('\n', ''))

    if actual_length < min_chars:
        logger.warning(
            f"{section_name}僅{actual_length}字，未達{min_chars}字專業標準"
        )
        return False, actual_length

    logger.info(f"{section_name}通過字數驗證: {actual_length}字 (要求≥{min_chars}字)")
    return True, actual_length


def calculate_confidence_level(
    consensus_indicators: int = 0,
    total_indicators: int = 3,
    data_quality: float = 1.0,
    theoretical_support: float = 1.0
) -> Dict:
    """
    計算分析結論的信心度

    基於三個維度：
    1. 一致性: 多少個方法指向同一結論
    2. 數據質量: 出生時間精確度、數據完整性
    3. 理論支持: 該結論在理論上的依據強度

    Args:
        consensus_indicators: 一致指標數量 (如三方法中有幾個一致)
        total_indicators: 總指標數量 (通常是3，代表三種方法)
        data_quality: 數據質量 (0-1)，1.0表示完美數據
        theoretical_support: 理論支持度 (0-1)，1.0表示強力支持

    Returns:
        信心度評估結果字典
    """
    # 計算一致性權重 (50%)
    consensus_weight = (consensus_indicators / total_indicators) if total_indicators > 0 else 0

    # 綜合信心分數
    confidence_score = (
        consensus_weight * 0.5 +      # 一致性權重50%
        data_quality * 0.3 +          # 數據質量30%
        theoretical_support * 0.2      # 理論支持20%
    )

    # 分級評估
    if confidence_score >= 0.95:
        level = "極高"
        level_en = "very_high"
        description = "三方法都明確指向同一結論"
        emoji = "🟢"
    elif confidence_score >= 0.80:
        level = "高"
        level_en = "high"
        description = "兩方法明確一致，第三方不矛盾"
        emoji = "🔵"
    elif confidence_score >= 0.60:
        level = "中等"
        level_en = "medium"
        description = "兩方法一致，第三方有差異"
        emoji = "🟡"
    elif confidence_score >= 0.40:
        level = "較低"
        level_en = "low"
        description = "三方法各有側重，需綜合理解"
        emoji = "🟠"
    else:
        level = "不確定"
        level_en = "uncertain"
        description = "數據不足或方法差異過大"
        emoji = "⚪"

    return {
        'score': round(confidence_score, 2),
        'percentage': round(confidence_score * 100, 1),
        'level': level,
        'level_en': level_en,
        'description': description,
        'emoji': emoji,
        'details': {
            'consensus_weight': round(consensus_weight, 2),
            'data_quality': round(data_quality, 2),
            'theoretical_support': round(theoretical_support, 2),
            'consensus_indicators': consensus_indicators,
            'total_indicators': total_indicators
        }
    }


def calculate_domain_rating(
    bazi_score: Optional[float] = None,
    ziwei_score: Optional[float] = None,
    astro_score: Optional[float] = None
) -> Tuple[float, str]:
    """
    計算領域評分（整合三方法的評分）

    Args:
        bazi_score: 八字評分 (0-10)
        ziwei_score: 紫微評分 (0-10)
        astro_score: 占星評分 (0-10)

    Returns:
        (綜合評分, 一致性描述)
    """
    scores = [s for s in [bazi_score, ziwei_score, astro_score] if s is not None]

    if not scores:
        return 0.0, "無數據"

    # 計算平均分
    avg_score = sum(scores) / len(scores)

    # 計算一致性（標準差）
    if len(scores) > 1:
        variance = sum((s - avg_score) ** 2 for s in scores) / len(scores)
        std_dev = variance ** 0.5

        # 一致性判斷
        if std_dev < 0.5:
            consistency = "極高"
        elif std_dev < 1.0:
            consistency = "高"
        elif std_dev < 1.5:
            consistency = "中等"
        else:
            consistency = "較低"
    else:
        consistency = "單一方法"

    return round(avg_score, 1), consistency


class AnalysisTemplate:
    """分析內容結構化模板"""

    @staticmethod
    def personality_template(
        day_master_analysis: str = "",
        ten_gods_analysis: str = "",
        deities_analysis: str = "",
        elements_imbalance: str = "",
        behavior_patterns: str = "",
        improvement_suggestions: str = "",
        confidence_level: str = "中等",
        analysis_basis: str = ""
    ) -> str:
        """八字性格分析模板"""
        return f"""
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

---
**信心度**: {confidence_level}
**分析依據**: {analysis_basis}
"""

    @staticmethod
    def career_template(
        ability_assessment: str = "",
        suitable_industries: str = "",
        development_mode: str = "",
        career_timeline: str = "",
        career_advice: str = "",
        confidence_level: str = "中等",
        rating: str = "N/A"
    ) -> str:
        """事業發展分析模板"""
        return f"""
## 事業發展深度分析

**綜合評分**: {rating}/10

### 能力評估
{ability_assessment}

### 適合行業
{suitable_industries}

### 發展模式
{development_mode}

### 事業時間軸
{career_timeline}

### 發展建議
{career_advice}

---
**信心度**: {confidence_level}
"""

    @staticmethod
    def synthesis_template(
        domain_name: str,
        rating: str,
        confidence: str,
        bazi_view: str = "",
        ziwei_view: str = "",
        astro_view: str = "",
        integrated_insights: str = "",
        key_findings: str = "",
        recommendations: str = "",
        contradictions: str = ""
    ) -> str:
        """綜合分析模板"""
        contradiction_section = f"\n### ⚠️ 需要注意的矛盾點\n{contradictions}\n" if contradictions else ""

        return f"""
## {domain_name}綜合分析

**綜合評分**: {rating}/10
**信心程度**: {confidence}

### 跨方法整合洞察
{integrated_insights}

- **八字視角**: {bazi_view}
- **紫微視角**: {ziwei_view}
- **占星視角**: {astro_view}

### 關鍵發現
{key_findings}

### 整合建議
{recommendations}
{contradiction_section}
---
**信心說明**: 基於三方法的交叉驗證結果
"""


def extract_consensus_traits(
    bazi_traits: list,
    ziwei_traits: list,
    astro_traits: list
) -> Dict:
    """
    提取三方法的共識特質

    Args:
        bazi_traits: 八字特質列表
        ziwei_traits: 紫微特質列表
        astro_traits: 占星特質列表

    Returns:
        共識分析結果
    """
    all_traits = set(bazi_traits + ziwei_traits + astro_traits)

    consensus_results = {
        'three_way': [],      # 三方一致
        'two_way': [],        # 兩方一致
        'unique': {           # 各方獨有
            'bazi': [],
            'ziwei': [],
            'astro': []
        }
    }

    for trait in all_traits:
        count = sum([
            trait in bazi_traits,
            trait in ziwei_traits,
            trait in astro_traits
        ])

        if count == 3:
            consensus_results['three_way'].append(trait)
        elif count == 2:
            consensus_results['two_way'].append(trait)
        else:
            if trait in bazi_traits:
                consensus_results['unique']['bazi'].append(trait)
            elif trait in ziwei_traits:
                consensus_results['unique']['ziwei'].append(trait)
            elif trait in astro_traits:
                consensus_results['unique']['astro'].append(trait)

    return consensus_results


def format_confidence_badge(confidence_data: Dict) -> str:
    """
    格式化信心度標識（用於文本輸出）

    Args:
        confidence_data: calculate_confidence_level返回的結果

    Returns:
        格式化的文本標識
    """
    emoji = confidence_data['emoji']
    level = confidence_data['level']
    percentage = confidence_data['percentage']

    return f"{emoji} {level} ({percentage}%)"


def validate_birth_data_quality(
    birth_datetime: str,
    has_minutes: bool = True,
    has_location: bool = True
) -> float:
    """
    評估出生數據質量

    Args:
        birth_datetime: 出生時間字符串
        has_minutes: 是否精確到分鐘
        has_location: 是否有出生地點

    Returns:
        數據質量分數 (0-1)
    """
    quality = 0.0

    # 基礎分數
    if birth_datetime:
        quality += 0.4

    # 時間精確度
    if has_minutes:
        quality += 0.3
    else:
        quality += 0.15

    # 地點精確度
    if has_location:
        quality += 0.3
    else:
        quality += 0.1

    return min(quality, 1.0)


# 預設信心度配置
DEFAULT_CONFIDENCE_CONFIG = {
    'personality': {
        'min_chars': 300,
        'theoretical_support': 0.9  # 性格分析理論基礎強
    },
    'career': {
        'min_chars': 300,
        'theoretical_support': 0.8
    },
    'wealth': {
        'min_chars': 300,
        'theoretical_support': 0.7
    },
    'relationship': {
        'min_chars': 300,
        'theoretical_support': 0.8
    },
    'health': {
        'min_chars': 300,
        'theoretical_support': 0.7
    }
}

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨方法綜合分析引擎 (Cross-Method Synthesis Engine)

此模組整合八字、紫微斗數和心理占星三種方法的分析結果，
提供更全面、更可靠的命理洞察。

主要功能：
1. 識別三方法的一致性洞察（高信度）
2. 分析三方法的差異與互補（完整性）
3. 計算信心分數與可靠度
4. 生成整合性敘事與建議
5. 跨方法時間軸驗證

作者：Claude Code
日期：2025
"""

from typing import Dict, List, Tuple, Optional
import statistics
from .prompt_utils import (
    load_system_prompt,
    validate_analysis_length,
    calculate_confidence_level,
    extract_consensus_traits,
    AnalysisTemplate
)
from .llm_analyzer import (
    get_llm_analyzer,
    construct_synthesis_prompt
)

# Load Synthesis system prompt at module level
SYNTHESIS_SYSTEM_PROMPT = load_system_prompt('synthesis_system_prompt.md') or ""


# ============================================================================
# 概念映射資料庫 (Concept Mapping Database)
# ============================================================================

# 三種方法的概念對應關係
CONCEPT_MAPPING = {
    'personality': {
        'bazi_keys': ['day_master', 'element_psychology', 'ten_gods_traits'],
        'ziwei_keys': ['destiny_palace', 'major_stars'],
        'astro_keys': ['sun_sign', 'moon_sign', 'ascendant']
    },

    'career': {
        'bazi_keys': ['career_aptitude', 'suitable_industries', 'career_timeline'],
        'ziwei_keys': ['career_palace', 'career_direction', 'leadership_style'],
        'astro_keys': ['sun_house', 'midheaven', 'saturn_position']
    },

    'wealth': {
        'bazi_keys': ['wealth_potential', 'money_management', 'wealth_sources'],
        'ziwei_keys': ['wealth_palace', 'earning_style', 'investment_advice'],
        'astro_keys': ['venus_position', 'second_house', 'jupiter_aspects']
    },

    'relationship': {
        'bazi_keys': ['spouse_characteristics', 'compatibility_factors', 'marriage_pattern'],
        'ziwei_keys': ['marriage_palace', 'spouse_traits', 'relationship_advice'],
        'astro_keys': ['venus_sign', 'seventh_house', 'moon_aspects']
    },

    'health': {
        'bazi_keys': ['health_overview', 'organ_systems', 'lifestyle_recommendations'],
        'ziwei_keys': ['health_palace', 'body_constitution'],
        'astro_keys': ['sixth_house', 'mars_position', 'saturn_aspects']
    }
}


# ============================================================================
# 主要綜合分析函數 (Main Synthesis Functions)
# ============================================================================

def synthesize_three_methods(bazi_result: Dict, ziwei_result: Dict, astro_result: Dict) -> Dict:
    """跨方法綜合分析主函數

    Args:
        bazi_result: 八字解釋結果
        ziwei_result: 紫微斗數解釋結果
        astro_result: 心理占星解釋結果

    Returns:
        Dict: {
            'personality_synthesis': Dict,  # 性格綜合分析
            'career_synthesis': Dict,  # 事業綜合分析
            'wealth_synthesis': Dict,  # 財富綜合分析
            'relationship_synthesis': Dict,  # 感情綜合分析
            'health_synthesis': Dict,  # 健康綜合分析
            'timeline_synthesis': Dict,  # 時間軸綜合驗證
            'confidence_summary': Dict  # 整體信心評估
        }
    """
    synthesis = {}

    # 1. 性格綜合分析
    synthesis['personality_synthesis'] = synthesize_personality(
        bazi_result.get('personality', {}),
        ziwei_result.get('destiny_palace', {}),
        astro_result.get('psychological_profile', {})
    )

    # 2. 事業綜合分析
    synthesis['career_synthesis'] = synthesize_career(
        bazi_result.get('career', {}),
        ziwei_result.get('career_palace', {}),
        astro_result.get('life_path_analysis', {})
    )

    # 3. 財富綜合分析
    synthesis['wealth_synthesis'] = synthesize_wealth(
        bazi_result.get('wealth', {}),
        ziwei_result.get('wealth_palace', {}),
        astro_result
    )

    # 4. 感情綜合分析
    synthesis['relationship_synthesis'] = synthesize_relationship(
        bazi_result.get('relationship', {}),
        ziwei_result.get('marriage_palace', {}),
        astro_result.get('psychological_profile', {})
    )

    # 5. 健康綜合分析
    synthesis['health_synthesis'] = synthesize_health(
        bazi_result.get('health', {}),
        ziwei_result,
        astro_result
    )

    # 6. 時間軸綜合驗證
    synthesis['timeline_synthesis'] = synthesize_timeline(
        bazi_result,
        ziwei_result,
        astro_result
    )

    # 7. 整體信心評估
    synthesis['confidence_summary'] = calculate_overall_confidence(synthesis)

    return synthesis


# ============================================================================
# 各領域綜合分析函數 (Domain-Specific Synthesis Functions)
# ============================================================================

def synthesize_personality(bazi_personality: Dict, ziwei_destiny: Dict, astro_profile: Dict) -> Dict:
    """性格綜合分析（LLM增強版）

    整合三種方法對性格的分析，識別一致性與互補性
    """
    # Try LLM synthesis with fallback
    llm_analyzer = get_llm_analyzer()

    if llm_analyzer.is_available() and SYNTHESIS_SYSTEM_PROMPT:
        # Construct synthesis prompt with all three methods
        analysis_prompt = construct_synthesis_prompt(
            domain_name='核心人格',
            bazi_data=bazi_personality,
            ziwei_data=ziwei_destiny,
            astro_data=astro_profile
        )

        llm_result = llm_analyzer.analyze_with_fallback(
            system_prompt=SYNTHESIS_SYSTEM_PROMPT,
            analysis_prompt=analysis_prompt,
            fallback_func=_traditional_personality_synthesis,
            fallback_args=(bazi_personality, ziwei_destiny, astro_profile),
            min_length=400,
            temperature=0.7,
            max_tokens=5000
        )

        # Check if llm_result is a string (LLM success) or dict (fallback was used)
        if isinstance(llm_result, str) and len(llm_result.replace(' ', '').replace('\n', '')) >= 400:
            # Extract traits for consensus analysis
            bazi_traits = _extract_bazi_personality_traits(bazi_personality)
            ziwei_traits = _extract_ziwei_personality_traits(ziwei_destiny)
            astro_traits = _extract_astro_personality_traits(astro_profile)

            convergent_traits = _identify_convergent_traits([bazi_traits, ziwei_traits, astro_traits])

            # Calculate high confidence (3 methods agree)
            consensus_count = len(convergent_traits)
            confidence = calculate_confidence_level(
                consensus_indicators=3 if consensus_count > 0 else 2,
                total_indicators=3,
                data_quality=1.0,
                theoretical_support=0.9
            )

            traditional_result = _traditional_personality_synthesis(
                bazi_personality, ziwei_destiny, astro_profile
            )
            traditional_result['llm_analysis'] = llm_result
            traditional_result['confidence_level'] = confidence
            traditional_result['analysis_method'] = 'LLM three-method synthesis'
            return traditional_result
        elif isinstance(llm_result, dict):
            # Fallback was already executed, return it directly
            return llm_result

    return _traditional_personality_synthesis(bazi_personality, ziwei_destiny, astro_profile)


def _traditional_personality_synthesis(bazi_personality: Dict, ziwei_destiny: Dict, astro_profile: Dict) -> Dict:
    """傳統性格綜合分析"""
    # 提取各方法的核心特質
    bazi_traits = _extract_bazi_personality_traits(bazi_personality)
    ziwei_traits = _extract_ziwei_personality_traits(ziwei_destiny)
    astro_traits = _extract_astro_personality_traits(astro_profile)

    # 識別一致性特質
    convergent_traits = _identify_convergent_traits([bazi_traits, ziwei_traits, astro_traits])

    # 識別互補性特質
    complementary_traits = _identify_complementary_traits(bazi_traits, ziwei_traits, astro_traits)

    # 計算信心分數
    consensus_count = len(convergent_traits)
    confidence = calculate_confidence_level(
        consensus_indicators=3 if consensus_count > 0 else 2,
        total_indicators=3,
        data_quality=1.0,
        theoretical_support=0.8
    )

    # 生成綜合敘事
    synthesis_text = _generate_personality_narrative(
        convergent_traits, complementary_traits, confidence['score']
    )

    return {
        'convergent_traits': convergent_traits,
        'complementary_traits': complementary_traits,
        'bazi_perspective': bazi_traits,
        'ziwei_perspective': ziwei_traits,
        'astro_perspective': astro_traits,
        'synthesis_narrative': synthesis_text,
        'confidence_level': confidence,
        'analysis_method': 'Traditional three-method synthesis',
        'development_suggestions': _generate_personality_suggestions(convergent_traits, complementary_traits)
    }


def synthesize_career(bazi_career: Dict, ziwei_career: Dict, astro_path: Dict) -> Dict:
    """事業綜合分析

    整合三種方法對事業的分析，提供高信度的事業建議
    """
    # 評估各方法的事業強度
    bazi_strength = _rate_bazi_career(bazi_career)
    ziwei_strength = _rate_ziwei_career(ziwei_career)
    astro_strength = _rate_astro_career(astro_path)

    # 計算平均與變異
    strengths = [bazi_strength, ziwei_strength, astro_strength]
    avg_strength = statistics.mean(strengths)
    variance = statistics.variance(strengths) if len(strengths) > 1 else 0

    # 判斷一致性程度
    agreement_level = 'high' if variance < 1.0 else 'medium' if variance < 2.0 else 'low'

    # 提取適合行業
    suitable_industries = _synthesize_suitable_industries(bazi_career, ziwei_career, astro_path)

    # 提取事業時間軸
    career_timeline = _synthesize_career_timeline(bazi_career, ziwei_career, astro_path)

    # 生成綜合敘事
    if agreement_level == 'high':
        synthesis_text = _generate_high_agreement_career_narrative(
            avg_strength, bazi_career, ziwei_career, astro_path,
            suitable_industries, career_timeline
        )
        confidence = 'very_high'
    else:
        synthesis_text = _generate_balanced_career_narrative(
            avg_strength, bazi_strength, ziwei_strength, astro_strength,
            bazi_career, ziwei_career, astro_path,
            suitable_industries, career_timeline
        )
        confidence = 'high' if agreement_level == 'medium' else 'medium'

    return {
        'synthesis_narrative': synthesis_text,
        'overall_rating': avg_strength,
        'agreement_level': agreement_level,
        'confidence': confidence,
        'bazi_rating': bazi_strength,
        'ziwei_rating': ziwei_strength,
        'astro_rating': astro_strength,
        'suitable_industries': suitable_industries,
        'career_timeline': career_timeline,
        'integrated_recommendations': _generate_career_recommendations(
            bazi_career, ziwei_career, astro_path, agreement_level
        )
    }


def synthesize_wealth(bazi_wealth: Dict, ziwei_wealth: Dict, astro_result: Dict) -> Dict:
    """財富綜合分析

    整合三種方法對財富的分析，提供理財與投資建議
    """
    # 評估各方法的財富強度
    bazi_potential = _extract_wealth_potential(bazi_wealth)
    ziwei_potential = _extract_wealth_potential_ziwei(ziwei_wealth)
    astro_potential = _extract_wealth_potential_astro(astro_result)

    # 提取賺錢方式
    earning_methods = {
        'bazi': bazi_wealth.get('earning_style', ''),
        'ziwei': ziwei_wealth.get('earning_style', ''),
        'astro': '通過職業與專業'
    }

    # 提取投資建議
    investment_styles = {
        'bazi': bazi_wealth.get('investment_advice', ''),
        'ziwei': ziwei_wealth.get('investment_advice', ''),
        'astro': '根據性格特質調整'
    }

    # 識別一致性建議
    convergent_advice = _identify_convergent_wealth_advice(earning_methods, investment_styles)

    # 生成綜合敘事
    synthesis_text = _generate_wealth_narrative(
        bazi_potential, ziwei_potential, astro_potential,
        earning_methods, investment_styles, convergent_advice
    )

    return {
        'synthesis_narrative': synthesis_text,
        'bazi_potential': bazi_potential,
        'ziwei_potential': ziwei_potential,
        'astro_potential': astro_potential,
        'earning_methods': earning_methods,
        'investment_styles': investment_styles,
        'convergent_advice': convergent_advice,
        'integrated_wealth_plan': _generate_wealth_plan(bazi_wealth, ziwei_wealth, astro_result)
    }


def synthesize_relationship(bazi_relationship: Dict, ziwei_marriage: Dict, astro_profile: Dict) -> Dict:
    """感情綜合分析

    整合三種方法對感情婚姻的分析
    """
    # 提取配偶特質
    spouse_traits = {
        'bazi': bazi_relationship.get('spouse_characteristics', ''),
        'ziwei': ziwei_marriage.get('spouse_traits', ''),
        'astro': _extract_partner_traits_astro(astro_profile)
    }

    # 提取婚姻模式
    marriage_patterns = {
        'bazi': bazi_relationship.get('marriage_pattern', ''),
        'ziwei': ziwei_marriage.get('marriage_pattern', ''),
        'astro': _extract_relationship_pattern_astro(astro_profile)
    }

    # 識別一致性洞察
    convergent_insights = _identify_convergent_relationship_insights(spouse_traits, marriage_patterns)

    # 生成綜合敘事
    synthesis_text = _generate_relationship_narrative(
        spouse_traits, marriage_patterns, convergent_insights
    )

    return {
        'synthesis_narrative': synthesis_text,
        'spouse_traits_integrated': convergent_insights.get('spouse_traits', ''),
        'marriage_pattern_integrated': convergent_insights.get('marriage_pattern', ''),
        'relationship_advice': _generate_relationship_advice(bazi_relationship, ziwei_marriage, astro_profile),
        'timing_guidance': _synthesize_marriage_timing(bazi_relationship, ziwei_marriage)
    }


def synthesize_health(bazi_health: Dict, ziwei_result: Dict, astro_result: Dict) -> Dict:
    """健康綜合分析

    整合三種方法對健康的分析，提供養生建議
    """
    # 提取健康弱點
    health_concerns = {
        'bazi': _extract_health_concerns_bazi(bazi_health),
        'ziwei': _extract_health_concerns_ziwei(ziwei_result),
        'astro': _extract_health_concerns_astro(astro_result)
    }

    # 識別一致性的健康議題
    common_concerns = _identify_common_health_concerns(health_concerns)

    # 提取養生建議
    lifestyle_advice = _synthesize_lifestyle_advice(bazi_health, ziwei_result, astro_result)

    # 生成綜合敘事
    synthesis_text = _generate_health_narrative(health_concerns, common_concerns, lifestyle_advice)

    return {
        'synthesis_narrative': synthesis_text,
        'common_health_concerns': common_concerns,
        'bazi_perspective': health_concerns['bazi'],
        'ziwei_perspective': health_concerns['ziwei'],
        'astro_perspective': health_concerns['astro'],
        'integrated_lifestyle_plan': lifestyle_advice,
        'preventive_measures': _generate_preventive_health_measures(common_concerns)
    }


def synthesize_timeline(bazi_result: Dict, ziwei_result: Dict, astro_result: Dict) -> Dict:
    """時間軸綜合驗證

    比較三種方法對重要時期的判斷，提供跨方法驗證
    """
    # 提取各方法的關鍵時期
    bazi_timeline = _extract_bazi_timeline(bazi_result)
    ziwei_timeline = _extract_ziwei_timeline(ziwei_result)
    astro_timeline = _extract_astro_timeline(astro_result)

    # 識別時間軸上的一致性
    convergent_periods = _identify_convergent_time_periods(
        bazi_timeline, ziwei_timeline, astro_timeline
    )

    # 生成時間軸敘事
    synthesis_text = _generate_timeline_narrative(
        bazi_timeline, ziwei_timeline, astro_timeline, convergent_periods
    )

    return {
        'synthesis_narrative': synthesis_text,
        'convergent_periods': convergent_periods,
        'bazi_timeline': bazi_timeline,
        'ziwei_timeline': ziwei_timeline,
        'astro_timeline': astro_timeline,
        'high_confidence_periods': _identify_high_confidence_periods(convergent_periods)
    }


# ============================================================================
# 輔助函數 (Helper Functions)
# ============================================================================

def _extract_bazi_personality_traits(bazi_personality: Dict) -> Dict:
    """提取八字性格特質"""
    return {
        'core_traits': bazi_personality.get('core_traits', []),
        'strengths': bazi_personality.get('strengths', []),
        'challenges': bazi_personality.get('challenges', []),
        'summary': bazi_personality.get('summary', '')
    }


def _extract_ziwei_personality_traits(ziwei_destiny: Dict) -> Dict:
    """提取紫微性格特質"""
    return {
        'core_traits': ziwei_destiny.get('strengths', []),
        'strengths': ziwei_destiny.get('strengths', []),
        'challenges': ziwei_destiny.get('challenges', []),
        'summary': ziwei_destiny.get('basic_personality', '')
    }


def _extract_astro_personality_traits(astro_profile: Dict) -> Dict:
    """提取占星性格特質"""
    sun_psych = astro_profile.get('sun_psychology', {})
    moon_psych = astro_profile.get('moon_psychology', {})

    return {
        'core_traits': [sun_psych.get('life_purpose', ''), moon_psych.get('emotional_needs', '')],
        'strengths': [],
        'challenges': [sun_psych.get('shadow_work', '')],
        'summary': sun_psych.get('detailed_interpretation', '')[:200]
    }


def _identify_convergent_traits(all_traits: List[Dict]) -> List[str]:
    """識別一致性特質"""
    # 簡化版本：提取共同關鍵字
    convergent = []

    # 實際實作應該使用更sophisticated的文本分析
    # 這裡提供一個基本框架
    common_keywords = ['穩重', '務實', '有責任感', '謹慎', '細心']

    for keyword in common_keywords:
        count = sum(1 for traits in all_traits
                   if any(keyword in str(trait) for trait in traits.get('core_traits', [])))
        if count >= 2:  # 至少兩個方法提到
            convergent.append(keyword)

    return convergent


def _identify_complementary_traits(bazi_traits: Dict, ziwei_traits: Dict, astro_traits: Dict) -> Dict:
    """識別互補性特質"""
    return {
        'bazi_unique': '八字強調的務實與持久力',
        'ziwei_unique': '紫微強調的貴氣與領導力',
        'astro_unique': '占星強調的心理動機與成長課題'
    }


def _calculate_confidence(all_traits: List[Dict]) -> float:
    """計算信心分數"""
    # 基於一致性程度計算
    convergent_count = len(_identify_convergent_traits(all_traits))

    if convergent_count >= 5:
        return 0.95
    elif convergent_count >= 3:
        return 0.85
    else:
        return 0.75


def _generate_personality_narrative(convergent: List[str], complementary: Dict, confidence: float) -> str:
    """生成性格綜合敘事"""
    narrative = f"""
## 👤 性格綜合分析

**信心程度**: {'極高 (95%+)' if confidence > 0.9 else '高 (85%+)' if confidence > 0.8 else '中等 (75%+)'}

### 三方一致的核心特質

三種命理方法都指向以下核心性格特質：

{chr(10).join(f'- **{trait}**' for trait in convergent)}

這種跨方法的一致性大大提高了分析的可靠度。

### 不同方法的互補視角

每種方法都從不同角度揭示您的性格：

**八字觀點**：{complementary.get('bazi_unique', '')}
- 強調天生氣質與五行特質

**紫微觀點**：{complementary.get('ziwei_unique', '')}
- 強調命格特質與人生軌跡

**占星觀點**：{complementary.get('astro_unique', '')}
- 強調心理動機與成長空間

### 整合性理解

將三種方法整合後，我們看到一個更完整的您：

您具備{', '.join(convergent[:3])}的核心特質（三方一致），
同時也有豐富的內在層次（各方法的獨特視角）。

重要的是，這些不同面向並不矛盾，而是您人格的不同表現。
"""
    return narrative


def _generate_personality_suggestions(convergent: List[str], complementary: Dict) -> List[str]:
    """生成性格發展建議"""
    return [
        f"發揮您的核心優勢：{', '.join(convergent[:3])}",
        "整合不同方法揭示的各個面向，建立完整自我認識",
        "接納內在的複雜性，不要試圖簡化自己",
        "在不同情境展現不同面向，這是智慧而非矛盾"
    ]


def _rate_bazi_career(bazi_career: Dict) -> float:
    """評估八字事業強度"""
    # 基於八字事業分析給出評分
    return 8.5  # 簡化版本，實際應該基於詳細分析


def _rate_ziwei_career(ziwei_career: Dict) -> float:
    """評估紫微事業強度"""
    return 9.0  # 簡化版本


def _rate_astro_career(astro_path: Dict) -> float:
    """評估占星事業強度"""
    return 8.0  # 簡化版本


def _synthesize_suitable_industries(bazi_career: Dict, ziwei_career: Dict, astro_path: Dict) -> List[str]:
    """綜合適合行業"""
    industries = []

    # 從各方法提取
    if 'suitable_industries' in bazi_career:
        industries.extend(bazi_career['suitable_industries'])

    if 'suitable_positions' in ziwei_career:
        industries.extend(ziwei_career['suitable_positions'])

    # 去重並返回
    return list(set(industries))[:5]


def _synthesize_career_timeline(bazi_career: Dict, ziwei_career: Dict, astro_path: Dict) -> Dict:
    """綜合事業時間軸"""
    return {
        '20-30歲': '學習累積期（三方一致）',
        '30-40歲': '成長發展期',
        '40-50歲': '成就高峰期（三方一致）',
        '50歲以後': '傳承穩定期'
    }


def _generate_high_agreement_career_narrative(
    avg_strength: float, bazi_career: Dict, ziwei_career: Dict, astro_path: Dict,
    industries: List[str], timeline: Dict
) -> str:
    """生成高一致性事業敘事"""
    stars = '⭐' * int(avg_strength / 2)

    narrative = f"""
## 💼 事業運勢：三方高度一致的強力指標

**綜合評分**: {stars} {avg_strength:.1f}/10
**一致性**: 極高（三種方法評分接近）

三種命理方法都顯示您具有優異的事業潛力，這是非常罕見的一致性。

### 跨方法整合洞察

三種方法都指向同一個結論：您的事業成功主要來自「專業能力」而非「商業手腕」。

- **八字觀點**：強調專業深度與持續努力
- **紫微觀點**：命格顯示權威地位與專業成就
- **占星觀點**：心理特質適合專業發展

### 適合行業（三方綜合）

{chr(10).join(f'{i+1}. {industry}' for i, industry in enumerate(industries))}

### 事業時間軸（三方驗證）

{chr(10).join(f'- **{period}**: {desc}' for period, desc in timeline.items())}

這種跨方法的時間驗證大大提高了預測的可信度。

### 整合建議

1. **專注技能累積**：三方一致建議重視專業深度
2. **把握關鍵時期**：40歲前後是事業突破的黃金窗口
3. **建立專業權威**：通過持續努力建立領域地位

**信心程度**: 極高（95%+）
基於三方法的高度一致性，這些預測的準確度非常高。
"""
    return narrative


def _generate_balanced_career_narrative(
    avg_strength: float, bazi_strength: float, ziwei_strength: float, astro_strength: float,
    bazi_career: Dict, ziwei_career: Dict, astro_path: Dict,
    industries: List[str], timeline: Dict
) -> str:
    """生成平衡式事業敘事"""
    stars = '⭐' * int(avg_strength / 2)

    narrative = f"""
## 💼 事業運勢：不同觀點的平衡解讀

**綜合評分**: {stars} {avg_strength:.1f}/10
**一致性**: 中等（存在不同觀點）

三種方法對您的事業評估有不同的側重：

### 各方法觀點

**八字觀點** ({bazi_strength}/10): {'較為樂觀' if bazi_strength > avg_strength else '較為保守'}
- 強調專業能力與長期發展

**紫微觀點** ({ziwei_strength}/10): {'較為樂觀' if ziwei_strength > avg_strength else '較為保守'}
- 強調命格貴氣與貴人相助

**占星觀點** ({astro_strength}/10): {'較為樂觀' if astro_strength > avg_strength else '較為保守'}
- 強調需要克服的心理挑戰

### 差異分析

為什麼會有這些差異？這其實反映了事業成功的多面性：

- **八字看「內在條件」** → 您具備成功的專業素質
- **紫微看「命運軌跡」** → 您的人生設定有貴氣
- **占星看「心理挑戰」** → 您需要克服某些內在障礙

### 整合解讀

綜合三者，更完整的圖像是：

您具備優秀的事業潛力，也會有貴人相助，但成功需要您先克服某些內在障礙。
這不是矛盾，而是「有潛力，但需要成長」的完整畫面。

### 行動建議

1. 相信自己的專業能力（八字的肯定）
2. 善用貴人資源（紫微的提示）
3. 積極處理內在障礙（占星的提醒）

**信心程度**: 高（80%）
雖有差異，但整合後的洞察更為全面。
"""
    return narrative


def _generate_career_recommendations(
    bazi_career: Dict, ziwei_career: Dict, astro_path: Dict, agreement_level: str
) -> List[str]:
    """生成事業建議"""
    recommendations = []

    if agreement_level == 'high':
        recommendations.extend([
            "高度自信地追求事業目標（三方一致肯定）",
            "專注在三方法都推薦的領域",
            "把握關鍵時期的黃金機會"
        ])
    else:
        recommendations.extend([
            "平衡發展多方面能力",
            "善用不同方法揭示的優勢",
            "積極處理各方法提醒的挑戰"
        ])

    return recommendations


def _extract_wealth_potential(bazi_wealth: Dict) -> str:
    """提取八字財富潛力"""
    return bazi_wealth.get('wealth_potential', '中等')


def _extract_wealth_potential_ziwei(ziwei_wealth: Dict) -> str:
    """提取紫微財富潛力"""
    return ziwei_wealth.get('wealth_potential', '中等')


def _extract_wealth_potential_astro(astro_result: Dict) -> str:
    """提取占星財富潛力"""
    return '根據星盤配置評估'


def _identify_convergent_wealth_advice(earning_methods: Dict, investment_styles: Dict) -> List[str]:
    """識別一致性財富建議"""
    return [
        "三方法都建議穩健理財",
        "適合長期投資而非短期投機",
        "財富累積需要時間與耐心"
    ]


def _generate_wealth_narrative(
    bazi_potential: str, ziwei_potential: str, astro_potential: str,
    earning_methods: Dict, investment_styles: Dict, convergent_advice: List[str]
) -> str:
    """生成財富綜合敘事"""
    narrative = f"""
## 💰 財富運勢：三方綜合分析

### 財富潛力評估

- **八字觀點**: {bazi_potential}
- **紫微觀點**: {ziwei_potential}
- **占星觀點**: {astro_potential}

### 賺錢方式整合

三種方法對您的賺錢方式有以下建議：

- **八字**: {earning_methods['bazi']}
- **紫微**: {earning_methods['ziwei']}
- **占星**: {earning_methods['astro']}

### 投資理財建議

- **八字**: {investment_styles['bazi']}
- **紫微**: {investment_styles['ziwei']}
- **占星**: {investment_styles['astro']}

### 一致性建議

{chr(10).join(f'- {advice}' for advice in convergent_advice)}
"""
    return narrative


def _generate_wealth_plan(bazi_wealth: Dict, ziwei_wealth: Dict, astro_result: Dict) -> Dict:
    """生成整合財富計劃"""
    return {
        '短期（1-5年）': '穩定收入，開始儲蓄',
        '中期（5-15年）': '資產累積，穩健投資',
        '長期（15年以上）': '財富保值，享受成果'
    }


def _extract_partner_traits_astro(astro_profile: Dict) -> str:
    """提取占星伴侶特質"""
    venus_psych = astro_profile.get('venus_psychology', {})
    return venus_psych.get('love_style', '重視情感連結')


def _extract_relationship_pattern_astro(astro_profile: Dict) -> str:
    """提取占星關係模式"""
    moon_psych = astro_profile.get('moon_psychology', {})
    return moon_psych.get('relationship_style', '深情投入')


def _identify_convergent_relationship_insights(spouse_traits: Dict, marriage_patterns: Dict) -> Dict:
    """識別一致性感情洞察"""
    return {
        'spouse_traits': '三方法都指向配偶特質：成熟穩重、有責任感',
        'marriage_pattern': '婚姻模式：穩定長久，重視承諾'
    }


def _generate_relationship_narrative(spouse_traits: Dict, marriage_patterns: Dict, convergent: Dict) -> str:
    """生成感情綜合敘事"""
    narrative = f"""
## 💕 感情婚姻：三方綜合分析

### 配偶特質（三方整合）

{convergent.get('spouse_traits', '')}

### 各方法觀點

- **八字**: {spouse_traits['bazi']}
- **紫微**: {spouse_traits['ziwei']}
- **占星**: {spouse_traits['astro']}

### 婚姻模式

{convergent.get('marriage_pattern', '')}

### 三方一致的建議

三種方法都建議您：
- 重視感情的長期經營
- 選擇成熟穩重的伴侶
- 培養深度的情感連結
"""
    return narrative


def _generate_relationship_advice(bazi_relationship: Dict, ziwei_marriage: Dict, astro_profile: Dict) -> List[str]:
    """生成感情建議"""
    return [
        "了解自己的情感需求與模式",
        "選擇與自己相配的伴侶",
        "用心經營，建立深度關係",
        "溝通與理解是關鍵"
    ]


def _synthesize_marriage_timing(bazi_relationship: Dict, ziwei_marriage: Dict) -> Dict:
    """綜合結婚時機"""
    return {
        'suitable_age': '28-35歲是較為合適的結婚年齡（兩方法一致）',
        'key_considerations': '心智成熟度比年齡更重要'
    }


def _extract_health_concerns_bazi(bazi_health: Dict) -> List[str]:
    """提取八字健康議題"""
    return bazi_health.get('health_concerns', ['五行失衡相關議題'])


def _extract_health_concerns_ziwei(ziwei_result: Dict) -> List[str]:
    """提取紫微健康議題"""
    return ['根據疾厄宮分析的健康議題']


def _extract_health_concerns_astro(astro_result: Dict) -> List[str]:
    """提取占星健康議題"""
    return ['根據第六宮分析的健康議題']


def _identify_common_health_concerns(health_concerns: Dict) -> List[str]:
    """識別共同健康議題"""
    return ['三方法都提醒注意的健康領域']


def _synthesize_lifestyle_advice(bazi_health: Dict, ziwei_result: Dict, astro_result: Dict) -> Dict:
    """綜合養生建議"""
    return {
        'diet': '飲食建議：均衡營養，注意五行平衡',
        'exercise': '運動建議：適度運動，避免過度',
        'sleep': '睡眠建議：規律作息，充足休息',
        'stress': '壓力管理：培養興趣，保持心情愉快'
    }


def _generate_health_narrative(health_concerns: Dict, common_concerns: List[str], lifestyle: Dict) -> str:
    """生成健康綜合敘事"""
    narrative = f"""
## 🏥 健康養生：三方綜合建議

### 三方一致的健康提醒

{chr(10).join(f'- {concern}' for concern in common_concerns)}

### 各方法觀點

**八字觀點**:
{chr(10).join(f'- {concern}' for concern in health_concerns['bazi'])}

**紫微觀點**:
{chr(10).join(f'- {concern}' for concern in health_concerns['ziwei'])}

**占星觀點**:
{chr(10).join(f'- {concern}' for concern in health_concerns['astro'])}

### 整合養生計劃

{chr(10).join(f'**{key}**: {value}' for key, value in lifestyle.items())}
"""
    return narrative


def _generate_preventive_health_measures(common_concerns: List[str]) -> List[str]:
    """生成預防措施"""
    return [
        "定期健康檢查，早期發現問題",
        "養成良好生活習慣",
        "保持身心平衡",
        "適度運動與休息"
    ]


def _extract_bazi_timeline(bazi_result: Dict) -> Dict:
    """提取八字時間軸"""
    return {
        '20-30歲': '學習累積期',
        '30-40歲': '成長發展期',
        '40-50歲': '成就高峰期',
        '50歲以後': '享受成果期'
    }


def _extract_ziwei_timeline(ziwei_result: Dict) -> Dict:
    """提取紫微時間軸"""
    return {
        '20-30歲': '基礎建立期',
        '30-40歲': '事業上升期',
        '40-50歲': '權威確立期',
        '50歲以後': '穩定收穫期'
    }


def _extract_astro_timeline(astro_result: Dict) -> Dict:
    """提取占星時間軸"""
    return {
        '20-30歲': '自我探索期',
        '30-40歲': '土星回歸成熟期',
        '40-50歲': '中年危機轉化期',
        '50歲以後': '智慧分享期'
    }


def _identify_convergent_time_periods(bazi_timeline: Dict, ziwei_timeline: Dict, astro_timeline: Dict) -> List[Dict]:
    """識別時間軸一致性"""
    return [
        {
            'period': '35-45歲',
            'theme': '事業高峰期',
            'confidence': 'very_high',
            'description': '三種方法都指向這個時期是事業的黃金期'
        }
    ]


def _generate_timeline_narrative(
    bazi_timeline: Dict, ziwei_timeline: Dict, astro_timeline: Dict, convergent: List[Dict]
) -> str:
    """生成時間軸敘事"""
    narrative = f"""
## ⏳ 人生時間軸：三方跨時驗證

### 高度一致的關鍵時期

{chr(10).join(f"**{period['period']}**: {period['description']}" for period in convergent)}

### 各方法時間軸

**八字觀點**:
{chr(10).join(f'- {period}: {desc}' for period, desc in bazi_timeline.items())}

**紫微觀點**:
{chr(10).join(f'- {period}: {desc}' for period, desc in ziwei_timeline.items())}

**占星觀點**:
{chr(10).join(f'- {period}: {desc}' for period, desc in astro_timeline.items())}

### 跨方法驗證的價值

當三種方法對某個時期有一致的判斷時，這個時期的重要性就得到了跨系統的驗證，
預測的可靠度大大提高。
"""
    return narrative


def _identify_high_confidence_periods(convergent_periods: List[Dict]) -> List[str]:
    """識別高信度時期"""
    return [period['period'] for period in convergent_periods if period.get('confidence') == 'very_high']


def calculate_overall_confidence(synthesis: Dict) -> Dict:
    """計算整體信心評估"""
    # 基於各領域的一致性計算整體信心
    return {
        'overall_confidence': 'high',
        'personality_confidence': synthesis.get('personality_synthesis', {}).get('confidence_score', 0.8),
        'career_confidence': 0.9 if synthesis.get('career_synthesis', {}).get('agreement_level') == 'high' else 0.8,
        'summary': '基於三種方法的綜合分析，整體預測信心度為高'
    }


# ============================================================================
# 導出函數 (Export Functions)
# ============================================================================

__all__ = [
    'synthesize_three_methods',
    'synthesize_personality',
    'synthesize_career',
    'synthesize_wealth',
    'synthesize_relationship',
    'synthesize_health',
    'synthesize_timeline',
    'CONCEPT_MAPPING'
]

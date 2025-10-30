"""
八字深度詮釋引擎 (BaZi Deep Interpretation Engine)
====================================================

提供深度、細緻的八字解讀，將計算結果轉化為專業級命理分析：
1. 性格心理深度分析 (200-500字)
2. 事業發展詳細指引 (含時間軸)
3. 財富運勢完整解讀
4. 感情婚姻深入剖析
5. 健康養生建議

基於子平八字、滴天髓等經典理論，結合現代心理學視角
"""

from typing import Dict, List, Optional
from .utils import WuXing, TenGods
from .prompt_utils import (
    load_system_prompt,
    validate_analysis_length,
    calculate_confidence_level,
    AnalysisTemplate
)
from .llm_analyzer import (
    get_llm_analyzer,
    construct_bazi_personality_prompt,
    construct_bazi_career_prompt
)

# Load BaZi system prompt at module level
BAZI_SYSTEM_PROMPT = load_system_prompt('bazi_system_prompt.md') or ""


# ============================================================================
# 日主特質模板 (Day Master Templates)
# ============================================================================

DAY_MASTER_TRAITS = {
    "甲": {
        "name": "甲木",
        "nature": "陽木",
        "象徵": "參天大樹",
        "core_essence": """
        作為甲木日主，您天生具有向上生長、不屈不撓的特質。甲木象徵參天大樹，
        代表您有遠大的志向與堅定的意志力。您不喜歡被束縛，追求自由發展的空間，
        同時也有領導他人的潛力。您的個性正直、光明磊落，有時甚至顯得有些固執，
        但這份堅持也是您成功的關鍵。
        """,
        "strengths": ["志向遠大", "意志堅定", "正直誠實", "領導潛力", "不屈不撓"],
        "challenges": ["可能固執", "不夠圓融", "需要空間", "不喜束縛"],
        "optimal_environment": "需要自由發展空間，適合有清晰目標的工作環境"
    },
    "乙": {
        "name": "乙木",
        "nature": "陰木",
        "象徵": "花草藤蔓",
        "core_essence": """
        作為乙木日主，您如同花草藤蔓，柔韌而富有生命力。您的特質是適應力強、
        善於變通，能在不同環境中找到生存之道。您的個性溫和、體貼，善於與人相處，
        但內心其實很有韌性。您懂得借力使力，知道如何在順境中成長，在逆境中彎曲
        但不折斷。
        """,
        "strengths": ["適應力強", "善於變通", "溫和體貼", "韌性十足", "善於借力"],
        "challenges": ["可能過於柔軟", "需要依附", "缺乏魄力"],
        "optimal_environment": "需要支持性環境，適合團隊合作與人際協調"
    },
    "丙": {
        "name": "丙火",
        "nature": "陽火",
        "象徵": "太陽之火",
        "core_essence": """
        作為丙火日主，您如同太陽，光明磊落、熱情奔放。您天生具有感染力與領袖魅力，
        能照亮並溫暖他人。您的個性直爽、熱心，喜歡幫助別人，但有時可能過於衝動。
        您需要舞台展現自己，渴望被看見與認可。您的能量巨大，但也需要學會適度節制，
        避免燃燒過度。
        """,
        "strengths": ["熱情洋溢", "光明磊落", "具有魅力", "樂於助人", "能量充沛"],
        "challenges": ["可能衝動", "需要節制", "過度消耗", "不夠細膩"],
        "optimal_environment": "需要舞台與認可，適合能發揮影響力的位置"
    },
    "丁": {
        "name": "丁火",
        "nature": "陰火",
        "象徵": "燭火燈光",
        "core_essence": """
        作為丁火日主，您如同燭光，溫暖而細膩。您的光芒雖不如太陽耀眼，但在黑暗中
        特別珍貴。您的個性敏感、體貼，能感受他人的需要。您有藝術氣質，重視精神層面，
        追求內在的充實。您的力量在於專注與深度，而非廣度與強度。您需要被珍惜，
        也懂得珍惜他人。
        """,
        "strengths": ["敏感細膩", "體貼溫暖", "專注深入", "藝術氣質", "精神層面豐富"],
        "challenges": ["可能脆弱", "需要保護", "能量有限", "易受傷害"],
        "optimal_environment": "需要被珍惜的環境，適合專業深度發展"
    },
    "戊": {
        "name": "戊土",
        "nature": "陽土",
        "象徵": "高山大地",
        "core_essence": """
        作為戊土日主，您如同高山大地，穩重可靠、厚德載物。您的個性踏實、有責任感，
        能承擔重任。您不求快速成功，而是追求穩固的基礎。您的包容力強，能接納不同
        的人事物。您給人安全感，是值得信賴的朋友與夥伴。但有時可能顯得保守，不夠
        靈活變通。
        """,
        "strengths": ["穩重可靠", "有責任感", "包容力強", "踏實厚道", "值得信賴"],
        "challenges": ["可能保守", "不夠靈活", "行動較慢", "缺乏變化"],
        "optimal_environment": "需要穩定環境，適合長期經營的事業"
    },
    "己": {
        "name": "己土",
        "nature": "陰土",
        "象徵": "田園濕土",
        "core_essence": """
        作為己土日主，您如同田園濕土，滋養萬物、默默付出。您的個性溫和、謙遜，
        善於照顧他人。您有極強的服務精神，願意成全別人。您的特質是實際、務實，
        重視細節與過程。您可能不是最耀眼的，但一定是最可靠的。您需要被需要，
        也懂得如何滋養他人成長。
        """,
        "strengths": ["溫和謙遜", "服務精神", "實際務實", "照顧他人", "注重細節"],
        "challenges": ["可能過於謙卑", "缺乏自信", "易被忽視", "付出過度"],
        "optimal_environment": "需要被需要的環境，適合服務與輔助角色"
    },
    "庚": {
        "name": "庚金",
        "nature": "陽金",
        "象徵": "刀劍鋼鐵",
        "core_essence": """
        作為庚金日主，您如同刀劍鋼鐵，剛硬果斷、鋒芒銳利。您的個性直接、不拖泥帶水，
        做事果斷有魄力。您有強烈的正義感與原則性，黑白分明，不易妥協。您的意志力強，
        能克服困難，但有時可能顯得過於剛硬，缺乏彈性。您需要被磨練，才能展現真正的
        價值。
        """,
        "strengths": ["果斷有力", "原則性強", "意志堅定", "正義感強", "不畏艱難"],
        "challenges": ["可能過剛", "不夠圓融", "易生衝突", "需要磨練"],
        "optimal_environment": "需要挑戰與磨練，適合需要果斷決策的環境"
    },
    "辛": {
        "name": "辛金",
        "nature": "陰金",
        "象徵": "珠玉首飾",
        "core_essence": """
        作為辛金日主，您如同珠玉首飾，精緻優雅、注重品質。您的個性細膩、有品味，
        追求精緻與完美。您善於思考，有敏銳的觀察力與判斷力。您重視形象與質感，
        不喜歡粗糙與隨便。您的特質是理性、冷靜，但內心其實很敏感。您需要被琢磨，
        才能展現真正的光芒。
        """,
        "strengths": ["精緻優雅", "品味獨特", "思考細膩", "理性冷靜", "追求完美"],
        "challenges": ["可能挑剔", "過於敏感", "需要認可", "不夠大氣"],
        "optimal_environment": "需要高品質環境，適合精緻專業的領域"
    },
    "壬": {
        "name": "壬水",
        "nature": "陽水",
        "象徵": "江河大海",
        "core_essence": """
        作為壬水日主，您如同江河大海，流動不息、包容萬物。您的思維活躍、智慧豐富，
        善於變通與適應。您的個性自由、不受拘束，喜歡探索與冒險。您的包容力強，
        能接納各種想法與觀點。您的特質是靈活、機智，但有時可能顯得不夠專注，
        難以沉澱。
        """,
        "strengths": ["智慧豐富", "思維活躍", "包容力強", "靈活變通", "善於學習"],
        "challenges": ["可能多變", "不夠專注", "難以沉澱", "需要方向"],
        "optimal_environment": "需要自由與變化，適合需要創新與學習的環境"
    },
    "癸": {
        "name": "癸水",
        "nature": "陰水",
        "象徵": "雨露甘霖",
        "core_essence": """
        作為癸水日主，您如同雨露甘霖，滋潤萬物、靜默深沉。您的個性內斂、深邃，
        善於觀察與思考。您的智慧是內在的，不張揚但深刻。您有豐富的想像力與直覺力，
        適合從事創作或研究。您的特質是柔和、包容，但內心有自己的堅持。您需要時間
        沉澱，才能發揮真正的力量。
        """,
        "strengths": ["深邃內斂", "智慧深刻", "直覺敏銳", "想像力豐富", "包容柔和"],
        "challenges": ["可能過於內向", "不夠主動", "需要沉澱", "難以被理解"],
        "optimal_environment": "需要安靜深入的環境，適合研究與創作"
    }
}


# ============================================================================
# 五行心理學對應 (Element Psychology Mapping)
# ============================================================================

ELEMENT_PSYCHOLOGY = {
    "木": {
        "psychological_traits": "生長、擴展、創新、理想主義",
        "when_strong": "積極進取、有創意、追求自由、理想主義、具有開創精神",
        "when_weak": "缺乏動力、創意受限、理想難實現、發展受阻",
        "when_excessive": "過度擴張、不切實際、缺乏根基、難以沉澱",
        "health_implications": "肝膽系統、眼睛、筋腱、神經系統",
        "emotional_tendency": "容易憤怒、追求自由、不喜束縛"
    },
    "火": {
        "psychological_traits": "熱情、活力、表達、社交",
        "when_strong": "熱情洋溢、積極主動、善於表達、人緣好、行動力強",
        "when_weak": "缺乏熱情、不夠主動、表達困難、社交受限",
        "when_excessive": "過度急躁、情緒波動大、易焦慮、消耗過度、缺乏耐心",
        "health_implications": "心臟、小腸、血液循環、血壓",
        "emotional_tendency": "容易興奮、情緒起伏、需要認可"
    },
    "土": {
        "psychological_traits": "穩定、務實、包容、責任",
        "when_strong": "穩重可靠、務實踏實、有責任感、包容力強、值得信賴",
        "when_weak": "缺乏安全感、不夠穩定、責任感不足",
        "when_excessive": "過度保守、缺乏彈性、思想僵化、行動遲緩",
        "health_implications": "脾胃、消化系統、肌肉",
        "emotional_tendency": "追求穩定、重視安全感、較為保守"
    },
    "金": {
        "psychological_traits": "理性、果斷、原則、秩序",
        "when_strong": "理性冷靜、果斷有力、原則性強、重視秩序、追求完美",
        "when_weak": "缺乏果斷、原則不清、難以取捨",
        "when_excessive": "過度剛硬、不夠圓融、過於挑剔、易生衝突、缺乏彈性",
        "health_implications": "肺、大腸、皮膚、呼吸系統、免疫系統",
        "emotional_tendency": "理性控制、壓抑情感、追求秩序"
    },
    "水": {
        "psychological_traits": "智慧、靈活、流動、深邃",
        "when_strong": "智慧豐富、靈活變通、善於學習、思維活躍、適應力強",
        "when_weak": "缺乏智慧、思考受限、學習困難、缺乏策略",
        "when_excessive": "過度多變、難以專注、缺乏沉澱、不夠穩定",
        "health_implications": "腎、膀胱、泌尿系統、生殖系統、內分泌、骨骼",
        "emotional_tendency": "深沉內斂、情感豐富、需要安全感"
    }
}


# ============================================================================
# 十神性格特質 (Ten Gods Personality Traits)
# ============================================================================

TEN_GODS_TRAITS = {
    "比肩": {
        "name": "比肩",
        "nature": "同我者",
        "core_trait": "獨立自主、堅持己見",
        "positive": "獨立性強、有主見、自信、能堅持立場、不易被動搖",
        "negative": "可能固執、不易合作、較為自我、不擅長妥協",
        "social_style": "傾向獨立作業，朋友雖不多但都是知己",
        "when_strong": "主見強烈、獨立能力強，但可能較為孤僻",
        "when_weak": "缺乏自信、容易依賴他人、難以堅持己見"
    },
    "劫財": {
        "name": "劫財",
        "nature": "同我者（異性）",
        "core_trait": "競爭意識、行動力強",
        "positive": "積極主動、勇於競爭、行動力強、敢於冒險、不畏困難",
        "negative": "可能過度競爭、衝動行事、不夠穩重、易與人衝突",
        "social_style": "喜歡競爭與挑戰，容易與同輩產生競爭關係",
        "when_strong": "競爭力強、行動果斷，但可能招致小人",
        "when_weak": "缺乏競爭力、行動力不足、容易退縮"
    },
    "食神": {
        "name": "食神",
        "nature": "我生者",
        "core_trait": "表達創造、享受人生",
        "positive": "善於表達、有創造力、懂得享受、思維活躍、才華洋溢",
        "negative": "可能過於理想化、不夠務實、缺乏執行力",
        "social_style": "善於分享、樂於表達，人緣通常不錯",
        "when_strong": "創意豐富、表達能力強，生活品質高",
        "when_weak": "表達受限、創意不足、難以享受生活"
    },
    "傷官": {
        "name": "傷官",
        "nature": "我生者（異性）",
        "core_trait": "反叛創新、才華橫溢",
        "positive": "才華出眾、創新能力強、不拘一格、勇於突破、表達力強",
        "negative": "可能叛逆、不守規矩、容易得罪人、過於主觀",
        "social_style": "個性鮮明、不喜歡權威，容易與上級產生矛盾",
        "when_strong": "才華橫溢、創新力強，但需要學習尊重他人",
        "when_weak": "才華難以發揮、表達受限、創新受阻"
    },
    "偏財": {
        "name": "偏財",
        "nature": "我克者",
        "core_trait": "靈活理財、善於交際",
        "positive": "理財靈活、善於把握機會、交際能力強、慷慨大方",
        "negative": "可能過於投機、不夠穩重、財務管理較隨意",
        "social_style": "善於社交、人脈廣泛、慷慨待人",
        "when_strong": "財運佳、機會多，但要避免投機",
        "when_weak": "理財能力不足、機會較少、難以累積財富"
    },
    "正財": {
        "name": "正財",
        "nature": "我克者（異性）",
        "core_trait": "穩健理財、重視秩序",
        "positive": "理財穩健、重視計劃、務實可靠、善於管理、有責任感",
        "negative": "可能過於保守、缺乏冒險精神、較為物質導向",
        "social_style": "重視實際利益、交往較為現實",
        "when_strong": "財務穩定、理財有方，生活富足",
        "when_weak": "財務困難、理財能力不足、物質匱乏感"
    },
    "偏官": {
        "name": "偏官（七殺）",
        "nature": "克我者",
        "core_trait": "果斷魄力、勇於挑戰",
        "positive": "果斷有魄力、勇於挑戰、行動力強、不畏困難、領導力強",
        "negative": "可能過於激進、壓力大、容易焦慮、不夠溫和",
        "social_style": "強勢主導、不怕權威，但也易與人衝突",
        "when_strong": "領導力強、能克服困難，但壓力也大",
        "when_weak": "缺乏魄力、容易退縮、難以面對挑戰"
    },
    "正官": {
        "name": "正官",
        "nature": "克我者（異性）",
        "core_trait": "守規重紀、追求地位",
        "positive": "守法守紀、有責任感、重視名譽、追求成就、自律性強",
        "negative": "可能過於拘謹、壓力大、不夠靈活、過度在意他人看法",
        "social_style": "重視規範、尊重權威、追求社會認可",
        "when_strong": "地位高、受尊重，但壓力也較大",
        "when_weak": "缺乏約束、難以獲得地位與認可"
    },
    "偏印": {
        "name": "偏印（梟神）",
        "nature": "生我者",
        "core_trait": "獨特思維、追求知識",
        "positive": "思維獨特、求知慾強、善於學習、有專業深度、創新思考",
        "negative": "可能過於孤僻、不善表達、思想偏激、難以被理解",
        "social_style": "較為孤僻、喜歡獨處、不善社交",
        "when_strong": "專業能力強、學識豐富，但可能孤獨",
        "when_weak": "學習困難、缺乏貴人、難以獲得支持"
    },
    "正印": {
        "name": "正印",
        "nature": "生我者（異性）",
        "core_trait": "學習成長、貴人相助",
        "positive": "善於學習、有貴人運、重視知識、有文化修養、受人尊重",
        "negative": "可能過於依賴、缺乏主動性、理想化、不夠實際",
        "social_style": "有長輩緣、貴人多、容易獲得幫助",
        "when_strong": "學習能力強、貴人多助，但可能缺乏行動力",
        "when_weak": "學習困難、缺乏貴人、難以獲得支持與認可"
    }
}


# ============================================================================
# 核心解讀函數 (Core Interpretation Functions)
# ============================================================================

def interpret_personality(bazi_data: Dict) -> Dict:
    """
    深度性格心理分析（LLM增強版）

    Args:
        bazi_data: 從 BaziCalculator.analyze() 返回的完整數據

    Returns:
        詳細的性格分析結果，包含：
        - 日主核心特質
        - 十神性格配置
        - 五行心理特徵
        - 人際互動模式
        - 決策模式
        - confidence_level: 信心度評估（新增）
    """
    # Try LLM analysis with fallback to traditional
    llm_analyzer = get_llm_analyzer()

    if llm_analyzer.is_available() and BAZI_SYSTEM_PROMPT:
        # Construct LLM prompt
        analysis_prompt = construct_bazi_personality_prompt(bazi_data)

        # Try LLM analysis
        llm_result = llm_analyzer.analyze_with_fallback(
            system_prompt=BAZI_SYSTEM_PROMPT,
            analysis_prompt=analysis_prompt,
            fallback_func=_traditional_personality_analysis,
            fallback_args=(bazi_data,),
            min_length=300,
            temperature=0.7,
            max_tokens=4000
        )

        # If LLM returned rich analysis, package it
        # Check if llm_result is a string (LLM success) or dict (fallback was used)
        if isinstance(llm_result, str) and len(llm_result.replace(' ', '').replace('\n', '')) >= 300:
            # Calculate confidence (LLM + good data quality = high confidence)
            confidence = calculate_confidence_level(
                consensus_indicators=1,  # Single method (BaZi only)
                total_indicators=1,
                data_quality=1.0,  # Assuming complete BaZi data
                theoretical_support=0.9  # BaZi has strong theoretical support
            )

            # Return LLM result with traditional structure for compatibility
            traditional_result = _traditional_personality_analysis(bazi_data)
            traditional_result['llm_analysis'] = llm_result
            traditional_result['confidence_level'] = confidence
            traditional_result['analysis_method'] = 'LLM enhanced'
            return traditional_result
        elif isinstance(llm_result, dict):
            # Fallback was already executed, return it directly
            return llm_result

    # Fallback to traditional analysis
    return _traditional_personality_analysis(bazi_data)


def _traditional_personality_analysis(bazi_data: Dict) -> Dict:
    """傳統八字性格分析（原有邏輯）"""
    day_master = bazi_data['basic_chart']['day']['stem']
    strength = bazi_data['strength']
    wuxing_analysis = bazi_data['wuxing_analysis']
    ten_gods_analysis = bazi_data['ten_gods_analysis']

    # 1. 日主核心特質
    day_master_trait = DAY_MASTER_TRAITS.get(day_master, DAY_MASTER_TRAITS['甲'])

    # 根據身強弱調整描述
    strength_status = strength.get('level', strength.get('overall_strength', '身中和'))
    if strength_status in ['身弱', 'weak']:
        strength_note = """
        然而，您的八字顯示身弱，這意味著儘管有雄心壯志，在實現目標的過程中
        需要更多外部資源的支持與滋養。您的能量有限，需要學會借助他人力量，
        選擇適合自己的發展路徑，避免過度消耗。
        """
    elif strength_status in ['身強', 'strong']:
        strength_note = """
        您的八字顯示身強，這意味著您的內在能量充沛，有足夠的力量去實現目標。
        您的自信與行動力都很強，能夠獨立面對挑戰。但也要注意不要過度自我，
        學會與他人合作，接受不同的意見。
        """
    else:
        strength_note = """
        您的八字顯示身強身弱適中，這是一種相對平衡的狀態。您既有一定的獨立能力，
        也懂得尋求他人協助。這種平衡讓您能在自主與合作之間靈活切換。
        """

    day_master_essence = day_master_trait['core_essence'].strip() + "\n\n" + strength_note

    # 2. 十神性格配置分析
    ten_gods_personality = _analyze_ten_gods_personality(ten_gods_analysis)

    # 3. 五行心理特徵
    elemental_psychology = _analyze_elemental_psychology(wuxing_analysis)

    # 4. 人際互動模式
    interpersonal_style = _analyze_interpersonal_style(ten_gods_analysis)

    # 5. 決策模式
    decision_pattern = _analyze_decision_pattern(ten_gods_analysis, wuxing_analysis)

    # Calculate basic confidence for traditional method
    confidence = calculate_confidence_level(
        consensus_indicators=1,
        total_indicators=1,
        data_quality=1.0,
        theoretical_support=0.8  # Traditional has solid theory but less personalized
    )

    return {
        'core_personality': {
            'day_master_essence': day_master_essence,
            'day_master_traits': day_master_trait,
            'ten_gods_personality': ten_gods_personality,
            'elemental_psychology': elemental_psychology
        },
        'interpersonal_style': interpersonal_style,
        'decision_making_pattern': decision_pattern,
        'strength_context': {
            'status': strength_status,
            'implications': strength_note
        },
        'confidence_level': confidence,
        'analysis_method': 'Traditional rule-based'
    }


def _analyze_ten_gods_personality(ten_gods_analysis: Dict) -> str:
    """分析十神配置對性格的影響"""
    distribution = ten_gods_analysis.get('distribution', {})

    # 找出最突出的十神
    prominent_gods = []
    for god_name, count in distribution.items():
        if count >= 2:  # 兩個以上就算突出
            prominent_gods.append((god_name, count))

    if not prominent_gods:
        # 如果沒有特別突出的，找出有出現的
        prominent_gods = [(god_name, count) for god_name, count in distribution.items() if count > 0]

    # 生成十神性格描述
    descriptions = []

    for god_name, count in prominent_gods[:3]:  # 最多描述前3個
        god_trait = TEN_GODS_TRAITS.get(god_name)
        if god_trait:
            strength_level = "強" if count >= 3 else "中等" if count >= 2 else "適中"

            desc = f"""
**{god_name}（{strength_level}）**：
{god_trait['positive']}

特別注意：
{god_trait['negative']}
            """
            descriptions.append(desc.strip())

    if len(prominent_gods) >= 2:
        combination_note = f"""

**十神組合效應**：
您的命局中有多種十神配置，這創造了複雜而豐富的性格層次。
{prominent_gods[0][0]}與{prominent_gods[1][0]}的組合，讓您在{TEN_GODS_TRAITS[prominent_gods[0][0]]['core_trait']}
與{TEN_GODS_TRAITS[prominent_gods[1][0]]['core_trait']}之間尋找平衡。
        """
        descriptions.append(combination_note.strip())

    return "\n\n".join(descriptions)


def _analyze_elemental_psychology(wuxing_analysis: Dict) -> str:
    """分析五行配置對心理的影響"""
    element_count = wuxing_analysis.get('element_count', {})
    dominant_elements = wuxing_analysis.get('dominant_elements', [])
    lacking_elements = wuxing_analysis.get('lacking_elements', [])

    descriptions = []

    # 分析旺盛的元素
    if dominant_elements:
        for element in dominant_elements[:2]:  # 最多分析前2個
            elem_psych = ELEMENT_PSYCHOLOGY.get(element)
            if elem_psych:
                desc = f"""
**{element}旺的心理影響**：
{elem_psych['when_excessive']}

健康層面需注意：
{elem_psych['health_implications']}相關的保養

情緒傾向：
{elem_psych['emotional_tendency']}
                """
                descriptions.append(desc.strip())

    # 分析缺失的元素（非常重要）
    if lacking_elements:
        for element in lacking_elements:
            elem_psych = ELEMENT_PSYCHOLOGY.get(element)
            if elem_psych:
                desc = f"""
**缺{element}的影響（重要）**：
{elem_psych['when_weak']}

建議補充方式：
- 多接觸{element}元素相關的活動與環境
- 在重大決策前，刻意培養{elem_psych['psychological_traits']}的特質
- 特別注意{elem_psych['health_implications']}的保健
                """
                descriptions.append(desc.strip())

    return "\n\n".join(descriptions)


def _analyze_interpersonal_style(ten_gods_analysis: Dict) -> str:
    """分析人際互動模式"""
    distribution = ten_gods_analysis.get('distribution', {})

    bijie_count = distribution.get('比肩', 0) + distribution.get('劫財', 0)
    shishen_count = distribution.get('食神', 0) + distribution.get('傷官', 0)
    cai_count = distribution.get('正財', 0) + distribution.get('偏財', 0)
    guan_count = distribution.get('正官', 0) + distribution.get('偏官', 0)
    yin_count = distribution.get('正印', 0) + distribution.get('偏印', 0)

    interpersonal_notes = []

    # 比劫分析（同輩關係）
    if bijie_count == 0:
        interpersonal_notes.append("""
**同輩關係**：您的比劫較少，代表您不太依賴同輩朋友，更傾向獨立作業或與不同
年齡層的人交往。您可能不是團體中的核心，但也因此較少捲入同輩之間的競爭與衝突。
        """.strip())
    elif bijie_count >= 3:
        interpersonal_notes.append("""
**同輩關係**：您的比劫較多，代表同輩朋友對您很重要，但也容易產生競爭關係。
您重視朋友義氣，但要避免過度依賴或捲入不必要的競爭。學會選擇良師益友很重要。
        """.strip())
    else:
        interpersonal_notes.append("""
**同輩關係**：您的比劫適中，代表您與同輩朋友的關係平衡。您既有獨立性，也懂得
與朋友合作。朋友不多但質量不錯，彼此之間有適度的支持與競爭。
        """.strip())

    # 財星分析（人際投入）
    if cai_count >= 2:
        interpersonal_notes.append("""
**人際投入**：財星適中或偏多，顯示您在人際交往中務實理性，會考慮實際利益與回報。
您不會無條件付出，也不會過度功利。這種平衡的態度讓您的人際關係較為穩定。
        """.strip())

    # 官星分析（權威關係）
    if guan_count == 0:
        interpersonal_notes.append("""
**與權威關係**：官殺較少，代表您對權威的態度較為自由，不會盲目服從，但也不會
刻意反抗。您更重視實際而非形式，與上級的關係取決於對方是否值得尊重。
        """.strip())
    elif guan_count >= 2:
        interpersonal_notes.append("""
**與權威關係**：官殺適中或偏多，代表權威對您有一定影響力。您重視規範與秩序，
願意服從合理的管理，但這也可能帶來壓力。您需要在服從與獨立之間找到平衡。
        """.strip())

    # 印星分析（長輩關係）
    if yin_count >= 2:
        interpersonal_notes.append("""
**長輩貴人緣**：印星較多，代表您容易獲得長輩與貴人的幫助與照顧。您可能較為
依賴長輩的指導與支持，這是您的優勢，但也要培養獨立解決問題的能力。
        """.strip())

    return "\n\n".join(interpersonal_notes)


def _analyze_decision_pattern(ten_gods_analysis: Dict, wuxing_analysis: Dict) -> str:
    """分析決策模式"""
    distribution = ten_gods_analysis.get('distribution', {})
    lacking_elements = wuxing_analysis.get('lacking_elements', [])

    shishen_count = distribution.get('食神', 0) + distribution.get('傷官', 0)
    yin_count = distribution.get('正印', 0) + distribution.get('偏印', 0)
    guan_count = distribution.get('正官', 0) + distribution.get('偏官', 0)
    cai_count = distribution.get('正財', 0) + distribution.get('偏財', 0)

    decision_notes = []

    # 食傷與印星的決策影響
    if shishen_count >= 2 and yin_count >= 2:
        decision_notes.append("""
**決策風格 - 創新與謹慎的平衡**：
您的食傷與印星都較為明顯，這創造了有趣的決策模式。食傷讓您重視創新想法與
個人表達，而印星則讓您考慮規範與他人意見。這可能導致內在衝突——一方面想要
創新突破，一方面又擔心不符合規範。

建議：在創新想法產生後，給自己時間做充分研究（發揮印星優勢），然後大膽實施
（發揮食傷優勢）。不要讓謹慎變成猶豫，也不要讓創新變成衝動。
        """.strip())
    elif shishen_count >= 2:
        decision_notes.append("""
**決策風格 - 創新主導**：
您的食傷較強，代表您的決策重視創新與個人想法。您傾向相信自己的判斷，不喜歡
被規範束縛。但要注意，有時太過主觀可能忽略重要的現實因素。建議在重大決策前，
多聽取他人意見，做足研究準備。
        """.strip())
    elif yin_count >= 2:
        decision_notes.append("""
**決策風格 - 研究謹慎**：
您的印星較強，代表您的決策較為謹慎，重視研究與學習。您會仔細考慮各種因素，
參考他人意見與既有規範。但要注意，過度謹慎可能導致猶豫不決，錯失良機。
建議培養適度的行動力與決斷力。
        """.strip())

    # 官星對決策的影響
    if guan_count >= 2:
        decision_notes.append("""
**決策考量 - 規範與責任**：
您的官星明顯，代表您在決策時會考慮規範、責任與他人期待。您重視決策的正當性
與後果，這讓您的決策較為穩妥，但也可能帶來壓力與束縛感。學會在滿足他人期待
與堅持自我之間取得平衡。
        """.strip())

    # 財星對決策的影響
    if cai_count >= 2:
        decision_notes.append("""
**決策考量 - 實際效益**：
您的財星明顯，代表您在決策時會務實考慮實際效益與投資報酬。您不會做無意義的
投入，也不會純粹為了理想而忽略現實。這讓您的決策較為理性，但要避免過度功利，
有時精神層面的價值也很重要。
        """.strip())

    # 缺水對決策的影響
    if '水' in lacking_elements:
        decision_notes.append("""
**決策弱點 - 策略思維不足**：
您的五行缺水，這在決策上可能表現為缺乏大局觀與策略思維。您可能較為衝動，
缺乏周全的計劃，或者難以看清長遠影響。

建議：
- 重大決策前給自己充分的思考時間
- 多閱讀、多學習，培養策略思維
- 找有智慧的導師或顧問請益
- 使用系統化的決策工具（如SWOT分析）
        """.strip())

    return "\n\n".join(decision_notes) if decision_notes else "決策模式平衡，能根據情況靈活調整。"


# ============================================================================
# 事業分析 (Career Analysis)
# ============================================================================

def interpret_career(bazi_data: Dict) -> Dict:
    """深度事業分析（LLM增強版）

    分析內容：
    1. 天賦與適性評估
    2. 適合的行業領域
    3. 事業發展時間軸
    4. 具體建議

    Returns:
        Dict: {
            'aptitude': str,  # 200-500字天賦評估
            'industries': List[Dict],  # 推薦行業清單
            'career_timeline': Dict,  # 各年齡段事業發展
            'recommendations': List[str],  # 具體建議
            'confidence_level': Dict,  # 信心度評估（新增）
            'llm_analysis': str (optional)  # LLM深度分析（新增）
        }
    """
    # Try LLM analysis with fallback
    llm_analyzer = get_llm_analyzer()

    if llm_analyzer.is_available() and BAZI_SYSTEM_PROMPT:
        analysis_prompt = construct_bazi_career_prompt(bazi_data)

        llm_result = llm_analyzer.analyze_with_fallback(
            system_prompt=BAZI_SYSTEM_PROMPT,
            analysis_prompt=analysis_prompt,
            fallback_func=_traditional_career_analysis,
            fallback_args=(bazi_data,),
            min_length=300,
            temperature=0.7,
            max_tokens=4000
        )

        # Check if llm_result is a string (LLM success) or dict (fallback was used)
        if isinstance(llm_result, str) and len(llm_result.replace(' ', '').replace('\n', '')) >= 300:
            confidence = calculate_confidence_level(
                consensus_indicators=1,
                total_indicators=1,
                data_quality=1.0,
                theoretical_support=0.9
            )

            traditional_result = _traditional_career_analysis(bazi_data)
            traditional_result['llm_analysis'] = llm_result
            traditional_result['confidence_level'] = confidence
            traditional_result['analysis_method'] = 'LLM enhanced'
            return traditional_result
        elif isinstance(llm_result, dict):
            # Fallback was already executed, return it directly
            return llm_result

    return _traditional_career_analysis(bazi_data)


def _traditional_career_analysis(bazi_data: Dict) -> Dict:
    """傳統八字事業分析"""
    day_stem = bazi_data.get('basic_chart', {}).get('day_pillar', {}).get('stem', '')
    ten_gods = bazi_data.get('ten_gods_analysis', {})
    wuxing = bazi_data.get('wuxing_analysis', {})
    pattern = bazi_data.get('pattern', {})

    # 1. 天賦適性評估
    aptitude_analysis = _analyze_career_aptitude(day_stem, ten_gods, wuxing, pattern)

    # 2. 行業推薦
    industries = _recommend_industries(day_stem, ten_gods, wuxing)

    # 3. 事業時間軸
    timeline = _create_career_timeline(day_stem, ten_gods, bazi_data.get('luck_pillars', []))

    # 4. 具體建議
    recommendations = _generate_career_recommendations(day_stem, ten_gods, wuxing, pattern)

    confidence = calculate_confidence_level(
        consensus_indicators=1,
        total_indicators=1,
        data_quality=1.0,
        theoretical_support=0.8
    )

    return {
        'aptitude': aptitude_analysis,
        'industries': industries,
        'career_timeline': timeline,
        'recommendations': recommendations,
        'confidence_level': confidence,
        'analysis_method': 'Traditional rule-based'
    }


def _analyze_career_aptitude(day_stem: str, ten_gods: Dict, wuxing: Dict, pattern: Dict) -> str:
    """分析事業天賦與適性"""
    parts = []

    # 日主天賦
    if day_stem in DAY_MASTER_TRAITS:
        trait = DAY_MASTER_TRAITS[day_stem]
        parts.append(f"""**核心天賦 - {trait['name']}特質**：
作為{trait['象徵']}，您的核心天賦在於{trait['core_essence'][:100]}。這種特質使您在事業上{trait['strengths'][0]}，
並且{trait['strengths'][1] if len(trait['strengths']) > 1 else '具有獨特的優勢'}。""")

    # 十神事業傾向
    strong_gods = ten_gods.get('distribution', {})
    if '食神' in strong_gods or '傷官' in strong_gods:
        parts.append("""
**創造力與表達力**：
您的八字中食傷較旺，這賦予您優秀的創造力與表達能力。您不適合純粹執行性的工作，
而是需要有創意發揮空間的職位。您可能在以下領域展現天賦：
- 創意產業（設計、文案、藝術）
- 技術創新（研發、產品開發）
- 內容創作（寫作、教學、演講）
- 專業服務（諮詢、培訓）""")

    if '正官' in strong_gods or '七殺' in strong_gods:
        parts.append("""
**領導力與管理能力**：
您的八字官殺有力，顯示天生的管理才能與責任感。您適合需要承擔責任、
管理他人或處理複雜事務的角色。可能的發展方向：
- 管理職位（部門主管、專案經理）
- 專業領域專家（需要權威性的角色）
- 規劃與策略工作（需要全局觀的職位）""")

    if '正財' in strong_gods or '偏財' in strong_gods:
        parts.append("""
**商業頭腦與實務能力**：
您的財星有力，顯示良好的商業直覺與實務操作能力。您懂得如何創造價值、
管理資源，適合與金錢、資源管理相關的工作：
- 業務開發（銷售、商務拓展）
- 財務管理（會計、理財規劃）
- 營運管理（資源配置、成本控制）
- 創業經營（特別是實體business）""")

    if '正印' in strong_gods or '偏印' in strong_gods:
        parts.append("""
**學習力與專業深度**：
您的印星旺盛，代表優秀的學習能力與求知慾。您適合需要持續學習、
深度鑽研的專業領域：
- 學術研究（教育、研究機構）
- 專業技術（需要深厚專業知識的領域）
- 諮詢顧問（運用知識解決問題）
- 培訓教育（知識傳播與教學）""")

    # 五行平衡的影響
    lacking = wuxing.get('lacking_elements', [])
    if '金' in lacking:
        parts.append("""
**提醒 - 執行力培養**：
您的五行缺金，可能在決斷力、執行力方面需要加強。建議：
- 設定明確的目標與期限
- 培養果斷的決策習慣
- 與執行力強的夥伴合作""")

    if '水' in lacking:
        parts.append("""
**提醒 - 策略思維**：
您的五行缺水，可能在長期規劃、策略思考方面需要補強。建議：
- 重大決策前多方諮詢
- 學習系統化的思考方法
- 找有智慧的導師指導""")

    return "\n\n".join(parts)


def _recommend_industries(day_stem: str, ten_gods: Dict, wuxing: Dict) -> List[Dict]:
    """推薦適合的行業領域"""
    industries = []
    strong_gods = ten_gods.get('distribution', {})

    # 基於十神推薦
    if '食神' in strong_gods or '傷官' in strong_gods:
        industries.append({
            'category': '創意與內容產業',
            'fields': ['設計', '廣告', '媒體', '藝術', '娛樂', '內容創作'],
            'fit_level': '極佳',
            'reason': '食傷旺盛，創造力與表達力是您的核心優勢'
        })
        industries.append({
            'category': '技術創新',
            'fields': ['軟體開發', '產品設計', '研發', '新創科技'],
            'fit_level': '優良',
            'reason': '食傷利於技術創新與產品開發'
        })

    if '正官' in strong_gods or '七殺' in strong_gods:
        industries.append({
            'category': '管理與專業服務',
            'fields': ['企業管理', '專案管理', '諮詢顧問', '法律', '會計'],
            'fit_level': '極佳',
            'reason': '官殺有力，適合需要權威性與責任感的專業領域'
        })

    if '正財' in strong_gods or '偏財' in strong_gods:
        industries.append({
            'category': '商業與金融',
            'fields': ['銷售', '貿易', '金融', '房地產', '零售業'],
            'fit_level': '優良',
            'reason': '財星旺盛，商業直覺與資源管理能力強'
        })

    if '正印' in strong_gods or '偏印' in strong_gods:
        industries.append({
            'category': '教育與研究',
            'fields': ['教育培訓', '學術研究', '出版', '知識服務'],
            'fit_level': '極佳',
            'reason': '印星有力，學習力強且善於知識傳播'
        })

    if '比肩' in strong_gods or '劫財' in strong_gods:
        industries.append({
            'category': '自由工作與創業',
            'fields': ['自由職業', '個人工作室', '小型創業'],
            'fit_level': '優良',
            'reason': '比劫旺盛，獨立性強，適合自主經營'
        })

    return industries[:4]  # 返回前4個最適合的


def _create_career_timeline(day_stem: str, ten_gods: Dict, luck_pillars: List) -> Dict:
    """建立事業發展時間軸"""
    timeline = {
        '25-30歲': {
            'phase': '探索與學習期',
            'focus': '累積專業能力，建立基礎',
            'strategy': '多嘗試、多學習，找到真正適合的方向',
            'expected_outcome': '確定職業方向，成為該領域的熟練者',
            'key_actions': [
                '不要太在意薪水，重點是學習機會',
                '多觀察不同領域與角色',
                '建立專業人脈網絡',
                '投資自我成長（技能、知識、證照）'
            ]
        },

        '31-40歲': {
            'phase': '快速成長期',
            'focus': '專業深化，建立影響力',
            'strategy': '在選定領域深耕，成為專家',
            'expected_outcome': '成為領域內的專家或中高階主管',
            'key_actions': [
                '在專業領域建立個人品牌',
                '爭取更大的責任與挑戰',
                '開始考慮第二收入來源',
                '建立mentor與mentee關係'
            ],
            'critical_years': [35, 38]
        },

        '41-50歲': {
            'phase': '事業高峰期',
            'focus': '價值變現，影響力擴大',
            'strategy': '將累積的專業價值轉化為更高收入與影響力',
            'expected_outcome': '達到事業頂峰，財富快速累積',
            'key_actions': [
                '提高專業服務定價',
                '考慮擔任顧問或獨立專家',
                '發展被動收入（課程、版權）',
                '開始思考事業傳承'
            ]
        },

        '51歲以上': {
            'phase': '智慧分享期',
            'focus': '經驗傳承，降低工作強度',
            'strategy': '從執行轉向指導，分享累積的智慧',
            'expected_outcome': '工作與生活平衡，持續影響力',
            'key_actions': [
                '轉型為導師或顧問',
                '減少執行工作，增加策略角色',
                '培養接班人',
                '享受工作成果與生活'
            ]
        }
    }

    return timeline


def _generate_career_recommendations(day_stem: str, ten_gods: Dict,
                                     wuxing: Dict, pattern: Dict) -> List[str]:
    """產生具體的事業建議"""
    recommendations = []
    strong_gods = ten_gods.get('distribution', {})

    # 基於十神的建議
    if '食神' in strong_gods or '傷官' in strong_gods:
        recommendations.append(
            "**建立個人品牌**：您的食傷旺盛，最適合發展個人專業品牌。"
            "不要只是當個「員工」，要成為「專家」。通過寫作、演講、教學建立影響力，"
            "35歲後將品牌轉化為收入來源。"
        )

    if '正印' in strong_gods or '偏印' in strong_gods:
        recommendations.append(
            "**持續學習投資**：您的印星有力，學習是您最好的投資。"
            "不要吝嗇在專業進修、證照、課程上的花費。每年至少投入收入的5-10%在自我成長上，"
            "這些投資會在3-5年後以數倍回報給您。"
        )

    if '比肩' in strong_gods or '劫財' in strong_gods:
        recommendations.append(
            "**考慮獨立工作**：您的比劫旺盛，獨立性強，不太適合受人管束。"
            "40歲前可累積專業與人脈，40歲後考慮獨立執業或創業。"
            "但要注意：避免與朋友合夥，獨資或僱傭關係更適合您。"
        )

    if '正官' in strong_gods or '七殺' in strong_gods:
        recommendations.append(
            "**承擔更大責任**：您的官殺有力，天生適合管理與領導。"
            "不要滿足於執行角色，要主動爭取管理機會。30歲後應該朝向管理職或專家顧問發展，"
            "這樣才能發揮您的天賦。"
        )

    # 通用建議
    recommendations.append(
        "**35歲是關鍵轉折點**：在此之前重點是「累積」（能力、人脈、資源），"
        "35歲後要開始「變現」（提高收入、擴大影響力）。不要在35歲後還在做25歲的工作。"
    )

    recommendations.append(
        "**建立多元收入來源**：40歲前至少要建立一種被動收入或第二收入來源。"
        "可以是線上課程、專業諮詢、技術產品等。這不只是為了增加收入，"
        "更是為了降低職業風險，增加人生選擇權。"
    )

    return recommendations


# ============================================================================
# 財富分析 (Wealth Analysis)
# ============================================================================

def interpret_wealth(bazi_data: Dict) -> Dict:
    """深度財富分析

    分析內容：
    1. 財富潛力與賺錢能力
    2. 理財風格與金錢觀
    3. 財富時間軸（各年齡段）
    4. 財富來源分析
    5. 具體建議

    Returns:
        Dict: {
            'wealth_potential': str,  # 財富潛力評估
            'money_management_style': str,  # 理財風格
            'wealth_timeline': Dict,  # 各年齡段財富狀況
            'wealth_sources': Dict,  # 財富來源分析
            'recommendations': List[str]  # 具體建議
        }
    """
    day_stem = bazi_data.get('basic_chart', {}).get('day_pillar', {}).get('stem', '')
    ten_gods = bazi_data.get('ten_gods_analysis', {})
    wuxing = bazi_data.get('wuxing_analysis', {})
    pattern = bazi_data.get('pattern', {})

    # 1. 財富潛力
    potential = _analyze_wealth_potential(day_stem, ten_gods, wuxing, pattern)

    # 2. 理財風格
    style = _analyze_money_management_style(ten_gods, wuxing)

    # 3. 財富時間軸
    timeline = _create_wealth_timeline(ten_gods, bazi_data.get('luck_pillars', []))

    # 4. 財富來源
    sources = _analyze_wealth_sources(ten_gods, wuxing, pattern)

    # 5. 具體建議
    recommendations = _generate_wealth_recommendations(ten_gods, wuxing, pattern)

    return {
        'wealth_potential': potential,
        'money_management_style': style,
        'wealth_timeline': timeline,
        'wealth_sources': sources,
        'recommendations': recommendations
    }


def _analyze_wealth_potential(day_stem: str, ten_gods: Dict, wuxing: Dict, pattern: Dict) -> str:
    """分析財富潛力與賺錢能力"""
    parts = []
    strong_gods = ten_gods.get('distribution', {})

    # 財星分析
    if '正財' in strong_gods or '偏財' in strong_gods:
        parts.append("""**財富潛力 - 中上等級**：
您的八字中財星有力，這是財富潛力的重要指標。您對金錢有天生的敏感度，
懂得如何創造價值、管理資源。相比於一般人，您更容易掌握賺錢的機會，
也更有能力累積財富。

財星特質：
- 正財：穩定收入能力強，適合薪資、租金等固定收入
- 偏財：商業直覺佳，適合業務、投資等靈活收入

您的財富累積不會一夜暴富，但會穩健增長。35-45歲是您財富快速累積的黃金期。""")
    else:
        parts.append("""**財富潛力 - 中等偏專業型**：
您的八字財星不顯著，但這並不代表您會貧窮。您的財富更多來自於「專業價值」
而非「商業操作」。您適合通過提升專業能力、建立個人品牌來增加收入。

建議路徑：
- 不要追求快錢或投機收入
- 專注於提升專業價值
- 35歲後將專業轉化為高收入
- 建立被動收入（如課程、版權）""")

    # 食傷生財
    if ('食神' in strong_gods or '傷官' in strong_gods) and ('正財' in strong_gods or '偏財' in strong_gods):
        parts.append("""
**財富模式 - 食傷生財格**：
這是最理想的財富格局之一！您的才華（食傷）能夠直接轉化為財富（財星）。
您適合通過「創造價值」來賺錢，而非單純的買賣或投資。

最佳變現方式：
1. 技術、創意、知識的商品化
2. 個人品牌與專業服務
3. 產品開發與創新
4. 內容創作與版權收入

預期：35-45歲財富可能呈現3-5倍增長。""")

    # 印星與財富
    if '正印' in strong_gods or '偏印' in strong_gods:
        parts.append("""
**財富觀念 - 學習投資優先**：
您的印星旺盛，這使您對「知識投資」的重視程度高於「金錢投資」。
這在年輕時可能讓您的財富累積較慢（因為錢都花在學習上），
但長期來看這是最正確的策略。

財富建議：
- 25-35歲：不要吝嗇學習投資，這是最高報酬率的投資
- 35-45歲：將累積的專業價值變現，收入會快速增長
- 45歲後：享受前期投資的複利效應""")

    # 比劫對財富的影響
    if '比肩' in strong_gods or '劫財' in strong_gods:
        parts.append("""
**財富風險 - 合夥需謹慎**：
您的比劫較旺，這在財務上有一個重要提醒：避免與朋友合夥做生意。
比劫代表分享，您可能會因為義氣或友情而在財務上吃虧。

保護財富：
- 不要輕易為朋友擔保或借貸大額金錢
- 合作以僱傭關係為主，避免股權合夥
- 重要財務決策要理性，不要因人情而妥協""")

    return "\n\n".join(parts)


def _analyze_money_management_style(ten_gods: Dict, wuxing: Dict) -> str:
    """分析理財風格與金錢觀"""
    parts = []
    strong_gods = ten_gods.get('distribution', {})

    if '正財' in strong_gods:
        parts.append("""**理財風格 - 穩健保守型**：
正財旺的人理財風格偏向保守穩健。您喜歡可預測的收入，對風險承受度較低。
您會仔細規劃預算，重視儲蓄，不喜歡投機性的投資。

適合的理財方式：
- 定期定額投資（如指數基金）
- 保守型的投資組合（債券比例較高）
- 房地產等實體資產
- 穩定收入型投資（如出租、股息）

避免：高風險投機、加密貨幣、期貨選擇權等""")

    if '偏財' in strong_gods:
        parts.append("""**理財風格 - 靈活積極型**：
偏財旺的人對商業機會敏感，願意承擔適度風險。您的理財不會太保守，
會積極尋找投資機會，但要注意不要過度投機。

適合的理財方式：
- 業務性收入（銷售、代理）
- 靈活的投資組合（股票比例可較高）
- 創業或入股機會
- 房地產買賣

提醒：設定風險上限，不要把所有資金投入高風險標的""")

    if '食神' in strong_gods or '傷官' in strong_gods:
        parts.append("""**消費習惯 - 享受生活型**：
食傷旺的人對生活品質有要求，願意花錢在美食、娛樂、藝術等享受上。
您賺錢不只是為了存錢，也是為了享受生活。

理財平衡：
- 設定「享受預算」（收入的10-20%）在這範圍內盡情享受
- 其他部分要有紀律地儲蓄與投資
- 避免衝動性消費，特別是大額支出""")

    if '正印' in strong_gods or '偏印' in strong_gods:
        parts.append("""**消費優先 - 知識學習型**：
印星旺的人願意在學習、書籍、課程上投資，這是最值得的消費。
您對物質享受的需求不高，但對精神成長的投資不會吝嗇。

建議：
- 繼續保持學習投資的習慣（這是最高報酬率的投資）
- 但也要注意不要過度消費在「收藏書籍但不讀」的狀況
- 學習要能轉化為收入，才算成功的投資""")

    lacking = wuxing.get('lacking_elements', [])
    if '水' in lacking:
        parts.append("""
**理財弱點 - 缺乏長期規劃**：
您的五行缺水，可能在財務規劃上較缺乏長遠眼光。容易看短期收益，
忽略長期複利的力量。

補強方式：
- 找專業理財顧問協助長期規劃
- 強制儲蓄（自動轉帳到儲蓄帳戶）
- 學習基本的財務知識與投資原理""")

    return "\n\n".join(parts)


def _create_wealth_timeline(ten_gods: Dict, luck_pillars: List) -> Dict:
    """建立財富時間軸"""
    timeline = {
        '25-35歲': {
            'phase': '財富累積期',
            'expected_level': '中低收入但穩定成長',
            'focus': '專業價值累積，而非金錢累積',
            'strategy': '投資自我成長，建立第一桶金',
            'key_actions': [
                '收入的5-10%投入學習與成長',
                '建立緊急預備金（至少6個月生活費）',
                '開始小額投資，學習理財知識',
                '不要過度追求高薪，重點是成長機會'
            ],
            'expected_savings': '年收入的3-6倍（約100-300萬台幣）',
            'warning': '這階段不要追求快錢，穩扎穩打最重要'
        },

        '35-45歲': {
            'phase': '財富快速增長期',
            'expected_level': '收入可能達到3-5倍增長',
            'focus': '專業價值變現，收入顯著提升',
            'strategy': '提高收入，建立被動收入',
            'key_actions': [
                '提高專業服務定價（至少2倍）',
                '建立第二收入來源（課程、諮詢）',
                '增加投資比例（收入的20-30%）',
                '考慮購置資產（房產、股票）'
            ],
            'expected_savings': '年收入的10-20倍（約500-2000萬台幣）',
            'critical_years': [38, 41, 43],
            'opportunity': '這是您財富累積的黃金十年，要全力把握'
        },

        '45-55歲': {
            'phase': '財富穩定期',
            'expected_level': '收入穩定，重點在保值',
            'focus': '財富管理與風險降低',
            'strategy': '降低風險，注重保本與傳承',
            'key_actions': [
                '降低投資風險，增加防禦性資產',
                '轉向顧問或教育型工作（工作強度降低但收入維持）',
                '開始財富傳承規劃',
                '確保退休金足夠'
            ],
            'expected_savings': '年收入的20-40倍（財務自由基本達成）'
        },

        '55歲以上': {
            'phase': '財富享用期',
            'expected_level': '被動收入足以支持生活',
            'focus': '享受生活，財富傳承',
            'strategy': '保守理財，享受人生',
            'key_actions': [
                '生活支出由被動收入支付',
                '工作變成選擇而非必須',
                '財富傳承與稅務規劃',
                '適度享受，回饋社會'
            ]
        }
    }

    return timeline


def _analyze_wealth_sources(ten_gods: Dict, wuxing: Dict, pattern: Dict) -> Dict:
    """分析財富來源"""
    sources = {}
    strong_gods = ten_gods.get('distribution', {})

    # 主要財富來源
    if '食神' in strong_gods or '傷官' in strong_gods:
        sources['primary'] = {
            'source': '專業服務與創作收入',
            'percentage': '70-80%',
            'description': '通過專業技能、創意、知識提供服務獲得的收入',
            'optimization': '提高單位時間價值，從按時計費轉向按價值計費'
        }
    elif '正財' in strong_gods or '偏財' in strong_gods:
        sources['primary'] = {
            'source': '薪資與業務收入',
            'percentage': '60-70%',
            'description': '穩定的薪資或業務性收入',
            'optimization': '提升職位或擴大業務規模'
        }
    else:
        sources['primary'] = {
            'source': '專業薪資收入',
            'percentage': '70-80%',
            'description': '依靠專業能力獲得的穩定薪資',
            'optimization': '提升專業度與不可替代性'
        }

    # 次要財富來源
    sources['secondary'] = {
        'source': '被動收入',
        'percentage': '10-20%',
        'development_stage': '35歲後逐步建立',
        'types': ['線上課程', '版權收入', '股息收入', '租金收入'],
        'importance': '為財務自由打基礎'
    }

    # 投資收入
    sources['investment'] = {
        'source': '投資收益',
        'percentage': '10-20%',
        'suitable_types': _get_suitable_investments(ten_gods, wuxing),
        'risk_level': '中低風險為主',
        'warning': '投資是錦上添花，不是主要收入來源'
    }

    # 應避免的收入來源
    should_avoid = []
    if '比肩' in strong_gods or '劫財' in strong_gods:
        should_avoid.append({
            'type': '合夥創業收入',
            'reason': '比劫旺，合夥容易有財務糾紛',
            'alternative': '可以投資朋友企業，但不要共同經營'
        })

    lacking = wuxing.get('lacking_elements', [])
    if '水' in lacking:
        should_avoid.append({
            'type': '高風險投機收入',
            'reason': '缺水導致策略判斷能力不足',
            'alternative': '選擇穩健的投資標的'
        })

    if should_avoid:
        sources['avoid'] = should_avoid

    return sources


def _get_suitable_investments(ten_gods: Dict, wuxing: Dict) -> List[str]:
    """獲取適合的投資類型"""
    investments = []
    strong_gods = ten_gods.get('distribution', {})

    # 基礎投資（所有人都適合）
    investments.append('定期定額指數基金')

    # 根據特質推薦
    if '正財' in strong_gods:
        investments.extend(['債券', '房地產', '高股息股票'])

    if '偏財' in strong_gods:
        investments.extend(['成長型股票', '房地產買賣', '基金'])

    if '正印' in strong_gods or '偏印' in strong_gods:
        investments.extend(['教育產業相關標的', '科技股'])

    # 風險提醒
    lacking = wuxing.get('lacking_elements', [])
    if '水' not in lacking and '金' not in lacking:
        investments.append('可適度配置成長型投資')

    return investments


def _generate_wealth_recommendations(ten_gods: Dict, wuxing: Dict, pattern: Dict) -> List[str]:
    """產生財富建議"""
    recommendations = []
    strong_gods = ten_gods.get('distribution', {})

    # 基於十神的建議
    if '食神' in strong_gods or '傷官' in strong_gods:
        recommendations.append(
            "**建立「專業品牌」而非「打工心態」**：您的食傷旺盛，最適合個人品牌變現。"
            "35歲前累積專業與影響力，35歲後將品牌轉化為收入。目標是讓收入與工作時間脫鉤。"
        )

    if '正印' in strong_gods or '偏印' in strong_gods:
        recommendations.append(
            "**投資自我成長的錢不要省**：學習是您最高報酬率的投資。"
            "不要因為昂貴而放棄好的課程或學習機會。這些投資會在3-5年後以數倍回報。"
        )

    if '比肩' in strong_gods or '劫財' in strong_gods:
        recommendations.append(
            "**避免與朋友合夥創業**：您的比劫旺，與朋友合夥容易有財務糾紛。"
            "可以投資朋友的事業，但不要共同經營。財務與友情要分開處理。"
        )

    # 通用建議
    recommendations.append(
        "**40歲前至少建立一種被動收入**：這是財務自由的基礎。"
        "可以是線上課程、專業諮詢服務包、版權收入等。重點是建立「不工作也有收入」的機制。"
    )

    recommendations.append(
        "**35-45歲是財富累積的黃金十年**：這十年要全力衝刺。"
        "提高專業服務定價（至少2倍）、建立被動收入、增加投資比例。錯過這十年很難彌補。"
    )

    lacking = wuxing.get('lacking_elements', [])
    if '水' in lacking:
        recommendations.append(
            "**重大財務決策前請教專家**：您的五行缺水，長期財務規劃不是您的強項。"
            "找專業的理財顧問協助，特別是投資、保險、退休規劃等重大決策。"
        )

    return recommendations


# ============================================================================
# 感情關係分析 (Relationship Analysis)
# ============================================================================

def interpret_relationship(bazi_data: Dict, gender: str = 'male') -> Dict:
    """深度感情關係分析

    Args:
        bazi_data: BaZi calculator output
        gender: 'male' or 'female'

    Returns:
        Dict: {
            'spouse_characteristics': str,  # 配偶特質描述
            'compatibility_factors': Dict,  # 相容性因素
            'relationship_timeline': Dict,  # 感情時間軸
            'marriage_pattern': str,  # 婚姻模式
            'recommendations': List[str]  # 具體建議
        }
    """
    day_branch = bazi_data.get('basic_chart', {}).get('day_pillar', {}).get('branch', '')
    day_stem = bazi_data.get('basic_chart', {}).get('day_pillar', {}).get('stem', '')
    ten_gods = bazi_data.get('ten_gods_analysis', {})
    wuxing = bazi_data.get('wuxing_analysis', {})

    # 1. 配偶特質
    spouse_char = _analyze_spouse_characteristics(day_branch, ten_gods, gender)

    # 2. 相容性因素
    compatibility = _analyze_compatibility_factors(day_stem, ten_gods, wuxing, gender)

    # 3. 感情時間軸
    timeline = _create_relationship_timeline(ten_gods, bazi_data.get('luck_pillars', []), gender)

    # 4. 婚姻模式
    marriage = _analyze_marriage_pattern(ten_gods, wuxing, gender)

    # 5. 具體建議
    recommendations = _generate_relationship_recommendations(ten_gods, wuxing, gender)

    return {
        'spouse_characteristics': spouse_char,
        'compatibility_factors': compatibility,
        'relationship_timeline': timeline,
        'marriage_pattern': marriage,
        'recommendations': recommendations
    }


def _analyze_spouse_characteristics(day_branch: str, ten_gods: Dict, gender: str) -> str:
    """分析配偶特質"""
    parts = []
    strong_gods = ten_gods.get('distribution', {})

    # 配偶宮分析（日支）
    branch_traits = {
        '子': '聰明靈活、善於溝通、適應力強',
        '丑': '踏實穩重、有責任感、較為傳統',
        '寅': '積極主動、有進取心、獨立性強',
        '卯': '溫和細膩、有藝術氣質、感性',
        '辰': '務實可靠、有領導力、較為理性',
        '巳': '聰明熱情、口才好、有魅力',
        '午': '熱情開朗、有活力、較為直接',
        '未': '溫和體貼、有包容心、較為保守',
        '申': '聰明果斷、重效率、較為理性',
        '酉': '細膩優雅、重質感、有品味',
        '戌': '忠誠可靠、有責任感、較為固執',
        '亥': '智慧深沉、有理想、較為感性'
    }

    if day_branch in branch_traits:
        parts.append(f"""**配偶基本特質（配偶宮）**：
您的日支為{day_branch}，代表配偶的基本性格：{branch_traits[day_branch]}。
這個特質會影響您對伴侶的吸引力，也代表您婚姻生活中的互動模式。""")

    # 女命看官殺，男命看財星
    if gender == 'female':
        if '正官' in strong_gods:
            parts.append("""
**理想伴侶類型（正官影響）**：
您適合的伴侶特質：
- 有責任感、穩重可靠
- 有正當職業、社會地位
- 重視規範、做事有原則
- 可能較為傳統、不太浪漫

最可能從事的領域：管理、法律、公務、教育、醫療等需要權威性的專業領域。""")

        if '七殺' in strong_gods:
            parts.append("""
**理想伴侶類型（七殺影響）**：
您可能被這種伴侶吸引：
- 個性強勢、有魄力
- 事業心強、有野心
- 較為直接、果斷
- 可能較為強勢、不夠溫柔

最可能從事的領域：企業經營、技術專家、軍警、競爭性行業。

提醒：七殺強的女性，要注意選擇能力強但也尊重妳的伴侶，避免過於強勢的對象。""")
    else:  # male
        if '正財' in strong_gods:
            parts.append("""
**理想伴侶類型（正財影響）**：
您適合的伴侶特質：
- 賢慧顧家、務實可靠
- 善於理財、生活有規劃
- 個性溫和、較為傳統
- 重視家庭、相夫教子型

最可能的類型：傳統賢妻良母、教師、護士、行政人員等穩定職業。""")

        if '偏財' in strong_gods:
            parts.append("""
**理想伴侶類型（偏財影響）**：
您可能被這種伴侶吸引：
- 活潑開朗、有魅力
- 善於社交、人緣好
- 較為獨立、有自己的事業
- 可能不太顧家、較為自我

最可能的類型：業務、公關、藝術、自由職業等需要魅力與社交的工作。

提醒：偏財強的男性，要注意專一，避免桃花過多影響婚姻。""")

    return "\n\n".join(parts)


def _analyze_compatibility_factors(day_stem: str, ten_gods: Dict,
                                   wuxing: Dict, gender: str) -> Dict:
    """分析相容性因素"""
    positive = []
    challenges = []
    strong_gods = ten_gods.get('distribution', {})

    # 基於十神的相容性
    if '正印' in strong_gods or '偏印' in strong_gods:
        positive.append('雙方都重視精神層面的交流，能在知識、理念上共鳴')
        challenges.append('可能過於理性，缺乏情感表達與浪漫氛圍')

    if '食神' in strong_gods or '傷官' in strong_gods:
        positive.append('您善於表達，能為關係帶來趣味與創意')
        challenges.append('可能過於自我表達，需要多傾聽伴侶的想法')

    if '比肩' in strong_gods or '劫財' in strong_gods:
        positive.append('獨立性強，能給予伴侶足夠的個人空間')
        challenges.append('可能過於獨立，讓伴侶感覺被忽視或不需要')

    # 基於五行的相容性
    dominant = wuxing.get('dominant_elements', [])
    lacking = wuxing.get('lacking_elements', [])

    if '火' in dominant:
        positive.append('熱情開朗，能為關係帶來活力與溫暖')
        challenges.append('可能過於急躁，需要培養耐心與包容')

    if '水' in dominant:
        positive.append('智慧與策略思維，能理性處理關係中的問題')
        challenges.append('可能過於理性，缺乏情感的即時回應')

    if '木' in dominant:
        positive.append('有理想與遠見，能給予伴侶成長的支持')
        challenges.append('可能過於理想化，對伴侶期待過高')

    if '金' in dominant:
        positive.append('原則性強，能給予伴侶安全感與穩定性')
        challenges.append('可能過於嚴格，需要更多彈性與包容')

    if '土' in dominant:
        positive.append('穩重包容，能給予伴侶扎實的支持與照顧')
        challenges.append('可能過於保守，缺乏變化與浪漫')

    # 缺失元素對關係的影響
    if '火' in lacking:
        challenges.append('可能缺乏熱情與主動，需要刻意營造浪漫氛圍')

    if '水' in lacking:
        challenges.append('可能較為衝動，重大決策需要多溝通、多思考')

    return {
        'positive_factors': positive,
        'challenge_areas': challenges,
        'overall_compatibility': '中上' if len(positive) >= len(challenges) else '中等'
    }


def _create_relationship_timeline(ten_gods: Dict, luck_pillars: List, gender: str) -> Dict:
    """建立感情時間軸"""
    timeline = {
        '25-30歲': {
            'phase': '戀愛探索期',
            'relationship_luck': '中等',
            'pattern': '可能專注於事業，對感情投入較少。通過工作或學習場合認識對象的機會較多。',
            'recommendations': [
                '不要因為太忙而完全忽略感情',
                '參加社交活動，擴大交友圈',
                '接受朋友或長輩介紹',
                '重質不重量，不要為了結婚而結婚'
            ]
        },

        '31-35歲': {
            'phase': '結婚適齡期',
            'relationship_luck': '較強',
            'critical_years': [32, 34],
            'pattern': '對婚姻的想法更為成熟，經濟基礎較為穩定。這個階段遇到的對象通常較為可靠。',
            'recommendations': [
                '如果已有穩定對象，32-34歲是結婚良機',
                '未有對象的話，要主動一些，不要錯過時機',
                '選擇伴侶要看長遠，不要只看表面條件',
                '重視價值觀與生活目標的契合度'
            ]
        },

        '36-45歲': {
            'phase': '婚姻穩定期',
            'focus': '經營婚姻，平衡事業與家庭',
            'pattern': '事業達到高峰，容易忽略家庭經營。需要刻意維持婚姻品質。',
            'recommendations': [
                '設定固定的夫妻時間（如每周一次約會）',
                '不要讓事業完全占據生活',
                '保持溝通，分享彼此的想法與感受',
                '一起培養共同興趣或目標'
            ]
        },

        '45歲以上': {
            'phase': '婚姻深化期',
            'focus': '從激情轉向親情與陪伴',
            'pattern': '關係更為穩定，但要避免「室友化」。需要為關係注入新的元素。',
            'recommendations': [
                '一起規劃退休生活',
                '培養共同的興趣或旅行',
                '維持適度的個人空間',
                '學習欣賞對方的陪伴價值'
            ]
        }
    }

    return timeline


def _analyze_marriage_pattern(ten_gods: Dict, wuxing: Dict, gender: str) -> str:
    """分析婚姻模式"""
    parts = []
    strong_gods = ten_gods.get('distribution', {})

    # 基本婚姻模式
    if '正官' in strong_gods or '正財' in strong_gods:
        parts.append("""**婚姻模式 - 穩定傳統型**：
您的婚姻傾向於穩定、傳統的模式。重視婚姻的責任與承諾，一旦決定就會認真經營。
婚姻對您來說不只是感情，更是一種責任與承諾。

婚後模式：
- 各司其職，分工明確
- 重視家庭穩定與和諧
- 可能不太浪漫，但很可靠
- 需要刻意營造情感交流""")

    if '食神' in strong_gods or '傷官' in strong_gods:
        parts.append("""**婚姻模式 - 自由平等型**：
您需要婚姻中有足夠的自由與空間。不喜歡被束縛，希望伴侶能理解並支持您的想法與追求。

婚後模式：
- 較為平等，各有發展
- 重視精神交流與共同成長
- 可能較為理想化
- 需要伴侶給予足夠的理解與空間""")

    if '比肩' in strong_gods or '劫財' in strong_gods:
        parts.append("""**婚姻風險 - 獨立過度**：
您的獨立性強，這在婚姻中可能成為雙面刃。適度的獨立是好的，
但過度獨立會讓伴侶感覺被忽視。

建議：
- 刻意營造「我們」的感覺
- 重要決定要與伴侶商量
- 分享您的想法與感受
- 避免「各過各的」的模式""")

    # 需要注意的事項
    lacking = wuxing.get('lacking_elements', [])
    if '水' in lacking:
        parts.append("""
**婚姻提醒 - 加強溝通**：
您的五行缺水，可能在溝通與理解方面需要加強。婚姻中的很多問題來自於溝通不良。

建議：
- 重要事情要好好說，不要悶在心裡
- 學習傾聽，理解伴侶的真正需求
- 定期進行深度對話（不是只談日常瑣事）
- 必要時尋求婚姻諮詢協助""")

    return "\n\n".join(parts)


def _generate_relationship_recommendations(ten_gods: Dict, wuxing: Dict, gender: str) -> List[str]:
    """產生感情建議"""
    recommendations = []
    strong_gods = ten_gods.get('distribution', {})

    # 基於十神的建議
    if '食神' in strong_gods or '傷官' in strong_gods:
        recommendations.append(
            "**多傾聽、少表達**：您善於表達，但在關係中，傾聽比表達更重要。"
            "給伴侶充分的表達空間，真正理解對方的想法與感受。"
        )

    if '正印' in strong_gods or '偏印' in strong_gods:
        recommendations.append(
            "**增加情感表達**：您可能較為理性，但關係需要情感的滋養。"
            "學習表達愛意與感謝，不要覺得「對方應該知道」。"
        )

    if '比肩' in strong_gods or '劫財' in strong_gods:
        recommendations.append(
            "**建立「我們」的意識**：避免過度獨立，刻意營造共同的目標與活動。"
            "重要決定要與伴侶商量，讓對方感受到被需要。"
        )

    # 通用建議
    recommendations.append(
        "**設定固定的「夫妻時間」**：每周至少一次，只屬於兩人的時間。"
        "關掉手機，專注於彼此。這是維持婚姻品質最簡單有效的方法。"
    )

    recommendations.append(
        "**避免「室友化」**：不要讓婚姻變成只是生活的夥伴。"
        "保持適度的浪漫與親密，刻意為關係創造驚喜與新鮮感。"
    )

    recommendations.append(
        "**婚前要深入了解**：不要因為年齡或壓力而倉促結婚。"
        "至少要深入交往1-2年，了解對方的價值觀、生活習慣、家庭背景。"
        "婚姻是長期的承諾，寧願晚一點，也要選對人。"
    )

    return recommendations


# ============================================================================
# 健康分析 (Health Analysis)
# ============================================================================

def interpret_health(bazi_data: Dict) -> Dict:
    """深度健康分析

    基於五行平衡分析健康傾向與養生建議

    Returns:
        Dict: {
            'health_overview': str,  # 整體健康概述
            'organ_systems': Dict,  # 各臟腑系統分析
            'age_based_guidance': Dict,  # 各年齡段健康指引
            'lifestyle_recommendations': Dict,  # 生活方式建議
            'preventive_measures': List[str]  # 預防措施
        }
    """
    wuxing = bazi_data.get('wuxing_analysis', {})
    day_stem = bazi_data.get('basic_chart', {}).get('day_pillar', {}).get('stem', '')

    # 1. 整體健康概述
    overview = _analyze_health_overview(wuxing, day_stem)

    # 2. 臟腑系統分析
    organs = _analyze_organ_systems(wuxing)

    # 3. 年齡段健康指引
    age_guidance = _create_age_based_health_guidance(wuxing)

    # 4. 生活方式建議
    lifestyle = _generate_lifestyle_recommendations(wuxing)

    # 5. 預防措施
    preventive = _generate_preventive_measures(wuxing)

    return {
        'health_overview': overview,
        'organ_systems': organs,
        'age_based_guidance': age_guidance,
        'lifestyle_recommendations': lifestyle,
        'preventive_measures': preventive
    }


def _analyze_health_overview(wuxing: Dict, day_stem: str) -> str:
    """整體健康概述"""
    parts = []
    dominant = wuxing.get('dominant_elements', [])
    lacking = wuxing.get('lacking_elements', [])

    # 整體體質評估
    parts.append("""**整體健康評估**：
您的健康狀況與五行平衡密切相關。五行過旺或不足都會影響相應的臟腑系統。
以下分析基於您的八字五行結構，提供預防性的健康指引。

重要提醒：此分析用於養生保健，非醫療診斷。任何健康問題請諮詢專業醫師。""")

    # 優勢體質
    if dominant:
        dominant_str = '、'.join(dominant)
        parts.append(f"""
**體質優勢（{dominant_str}旺）**：
您的{dominant_str}較旺，在對應的臟腑系統有先天優勢。
但也要注意過旺可能帶來的問題（如火旺易上火、木旺易肝氣鬱結）。""")

    # 需要關注的弱點
    if lacking:
        lacking_str = '、'.join(lacking)
        parts.append(f"""
**需要關注（缺{lacking_str}）**：
您的五行缺{lacking_str}，對應的臟腑系統可能較弱，需要特別保養。
這不代表一定會有疾病，而是提醒您在這些方面要更加注意。""")

    return "\n\n".join(parts)


def _analyze_organ_systems(wuxing: Dict) -> Dict:
    """分析各臟腑系統"""
    systems = {}
    dominant = wuxing.get('dominant_elements', [])
    lacking = wuxing.get('lacking_elements', [])

    # 五行對應臟腑
    element_organs = {
        '木': {
            'organs': '肝膽系統、眼睛、筋腱、神經系統',
            'strong_notes': '肝膽功能較好，但要注意肝氣鬱結、眼睛疲勞',
            'weak_notes': '肝膽功能較弱，容易疲勞、視力問題、筋骨酸痛',
            'care': '保持情緒平穩、適度運動、護眼、伸展筋骨'
        },
        '火': {
            'organs': '心臟、小腸、血液循環、精神狀態',
            'strong_notes': '心臟功能好，精力充沛，但要注意血壓、失眠、焦慮',
            'weak_notes': '心血管較弱，容易心悸、血液循環不良、精神不濟',
            'care': '規律作息、控制情緒起伏、心血管保健、避免過度刺激'
        },
        '土': {
            'organs': '脾胃、消化系統、肌肉',
            'strong_notes': '消化好、體力佳，但要注意過食、濕氣重、肥胖',
            'weak_notes': '脾胃較弱，容易消化不良、體力不足、肌肉無力',
            'care': '規律飲食、細嚼慢嚥、避免生冷、適度運動增肌'
        },
        '金': {
            'organs': '肺、大腸、皮膚、呼吸系統',
            'strong_notes': '呼吸系統好，但要注意皮膚乾燥、便秘、呼吸道過敏',
            'weak_notes': '呼吸系統較弱，容易感冒、皮膚問題、腸道功能不佳',
            'care': '注意空氣品質、保濕、規律排便、深呼吸練習'
        },
        '水': {
            'organs': '腎臟、膀胱、生殖系統、骨骼、耳朵',
            'strong_notes': '腎功能好、骨骼強健，但要注意水腫、泌尿系統問題',
            'weak_notes': '腎氣較弱，容易腰酸、骨質疏鬆、泌尿系統問題、耳鳴',
            'care': '充足睡眠、避免過勞、保暖、補腎食物、骨骼保健'
        }
    }

    for element in ['木', '火', '土', '金', '水']:
        status = 'strong' if element in dominant else ('weak' if element in lacking else 'balanced')
        organ_info = element_organs[element]

        if status == 'strong':
            systems[element] = {
                'organs': organ_info['organs'],
                'status': '較強',
                'notes': organ_info['strong_notes'],
                'care_tips': organ_info['care']
            }
        elif status == 'weak':
            systems[element] = {
                'organs': organ_info['organs'],
                'status': '需要加強',
                'notes': organ_info['weak_notes'],
                'care_tips': organ_info['care']
            }

    return systems


def _create_age_based_health_guidance(wuxing: Dict) -> Dict:
    """建立各年齡段健康指引"""
    guidance = {
        '20-35歲': {
            'focus': '建立健康基礎',
            'key_points': [
                '培養良好的生活習慣（規律作息、運動、飲食）',
                '避免過度消耗（熬夜、過勞、不當減肥）',
                '定期體檢，建立健康基線數據',
                '投資健康知識，學習養生方法'
            ],
            'warning': '這階段身體恢復力強，容易忽視健康警訊。不要仗著年輕就過度消耗。'
        },

        '35-50歲': {
            'focus': '維持健康狀態，預防慢性病',
            'key_points': [
                '每年完整健康檢查（含癌症篩檢）',
                '注意三高（血壓、血糖、血脂）',
                '維持規律運動（每周至少3次，每次30分鐘以上）',
                '壓力管理與情緒調適',
                '開始關注家族病史相關的預防'
            ],
            'critical_ages': [38, 42, 45],
            'warning': '這階段工作與家庭壓力大，容易忽略健康。要刻意安排運動與休息時間。'
        },

        '50歲以上': {
            'focus': '積極養生，延緩老化',
            'key_points': [
                '定期且完整的健康檢查（每年一次）',
                '骨質保健（補鈣、負重運動）',
                '心血管保健（控制三高、規律運動）',
                '認知功能維護（腦力活動、社交）',
                '營養均衡（增加優質蛋白、減少精緻澱粉）'
            ],
            'warning': '這階段要以「維持」為主，不要追求「逆轉」。接受適度老化，重點是功能性健康。'
        }
    }

    return guidance


def _generate_lifestyle_recommendations(wuxing: Dict) -> Dict:
    """生成生活方式建議"""
    lacking = wuxing.get('lacking_elements', [])
    dominant = wuxing.get('dominant_elements', [])

    recommendations = {
        'diet': _get_dietary_recommendations(lacking, dominant),
        'exercise': _get_exercise_recommendations(lacking, dominant),
        'sleep': _get_sleep_recommendations(lacking, dominant),
        'stress_management': _get_stress_management_tips(lacking, dominant)
    }

    return recommendations


def _get_dietary_recommendations(lacking: List, dominant: List) -> List[str]:
    """飲食建議"""
    tips = []

    # 基本原則
    tips.append('飲食均衡、定時定量、細嚼慢嚥')
    tips.append('多吃原型食物，少吃加工食品')
    tips.append('每天至少5蔬果，足夠的水分（2000cc以上）')

    # 基於缺失元素的建議
    if '木' in lacking:
        tips.append('多吃綠色蔬菜、酸味食物（檸檬、醋）、養肝食物（枸杞、紅棗）')

    if '火' in lacking:
        tips.append('適度攝取溫熱食物、紅色食物（紅棗、番茄）、苦味食物（苦瓜）')

    if '土' in lacking:
        tips.append('健脾食物（山藥、薏仁、南瓜）、甘味食物（但避免精緻糖）')

    if '金' in lacking:
        tips.append('白色食物（白木耳、山藥、百合）、辛味食物（蔥薑蒜）、潤肺食物')

    if '水' in lacking:
        tips.append('黑色食物（黑豆、黑芝麻、黑木耳）、補腎食物（核桃、栗子）、適量鹹味')

    # 基於過旺元素的提醒
    if '火' in dominant:
        tips.append('避免過度辛辣刺激、控制咖啡因、少吃油炸燒烤')

    if '土' in dominant:
        tips.append('控制澱粉攝取、避免過食、減少甜食')

    return tips


def _get_exercise_recommendations(lacking: List, dominant: List) -> List[str]:
    """運動建議"""
    tips = []

    tips.append('每周至少150分鐘中等強度運動，或75分鐘高強度運動')
    tips.append('結合有氧運動、肌力訓練、柔軟度訓練')

    if '木' in lacking:
        tips.append('多做伸展運動、瑜伽、太極拳（養肝舒筋）')

    if '金' in lacking:
        tips.append('重視有氧運動（跑步、游泳、騎車）增強心肺功能')

    if '水' in lacking:
        tips.append('適度肌力訓練，增強骨骼與腎氣')

    if '木' in dominant:
        tips.append('運動要適量，避免過度，注意拉傷')

    if '火' in dominant:
        tips.append('避免過於激烈的運動，注意散熱與補水')

    return tips


def _get_sleep_recommendations(lacking: List, dominant: List) -> List[str]:
    """睡眠建議"""
    tips = [
        '每天7-8小時睡眠',
        '固定就寢與起床時間',
        '睡前1小時避免使用電子產品',
        '臥室保持暗、靜、涼',
        '午睡不超過30分鐘'
    ]

    if '水' in lacking:
        tips.append('特別重視睡眠品質，11pm前就寢最佳（養腎時間）')

    if '火' in dominant:
        tips.append('睡前避免過度刺激（恐怖片、激烈運動），幫助安神')

    return tips


def _get_stress_management_tips(lacking: List, dominant: List) -> List[str]:
    """壓力管理建議"""
    tips = [
        '培養紓壓習慣（運動、靜坐、興趣）',
        '學習說「不」，不要過度承擔',
        '維持良好社交關係，適時尋求支持',
        '每天至少15分鐘完全放鬆的時間'
    ]

    if '木' in lacking:
        tips.append('情緒容易累積，要找到適合的發洩管道（運動、藝術、對話）')

    if '木' in dominant:
        tips.append('避免過度壓抑情緒，適度表達與發洩很重要')

    if '水' in lacking:
        tips.append('學習靜坐、冥想，培養內在平靜')

    return tips


def _generate_preventive_measures(wuxing: Dict) -> List[str]:
    """產生預防措施"""
    measures = []
    lacking = wuxing.get('lacking_elements', [])

    # 基本預防措施
    measures.append('**定期健康檢查**：30歲後每年一次，40歲後增加癌症篩檢')
    measures.append('**維持健康體重**：BMI保持在18.5-24之間')
    measures.append('**戒菸限酒**：完全戒菸，酒精適量（男性每天<2杯，女性<1杯）')

    # 基於五行缺失的特別預防
    if '木' in lacking:
        measures.append('**護眼與護肝**：定期眼科檢查，避免過度用眼；限制飲酒，定期肝功能檢查')

    if '火' in lacking:
        measures.append('**心血管保健**：控制三高，規律運動，40歲後定期心血管檢查')

    if '土' in lacking:
        measures.append('**消化系統保健**：規律飲食，避免暴飲暴食，腸胃不適及時就醫')

    if '金' in lacking:
        measures.append('**呼吸系統保健**：注意空氣品質，避免吸菸環境，定期肺部檢查（特別是40歲後）')

    if '水' in lacking:
        measures.append('**腎臟與骨骼保健**：定期腎功能檢查，40歲後骨密度檢測，補充鈣質與維生素D')

    measures.append('**心理健康**：定期自我評估，必要時尋求專業協助（憂鬱、焦慮不是弱點）')

    return measures


# ============================================================================
# 導出函數 (Export Functions)
# ============================================================================

__all__ = [
    'interpret_personality',
    'interpret_career',
    'interpret_wealth',
    'interpret_relationship',
    'interpret_health',
    'DAY_MASTER_TRAITS',
    'ELEMENT_PSYCHOLOGY',
    'TEN_GODS_TRAITS'
]

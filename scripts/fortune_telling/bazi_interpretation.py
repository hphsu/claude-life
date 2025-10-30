"""
八字深度詮釋引擎 (BaZi Interpretation Engine)
==============================================

提供專業級八字命理詮釋，包括：
1. 性格心理分析（200-300字）
2. 事業深度解讀（500-800字）
3. 財富運勢詳析（500-800字）
4. 感情婚姻指南（500-800字）
5. 健康養生建議（500-800字）

基於子平八字、滴天髓等經典命理理論，提供具體、可行動的洞察
"""

from typing import Dict, List, Optional
from .utils import (
    WuXing,
    TenGods,
    get_wuxing_from_stem,
    WUXING_GENERATES,
    WUXING_CONTROLS
)


# ============================================
# 天干特質資料庫
# ============================================

DAY_MASTER_ESSENCE = {
    "甲": {
        "essence": """作為甲木日主，您天生具有向上生長、不屈不撓的特質。甲木象徵參天大樹，
代表您有遠大的志向與堅定的意志力。您不喜歡被束縛，追求自由發展的空間，
同時也有領導他人的潛力。您的性格正直剛毅，做事光明磊落，但有時可能過於固執，
不夠圓融。在成長過程中，您需要學習彈性與包容，才能將您的領導才能發揮到極致。""",
        "strengths": ["正直剛毅", "有遠大志向", "領導能力", "不屈不撓"],
        "challenges": ["過於固執", "不夠圓融", "難以妥協"],
        "growth_path": "學習彈性思考，培養同理心，在堅持原則與圓融處事之間取得平衡"
    },
    "乙": {
        "essence": """作為乙木日主，您如同柔軟的藤蔓或花草，具有柔韌適應的特質。
您善於順應環境，以柔克剛，在困難中依然能找到生存之道。您的性格溫和親切，
善於與人相處，具有很強的同理心。您的優勢在於適應力強，能夠在各種環境中生存發展，
但有時可能缺乏主見，過於隨波逐流。您需要培養內在的核心信念，在保持彈性的同時，
也要有自己的原則與立場。""",
        "strengths": ["適應力強", "溫和親切", "善於協調", "堅韌不拔"],
        "challenges": ["缺乏主見", "容易隨波逐流", "不夠果斷"],
        "growth_path": "建立核心價值觀，在靈活與原則之間找到平衡點"
    },
    "丙": {
        "essence": """作為丙火日主，您如同太陽一般，熱情洋溢、光明磊落。
您天生具有感染他人的魅力，走到哪裡都能成為焦點。您的性格開朗積極，
充滿活力與創造力，喜歡嘗試新事物。您慷慨大方，願意幫助他人，
但有時可能過於衝動，缺乏深思熟慮。您的能量像太陽一樣強大但容易消耗，
需要學習節制與持久力，才能將您的光芒長久地照耀他人。""",
        "strengths": ["熱情洋溢", "光明磊落", "富有魅力", "創造力強"],
        "challenges": ["過於衝動", "缺乏耐性", "能量消耗快"],
        "growth_path": "培養耐心與持久力，學習在熱情與冷靜之間取得平衡"
    },
    "丁": {
        "essence": """作為丁火日主，您如同燭火或星光，雖不如太陽耀眼，但溫暖持久。
您的性格細膩敏感，內心豐富，具有藝術氣質。您注重細節，做事精緻，
對美有獨特的品味。您的光芒雖然柔和，但能在黑暗中給人指引與溫暖。
您可能較為內向，不喜歡張揚，但內心有堅定的信念。您需要學習展現自己，
不要過度謙虛，您的光芒值得被更多人看見。""",
        "strengths": ["細膩敏感", "藝術氣質", "注重品質", "溫暖持久"],
        "challenges": ["過於內向", "自我懷疑", "不夠自信"],
        "growth_path": "培養自信，學習適度展現自己的才華與價值"
    },
    "戊": {
        "essence": """作為戊土日主，您如同高山大地，穩重厚實、包容萬物。
您的性格踏實可靠，做事認真負責，是他人可以依靠的對象。您有很強的責任感，
一旦承諾就會全力以赴。您的思維務實，不喜歡空談理論，重視實際成果。
您的穩定性是您最大的優勢，但有時可能過於保守，缺乏創新。
您需要學習適度冒險，在穩健與創新之間找到平衡。""",
        "strengths": ["穩重踏實", "責任感強", "可靠值得信賴", "務實"],
        "challenges": ["過於保守", "缺乏創新", "變通性不足"],
        "growth_path": "培養創新思維，學習在穩健中求變革"
    },
    "己": {
        "essence": """作為己土日主，您如同田園沃土，溫和滋養、默默奉獻。
您的性格謙和低調，善於照顧他人，具有很強的服務精神。您注重實際，
腳踏實地，不好高騖遠。您的包容力很強，能接納各種不同的人與事。
您可能不太會拒絕他人，有時會委屈自己成全別人。您需要學習設定界限，
在照顧他人的同時，也要照顧好自己的需求。""",
        "strengths": ["溫和謙遜", "包容力強", "服務精神", "務實可靠"],
        "challenges": ["難以拒絕", "容易委屈自己", "缺乏自我主張"],
        "growth_path": "學習設定界限，在付出與接受之間找到平衡"
    },
    "庚": {
        "essence": """作為庚金日主，您如同堅硬的礦石或刀劍，果斷剛毅、不屈不撓。
您的性格直率坦誠，做事果決，不拖泥帶水。您有很強的原則性，
黑白分明，不喜歡曖昧模糊。您的決策能力強，在關鍵時刻能當機立斷。
您的正義感強，願意為正確的事情挺身而出。但有時可能過於剛硬，
不夠柔軟，在人際關係上可能顯得不夠圓融。您需要學習柔軟與包容，
在剛毅與溫和之間取得平衡。""",
        "strengths": ["果斷剛毅", "原則性強", "正義感", "決策力強"],
        "challenges": ["過於剛硬", "不夠圓融", "容易得罪人"],
        "growth_path": "培養同理心與包容力，學習剛柔並濟"
    },
    "辛": {
        "essence": """作為辛金日主，您如同珠玉寶石，精緻細膩、注重品質。
您的性格優雅有品味，做事精益求精，追求完美。您重視細節，
有很好的審美能力。您的思維細膩，善於觀察，能注意到他人忽略的地方。
您可能較為敏感，容易受環境影響，對批評比較在意。您需要學習接納不完美，
培養內在的堅韌，不要過度追求外在的完美。""",
        "strengths": ["優雅精緻", "追求完美", "審美力強", "細膩敏銳"],
        "challenges": ["過度敏感", "容易受傷", "完美主義"],
        "growth_path": "接納不完美，培養內在堅韌，學習自我慈悲"
    },
    "壬": {
        "essence": """作為壬水日主，您如同江河大海，智慧深遠、包容廣闊。
您的思維靈活，善於變通，能夠適應各種環境。您聰明機智，
學習能力強，對知識充滿好奇。您的視野開闊，不拘小節，
能看到事情的全局。您的適應力和生存力都很強。但有時可能過於善變，
缺乏持久力，做事容易三分鐘熱度。您需要學習專注與堅持，
在靈活與穩定之間找到平衡。""",
        "strengths": ["聰明機智", "靈活變通", "視野開闊", "學習力強"],
        "challenges": ["善變不定", "缺乏持久力", "容易分心"],
        "growth_path": "培養專注力與持久力，在變與不變之間取得平衡"
    },
    "癸": {
        "essence": """作為癸水日主，您如同雨露甘霖，溫柔細膩、滋養萬物。
您的性格溫和內斂，富有同情心，善於理解他人。您的思維細膩深邃，
有很強的直覺力和洞察力。您喜歡思考，重視精神層面的追求。
您可能較為內向，不太喜歡張揚，但內心世界豐富。您的包容性強，
但有時可能過於柔弱，缺乏主見。您需要學習堅定立場，
在柔軟與堅定之間找到平衡。""",
        "strengths": ["溫柔細膩", "直覺力強", "富有同情心", "思考深邃"],
        "challenges": ["過於柔弱", "缺乏主見", "容易猶豫"],
        "growth_path": "培養決斷力，在溫柔與堅定之間取得平衡"
    }
}


# ============================================
# 十神性格特質資料庫
# ============================================

TEN_GODS_PERSONALITY = {
    TenGods.BI_JIAN.value: {
        "traits": "獨立自主，有主見，競爭意識強",
        "positive": "自信果斷，不依賴他人，能獨當一面",
        "negative": "可能較為自我，不易妥協，競爭心過強",
        "advice": "學習團隊合作，培養包容心"
    },
    TenGods.JIE_CAI.value: {
        "traits": "行動力強，勇於冒險，喜歡挑戰",
        "positive": "積極進取，敢於突破，執行力強",
        "negative": "可能過於激進，衝動行事，容易與人衝突",
        "advice": "培養耐心，三思而後行"
    },
    TenGods.SHI_SHEN.value: {
        "traits": "樂觀開朗，富有創意，善於表達",
        "positive": "思維活躍，點子多，溝通能力強，享受生活",
        "negative": "可能過於理想化，缺乏執行力，容易分心",
        "advice": "增強執行力，將創意落實為成果"
    },
    TenGods.SHANG_GUAN.value: {
        "traits": "聰明才智，表達能力強，追求創新",
        "positive": "才華橫溢，口才佳，創造力強，勇於表達",
        "negative": "可能過於主觀，不服管教，容易得罪人",
        "advice": "學習謙虛，尊重他人意見"
    },
    TenGods.PIAN_CAI.value: {
        "traits": "靈活機智，善於把握機會，財運佳",
        "positive": "商業頭腦好，應變能力強，容易獲得橫財",
        "negative": "可能過於投機，缺乏穩定性，感情複雜",
        "advice": "注重穩健經營，建立長期關係"
    },
    TenGods.ZHENG_CAI.value: {
        "traits": "務實穩重，理財有道，重視物質",
        "positive": "財務規劃好，收入穩定，懂得積累",
        "negative": "可能過於現實，缺乏浪漫，較為保守",
        "advice": "平衡物質與精神追求"
    },
    TenGods.QI_SHA.value: {
        "traits": "果斷剛毅，意志堅定，有魄力",
        "positive": "領導力強，能在困境中突破，執行力佳",
        "negative": "可能過於強勢，缺乏耐心，容易與人對立",
        "advice": "學習柔軟，以德服人而非以力壓人"
    },
    TenGods.ZHENG_GUAN.value: {
        "traits": "正直守規，責任感強，重視名譽",
        "positive": "品德端正，值得信賴，適合管理職",
        "negative": "可能過於保守，缺乏創新，壓力大",
        "advice": "適度放鬆，培養創新思維"
    },
    TenGods.PIAN_YIN.value: {
        "traits": "聰明好學，第六感強，獨立思考",
        "positive": "學習能力強，直覺準確，有專業深度",
        "negative": "可能過於孤僻，不善社交，想太多",
        "advice": "多與人交流，將知識轉化為實際應用"
    },
    TenGods.ZHENG_YIN.value: {
        "traits": "溫和穩重，重視學習，有貴人運",
        "positive": "熱愛知識，品德良好，長輩相助",
        "negative": "可能過於依賴，缺乏主動性，思慮過多",
        "advice": "培養獨立性，勇於主動出擊"
    }
}


# ============================================
# 核心詮釋函數
# ============================================

def interpret_personality(bazi_data: Dict) -> Dict:
    """
    深度性格詮釋

    Args:
        bazi_data: 八字分析結果（來自 BaziCalculator.analyze()）

    Returns:
        詳細的性格分析，包含 2000+ 字的深度解讀
    """
    day_master = bazi_data["basic_chart"]["day_master"]
    strength = bazi_data["strength"]
    ten_gods = bazi_data["ten_gods_analysis"]
    wuxing = bazi_data["wuxing_analysis"]

    # 1. 日主本質
    day_master_profile = DAY_MASTER_ESSENCE.get(day_master, DAY_MASTER_ESSENCE["甲"])

    # 2. 身強身弱的影響
    strength_influence = _interpret_strength_personality(strength, day_master)

    # 3. 十神性格特質
    ten_gods_personality = _interpret_ten_gods_personality(ten_gods)

    # 4. 五行心理學
    elemental_psychology = _interpret_elemental_psychology(wuxing, day_master)

    # 5. 人際風格
    interpersonal_style = _interpret_interpersonal_style(ten_gods, strength)

    # 6. 決策模式
    decision_pattern = _interpret_decision_pattern(ten_gods, wuxing)

    return {
        "core_personality": {
            "day_master_essence": day_master_profile["essence"],
            "strengths": day_master_profile["strengths"],
            "challenges": day_master_profile["challenges"],
            "growth_path": day_master_profile["growth_path"],
            "strength_influence": strength_influence,
            "ten_gods_personality": ten_gods_personality,
            "elemental_psychology": elemental_psychology
        },
        "interpersonal_style": interpersonal_style,
        "decision_making_pattern": decision_pattern,
        "summary": _generate_personality_summary(day_master_profile, strength, ten_gods)
    }


def _interpret_strength_personality(strength: Dict, day_master: str) -> str:
    """詮釋身強弱對性格的影響"""
    level = strength["level"]
    score = strength["score"]

    if level == "身強":
        return f"""您的八字顯示身強（強度指數：{score}），這意味著您的日主力量充足，
擁有較強的自我意識與獨立能力。您不太依賴他人，喜歡按照自己的想法行事。
這種特質讓您在面對挑戰時更有韌性，但也可能讓您顯得較為自我，
不夠靈活。建議您多聽取他人意見，培養團隊合作精神。"""

    elif level == "身弱":
        return f"""您的八字顯示身弱（強度指數：{score}），這意味著您的日主力量相對不足，
可能較為敏感細膩，善於觀察他人需求。您比較能夠接納不同意見，
具有較強的適應力。但有時可能缺乏主見，容易受他人影響。
建議您培養內在力量，建立自己的核心信念，不要過度迎合他人。"""

    else:  # 身中和
        return f"""您的八字顯示身中和（強度指數：{score}），這是非常理想的平衡狀態。
您既有自己的主見，又能聽取他人意見；既能獨立自主，也懂得尋求協助。
這種平衡讓您在人際關係與個人發展上都能取得較好的成果。
繼續保持這種平衡，是您的優勢所在。"""


def _interpret_ten_gods_personality(ten_gods: Dict) -> str:
    """詮釋十神對性格的影響"""
    distribution = ten_gods["distribution"]
    dominant = ten_gods["dominant"]

    # 找出主要的十神
    main_gods = []
    for god_name, count in distribution.items():
        if count > 0:
            main_gods.append((god_name, count))

    main_gods.sort(key=lambda x: x[1], reverse=True)

    interpretation = "您的命局十神配置顯示：\n\n"

    # 詮釋前3個主要十神
    for i, (god_name, count) in enumerate(main_gods[:3]):
        if god_name in TEN_GODS_PERSONALITY:
            god_profile = TEN_GODS_PERSONALITY[god_name]
            interpretation += f"**{god_name}（{count}個）**：\n"
            interpretation += f"- 特質：{god_profile['traits']}\n"
            interpretation += f"- 優勢：{god_profile['positive']}\n"
            interpretation += f"- 挑戰：{god_profile['negative']}\n"
            interpretation += f"- 建議：{god_profile['advice']}\n\n"

    # 特殊組合詮釋
    if distribution.get(TenGods.SHI_SHEN.value, 0) > 0 and distribution.get(TenGods.ZHENG_YIN.value, 0) > 0:
        interpretation += """**特殊組合：食神佩印**
這是非常珍貴的組合！食神代表創造力與表達，正印代表專業與學習。
兩者結合，表示您既有創意又有深度，最適合從事需要專業知識的創意工作，
如技術研發、專業諮詢、教育創新等領域。您能將理論知識轉化為實際應用，
這是您最大的競爭優勢。\n\n"""

    if distribution.get(TenGods.ZHENG_GUAN.value, 0) > 0 and distribution.get(TenGods.ZHENG_YIN.value, 0) > 0:
        interpretation += """**特殊組合：官印相生**
這是吉利的組合！正官代表權威與責任，正印代表學習與智慧。
官印相生表示您能通過學習提升地位，也能以德服人。
您適合在需要專業知識與管理能力的領域發展，如教育管理、專業經理人等。
貴人運不錯，長輩或上司會欣賞您。\n\n"""

    return interpretation.strip()


def _interpret_elemental_psychology(wuxing: Dict, day_master: str) -> str:
    """五行心理學詮釋"""
    counts = wuxing["counts"]
    missing = wuxing["missing"]
    strong = wuxing["strong"]

    day_master_wuxing = get_wuxing_from_stem(day_master).value

    interpretation = f"您的五行配置對性格的影響：\n\n"

    # 詮釋旺盛的五行
    if strong:
        interpretation += "**旺盛的五行**：\n"
        for wx in strong:
            interpretation += _wuxing_psychology_strong(wx)

    # 詮釋缺失的五行（最重要）
    if missing:
        interpretation += "\n**缺失的五行（關鍵）**：\n"
        for wx in missing:
            interpretation += _wuxing_psychology_missing(wx)

    # 日主五行的特別提示
    interpretation += f"\n**日主五行（{day_master_wuxing}）的特別提示**：\n"
    interpretation += _wuxing_psychology_day_master(day_master_wuxing, counts[day_master_wuxing])

    return interpretation


def _wuxing_psychology_strong(wuxing: str) -> str:
    """旺盛五行的心理特徵"""
    profiles = {
        "木": "- 木旺：仁慈有愛心，富有同情心，但可能過於理想化，容易受傷\n",
        "火": "- 火旺：熱情積極，行動力強，但可能較為急躁，情緒起伏大\n",
        "土": "- 土旺：穩重可靠，做事踏實，但可能過於保守，缺乏創新\n",
        "金": "- 金旺：果斷剛毅，原則性強，但可能過於剛硬，不夠圓融\n",
        "水": "- 水旺：聰明靈活，適應力強，但可能過於善變，缺乏持久力\n"
    }
    return profiles.get(wuxing, "")


def _wuxing_psychology_missing(wuxing: str) -> str:
    """缺失五行的心理影響與建議"""
    profiles = {
        "木": """- 缺木：可能缺乏仁愛之心，較為現實理性。建議多接觸大自然，
  培養同理心，學習關懷他人。可多穿綠色衣物，從事與木相關的活動（閱讀、園藝）。\n""",

        "火": """- 缺火：可能缺乏熱情與活力，較為內向被動。建議多參與社交活動，
  培養積極主動的態度。可多穿紅色衣物，多曬太陽，從事需要表達的活動。\n""",

        "土": """- 缺土：可能缺乏安全感，較為不安定。建議培養務實態度，
  建立穩定的生活習慣。可多穿黃色衣物，多接觸土地（運動、爬山）。\n""",

        "金": """- 缺金：可能缺乏果斷力，較為優柔寡斷。建議培養決斷力，
  學習堅持原則。可多穿白色衣物，從事需要決策的活動。\n""",

        "水": """- 缺水：可能缺乏智慧與策略思維，較為衝動。建議多思考，培養冷靜，
  在行動前給自己思考時間。可多穿黑色或藍色衣物，多喝水，
  從事需要思考的活動（閱讀、下棋、冥想）。這是您最需要補足的部分！\n"""
    }
    return profiles.get(wuxing, "")


def _wuxing_psychology_day_master(wuxing: str, count: int) -> str:
    """日主五行的心理特徵"""
    if count >= 4:
        return f"{wuxing}元素在您命中很旺，{wuxing}的特質會非常明顯。請特別注意{wuxing}過旺的負面影響。"
    elif count <= 2:
        return f"{wuxing}元素在您命中偏弱，您可能需要更多{wuxing}的能量來支持自己。"
    else:
        return f"{wuxing}元素在您命中適中，這是理想的狀態。"


def _interpret_interpersonal_style(ten_gods: Dict, strength: Dict) -> str:
    """人際風格詮釋"""
    distribution = ten_gods["distribution"]

    bijian_count = distribution.get(TenGods.BI_JIAN.value, 0) + distribution.get(TenGods.JIE_CAI.value, 0)
    yinxing_count = distribution.get(TenGods.ZHENG_YIN.value, 0) + distribution.get(TenGods.PIAN_YIN.value, 0)
    guansha_count = distribution.get(TenGods.ZHENG_GUAN.value, 0) + distribution.get(TenGods.QI_SHA.value, 0)

    interpretation = ""

    if bijian_count == 0:
        interpretation += """在人際關係方面，您的比劫較少，代表您不太依賴同輩朋友，
更傾向獨立作業或與不同年齡層的人交往。您可能不太需要從朋友處獲得認同，
而是更注重自己的判斷。這讓您較為獨立，但也可能在需要團隊合作時感到挑戰。
建議您有意識地培養與同輩的友誼，學習團隊合作的技巧。"""

    elif bijian_count >= 2:
        interpretation += """您的比劫較多，代表您重視同輩友誼，喜歡與朋友一起行動。
您可能有較強的團隊意識，但也可能在財務或感情上與朋友有競爭或糾葛。
建議您在與朋友的互動中，注意界限的設定，特別是涉及金錢時要更加謹慎。"""

    if yinxing_count > 0:
        interpretation += """\n\n您命中有印星，表示您重視長輩或權威人士的意見，
也容易獲得他們的幫助。您在職場上會有貴人相助，特別是年長或資深的同事。
善用這個優勢，多向前輩請益，他們會是您成長的重要助力。"""

    if guansha_count > 0:
        interpretation += """\n\n您命中有官殺星，表示您對權威既有尊重也有警惕。
您能夠在服從與獨立之間取得平衡，既能遵守規則，也能保持自己的立場。
這讓您適合在有明確規範的組織中工作。"""

    return interpretation.strip()


def _interpret_decision_pattern(ten_gods: Dict, wuxing: Dict) -> str:
    """決策模式詮釋"""
    distribution = ten_gods["distribution"]
    missing = wuxing["missing"]

    shishang_count = distribution.get(TenGods.SHI_SHEN.value, 0) + distribution.get(TenGods.SHANG_GUAN.value, 0)
    yinxing_count = distribution.get(TenGods.ZHENG_YIN.value, 0) + distribution.get(TenGods.PIAN_YIN.value, 0)

    interpretation = "您的決策模式特徵：\n\n"

    if shishang_count > 0 and yinxing_count > 0:
        interpretation += """食傷與印星並存：您的決策過程可能充滿內在對話。
食傷讓您重視創新與個人想法，而印星則讓您考慮規範與他人意見。
這可能導致內在衝突——一方面想要創新突破，一方面又擔心不符合規範。

**建議決策流程**：
1. 先讓創意自由發揮（食傷）
2. 給自己時間做充分研究（印星）
3. 整合兩者後大膽實施

這樣既能發揮創新優勢，又能做好充分準備。"""

    elif shishang_count > yinxing_count:
        interpretation += """食傷較旺：您的決策較為快速直覺，重視個人想法與創新。
您可能不太喜歡繁文縟節，希望快速行動。這是優勢，但也要注意：

**建議**：
- 重大決策前給自己48小時冷靜期
- 諮詢專業人士意見（補充印星能量）
- 做好風險評估，不要過度樂觀"""

    elif yinxing_count > shishang_count:
        interpretation += """印星較旺：您的決策較為謹慎，重視規範與專業意見。
您可能會花較多時間研究，希望做出最穩妥的決定。這是優勢，但也要注意：

**建議**：
- 避免分析癱瘓，設定決策時限
- 相信自己的直覺（培養食傷能量）
- 有時候完成比完美更重要"""

    # 缺水的特別提示
    if "水" in missing:
        interpretation += """\n\n**特別提示（缺水）**：
缺水可能影響您的策略思維與大局觀。您可能較為衝動，缺乏深思熟慮。

**補救方法**：
- 重大決策前，寫下所有優缺點（強迫思考）
- 找智慧型的導師或顧問請益
- 學習系統思考、商業策略等課程
- 培養冥想或靜坐的習慣，訓練冷靜思考"""

    return interpretation.strip()


def _generate_personality_summary(day_master_profile: Dict, strength: Dict, ten_gods: Dict) -> str:
    """生成性格總結"""
    summary = f"""
綜合您的八字配置，您是一個{day_master_profile['strengths'][0]}、
{day_master_profile['strengths'][1]}的人。您的核心優勢在於{day_master_profile['strengths'][0]}，
但也需要注意{day_master_profile['challenges'][0]}的傾向。

在人生發展中，{day_master_profile['growth_path']}將是您最重要的成長方向。

您的身強弱狀態為{strength['level']}，這影響了您的自我意識與獨立程度。
十神配置中，{ten_gods['dominant'][0] if ten_gods['dominant'] else '比劫'}的特質較為明顯，
這形塑了您獨特的性格與行為模式。

記住：了解自己的天性是成長的第一步，但不要被命盤限制。
您永遠有選擇與成長的空間。
"""
    return summary.strip()


# ============================================
# 導出函數
# ============================================

def interpret_bazi_personality(bazi_data: Dict) -> Dict:
    """
    八字性格深度詮釋（主要入口函數）

    Args:
        bazi_data: 來自 BaziCalculator.analyze() 的完整分析結果

    Returns:
        包含詳細性格分析的字典
    """
    return interpret_personality(bazi_data)


def interpret_career(bazi_data: Dict) -> Dict:
    """
    事業深度詮釋

    Returns:
        詳細的事業分析，包含能力評估、行業推薦、時間軸規劃等
    """
    ten_gods = bazi_data["ten_gods_analysis"]
    strength = bazi_data["strength"]
    wuxing = bazi_data["wuxing_analysis"]
    yongshen = bazi_data["yongshen"]
    luck_pillars = bazi_data.get("luck_pillars", [])

    distribution = ten_gods["distribution"]

    # 計算事業評分
    career_rating = _calculate_career_rating(distribution, strength)

    # 天賦才能評估
    aptitude = _analyze_career_aptitude(ten_gods, strength, wuxing)

    # 行業推薦
    industries = _recommend_industries(ten_gods, wuxing, yongshen)

    # 事業發展時間軸
    timeline = _analyze_career_timeline(luck_pillars, yongshen)

    # 具體建議
    recommendations = _generate_career_recommendations(ten_gods, wuxing, strength, timeline)

    return {
        "overall_rating": career_rating,
        "aptitude_assessment": aptitude,
        "industry_recommendations": industries,
        "career_development_timeline": timeline,
        "specific_recommendations": recommendations,
        "summary": _generate_career_summary(career_rating, aptitude, industries)
    }


def _calculate_career_rating(distribution: Dict, strength: Dict) -> float:
    """計算事業評分 (0-10)"""
    score = 5.0

    # 官星加分
    if distribution.get(TenGods.ZHENG_GUAN.value, 0) > 0:
        score += 2.0
    if distribution.get(TenGods.QI_SHA.value, 0) > 0:
        score += 1.5

    # 印星加分（學習與專業）
    if distribution.get(TenGods.ZHENG_YIN.value, 0) > 0:
        score += 1.5
    if distribution.get(TenGods.PIAN_YIN.value, 0) > 0:
        score += 1.0

    # 食傷加分（創造與表達）
    if distribution.get(TenGods.SHI_SHEN.value, 0) > 0:
        score += 1.0
    if distribution.get(TenGods.SHANG_GUAN.value, 0) > 0:
        score += 0.8

    # 身強加分
    if strength["level"] == "身強":
        score += 1.0
    elif strength["level"] == "身弱":
        score -= 0.5

    return min(round(score, 1), 10.0)


def _analyze_career_aptitude(ten_gods: Dict, strength: Dict, wuxing: Dict) -> Dict:
    """分析事業天賦"""
    distribution = ten_gods["distribution"]

    talents = []

    # 食神+印星 = 專業創新
    if distribution.get(TenGods.SHI_SHEN.value, 0) > 0 and distribution.get(TenGods.ZHENG_YIN.value, 0) > 0:
        talents.append({
            "talent": "專業技術能力",
            "source": "食神+印星組合",
            "manifestation": "能將專業知識轉化為創新應用",
            "best_applications": ["技術研發", "專業顧問", "教育培訓"],
            "strength": "極強"
        })

    # 官星得位 = 管理領導
    if distribution.get(TenGods.ZHENG_GUAN.value, 0) > 0:
        talents.append({
            "talent": "領導與管理",
            "source": "正官星",
            "manifestation": "具備管理權威，適合管理職位",
            "best_applications": ["企業管理", "行政管理", "專案管理"],
            "strength": "強"
        })

    # 食傷旺 = 創意表達
    if distribution.get(TenGods.SHANG_GUAN.value, 0) + distribution.get(TenGods.SHI_SHEN.value, 0) >= 2:
        talents.append({
            "talent": "創意與表達",
            "source": "食傷旺",
            "manifestation": "創造力強，善於溝通表達",
            "best_applications": ["創意設計", "媒體傳播", "藝術創作"],
            "strength": "強"
        })

    # 財星旺 = 商業頭腦
    if distribution.get(TenGods.ZHENG_CAI.value, 0) + distribution.get(TenGods.PIAN_CAI.value, 0) >= 2:
        talents.append({
            "talent": "商業與財務",
            "source": "財星旺",
            "manifestation": "財務敏感度高，商業嗅覺佳",
            "best_applications": ["商業經營", "財務管理", "投資理財"],
            "strength": "強"
        })

    # 工作風格
    working_style = _describe_working_style(ten_gods, strength)

    return {
        "natural_talents": talents,
        "working_style": working_style
    }


def _describe_working_style(ten_gods: Dict, strength: Dict) -> str:
    """描述工作風格"""
    distribution = ten_gods["distribution"]

    style = "您最適合的工作環境特徵：\n\n"

    if distribution.get(TenGods.ZHENG_YIN.value, 0) > 0:
        style += "- 需要持續學習與專業成長（印星需求）\n"
        style += "- 有清晰的職涯發展路徑\n"

    if distribution.get(TenGods.SHI_SHEN.value, 0) > 0 or distribution.get(TenGods.SHANG_GUAN.value, 0) > 0:
        style += "- 允許創新與表達（食傷需求）\n"
        style += "- 不過度束縛自由\n"

    if distribution.get(TenGods.ZHENG_GUAN.value, 0) > 0:
        style += "- 有明確的規範與制度（官星需求）\n"
        style += "- 重視專業表現與成就\n"

    if strength["level"] == "身弱":
        style += "\n**注意**：由於身弱，建議選擇團隊支持較好的環境，避免單打獨鬥。"

    return style


def _recommend_industries(ten_gods: Dict, wuxing: Dict, yongshen: Dict) -> Dict:
    """推薦適合的行業"""
    distribution = ten_gods["distribution"]

    highly_suitable = []
    moderately_suitable = []
    not_recommended = []

    # 科技研發（食神+印星）
    if distribution.get(TenGods.SHI_SHEN.value, 0) > 0 and distribution.get(TenGods.ZHENG_YIN.value, 0) > 0:
        highly_suitable.append({
            "industry": "科技研發",
            "reason": "食神+印星的專業創新組合",
            "specific_roles": ["軟體工程師", "技術專家", "產品設計師"],
            "success_probability": "85%"
        })

    # 教育培訓（印星旺）
    if distribution.get(TenGods.ZHENG_YIN.value, 0) > 0:
        highly_suitable.append({
            "industry": "教育培訓",
            "reason": "印星旺，善於傳授知識",
            "specific_roles": ["專業講師", "企業培訓師", "教育顧問"],
            "success_probability": "80%"
        })

    # 創意設計（食傷旺）
    if distribution.get(TenGods.SHANG_GUAN.value, 0) + distribution.get(TenGods.SHI_SHEN.value, 0) >= 2:
        highly_suitable.append({
            "industry": "創意設計",
            "reason": "食傷的創造表達能力",
            "specific_roles": ["UX設計師", "創意總監", "品牌策劃"],
            "success_probability": "75%"
        })

    # 管理諮詢（官印相生）
    if distribution.get(TenGods.ZHENG_GUAN.value, 0) > 0 and distribution.get(TenGods.ZHENG_YIN.value, 0) > 0:
        highly_suitable.append({
            "industry": "管理諮詢",
            "reason": "官印相生，管理與專業兼備",
            "specific_roles": ["管理顧問", "策略顧問", "專案經理"],
            "success_probability": "80%"
        })

    # 純銷售（比劫弱則不適合）
    bijian_count = distribution.get(TenGods.BI_JIAN.value, 0) + distribution.get(TenGods.JIE_CAI.value, 0)
    if bijian_count == 0:
        not_recommended.append({
            "industry": "純銷售業務",
            "reason": "比劫弱，不利競爭型工作",
            "alternative": "可考慮技術銷售或顧問式銷售"
        })

    return {
        "highly_suitable": highly_suitable,
        "moderately_suitable": moderately_suitable,
        "not_recommended": not_recommended
    }


def _analyze_career_timeline(luck_pillars: List[Dict], yongshen: Dict) -> Dict:
    """分析事業發展時間軸"""
    if not luck_pillars:
        return {}

    timeline = {}

    # 簡化版：根據大運分析
    for pillar in luck_pillars[:5]:  # 分析前5步大運（50年）
        age_range = pillar["age_range"]
        stem = pillar["stem"]
        branch = pillar["branch"]

        # 判斷這步大運的特性（簡化版）
        phase_desc = _describe_luck_period(stem, branch, yongshen)

        timeline[age_range] = phase_desc

    return timeline


def _describe_luck_period(stem: str, branch: str, yongshen: Dict) -> Dict:
    """描述某步大運的事業運勢"""
    # 這是簡化版，實際需要更複雜的判斷邏輯
    return {
        "phase": "發展期",
        "opportunities": "事業機會增加",
        "challenges": "需要把握時機",
        "key_actions": ["積極爭取", "展現專業", "建立人脈"]
    }


def _generate_career_recommendations(ten_gods: Dict, wuxing: Dict, strength: Dict, timeline: Dict) -> List[Dict]:
    """生成具體事業建議"""
    recommendations = []

    distribution = ten_gods["distribution"]
    missing = wuxing["missing"]

    # 建議1：根據印星給建議
    if distribution.get(TenGods.ZHENG_YIN.value, 0) > 0:
        recommendations.append({
            "recommendation": "在30歲前專注技術深度而非管理職",
            "reasoning": "印星運期適合累積專業資本",
            "action_steps": [
                "選擇有技術深度的公司或專案",
                "投資自我學習（課程、認證、進修）",
                "建立個人專業品牌（寫作、演講）"
            ],
            "priority": "高"
        })

    # 建議2：根據官星給建議
    if distribution.get(TenGods.ZHENG_GUAN.value, 0) > 0:
        recommendations.append({
            "recommendation": "35-40歲把握升遷或創業機會",
            "reasoning": "官星運轉的黃金窗口",
            "action_steps": [
                "提前布局：33-34歲開始準備",
                "主動爭取更大責任與專案",
                "若創業，這是較佳時機"
            ],
            "priority": "高"
        })

    # 建議3：根據缺水給建議
    if "水" in missing:
        recommendations.append({
            "recommendation": "培養策略思維能力（補水）",
            "reasoning": "缺水可能導致缺乏大局觀",
            "action_steps": [
                "學習商業策略、系統思考",
                "多閱讀、多思考、少衝動",
                "找有智慧的導師請益"
            ],
            "priority": "中"
        })

    return recommendations


def _generate_career_summary(rating: float, aptitude: Dict, industries: Dict) -> str:
    """生成事業分析總結"""
    talents = aptitude.get("natural_talents", [])
    talent_desc = talents[0]["talent"] if talents else "專業能力"

    summary = f"""
您的事業運勢評分為 {rating}/10，屬於{"極佳" if rating >= 8 else "良好" if rating >= 6.5 else "中等"}水平。

您的核心優勢是{talent_desc}，這將是您職涯發展的最大資本。
建議您專注在此領域深耕，不要輕易轉換跑道。

從行業選擇來看，您最適合從事需要專業知識與持續學習的領域，
避免純粹重複性或過度競爭的工作環境。

成功關鍵：在30歲前累積專業深度，35-40歲把握機會突破，
40歲後轉向領導或傳承角色。
"""
    return summary.strip()


def interpret_wealth(bazi_data: Dict) -> Dict:
    """
    財富深度詮釋
    """
    ten_gods = bazi_data["ten_gods_analysis"]
    wuxing = bazi_data["wuxing_analysis"]
    strength = bazi_data["strength"]

    distribution = ten_gods["distribution"]

    # 財富評分
    wealth_rating = _calculate_wealth_rating(distribution, strength)

    # 財富能力分析
    wealth_capacity = _analyze_wealth_capacity(ten_gods, strength, wuxing)

    # 財富時間軸
    wealth_timeline = _analyze_wealth_timeline()

    # 財富來源
    wealth_sources = _analyze_wealth_sources(ten_gods)

    # 具體建議
    wealth_recommendations = _generate_wealth_recommendations(ten_gods, wuxing)

    return {
        "overall_rating": wealth_rating,
        "wealth_capacity": wealth_capacity,
        "wealth_timeline": wealth_timeline,
        "wealth_sources": wealth_sources,
        "specific_recommendations": wealth_recommendations
    }


def _calculate_wealth_rating(distribution: Dict, strength: Dict) -> float:
    """計算財富評分"""
    score = 5.0

    if distribution.get(TenGods.ZHENG_CAI.value, 0) > 0:
        score += 2.0
    if distribution.get(TenGods.PIAN_CAI.value, 0) > 0:
        score += 1.5
    if distribution.get(TenGods.SHI_SHEN.value, 0) > 0:
        score += 1.0  # 食神生財

    if strength["level"] == "身強":
        score += 1.0  # 身強能擔財
    elif strength["level"] == "身弱":
        score -= 1.0  # 身弱財多身弱

    return min(round(score, 1), 10.0)


def _analyze_wealth_capacity(ten_gods: Dict, strength: Dict, wuxing: Dict) -> Dict:
    """分析財富能力"""
    distribution = ten_gods["distribution"]

    earning_potential = ""
    money_management = ""

    # 食神生財格局
    if distribution.get(TenGods.SHI_SHEN.value, 0) > 0:
        earning_potential = """您的財星配置顯示「食神生財」格局，表示您的財富
主要來自專業價值而非純商業操作。您通過展現專業能力、提供有價值的服務來獲得財富，
而非投機或純粹的商業買賣。這種財富模式較為穩定，但需要時間累積。"""

    # 理財風格
    if distribution.get(TenGods.ZHENG_CAI.value, 0) > 0:
        money_management = """您對金錢有基本規劃，理財較為穩健，
不會過度冒險也不會過度守財。建議建立自動化儲蓄機制，
投資在自我成長的錢不要省（這是您最好的投資）。"""

    return {
        "earning_potential": earning_potential,
        "money_management_style": money_management
    }


def _analyze_wealth_timeline() -> Dict:
    """財富時間軸分析"""
    return {
        "25-35歲": {
            "phase": "財富累積期",
            "expected_level": "中低收入但穩定成長",
            "strategy": "重點不在賺大錢，而在累積專業價值",
            "key_actions": ["投資技能與知識", "建立第一桶金", "避免高風險投資"]
        },
        "35-45歲": {
            "phase": "財富快速增長期",
            "expected_level": "收入顯著提升",
            "strategy": "專業價值變現的黃金期",
            "key_actions": ["提高專業服務定價", "建立被動收入", "適度增加投資"]
        },
        "45歲以上": {
            "phase": "財富穩定期",
            "expected_level": "收入穩定，重點在保值",
            "strategy": "智慧變現，降低風險",
            "key_actions": ["轉向顧問或教育", "降低投資風險", "考慮財富傳承"]
        }
    }


def _analyze_wealth_sources(ten_gods: Dict) -> Dict:
    """分析財富來源"""
    distribution = ten_gods["distribution"]

    sources = {
        "primary_source": {
            "source": "專業服務收入",
            "percentage": "70-80%",
            "description": "通過提供專業技術或知識服務獲得的收入"
        }
    }

    if distribution.get(TenGods.SHI_SHEN.value, 0) > 0:
        sources["secondary_source"] = {
            "source": "知識產權收入",
            "percentage": "10-20%",
            "description": "課程、書籍、專利等形式的被動收入"
        }

    return sources


def _generate_wealth_recommendations(ten_gods: Dict, wuxing: Dict) -> List[Dict]:
    """生成財富建議"""
    recommendations = []

    distribution = ten_gods["distribution"]

    if distribution.get(TenGods.SHI_SHEN.value, 0) > 0:
        recommendations.append({
            "recommendation": "建立「專業品牌」而非「打工心態」",
            "reasoning": "食神生財格局最適合個人品牌變現",
            "action_steps": [
                "在專業領域建立個人影響力",
                "通過寫作、演講建立專家形象",
                "35歲後將品牌轉化為收入"
            ]
        })

    recommendations.append({
        "recommendation": "40歲前至少建立一種被動收入",
        "reasoning": "為後續的財務自由打基礎",
        "suggestions": ["線上課程", "技術諮詢服務", "專業工具或產品"]
    })

    bijian_count = distribution.get(TenGods.BI_JIAN.value, 0) + distribution.get(TenGods.JIE_CAI.value, 0)
    if bijian_count == 0:
        recommendations.append({
            "recommendation": "避免與朋友合夥創業",
            "reasoning": "比劫弱，合夥容易破財",
            "alternative": "可以投資朋友企業，但不要共同經營"
        })

    return recommendations


def interpret_relationship(bazi_data: Dict, gender: str = "女") -> Dict:
    """
    感情婚姻深度詮釋
    """
    ten_gods = bazi_data["ten_gods_analysis"]
    basic_chart = bazi_data["basic_chart"]

    # 配偶特質
    spouse_characteristics = _analyze_spouse_characteristics(basic_chart, ten_gods, gender)

    # 感情時間軸
    relationship_timeline = _analyze_relationship_timeline(gender)

    # 感情挑戰
    relationship_challenges = _analyze_relationship_challenges(ten_gods)

    # 具體建議
    relationship_recommendations = _generate_relationship_recommendations(ten_gods)

    return {
        "overall_rating": 7.5,
        "spouse_characteristics": spouse_characteristics,
        "relationship_timeline": relationship_timeline,
        "relationship_challenges": relationship_challenges,
        "specific_recommendations": relationship_recommendations
    }


def _analyze_spouse_characteristics(basic_chart: Dict, ten_gods: Dict, gender: str) -> Dict:
    """分析配偶特質"""
    day_branch = basic_chart["day"]["branch"]

    # 根據日支分析配偶宮
    spouse_profile = f"""
**配偶宮分析（日支：{day_branch}）**：
配偶性格較為{_get_branch_personality(day_branch)}，
在婚姻中會展現出相應的特質。
"""

    # 根據性別看官財星
    ideal_partner = ""
    if gender == "女":
        # 女命看官星
        ideal_partner = """最適合的伴侶類型是「理性務實但有事業心」的人，
對方可能從事管理、技術或專業領域工作。"""
    else:
        # 男命看財星
        ideal_partner = """最適合的伴侶類型是「溫柔賢淑但有主見」的人，
對方能照顧家庭但也有自己的事業或興趣。"""

    return {
        "ideal_partner_profile": spouse_profile + "\n" + ideal_partner,
        "compatibility_factors": {
            "positive": ["彼此尊重", "理性溝通"],
            "challenges": ["可能過於忙碌", "需要刻意營造浪漫"]
        }
    }


def _get_branch_personality(branch: str) -> str:
    """根據地支判斷性格特徵（簡化版）"""
    personalities = {
        "子": "聰明機智", "丑": "穩重踏實", "寅": "積極進取",
        "卯": "溫和友善", "辰": "成熟穩重", "巳": "聰明細膩",
        "午": "熱情開朗", "未": "溫柔體貼", "申": "靈活聰穎",
        "酉": "注重細節", "戌": "忠誠可靠", "亥": "純真善良"
    }
    return personalities.get(branch, "獨特有個性")


def _analyze_relationship_timeline(gender: str) -> Dict:
    """感情時間軸分析"""
    return {
        "25-30歲": {
            "phase": "戀愛探索期",
            "relationship_luck": "中等",
            "recommendations": ["不要因太忙而忽略感情", "參加社交活動擴大交友圈"]
        },
        "31-35歲": {
            "phase": "結婚適齡期",
            "relationship_luck": "較強",
            "critical_years": [32, 34],
            "recommendations": ["如有穩定對象，是結婚良機", "未有對象要主動一些"]
        },
        "婚後經營": {
            "marriage_pattern": "理性穩定型",
            "long_term_success_keys": ["定期約會", "學習表達情感", "共同培養興趣"]
        }
    }


def _analyze_relationship_challenges(ten_gods: Dict) -> List[Dict]:
    """分析感情挑戰"""
    challenges = []

    distribution = ten_gods["distribution"]

    if distribution.get(TenGods.ZHENG_GUAN.value, 0) > 0:
        challenges.append({
            "challenge": "過度理性，缺乏浪漫",
            "source": "官星影響，偏重理性",
            "solution": "刻意學習表達愛意，創造浪漫時刻",
            "practices": ["定期送小禮物", "記住重要日子", "學習對方的愛的語言"]
        })

    if distribution.get(TenGods.SHI_SHEN.value, 0) + distribution.get(TenGods.SHANG_GUAN.value, 0) >= 2:
        challenges.append({
            "challenge": "事業心太重，忽略家庭",
            "source": "食傷旺，專注事業",
            "solution": "建立工作與生活的界限",
            "practices": ["設定家庭時間", "培養共同興趣", "定期休假"]
        })

    return challenges


def _generate_relationship_recommendations(ten_gods: Dict) -> List[Dict]:
    """生成感情建議"""
    return [
        {
            "recommendation": "選擇事業心強但也重視家庭的伴侶",
            "reasoning": "需要對方理解您的事業投入，但也能提醒您回歸家庭",
            "warning": "避免選擇完全沒有事業心的伴侶，會有價值觀衝突"
        },
        {
            "recommendation": "婚前深入了解對方的家庭觀念",
            "reasoning": "可能因事業忙碌而忽略家庭，需要對方能理解並協調",
            "key_questions": ["對雙薪家庭的看法", "對家事分工的期待", "對育兒的參與度"]
        }
    ]


def interpret_health(bazi_data: Dict) -> Dict:
    """
    健康深度詮釋
    """
    wuxing = bazi_data["wuxing_analysis"]
    basic_chart = bazi_data["basic_chart"]

    # 五行健康對應
    elemental_health = _analyze_elemental_health(wuxing)

    # 年齡段健康指引
    age_based_guidance = _analyze_age_based_health()

    # 生活方式建議
    lifestyle_recommendations = _generate_lifestyle_recommendations(wuxing)

    # 具體建議
    health_recommendations = _generate_health_recommendations(wuxing)

    return {
        "overall_rating": wuxing["balance_score"] * 10,
        "elemental_health_mapping": elemental_health,
        "age_based_health_guidance": age_based_guidance,
        "lifestyle_recommendations": lifestyle_recommendations,
        "specific_recommendations": health_recommendations
    }


def _analyze_elemental_health(wuxing: Dict) -> Dict:
    """五行健康對應分析"""
    counts = wuxing["counts"]
    missing = wuxing["missing"]
    strong = wuxing["strong"]

    health_mapping = {}

    # 五行對應的臟腑
    wuxing_organs = {
        "木": {"organs": ["肝", "膽", "眼睛", "筋腱"], "element": "木"},
        "火": {"organs": ["心臟", "小腸", "血液循環"], "element": "火"},
        "土": {"organs": ["脾", "胃", "消化系統"], "element": "土"},
        "金": {"organs": ["肺", "大腸", "皮膚", "呼吸系統"], "element": "金"},
        "水": {"organs": ["腎", "膀胱", "泌尿系統", "生殖系統"], "element": "水"}
    }

    for wx, info in wuxing_organs.items():
        count = counts.get(wx, 0)

        if wx in missing:
            status = "缺失（關鍵問題）"
            implications = f"{wx}缺失，{info['organs'][0]}系統需要特別保養"
        elif wx in strong:
            status = "過旺"
            implications = f"{wx}過旺，可能對{info['organs'][0]}系統造成壓力"
        else:
            status = "適中"
            implications = f"{wx}適中，{info['organs'][0]}系統基本健康"

        health_mapping[wx] = {
            "organs": info["organs"],
            "status": status,
            "implications": implications,
            "preventive_care": _get_preventive_care(wx, status)
        }

    return health_mapping


def _get_preventive_care(wuxing: str, status: str) -> List[str]:
    """獲取預防保健建議"""
    if status == "缺失（關鍵問題）":
        care_map = {
            "水": [
                "充分補水（每日至少2000ml）",
                "避免過度勞累，保護腎臟",
                "定期檢查腎功能",
                "多吃黑色食物（黑豆、黑芝麻）"
            ],
            "木": ["避免熬夜", "控制情緒", "多做伸展運動"],
            "火": ["避免過度刺激", "保持運動", "學習放鬆技巧"],
            "土": ["規律飲食", "避免暴飲暴食", "壓力管理"],
            "金": ["保持空氣清新", "皮膚保濕", "補充益生菌"]
        }
        return care_map.get(wuxing, [])
    elif status == "過旺":
        return ["避免過度", "保持平衡", "適度調節"]
    else:
        return ["保持現狀", "定期檢查"]


def _analyze_age_based_health() -> Dict:
    """年齡段健康指引"""
    return {
        "25-35歲": {
            "overall_condition": "身體狀況良好，但開始累積問題",
            "key_risks": ["過度勞累", "不規律作息", "久坐"],
            "preventive_priorities": [
                "建立良好作息",
                "開始規律運動",
                "定期健康檢查",
                "充分補水"
            ]
        },
        "35-45歲": {
            "overall_condition": "進入健康關鍵期",
            "key_risks": ["心血管問題", "代謝症候群", "筋骨問題"],
            "preventive_priorities": [
                "心血管檢查",
                "控制體重",
                "腎功能檢查",
                "壓力管理"
            ]
        },
        "45歲以上": {
            "overall_condition": "維護為主，避免惡化",
            "focus": "生活質量重於壽命長度",
            "priorities": ["慢性病控制", "維持活動能力", "心理健康"]
        }
    }


def _generate_lifestyle_recommendations(wuxing: Dict) -> Dict:
    """生成生活方式建議"""
    missing = wuxing["missing"]

    recommendations = {
        "diet": {
            "principles": ["均衡飲食", "少油少鹽", "多蔬果"],
            "avoid": ["過度辛辣", "過度油膩", "酒精"]
        },
        "exercise": {
            "recommended": ["游泳", "瑜伽", "太極", "散步"],
            "avoid": ["過度激烈運動", "長時間久坐"],
            "frequency": "每週3-5次，每次30-60分鐘"
        },
        "sleep": {
            "importance": "睡眠對健康至關重要",
            "recommendations": [
                "每晚至少7-8小時",
                "晚上11點前入睡",
                "營造良好睡眠環境"
            ]
        }
    }

    # 根據缺失五行調整
    if "水" in missing:
        recommendations["diet"]["principles"].insert(0, "多補水（每日2000ml以上）")
        recommendations["exercise"]["recommended"].insert(0, "游泳（補水最佳運動）")

    return recommendations


def _generate_health_recommendations(wuxing: Dict) -> List[Dict]:
    """生成健康建議"""
    recommendations = []
    missing = wuxing["missing"]

    if "水" in missing:
        recommendations.append({
            "recommendation": "補水是您健康的第一要務",
            "reasoning": "五行缺水影響腎臟、代謝系統",
            "action_steps": [
                "每天喝水至少2000ml",
                "多吃水分多的食物",
                "環境保持濕潤",
                "冬季特別注意補水"
            ],
            "priority": "極高"
        })

    recommendations.append({
        "recommendation": "培養靜態興趣，平衡生活",
        "reasoning": "現代人壓力大，需要放鬆活動",
        "suggestions": ["閱讀", "書法", "園藝", "冥想"],
        "priority": "高"
    })

    return recommendations


if __name__ == "__main__":
    print("八字深度詮釋引擎")
    print("請配合 BaziCalculator 使用")

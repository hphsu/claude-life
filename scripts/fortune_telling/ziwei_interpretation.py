#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
紫微斗數深度解釋引擎 (ZiWei DuoShu Interpretation Engine)

此模組提供紫微斗數的深度解釋功能，將基本排盤數據轉化為詳細的文字分析。

主要功能：
1. 十二宮位深度解釋（每宮 200-300 字）
2. 星曜組合解讀庫
3. 四化飛星動態分析
4. 跨宮位綜合分析
5. 人生階段運勢分析

作者：Claude Code
日期：2025
"""

from typing import Dict, List, Tuple, Optional
from .prompt_utils import (
    load_system_prompt,
    validate_analysis_length,
    calculate_confidence_level
)
from .llm_analyzer import (
    get_llm_analyzer,
    construct_ziwei_palace_prompt
)

# Load Zi Wei system prompt at module level
ZIWEI_SYSTEM_PROMPT = load_system_prompt('ziwei_system_prompt.md') or ""


# ============================================================================
# 主星特質資料庫 (Major Stars Database)
# ============================================================================

MAJOR_STAR_TRAITS = {
    '紫微': {
        'name': '紫微星',
        'category': '北斗帝星',
        'element': '土',
        'nature': '尊貴、領導、權威',
        'core_essence': """
        紫微為帝星，代表至高無上的權威與領導力。如同古代帝王，紫微星坐命的人
        天生具有統御他人的氣質與能力。您重視尊嚴與面子，有大格局的思維，
        不喜歡被人輕視或忽略。您的人生追求往往與地位、成就、被尊重有關。
        """,
        'strengths': ['領導能力強', '有責任感', '格局大', '貴人運佳', '穩重可靠'],
        'challenges': ['可能過於自我中心', '重視面子', '不夠親和', '可能固執'],
        'career': '適合管理、政府、大型企業、需要權威性的專業領域',
        'wealth': '財運穩定，適合穩健投資，晚年富足',
        'relationship': '配偶多為能幹之人，婚姻穩定但需要相互尊重'
    },

    '天機': {
        'name': '天機星',
        'category': '南斗智星',
        'element': '木',
        'nature': '智慧、變動、策劃',
        'core_essence': """
        天機為智慧之星，代表靈活的頭腦與優秀的策劃能力。您思維敏捷，反應快速，
        善於分析問題並找到解決方案。天機星帶有變動性質，您的人生可能充滿變化，
        不太適合一成不變的環境。您適合需要動腦的工作，而非純粹體力勞動。
        """,
        'strengths': ['聰明機智', '分析力強', '應變能力佳', '善於策劃', '學習能力好'],
        'challenges': ['想太多', '缺乏行動力', '多疑', '不夠穩定'],
        'career': '適合策劃、顧問、設計、研發、教育、技術等需要智慧的工作',
        'wealth': '財運變動大，適合多元投資，靠智慧賺錢',
        'relationship': '感情多變，需要心靈契合的伴侶'
    },

    '太陽': {
        'name': '太陽星',
        'category': '中天貴星',
        'element': '火',
        'nature': '光明、博愛、付出',
        'core_essence': """
        太陽為光明之星，代表溫暖、博愛與無私付出。您個性開朗熱情，樂於助人，
        有強烈的正義感。太陽星具有照耀他人的特質，您的存在能為周圍帶來正能量。
        但太陽也代表消耗，您可能過度付出而忽略自己的需求。
        """,
        'strengths': ['熱情開朗', '樂於助人', '正直', '有領導力', '人緣好'],
        'challenges': ['過度付出', '可能太過理想化', '不夠務實', '容易疲憊'],
        'career': '適合公職、教育、醫療、公益、需要服務他人的工作',
        'wealth': '財運受地位影響，適合靠名聲與專業賺錢',
        'relationship': '熱情大方，但要注意不要過度犧牲自己'
    },

    '武曲': {
        'name': '武曲星',
        'category': '北斗財星',
        'element': '金',
        'nature': '剛毅、財富、決斷',
        'core_essence': """
        武曲為財星，代表財富與決斷力。您個性剛毅果斷，做事直接不拖泥帶水。
        武曲星帶有金的特質，剛強但可能缺乏柔軟。您對金錢有天生的敏感度，
        善於理財與投資。但要注意過於剛硬可能影響人際關係。
        """,
        'strengths': ['果斷堅毅', '理財能力強', '執行力好', '有原則', '不輕易妥協'],
        'challenges': ['可能過於剛硬', '不夠圓融', '感情表達較差', '孤獨感'],
        'career': '適合金融、工程、軍警、技術、需要決斷力的工作',
        'wealth': '財運佳，適合實業投資，晚年富足',
        'relationship': '感情較為理性，需要學習柔軟與表達'
    },

    '天同': {
        'name': '天同星',
        'category': '南斗福星',
        'element': '水',
        'nature': '和平、享受、隨性',
        'core_essence': """
        天同為福星，代表和平與享受。您個性溫和隨性，不喜歡爭鬥與壓力，
        追求舒適自在的生活。天同星帶有孩子氣的特質，您保持一顆童心，
        樂觀開朗。但可能缺乏野心與競爭力，需要培養積極進取的精神。
        """,
        'strengths': ['和善親切', '樂觀開朗', '隨遇而安', '人緣好', '懂得享受'],
        'challenges': ['缺乏野心', '可能懶散', '依賴性強', '不夠積極'],
        'career': '適合服務業、藝術、娛樂、不需要高壓競爭的工作',
        'wealth': '財運平穩，適合穩定收入，不宜投機',
        'relationship': '感情甜蜜，但要注意不要過於依賴'
    },

    '廉貞': {
        'name': '廉貞星',
        'category': '北斗囚星',
        'element': '火',
        'nature': '囚禁、轉化、熱情',
        'core_essence': """
        廉貞為囚星，代表束縛與轉化。您個性複雜矛盾，內心熱情但外表可能冷淡。
        廉貞帶有囚禁的特質，您可能感到內心的掙扎與束縛。但廉貞也代表轉化，
        您能將困境轉化為成長的動力。廉貞星坐命的人多才多藝，但要注意情緒管理。
        """,
        'strengths': ['多才多藝', '適應力強', '熱情', '有魅力', '轉化能力強'],
        'challenges': ['情緒起伏大', '容易糾結', '可能自我束縛', '桃花問題'],
        'career': '適合藝術、娛樂、公關、銷售、需要魅力的工作',
        'wealth': '財運起伏大，有橫財但也易破財',
        'relationship': '感情豐富但複雜，需要自我約束'
    },

    '天府': {
        'name': '天府星',
        'category': '南斗財庫',
        'element': '土',
        'nature': '穩健、保守、財庫',
        'core_essence': """
        天府為財庫星，代表穩健與保守。您做事謹慎小心，不會輕易冒險。
        天府星具有儲蓄的特質，您善於理財，能守住財富。您重視安全感與穩定性，
        追求平穩的人生。但可能過於保守，錯失一些機會。
        """,
        'strengths': ['穩重可靠', '理財能力強', '謹慎小心', '有耐心', '能守財'],
        'challenges': ['過於保守', '缺乏冒險精神', '可能固執', '變通性不足'],
        'career': '適合財務、會計、行政、傳統產業、需要穩定的工作',
        'wealth': '財運穩定，善於儲蓄，中晚年富足',
        'relationship': '婚姻穩定，但需要注意不要過於保守'
    },

    '太陰': {
        'name': '太陰星',
        'category': '中天田宅',
        'element': '水',
        'nature': '柔和、內斂、計劃',
        'core_essence': """
        太陰為月亮之星，代表柔和與內斂。您個性溫和細膩，善於觀察與規劃。
        太陰星具有陰柔的特質，您可能較為內向，不喜歡張揚。您的力量是柔性的，
        善於以柔克剛。太陰也代表女性與母親，您可能特別重視家庭。
        """,
        'strengths': ['溫柔體貼', '觀察力強', '善於規劃', '細膩', '有耐心'],
        'challenges': ['可能過於內向', '優柔寡斷', '情緒化', '不夠果斷'],
        'career': '適合企劃、設計、教育、照護、需要細膩的工作',
        'wealth': '財運平穩，適合長期投資，靠計劃賺錢',
        'relationship': '感情細膩，重視家庭，但要注意情緒管理'
    },

    '貪狼': {
        'name': '貪狼星',
        'category': '北斗桃花',
        'element': '木/水',
        'nature': '慾望、多才、交際',
        'core_essence': """
        貪狼為慾望之星，代表追求與多才多藝。您興趣廣泛，多才多藝，
        善於交際。貪狼星帶有桃花特質，您魅力強，容易吸引異性。
        您的慾望強烈，追求刺激與新鮮感。但要注意不要過於貪心或分散精力。
        """,
        'strengths': ['多才多藝', '善於交際', '有魅力', '適應力強', '學習快'],
        'challenges': ['容易分心', '貪心', '桃花問題', '不夠專注', '可能投機'],
        'career': '適合娛樂、藝術、銷售、公關、多元發展',
        'wealth': '財運起伏大，有橫財但要小心破財',
        'relationship': '感情豐富，桃花多，需要自律'
    },

    '巨門': {
        'name': '巨門星',
        'category': '北斗暗星',
        'element': '水',
        'nature': '口才、是非、深沉',
        'core_essence': """
        巨門為暗星，代表口才與是非。您口才好，善於辯論與溝通。
        巨門星帶有暗的特質，您可能較為深沉，不輕易表露真實想法。
        您的優勢在於語言與溝通，但要注意可能招惹是非口舌。
        """,
        'strengths': ['口才好', '分析力強', '善於溝通', '邏輯清晰', '有深度'],
        'challenges': ['容易招是非', '可能多疑', '不夠開朗', '言語可能傷人'],
        'career': '適合律師、教師、傳媒、業務、需要口才的工作',
        'wealth': '財運靠口才，適合知識與服務業',
        'relationship': '溝通是關鍵，要注意言語表達'
    },

    '天相': {
        'name': '天相星',
        'category': '南斗印星',
        'element': '水',
        'nature': '輔佐、隨和、印綬',
        'core_essence': """
        天相為印星，代表輔佐與隨和。您個性隨和，善於協調與配合。
        天相星具有印綬的特質，適合輔佐他人，在團隊中扮演重要角色。
        您重視外表與形象，有品味。但可能缺乏主見，容易受人影響。
        """,
        'strengths': ['隨和親切', '協調能力強', '有品味', '善於輔佐', '人緣好'],
        'challenges': ['缺乏主見', '容易受影響', '可能依賴他人', '不夠堅定'],
        'career': '適合幕僚、公關、服務、需要協調的工作',
        'wealth': '財運平穩，適合穩定工作，靠他人提攜',
        'relationship': '感情和諧，但要注意建立自己的主見'
    },

    '天梁': {
        'name': '天梁星',
        'category': '南斗壽星',
        'element': '土',
        'nature': '蔭護、清高、孤獨',
        'core_essence': """
        天梁為蔭星，代表庇護與清高。您個性清高，有正義感，喜歡幫助他人。
        天梁星帶有長者的特質，您可能較為成熟穩重，甚至有些孤獨感。
        您適合當他人的靠山，但要注意不要過於清高而與人疏離。
        """,
        'strengths': ['正直清高', '有正義感', '穩重', '善於照顧他人', '貴人運佳'],
        'challenges': ['可能孤獨', '過於清高', '不夠親和', '固執'],
        'career': '適合公職、醫療、社工、宗教、需要幫助他人的工作',
        'wealth': '財運平穩，晚年運佳，靠名聲與地位',
        'relationship': '感情穩定，但可能較為平淡'
    },

    '七殺': {
        'name': '七殺星',
        'category': '南斗將星',
        'element': '金',
        'nature': '剛烈、衝動、開創',
        'core_essence': """
        七殺為將星，代表剛烈與開創。您個性剛強果斷，有魄力與衝勁。
        七殺星具有將軍的特質，您適合開創與競爭，不怕挑戰。
        但要注意過於衝動可能帶來風險，需要培養耐心與策略思維。
        """,
        'strengths': ['果斷有魄力', '勇於挑戰', '執行力強', '不怕困難', '開創性強'],
        'challenges': ['過於衝動', '缺乏耐心', '可能孤獨', '不夠圓融'],
        'career': '適合軍警、創業、競爭性行業、需要魄力的工作',
        'wealth': '財運起伏大，適合創業與投資，但風險高',
        'relationship': '感情直接，但要注意不要過於剛強'
    },

    '破軍': {
        'name': '破軍星',
        'category': '北斗耗星',
        'element': '水',
        'nature': '破壞、變動、創新',
        'core_essence': """
        破軍為耗星，代表破壞與創新。您勇於打破現狀，追求變革與創新。
        破軍星帶有破壞的特質，您的人生可能充滿變動，不安於現狀。
        您是天生的改革者，但要注意破壞後要懂得建設。
        """,
        'strengths': ['勇於創新', '不怕改變', '開創性強', '有衝勁', '適應力強'],
        'challenges': ['過於變動', '不夠穩定', '可能破壞性強', '缺乏耐心'],
        'career': '適合創新產業、改革、創業、需要變革的工作',
        'wealth': '財運起伏大，適合創新投資，但風險高',
        'relationship': '感情變動大，需要穩定的伴侶'
    }
}


# ============================================================================
# 星曜組合解讀庫 (Star Combination Interpretations)
# ============================================================================

STAR_COMBINATIONS = {
    ('紫微', '天府'): {
        'name': '君臣慶會',
        'quality': '極佳',
        'interpretation': """
        紫微天府同宮是紫微斗數中最穩定的帝星組合，被稱為「君臣慶會」格局。
        紫微代表領導權威，天府代表財富穩健，兩者結合形成「有權有財」的完美平衡。

        **組合特質**：
        - 一生較為順遂，少有大起大落
        - 既有領導氣質，又有理財能力
        - 適合在大型組織中擔任要職
        - 財務管理能力強，善於守財
        - 晚年運勢特別好

        **注意事項**：
        - 可能過於保守，錯失創新機會
        - 需要避免過度自我中心
        - 應該培養冒險與創新精神
        - 不要過於重視面子而失去彈性
        """,
        'career': '適合管理、行政、金融、政府部門、大型企業高階主管',
        'wealth': '財運穩定，善於理財，中晚年富足，適合穩健投資',
        'relationship': '婚姻穩定，配偶能幹，但可能缺乏激情與浪漫'
    },

    ('廉貞', '貪狼'): {
        'name': '桃花犯主',
        'quality': '複雜',
        'interpretation': """
        廉貞貪狼組合充滿矛盾與張力，是紫微斗數中最複雜的組合之一。
        廉貞為囚星代表束縛與轉化，貪狼為桃花星代表慾望與追求。

        **組合特質**：
        - 魅力強大，容易吸引異性
        - 慾望強烈，追求刺激與新鮮感
        - 多才多藝，興趣廣泛
        - 適應力強，能在不同領域發展
        - 容易陷入感情糾葛

        **注意事項**：
        - 感情方面要特別自律
        - 避免過度投機冒險
        - 培養專注力，不要太分散
        - 情緒管理很重要
        """,
        'career': '適合娛樂、藝術、銷售、公關、需要魅力與多元才能的工作',
        'wealth': '財運起伏大，有橫財但也易破財，不宜過度投機',
        'relationship': '感情豐富但複雜，桃花多，需要自我約束與專一'
    },

    ('武曲', '七殺'): {
        'name': '將星得位',
        'quality': '強勢',
        'interpretation': """
        武曲七殺組合是剛強果斷的代表，兩顆金星同宮形成強大的決斷力。

        **組合特質**：
        - 個性剛強果斷，魄力十足
        - 執行力超強，說做就做
        - 適合開創性工作或創業
        - 不怕挑戰與競爭
        - 財運與事業運皆強

        **注意事項**：
        - 過於剛硬，人際關係可能緊張
        - 需要培養柔軟與圓融
        - 避免過度衝動的決策
        - 感情表達需要加強
        """,
        'career': '適合軍警、工程、技術、創業、需要魄力與決斷的工作',
        'wealth': '財運佳，適合創業與投資，但要注意風險控管',
        'relationship': '感情較為理性剛強，需要柔軟的伴侶平衡'
    },

    ('太陽', '太陰'): {
        'name': '日月並明',
        'quality': '極佳',
        'interpretation': """
        太陽太陰組合是陰陽調和的完美象徵，代表剛柔並濟。

        **組合特質**：
        - 個性平衡，既開朗又細膩
        - 適應力強，能剛能柔
        - 人際關係佳，左右逢源
        - 貴人運強，容易得到幫助
        - 男女皆宜的好格局

        **注意事項**：
        - 要注意太陽與太陰的廟旺位置
        - 可能過於在意他人看法
        - 需要培養自己的主見
        """,
        'career': '適合公職、教育、服務業、需要平衡能力的工作',
        'wealth': '財運平穩，靠名聲與專業，中晚年運佳',
        'relationship': '感情和諧，能兼顧家庭與事業'
    },

    ('天機', '巨門'): {
        'name': '善談兵',
        'quality': '中等',
        'interpretation': """
        天機巨門組合是智慧與口才的結合，但也帶來是非困擾。

        **組合特質**：
        - 聰明機智，口才極佳
        - 分析能力強，邏輯清晰
        - 善於辯論與溝通
        - 適合需要腦力與口才的工作
        - 但容易招惹是非口舌

        **注意事項**：
        - 說話要謹慎，避免得罪人
        - 不要過於多疑
        - 培養積極正面的思維
        - 行動力需要加強
        """,
        'career': '適合律師、教師、傳媒、顧問、需要智慧與口才的工作',
        'wealth': '財運靠智慧與口才，適合知識服務業',
        'relationship': '溝通是關鍵，但要注意言語可能傷人'
    },

    ('天機', '天梁'): {
        'name': '機梁善談兵',
        'quality': '佳',
        'interpretation': """
        天機天梁組合是智慧與蔭護的結合，被稱為「善談兵」格局。

        **組合特質**：
        - 智慧與經驗兼備
        - 善於策劃與指導
        - 適合軍師、顧問角色
        - 有長者風範，受人尊敬
        - 貴人運強

        **注意事項**：
        - 可能過於清高
        - 需要注意不要太理論化
        - 行動力要加強
        """,
        'career': '適合顧問、策劃、教育、宗教、需要智慧與經驗的工作',
        'wealth': '財運平穩，靠智慧與經驗，晚年運佳',
        'relationship': '感情穩定，配偶可能年紀較大或較為成熟'
    },

    ('武曲', '貪狼'): {
        'name': '武貪',
        'quality': '複雜',
        'interpretation': """
        武曲貪狼組合是財星與慾望星的結合，極具爆發力。

        **組合特質**：
        - 賺錢能力強，敢拼敢賺
        - 多才多藝，適應力強
        - 有橫財運，可能突然發達
        - 慾望強烈，追求刺激
        - 適合創業與投資

        **注意事項**：
        - 容易投機冒險
        - 感情方面要自律
        - 避免過度貪心
        - 財來財去，要懂得守財
        """,
        'career': '適合創業、投資、娛樂、銷售、需要爆發力的工作',
        'wealth': '財運起伏大，有橫財但也易破財，適合創業與投資',
        'relationship': '感情豐富但複雜，桃花多，需要專一'
    },

    ('紫微', '破軍'): {
        'name': '紫破',
        'quality': '強勢',
        'interpretation': """
        紫微破軍組合是帝星與開創星的結合，具有強大的改革力量。

        **組合特質**：
        - 領導力強，勇於創新
        - 不怕挑戰，敢於破舊立新
        - 適合開創性工作
        - 一生多變動，不安於現狀
        - 能成就大事業

        **注意事項**：
        - 變動太大可能不穩定
        - 破壞後要懂得建設
        - 需要培養耐心
        - 避免過度衝動
        """,
        'career': '適合創新產業、改革、創業、需要開創精神的工作',
        'wealth': '財運起伏大，適合創業與投資，但風險高',
        'relationship': '感情變動大，需要包容的伴侶'
    },

    ('天同', '天梁'): {
        'name': '同梁',
        'quality': '佳',
        'interpretation': """
        天同天梁組合是福星與蔭星的結合，代表平順安逸。

        **組合特質**：
        - 一生較為平順，少有大風波
        - 貴人運強，容易得到幫助
        - 個性溫和，人緣好
        - 適合穩定的工作
        - 晚年運特別好

        **注意事項**：
        - 可能缺乏野心與競爭力
        - 需要培養積極進取精神
        - 避免過於安逸而停滯不前
        """,
        'career': '適合公職、教育、社會服務、需要穩定的工作',
        'wealth': '財運平穩，適合穩定收入，晚年富足',
        'relationship': '感情和諧穩定，婚姻美滿'
    },

    ('廉貞', '七殺'): {
        'name': '廉殺',
        'quality': '強勢',
        'interpretation': """
        廉貞七殺組合充滿爆發力與衝勁，是紫微斗數中的強勢組合。

        **組合特質**：
        - 個性剛烈，魄力十足
        - 執行力超強，敢作敢為
        - 適合開創性工作
        - 有魅力，容易成為焦點
        - 事業運強

        **注意事項**：
        - 過於剛烈，人際關係緊張
        - 情緒起伏大，需要控制
        - 感情可能複雜
        - 避免過度衝動
        """,
        'career': '適合軍警、創業、競爭性行業、需要魄力的工作',
        'wealth': '財運起伏大，適合創業與投資，但風險高',
        'relationship': '感情熱烈但複雜，需要理性伴侶平衡'
    }
}


# ============================================================================
# 十二宮位解釋函數 (Palace Interpretation Functions)
# ============================================================================

def interpret_ziwei_palaces(ziwei_data: Dict) -> Dict:
    """紫微斗數十二宮位深度解釋

    Args:
        ziwei_data: ZiWei calculator output

    Returns:
        Dict: {
            'palace_interpretations': Dict,  # 各宮位詳細解釋
            'major_patterns': List[str],  # 主要格局
            'life_summary': str,  # 整體命盤總結
            'key_recommendations': List[str]  # 關鍵建議
        }
    """
    palaces_data = ziwei_data.get('palaces', {})

    # 解釋各宮位
    interpretations = {}
    palace_names = ['命宮', '兄弟宮', '夫妻宮', '子女宮', '財帛宮', '疾厄宮',
                    '遷移宮', '奴僕宮', '官祿宮', '田宅宮', '福德宮', '父母宮']

    for palace_name in palace_names:
        if palace_name in palaces_data:
            interpretations[palace_name] = _interpret_single_palace(
                palace_name,
                palaces_data[palace_name]
            )

    # 識別主要格局
    major_patterns = _identify_major_patterns(palaces_data)

    # 生成整體總結
    life_summary = _generate_life_summary(interpretations, major_patterns)

    # 關鍵建議
    key_recommendations = _generate_key_recommendations(interpretations, major_patterns)

    return {
        'palace_interpretations': interpretations,
        'major_patterns': major_patterns,
        'life_summary': life_summary,
        'key_recommendations': key_recommendations
    }


def _interpret_single_palace(palace_name: str, palace_data: Dict) -> Dict:
    """解釋單一宮位"""
    major_stars = palace_data.get('major_stars', [])
    minor_stars = palace_data.get('minor_stars', [])
    brightness = palace_data.get('brightness', '平')

    # 生成宮位解釋
    interpretation = _generate_palace_interpretation(
        palace_name, major_stars, minor_stars, brightness
    )

    # 生成人生啟示
    implications = _generate_palace_implications(palace_name, major_stars)

    # 生成建議
    recommendations = _generate_palace_recommendations(palace_name, major_stars)

    return {
        'major_stars': major_stars,
        'minor_stars': minor_stars,
        'brightness': brightness,
        'detailed_interpretation': interpretation,
        'life_implications': implications,
        'recommendations': recommendations
    }


def _generate_palace_interpretation(palace_name: str, major_stars: List[str],
                                    minor_stars: List[str], brightness: str) -> str:
    """生成宮位詳細解釋"""
    parts = []

    # 宮位標題
    stars_str = '、'.join(major_stars) if major_stars else '無主星'
    parts.append(f"## {palace_name}：{stars_str}")

    # 主星解釋
    if len(major_stars) >= 2:
        # 檢查是否有組合解釋
        combo_key = tuple(sorted(major_stars[:2]))
        if combo_key in STAR_COMBINATIONS:
            combo = STAR_COMBINATIONS[combo_key]
            parts.append(f"\n**{combo['name']}格局**（{combo['quality']}）")
            parts.append(combo['interpretation'])
        else:
            # 分別解釋各星
            for star in major_stars:
                if star in MAJOR_STAR_TRAITS:
                    trait = MAJOR_STAR_TRAITS[star]
                    parts.append(f"\n**{trait['name']}特質**：")
                    parts.append(trait['core_essence'])
    elif len(major_stars) == 1:
        star = major_stars[0]
        if star in MAJOR_STAR_TRAITS:
            trait = MAJOR_STAR_TRAITS[star]
            parts.append(f"\n**{trait['name']}獨坐**：")
            parts.append(trait['core_essence'])
            parts.append(f"\n**優勢**：{', '.join(trait['strengths'])}")
            parts.append(f"\n**挑戰**：{', '.join(trait['challenges'])}")
    else:
        parts.append("\n此宮無主星，需要參考對宮星曜來判斷。")

    # 廟旺平陷的影響
    if brightness:
        brightness_effect = {
            '廟': '星曜力量最強，能充分發揮正面特質',
            '旺': '星曜力量強，大多能發揮正面作用',
            '平': '星曜力量中等，吉凶參半',
            '陷': '星曜力量弱，負面特質可能顯現',
            '落': '星曜力量最弱，需要努力克服困難'
        }
        if brightness in brightness_effect:
            parts.append(f"\n**廟旺狀態**：{brightness} - {brightness_effect[brightness]}")

    # 輔星影響
    if minor_stars:
        auspicious = [s for s in minor_stars if s in ['左輔', '右弼', '文昌', '文曲', '天魁', '天鉞']]
        inauspicious = [s for s in minor_stars if s in ['擎羊', '陀羅', '火星', '鈴星', '地空', '地劫']]

        if auspicious:
            parts.append(f"\n**吉星加持**：{', '.join(auspicious)} - 增強正面力量，貴人運佳")
        if inauspicious:
            parts.append(f"\n**煞星同宮**：{', '.join(inauspicious)} - 增加挑戰，需要特別注意")

    return "\n".join(parts)


def _generate_palace_implications(palace_name: str, major_stars: List[str]) -> Dict:
    """生成宮位人生啟示"""
    implications = {
        '命宮': {
            'aspect': '個性與人生方向',
            'description': '命宮決定您的基本個性、人生追求與整體運勢走向'
        },
        '兄弟宮': {
            'aspect': '手足關係與平輩互動',
            'description': '兄弟宮顯示您與兄弟姊妹、朋友同事的關係，以及合夥運勢'
        },
        '夫妻宮': {
            'aspect': '婚姻與感情狀況',
            'description': '夫妻宮代表您的婚姻狀況、配偶特質與感情模式'
        },
        '子女宮': {
            'aspect': '子女關係與創造力',
            'description': '子女宮顯示與子女的緣分、教育方式，也代表創造力與性生活'
        },
        '財帛宮': {
            'aspect': '財運與理財能力',
            'description': '財帛宮決定您的財運、賺錢能力與理財方式'
        },
        '疾厄宮': {
            'aspect': '健康狀況與體質',
            'description': '疾厄宮顯示您的健康傾向、體質強弱與需要注意的疾病'
        },
        '遷移宮': {
            'aspect': '外出運與人際關係',
            'description': '遷移宮代表外出運勢、貴人運與在外表現'
        },
        '奴僕宮': {
            'aspect': '部屬關係與社交',
            'description': '奴僕宮（交友宮）顯示您的社交能力、朋友品質與部屬運'
        },
        '官祿宮': {
            'aspect': '事業與工作狀況',
            'description': '官祿宮決定您的事業運、適合的工作類型與成就高低'
        },
        '田宅宮': {
            'aspect': '不動產與家庭',
            'description': '田宅宮代表不動產運、家庭環境與祖產情況'
        },
        '福德宮': {
            'aspect': '精神生活與福氣',
            'description': '福德宮顯示您的精神狀態、興趣愛好與晚年福氣'
        },
        '父母宮': {
            'aspect': '父母關係與長輩緣',
            'description': '父母宮代表與父母的關係、長輩緣分與讀書運'
        }
    }

    return implications.get(palace_name, {'aspect': palace_name, 'description': ''})


def _generate_palace_recommendations(palace_name: str, major_stars: List[str]) -> List[str]:
    """生成宮位建議"""
    recommendations = []

    # 根據宮位給出針對性建議
    palace_advice = {
        '命宮': [
            '了解自己的個性優勢，發揮長處',
            '注意個性中的挑戰，努力改善',
            '設定符合命格的人生目標'
        ],
        '夫妻宮': [
            '了解理想伴侶的特質',
            '注意感情中的挑戰與風險',
            '經營婚姻需要用心與智慧'
        ],
        '財帛宮': [
            '選擇適合自己的賺錢方式',
            '培養良好的理財習慣',
            '避免不適合的投資方式'
        ],
        '官祿宮': [
            '選擇適合的職業方向',
            '發展事業上的核心競爭力',
            '注意職場中的人際關係'
        ]
    }

    return palace_advice.get(palace_name, ['發揮此宮的正面力量', '注意並改善挑戰'])


def _identify_major_patterns(palaces_data: Dict) -> List[str]:
    """識別主要格局"""
    patterns = []

    # 檢查命宮星曜組合
    ming_gong = palaces_data.get('命宮', {})
    major_stars = ming_gong.get('major_stars', [])

    if len(major_stars) >= 2:
        combo_key = tuple(sorted(major_stars[:2]))
        if combo_key in STAR_COMBINATIONS:
            patterns.append(STAR_COMBINATIONS[combo_key]['name'])

    # 可以添加更多格局識別邏輯
    # 例如：祿存、化祿、化權、化科、化忌的組合

    return patterns if patterns else ['一般格局']


def _generate_life_summary(interpretations: Dict, major_patterns: List[str]) -> str:
    """生成整體命盤總結"""
    summary_parts = []

    summary_parts.append("## 命盤整體總結\n")

    # 主要格局
    if major_patterns:
        patterns_str = '、'.join(major_patterns)
        summary_parts.append(f"**主要格局**：{patterns_str}\n")

    # 命宮概述
    if '命宮' in interpretations:
        ming_gong = interpretations['命宮']
        stars = ming_gong.get('major_stars', [])
        if stars:
            summary_parts.append(f"您的命宮坐落 {', '.join(stars)}，")
            summary_parts.append("這決定了您的基本性格與人生方向。\n")

    # 整體評估
    summary_parts.append("""
您的命盤顯示了獨特的人生軌跡。每個宮位都有其意義，
重要的是了解自己的優勢與挑戰，善用優勢，改善不足。
紫微斗數提供的是人生的可能性與傾向，實際發展仍取決於您的努力與選擇。
""")

    return "".join(summary_parts)


def _generate_key_recommendations(interpretations: Dict, major_patterns: List[str]) -> List[str]:
    """生成關鍵建議"""
    recommendations = []

    recommendations.append("**了解自己的命格特質**：認識自己的優勢與挑戰是改變的第一步")
    recommendations.append("**發揮正面星曜的力量**：善用命格中的吉星與好的組合")
    recommendations.append("**克服負面影響**：面對挑戰，化煞為權")
    recommendations.append("**把握大運流年**：了解運勢變化，順勢而為")
    recommendations.append("**積極創造命運**：命理只是參考，努力才能改變人生")

    return recommendations


# ============================================================================
# 四化飛星分析 (Four Transformations Analysis)
# ============================================================================

# 四化飛星特質資料庫
FOUR_TRANSFORMATIONS = {
    '化祿': {
        'name': '化祿',
        'nature': '財富、順利、喜悅',
        'effect': '增強星曜的正面力量，帶來財富與機會',
        'interpretation': '化祿代表順利與財富，是四化中最吉利的。無論化祿落在哪個宮位，都能增強該宮位的正面能量，帶來順利與收穫。'
    },
    '化權': {
        'name': '化權',
        'nature': '權力、掌控、積極',
        'effect': '增強星曜的權力與掌控力',
        'interpretation': '化權代表權力與掌控，能增強星曜的領導力與執行力。化權落宮，代表在該領域有掌控力，但也可能過於強勢。'
    },
    '化科': {
        'name': '化科',
        'nature': '名聲、文采、貴人',
        'effect': '帶來名聲、貴人與好運',
        'interpretation': '化科代表名聲與貴人，能帶來好的名聲與貴人相助。化科落宮，代表在該領域容易獲得認可與幫助。'
    },
    '化忌': {
        'name': '化忌',
        'nature': '阻礙、糾結、執著',
        'effect': '帶來挑戰與困擾，但也代表執著',
        'interpretation': '化忌代表阻礙與糾結，是四化中較為負面的。但化忌也代表執著，若能正面轉化，可成為動力。化忌落宮需要特別注意該領域的問題。'
    }
}


def analyze_four_transformations(ziwei_data: Dict) -> Dict:
    """四化飛星動態分析

    Args:
        ziwei_data: ZiWei calculator output

    Returns:
        Dict: {
            'transformations': Dict,  # 四化星曜位置
            'dynamic_analysis': List[str],  # 動態分析
            'life_events': Dict,  # 人生事件預測
            'recommendations': List[str]  # 建議
        }
    """
    transformations = ziwei_data.get('four_transformations', {})
    palaces_data = ziwei_data.get('palaces', {})

    analysis = {
        'transformations': transformations,
        'dynamic_analysis': [],
        'life_events': {},
        'recommendations': []
    }

    # 分析化祿位置
    if '化祿' in transformations:
        lu_palace = transformations['化祿']['palace']
        lu_star = transformations['化祿']['star']
        analysis['dynamic_analysis'].append(
            f"**化祿在{lu_palace}（{lu_star}星化祿）**：此宮位將有順利發展與財富收穫的機會。"
        )

    # 分析化權位置
    if '化權' in transformations:
        quan_palace = transformations['化權']['palace']
        quan_star = transformations['化權']['star']
        analysis['dynamic_analysis'].append(
            f"**化權在{quan_palace}（{quan_star}星化權）**：在此領域您有掌控力，但要注意不要過於強勢。"
        )

    # 分析化科位置
    if '化科' in transformations:
        ke_palace = transformations['化科']['palace']
        ke_star = transformations['化科']['star']
        analysis['dynamic_analysis'].append(
            f"**化科在{ke_palace}（{ke_star}星化科）**：此領域容易獲得名聲與貴人相助。"
        )

    # 分析化忌位置
    if '化忌' in transformations:
        ji_palace = transformations['化忌']['palace']
        ji_star = transformations['化忌']['star']
        analysis['dynamic_analysis'].append(
            f"**化忌在{ji_palace}（{ji_star}星化忌）**：此宮位需要特別注意，可能有阻礙或糾結，需要用心經營。"
        )

    # 生成人生事件預測
    analysis['life_events'] = _generate_life_events_from_transformations(transformations)

    # 生成建議
    analysis['recommendations'] = _generate_transformation_recommendations(transformations)

    return analysis


def _generate_life_events_from_transformations(transformations: Dict) -> Dict:
    """根據四化生成人生事件預測"""
    events = {}

    if '化祿' in transformations:
        palace = transformations['化祿']['palace']
        events['fortune_area'] = f"{palace}是您的幸運領域，容易有順利發展"

    if '化忌' in transformations:
        palace = transformations['化忌']['palace']
        events['challenge_area'] = f"{palace}可能是您的挑戰領域，需要特別用心"

    return events


def _generate_transformation_recommendations(transformations: Dict) -> List[str]:
    """根據四化生成建議"""
    recommendations = []

    if '化祿' in transformations:
        recommendations.append("善用化祿宮位的優勢，把握順利發展的機會")

    if '化權' in transformations:
        recommendations.append("發揮化權宮位的領導力，但要注意不要過於強勢")

    if '化科' in transformations:
        recommendations.append("重視化科宮位的名聲與貴人，建立良好口碑")

    if '化忌' in transformations:
        recommendations.append("化忌宮位需要特別用心經營，將執著轉化為動力")

    return recommendations


# ============================================================================
# 專門宮位解釋函數 (Specialized Palace Interpretation Functions)
# ============================================================================

def interpret_destiny_palace(ziwei_data: Dict) -> Dict:
    """命宮深度解釋（LLM增強版）

    Returns:
        Dict: {
            'basic_personality': str,  # 基本個性（200-300字）
            'life_direction': str,  # 人生方向
            'strengths': List[str],  # 優勢特質
            'challenges': List[str],  # 挑戰特質
            'development_suggestions': List[str],  # 發展建議
            'confidence_level': Dict,  # 信心度評估
            'llm_analysis': str (optional)  # LLM深度分析
        }
    """
    # Try LLM analysis with fallback
    llm_analyzer = get_llm_analyzer()

    if llm_analyzer.is_available() and ZIWEI_SYSTEM_PROMPT:
        palaces_data = ziwei_data.get('palaces', {})
        ming_gong = palaces_data.get('命宮', {})

        analysis_prompt = construct_ziwei_palace_prompt('命宮', ming_gong)

        llm_result = llm_analyzer.analyze_with_fallback(
            system_prompt=ZIWEI_SYSTEM_PROMPT,
            analysis_prompt=analysis_prompt,
            fallback_func=_traditional_destiny_palace_analysis,
            fallback_args=(ziwei_data,),
            min_length=250,
            temperature=0.7,
            max_tokens=3000
        )

        # Check if llm_result is a string (LLM success) or dict (fallback was used)
        if isinstance(llm_result, str) and len(llm_result.replace(' ', '').replace('\n', '')) >= 250:
            confidence = calculate_confidence_level(
                consensus_indicators=1,
                total_indicators=1,
                data_quality=1.0,
                theoretical_support=0.9
            )

            traditional_result = _traditional_destiny_palace_analysis(ziwei_data)
            traditional_result['llm_analysis'] = llm_result
            traditional_result['confidence_level'] = confidence
            traditional_result['analysis_method'] = 'LLM enhanced'
            return traditional_result
        elif isinstance(llm_result, dict):
            # Fallback was already executed, return it directly
            return llm_result

    return _traditional_destiny_palace_analysis(ziwei_data)


def _traditional_destiny_palace_analysis(ziwei_data: Dict) -> Dict:
    """傳統命宮分析"""
    palaces_data = ziwei_data.get('palaces', {})
    ming_gong = palaces_data.get('命宮', {})
    major_stars = ming_gong.get('major_stars', [])

    result = {
        'basic_personality': '',
        'life_direction': '',
        'strengths': [],
        'challenges': [],
        'development_suggestions': []
    }

    # 基本個性描述
    personality_parts = ["## 命宮：您的基本個性\n"]

    if major_stars:
        stars_str = '、'.join(major_stars)
        personality_parts.append(f"您的命宮坐落 **{stars_str}**，這決定了您的基本性格與人生追求。\n")

        # 整合主星特質
        for star in major_stars:
            if star in MAJOR_STAR_TRAITS:
                trait = MAJOR_STAR_TRAITS[star]
                personality_parts.append(f"\n**{trait['name']}特質**：{trait['nature']}")
                personality_parts.append(trait['core_essence'])
                result['strengths'].extend(trait['strengths'][:3])
                result['challenges'].extend(trait['challenges'][:2])
    else:
        personality_parts.append("您的命宮無主星，需要參考對宮（遷移宮）的星曜來判斷基本性格。")

    result['basic_personality'] = "\n".join(personality_parts)

    # 人生方向
    if major_stars:
        direction_map = {
            '紫微': '追求地位、成就與被尊重',
            '天機': '追求智慧、變化與策劃',
            '太陽': '追求光明、服務與正義',
            '武曲': '追求財富、實力與果斷',
            '天同': '追求和平、享受與自在',
            '廉貞': '追求轉化、熱情與多元',
            '天府': '追求穩定、財富與安全',
            '太陰': '追求計劃、細膩與家庭',
            '貪狼': '追求多元、刺激與慾望',
            '巨門': '追求真相、溝通與深度',
            '天相': '追求協調、輔佐與品味',
            '天梁': '追求清高、蔭護與正義',
            '七殺': '追求開創、挑戰與競爭',
            '破軍': '追求創新、變革與突破'
        }

        directions = [direction_map.get(star, '') for star in major_stars if star in direction_map]
        result['life_direction'] = '、'.join(directions) if directions else '多元發展，尋找適合的道路'

    # 發展建議
    result['development_suggestions'] = [
        '認識並發揮您的優勢特質',
        '正視並改善挑戰特質',
        '選擇符合命格特質的發展道路',
        '培養命宮星曜所需的能力',
        '善用輔星的正面力量'
    ]

    # Add confidence scoring
    confidence = calculate_confidence_level(
        consensus_indicators=1,
        total_indicators=1,
        data_quality=1.0,
        theoretical_support=0.8
    )
    result['confidence_level'] = confidence
    result['analysis_method'] = 'Traditional rule-based'

    return result


def interpret_wealth_palace(ziwei_data: Dict) -> Dict:
    """財帛宮深度解釋（類似八字的財富分析）

    Returns:
        Dict: {
            'wealth_potential': str,  # 財富潛力評估
            'earning_style': str,  # 賺錢方式
            'suitable_industries': List[str],  # 適合行業
            'investment_advice': str,  # 投資建議
            'wealth_timeline': Dict  # 財富時間軸
        }
    """
    palaces_data = ziwei_data.get('palaces', {})
    wealth_palace = palaces_data.get('財帛宮', {})
    major_stars = wealth_palace.get('major_stars', [])

    result = {
        'wealth_potential': '',
        'earning_style': '',
        'suitable_industries': [],
        'investment_advice': '',
        'wealth_timeline': {}
    }

    # 財富潛力評估
    if major_stars:
        stars_str = '、'.join(major_stars)
        potential_intro = f"您的財帛宮有 **{stars_str}**，"

        # 根據主星判斷財富潛力
        strong_wealth_stars = ['武曲', '天府', '太陰', '貪狼']
        has_strong_star = any(star in major_stars for star in strong_wealth_stars)

        if has_strong_star:
            result['wealth_potential'] = potential_intro + "財運整體不錯，具有良好的賺錢能力與理財天賦。"
        else:
            result['wealth_potential'] = potential_intro + "財運平穩，需要通過努力與智慧來累積財富。"

    # 賺錢方式
    earning_styles = {
        '武曲': '適合實業投資、金融財務，靠決斷力與執行力賺錢',
        '天府': '適合穩健投資、財務管理，靠保守穩健賺錢',
        '太陰': '適合計劃投資、不動產，靠細膩規劃賺錢',
        '貪狼': '適合多元發展、創業投資，靠多才多藝賺錢',
        '紫微': '適合管理職位、名聲地位，靠領導力賺錢',
        '天機': '適合策劃顧問、智慧服務，靠頭腦賺錢',
        '太陽': '適合專業服務、公職，靠名聲與專業賺錢',
        '天同': '適合穩定收入、服務業，靠穩定工作賺錢',
        '廉貞': '適合藝術娛樂、多元發展，靠魅力與才藝賺錢',
        '巨門': '適合口才服務、知識產業，靠口才與分析賺錢',
        '天相': '適合輔助管理、服務業，靠協調能力賺錢',
        '天梁': '適合專業服務、長者產業，靠經驗與名聲賺錢',
        '七殺': '適合創業開創、競爭產業，靠魄力與執行力賺錢',
        '破軍': '適合創新產業、改革事業，靠創新與變革賺錢'
    }

    styles = [earning_styles.get(star, '') for star in major_stars if star in earning_styles]
    result['earning_style'] = '、'.join(styles) if styles else '需要多方嘗試，找到適合的賺錢方式'

    # 適合行業（從主星特質中提取）
    for star in major_stars:
        if star in MAJOR_STAR_TRAITS:
            career_hint = MAJOR_STAR_TRAITS[star].get('career', '')
            if career_hint:
                result['suitable_industries'].append(career_hint)

    # 投資建議
    conservative_stars = ['天府', '太陰', '天同', '天相']
    aggressive_stars = ['武曲', '貪狼', '七殺', '破軍']

    has_conservative = any(star in major_stars for star in conservative_stars)
    has_aggressive = any(star in major_stars for star in aggressive_stars)

    if has_conservative:
        result['investment_advice'] = "適合穩健保守的投資策略，長期持有，避免高風險投機。"
    elif has_aggressive:
        result['investment_advice'] = "可以適度冒險投資，但要做好風險控管，避免過度投機。"
    else:
        result['investment_advice'] = "投資需謹慎評估，建議分散風險，穩健為主。"

    # 財富時間軸
    result['wealth_timeline'] = {
        '青年期（20-35歲）': '財富累積期，需要努力工作與儲蓄',
        '中年期（35-50歲）': '財富成長期，事業與收入穩定上升',
        '壯年期（50-65歲）': '財富高峰期，收入達到頂峰',
        '老年期（65歲以後）': '財富保存期，享受累積的財富'
    }

    return result


def interpret_career_palace(ziwei_data: Dict) -> Dict:
    """官祿宮深度解釋（類似八字的事業分析）

    Returns:
        Dict: {
            'career_direction': str,  # 事業方向
            'leadership_style': str,  # 領導風格
            'suitable_positions': List[str],  # 適合職位
            'career_challenges': List[str],  # 事業挑戰
            'success_keys': List[str]  # 成功關鍵
        }
    """
    palaces_data = ziwei_data.get('palaces', {})
    career_palace = palaces_data.get('官祿宮', {})
    major_stars = career_palace.get('major_stars', [])

    result = {
        'career_direction': '',
        'leadership_style': '',
        'suitable_positions': [],
        'career_challenges': [],
        'success_keys': []
    }

    # 事業方向
    if major_stars:
        stars_str = '、'.join(major_stars)
        result['career_direction'] = f"您的官祿宮有 **{stars_str}**，"

        leadership_stars = ['紫微', '天府', '武曲', '七殺']
        creative_stars = ['天機', '貪狼', '破軍']
        service_stars = ['太陽', '天同', '天相', '天梁']

        if any(star in major_stars for star in leadership_stars):
            result['career_direction'] += "適合管理領導類工作，能掌握權力與資源。"
        elif any(star in major_stars for star in creative_stars):
            result['career_direction'] += "適合創新策劃類工作，發揮創意與變革能力。"
        elif any(star in major_stars for star in service_stars):
            result['career_direction'] += "適合服務專業類工作，發揮助人與專業精神。"
        else:
            result['career_direction'] += "需要依據個人興趣與能力選擇合適的發展方向。"

    # 領導風格（僅針對主要領導星）
    leadership_map = {
        '紫微': '權威型領導，重視尊嚴與制度，適合擔任最高主管',
        '天府': '穩健型領導，重視財務與穩定，適合財務或行政主管',
        '武曲': '果斷型領導，重視效率與執行，適合執行長或業務主管',
        '七殺': '衝鋒型領導，重視開創與競爭，適合創業或開拓主管',
        '天機': '智囊型領導，重視策劃與分析，適合幕僚或顧問',
        '太陽': '服務型領導，重視公平與照顧，適合公職或人資主管',
        '破軍': '改革型領導，重視創新與變革，適合創新或改革主管'
    }

    styles = [leadership_map.get(star, '') for star in major_stars if star in leadership_map]
    result['leadership_style'] = styles[0] if styles else '需要培養適合自己的領導風格'

    # 適合職位
    for star in major_stars:
        if star in MAJOR_STAR_TRAITS:
            career_hint = MAJOR_STAR_TRAITS[star].get('career', '')
            if career_hint:
                result['suitable_positions'].append(career_hint)

    # 事業挑戰
    challenge_stars = {
        '紫微': '可能過於重視面子，需要培養親和力',
        '武曲': '可能過於剛硬，需要培養圓融',
        '七殺': '可能過於衝動，需要培養耐心',
        '破軍': '可能過於變動，需要培養穩定性',
        '貪狼': '可能過於分散，需要培養專注力',
        '巨門': '可能容易招是非，需要謹言慎行'
    }

    for star in major_stars:
        if star in challenge_stars:
            result['career_challenges'].append(challenge_stars[star])

    # 成功關鍵
    result['success_keys'] = [
        '發揮命格中的優勢特質',
        '選擇適合的職業領域',
        '培養所需的專業能力',
        '建立良好的人際網絡',
        '把握關鍵的發展機會'
    ]

    return result


def interpret_marriage_palace(ziwei_data: Dict, gender: str = 'male') -> Dict:
    """夫妻宮深度解釋（類似八字的感情分析）

    Args:
        ziwei_data: ZiWei calculator output
        gender: 'male' or 'female'

    Returns:
        Dict: {
            'spouse_traits': str,  # 配偶特質
            'marriage_pattern': str,  # 婚姻模式
            'relationship_advice': List[str],  # 感情建議
            'marriage_timing': Dict,  # 結婚時機
            'compatibility_keys': List[str]  # 相處之道
        }
    """
    palaces_data = ziwei_data.get('palaces', {})
    marriage_palace = palaces_data.get('夫妻宮', {})
    major_stars = marriage_palace.get('major_stars', [])

    result = {
        'spouse_traits': '',
        'marriage_pattern': '',
        'relationship_advice': [],
        'marriage_timing': {},
        'compatibility_keys': []
    }

    # 配偶特質
    if major_stars:
        stars_str = '、'.join(major_stars)
        traits_intro = f"您的夫妻宮有 **{stars_str}**，"

        spouse_traits_map = {
            '紫微': '配偶可能較為尊貴、有地位，個性穩重有責任感',
            '天府': '配偶可能較為穩重、善於理財，重視家庭與安全感',
            '武曲': '配偶可能較為剛毅、有原則，理性務實但可能不夠浪漫',
            '天機': '配偶可能較為聰明、善變，重視心靈溝通',
            '太陽': '配偶可能較為開朗、熱情，樂於助人但可能較忙碌',
            '太陰': '配偶可能較為溫柔、細膩，重視家庭與情感',
            '天同': '配偶可能較為隨和、善良，重視生活品質',
            '廉貞': '配偶可能較為熱情、有魅力，但感情可能複雜',
            '貪狼': '配偶可能較為多才多藝、有魅力，但桃花可能多',
            '巨門': '配偶可能較為深沉、口才好，溝通是關鍵',
            '天相': '配偶可能較為隨和、有品味，善於協調',
            '天梁': '配偶可能較為成熟、有智慧，年紀可能較大',
            '七殺': '配偶可能較為剛強、有魄力，個性直接',
            '破軍': '配偶可能較為創新、善變，感情可能多變'
        }

        traits = [spouse_traits_map.get(star, '') for star in major_stars if star in spouse_traits_map]
        result['spouse_traits'] = traits_intro + '、'.join(traits) if traits else traits_intro + '需要通過相處了解配偶特質'

    # 婚姻模式
    stable_stars = ['紫微', '天府', '太陰', '天同', '天相', '天梁']
    dynamic_stars = ['廉貞', '貪狼', '七殺', '破軍']

    has_stable = any(star in major_stars for star in stable_stars)
    has_dynamic = any(star in major_stars for star in dynamic_stars)

    if has_stable:
        result['marriage_pattern'] = '婚姻較為穩定，重視家庭與承諾，離婚率較低。'
    elif has_dynamic:
        result['marriage_pattern'] = '婚姻可能較為波動，感情豐富但變化大，需要用心經營。'
    else:
        result['marriage_pattern'] = '婚姻模式需視其他因素而定，重要的是雙方用心經營。'

    # 感情建議
    result['relationship_advice'] = [
        '了解配偶的性格特質，互相包容',
        '重視溝通，避免誤會與衝突',
        '經營感情需要用心與智慧',
        '不要過度依賴或控制對方',
        '培養共同興趣與目標'
    ]

    # 結婚時機
    result['marriage_timing'] = {
        'early_marriage': '25歲前結婚，感情較為衝動，需要慎重',
        'suitable_age': '28-35歲是較為合適的結婚年齡，心智成熟',
        'late_marriage': '35歲後結婚，較為穩定成熟，但要注意生育'
    }

    # 相處之道
    result['compatibility_keys'] = [
        '互相尊重，給對方空間',
        '良好溝通，解決問題',
        '共同成長，支持對方',
        '保持浪漫，經營感情',
        '面對挑戰，共同面對'
    ]

    return result


# ============================================================================
# 導出函數 (Export Functions)
# ============================================================================

__all__ = [
    'interpret_ziwei_palaces',
    'analyze_four_transformations',
    'interpret_destiny_palace',
    'interpret_wealth_palace',
    'interpret_career_palace',
    'interpret_marriage_palace',
    'MAJOR_STAR_TRAITS',
    'STAR_COMBINATIONS',
    'FOUR_TRANSFORMATIONS'
]

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
心理占星學深度解釋引擎 (Psychological Astrology Interpretation Engine)

此模組提供心理占星學的深度解釋功能，將星盤數據轉化為心理層面的分析。

主要功能：
1. 個人行星心理分析（太陽、月亮、水星、金星、火星）
2. 宮位心理學解釋
3. 相位心理動力學分析
4. 整合性人格分析
5. 人生發展建議

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
    construct_astrology_area_prompt
)

# Load Astrology system prompt at module level
ASTROLOGY_SYSTEM_PROMPT = load_system_prompt('astrology_system_prompt.md') or ""


# ============================================================================
# 星座心理特質資料庫 (Zodiac Sign Psychology Database)
# ============================================================================

ZODIAC_PSYCHOLOGY = {
    '白羊座': {
        'name': '白羊座',
        'element': '火',
        'quality': '開創',
        'ruler': '火星',
        'core_archetype': '戰士、先鋒、開拓者',
        'psychological_essence': """
        白羊座代表純粹的自我意志與行動力。這是黃道第一個星座，象徵著生命的開始、
        自我的誕生與獨立意識的覺醒。白羊座的核心心理動力是「我要」、「我能」、「我做」。

        **核心心理特質**：
        - 強烈的自我意識與獨立性
        - 行動導向，想到就做
        - 勇於冒險，不怕失敗
        - 直接坦率，不拐彎抹角
        - 競爭意識強，喜歡第一

        **成長課題**：
        - 學習耐心與等待
        - 培養對他人感受的敏感度
        - 完成開始的事情（不要虎頭蛇尾）
        - 控制衝動，學習策略思考
        """,
        'strengths': ['勇敢', '直接', '有活力', '開創性', '行動力強'],
        'challenges': ['衝動', '缺乏耐心', '自我中心', '容易放棄'],
        'keywords': ['開創', '勇氣', '行動', '自我', '競爭']
    },

    '金牛座': {
        'name': '金牛座',
        'element': '土',
        'quality': '固定',
        'ruler': '金星',
        'core_archetype': '建設者、享受者、守護者',
        'psychological_essence': """
        金牛座代表物質安全感的追求與感官享受的需求。這個星座連結著我們對穩定、
        價值、美感與舒適的渴望。金牛座的核心心理動力是「我擁有」、「我珍惜」、「我建設」。

        **核心心理特質**：
        - 重視物質安全與穩定
        - 追求感官享受與美感
        - 持之以恆，耐力驚人
        - 務實可靠，腳踏實地
        - 價值觀明確，重視品質

        **成長課題**：
        - 學習放手與改變
        - 平衡物質與精神追求
        - 培養彈性與適應力
        - 避免過度固執與佔有
        """,
        'strengths': ['穩定', '可靠', '有耐心', '審美力強', '務實'],
        'challenges': ['固執', '抗拒改變', '過度物質化', '佔有欲強'],
        'keywords': ['穩定', '價值', '享受', '建設', '固執']
    },

    '雙子座': {
        'name': '雙子座',
        'element': '風',
        'quality': '變動',
        'ruler': '水星',
        'core_archetype': '傳訊者、學習者、連結者',
        'psychological_essence': """
        雙子座代表好奇心、溝通與資訊交流的需求。這個星座象徵著心智的靈活性、
        多樣性思維與人際連結。雙子座的核心心理動力是「我思考」、「我溝通」、「我連結」。

        **核心心理特質**：
        - 好奇心強，興趣廣泛
        - 溝通能力佳，善於表達
        - 思維靈活，適應力強
        - 喜歡學習與分享資訊
        - 多才多藝，但可能不夠專精

        **成長課題**：
        - 培養專注力與深度
        - 學習承諾與堅持
        - 整合多元興趣，找到核心
        - 從表面學習深入到真正理解
        """,
        'strengths': ['聰明', '靈活', '善於溝通', '適應力強', '多才多藝'],
        'challenges': ['不專注', '表面化', '多變', '缺乏深度'],
        'keywords': ['溝通', '好奇', '靈活', '多樣', '資訊']
    },

    '巨蟹座': {
        'name': '巨蟹座',
        'element': '水',
        'quality': '開創',
        'ruler': '月亮',
        'core_archetype': '養育者、保護者、情感守護者',
        'psychological_essence': """
        巨蟹座代表情感安全感、歸屬需求與養育本能。這個星座連結著我們內在的
        情感世界、家庭記憶與保護機制。巨蟹座的核心心理動力是「我感受」、「我照顧」、「我保護」。

        **核心心理特質**：
        - 情感豐富，同理心強
        - 重視家庭與歸屬感
        - 保護欲強，關懷他人
        - 直覺敏銳，情感細膩
        - 情緒波動，容易受傷

        **成長課題**：
        - 學習情緒界線與獨立
        - 不要過度保護或依賴
        - 接納情緒，但不被淹沒
        - 療癒童年創傷與家庭議題
        """,
        'strengths': ['同理心強', '關懷他人', '直覺敏銳', '忠誠', '情感豐富'],
        'challenges': ['情緒化', '依賴', '過度保護', '容易受傷'],
        'keywords': ['情感', '家庭', '養育', '保護', '歸屬']
    },

    '獅子座': {
        'name': '獅子座',
        'element': '火',
        'quality': '固定',
        'ruler': '太陽',
        'core_archetype': '國王、創造者、表演者',
        'psychological_essence': """
        獅子座代表創造力、自我表達與被認可的需求。這個星座象徵著生命力、
        自信與個人魅力的展現。獅子座的核心心理動力是「我創造」、「我發光」、「我被看見」。

        **核心心理特質**：
        - 自信有魅力，吸引他人
        - 創造力強，喜歡表現
        - 慷慨大方，重視尊嚴
        - 領導能力，天生王者氣質
        - 需要被認可與欣賞

        **成長課題**：
        - 學習謙遜，不要過度自戀
        - 接納不完美，允許失敗
        - 分享舞台，欣賞他人光芒
        - 內在自我認可，不依賴外在肯定
        """,
        'strengths': ['自信', '慷慨', '有創造力', '領導力強', '忠誠'],
        'challenges': ['自戀', '需要關注', '驕傲', '固執'],
        'keywords': ['創造', '表達', '自信', '領導', '認可']
    },

    '處女座': {
        'name': '處女座',
        'element': '土',
        'quality': '變動',
        'ruler': '水星',
        'core_archetype': '分析者、服務者、完美主義者',
        'psychological_essence': """
        處女座代表分析能力、服務精神與追求完美的傾向。這個星座連結著我們的
        實用智慧、健康意識與改善的動力。處女座的核心心理動力是「我分析」、「我改善」、「我服務」。

        **核心心理特質**：
        - 分析能力強，注重細節
        - 追求完美，標準高
        - 服務精神，樂於幫助
        - 實用主義，講求效率
        - 重視健康與秩序

        **成長課題**：
        - 接納不完美，學習放鬆
        - 不要過度批判自己與他人
        - 看見整體，不只是細節
        - 平衡服務與自我照顧
        """,
        'strengths': ['細心', '分析力強', '有服務精神', '實用', '追求完美'],
        'challenges': ['過度批判', '焦慮', '吹毛求疵', '難以放鬆'],
        'keywords': ['分析', '完美', '服務', '健康', '細節']
    },

    '天秤座': {
        'name': '天秤座',
        'element': '風',
        'quality': '開創',
        'ruler': '金星',
        'core_archetype': '外交官、藝術家、和平使者',
        'psychological_essence': """
        天秤座代表和諧、平衡與人際關係的需求。這個星座象徵著美感、公正與
        合作精神。天秤座的核心心理動力是「我平衡」、「我協調」、「我關聯」。

        **核心心理特質**：
        - 追求和諧與平衡
        - 審美觀強，品味佳
        - 善於社交，人際關係好
        - 公正客觀，能看多面
        - 重視伴侶與合作關係

        **成長課題**：
        - 學習做決定，不要過度猶豫
        - 建立自我認同，不依賴他人
        - 面對衝突，不逃避問題
        - 平衡自我與他人需求
        """,
        'strengths': ['和諧', '公正', '善於社交', '審美力強', '外交手腕'],
        'challenges': ['猶豫不決', '依賴他人', '逃避衝突', '缺乏主見'],
        'keywords': ['平衡', '和諧', '關係', '美感', '公正']
    },

    '天蠍座': {
        'name': '天蠍座',
        'element': '水',
        'quality': '固定',
        'ruler': '冥王星/火星',
        'core_archetype': '轉化者、深度探索者、煉金術士',
        'psychological_essence': """
        天蠍座代表深度、轉化與心理力量。這個星座連結著我們的潛意識、
        慾望與再生能力。天蠍座的核心心理動力是「我渴望」、「我轉化」、「我深入」。

        **核心心理特質**：
        - 情感強烈，直覺敏銳
        - 洞察力強，能看穿本質
        - 追求深度與真相
        - 轉化能力，能從危機中重生
        - 控制慾強，不輕易信任

        **成長課題**：
        - 學習信任與放手
        - 釋放控制，接納脆弱
        - 轉化負面情緒，不報復
        - 分享權力，建立親密關係
        """,
        'strengths': ['深刻', '洞察力強', '專注', '轉化能力強', '意志堅定'],
        'challenges': ['控制慾', '報復心', '不信任', '嫉妒'],
        'keywords': ['深度', '轉化', '權力', '親密', '再生']
    },

    '射手座': {
        'name': '射手座',
        'element': '火',
        'quality': '變動',
        'ruler': '木星',
        'core_archetype': '哲學家、探險家、導師',
        'psychological_essence': """
        射手座代表擴展、探索與尋求意義的需求。這個星座象徵著自由、
        樂觀與哲學思考。射手座的核心心理動力是「我探索」、「我理解」、「我相信」。

        **核心心理特質**：
        - 樂觀積極，充滿希望
        - 追求自由與冒險
        - 哲學思考，尋求意義
        - 誠實直率，坦白真誠
        - 視野廣闊，國際觀強

        **成長課題**：
        - 學習承諾與責任
        - 注意細節，不只看大局
        - 培養耐心，完成開始的事
        - 真誠但不魯莽，考慮他人感受
        """,
        'strengths': ['樂觀', '自由', '誠實', '有遠見', '哲學性'],
        'challenges': ['不負責任', '過度樂觀', '魯莽', '缺乏細節'],
        'keywords': ['探索', '自由', '意義', '樂觀', '擴展']
    },

    '摩羯座': {
        'name': '摩羯座',
        'element': '土',
        'quality': '開創',
        'ruler': '土星',
        'core_archetype': '建築師、權威、成就者',
        'psychological_essence': """
        摩羯座代表野心、責任與長期目標的追求。這個星座象徵著紀律、
        成熟與社會成就。摩羯座的核心心理動力是「我使用」、「我成就」、「我負責」。

        **核心心理特質**：
        - 野心大，追求成就
        - 責任感強，可靠穩重
        - 紀律嚴謹，自我要求高
        - 務實現實，長期規劃
        - 尊重傳統與權威

        **成長課題**：
        - 學習放鬆，享受過程
        - 不要過度嚴苛，接納不完美
        - 平衡工作與生活
        - 允許情感表達，不壓抑
        """,
        'strengths': ['負責任', '有野心', '紀律', '務實', '堅韌'],
        'challenges': ['過度嚴肅', '悲觀', '工作狂', '情感壓抑'],
        'keywords': ['成就', '責任', '野心', '紀律', '權威']
    },

    '水瓶座': {
        'name': '水瓶座',
        'element': '風',
        'quality': '固定',
        'ruler': '天王星/土星',
        'core_archetype': '革新者、人道主義者、未來主義者',
        'psychological_essence': """
        水瓶座代表創新、獨立與人道主義精神。這個星座連結著我們對自由、
        平等與未來願景的追求。水瓶座的核心心理動力是「我知道」、「我革新」、「我解放」。

        **核心心理特質**：
        - 獨立思考，不隨波逐流
        - 創新精神，追求改變
        - 人道主義，關心社會
        - 理性客觀，情感疏離
        - 重視友誼與團體

        **成長課題**：
        - 學習親密，不只是友誼
        - 接納情感，不只用理性
        - 實踐理想，不只是理論
        - 個人與群體的平衡
        """,
        'strengths': ['創新', '獨立', '人道', '理性', '友善'],
        'challenges': ['情感疏離', '叛逆', '不切實際', '固執己見'],
        'keywords': ['創新', '獨立', '人道', '未來', '自由']
    },

    '雙魚座': {
        'name': '雙魚座',
        'element': '水',
        'quality': '變動',
        'ruler': '海王星/木星',
        'core_archetype': '夢想家、神秘主義者、同理者',
        'psychological_essence': """
        雙魚座代表同理心、想像力與靈性連結。這個星座象徵著溶解邊界、
        無條件的愛與超越性體驗。雙魚座的核心心理動力是「我相信」、「我夢想」、「我融合」。

        **核心心理特質**：
        - 同理心強，能感受他人
        - 想像力豐富，藝術天分
        - 靈性傾向，追求超越
        - 適應力強，但缺乏界線
        - 理想主義，逃避現實

        **成長課題**：
        - 建立健康界線，不被淹沒
        - 面對現實，不逃避
        - 區分自己與他人的情感
        - 實踐夢想，不只是幻想
        """,
        'strengths': ['同理心', '想像力', '適應力', '靈性', '藝術性'],
        'challenges': ['缺乏界線', '逃避', '受害者心態', '不切實際'],
        'keywords': ['同理', '想像', '靈性', '融合', '超越']
    }
}


# ============================================================================
# 宮位心理學資料庫 (House Psychology Database)
# ============================================================================

HOUSE_PSYCHOLOGY = {
    1: {
        'name': '第一宮',
        'traditional_name': '命宮、上升',
        'life_area': '自我認同、外在形象、身體',
        'psychological_theme': '我是誰？我如何展現自己？',
        'essence': """
        第一宮代表自我意識的開始、個人身份與外在形象。這是「我」的誕生，
        是我們展現給世界的第一印象。第一宮連結著我們的身體、外貌、
        基本個性與自發性反應。

        **心理意義**：
        - 自我認同的建立
        - 個人意志的表達
        - 身體形象與健康
        - 初始反應模式
        - 人生態度與方向
        """
    },

    2: {
        'name': '第二宮',
        'traditional_name': '財帛宮',
        'life_area': '物質資源、價值觀、自我價值',
        'psychological_theme': '我擁有什麼？我的價值是什麼？',
        'essence': """
        第二宮代表物質安全感、個人資源與自我價值。這個宮位連結著我們對
        「擁有」的需求、金錢態度與內在價值感。

        **心理意義**：
        - 物質安全需求
        - 自我價值感
        - 金錢與資源態度
        - 才能與天賦
        - 感官享受需求
        """
    },

    3: {
        'name': '第三宮',
        'traditional_name': '兄弟宮',
        'life_area': '溝通、學習、近親',
        'psychological_theme': '我如何思考？我如何溝通？',
        'essence': """
        第三宮代表心智功能、溝通方式與基礎學習。這個宮位連結著我們的
        思維模式、語言能力與日常互動。

        **心理意義**：
        - 思維與溝通模式
        - 學習風格與好奇心
        - 手足與近親關係
        - 日常環境適應
        - 資訊處理方式
        """
    },

    4: {
        'name': '第四宮',
        'traditional_name': '田宅宮、天底',
        'life_area': '家庭、根源、內在安全',
        'psychological_theme': '我的根在哪裡？什麼給我安全感？',
        'essence': """
        第四宮代表家庭根源、內在安全與情感基礎。這個宮位連結著我們的
        童年記憶、家庭模式與內心深處的情感需求。

        **心理意義**：
        - 家庭背景與童年
        - 情感安全需求
        - 內在自我與私密性
        - 根源與歸屬感
        - 晚年生活基調
        """
    },

    5: {
        'name': '第五宮',
        'traditional_name': '子女宮',
        'life_area': '創造力、戀愛、自我表達',
        'psychological_theme': '我如何創造？我如何表達喜悅？',
        'essence': """
        第五宮代表創造力、自我表達與喜悅追求。這個宮位連結著我們的
        創意、戀愛、遊戲與子女。

        **心理意義**：
        - 創造力與自我表達
        - 戀愛與浪漫
        - 遊戲與娛樂
        - 子女與內在孩童
        - 生命喜悅的追求
        """
    },

    6: {
        'name': '第六宮',
        'traditional_name': '奴僕宮',
        'life_area': '工作、健康、日常服務',
        'psychological_theme': '我如何服務？我如何照顧身體？',
        'essence': """
        第六宮代表日常工作、健康習慣與服務精神。這個宮位連結著我們的
        工作態度、健康意識與自我改善。

        **心理意義**：
        - 工作態度與技能
        - 健康習慣與身心連結
        - 服務精神與助人
        - 日常例行與秩序
        - 自我完善的動力
        """
    },

    7: {
        'name': '第七宮',
        'traditional_name': '夫妻宮、下降',
        'life_area': '伴侶、合作、一對一關係',
        'psychological_theme': '我如何關聯他人？我需要什麼樣的伴侶？',
        'essence': """
        第七宮代表伴侶關係、合作與一對一互動。這個宮位連結著我們對
        「他者」的需求、投射與親密關係模式。

        **心理意義**：
        - 伴侶需求與模式
        - 合作與妥協能力
        - 投射與陰影
        - 一對一關係動力
        - 平衡自我與他人
        """
    },

    8: {
        'name': '第八宮',
        'traditional_name': '疾厄宮',
        'life_area': '轉化、親密、共享資源',
        'psychological_theme': '我如何轉化？什麼讓我重生？',
        'essence': """
        第八宮代表深度轉化、親密連結與共享資源。這個宮位連結著我們的
        潛意識、慾望、死亡與再生。

        **心理意義**：
        - 深度轉化與重生
        - 親密與性
        - 權力與控制議題
        - 共享資源與遺產
        - 潛意識與陰影
        """
    },

    9: {
        'name': '第九宮',
        'traditional_name': '遷移宮',
        'life_area': '哲學、旅行、高等教育',
        'psychological_theme': '我相信什麼？生命的意義是什麼？',
        'essence': """
        第九宮代表哲學信念、意義追求與視野擴展。這個宮位連結著我們的
        信仰、高等學習與遠方旅行。

        **心理意義**：
        - 哲學與信仰系統
        - 生命意義的追求
        - 高等教育與智慧
        - 遠行與文化探索
        - 視野的擴展
        """
    },

    10: {
        'name': '第十宮',
        'traditional_name': '官祿宮、天頂',
        'life_area': '事業、社會地位、成就',
        'psychological_theme': '我的使命是什麼？我想成為什麼？',
        'essence': """
        第十宮代表事業成就、社會地位與人生目標。這個宮位連結著我們的
        野心、公眾形象與對成功的定義。

        **心理意義**：
        - 事業目標與野心
        - 社會地位與聲譽
        - 權威與責任
        - 人生使命
        - 公眾形象
        """
    },

    11: {
        'name': '第十一宮',
        'traditional_name': '福德宮',
        'life_area': '友誼、團體、理想',
        'psychological_theme': '我屬於哪個群體？我的理想是什麼？',
        'essence': """
        第十一宮代表友誼、團體歸屬與未來願景。這個宮位連結著我們的
        社交網絡、集體理想與人道關懷。

        **心理意義**：
        - 友誼與社交網絡
        - 團體歸屬與貢獻
        - 理想與未來願景
        - 人道關懷
        - 個人與集體的整合
        """
    },

    12: {
        'name': '第十二宮',
        'traditional_name': '相貌宮',
        'life_area': '潛意識、靈性、隱藏',
        'psychological_theme': '什麼是我未知的？我如何超越自我？',
        'essence': """
        第十二宮代表潛意識、靈性與超越。這個宮位連結著我們的隱藏面、
        集體無意識與靈性追求。

        **心理意義**：
        - 潛意識與夢境
        - 靈性與超越性
        - 隱藏與犧牲
        - 業力與前世
        - 溶解邊界與合一
        """
    }
}


# ============================================================================
# 相位心理動力學資料庫 (Aspect Psychology Database)
# ============================================================================

ASPECT_PSYCHOLOGY = {
    'conjunction': {
        'name': '合相',
        'angle': 0,
        'orb': 8,
        'nature': '融合',
        'psychological_dynamic': """
        合相代表兩個行星能量的完全融合。這是最強烈的相位，兩個原型
        無法分離，必須學習整合。合相可以帶來強大的力量，但也可能造成
        能量混亂，需要有意識地整合兩種能量。

        **心理意義**：
        - 能量完全融合
        - 無法分離的組合
        - 強大但可能混亂
        - 需要有意識整合
        """
    },

    'opposition': {
        'name': '對分相',
        'angle': 180,
        'orb': 8,
        'nature': '極性張力',
        'psychological_dynamic': """
        對分相代表兩個行星能量的極性張力。這個相位創造出「非此即彼」
        的動力，容易投射或搖擺於兩極。成長的關鍵在於整合兩極，
        找到平衡點，而非選擇其一。

        **心理意義**：
        - 極性張力與衝突
        - 投射與搖擺
        - 需要整合平衡
        - 對立中見互補
        """
    },

    'square': {
        'name': '刑相位',
        'angle': 90,
        'orb': 7,
        'nature': '動態張力',
        'psychological_dynamic': """
        刑相位代表內在張力與挑戰。這個相位帶來摩擦與不適，驅使我們
        行動與改變。刑相位是成長的催化劑，雖然痛苦但能帶來突破。
        關鍵是將張力轉化為建設性的行動。

        **心理意義**：
        - 內在張力與摩擦
        - 成長的催化劑
        - 挑戰與突破
        - 需要行動與改變
        """
    },

    'trine': {
        'name': '拱相位',
        'angle': 120,
        'orb': 7,
        'nature': '和諧流動',
        'psychological_dynamic': """
        拱相位代表和諧與天賦。這個相位帶來輕鬆流動的能量，事情似乎
        自然而然就發生。但過度和諧可能造成懶散，需要有意識地發揮
        這些天賦，而非視為理所當然。

        **心理意義**：
        - 和諧流動的能量
        - 天賦與才能
        - 輕鬆但可能懶散
        - 需要有意識發揮
        """
    },

    'sextile': {
        'name': '六分相',
        'angle': 60,
        'orb': 6,
        'nature': '機會',
        'psychological_dynamic': """
        六分相代表機會與潛能。這個相位比拱相位更需要主動，能量不會
        自動展現，需要我們去把握機會。六分相提供成長的可能性，
        但需要努力才能實現。

        **心理意義**：
        - 機會與潛能
        - 需要主動把握
        - 成長的可能性
        - 努力才能實現
        """
    }
}


# ============================================================================
# 主要解釋函數 (Main Interpretation Functions)
# ============================================================================

def interpret_natal_chart(astrology_data: Dict) -> Dict:
    """心理占星學星盤深度解釋（LLM增強版）

    Args:
        astrology_data: Astrology calculator output

    Returns:
        Dict: {
            'psychological_profile': Dict,  # 心理特質分析
            'aspect_dynamics': List[Dict],  # 相位動力學
            'life_path_analysis': Dict,  # 人生道路分析
            'integration_guidance': List[str],  # 整合指引
            'confidence_level': Dict,  # 信心度評估
            'llm_analysis': str (optional)  # LLM深度分析
        }
    """
    # Try LLM analysis with fallback
    llm_analyzer = get_llm_analyzer()

    if llm_analyzer.is_available() and ASTROLOGY_SYSTEM_PROMPT:
        # For comprehensive chart analysis
        analysis_prompt = construct_astrology_area_prompt('綜合星盤分析', astrology_data)

        llm_result = llm_analyzer.analyze_with_fallback(
            system_prompt=ASTROLOGY_SYSTEM_PROMPT,
            analysis_prompt=analysis_prompt,
            fallback_func=_traditional_natal_chart_analysis,
            fallback_args=(astrology_data,),
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

            traditional_result = _traditional_natal_chart_analysis(astrology_data)
            traditional_result['llm_analysis'] = llm_result
            traditional_result['confidence_level'] = confidence
            traditional_result['analysis_method'] = 'LLM enhanced'
            return traditional_result
        elif isinstance(llm_result, dict):
            # Fallback was already executed, return it directly
            return llm_result

    return _traditional_natal_chart_analysis(astrology_data)


def _traditional_natal_chart_analysis(astrology_data: Dict) -> Dict:
    """傳統占星分析"""
    planets = astrology_data.get('planets', {})
    aspects = astrology_data.get('aspects', [])
    houses = astrology_data.get('houses', {})

    confidence = calculate_confidence_level(
        consensus_indicators=1,
        total_indicators=1,
        data_quality=1.0,
        theoretical_support=0.8
    )

    result = {
        'psychological_profile': _analyze_psychological_profile(planets, houses),
        'aspect_dynamics': _analyze_aspect_dynamics(aspects, planets),
        'life_path_analysis': _analyze_life_path(planets, houses),
        'integration_guidance': _generate_integration_guidance(planets, aspects, houses),
        'confidence_level': confidence,
        'analysis_method': 'Traditional rule-based'
    }

    return result


def _analyze_psychological_profile(planets: Dict, houses: Dict) -> Dict:
    """分析心理特質"""
    profile = {}

    # 太陽：核心自我
    if 'Sun' in planets:
        profile['sun_psychology'] = _interpret_sun_psychology(planets['Sun'], houses)

    # 月亮：情感需求
    if 'Moon' in planets:
        profile['moon_psychology'] = _interpret_moon_psychology(planets['Moon'], houses)

    # 水星：思維溝通
    if 'Mercury' in planets:
        profile['mercury_psychology'] = _interpret_mercury_psychology(planets['Mercury'], houses)

    # 金星：愛與價值
    if 'Venus' in planets:
        profile['venus_psychology'] = _interpret_venus_psychology(planets['Venus'], houses)

    # 火星：行動慾望
    if 'Mars' in planets:
        profile['mars_psychology'] = _interpret_mars_psychology(planets['Mars'], houses)

    return profile


def _interpret_sun_psychology(sun_data: Dict, houses: Dict) -> Dict:
    """太陽心理學解釋"""
    sign = sun_data.get('sign', '')
    house = sun_data.get('house', 1)

    sign_psych = ZODIAC_PSYCHOLOGY.get(sign, {})
    house_psych = HOUSE_PSYCHOLOGY.get(house, {})

    return {
        'sign': sign,
        'house': house,
        'detailed_interpretation': f"""
        ## 太陽在{sign}第{house}宮：核心自我與人生目標

        太陽代表您的核心自我、生命力與人生目標。太陽落在{sign}第{house}宮，
        顯示您的人生主軸是「{house_psych.get('psychological_theme', '')}」。

        **{sign}太陽核心特質**：
        {sign_psych.get('psychological_essence', '')}

        **第{house}宮的影響**：
        {house_psych.get('essence', '')}

        **綜合解讀**：
        您的太陽在{sign}強調{', '.join(sign_psych.get('keywords', [])[:3])}的特質，
        而落入第{house}宮則將這些能量導向{house_psych.get('life_area', '')}領域。
        您的人生使命與{house_psych.get('traditional_name', '')}的主題密切相關。

        **人生建議**：
        - 發揮{sign}的優勢：{', '.join(sign_psych.get('strengths', [])[:3])}
        - 克服{sign}的挑戰：{', '.join(sign_psych.get('challenges', [])[:2])}
        - 在{house_psych.get('life_area', '')}領域實現自我
        """,
        'life_purpose': f"通過{house_psych.get('life_area', '')}領域，展現{sign}的核心特質",
        'success_pattern': f"{sign}風格的成功模式",
        'shadow_work': f"需要克服{sign}的陰影面：{', '.join(sign_psych.get('challenges', [])[:2])}"
    }


def _interpret_moon_psychology(moon_data: Dict, houses: Dict) -> Dict:
    """月亮心理學解釋"""
    sign = moon_data.get('sign', '')
    house = moon_data.get('house', 1)

    sign_psych = ZODIAC_PSYCHOLOGY.get(sign, {})
    house_psych = HOUSE_PSYCHOLOGY.get(house, {})

    return {
        'sign': sign,
        'house': house,
        'detailed_interpretation': f"""
        ## 月亮在{sign}第{house}宮：情感需求與內在安全感

        月亮代表您的情感需求、內在安全感與潛意識反應。月亮落在{sign}第{house}宮，
        顯示您的情感世界與{house_psych.get('life_area', '')}密切相關。

        **{sign}月亮特質**：
        {sign_psych.get('psychological_essence', '')}

        **第{house}宮的影響**：
        月亮在第{house}宮讓情感需求聚焦在{house_psych.get('psychological_theme', '')}

        **情感需求**：
        您需要通過{house_psych.get('life_area', '')}來獲得情感滿足與安全感。
        {sign}月亮的您，在情感上{sign_psych.get('psychological_essence', '')[:100]}

        **人生建議**：
        - 認識並滿足自己的情感需求
        - 在{house_psych.get('life_area', '')}領域建立安全感
        - 允許自己展現{sign}月亮的情感特質
        - 照顧好內在的情緒世界
        """,
        'emotional_needs': f"{sign}風格的情感需求，聚焦在{house_psych.get('life_area', '')}",
        'relationship_style': f"{sign}月亮的情感表達與關係模式",
        'self_care': f"通過{house_psych.get('life_area', '')}進行情感照顧"
    }


def _interpret_mercury_psychology(mercury_data: Dict, houses: Dict) -> Dict:
    """水星心理學解釋"""
    sign = mercury_data.get('sign', '')
    house = mercury_data.get('house', 1)

    return {
        'sign': sign,
        'house': house,
        'communication_style': f"{sign}風格的思維與溝通",
        'learning_pattern': f"通過{sign}的方式學習與理解",
        'mental_strengths': f"{sign}水星的心智優勢"
    }


def _interpret_venus_psychology(venus_data: Dict, houses: Dict) -> Dict:
    """金星心理學解釋"""
    sign = venus_data.get('sign', '')
    house = venus_data.get('house', 1)

    return {
        'sign': sign,
        'house': house,
        'love_style': f"{sign}風格的愛與關係",
        'value_system': f"{sign}金星的價值觀",
        'aesthetic_preference': f"{sign}的審美與品味"
    }


def _interpret_mars_psychology(mars_data: Dict, houses: Dict) -> Dict:
    """火星心理學解釋"""
    sign = mars_data.get('sign', '')
    house = mars_data.get('house', 1)

    return {
        'sign': sign,
        'house': house,
        'action_pattern': f"{sign}風格的行動與慾望",
        'assertiveness_style': f"{sign}火星的自我主張",
        'energy_expression': f"{sign}的能量表達方式"
    }


def _analyze_aspect_dynamics(aspects: List[Dict], planets: Dict) -> List[Dict]:
    """分析相位動力學"""
    dynamics = []

    for aspect in aspects:
        planet1 = aspect.get('planet1', '')
        planet2 = aspect.get('planet2', '')
        aspect_type = aspect.get('type', '')

        aspect_psych = ASPECT_PSYCHOLOGY.get(aspect_type, {})

        if aspect_psych:
            dynamics.append({
                'aspect': f"{planet1} {aspect_psych.get('name', '')} {planet2}",
                'angle': aspect_psych.get('angle', 0),
                'interpretation': f"""
                ## {planet1} {aspect_psych.get('name', '')} {planet2}

                {aspect_psych.get('psychological_dynamic', '')}

                這個相位將{planet1}與{planet2}的能量以{aspect_psych.get('nature', '')}的方式連結。
                """,
                'integration_tip': f"整合{planet1}與{planet2}的能量"
            })

    return dynamics


def _analyze_life_path(planets: Dict, houses: Dict) -> Dict:
    """分析人生道路"""
    return {
        'core_identity': '基於太陽與上升的核心身份',
        'emotional_foundation': '基於月亮的情感基礎',
        'life_direction': '基於宮位配置的人生方向',
        'karmic_lessons': '基於土星與南北交點的業力課題'
    }


def _generate_integration_guidance(planets: Dict, aspects: List[Dict], houses: Dict) -> List[str]:
    """生成整合指引"""
    return [
        '認識並接納星盤中的所有能量',
        '整合相位帶來的張力與挑戰',
        '在生活中有意識地實踐星盤的智慧',
        '將困難相位轉化為成長的動力',
        '發揮和諧相位的天賦與才能'
    ]


# ============================================================================
# 導出函數 (Export Functions)
# ============================================================================

__all__ = [
    'interpret_natal_chart',
    'ZODIAC_PSYCHOLOGY',
    'HOUSE_PSYCHOLOGY',
    'ASPECT_PSYCHOLOGY'
]

"""
梅花易數計算模組 (Plum Blossom Numerology Calculator)
基於《易經》64卦的占卜系統
"""

from datetime import datetime
from typing import Dict, List, Any, Tuple


class PlumBlossomCalculator:
    """梅花易數計算器"""

    # 八卦基本屬性
    BAGUA = {
        1: {"name": "乾", "wuxing": "金", "nature": "天", "symbol": "☰", "attribute": "剛健"},
        2: {"name": "兌", "wuxing": "金", "nature": "澤", "symbol": "☱", "attribute": "喜悅"},
        3: {"name": "離", "wuxing": "火", "nature": "火", "symbol": "☲", "attribute": "光明"},
        4: {"name": "震", "wuxing": "木", "nature": "雷", "symbol": "☳", "attribute": "震動"},
        5: {"name": "巽", "wuxing": "木", "nature": "風", "symbol": "☴", "attribute": "入"},
        6: {"name": "坎", "wuxing": "水", "nature": "水", "symbol": "☵", "attribute": "險陷"},
        7: {"name": "艮", "wuxing": "土", "nature": "山", "symbol": "☶", "attribute": "止"},
        8: {"name": "坤", "wuxing": "土", "nature": "地", "symbol": "☷", "attribute": "柔順"}
    }

    # 64卦卦名和卦辭
    HEXAGRAMS = {
        (1, 1): {"name": "乾為天", "num": 1, "desc": "元亨利貞", "meaning": "純陽之卦，大吉大利"},
        (1, 2): {"name": "天澤履", "num": 10, "desc": "履虎尾，不咥人", "meaning": "行事需謹慎"},
        (1, 3): {"name": "天火同人", "num": 13, "desc": "同人于野", "meaning": "團結合作"},
        (1, 4): {"name": "天雷無妄", "num": 25, "desc": "無妄之災", "meaning": "順其自然"},
        (1, 5): {"name": "天風姤", "num": 44, "desc": "女壯，勿用取女", "meaning": "邪不壓正"},
        (1, 6): {"name": "天水訟", "num": 6, "desc": "有孚窒惕，中吉", "meaning": "爭訟不利"},
        (1, 7): {"name": "天山遯", "num": 33, "desc": "小利貞", "meaning": "退守為吉"},
        (1, 8): {"name": "天地否", "num": 12, "desc": "否之匪人", "meaning": "閉塞不通"},

        (2, 1): {"name": "澤天夬", "num": 43, "desc": "揚于王庭", "meaning": "決斷果敢"},
        (2, 2): {"name": "兌為澤", "num": 58, "desc": "亨，利貞", "meaning": "喜悅和悅"},
        (2, 3): {"name": "澤火革", "num": 49, "desc": "巳日乃孚", "meaning": "變革創新"},
        (2, 4): {"name": "澤雷隨", "num": 17, "desc": "元亨利貞", "meaning": "追隨順從"},
        (2, 5): {"name": "澤風大過", "num": 28, "desc": "棟撓，利有攸往", "meaning": "非常時期"},
        (2, 6): {"name": "澤水困", "num": 47, "desc": "亨，貞大人吉", "meaning": "困境考驗"},
        (2, 7): {"name": "澤山咸", "num": 31, "desc": "取女吉", "meaning": "感應相通"},
        (2, 8): {"name": "澤地萃", "num": 45, "desc": "亨，王假有廟", "meaning": "聚集會合"},

        (3, 1): {"name": "火天大有", "num": 14, "desc": "元亨", "meaning": "豐收大成"},
        (3, 2): {"name": "火澤睽", "num": 38, "desc": "小事吉", "meaning": "乖違相背"},
        (3, 3): {"name": "離為火", "num": 30, "desc": "利貞，亨", "meaning": "光明附麗"},
        (3, 4): {"name": "火雷噬嗑", "num": 21, "desc": "亨，利用獄", "meaning": "啟明除障"},
        (3, 5): {"name": "火風鼎", "num": 50, "desc": "元吉，亨", "meaning": "革故鼎新"},
        (3, 6): {"name": "火水未濟", "num": 64, "desc": "亨，小狐汔濟", "meaning": "未完成事"},
        (3, 7): {"name": "火山旅", "num": 56, "desc": "小亨", "meaning": "旅途漂泊"},
        (3, 8): {"name": "火地晉", "num": 35, "desc": "康侯用錫馬蕃庶", "meaning": "光明進展"},

        (4, 1): {"name": "雷天大壯", "num": 34, "desc": "利貞", "meaning": "剛健壯盛"},
        (4, 2): {"name": "雷澤歸妹", "num": 54, "desc": "征凶，無攸利", "meaning": "婚姻謹慎"},
        (4, 3): {"name": "雷火豐", "num": 55, "desc": "亨，王假之", "meaning": "豐盛充滿"},
        (4, 4): {"name": "震為雷", "num": 51, "desc": "亨，震來虩虩", "meaning": "震動警覺"},
        (4, 5): {"name": "雷風恆", "num": 32, "desc": "亨，無咎，利貞", "meaning": "恆久持久"},
        (4, 6): {"name": "雷水解", "num": 40, "desc": "利西南", "meaning": "解除困難"},
        (4, 7): {"name": "雷山小過", "num": 62, "desc": "亨，利貞", "meaning": "小事可為"},
        (4, 8): {"name": "雷地豫", "num": 16, "desc": "利建侯行師", "meaning": "歡樂和順"},

        (5, 1): {"name": "風天小畜", "num": 9, "desc": "亨", "meaning": "小有積蓄"},
        (5, 2): {"name": "風澤中孚", "num": 61, "desc": "豚魚吉", "meaning": "誠信中正"},
        (5, 3): {"name": "風火家人", "num": 37, "desc": "利女貞", "meaning": "家庭和睦"},
        (5, 4): {"name": "風雷益", "num": 42, "desc": "利有攸往", "meaning": "增益得利"},
        (5, 5): {"name": "巽為風", "num": 57, "desc": "小亨，利有攸往", "meaning": "謙遜順從"},
        (5, 6): {"name": "風水渙", "num": 59, "desc": "亨，王假有廟", "meaning": "渙散離散"},
        (5, 7): {"name": "風山漸", "num": 53, "desc": "女歸吉", "meaning": "循序漸進"},
        (5, 8): {"name": "風地觀", "num": 20, "desc": "盥而不薦", "meaning": "觀察省思"},

        (6, 1): {"name": "水天需", "num": 5, "desc": "有孚，光亨", "meaning": "需要等待"},
        (6, 2): {"name": "水澤節", "num": 60, "desc": "亨，苦節不可貞", "meaning": "節制適度"},
        (6, 3): {"name": "水火既濟", "num": 63, "desc": "亨小，利貞", "meaning": "功成圓滿"},
        (6, 4): {"name": "水雷屯", "num": 3, "desc": "元亨利貞", "meaning": "萬事起頭難"},
        (6, 5): {"name": "水風井", "num": 48, "desc": "改邑不改井", "meaning": "井水長流"},
        (6, 6): {"name": "坎為水", "num": 29, "desc": "習坎，有孚", "meaning": "重險疊難"},
        (6, 7): {"name": "水山蹇", "num": 39, "desc": "利西南", "meaning": "艱難險阻"},
        (6, 8): {"name": "水地比", "num": 8, "desc": "吉，原筮", "meaning": "親附輔助"},

        (7, 1): {"name": "山天大畜", "num": 26, "desc": "利貞，不家食吉", "meaning": "積蓄力量"},
        (7, 2): {"name": "山澤損", "num": 41, "desc": "有孚，元吉", "meaning": "減損謹慎"},
        (7, 3): {"name": "山火賁", "num": 22, "desc": "亨，小利有攸往", "meaning": "文飾美化"},
        (7, 4): {"name": "山雷頤", "num": 27, "desc": "貞吉", "meaning": "養生養賢"},
        (7, 5): {"name": "山風蠱", "num": 18, "desc": "元亨，利涉大川", "meaning": "革除積弊"},
        (7, 6): {"name": "山水蒙", "num": 4, "desc": "亨，匪我求童蒙", "meaning": "啟蒙教育"},
        (7, 7): {"name": "艮為山", "num": 52, "desc": "艮其背", "meaning": "止而不動"},
        (7, 8): {"name": "山地剝", "num": 23, "desc": "不利有攸往", "meaning": "剝落衰敗"},

        (8, 1): {"name": "地天泰", "num": 11, "desc": "小往大來", "meaning": "通泰吉祥"},
        (8, 2): {"name": "地澤臨", "num": 19, "desc": "元亨利貞", "meaning": "君臨天下"},
        (8, 3): {"name": "地火明夷", "num": 36, "desc": "利艱貞", "meaning": "光明受傷"},
        (8, 4): {"name": "地雷復", "num": 24, "desc": "亨，出入無疾", "meaning": "復歸本位"},
        (8, 5): {"name": "地風升", "num": 46, "desc": "元亨", "meaning": "上升發展"},
        (8, 6): {"name": "地水師", "num": 7, "desc": "貞，丈人吉", "meaning": "統帥之道"},
        (8, 7): {"name": "地山謙", "num": 15, "desc": "亨，君子有終", "meaning": "謙虛謹慎"},
        (8, 8): {"name": "坤為地", "num": 2, "desc": "元亨，利牝馬之貞", "meaning": "純陰柔順"}
    }

    def __init__(self, birth_datetime: datetime, method: str = "time"):
        """
        初始化梅花易數計算器

        Args:
            birth_datetime: 出生時間
            method: 起卦方法 ("time" 時間起卦, "number" 數字起卦)
        """
        self.birth_datetime = birth_datetime
        self.method = method

    def get_gua_by_time(self, dt: datetime) -> Tuple[int, int, int]:
        """
        時間起卦法

        Args:
            dt: 日期時間

        Returns:
            (上卦數, 下卦數, 動爻數)
        """
        # 年月日時的數字
        year = dt.year
        month = dt.month
        day = dt.day
        hour = dt.hour

        # 將時辰轉換為地支序數（1-12）
        hour_branch = ((hour + 1) // 2) % 12
        if hour_branch == 0:
            hour_branch = 12

        # 上卦：年數 + 月數 + 日數，除以8取餘
        upper = (year + month + day) % 8
        if upper == 0:
            upper = 8

        # 下卦：年數 + 月數 + 日數 + 時辰數，除以8取餘
        lower = (year + month + day + hour_branch) % 8
        if lower == 0:
            lower = 8

        # 動爻：年數 + 月數 + 日數 + 時辰數，除以6取餘
        changing_line = (year + month + day + hour_branch) % 6
        if changing_line == 0:
            changing_line = 6

        return upper, lower, changing_line

    def get_gua_by_number(self, num1: int, num2: int) -> Tuple[int, int, int]:
        """
        數字起卦法（可用於其他隨機起卦）

        Args:
            num1: 第一個數字（用於上卦）
            num2: 第二個數字（用於下卦）

        Returns:
            (上卦數, 下卦數, 動爻數)
        """
        upper = num1 % 8
        if upper == 0:
            upper = 8

        lower = num2 % 8
        if lower == 0:
            lower = 8

        changing_line = (num1 + num2) % 6
        if changing_line == 0:
            changing_line = 6

        return upper, lower, changing_line

    def get_hexagram_info(self, upper: int, lower: int) -> Dict[str, Any]:
        """
        獲取卦象資訊

        Args:
            upper: 上卦數
            lower: 下卦數

        Returns:
            卦象詳細資訊
        """
        if (upper, lower) in self.HEXAGRAMS:
            hex_info = self.HEXAGRAMS[(upper, lower)]
        else:
            # 如果沒有定義，返回基本資訊
            hex_info = {
                "name": f"{self.BAGUA[upper]['name']}{self.BAGUA[lower]['name']}",
                "desc": "待解析",
                "meaning": "此卦組合需進一步分析"
            }

        return {
            "name": hex_info["name"],
            "upper_gua": self.BAGUA[upper],
            "lower_gua": self.BAGUA[lower],
            "description": hex_info["desc"],
            "meaning": hex_info["meaning"],
            "upper_symbol": self.BAGUA[upper]["symbol"],
            "lower_symbol": self.BAGUA[lower]["symbol"],
            "full_symbol": f"{self.BAGUA[upper]['symbol']}\n{self.BAGUA[lower]['symbol']}"
        }

    def get_changing_hexagram(self, upper: int, lower: int, changing_line: int) -> Dict[str, Any]:
        """
        計算變卦（動爻變化後的卦象）

        Args:
            upper: 原卦上卦
            lower: 原卦下卦
            changing_line: 動爻位置（1-6，從下往上數）

        Returns:
            變卦資訊
        """
        # 確定動爻在上卦還是下卦
        if changing_line <= 3:
            # 動爻在下卦
            # 簡化處理：根據動爻位置轉換下卦
            new_lower = (lower + changing_line - 1) % 8
            if new_lower == 0:
                new_lower = 8
            new_upper = upper
        else:
            # 動爻在上卦
            new_upper = (upper + (changing_line - 3) - 1) % 8
            if new_upper == 0:
                new_upper = 8
            new_lower = lower

        return self.get_hexagram_info(new_upper, new_lower)

    def analyze_wuxing_relation(self, gua1_wuxing: str, gua2_wuxing: str) -> Dict[str, str]:
        """
        分析兩卦之間的五行生剋關係
        """
        sheng = {
            "木": "火", "火": "土", "土": "金", "金": "水", "水": "木"
        }
        ke = {
            "木": "土", "土": "水", "水": "火", "火": "金", "金": "木"
        }

        if sheng.get(gua1_wuxing) == gua2_wuxing:
            return {
                "relation": "相生",
                "effect": "吉",
                "description": f"{gua1_wuxing}生{gua2_wuxing}，上下和諧，吉利之象"
            }
        elif ke.get(gua1_wuxing) == gua2_wuxing:
            return {
                "relation": "相剋",
                "effect": "凶",
                "description": f"{gua1_wuxing}剋{gua2_wuxing}，上克下，需謹慎行事"
            }
        elif sheng.get(gua2_wuxing) == gua1_wuxing:
            return {
                "relation": "被生",
                "effect": "吉",
                "description": f"{gua2_wuxing}生{gua1_wuxing}，下生上，得助力"
            }
        elif ke.get(gua2_wuxing) == gua1_wuxing:
            return {
                "relation": "被剋",
                "effect": "凶",
                "description": f"{gua2_wuxing}剋{gua1_wuxing}，下克上，有逆境"
            }
        elif gua1_wuxing == gua2_wuxing:
            return {
                "relation": "比和",
                "effect": "平",
                "description": f"五行相同，力量加倍，平穩發展"
            }
        else:
            return {
                "relation": "無特殊關係",
                "effect": "平",
                "description": "五行無直接生剋，需綜合判斷"
            }

    def analyze(self) -> Dict[str, Any]:
        """
        執行完整的梅花易數分析

        Returns:
            完整的卦象分析結果
        """
        # 根據方法起卦
        if self.method == "time":
            upper, lower, changing_line = self.get_gua_by_time(self.birth_datetime)
        else:
            # 默認使用時間數字
            num1 = self.birth_datetime.year + self.birth_datetime.month
            num2 = self.birth_datetime.day + self.birth_datetime.hour
            upper, lower, changing_line = self.get_gua_by_number(num1, num2)

        # 獲取本卦資訊
        ben_gua = self.get_hexagram_info(upper, lower)

        # 獲取變卦資訊
        bian_gua = self.get_changing_hexagram(upper, lower, changing_line)

        # 分析五行關係
        wuxing_relation = self.analyze_wuxing_relation(
            ben_gua["upper_gua"]["wuxing"],
            ben_gua["lower_gua"]["wuxing"]
        )

        # 分析動爻含義
        yao_positions = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"]
        changing_yao_desc = f"第{changing_line}爻（{yao_positions[changing_line-1]}）發動"

        # 綜合判斷
        if wuxing_relation["effect"] == "吉":
            overall_luck = "吉"
        elif wuxing_relation["effect"] == "凶":
            overall_luck = "凶"
        else:
            overall_luck = "平"

        return {
            "divination_time": self.birth_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "method": "時間起卦" if self.method == "time" else "數字起卦",
            "ben_gua": {
                "name": ben_gua["name"],
                "upper": {
                    "number": upper,
                    "name": ben_gua["upper_gua"]["name"],
                    "wuxing": ben_gua["upper_gua"]["wuxing"],
                    "nature": ben_gua["upper_gua"]["nature"],
                    "symbol": ben_gua["upper_symbol"],
                    "attribute": ben_gua["upper_gua"]["attribute"]
                },
                "lower": {
                    "number": lower,
                    "name": ben_gua["lower_gua"]["name"],
                    "wuxing": ben_gua["lower_gua"]["wuxing"],
                    "nature": ben_gua["lower_gua"]["nature"],
                    "symbol": ben_gua["lower_symbol"],
                    "attribute": ben_gua["lower_gua"]["attribute"]
                },
                "description": ben_gua["description"],
                "meaning": ben_gua["meaning"],
                "symbol": ben_gua["full_symbol"]
            },
            "changing_line": {
                "position": changing_line,
                "description": changing_yao_desc,
                "yao_name": yao_positions[changing_line-1]
            },
            "bian_gua": {
                "name": bian_gua["name"],
                "description": bian_gua["description"],
                "meaning": bian_gua["meaning"],
                "symbol": bian_gua["full_symbol"]
            },
            "wuxing_analysis": wuxing_relation,
            "overall_judgment": {
                "luck": overall_luck,
                "summary": f"本卦為{ben_gua['name']}，{ben_gua['meaning']}。動爻為{changing_yao_desc}，變卦為{bian_gua['name']}。{wuxing_relation['description']}"
            }
        }


def test_plum_blossom():
    """測試函數"""
    # 測試時間起卦
    test_datetime = datetime(1990, 5, 15, 14, 30)

    print("="*80)
    print("梅花易數測試")
    print("="*80)
    print(f"\n測試時間：{test_datetime.strftime('%Y年%m月%d日 %H:%M')}")

    calculator = PlumBlossomCalculator(test_datetime, method="time")
    result = calculator.analyze()

    print(f"\n📅 起卦時間：{result['divination_time']}")
    print(f"📋 起卦方法：{result['method']}")

    print(f"\n🎯 本卦：{result['ben_gua']['name']}")
    print(f"   上卦：{result['ben_gua']['upper']['name']}（{result['ben_gua']['upper']['wuxing']}）{result['ben_gua']['upper']['symbol']}")
    print(f"   下卦：{result['ben_gua']['lower']['name']}（{result['ben_gua']['lower']['wuxing']}）{result['ben_gua']['lower']['symbol']}")
    print(f"   卦辭：{result['ben_gua']['description']}")
    print(f"   釋義：{result['ben_gua']['meaning']}")

    print(f"\n🔄 動爻：{result['changing_line']['description']}")

    print(f"\n🎯 變卦：{result['bian_gua']['name']}")
    print(f"   卦辭：{result['bian_gua']['description']}")
    print(f"   釋義：{result['bian_gua']['meaning']}")

    print(f"\n⚖️ 五行分析：")
    print(f"   關係：{result['wuxing_analysis']['relation']}")
    print(f"   吉凶：{result['wuxing_analysis']['effect']}")
    print(f"   說明：{result['wuxing_analysis']['description']}")

    print(f"\n✨ 綜合判斷：")
    print(f"   吉凶：{result['overall_judgment']['luck']}")
    print(f"   總結：{result['overall_judgment']['summary']}")


if __name__ == "__main__":
    test_plum_blossom()

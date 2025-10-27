"""
紫微斗數計算器 (Zi Wei Dou Shu Calculator) - 精簡版
============================================

核心功能：
1. 十二宮定位
2. 主星安置
3. 四化計算
4. 基本宮位解讀
"""

from typing import Dict, List, Tuple
from .utils import EARTHLY_BRANCHES, ZIWEI_MAJOR_STARS, ZIWEI_TWELVE_PALACES


class ZiweiCalculator:
    """紫微斗數計算器 - 精簡實用版"""

    def __init__(self, calendar_data: Dict, gender: str):
        self.calendar_data = calendar_data
        self.gender = gender

        # 提取農曆和四柱資訊
        self.lunar = calendar_data["lunar"]
        self.four_pillars = calendar_data["four_pillars"]

        # 出生年月日時（農曆）
        self.birth_year = self.lunar["year"]
        self.birth_month = self.lunar["month"]
        self.birth_day = self.lunar["day"]
        self.birth_hour_branch = self.four_pillars["hour"]["branch"]

    def analyze(self) -> Dict:
        """完整紫微分析"""
        # 1. 定命宮
        ming_palace_position = self._locate_ming_palace()

        # 2. 安紫微星
        ziwei_position = self._locate_ziwei_star()

        # 3. 建立十二宮
        palaces = self._build_twelve_palaces(ming_palace_position)

        # 4. 安置主星
        palaces_with_stars = self._place_major_stars(palaces, ziwei_position)

        # 5. 四化
        four_transformations = self._calculate_four_transformations()

        # 6. 宮位解讀
        interpretations = self._interpret_palaces(palaces_with_stars)

        return {
            "ming_palace_position": ming_palace_position,
            "ziwei_position": ziwei_position,
            "palaces": palaces_with_stars,
            "four_transformations": four_transformations,
            "interpretations": interpretations,
            "chart_summary": self._generate_summary(palaces_with_stars)
        }

    def _locate_ming_palace(self) -> int:
        """
        定命宮位置

        口訣：子上起正月，逆數到生月，再從生月起子時，順數到生時

        Returns:
            命宮在地支的索引位置 (0-11)
        """
        # 從子位（0）起正月，逆數到生月
        month = self.birth_month
        month_position = (12 - month + 1) % 12  # 逆數

        # 從生月位置起子時，順數到生時
        hour_index = EARTHLY_BRANCHES.index(self.birth_hour_branch)
        ming_palace_position = (month_position + hour_index) % 12

        return ming_palace_position

    def _locate_ziwei_star(self) -> int:
        """
        定紫微星位置

        使用生日和五行局數

        Returns:
            紫微星在地支的索引位置 (0-11)
        """
        # 簡化版：根據生日直接定位（實際需要五行局數）
        day = self.birth_day

        # 紫微星定位表（簡化）
        if 1 <= day <= 10:
            base = 0  # 寅宮
        elif 11 <= day <= 20:
            base = 4  # 午宮
        else:
            base = 8  # 戌宮

        # 根據日數微調
        offset = (day - 1) % 3
        ziwei_position = (base + offset) % 12

        return ziwei_position

    def _build_twelve_palaces(self, ming_palace_position: int) -> Dict:
        """
        建立十二宮結構

        從命宮開始順時針排列
        """
        palaces = {}

        for i, palace_name in enumerate(ZIWEI_TWELVE_PALACES):
            position = (ming_palace_position + i) % 12
            branch = EARTHLY_BRANCHES[position]

            palaces[palace_name] = {
                "name": palace_name,
                "position": position,
                "branch": branch,
                "major_stars": [],
                "transformations": []
            }

        return palaces

    def _place_major_stars(self, palaces: Dict, ziwei_position: int) -> Dict:
        """
        安置十四主星

        根據紫微星位置推算其他主星
        """
        # 主星排列規則（簡化版）
        # 實際紫微斗數星曜排列非常複雜

        star_offsets = {
            "紫微": 0,
            "天機": 1,
            "太陽": 2,
            "武曲": 3,
            "天同": 4,
            "廉貞": 5,
            "天府": 6,
            "太陰": 7,
            "貪狼": 8,
            "巨門": 9,
            "天相": 10,
            "天梁": 11,
            "七殺": 6,   # 與紫微相對
            "破軍": 4    # 固定位置
        }

        # 根據紫微位置計算各星位置
        for star_name, offset in star_offsets.items():
            if star_name in ["七殺", "破軍"]:
                # 特殊星曜有固定關係
                star_position = (ziwei_position + offset) % 12
            else:
                star_position = (ziwei_position + offset) % 12

            # 找到對應宮位並添加星曜
            for palace_name, palace_data in palaces.items():
                if palace_data["position"] == star_position:
                    palace_data["major_stars"].append(star_name)
                    break

        return palaces

    def _calculate_four_transformations(self) -> Dict:
        """
        計算四化（祿權科忌）

        根據出生年天干確定
        """
        year_stem = self.four_pillars["year"]["stem"]

        # 四化表（簡化版）
        transformations_table = {
            "甲": {"祿": "廉貞", "權": "破軍", "科": "武曲", "忌": "太陽"},
            "乙": {"祿": "天機", "權": "天梁", "科": "紫微", "忌": "太陰"},
            "丙": {"祿": "天同", "權": "天機", "科": "文昌", "忌": "廉貞"},
            "丁": {"祿": "太陰", "權": "天同", "科": "天機", "忌": "巨門"},
            "戊": {"祿": "貪狼", "權": "太陰", "科": "右弼", "忌": "天機"},
            "己": {"祿": "武曲", "權": "貪狼", "科": "天梁", "忌": "文曲"},
            "庚": {"祿": "太陽", "權": "武曲", "科": "太陰", "忌": "天同"},
            "辛": {"祿": "巨門", "權": "太陽", "科": "文曲", "忌": "文昌"},
            "壬": {"祿": "天梁", "權": "紫微", "科": "左輔", "忌": "武曲"},
            "癸": {"祿": "破軍", "權": "巨門", "科": "太陰", "忌": "貪狼"}
        }

        return transformations_table.get(year_stem, {})

    def _interpret_palaces(self, palaces: Dict) -> Dict:
        """
        解讀各宮位

        根據主星組合給出基本解釋
        """
        interpretations = {}

        # 星曜基本含義（極簡版）
        star_meanings = {
            "紫微": "帝王之星，主貴氣權威",
            "天機": "智慧之星，主聰明靈活",
            "太陽": "光明之星，主熱情積極",
            "武曲": "財帛之星，主理財能力",
            "天同": "福德之星，主享福安逸",
            "廉貞": "桃花之星，主感情豐富",
            "天府": "財庫之星，主守成穩健",
            "太陰": "柔順之星，主細膩溫和",
            "貪狼": "多才之星，主才藝廣泛",
            "巨門": "口才之星，主善於溝通",
            "天相": "輔佐之星，主助人為樂",
            "天梁": "蔭庇之星，主化解災厄",
            "七殺": "將星之星，主果斷勇敢",
            "破軍": "開創之星，主變革創新"
        }

        for palace_name, palace_data in palaces.items():
            stars = palace_data["major_stars"]

            if not stars:
                interpretation = "此宮無主星，需借對宮之星參看"
            elif len(stars) == 1:
                interpretation = star_meanings.get(stars[0], "主星特質待分析")
            else:
                # 多星組合
                star_names = "、".join(stars)
                interpretation = f"有{star_names}組合，主{star_names}的綜合特質"

            interpretations[palace_name] = {
                "stars": stars,
                "interpretation": interpretation,
                "importance": self._rate_palace_importance(palace_name, stars)
            }

        return interpretations

    def _rate_palace_importance(self, palace_name: str, stars: List[str]) -> str:
        """評估宮位重要性"""
        # 命宮最重要
        if palace_name == "命宮":
            return "極為重要"

        # 有主星的宮位較重要
        important_palaces = ["夫妻", "財帛", "官祿", "福德"]
        if palace_name in important_palaces:
            return "重要" if stars else "次要"

        return "一般"

    def _generate_summary(self, palaces: Dict) -> Dict:
        """生成命盤摘要"""
        ming_palace = palaces["命宮"]
        caibo_palace = palaces["財帛"]
        guanlu_palace = palaces["官祿"]

        return {
            "命宮主星": ming_palace["major_stars"] or ["無主星"],
            "財帛主星": caibo_palace["major_stars"] or ["無主星"],
            "官祿主星": guanlu_palace["major_stars"] or ["無主星"],
            "命格特徵": self._determine_fate_pattern(ming_palace)
        }

    def _determine_fate_pattern(self, ming_palace: Dict) -> str:
        """判斷命格特徵"""
        stars = ming_palace["major_stars"]

        if not stars:
            return "借星命格，需參考對宮"

        if "紫微" in stars:
            return "紫微坐命，帝王之格"
        elif "天府" in stars:
            return "天府坐命，財庫之格"
        elif "武曲" in stars:
            return "武曲坐命，財帛之格"
        else:
            return f"{stars[0]}坐命格局"


def quick_ziwei_analysis(calendar_data: Dict, gender: str) -> Dict:
    """快速紫微分析"""
    calculator = ZiweiCalculator(calendar_data, gender)
    return calculator.analyze()


if __name__ == "__main__":
    print("紫微斗數計算器 - 精簡版")
    print("配合 calendar_converter 使用")

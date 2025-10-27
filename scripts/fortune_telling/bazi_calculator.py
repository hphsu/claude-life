"""
八字命理計算器 (BaZi Calculator)
================================

專業級八字命理分析系統，提供：
1. 四柱八字排盤
2. 五行統計與分析
3. 十神配置
4. 格局判斷
5. 用神分析
6. 大運推算
7. 流年分析
8. 命運特徵解讀

基於子平八字、滴天髓等經典命理理論
"""

from typing import Dict, List, Tuple, Optional
from collections import Counter
from .utils import (
    HEAVENLY_STEMS,
    EARTHLY_BRANCHES,
    WuXing,
    TenGods,
    BRANCH_HIDDEN_STEMS,
    get_wuxing_from_stem,
    get_wuxing_from_branch,
    get_ten_god,
    get_nayin,
    get_stem_branch_by_index,
    is_yin_yang,
    FourPillars
)


class BaziCalculator:
    """
    八字命理計算器

    負責所有八字相關的計算與分析
    """

    def __init__(self, calendar_data: Dict):
        """
        初始化八字計算器

        Args:
            calendar_data: 從 CalendarConverter 返回的完整日期資訊
        """
        self.calendar_data = calendar_data
        self.four_pillars = calendar_data["four_pillars"]

        # 提取四柱干支
        self.year_stem = self.four_pillars["year"]["stem"]
        self.year_branch = self.four_pillars["year"]["branch"]
        self.month_stem = self.four_pillars["month"]["stem"]
        self.month_branch = self.four_pillars["month"]["branch"]
        self.day_stem = self.four_pillars["day"]["stem"]
        self.day_branch = self.four_pillars["day"]["branch"]
        self.hour_stem = self.four_pillars["hour"]["stem"]
        self.hour_branch = self.four_pillars["hour"]["branch"]

        # 日主（命主）
        self.day_master = self.day_stem

    def analyze(self, gender: str = "男", include_luck_pillars: bool = True) -> Dict:
        """
        完整八字分析

        Args:
            gender: 性別（"男" 或 "女"）
            include_luck_pillars: 是否包含大運分析

        Returns:
            完整的八字分析結果
        """
        # 1. 基本命盤
        basic_chart = self._get_basic_chart()

        # 2. 五行統計
        wuxing_analysis = self._analyze_wuxing()

        # 3. 十神分析
        ten_gods_analysis = self._analyze_ten_gods()

        # 4. 地支藏干
        hidden_stems = self._analyze_hidden_stems()

        # 5. 格局判斷
        pattern_analysis = self._analyze_pattern()

        # 6. 用神分析
        yongshen_analysis = self._analyze_yongshen(wuxing_analysis)

        # 7. 身強身弱
        strength = self._calculate_strength(wuxing_analysis)

        # 8. 大運（如果需要）
        luck_pillars = None
        if include_luck_pillars:
            birth_date = self.calendar_data["gregorian"]["datetime"]
            luck_pillars = self._calculate_luck_pillars(gender, birth_date)

        # 9. 命運特徵
        destiny_features = self._analyze_destiny_features(
            wuxing_analysis,
            ten_gods_analysis,
            strength
        )

        return {
            "basic_chart": basic_chart,
            "wuxing_analysis": wuxing_analysis,
            "ten_gods_analysis": ten_gods_analysis,
            "hidden_stems": hidden_stems,
            "pattern": pattern_analysis,
            "yongshen": yongshen_analysis,
            "strength": strength,
            "luck_pillars": luck_pillars,
            "destiny_features": destiny_features
        }

    def _get_basic_chart(self) -> Dict:
        """獲取基本四柱資訊"""
        return {
            "year": {
                "pillar": f"{self.year_stem}{self.year_branch}",
                "stem": self.year_stem,
                "branch": self.year_branch,
                "stem_wuxing": get_wuxing_from_stem(self.year_stem).value,
                "branch_wuxing": get_wuxing_from_branch(self.year_branch).value,
                "nayin": get_nayin(self.year_stem, self.year_branch),
                "yinyang": {
                    "stem": is_yin_yang(self.year_stem),
                    "branch": is_yin_yang(self.year_branch)
                }
            },
            "month": {
                "pillar": f"{self.month_stem}{self.month_branch}",
                "stem": self.month_stem,
                "branch": self.month_branch,
                "stem_wuxing": get_wuxing_from_stem(self.month_stem).value,
                "branch_wuxing": get_wuxing_from_branch(self.month_branch).value,
                "nayin": get_nayin(self.month_stem, self.month_branch),
                "yinyang": {
                    "stem": is_yin_yang(self.month_stem),
                    "branch": is_yin_yang(self.month_branch)
                }
            },
            "day": {
                "pillar": f"{self.day_stem}{self.day_branch}",
                "stem": self.day_stem,
                "branch": self.day_branch,
                "stem_wuxing": get_wuxing_from_stem(self.day_stem).value,
                "branch_wuxing": get_wuxing_from_branch(self.day_branch).value,
                "nayin": get_nayin(self.day_stem, self.day_branch),
                "yinyang": {
                    "stem": is_yin_yang(self.day_stem),
                    "branch": is_yin_yang(self.day_branch)
                }
            },
            "hour": {
                "pillar": f"{self.hour_stem}{self.hour_branch}",
                "stem": self.hour_stem,
                "branch": self.hour_branch,
                "stem_wuxing": get_wuxing_from_stem(self.hour_stem).value,
                "branch_wuxing": get_wuxing_from_branch(self.hour_branch).value,
                "nayin": get_nayin(self.hour_stem, self.hour_branch),
                "yinyang": {
                    "stem": is_yin_yang(self.hour_stem),
                    "branch": is_yin_yang(self.hour_branch)
                }
            },
            "day_master": self.day_master,
            "day_master_wuxing": get_wuxing_from_stem(self.day_master).value
        }

    def _analyze_wuxing(self) -> Dict:
        """
        五行統計與分析

        Returns:
            五行分佈與強弱分析
        """
        # 統計天干五行
        stems = [self.year_stem, self.month_stem, self.day_stem, self.hour_stem]
        stem_wuxing = [get_wuxing_from_stem(s) for s in stems]

        # 統計地支五行
        branches = [self.year_branch, self.month_branch, self.day_branch, self.hour_branch]
        branch_wuxing = [get_wuxing_from_branch(b) for b in branches]

        # 統計藏干五行
        hidden_wuxing = []
        for branch in branches:
            for hidden_stem, _ in BRANCH_HIDDEN_STEMS[branch]:
                hidden_wuxing.append(get_wuxing_from_stem(hidden_stem))

        # 綜合統計
        all_wuxing = stem_wuxing + branch_wuxing + hidden_wuxing
        wuxing_counter = Counter(all_wuxing)

        # 計算各五行數量
        wuxing_count = {
            WuXing.WOOD.value: wuxing_counter[WuXing.WOOD],
            WuXing.FIRE.value: wuxing_counter[WuXing.FIRE],
            WuXing.EARTH.value: wuxing_counter[WuXing.EARTH],
            WuXing.METAL.value: wuxing_counter[WuXing.METAL],
            WuXing.WATER.value: wuxing_counter[WuXing.WATER]
        }

        # 找出缺失和旺盛的五行
        total = sum(wuxing_count.values())
        average = total / 5

        missing = [wx for wx, count in wuxing_count.items() if count == 0]
        weak = [wx for wx, count in wuxing_count.items() if 0 < count < average * 0.6]
        strong = [wx for wx, count in wuxing_count.items() if count > average * 1.5]

        return {
            "counts": wuxing_count,
            "total": total,
            "average": average,
            "missing": missing,
            "weak": weak,
            "strong": strong,
            "balance_score": self._calculate_balance_score(wuxing_count)
        }

    def _calculate_balance_score(self, wuxing_count: Dict) -> float:
        """
        計算五行平衡度（0-1，1為完全平衡）
        """
        counts = list(wuxing_count.values())
        if not counts:
            return 0.0

        average = sum(counts) / len(counts)
        variance = sum((c - average) ** 2 for c in counts) / len(counts)

        # 標準化為0-1分數（方差越小越平衡）
        max_variance = average ** 2
        balance_score = 1.0 - min(variance / max_variance, 1.0)

        return round(balance_score, 2)

    def _analyze_ten_gods(self) -> Dict:
        """
        十神分析

        Returns:
            十神配置與解讀
        """
        # 計算各柱的十神
        year_god = get_ten_god(self.day_stem, self.year_stem)
        month_god = get_ten_god(self.day_stem, self.month_stem)
        day_god = TenGods.BI_JIAN  # 日柱天干就是日主，必為比肩
        hour_god = get_ten_god(self.day_stem, self.hour_stem)

        # 統計十神分佈
        gods = [year_god, month_god, hour_god]  # 不包含日主
        god_counter = Counter(gods)

        # 統計各類十神數量
        god_distribution = {}
        for god in TenGods:
            god_distribution[god.value] = god_counter[god]

        # 分析主要特徵
        dominant_gods = [god.value for god, count in god_counter.most_common(2) if count > 0]

        return {
            "year": year_god.value,
            "month": month_god.value,
            "day": day_god.value,
            "hour": hour_god.value,
            "distribution": god_distribution,
            "dominant": dominant_gods,
            "interpretation": self._interpret_ten_gods(god_counter)
        }

    def _interpret_ten_gods(self, god_counter: Counter) -> Dict:
        """解讀十神特徵"""
        interpretation = {
            "career": "",  # 事業
            "wealth": "",  # 財運
            "relationship": "",  # 感情
            "character": ""  # 性格
        }

        # 簡化的十神解讀邏輯
        # 實際應用中需要更複雜的規則系統

        if god_counter[TenGods.ZHENG_GUAN] > 0 or god_counter[TenGods.QI_SHA] > 0:
            interpretation["career"] = "有官運，適合從事管理或公職"

        if god_counter[TenGods.ZHENG_CAI] > 0 or god_counter[TenGods.PIAN_CAI] > 0:
            interpretation["wealth"] = "財運較好，有經商天賦"

        if god_counter[TenGods.SHANG_GUAN] > 1:
            interpretation["character"] = "聰明靈活但較為叛逆"

        if god_counter[TenGods.ZHENG_YIN] > 0:
            interpretation["character"] = "重視學習，有文化修養"

        return interpretation

    def _analyze_hidden_stems(self) -> Dict:
        """分析地支藏干"""
        hidden_analysis = {}

        for position, branch in [
            ("year", self.year_branch),
            ("month", self.month_branch),
            ("day", self.day_branch),
            ("hour", self.hour_branch)
        ]:
            hidden = []
            for stem, days in BRANCH_HIDDEN_STEMS[branch]:
                hidden.append({
                    "stem": stem,
                    "days": days,
                    "wuxing": get_wuxing_from_stem(stem).value,
                    "ten_god": get_ten_god(self.day_stem, stem).value
                })
            hidden_analysis[position] = hidden

        return hidden_analysis

    def _analyze_pattern(self) -> Dict:
        """
        格局判斷

        Returns:
            格局類型與評估
        """
        # 這是簡化版的格局判斷
        # 實際八字格局判斷非常複雜，需要考慮月令、透干、會局等多種因素

        month_god = get_ten_god(self.day_stem, self.month_stem)

        pattern_type = "普通格局"
        pattern_quality = "中等"

        # 基本格局判斷
        if month_god == TenGods.ZHENG_GUAN:
            pattern_type = "正官格"
            pattern_quality = "良好"
        elif month_god == TenGods.ZHENG_CAI:
            pattern_type = "正財格"
            pattern_quality = "良好"
        elif month_god == TenGods.ZHENG_YIN:
            pattern_type = "正印格"
            pattern_quality = "良好"
        elif month_god == TenGods.SHI_SHEN:
            pattern_type = "食神格"
            pattern_quality = "良好"

        return {
            "type": pattern_type,
            "quality": pattern_quality,
            "month_commander": month_god.value,
            "note": "格局判斷需結合整體命局綜合分析"
        }

    def _analyze_yongshen(self, wuxing_analysis: Dict) -> Dict:
        """
        用神分析

        Args:
            wuxing_analysis: 五行分析結果

        Returns:
            用神、喜神、忌神分析
        """
        day_master_wuxing = get_wuxing_from_stem(self.day_master)
        strong_wx = wuxing_analysis["strong"]
        weak_wx = wuxing_analysis["weak"]
        missing_wx = wuxing_analysis["missing"]

        # 簡化的用神取法
        # 實際需要綜合考慮月令、格局、五行平衡等多種因素

        yongshen = []
        xishen = []
        jishen = []

        # 如果日主五行過強，用神取克洩耗
        if day_master_wuxing.value in strong_wx:
            # 取克我、我生的五行為用神
            from .utils import WUXING_GENERATES, WUXING_CONTROLS

            # 找出克制日主的五行
            for wx, controlled in WUXING_CONTROLS.items():
                if controlled == day_master_wuxing:
                    yongshen.append(wx.value)

            # 日主所生的五行（洩氣）
            if day_master_wuxing in WUXING_GENERATES:
                yongshen.append(WUXING_GENERATES[day_master_wuxing].value)

        # 如果日主五行過弱，用神取生扶
        elif day_master_wuxing.value in weak_wx or day_master_wuxing.value in missing_wx:
            # 取生我、助我的五行為用神
            from .utils import WUXING_GENERATES

            # 找出生日主的五行
            for wx, generated in WUXING_GENERATES.items():
                if generated == day_master_wuxing:
                    yongshen.append(wx.value)

            # 同類五行（比劫）
            yongshen.append(day_master_wuxing.value)

        # 去重
        yongshen = list(set(yongshen))

        # 喜神通常是生用神的五行
        # 忌神通常是克用神的五行

        return {
            "yongshen": yongshen,
            "xishen": xishen,
            "jishen": strong_wx if yongshen else [],
            "day_master_wuxing": day_master_wuxing.value,
            "recommendation": self._generate_yongshen_recommendations(yongshen)
        }

    def _generate_yongshen_recommendations(self, yongshen: List[str]) -> Dict:
        """生成用神建議"""
        recommendations = {
            "colors": [],
            "directions": [],
            "industries": []
        }

        # 五行對應建議（簡化版）
        wuxing_recommendations = {
            "木": {
                "colors": ["綠色", "青色"],
                "directions": ["東方"],
                "industries": ["文化教育", "醫療衛生", "木材家具"]
            },
            "火": {
                "colors": ["紅色", "紫色"],
                "directions": ["南方"],
                "industries": ["能源電力", "電子科技", "餐飲娛樂"]
            },
            "土": {
                "colors": ["黃色", "棕色"],
                "directions": ["中央", "西南", "東北"],
                "industries": ["房地產", "建築工程", "農業畜牧"]
            },
            "金": {
                "colors": ["白色", "金色"],
                "directions": ["西方"],
                "industries": ["金融財經", "機械製造", "珠寶首飾"]
            },
            "水": {
                "colors": ["黑色", "藍色"],
                "directions": ["北方"],
                "industries": ["物流運輸", "水產漁業", "旅遊服務"]
            }
        }

        for wx in yongshen:
            if wx in wuxing_recommendations:
                rec = wuxing_recommendations[wx]
                recommendations["colors"].extend(rec["colors"])
                recommendations["directions"].extend(rec["directions"])
                recommendations["industries"].extend(rec["industries"])

        return recommendations

    def _calculate_strength(self, wuxing_analysis: Dict) -> Dict:
        """
        計算身強身弱

        Returns:
            身強弱評估
        """
        day_master_wuxing = get_wuxing_from_stem(self.day_master)
        day_master_count = wuxing_analysis["counts"][day_master_wuxing.value]
        average = wuxing_analysis["average"]

        # 簡化的身強弱判斷
        if day_master_count > average * 1.2:
            strength_level = "身強"
            description = "日主力量充足，能承擔財官"
        elif day_master_count < average * 0.8:
            strength_level = "身弱"
            description = "日主力量不足，需要生扶"
        else:
            strength_level = "身中和"
            description = "日主力量適中，平衡穩定"

        return {
            "level": strength_level,
            "score": round(day_master_count / average, 2),
            "description": description
        }

    def _calculate_luck_pillars(self, gender: str, birth_date) -> List[Dict]:
        """
        計算大運

        Args:
            gender: 性別
            birth_date: 出生日期

        Returns:
            大運列表
        """
        # 確定順行還是逆行
        # 陽男陰女順行，陰男陽女逆行
        year_stem_yinyang = is_yin_yang(self.year_stem)

        if gender == "男":
            forward = (year_stem_yinyang == "陽")
        else:  # 女
            forward = (year_stem_yinyang == "陰")

        # 計算起運歲數（簡化版，實際需要根據節氣精確計算）
        # 這裡使用3歲起運的簡化算法
        start_age = 3

        # 從月柱開始推算大運
        month_pillar_index = HEAVENLY_STEMS.index(self.month_stem) * 6 + \
                            EARTHLY_BRANCHES.index(self.month_branch)

        luck_pillars = []
        for i in range(8):  # 計算8步大運（80年）
            age_start = start_age + i * 10
            age_end = age_start + 9

            if forward:
                luck_index = (month_pillar_index + i + 1) % 60
            else:
                luck_index = (month_pillar_index - i - 1) % 60

            stem, branch = get_stem_branch_by_index(luck_index)

            luck_pillars.append({
                "sequence": i + 1,
                "age_range": f"{age_start}-{age_end}歲",
                "pillar": f"{stem}{branch}",
                "stem": stem,
                "branch": branch,
                "stem_wuxing": get_wuxing_from_stem(stem).value,
                "branch_wuxing": get_wuxing_from_branch(branch).value,
                "nayin": get_nayin(stem, branch)
            })

        return luck_pillars

    def _analyze_destiny_features(
        self,
        wuxing_analysis: Dict,
        ten_gods_analysis: Dict,
        strength: Dict
    ) -> Dict:
        """
        綜合分析命運特徵

        Returns:
            事業、財運、感情、健康等方面的特徵
        """
        features = {
            "career": self._analyze_career(ten_gods_analysis, strength),
            "wealth": self._analyze_wealth(ten_gods_analysis, wuxing_analysis),
            "relationship": self._analyze_relationship(ten_gods_analysis),
            "health": self._analyze_health(wuxing_analysis),
            "character": self._analyze_character(ten_gods_analysis, wuxing_analysis)
        }

        return features

    def _analyze_career(self, ten_gods: Dict, strength: Dict) -> Dict:
        """事業運分析"""
        gods = ten_gods["distribution"]

        career_score = 5.0  # 基礎分5分（滿分10分）
        characteristics = []

        if gods.get(TenGods.ZHENG_GUAN.value, 0) > 0:
            career_score += 2.0
            characteristics.append("適合從事管理工作")

        if gods.get(TenGods.QI_SHA.value, 0) > 0:
            career_score += 1.5
            characteristics.append("有領導能力")

        if gods.get(TenGods.ZHENG_YIN.value, 0) > 0:
            career_score += 1.0
            characteristics.append("適合學術或教育行業")

        if strength["level"] == "身強":
            career_score += 1.0

        return {
            "score": min(career_score, 10.0),
            "level": self._score_to_level(career_score),
            "characteristics": characteristics
        }

    def _analyze_wealth(self, ten_gods: Dict, wuxing: Dict) -> Dict:
        """財運分析"""
        gods = ten_gods["distribution"]

        wealth_score = 5.0
        characteristics = []

        if gods.get(TenGods.ZHENG_CAI.value, 0) > 0:
            wealth_score += 2.0
            characteristics.append("正財運佳，適合穩定收入")

        if gods.get(TenGods.PIAN_CAI.value, 0) > 0:
            wealth_score += 1.5
            characteristics.append("偏財運好，適合投資")

        if gods.get(TenGods.SHI_SHEN.value, 0) > 0:
            wealth_score += 1.0
            characteristics.append("食神生財，有賺錢天賦")

        return {
            "score": min(wealth_score, 10.0),
            "level": self._score_to_level(wealth_score),
            "characteristics": characteristics
        }

    def _analyze_relationship(self, ten_gods: Dict) -> Dict:
        """感情婚姻分析"""
        gods = ten_gods["distribution"]

        relationship_score = 5.0
        characteristics = []

        # 男命看財星，女命看官星（簡化處理）
        if gods.get(TenGods.ZHENG_CAI.value, 0) > 0:
            relationship_score += 1.5
            characteristics.append("感情專一穩定")

        if gods.get(TenGods.PIAN_CAI.value, 0) > 1:
            characteristics.append("桃花較多，需注意專情")

        return {
            "score": min(relationship_score, 10.0),
            "level": self._score_to_level(relationship_score),
            "characteristics": characteristics
        }

    def _analyze_health(self, wuxing: Dict) -> Dict:
        """健康狀況分析"""
        balance_score = wuxing["balance_score"]
        missing = wuxing["missing"]

        health_score = balance_score * 10  # 五行平衡度直接影響健康
        concerns = []

        if "水" in missing:
            concerns.append("注意腎臟、泌尿系統")
        if "木" in missing:
            concerns.append("注意肝膽、四肢")
        if "火" in missing:
            concerns.append("注意心臟、血液循環")
        if "土" in missing:
            concerns.append("注意脾胃、消化系統")
        if "金" in missing:
            concerns.append("注意呼吸系統、皮膚")

        return {
            "score": health_score,
            "level": self._score_to_level(health_score),
            "concerns": concerns,
            "balance_score": balance_score
        }

    def _analyze_character(self, ten_gods: Dict, wuxing: Dict) -> Dict:
        """性格特質分析"""
        characteristics = []

        # 根據主導十神分析
        dominant = ten_gods["dominant"]

        if TenGods.BI_JIAN.value in dominant or TenGods.JIE_CAI.value in dominant:
            characteristics.append("獨立自主，有主見")

        if TenGods.SHANG_GUAN.value in dominant:
            characteristics.append("聰明機智，善於表達")

        if TenGods.ZHENG_YIN.value in dominant:
            characteristics.append("溫和穩重，重視學習")

        # 根據五行特徵
        strong_wx = wuxing["strong"]
        if "木" in strong_wx:
            characteristics.append("仁慈有愛心")
        if "火" in strong_wx:
            characteristics.append("熱情積極")
        if "土" in strong_wx:
            characteristics.append("穩重可靠")
        if "金" in strong_wx:
            characteristics.append("果斷堅強")
        if "水" in strong_wx:
            characteristics.append("聰明靈活")

        return {
            "primary_traits": characteristics[:3],  # 主要特質
            "all_traits": characteristics
        }

    def _score_to_level(self, score: float) -> str:
        """將分數轉換為等級"""
        if score >= 8.5:
            return "極佳"
        elif score >= 7.0:
            return "良好"
        elif score >= 5.5:
            return "中等"
        elif score >= 4.0:
            return "偏弱"
        else:
            return "較差"


# ============================================
# 便捷函數
# ============================================

def quick_bazi_analysis(calendar_data: Dict, gender: str = "男") -> Dict:
    """
    快速八字分析

    Args:
        calendar_data: CalendarConverter 的輸出
        gender: 性別

    Returns:
        完整的八字分析結果
    """
    calculator = BaziCalculator(calendar_data)
    return calculator.analyze(gender=gender)


if __name__ == "__main__":
    # 測試代碼需要配合 calendar_converter 使用
    print("八字計算器模組")
    print("請配合 calendar_converter 使用")

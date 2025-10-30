"""
奇門遁甲計算模組 (Qi Men Dun Jia Calculator)
道家最高層次的術數預測系統
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple


class QimenCalculator:
    """奇門遁甲計算器"""

    # 天干
    TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

    # 地支
    DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

    # 九星
    JIUXING = {
        1: {"name": "天蓬星", "wuxing": "水", "nature": "凶", "meaning": "賊盜、暗昧"},
        2: {"name": "天芮星", "wuxing": "土", "nature": "凶", "meaning": "疾病、死亡"},
        3: {"name": "天沖星", "wuxing": "木", "nature": "凶", "meaning": "衝突、急躁"},
        4: {"name": "天輔星", "wuxing": "木", "nature": "吉", "meaning": "文書、貴人"},
        5: {"name": "天禽星", "wuxing": "土", "nature": "平", "meaning": "中正、和合"},
        6: {"name": "天心星", "wuxing": "金", "nature": "大吉", "meaning": "醫藥、謀略"},
        7: {"name": "天柱星", "wuxing": "金", "nature": "凶", "meaning": "破壞、阻礙"},
        8: {"name": "天任星", "wuxing": "土", "nature": "吉", "meaning": "財富、田宅"},
        9: {"name": "天英星", "wuxing": "火", "nature": "凶", "meaning": "文書、火災"}
    }

    # 八門
    BAMEN = {
        1: {"name": "休門", "wuxing": "水", "nature": "吉", "meaning": "休息、退守", "suitable": "修養、求醫"},
        2: {"name": "死門", "wuxing": "土", "nature": "凶", "meaning": "死亡、終結", "suitable": "弔唁、狩獵"},
        3: {"name": "傷門", "wuxing": "木", "nature": "凶", "meaning": "傷害、損失", "suitable": "索債、捕獵"},
        4: {"name": "杜門", "wuxing": "木", "nature": "凶", "meaning": "閉塞、阻隔", "suitable": "躲藏、閉關"},
        5: {"name": "開門", "wuxing": "金", "nature": "大吉", "meaning": "開創、發展", "suitable": "開業、求財"},
        6: {"name": "驚門", "wuxing": "金", "nature": "凶", "meaning": "驚恐、官非", "suitable": "討債、訴訟"},
        7: {"name": "生門", "wuxing": "土", "nature": "大吉", "meaning": "生長、發展", "suitable": "求財、婚嫁"},
        8: {"name": "景門", "wuxing": "火", "nature": "中吉", "meaning": "光明、文書", "suitable": "考試、宴會"}
    }

    # 八神
    BASHEN = {
        1: {"name": "值符", "nature": "吉", "meaning": "貴人、權威"},
        2: {"name": "騰蛇", "nature": "凶", "meaning": "驚恐、虛詐"},
        3: {"name": "太陰", "nature": "吉", "meaning": "暗昧、陰謀"},
        4: {"name": "六合", "nature": "吉", "meaning": "婚姻、合作"},
        5: {"name": "白虎", "nature": "凶", "meaning": "凶禍、傷災"},
        6: {"name": "玄武", "nature": "凶", "meaning": "盜賊、失物"},
        7: {"name": "九地", "nature": "吉", "meaning": "穩固、防守"},
        8: {"name": "九天", "nature": "吉", "meaning": "顯揚、遠行"}
    }

    # 九宮方位
    JIUGONG = {
        1: {"name": "坎宮", "direction": "北", "wuxing": "水"},
        2: {"name": "坤宮", "direction": "西南", "wuxing": "土"},
        3: {"name": "震宮", "direction": "東", "wuxing": "木"},
        4: {"name": "巽宮", "direction": "東南", "wuxing": "木"},
        5: {"name": "中宮", "direction": "中", "wuxing": "土"},
        6: {"name": "乾宮", "direction": "西北", "wuxing": "金"},
        7: {"name": "兌宮", "direction": "西", "wuxing": "金"},
        8: {"name": "艮宮", "direction": "東北", "wuxing": "土"},
        9: {"name": "離宮", "direction": "南", "wuxing": "火"}
    }

    def __init__(self, divination_time: datetime, method: str = "時家奇門"):
        """
        初始化奇門遁甲計算器

        Args:
            divination_time: 占卜時間
            method: 起局方法（"時家奇門", "日家奇門", "月家奇門"）
        """
        self.divination_time = divination_time
        self.method = method

    def get_jieqi_index(self, dt: datetime) -> Tuple[str, int]:
        """
        獲取當前節氣索引（簡化版）

        Returns:
            (節氣名稱, 局數)
        """
        # 簡化的節氣判斷（實際應用需要精確計算）
        month = dt.month
        day = dt.day

        jieqi_map = {
            (2, 4): ("立春", 8), (2, 19): ("雨水", 9),
            (3, 6): ("驚蟄", 3), (3, 21): ("春分", 4),
            (4, 5): ("清明", 5), (4, 20): ("穀雨", 6),
            (5, 6): ("立夏", 1), (5, 21): ("小滿", 2),
            (6, 6): ("芒種", 3), (6, 22): ("夏至", 4),
            (7, 7): ("小暑", 5), (7, 23): ("大暑", 6),
            (8, 8): ("立秋", 7), (8, 23): ("處暑", 8),
            (9, 8): ("白露", 9), (9, 23): ("秋分", 1),
            (10, 8): ("寒露", 2), (10, 24): ("霜降", 3),
            (11, 7): ("立冬", 4), (11, 22): ("小雪", 5),
            (12, 7): ("大雪", 6), (12, 22): ("冬至", 7),
            (1, 6): ("小寒", 8), (1, 20): ("大寒", 9)
        }

        # 找到最接近的節氣
        closest_jieqi = ("立春", 8)  # 默認值
        min_diff = float('inf')

        for (m, d), jieqi in jieqi_map.items():
            if m == month and d <= day:
                if day - d < min_diff:
                    min_diff = day - d
                    closest_jieqi = jieqi

        return closest_jieqi

    def get_time_gan_zhi(self, dt: datetime) -> Dict[str, str]:
        """
        獲取時辰的天干地支（簡化計算）

        Returns:
            時辰干支資訊
        """
        # 簡化的時辰計算
        hour = dt.hour
        hour_branch_index = ((hour + 1) // 2) % 12

        # 簡化的天干計算（實際需要根據日干推算）
        hour_stem_index = (dt.day + hour_branch_index) % 10

        return {
            "stem": self.TIANGAN[hour_stem_index],
            "branch": self.DIZHI[hour_branch_index],
            "shichen": f"{self.TIANGAN[hour_stem_index]}{self.DIZHI[hour_branch_index]}"
        }

    def determine_ju_number(self, dt: datetime) -> Dict[str, Any]:
        """
        確定陽遁或陰遁，以及局數

        Returns:
            局數資訊
        """
        jieqi, base_ju = self.get_jieqi_index(dt)

        # 簡化判斷：冬至到夏至為陽遁，夏至到冬至為陰遁
        month = dt.month
        if 3 <= month <= 8:
            dun_type = "陽遁"
        else:
            dun_type = "陰遁"

        ju_number = base_ju

        return {
            "dun_type": dun_type,
            "ju_number": ju_number,
            "jieqi": jieqi,
            "description": f"{dun_type}{ju_number}局"
        }

    def arrange_jiuxing(self, ju_number: int, hour_branch_index: int) -> Dict[int, Dict]:
        """
        排九星到九宮

        Args:
            ju_number: 局數
            hour_branch_index: 時辰地支索引

        Returns:
            九宮九星配置
        """
        # 簡化的九星排布（實際需要根據局數和值符計算）
        # 這裡使用固定順序：天蓬、天芮、天沖、天輔、天禽、天心、天柱、天任、天英
        star_sequence = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        # 根據局數和時辰輪轉
        offset = (ju_number + hour_branch_index) % 9

        result = {}
        for i in range(9):
            gong_num = i + 1
            star_index = (i + offset) % 9
            star_num = star_sequence[star_index]
            result[gong_num] = self.JIUXING[star_num].copy()
            result[gong_num]["star_num"] = star_num

        return result

    def arrange_bamen(self, ju_number: int, hour_branch_index: int) -> Dict[int, Dict]:
        """
        排八門到九宮

        Args:
            ju_number: 局數
            hour_branch_index: 時辰地支索引

        Returns:
            九宮八門配置
        """
        # 簡化的八門排布
        # 順序：休、生、傷、杜、景、死、驚、開
        men_sequence = [1, 7, 3, 4, 8, 2, 6, 5]

        offset = (ju_number + hour_branch_index) % 8

        result = {}
        gong_index = 0
        for i in range(8):
            gong_num = (gong_index % 9) + 1
            if gong_num == 5:  # 跳過中宮
                gong_index += 1
                gong_num = (gong_index % 9) + 1

            men_index = (i + offset) % 8
            men_num = men_sequence[men_index]
            result[gong_num] = self.BAMEN[men_num].copy()
            result[gong_num]["men_num"] = men_num
            gong_index += 1

        return result

    def arrange_bashen(self, ju_number: int, hour_branch_index: int) -> Dict[int, Dict]:
        """
        排八神到九宮

        Args:
            ju_number: 局數
            hour_branch_index: 時辰地支索引

        Returns:
            九宮八神配置
        """
        # 簡化的八神排布
        # 順序：值符、騰蛇、太陰、六合、白虎、玄武、九地、九天
        shen_sequence = [1, 2, 3, 4, 5, 6, 7, 8]

        offset = (ju_number + hour_branch_index) % 8

        result = {}
        gong_index = 0
        for i in range(8):
            gong_num = (gong_index % 9) + 1
            if gong_num == 5:  # 跳過中宮
                gong_index += 1
                gong_num = (gong_index % 9) + 1

            shen_index = (i + offset) % 8
            shen_num = shen_sequence[shen_index]
            result[gong_num] = self.BASHEN[shen_num].copy()
            result[gong_num]["shen_num"] = shen_num
            gong_index += 1

        return result

    def analyze_gong(self, gong_num: int, star: Dict, men: Dict, shen: Dict) -> Dict[str, Any]:
        """
        分析單個宮位的吉凶

        Args:
            gong_num: 宮位編號
            star: 九星資訊
            men: 八門資訊
            shen: 八神資訊

        Returns:
            宮位分析結果
        """
        # 統計吉凶
        luck_scores = []

        # 九星吉凶
        if star["nature"] == "大吉":
            luck_scores.append(10)
        elif star["nature"] == "吉":
            luck_scores.append(7)
        elif star["nature"] == "平":
            luck_scores.append(5)
        else:
            luck_scores.append(3)

        # 八門吉凶
        if men["nature"] == "大吉":
            luck_scores.append(10)
        elif men["nature"] == "吉" or men["nature"] == "中吉":
            luck_scores.append(7)
        else:
            luck_scores.append(3)

        # 八神吉凶
        if shen["nature"] == "吉":
            luck_scores.append(7)
        else:
            luck_scores.append(3)

        avg_score = sum(luck_scores) / len(luck_scores)

        if avg_score >= 8:
            overall_luck = "大吉"
        elif avg_score >= 6:
            overall_luck = "吉"
        elif avg_score >= 4:
            overall_luck = "平"
        else:
            overall_luck = "凶"

        return {
            "gong": self.JIUGONG[gong_num],
            "star": star,
            "men": men,
            "shen": shen,
            "luck_score": round(avg_score, 1),
            "overall_luck": overall_luck,
            "analysis": f"{self.JIUGONG[gong_num]['name']}（{self.JIUGONG[gong_num]['direction']}）：{star['name']}、{men['name']}、{shen['name']}，綜合{overall_luck}"
        }

    def find_best_direction(self, palace_analysis: Dict[int, Dict]) -> Dict[str, Any]:
        """
        找出最吉利的方位

        Returns:
            最佳方位資訊
        """
        best_gong = None
        best_score = 0

        for gong_num, analysis in palace_analysis.items():
            if analysis["luck_score"] > best_score:
                best_score = analysis["luck_score"]
                best_gong = gong_num

        if best_gong:
            best_analysis = palace_analysis[best_gong]
            return {
                "direction": best_analysis["gong"]["direction"],
                "gong_name": best_analysis["gong"]["name"],
                "luck_score": best_analysis["luck_score"],
                "star": best_analysis["star"]["name"],
                "men": best_analysis["men"]["name"],
                "shen": best_analysis["shen"]["name"],
                "recommendation": f"最佳方位為{best_analysis['gong']['direction']}方（{best_analysis['gong']['name']}），宜{best_analysis['men']['suitable']}"
            }
        return {}

    def analyze(self) -> Dict[str, Any]:
        """
        執行完整的奇門遁甲分析

        Returns:
            完整的奇門遁甲盤象分析
        """
        # 獲取時辰干支
        time_gz = self.get_time_gan_zhi(self.divination_time)

        # 確定局數
        ju_info = self.determine_ju_number(self.divination_time)

        # 時辰地支索引
        hour_branch_index = self.DIZHI.index(time_gz["branch"])

        # 排九星、八門、八神
        jiuxing_layout = self.arrange_jiuxing(ju_info["ju_number"], hour_branch_index)
        bamen_layout = self.arrange_bamen(ju_info["ju_number"], hour_branch_index)
        bashen_layout = self.arrange_bashen(ju_info["ju_number"], hour_branch_index)

        # 分析各宮
        palace_analysis = {}
        for gong_num in range(1, 10):
            if gong_num == 5:  # 中宮特殊處理
                palace_analysis[gong_num] = {
                    "gong": self.JIUGONG[gong_num],
                    "star": jiuxing_layout.get(gong_num, {"name": "天禽星"}),
                    "men": {"name": "寄坤二宮", "meaning": "中宮無門"},
                    "shen": {"name": "中宮", "meaning": "中央之位"},
                    "luck_score": 5,
                    "overall_luck": "平",
                    "analysis": "中宮為中央樞紐，統籌八方"
                }
            else:
                palace_analysis[gong_num] = self.analyze_gong(
                    gong_num,
                    jiuxing_layout.get(gong_num, {}),
                    bamen_layout.get(gong_num, {}),
                    bashen_layout.get(gong_num, {})
                )

        # 找出最佳方位
        best_direction = self.find_best_direction(palace_analysis)

        # 生成盤面圖（簡化版文字表示）
        board_display = self.generate_board_display(palace_analysis)

        return {
            "divination_time": self.divination_time.strftime("%Y-%m-%d %H:%M:%S"),
            "method": self.method,
            "time_ganzhi": time_gz,
            "ju_info": ju_info,
            "palace_analysis": palace_analysis,
            "best_direction": best_direction,
            "board_display": board_display,
            "summary": {
                "ju_description": ju_info["description"],
                "time_shichen": time_gz["shichen"],
                "best_direction_summary": best_direction.get("recommendation", "需進一步分析"),
                "overall_advice": self.generate_overall_advice(palace_analysis)
            }
        }

    def generate_board_display(self, palace_analysis: Dict[int, Dict]) -> str:
        """
        生成奇門盤面的文字顯示

        Returns:
            盤面字串
        """
        # 九宮排列順序（左上到右下）
        layout = [
            [4, 9, 2],
            [3, 5, 7],
            [8, 1, 6]
        ]

        board = []
        for row in layout:
            row_strs = []
            for gong_num in row:
                analysis = palace_analysis[gong_num]
                cell = f"{analysis['gong']['name']}\n"
                if 'star' in analysis and 'name' in analysis['star']:
                    cell += f"{analysis['star']['name']}\n"
                if 'men' in analysis and 'name' in analysis['men']:
                    cell += f"{analysis['men']['name']}\n"
                if 'shen' in analysis and 'name' in analysis['shen']:
                    cell += f"{analysis['shen']['name']}"
                row_strs.append(cell)
            board.append(" | ".join(row_strs))

        return "\n" + "-" * 80 + "\n" + "\n".join(board) + "\n" + "-" * 80

    def generate_overall_advice(self, palace_analysis: Dict[int, Dict]) -> str:
        """
        生成整體建議

        Returns:
            建議文字
        """
        # 統計吉凶宮位數量
        da_ji = sum(1 for p in palace_analysis.values() if p.get("overall_luck") == "大吉")
        ji = sum(1 for p in palace_analysis.values() if p.get("overall_luck") == "吉")
        xiong = sum(1 for p in palace_analysis.values() if p.get("overall_luck") == "凶")

        if da_ji + ji >= 5:
            return "此時盤局吉星眾多，適合主動出擊、開創事業"
        elif xiong >= 5:
            return "此時盤局凶星較多，宜守不宜攻，靜待時機"
        else:
            return "此時盤局吉凶參半，謹慎行事，趨吉避凶"


def test_qimen():
    """測試函數"""
    test_time = datetime(2025, 10, 30, 14, 30)

    print("="*80)
    print("奇門遁甲測試")
    print("="*80)
    print(f"\n占測時間：{test_time.strftime('%Y年%m月%d日 %H:%M')}")

    calculator = QimenCalculator(test_time)
    result = calculator.analyze()

    print(f"\n📅 起局資訊：")
    print(f"   方法：{result['method']}")
    print(f"   時辰：{result['time_ganzhi']['shichen']}")
    print(f"   局數：{result['ju_info']['description']}")
    print(f"   節氣：{result['ju_info']['jieqi']}")

    print(f"\n🎯 最佳方位：")
    best = result['best_direction']
    print(f"   方向：{best.get('direction', '未知')}")
    print(f"   宮位：{best.get('gong_name', '未知')}")
    print(f"   評分：{best.get('luck_score', 0)}/10")
    print(f"   配置：{best.get('star', '')}, {best.get('men', '')}, {best.get('shen', '')}")
    print(f"   建議：{best.get('recommendation', '')}")

    print(f"\n✨ 整體建議：")
    print(f"   {result['summary']['overall_advice']}")

    print(result['board_display'])


if __name__ == "__main__":
    test_qimen()

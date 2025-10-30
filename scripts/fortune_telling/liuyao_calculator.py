"""
六爻占卜計算模組 (Liu Yao Divination Calculator)
基於《易經》的六爻預測系統
"""

from datetime import datetime
import random
from typing import Dict, List, Any, Tuple


class LiuyaoCalculator:
    """六爻占卜計算器"""

    # 八卦基本屬性
    BAGUA = {
        0: {"name": "坤", "trigram": "☷", "nature": "地", "wuxing": "土", "family": "母"},
        1: {"name": "艮", "trigram": "☶", "nature": "山", "wuxing": "土", "family": "少男"},
        2: {"name": "坎", "trigram": "☵", "nature": "水", "wuxing": "水", "family": "中男"},
        3: {"name": "巽", "trigram": "☴", "nature": "風", "wuxing": "木", "family": "長女"},
        4: {"name": "震", "trigram": "☳", "nature": "雷", "wuxing": "木", "family": "長男"},
        5: {"name": "離", "trigram": "☲", "nature": "火", "wuxing": "火", "family": "中女"},
        6: {"name": "兌", "trigram": "☱", "nature": "澤", "wuxing": "金", "family": "少女"},
        7: {"name": "乾", "trigram": "☰", "nature": "天", "wuxing": "金", "family": "父"}
    }

    # 64卦資訊
    HEXAGRAMS = {
        (7, 7): {"name": "乾為天", "desc": "元亨利貞", "judgment": "吉", "meaning": "剛健中正，大吉大利"},
        (0, 0): {"name": "坤為地", "desc": "元亨，利牝馬之貞", "judgment": "吉", "meaning": "柔順承載，厚德載物"},
        (2, 4): {"name": "水雷屯", "desc": "元亨利貞", "judgment": "平", "meaning": "萬事起頭難，需要耐心"},
        (1, 2): {"name": "山水蒙", "desc": "亨，匪我求童蒙", "judgment": "平", "meaning": "啟蒙教育，循序漸進"},
        (2, 7): {"name": "水天需", "desc": "有孚，光亨", "judgment": "吉", "meaning": "等待時機，誠信則亨"},
        (7, 2): {"name": "天水訟", "desc": "有孚窒惕，中吉", "judgment": "凶", "meaning": "爭訟不利，宜和解"},
        (0, 2): {"name": "地水師", "desc": "貞，丈人吉", "judgment": "平", "meaning": "統帥之道，需正義"},
        (2, 0): {"name": "水地比", "desc": "吉，原筮", "judgment": "吉", "meaning": "親附輔助，團結一致"},
        # 更多卦象... (簡化版，實際應包含全部64卦)
        (7, 3): {"name": "天風姤", "desc": "女壯，勿用取女", "judgment": "凶", "meaning": "陰長陽消，需防小人"},
        (3, 7): {"name": "風天小畜", "desc": "亨", "judgment": "平", "meaning": "小有積蓄，未能大成"},
        (7, 0): {"name": "天地否", "desc": "否之匪人", "judgment": "凶", "meaning": "閉塞不通，天地不交"},
        (0, 7): {"name": "地天泰", "desc": "小往大來", "judgment": "吉", "meaning": "通泰吉祥，天地交泰"},
    }

    # 六親
    LIUQIN = ["父母", "兄弟", "子孫", "妻財", "官鬼"]

    # 六獸
    LIUSHOU = ["青龍", "朱雀", "勾陳", "螣蛇", "白虎", "玄武"]

    def __init__(self, divination_time: datetime, method: str = "時間起卦"):
        """
        初始化六爻計算器

        Args:
            divination_time: 占卜時間
            method: 起卦方法（"時間起卦", "手搖銅錢", "數字起卦"）
        """
        self.divination_time = divination_time
        self.method = method

    def shake_coins(self) -> Tuple[int, bool]:
        """
        模擬搖銅錢法
        三個銅錢，正面為3，背面為2
        三個正面=9（老陽，動爻，記為"—○"）
        三個背面=6（老陰，動爻，記為"- -×"）
        兩正一背=8（少陰，記為"- -"）
        兩背一正=7（少陽，記為"—"）

        Returns:
            (數值, 是否為動爻)
        """
        coins = [random.choice([2, 3]) for _ in range(3)]
        total = sum(coins)

        # 判斷陰陽和動靜
        if total == 9:  # 老陽（動）
            return (1, True)  # 1代表陽爻
        elif total == 6:  # 老陰（動）
            return (0, True)  # 0代表陰爻
        elif total == 8:  # 少陰（靜）
            return (0, False)
        else:  # total == 7, 少陽（靜）
            return (1, False)

    def cast_hexagram_by_coins(self) -> Tuple[List[int], List[bool]]:
        """
        通過搖銅錢起卦（六次）

        Returns:
            (六爻列表，動爻標記列表)
        """
        yaos = []
        changing_yaos = []

        for _ in range(6):
            yao, is_changing = self.shake_coins()
            yaos.append(yao)
            changing_yaos.append(is_changing)

        return yaos, changing_yaos

    def cast_hexagram_by_time(self, dt: datetime) -> Tuple[List[int], List[bool]]:
        """
        通過時間起卦

        Args:
            dt: 占卜時間

        Returns:
            (六爻列表，動爻標記列表)
        """
        # 使用年月日時的數字
        year = dt.year
        month = dt.month
        day = dt.day
        hour = dt.hour

        # 計算上卦（年+月+日除以8取餘）
        upper = (year + month + day) % 8

        # 計算下卦（年+月+日+時除以8取餘）
        lower = (year + month + day + hour) % 8

        # 計算動爻（年+月+日+時除以6取餘）
        changing_line = (year + month + day + hour) % 6
        if changing_line == 0:
            changing_line = 6

        # 將卦象轉換為六爻
        # 上卦（外卦）佔第4-6爻，下卦（內卦）佔第1-3爻
        upper_binary = format(upper, '03b')
        lower_binary = format(lower, '03b')

        yaos = [int(b) for b in lower_binary] + [int(b) for b in upper_binary]

        # 標記動爻
        changing_yaos = [i == (changing_line - 1) for i in range(6)]

        return yaos, changing_yaos

    def cast_hexagram_by_numbers(self, num1: int, num2: int, num3: int = None) -> Tuple[List[int], List[bool]]:
        """
        通過數字起卦

        Args:
            num1: 第一個數字（上卦）
            num2: 第二個數字（下卦）
            num3: 第三個數字（動爻），可選

        Returns:
            (六爻列表，動爻標記列表)
        """
        upper = num1 % 8
        lower = num2 % 8

        if num3 is not None:
            changing_line = num3 % 6
            if changing_line == 0:
                changing_line = 6
        else:
            changing_line = (num1 + num2) % 6
            if changing_line == 0:
                changing_line = 6

        # 將卦象轉換為六爻
        upper_binary = format(upper, '03b')
        lower_binary = format(lower, '03b')

        yaos = [int(b) for b in lower_binary] + [int(b) for b in upper_binary]
        changing_yaos = [i == (changing_line - 1) for i in range(6)]

        return yaos, changing_yaos

    def get_bagua_from_yaos(self, yaos: List[int], start_idx: int) -> int:
        """
        從六爻中提取八卦索引

        Args:
            yaos: 六爻列表
            start_idx: 起始索引（0為下卦，3為上卦）

        Returns:
            八卦索引（0-7）
        """
        trigram_yaos = yaos[start_idx:start_idx + 3]
        bagua_index = int(''.join(map(str, trigram_yaos)), 2)
        return bagua_index

    def get_hexagram_info(self, upper_bagua_idx: int, lower_bagua_idx: int) -> Dict[str, Any]:
        """
        獲取卦象資訊

        Args:
            upper_bagua_idx: 上卦索引
            lower_bagua_idx: 下卦索引

        Returns:
            卦象詳細資訊
        """
        hex_key = (upper_bagua_idx, lower_bagua_idx)

        if hex_key in self.HEXAGRAMS:
            hex_info = self.HEXAGRAMS[hex_key]
        else:
            # 如果沒有定義，返回基本資訊
            upper_gua = self.BAGUA[upper_bagua_idx]
            lower_gua = self.BAGUA[lower_bagua_idx]
            hex_info = {
                "name": f"{upper_gua['name']}{lower_gua['name']}",
                "desc": "待解析",
                "judgment": "平",
                "meaning": "此卦組合需進一步分析"
            }

        return {
            **hex_info,
            "upper_gua": self.BAGUA[upper_bagua_idx],
            "lower_gua": self.BAGUA[lower_bagua_idx]
        }

    def get_changing_hexagram(self, original_yaos: List[int], changing_yaos: List[bool]) -> List[int]:
        """
        計算變卦

        Args:
            original_yaos: 原始六爻
            changing_yaos: 動爻標記

        Returns:
            變卦的六爻
        """
        changed_yaos = original_yaos.copy()
        for i, is_changing in enumerate(changing_yaos):
            if is_changing:
                changed_yaos[i] = 1 - changed_yaos[i]  # 陰變陽，陽變陰

        return changed_yaos

    def assign_liuqin(self, yaos: List[int], ri_gan: str) -> List[Dict[str, Any]]:
        """
        配置六親（簡化版）

        Args:
            yaos: 六爻列表
            ri_gan: 日干

        Returns:
            六親配置列表
        """
        # 簡化的六親分配
        liuqin_assignment = []
        yao_names = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"]

        for i, yao in enumerate(yaos):
            liuqin_index = i % len(self.LIUQIN)
            liushou_index = i % len(self.LIUSHOU)

            liuqin_assignment.append({
                "position": i + 1,
                "name": yao_names[i],
                "yao_type": "陽爻(—)" if yao == 1 else "陰爻(- -)",
                "liuqin": self.LIUQIN[liuqin_index],
                "liushou": self.LIUSHOU[liushou_index]
            })

        return liuqin_assignment

    def interpret_hexagram(self, hex_info: Dict[str, Any], changing_yaos: List[bool]) -> str:
        """
        解釋卦象吉凶

        Args:
            hex_info: 卦象資訊
            changing_yaos: 動爻標記

        Returns:
            解釋文字
        """
        # 統計動爻數量
        num_changing = sum(changing_yaos)

        if num_changing == 0:
            interpretation = f"卦象為{hex_info['name']}，無動爻，以本卦斷。{hex_info['meaning']}"
        elif num_changing == 1:
            changing_position = changing_yaos.index(True) + 1
            yao_names = ["初", "二", "三", "四", "五", "上"]
            interpretation = f"卦象為{hex_info['name']}，{yao_names[changing_position-1]}爻動。{hex_info['meaning']}需注意變化。"
        elif num_changing == 2:
            interpretation = f"卦象為{hex_info['name']}，兩爻動，吉凶參半，需綜合判斷。"
        elif num_changing >= 3:
            interpretation = f"卦象為{hex_info['name']}，多爻動，變化劇烈，以變卦為主斷。"

        return interpretation

    def analyze(self) -> Dict[str, Any]:
        """
        執行完整的六爻占卜分析

        Returns:
            完整的六爻占卜結果
        """
        # 根據方法起卦
        if self.method == "手搖銅錢":
            yaos, changing_yaos = self.cast_hexagram_by_coins()
        elif self.method == "時間起卦":
            yaos, changing_yaos = self.cast_hexagram_by_time(self.divination_time)
        elif self.method == "數字起卦":
            # 使用時間作為數字源
            num1 = self.divination_time.year + self.divination_time.month
            num2 = self.divination_time.day + self.divination_time.hour
            yaos, changing_yaos = self.cast_hexagram_by_numbers(num1, num2)
        else:
            yaos, changing_yaos = self.cast_hexagram_by_time(self.divination_time)

        # 獲取上下卦
        lower_bagua_idx = self.get_bagua_from_yaos(yaos, 0)
        upper_bagua_idx = self.get_bagua_from_yaos(yaos, 3)

        # 獲取本卦資訊
        ben_gua = self.get_hexagram_info(upper_bagua_idx, lower_bagua_idx)

        # 計算變卦
        changed_yaos = self.get_changing_hexagram(yaos, changing_yaos)
        changed_lower = self.get_bagua_from_yaos(changed_yaos, 0)
        changed_upper = self.get_bagua_from_yaos(changed_yaos, 3)
        bian_gua = self.get_hexagram_info(changed_upper, changed_lower)

        # 配置六親六獸（簡化版）
        ri_gan = "甲"  # 簡化處理
        liuqin_config = self.assign_liuqin(yaos, ri_gan)

        # 標記動爻
        for i, yao_info in enumerate(liuqin_config):
            yao_info["is_changing"] = changing_yaos[i]

        # 解釋卦象
        interpretation = self.interpret_hexagram(ben_gua, changing_yaos)

        # 綜合判斷
        if ben_gua.get("judgment") == "吉":
            overall_judgment = "吉利"
        elif ben_gua.get("judgment") == "凶":
            overall_judgment = "不利"
        else:
            overall_judgment = "平穩"

        # 統計動爻
        num_changing = sum(changing_yaos)
        if num_changing > 0:
            overall_judgment += f"，有{num_changing}爻動，事態有變"

        return {
            "divination_time": self.divination_time.strftime("%Y-%m-%d %H:%M:%S"),
            "method": self.method,
            "ben_gua": {
                "name": ben_gua["name"],
                "upper_gua": ben_gua["upper_gua"],
                "lower_gua": ben_gua["lower_gua"],
                "description": ben_gua["desc"],
                "judgment": ben_gua["judgment"],
                "meaning": ben_gua["meaning"]
            },
            "bian_gua": {
                "name": bian_gua["name"],
                "upper_gua": bian_gua["upper_gua"],
                "lower_gua": bian_gua["lower_gua"],
                "description": bian_gua["desc"],
                "judgment": bian_gua["judgment"],
                "meaning": bian_gua["meaning"]
            },
            "yaos": yaos,
            "changing_yaos": changing_yaos,
            "liuqin_config": liuqin_config,
            "num_changing_yaos": num_changing,
            "interpretation": interpretation,
            "overall_judgment": overall_judgment,
            "display": self.generate_display(yaos, changing_yaos, ben_gua, bian_gua)
        }

    def generate_display(self, yaos: List[int], changing_yaos: List[bool],
                         ben_gua: Dict, bian_gua: Dict) -> str:
        """
        生成卦象顯示

        Returns:
            卦象文字顯示
        """
        yao_names = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"]
        display_lines = []

        display_lines.append(f"\n本卦：{ben_gua['name']} ({ben_gua['upper_gua']['trigram']}{ben_gua['lower_gua']['trigram']})")
        display_lines.append(f"變卦：{bian_gua['name']} ({bian_gua['upper_gua']['trigram']}{bian_gua['lower_gua']['trigram']})\n")

        # 從上到下顯示六爻（第6爻到第1爻）
        for i in range(5, -1, -1):
            yao = yaos[i]
            is_changing = changing_yaos[i]

            if yao == 1:
                yao_symbol = "━━━" if not is_changing else "━━━ ○"
            else:
                yao_symbol = "━  ━" if not is_changing else "━  ━ ×"

            display_lines.append(f"{yao_names[i]}: {yao_symbol}")

        return "\n".join(display_lines)


def test_liuyao():
    """測試函數"""
    test_time = datetime(2025, 10, 30, 14, 30)

    print("="*80)
    print("六爻占卜測試")
    print("="*80)
    print(f"\n占卜時間：{test_time.strftime('%Y年%m月%d日 %H:%M')}")

    # 測試時間起卦法
    calculator = LiuyaoCalculator(test_time, method="時間起卦")
    result = calculator.analyze()

    print(f"\n📅 起卦資訊：")
    print(f"   方法：{result['method']}")
    print(f"   時間：{result['divination_time']}")

    print(f"\n🎯 本卦：{result['ben_gua']['name']}")
    print(f"   上卦：{result['ben_gua']['upper_gua']['name']}（{result['ben_gua']['upper_gua']['trigram']}）- {result['ben_gua']['upper_gua']['nature']}")
    print(f"   下卦：{result['ben_gua']['lower_gua']['name']}（{result['ben_gua']['lower_gua']['trigram']}）- {result['ben_gua']['lower_gua']['nature']}")
    print(f"   卦辭：{result['ben_gua']['description']}")
    print(f"   釋義：{result['ben_gua']['meaning']}")
    print(f"   判斷：{result['ben_gua']['judgment']}")

    print(f"\n🔄 變卦：{result['bian_gua']['name']}")
    print(f"   卦辭：{result['bian_gua']['description']}")
    print(f"   釋義：{result['bian_gua']['meaning']}")

    print(f"\n🎲 動爻：{result['num_changing_yaos']}爻動")

    print(result['display'])

    print(f"\n✨ 解釋：")
    print(f"   {result['interpretation']}")

    print(f"\n📊 綜合判斷：{result['overall_judgment']}")


if __name__ == "__main__":
    test_liuyao()

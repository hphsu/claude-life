"""
生命靈數計算模組 (Western Numerology Calculator)
基於畢達哥拉斯數字命理學系統
"""

from datetime import datetime
from typing import Dict, List, Any


class NumerologyCalculator:
    """生命靈數計算器"""

    # 生命靈數特質 (1-9 和特殊數字 11, 22, 33)
    LIFE_PATH_MEANINGS = {
        1: {
            "name": "領導者",
            "keywords": ["獨立", "創新", "領導", "自信", "開創"],
            "positive": "獨立自主、創新能力強、有領導才能、勇於開創新局",
            "negative": "過於自我、獨斷專行、不善妥協、孤獨",
            "career": "企業家、管理者、發明家、設計師",
            "challenge": "學習合作與傾聽他人意見"
        },
        2: {
            "name": "協調者",
            "keywords": ["和平", "合作", "敏感", "外交", "平衡"],
            "positive": "善於協調、細膩敏感、重視和諧、有外交手腕",
            "negative": "過於敏感、優柔寡斷、依賴他人、缺乏自信",
            "career": "外交官、顧問、心理諮商師、調解員",
            "challenge": "建立自信與果斷決策能力"
        },
        3: {
            "name": "創作者",
            "keywords": ["創意", "表達", "樂觀", "社交", "藝術"],
            "positive": "創意豐富、善於表達、樂觀開朗、社交能力強",
            "negative": "散漫無序、三分鐘熱度、過於樂觀、不切實際",
            "career": "藝術家、作家、演員、設計師、講師",
            "challenge": "培養專注力與紀律"
        },
        4: {
            "name": "建設者",
            "keywords": ["穩定", "務實", "組織", "紀律", "可靠"],
            "positive": "務實穩重、組織能力強、有紀律、值得信賴",
            "negative": "過於死板、缺乏彈性、保守固執、壓抑情感",
            "career": "工程師、會計師、建築師、項目經理",
            "challenge": "學習靈活變通與享受生活"
        },
        5: {
            "name": "冒險家",
            "keywords": ["自由", "變化", "冒險", "多才", "好奇"],
            "positive": "熱愛自由、適應力強、多才多藝、勇於冒險",
            "negative": "不安定、缺乏耐心、衝動魯莽、無法承諾",
            "career": "旅行家、記者、銷售員、企業家",
            "challenge": "學習專注與承諾"
        },
        6: {
            "name": "照顧者",
            "keywords": ["責任", "愛心", "家庭", "服務", "和諧"],
            "positive": "富有愛心、重視家庭、負責任、樂於助人",
            "negative": "過度付出、控制慾強、容易焦慮、期望過高",
            "career": "教師、護士、諮商師、社工、餐飲業",
            "challenge": "學習放手與照顧自己"
        },
        7: {
            "name": "追尋者",
            "keywords": ["智慧", "靈性", "分析", "獨處", "神秘"],
            "positive": "善於分析、追求真理、有靈性深度、智慧獨特",
            "negative": "過於孤僻、難以親近、過度分析、逃避現實",
            "career": "研究員、哲學家、心理學家、神秘學家",
            "challenge": "學習信任與情感表達"
        },
        8: {
            "name": "成就者",
            "keywords": ["權力", "財富", "成就", "權威", "物質"],
            "positive": "事業心強、善於理財、有權威感、追求成就",
            "negative": "工作狂、物質主義、控制慾強、忽略家庭",
            "career": "企業家、金融家、CEO、投資家",
            "challenge": "平衡物質與精神生活"
        },
        9: {
            "name": "完成者",
            "keywords": ["人道", "博愛", "理想", "完成", "智慧"],
            "positive": "富有同情心、胸懷寬廣、理想主義、智慧成熟",
            "negative": "過於理想化、難以放下、情緒化、自我犧牲",
            "career": "慈善家、藝術家、教師、靈性導師",
            "challenge": "學習實際與照顧自己"
        },
        11: {
            "name": "靈性使者（大師數）",
            "keywords": ["直覺", "靈感", "啟發", "理想", "敏感"],
            "positive": "直覺力強、有靈性天賦、能啟發他人、理想崇高",
            "negative": "過度敏感、神經質、理想與現實衝突、壓力大",
            "career": "靈性導師、心靈作家、藝術家、演說家",
            "challenge": "腳踏實地並管理高度敏感性"
        },
        22: {
            "name": "大師建造者（大師數）",
            "keywords": ["願景", "實現", "領導", "宏大", "務實"],
            "positive": "有宏大願景、能將理想實現、領導能力卓越",
            "negative": "壓力過大、期望過高、完美主義、工作狂",
            "career": "企業領袖、建築大師、政治家、社會改革者",
            "challenge": "平衡理想與現實，避免過度壓力"
        },
        33: {
            "name": "大師教師（大師數）",
            "keywords": ["奉獻", "教導", "療癒", "愛", "犧牲"],
            "positive": "無私奉獻、療癒能力、大愛精神、啟發眾生",
            "negative": "自我犧牲過度、殉道心態、忽略自身需求",
            "career": "靈性教師、療癒師、慈善領袖、人道工作者",
            "challenge": "在奉獻中不失去自我"
        }
    }

    # 命運數含義（與生命靈數相似但側重點不同）
    DESTINY_MEANINGS = {
        1: "天生領導者，命運要你開創新局、獨立自主",
        2: "天生協調者，命運要你促進和平、建立關係",
        3: "天生創作者，命運要你表達自我、激發創意",
        4: "天生建設者，命運要你建立秩序、創造穩定",
        5: "天生探險家，命運要你體驗自由、擁抱變化",
        6: "天生照顧者，命運要你服務他人、創造和諧",
        7: "天生哲學家，命運要你追尋真理、探索奧秘",
        8: "天生領導者，命運要你創造成就、掌握資源",
        9: "天生人道主義者，命運要你服務眾生、完成使命",
        11: "天生靈性導師，命運要你啟發他人、傳播光明",
        22: "天生大師級建造者，命運要你實現偉大願景",
        33: "天生大師級教師，命運要你以大愛療癒世界"
    }

    # 靈魂數含義（內在驅動力）
    SOUL_MEANINGS = {
        1: "內心渴望獨立自主、成為第一",
        2: "內心渴望和諧關係、情感連結",
        3: "內心渴望創意表達、歡樂分享",
        4: "內心渴望穩定安全、建立秩序",
        5: "內心渴望自由探索、新鮮體驗",
        6: "內心渴望愛與被愛、照顧他人",
        7: "內心渴望真理智慧、心靈寧靜",
        8: "內心渴望成就權力、物質豐盛",
        9: "內心渴望理想實現、服務人類",
        11: "內心渴望靈性啟發、光明傳遞",
        22: "內心渴望偉大成就、改變世界",
        33: "內心渴望無私奉獻、療癒眾生"
    }

    def __init__(self, birth_date: datetime, full_name: str = ""):
        """
        初始化生命靈數計算器

        Args:
            birth_date: 出生日期
            full_name: 全名（用於計算命運數和靈魂數，可選）
        """
        self.birth_date = birth_date
        self.full_name = full_name

    def reduce_to_single_digit(self, number: int, allow_master_numbers: bool = True) -> int:
        """
        將數字化簡為個位數（保留大師數 11, 22, 33）

        Args:
            number: 要化簡的數字
            allow_master_numbers: 是否保留大師數

        Returns:
            化簡後的數字
        """
        # 如果是大師數且允許保留，直接返回
        if allow_master_numbers and number in [11, 22, 33]:
            return number

        # 持續相加直到變成個位數
        while number > 9:
            number = sum(int(digit) for digit in str(number))
            # 檢查是否變成大師數
            if allow_master_numbers and number in [11, 22, 33]:
                return number

        return number

    def calculate_life_path_number(self) -> Dict[str, Any]:
        """
        計算生命靈數（Life Path Number）
        基於出生日期：年月日分別化簡後相加

        Returns:
            生命靈數及其含義
        """
        year = self.birth_date.year
        month = self.birth_date.month
        day = self.birth_date.day

        # 將年月日分別化簡
        year_reduced = self.reduce_to_single_digit(year)
        month_reduced = self.reduce_to_single_digit(month)
        day_reduced = self.reduce_to_single_digit(day)

        # 相加後再次化簡
        total = year_reduced + month_reduced + day_reduced
        life_path = self.reduce_to_single_digit(total)

        return {
            "number": life_path,
            "calculation": f"{year} → {year_reduced}, {month} → {month_reduced}, {day} → {day_reduced} → {year_reduced}+{month_reduced}+{day_reduced} = {life_path}",
            "meaning": self.LIFE_PATH_MEANINGS.get(life_path, {}),
            "is_master_number": life_path in [11, 22, 33]
        }

    def calculate_destiny_number(self) -> Dict[str, Any]:
        """
        計算命運數（Destiny/Expression Number）
        基於全名的字母數值總和（需要英文名）

        Returns:
            命運數及其含義
        """
        if not self.full_name:
            return {
                "number": None,
                "calculation": "需要提供英文全名",
                "meaning": {}
            }

        # 字母對應數值表（畢達哥拉斯系統）
        letter_values = {
            'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
            'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
            'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
        }

        # 計算全名的數值總和
        total = 0
        calculation_steps = []
        for char in self.full_name.upper():
            if char.isalpha():
                value = letter_values.get(char, 0)
                total += value
                calculation_steps.append(f"{char}={value}")

        destiny = self.reduce_to_single_digit(total)

        return {
            "number": destiny,
            "calculation": f"{' + '.join(calculation_steps)} = {total} → {destiny}",
            "meaning": self.DESTINY_MEANINGS.get(destiny, "需進一步分析"),
            "is_master_number": destiny in [11, 22, 33]
        }

    def calculate_soul_urge_number(self) -> Dict[str, Any]:
        """
        計算靈魂數（Soul Urge/Heart's Desire Number）
        基於全名中的母音

        Returns:
            靈魂數及其含義
        """
        if not self.full_name:
            return {
                "number": None,
                "calculation": "需要提供英文全名",
                "meaning": ""
            }

        letter_values = {
            'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
            'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
            'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
        }

        vowels = set('AEIOUY')

        # 只計算母音
        total = 0
        calculation_steps = []
        for char in self.full_name.upper():
            if char in vowels:
                value = letter_values.get(char, 0)
                total += value
                calculation_steps.append(f"{char}={value}")

        soul = self.reduce_to_single_digit(total)

        return {
            "number": soul,
            "calculation": f"{' + '.join(calculation_steps)} = {total} → {soul}",
            "meaning": self.SOUL_MEANINGS.get(soul, "需進一步分析"),
            "is_master_number": soul in [11, 22, 33]
        }

    def calculate_personality_number(self) -> Dict[str, Any]:
        """
        計算人格數（Personality Number）
        基於全名中的子音

        Returns:
            人格數及其含義
        """
        if not self.full_name:
            return {
                "number": None,
                "calculation": "需要提供英文全名",
                "meaning": ""
            }

        letter_values = {
            'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
            'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
            'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
        }

        vowels = set('AEIOUY')

        # 只計算子音
        total = 0
        calculation_steps = []
        for char in self.full_name.upper():
            if char.isalpha() and char not in vowels:
                value = letter_values.get(char, 0)
                total += value
                calculation_steps.append(f"{char}={value}")

        personality = self.reduce_to_single_digit(total)

        return {
            "number": personality,
            "calculation": f"{' + '.join(calculation_steps)} = {total} → {personality}",
            "meaning": f"外在展現的數字{personality}特質",
            "is_master_number": personality in [11, 22, 33]
        }

    def calculate_birth_day_number(self) -> Dict[str, Any]:
        """
        計算生日數（Birth Day Number）
        直接基於出生日期的日數

        Returns:
            生日數及其含義
        """
        day = self.birth_date.day
        birth_day = self.reduce_to_single_digit(day)

        return {
            "number": birth_day,
            "original_day": day,
            "calculation": f"{day} → {birth_day}",
            "meaning": f"天賦才能的數字{birth_day}特質",
            "is_master_number": birth_day in [11, 22, 33]
        }

    def analyze(self) -> Dict[str, Any]:
        """
        執行完整的生命靈數分析

        Returns:
            完整的生命靈數分析結果
        """
        # 計算各種核心數字
        life_path = self.calculate_life_path_number()
        destiny = self.calculate_destiny_number()
        soul_urge = self.calculate_soul_urge_number()
        personality = self.calculate_personality_number()
        birth_day = self.calculate_birth_day_number()

        # 統計大師數
        master_numbers = []
        if life_path["is_master_number"]:
            master_numbers.append(f"生命靈數 {life_path['number']}")
        if destiny["number"] and destiny["is_master_number"]:
            master_numbers.append(f"命運數 {destiny['number']}")
        if soul_urge["number"] and soul_urge["is_master_number"]:
            master_numbers.append(f"靈魂數 {soul_urge['number']}")

        # 綜合分析
        core_summary = f"生命靈數 {life_path['number']} - {life_path['meaning'].get('name', '未知')}"
        if master_numbers:
            core_summary += f"（擁有大師數：{', '.join(master_numbers)}）"

        return {
            "birth_date": self.birth_date.strftime("%Y-%m-%d"),
            "full_name": self.full_name if self.full_name else "未提供",
            "core_numbers": {
                "life_path": life_path,
                "destiny": destiny,
                "soul_urge": soul_urge,
                "personality": personality,
                "birth_day": birth_day
            },
            "master_numbers": master_numbers if master_numbers else ["無"],
            "summary": core_summary,
            "primary_traits": life_path["meaning"].get("keywords", []),
            "life_purpose": life_path["meaning"].get("positive", ""),
            "challenges": life_path["meaning"].get("challenge", ""),
            "suitable_careers": life_path["meaning"].get("career", "")
        }


def test_numerology():
    """測試函數"""
    # 測試範例
    test_date = datetime(1990, 5, 15)
    test_name = "John Smith"

    print("="*80)
    print("生命靈數測試")
    print("="*80)
    print(f"\n出生日期：{test_date.strftime('%Y年%m月%d日')}")
    print(f"英文姓名：{test_name}")

    calculator = NumerologyCalculator(test_date, test_name)
    result = calculator.analyze()

    print(f"\n📊 核心數字：")
    print(f"   生命靈數（Life Path）：{result['core_numbers']['life_path']['number']}")
    print(f"   計算：{result['core_numbers']['life_path']['calculation']}")
    print(f"   命運數（Destiny）：{result['core_numbers']['destiny']['number']}")
    print(f"   靈魂數（Soul Urge）：{result['core_numbers']['soul_urge']['number']}")
    print(f"   人格數（Personality）：{result['core_numbers']['personality']['number']}")
    print(f"   生日數（Birth Day）：{result['core_numbers']['birth_day']['number']}")

    print(f"\n✨ 大師數：{', '.join(result['master_numbers'])}")

    print(f"\n🎯 核心特質：")
    lp_meaning = result['core_numbers']['life_path']['meaning']
    print(f"   類型：{lp_meaning.get('name', '未知')}")
    print(f"   關鍵字：{', '.join(lp_meaning.get('keywords', []))}")
    print(f"   正面特質：{lp_meaning.get('positive', '')}")
    print(f"   負面特質：{lp_meaning.get('negative', '')}")
    print(f"   適合職業：{lp_meaning.get('career', '')}")
    print(f"   人生挑戰：{lp_meaning.get('challenge', '')}")


if __name__ == "__main__":
    test_numerology()

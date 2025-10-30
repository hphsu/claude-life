"""
姓名學計算模組 (Chinese Name Analysis Calculator)
基於五格剖象法和姓名筆畫數理
"""

from typing import Dict, List, Any


class NameAnalysisCalculator:
    """姓名學計算器"""

    # 姓名學數理吉凶表 (1-81)
    SHULI_MEANINGS = {
        1: {"luck": "大吉", "meaning": "天地開泰萬物生", "desc": "天地開泰，萬物成形，繁榮昌隆，有領導力"},
        2: {"luck": "凶", "meaning": "混沌未定終歸分", "desc": "混沌未定，分離破敗，事業不順，需要依靠他人"},
        3: {"luck": "大吉", "meaning": "立身出世權威重", "desc": "智慧仁勇，意志堅固，建立事業，名利雙收"},
        4: {"luck": "凶", "meaning": "破敗凶變萬事休", "desc": "日被雲遮，苦難折磨，非有毅力，難望成功"},
        5: {"luck": "大吉", "meaning": "福祿長壽陰陽和", "desc": "陰陽和合，精神愉快，榮譽達利，一門興隆"},
        6: {"luck": "大吉", "meaning": "安穩餘慶福祿開", "desc": "天德地祥，福祿豐厚，平安幸福，名利雙收"},
        7: {"luck": "吉", "meaning": "剛毅果敢獨立權", "desc": "精力旺盛，頭腦明敏，克服萬難，必獲成功"},
        8: {"luck": "大吉", "meaning": "志剛意健勤勉興", "desc": "意志如鐵，富於進取，突破萬難，必獲成功"},
        9: {"luck": "凶", "meaning": "興盡凶始困苦多", "desc": "雖有才能，有志難伸，缺乏領導才能，難成大業"},
        10: {"luck": "凶", "meaning": "萬物終局充滿損", "desc": "黑暗之境，空虛無物，前途不明，災難重重"},
        11: {"luck": "大吉", "meaning": "草木逢春枯木逢", "desc": "陰陽復新，家運隆昌，萬事如意，享天賦幸運"},
        12: {"luck": "凶", "meaning": "薄弱無力孤立無", "desc": "家庭緣薄，孤獨遭難，謀事不達，悲慘不堪"},
        13: {"luck": "大吉", "meaning": "智略超群博學多", "desc": "天賦幸運，能得人望，善用智慧，必獲成功"},
        14: {"luck": "凶", "meaning": "淪落天涯失意煩", "desc": "家庭緣薄，孤獨受苦，謀事不成，前途暗淡"},
        15: {"luck": "大吉", "meaning": "福壽圓滿財帛豐", "desc": "福壽圓滿，富貴榮譽，涵養雅量，德高望重"},
        16: {"luck": "大吉", "meaning": "貴人多助成大業", "desc": "反凶化吉，得貴人助，可成大業，富貴榮達"},
        17: {"luck": "大吉", "meaning": "突破萬難權威高", "desc": "權威剛強，意志堅定，突破萬難，必獲成功"},
        18: {"luck": "大吉", "meaning": "有志竟成功名就", "desc": "經商做事，順利昌隆，如能慎始，百事亨通"},
        21: {"luck": "大吉", "meaning": "明月中天光輝照", "desc": "光風霽月，萬物確立，官運亨通，大搏名利"},
        23: {"luck": "大吉", "meaning": "旭日東昇發育茂", "desc": "偉大昌隆，威震四方，名利俱全，領導眾人"},
        24: {"luck": "大吉", "meaning": "錦繡前程靠自立", "desc": "家門餘慶，金錢豐盈，白手成家，財源廣進"},
        25: {"luck": "大吉", "meaning": "資性英敏剛毅果", "desc": "資性英敏，有奇特才能，克服傲慢，成功可期"},
        29: {"luck": "大吉", "meaning": "智謀兼備成大業", "desc": "智謀優秀，財力歸集，名聞海內，成就大業"},
        31: {"luck": "大吉", "meaning": "智仁勇全得人望", "desc": "智仁勇俱備，意志堅固，千載一遇，博得名利"},
        32: {"luck": "大吉", "meaning": "僥倖多能意外惠", "desc": "僥倖多望，貴人多助，財源廣進，繁榮至上"},
        33: {"luck": "大吉", "meaning": "家門隆昌才德開", "desc": "家門隆昌，才德開展，智謀奇略，成就大業"},
        35: {"luck": "大吉", "meaning": "溫和平靜優雅開", "desc": "溫和平靜，智達通暢，文昌技藝，奏功洋洋"},
        37: {"luck": "大吉", "meaning": "權威顯達猛虎出", "desc": "獨立權威，忠誠可嘉，能成大業，功名顯達"},
        39: {"luck": "大吉", "meaning": "富貴榮華權威重", "desc": "富貴榮華，財帛豐盈，暗藏險象，德澤四方"},
        41: {"luck": "大吉", "meaning": "德望高大事事成", "desc": "德高望重，有實力，智謀兼備，可成大業"},
        45: {"luck": "大吉", "meaning": "順風揚帆新事業", "desc": "順風揚帆，有智謀，經緯事業，必獲成功"},
        47: {"luck": "大吉", "meaning": "有貴人助成大業", "desc": "貴人相助，可成大業，雖遇困難，浮沉不定"},
        48: {"luck": "大吉", "meaning": "智謀兼備有德能", "desc": "智謀兼備，德量榮達，威望成師，洋洋大觀"},
        52: {"luck": "大吉", "meaning": "先見之明實現志", "desc": "眼光遠大，理想實現，有計劃力，能成大業"},
        # 凶數
        19: {"luck": "凶", "meaning": "風雲遮日辛苦重", "desc": "風云蔽日，辛苦重來，雖有智謀，萬事挫折"},
        20: {"luck": "凶", "meaning": "智高志大難望成", "desc": "智高志大，歷盡艱難，憂悶煩惱，進退兩難"},
        22: {"luck": "凶", "meaning": "秋草逢霜勞苦多", "desc": "秋草逢霜，懷才不遇，憂愁怨苦，事不如意"},
        26: {"luck": "凶", "meaning": "變怪奇異豪俠義", "desc": "變怪之謎，英雄豪傑，波瀾重疊，而奏大功"},
        27: {"luck": "凶", "meaning": "自我心強誹謗中", "desc": "自我心過強，多受誹謗攻擊，誹難亦能成功"},
        28: {"luck": "凶", "meaning": "豪傑氣概四海漂", "desc": "遭難運，豪傑氣概，四海飄泊，終世躁動"},
        30: {"luck": "半吉", "meaning": "沉浮不定成敗間", "desc": "一成一敗，絕處逢生，有智謀，成功可期"},
        34: {"luck": "凶", "meaning": "災難不絕辛苦多", "desc": "災難不絕，難望成功，此數大凶，不如更名"},
        36: {"luck": "凶", "meaning": "波瀾萬丈俠義薄", "desc": "波瀾重疊，常陷窮困，動不如靜，有才無命"},
        38: {"luck": "半吉", "meaning": "磨鐵成針意志強", "desc": "非無大志，實乏統率，難望成功，宜謹守為安"},
        40: {"luck": "凶", "meaning": "智謀膽力冒險投", "desc": "智謀膽力，冒險投機，沉浮不定，退保平安"},
        42: {"luck": "凶", "meaning": "寒蟬在柳十藝不", "desc": "博識多能，精通世情，如能專心，可望成功"},
        43: {"luck": "凶", "meaning": "散財破產外祥內", "desc": "外祥內苦，外緣雖好，內裡空虛，財難聚"},
        44: {"luck": "凶", "meaning": "難成大業破家財", "desc": "難成大業，外觀雖好，內在空虛，需有耐心"},
        46: {"luck": "凶", "meaning": "載寶沉舟苦難多", "desc": "載寶沉舟，浪裡淘金，大難嘗盡，終獲成功"},
        49: {"luck": "凶", "meaning": "吉凶互見一成一", "desc": "吉凶互見，一成一敗，凶中有吉，吉中有凶"},
        50: {"luck": "凶", "meaning": "小舟入海吉凶參", "desc": "小舟入海，吉凶參半，須防傾覆，凶多吉少"}
    }

    # 三才配置吉凶 (天格/人格/地格的五行組合)
    SANCAI_COMBINATIONS = {
        # 大吉組合
        ("木", "木", "木"): {"luck": "大吉", "desc": "同心同德，成功順利，能平安實現目的"},
        ("木", "木", "火"): {"luck": "大吉", "desc": "成功順調，向上發展，基礎安泰"},
        ("木", "火", "木"): {"luck": "大吉", "desc": "成功運佳，境遇安定，配置吉祥"},
        ("木", "火", "火"): {"luck": "大吉", "desc": "受上司之惠澤，向上順利發展"},
        ("木", "火", "土"): {"luck": "大吉", "desc": "得長輩或上司之惠助，成功順利發展"},
        ("火", "木", "木"): {"luck": "大吉", "desc": "成功順利，能平安達到目的"},
        ("火", "木", "火"): {"luck": "大吉", "desc": "成功運佳，向上發展容易達到目的"},
        ("火", "火", "木"): {"luck": "大吉", "desc": "盛運昌隆，成功發展，目的達成"},
        ("火", "火", "火"): {"luck": "吉", "desc": "積極進取，成功迅速，但需防急躁"},
        ("火", "火", "土"): {"luck": "大吉", "desc": "得上司惠澤，成功順利發展"},
        ("土", "火", "火"): {"luck": "大吉", "desc": "得祖輩或上司之惠助，可成功發展"},
        ("土", "火", "土"): {"luck": "大吉", "desc": "可得意外之大成功發展"},
        ("土", "土", "火"): {"luck": "大吉", "desc": "境遇安固，身心健康，可望長壽"},
        ("土", "土", "土"): {"luck": "大吉", "desc": "性情穩固，成功緩慢但平安"},
        ("金", "土", "土"): {"luck": "大吉", "desc": "承蒙上司引進，成功順利發展"},
        ("金", "土", "金"): {"luck": "大吉", "desc": "容易成功達到目的，境遇安固"},
        ("金", "金", "土"): {"luck": "大吉", "desc": "成功運佳，可達目的，境遇安泰"},
        ("金", "金", "金"): {"luck": "吉", "meaning": "成功順利，但需防過剛"},
        ("水", "金", "金"): {"luck": "大吉", "desc": "成功順利，能平安實現目的"},
        ("水", "金", "水"): {"luck": "大吉", "desc": "得長輩或上司之惠助，成功發展"},
        ("水", "水", "金"): {"luck": "大吉", "desc": "承父祖之蔭，成功運佳"},
        ("水", "水", "水"): {"luck": "吉", "desc": "成功運佳，但需防過於流動"},
        # 凶組合
        ("木", "土", "火"): {"luck": "凶", "desc": "成功運被壓抑，不能伸張"},
        ("木", "土", "土"): {"luck": "凶", "desc": "成功運被壓抑，不能有所伸張"},
        ("木", "金", "木"): {"luck": "凶", "desc": "雖可獲得發展，但基礎不穩"},
        ("木", "金", "金"): {"luck": "凶", "desc": "成功運被壓抑，不能成功"},
        ("火", "水", "木"): {"luck": "凶", "desc": "水火相克，配置不良"},
        ("火", "水", "火"): {"luck": "大凶", "desc": "水火相克，易遭災難"},
        ("火", "水", "水"): {"luck": "大凶", "desc": "水火不容，凶險萬分"},
        ("火", "金", "木"): {"luck": "凶", "desc": "雖有成功運，但基礎不穩"},
        ("土", "木", "木"): {"luck": "凶", "desc": "成功運被壓抑，不能有所伸張"},
        ("土", "木", "火"): {"luck": "凶", "desc": "雖可成功，但常受困擾"},
        ("土", "水", "火"): {"luck": "凶", "desc": "境遇不安，變動頻繁"},
        ("土", "水", "水"): {"luck": "凶", "desc": "成功運被壓抑，不能有所伸張"},
        ("金", "火", "木"): {"luck": "凶", "desc": "火克金，易生災禍"},
        ("金", "火", "火"): {"luck": "大凶", "desc": "火克金，凶險萬分"},
        ("金", "木", "木"): {"luck": "凶", "desc": "雖可成功，但常受挫折"},
        ("金", "木", "火"): {"luck": "凶", "desc": "雖可成功發展，但易生災變"},
        ("水", "土", "火"): {"luck": "凶", "desc": "土克水，成功運被壓抑"},
        ("水", "土", "土"): {"luck": "大凶", "desc": "土克水，難以成功"},
        ("水", "火", "木"): {"luck": "凶", "desc": "水火不容，易生災禍"},
        ("水", "火", "火"): {"luck": "大凶", "desc": "水火相克，凶險萬分"}
    }

    def __init__(self, name: str, gender: str = "男"):
        """
        初始化姓名分析計算器

        Args:
            name: 姓名（繁體或簡體中文）
            gender: 性別（"男" 或 "女"）
        """
        self.name = name
        self.gender = gender
        self.name_chars = list(name)

    def get_stroke_count(self, char: str) -> int:
        """
        獲取單個漢字的筆畫數（姓名學專用筆畫）
        這裡使用簡化版本，實際應用中需要完整的姓名學筆畫字典
        """
        # 常用姓氏筆畫（部分示例）
        common_surnames_strokes = {
            # 單姓
            "王": 4, "李": 7, "張": 11, "劉": 15, "陳": 16, "楊": 13, "黃": 12, "趙": 14,
            "周": 8, "吳": 7, "徐": 10, "孫": 10, "馬": 10, "朱": 6, "胡": 11, "郭": 15,
            "何": 7, "高": 10, "林": 8, "羅": 20, "鄭": 19, "梁": 11, "謝": 17, "宋": 7,
            "唐": 10, "許": 11, "韓": 17, "馮": 12, "鄧": 19, "曹": 11, "彭": 12, "曾": 12,
            "蕭": 19, "蔡": 17, "潘": 16, "田": 5, "董": 15, "袁": 10, "於": 8, "余": 7,
            "葉": 15, "蔣": 17, "杜": 7, "蘇": 22, "魏": 18, "程": 12, "呂": 7, "丁": 2,
            "沈": 8, "任": 6, "姚": 9, "盧": 16, "傅": 12, "鍾": 17, "汪": 8, "戴": 18,
            "崔": 11, "廖": 15, "賈": 13, "方": 4, "石": 5, "姜": 9, "邱": 12, "侯": 9,
            # 複姓
            "司馬": 15, "歐陽": 23, "上官": 11, "諸葛": 23, "東方": 12, "慕容": 24,
            # 名字常用字
            "偉": 11, "華": 14, "明": 8, "強": 12, "軍": 9, "建": 9, "國": 11, "文": 4,
            "志": 7, "勇": 9, "傑": 12, "鵬": 19, "龍": 16, "海": 11, "波": 9, "濤": 18,
            "宇": 6, "浩": 11, "宏": 7, "博": 12, "凱": 12, "雷": 13, "磊": 15, "峰": 10,
            "超": 12, "斌": 11, "輝": 15, "剛": 10, "平": 5, "飛": 9, "亮": 9, "東": 8,
            "雪": 11, "梅": 11, "麗": 19, "芳": 10, "玉": 5, "蘭": 23, "紅": 9, "秀": 7,
            "婷": 12, "娟": 10, "靜": 16, "瑩": 15, "敏": 11, "嬌": 15, "琳": 13, "穎": 16,
            "霞": 17, "燕": 16, "晶": 12, "妍": 7, "萍": 14, "莉": 13, "慧": 15, "艷": 24,
            "欣": 8, "怡": 9, "佳": 8, "琪": 13, "雅": 12, "婷": 12, "薇": 19, "瑤": 15,
            "子": 3, "一": 1, "之": 4, "天": 4, "心": 4, "成": 7, "安": 6, "仁": 4,
            "義": 13, "禮": 18, "智": 12, "信": 9, "德": 15, "福": 14, "祿": 13, "壽": 14,
            "喜": 12, "樂": 15, "和": 8, "平": 5, "吉": 6, "祥": 11, "順": 12, "達": 16
        }

        # 如果在字典中，返回對應筆畫
        if char in common_surnames_strokes:
            return common_surnames_strokes[char]

        # 否則使用簡化估算（實際應用需完整字典）
        # 這裡使用 Unicode 碼位的簡化估算
        code = ord(char)
        if 0x4E00 <= code <= 0x9FFF:  # CJK統一漢字
            # 簡化估算：根據部首複雜度
            return max(1, min(30, (code - 0x4E00) % 30 + 1))
        return 1

    def calculate_five_grids(self) -> Dict[str, Any]:
        """
        計算五格：天格、人格、地格、外格、總格

        Returns:
            五格配置字典
        """
        # 獲取姓名各字筆畫
        strokes = [self.get_stroke_count(char) for char in self.name_chars]

        # 根據姓名長度計算五格
        if len(self.name_chars) == 2:  # 單姓單名
            surname_stroke = strokes[0]
            name_stroke = strokes[1]

            tian_ge = surname_stroke + 1  # 天格
            ren_ge = surname_stroke + name_stroke  # 人格
            di_ge = name_stroke + 1  # 地格
            wai_ge = 2  # 外格
            zong_ge = surname_stroke + name_stroke  # 總格

        elif len(self.name_chars) == 3:  # 單姓雙名
            surname_stroke = strokes[0]
            name1_stroke = strokes[1]
            name2_stroke = strokes[2]

            tian_ge = surname_stroke + 1  # 天格
            ren_ge = surname_stroke + name1_stroke  # 人格
            di_ge = name1_stroke + name2_stroke  # 地格
            wai_ge = name2_stroke + 1  # 外格
            zong_ge = surname_stroke + name1_stroke + name2_stroke  # 總格

        elif len(self.name_chars) == 4:  # 複姓或複姓雙名
            # 假設前兩字為姓
            surname1_stroke = strokes[0]
            surname2_stroke = strokes[1]
            name1_stroke = strokes[2] if len(strokes) > 2 else 1
            name2_stroke = strokes[3] if len(strokes) > 3 else 1

            tian_ge = surname1_stroke + surname2_stroke  # 天格
            ren_ge = surname2_stroke + name1_stroke  # 人格
            di_ge = name1_stroke + name2_stroke  # 地格
            wai_ge = surname1_stroke + name2_stroke  # 外格
            zong_ge = sum(strokes)  # 總格
        else:
            # 其他情況的簡化處理
            tian_ge = strokes[0] + 1
            ren_ge = sum(strokes[:2]) if len(strokes) >= 2 else strokes[0] + 1
            di_ge = sum(strokes[1:]) + 1 if len(strokes) > 1 else strokes[0] + 1
            wai_ge = 2
            zong_ge = sum(strokes)

        # 確保數值在1-81範圍內
        tian_ge = ((tian_ge - 1) % 81) + 1
        ren_ge = ((ren_ge - 1) % 81) + 1
        di_ge = ((di_ge - 1) % 81) + 1
        wai_ge = ((wai_ge - 1) % 81) + 1
        zong_ge = ((zong_ge - 1) % 81) + 1

        return {
            "tian_ge": {
                "value": tian_ge,
                "meaning": self.get_shuli_meaning(tian_ge),
                "wuxing": self.get_wuxing(tian_ge)
            },
            "ren_ge": {
                "value": ren_ge,
                "meaning": self.get_shuli_meaning(ren_ge),
                "wuxing": self.get_wuxing(ren_ge)
            },
            "di_ge": {
                "value": di_ge,
                "meaning": self.get_shuli_meaning(di_ge),
                "wuxing": self.get_wuxing(di_ge)
            },
            "wai_ge": {
                "value": wai_ge,
                "meaning": self.get_shuli_meaning(wai_ge),
                "wuxing": self.get_wuxing(wai_ge)
            },
            "zong_ge": {
                "value": zong_ge,
                "meaning": self.get_shuli_meaning(zong_ge),
                "wuxing": self.get_wuxing(zong_ge)
            },
            "strokes": strokes
        }

    def get_wuxing(self, number: int) -> str:
        """
        根據數字尾數獲取五行屬性
        1-2: 木, 3-4: 火, 5-6: 土, 7-8: 金, 9-0: 水
        """
        last_digit = number % 10
        if last_digit in [1, 2]:
            return "木"
        elif last_digit in [3, 4]:
            return "火"
        elif last_digit in [5, 6]:
            return "土"
        elif last_digit in [7, 8]:
            return "金"
        else:  # 9, 0
            return "水"

    def get_shuli_meaning(self, number: int) -> Dict[str, str]:
        """獲取數理吉凶含義"""
        if number in self.SHULI_MEANINGS:
            return self.SHULI_MEANINGS[number]
        else:
            # 對於未定義的數字，返回中性評價
            return {
                "luck": "平",
                "meaning": "平常之數",
                "desc": "此數理含義尚需進一步研究"
            }

    def analyze_sancai(self, five_grids: Dict) -> Dict[str, Any]:
        """
        分析三才配置（天格、人格、地格的五行組合）
        """
        tian_wuxing = five_grids["tian_ge"]["wuxing"]
        ren_wuxing = five_grids["ren_ge"]["wuxing"]
        di_wuxing = five_grids["di_ge"]["wuxing"]

        combination = (tian_wuxing, ren_wuxing, di_wuxing)

        # 查找三才配置
        if combination in self.SANCAI_COMBINATIONS:
            sancai_result = self.SANCAI_COMBINATIONS[combination]
        else:
            # 分析五行生剋關係
            sancai_result = self.analyze_wuxing_relation(tian_wuxing, ren_wuxing, di_wuxing)

        return {
            "combination": f"{tian_wuxing}{ren_wuxing}{di_wuxing}",
            "tian_ge_wuxing": tian_wuxing,
            "ren_ge_wuxing": ren_wuxing,
            "di_ge_wuxing": di_wuxing,
            "luck": sancai_result.get("luck", "平"),
            "description": sancai_result.get("desc", "三才配置需進一步分析")
        }

    def analyze_wuxing_relation(self, tian: str, ren: str, di: str) -> Dict[str, str]:
        """
        分析三才五行生剋關係
        """
        # 五行相生：木→火→土→金→水→木
        # 五行相剋：木剋土、土剋水、水剋火、火剋金、金剋木
        sheng = {
            "木": "火", "火": "土", "土": "金", "金": "水", "水": "木"
        }
        ke = {
            "木": "土", "土": "水", "水": "火", "火": "金", "金": "木"
        }

        # 檢查天格→人格關係
        if sheng.get(tian) == ren:
            tian_ren = "相生（吉）"
        elif ke.get(tian) == ren:
            tian_ren = "相剋（凶）"
        elif tian == ren:
            tian_ren = "比和（平）"
        else:
            tian_ren = "無特殊關係"

        # 檢查人格→地格關係
        if sheng.get(ren) == di:
            ren_di = "相生（吉）"
        elif ke.get(ren) == di:
            ren_di = "相剋（凶）"
        elif ren == di:
            ren_di = "比和（平）"
        else:
            ren_di = "無特殊關係"

        # 綜合判斷
        if "相生" in tian_ren and "相生" in ren_di:
            luck = "吉"
            desc = "三才配置，天格生人格，人格生地格，大吉之象"
        elif "相剋" in tian_ren or "相剋" in ren_di:
            luck = "凶"
            desc = "三才配置有相剋之象，需注意調和"
        else:
            luck = "平"
            desc = "三才配置平穩，無特別吉凶"

        return {
            "luck": luck,
            "desc": desc,
            "tian_ren_relation": tian_ren,
            "ren_di_relation": ren_di
        }

    def analyze(self) -> Dict[str, Any]:
        """
        執行完整的姓名學分析

        Returns:
            完整的姓名學分析結果
        """
        # 計算五格
        five_grids = self.calculate_five_grids()

        # 分析三才
        sancai = self.analyze_sancai(five_grids)

        # 綜合評分（簡化版）
        scores = []
        for grid_name in ["tian_ge", "ren_ge", "di_ge", "wai_ge", "zong_ge"]:
            luck = five_grids[grid_name]["meaning"]["luck"]
            if "大吉" in luck:
                scores.append(10)
            elif "吉" in luck:
                scores.append(7)
            elif "平" in luck or "半" in luck:
                scores.append(5)
            else:
                scores.append(3)

        overall_score = sum(scores) / len(scores)

        # 判斷整體吉凶
        if overall_score >= 8:
            overall_luck = "大吉"
        elif overall_score >= 6:
            overall_luck = "吉"
        elif overall_score >= 4:
            overall_luck = "平"
        else:
            overall_luck = "凶"

        return {
            "name": self.name,
            "gender": self.gender,
            "name_characters": self.name_chars,
            "five_grids": five_grids,
            "sancai": sancai,
            "overall_score": round(overall_score, 2),
            "overall_luck": overall_luck,
            "analysis_summary": {
                "tian_ge_summary": f"天格{five_grids['tian_ge']['value']}（{five_grids['tian_ge']['wuxing']}）- {five_grids['tian_ge']['meaning']['luck']}",
                "ren_ge_summary": f"人格{five_grids['ren_ge']['value']}（{five_grids['ren_ge']['wuxing']}）- {five_grids['ren_ge']['meaning']['luck']}",
                "di_ge_summary": f"地格{five_grids['di_ge']['value']}（{five_grids['di_ge']['wuxing']}）- {five_grids['di_ge']['meaning']['luck']}",
                "wai_ge_summary": f"外格{five_grids['wai_ge']['value']}（{five_grids['wai_ge']['wuxing']}）- {five_grids['wai_ge']['meaning']['luck']}",
                "zong_ge_summary": f"總格{five_grids['zong_ge']['value']}（{five_grids['zong_ge']['wuxing']}）- {five_grids['zong_ge']['meaning']['luck']}",
                "sancai_summary": f"三才配置：{sancai['combination']} - {sancai['luck']}"
            }
        }


def test_name_analysis():
    """測試函數"""
    # 測試範例
    test_names = [
        ("王小明", "男"),
        ("李美麗", "女"),
        ("張偉華", "男")
    ]

    for name, gender in test_names:
        print(f"\n{'='*80}")
        print(f"測試姓名：{name}（{gender}）")
        print('='*80)

        calculator = NameAnalysisCalculator(name, gender)
        result = calculator.analyze()

        print(f"\n📊 五格配置：")
        print(f"   {result['analysis_summary']['tian_ge_summary']}")
        print(f"   {result['analysis_summary']['ren_ge_summary']}")
        print(f"   {result['analysis_summary']['di_ge_summary']}")
        print(f"   {result['analysis_summary']['wai_ge_summary']}")
        print(f"   {result['analysis_summary']['zong_ge_summary']}")

        print(f"\n🔮 三才配置：")
        print(f"   {result['analysis_summary']['sancai_summary']}")
        print(f"   {result['sancai']['description']}")

        print(f"\n✨ 綜合評價：")
        print(f"   評分：{result['overall_score']}/10")
        print(f"   吉凶：{result['overall_luck']}")


if __name__ == "__main__":
    test_name_analysis()

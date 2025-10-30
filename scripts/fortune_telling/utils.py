"""
工具模組 (Utility Module)
=========================

包含命理計算所需的基本常數、數據結構和輔助函數。
"""

from typing import Dict, List, Tuple, Optional
from enum import Enum
from pydantic import BaseModel, Field, validator
from datetime import datetime

# ============================================
# 天干地支系統 (Heavenly Stems & Earthly Branches)
# ============================================

# 十天干 (Ten Heavenly Stems)
HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 十二地支 (Twelve Earthly Branches)
EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 十二時辰對應表 (Hour to Earthly Branch mapping)
HOUR_TO_BRANCH = {
    (23, 1): "子", (1, 3): "丑", (3, 5): "寅", (5, 7): "卯",
    (7, 9): "辰", (9, 11): "巳", (11, 13): "午", (13, 15): "未",
    (15, 17): "申", (17, 19): "酉", (19, 21): "戌", (21, 23): "亥"
}

# 六十甲子納音表 (60 Jia Zi Nayin - Heavenly Sounds)
NAYIN_TABLE = {
    ("甲子", "乙丑"): "海中金", ("丙寅", "丁卯"): "爐中火",
    ("戊辰", "己巳"): "大林木", ("庚午", "辛未"): "路旁土",
    ("壬申", "癸酉"): "劍鋒金", ("甲戌", "乙亥"): "山頭火",
    ("丙子", "丁丑"): "澗下水", ("戊寅", "己卯"): "城頭土",
    ("庚辰", "辛巳"): "白蠟金", ("壬午", "癸未"): "楊柳木",
    ("甲申", "乙酉"): "泉中水", ("丙戌", "丁亥"): "屋上土",
    ("戊子", "己丑"): "霹靂火", ("庚寅", "辛卯"): "松柏木",
    ("壬辰", "癸巳"): "長流水", ("甲午", "乙未"): "沙中金",
    ("丙申", "丁酉"): "山下火", ("戊戌", "己亥"): "平地木",
    ("庚子", "辛丑"): "壁上土", ("壬寅", "癸卯"): "金箔金",
    ("甲辰", "乙巳"): "覆燈火", ("丙午", "丁未"): "天河水",
    ("戊申", "己酉"): "大驛土", ("庚戌", "辛亥"): "釵釧金",
    ("壬子", "癸丑"): "桑柘木", ("甲寅", "乙卯"): "大溪水",
    ("丙辰", "丁巳"): "沙中土", ("戊午", "己未"): "天上火",
    ("庚申", "辛酉"): "石榴木", ("壬戌", "癸亥"): "大海水"
}

# ============================================
# 五行系統 (Five Elements)
# ============================================

class WuXing(str, Enum):
    """五行枚舉"""
    WOOD = "木"    # 木
    FIRE = "火"    # 火
    EARTH = "土"   # 土
    METAL = "金"   # 金
    WATER = "水"   # 水

# 天干五行對應
STEM_TO_WUXING: Dict[str, WuXing] = {
    "甲": WuXing.WOOD, "乙": WuXing.WOOD,
    "丙": WuXing.FIRE, "丁": WuXing.FIRE,
    "戊": WuXing.EARTH, "己": WuXing.EARTH,
    "庚": WuXing.METAL, "辛": WuXing.METAL,
    "壬": WuXing.WATER, "癸": WuXing.WATER
}

# 地支五行對應
BRANCH_TO_WUXING: Dict[str, WuXing] = {
    "寅": WuXing.WOOD, "卯": WuXing.WOOD,
    "巳": WuXing.FIRE, "午": WuXing.FIRE,
    "辰": WuXing.EARTH, "戌": WuXing.EARTH, "丑": WuXing.EARTH, "未": WuXing.EARTH,
    "申": WuXing.METAL, "酉": WuXing.METAL,
    "亥": WuXing.WATER, "子": WuXing.WATER
}

# 五行生剋關係
WUXING_GENERATES = {
    WuXing.WOOD: WuXing.FIRE,
    WuXing.FIRE: WuXing.EARTH,
    WuXing.EARTH: WuXing.METAL,
    WuXing.METAL: WuXing.WATER,
    WuXing.WATER: WuXing.WOOD
}

WUXING_CONTROLS = {
    WuXing.WOOD: WuXing.EARTH,
    WuXing.FIRE: WuXing.METAL,
    WuXing.EARTH: WuXing.WATER,
    WuXing.METAL: WuXing.WOOD,
    WuXing.WATER: WuXing.FIRE
}

# ============================================
# 地支藏干表 (Hidden Stems in Branches)
# ============================================

BRANCH_HIDDEN_STEMS: Dict[str, List[Tuple[str, int]]] = {
    "子": [("癸", 10)],
    "丑": [("己", 9), ("癸", 3), ("辛", 18)],
    "寅": [("甲", 7), ("丙", 7), ("戊", 16)],
    "卯": [("乙", 10)],
    "辰": [("戊", 9), ("乙", 3), ("癸", 18)],
    "巳": [("丙", 7), ("庚", 7), ("戊", 16)],
    "午": [("丁", 7), ("己", 23)],
    "未": [("己", 9), ("丁", 3), ("乙", 18)],
    "申": [("庚", 7), ("壬", 7), ("戊", 16)],
    "酉": [("辛", 10)],
    "戌": [("戊", 9), ("辛", 3), ("丁", 18)],
    "亥": [("壬", 7), ("甲", 23)]
}

# ============================================
# 十神系統 (Ten Gods)
# ============================================

class TenGods(str, Enum):
    """十神枚舉"""
    BI_JIAN = "比肩"      # 比肩
    JIE_CAI = "劫財"      # 劫財
    SHANG_GUAN = "傷官"   # 傷官
    SHI_SHEN = "食神"     # 食神
    ZHENG_CAI = "正財"    # 正財
    PIAN_CAI = "偏財"     # 偏財
    ZHENG_GUAN = "正官"   # 正官
    QI_SHA = "七殺"       # 七殺 (偏官)
    ZHENG_YIN = "正印"    # 正印
    PIAN_YIN = "偏印"     # 偏印 (梟神)

# 十神生剋關係表 (根據日主與其他天干的陰陽五行關係)
# 此為簡化版，實際使用時需根據陰陽配合

# ============================================
# 二十四節氣 (24 Solar Terms)
# ============================================

SOLAR_TERMS = [
    "小寒", "大寒", "立春", "雨水", "驚蟄", "春分",
    "清明", "穀雨", "立夏", "小滿", "芒種", "夏至",
    "小暑", "大暑", "立秋", "處暑", "白露", "秋分",
    "寒露", "霜降", "立冬", "小雪", "大雪", "冬至"
]

# 節氣對應月令 (Solar Terms to Month mapping)
SOLAR_TERM_TO_MONTH = {
    "立春": "寅", "驚蟄": "卯", "清明": "辰",
    "立夏": "巳", "芒種": "午", "小暑": "未",
    "立秋": "申", "白露": "酉", "寒露": "戌",
    "立冬": "亥", "大雪": "子", "小寒": "丑"
}

# ============================================
# 紫微斗數星曜 (Zi Wei Stars)
# ============================================

# 主星 (Major Stars)
ZIWEI_MAJOR_STARS = [
    "紫微", "天機", "太陽", "武曲", "天同", "廉貞",
    "天府", "太陰", "貪狼", "巨門", "天相", "天梁",
    "七殺", "破軍"
]

# 輔星 (Minor/Auxiliary Stars)
ZIWEI_MINOR_STARS = [
    "文昌", "文曲", "左輔", "右弼", "天魁", "天鉞",
    "祿存", "天馬", "化祿", "化權", "化科", "化忌"
]

# 煞星 (Malefic Stars)
ZIWEI_SHA_STARS = [
    "擎羊", "陀羅", "火星", "鈴星", "地空", "地劫"
]

# 十二宮 (Twelve Palaces)
ZIWEI_TWELVE_PALACES = [
    "命宮", "兄弟", "夫妻", "子女", "財帛", "疾厄",
    "遷移", "僕役", "官祿", "田宅", "福德", "父母"
]

# ============================================
# 占星符號 (Astrology Symbols)
# ============================================

# 黃道十二星座 (Zodiac Signs)
ZODIAC_SIGNS = [
    "白羊座", "金牛座", "雙子座", "巨蟹座", "獅子座", "處女座",
    "天秤座", "天蠍座", "射手座", "摩羯座", "水瓶座", "雙魚座"
]

ZODIAC_SIGNS_EN = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# 行星 (Planets)
PLANETS = {
    "sun": "太陽", "moon": "月亮", "mercury": "水星", "venus": "金星",
    "mars": "火星", "jupiter": "木星", "saturn": "土星",
    "uranus": "天王星", "neptune": "海王星", "pluto": "冥王星"
}

# 相位 (Aspects)
ASPECTS = {
    "conjunction": {"name": "合相", "angle": 0, "orb": 8},
    "sextile": {"name": "六分相", "angle": 60, "orb": 6},
    "square": {"name": "四分相", "angle": 90, "orb": 8},
    "trine": {"name": "三分相", "angle": 120, "orb": 8},
    "opposition": {"name": "對分相", "angle": 180, "orb": 8},
    "quincunx": {"name": "梅花相", "angle": 150, "orb": 3}
}

# ============================================
# 數據模型 (Data Models using Pydantic)
# ============================================

class BirthInfo(BaseModel):
    """出生資訊數據模型"""
    name: str = Field(..., description="姓名")
    birth_date: datetime = Field(..., description="出生日期時間（公曆）")
    location: str = Field(..., description="出生地點")
    gender: str = Field(..., pattern="^(男|女)$", description="性別")
    timezone: str = Field(default="Asia/Taipei", description="時區")
    longitude: Optional[float] = Field(default=None, description="經度")
    latitude: Optional[float] = Field(default=None, description="緯度")

    @validator('birth_date')
    def validate_birth_date(cls, v):
        if v > datetime.now():
            raise ValueError("出生日期不能是未來時間")
        if v.year < 1900:
            raise ValueError("出生年份應在1900年之後")
        return v

class LunarDate(BaseModel):
    """農曆日期數據模型"""
    year: int = Field(..., description="農曆年")
    month: int = Field(..., ge=1, le=12, description="農曆月")
    day: int = Field(..., ge=1, le=30, description="農曆日")
    is_leap_month: bool = Field(default=False, description="是否閏月")
    hour_branch: str = Field(..., description="時辰地支")
    solar_term: str = Field(..., description="節氣")

class FourPillars(BaseModel):
    """四柱八字數據模型"""
    year_stem: str = Field(..., description="年柱天干")
    year_branch: str = Field(..., description="年柱地支")
    month_stem: str = Field(..., description="月柱天干")
    month_branch: str = Field(..., description="月柱地支")
    day_stem: str = Field(..., description="日柱天干")
    day_branch: str = Field(..., description="日柱地支")
    hour_stem: str = Field(..., description="時柱天干")
    hour_branch: str = Field(..., description="時柱地支")

# ============================================
# 輔助函數 (Helper Functions)
# ============================================

def get_stem_branch_index(stem: str, branch: str) -> int:
    """
    獲取天干地支組合的六十甲子序號 (0-59)

    Args:
        stem: 天干
        branch: 地支

    Returns:
        六十甲子序號
    """
    stem_index = HEAVENLY_STEMS.index(stem)
    branch_index = EARTHLY_BRANCHES.index(branch)
    return (stem_index * 6 + branch_index) % 60

def get_stem_branch_by_index(index: int) -> Tuple[str, str]:
    """
    根據六十甲子序號獲取天干地支組合

    Args:
        index: 六十甲子序號 (0-59)

    Returns:
        (天干, 地支) 元組
    """
    index = index % 60
    stem = HEAVENLY_STEMS[index % 10]
    branch = EARTHLY_BRANCHES[index % 12]
    return (stem, branch)

def get_wuxing_from_stem(stem: str) -> WuXing:
    """獲取天干對應的五行"""
    return STEM_TO_WUXING[stem]

def get_wuxing_from_branch(branch: str) -> WuXing:
    """獲取地支對應的五行"""
    return BRANCH_TO_WUXING[branch]

def get_nayin(stem: str, branch: str) -> str:
    """
    獲取納音五行

    Args:
        stem: 天干
        branch: 地支

    Returns:
        納音名稱（如「海中金」）
    """
    pillar = stem + branch
    for key, value in NAYIN_TABLE.items():
        if pillar in key:
            return value
    return "未知"

def calculate_hour_branch(hour: int, minute: int = 0) -> str:
    """
    計算時辰地支

    Args:
        hour: 小時 (0-23)
        minute: 分鐘 (0-59)

    Returns:
        時辰地支
    """
    # 子時特殊處理：23:00-00:59
    if hour == 23 or hour == 0:
        return "子"

    # 其他時辰：每兩小時一個時辰
    for (start, end), branch in HOUR_TO_BRANCH.items():
        if start <= hour < end:
            return branch

    return "子"  # 默認返回子時

def is_yin_yang(character: str) -> str:
    """
    判斷天干或地支的陰陽

    Args:
        character: 天干或地支

    Returns:
        "陽" 或 "陰"
    """
    if character in HEAVENLY_STEMS:
        index = HEAVENLY_STEMS.index(character)
        return "陽" if index % 2 == 0 else "陰"
    elif character in EARTHLY_BRANCHES:
        index = EARTHLY_BRANCHES.index(character)
        return "陽" if index % 2 == 0 else "陰"
    return "未知"

def get_ten_god(day_stem: str, other_stem: str) -> TenGods:
    """
    計算十神關係

    Args:
        day_stem: 日主天干
        other_stem: 其他天干

    Returns:
        十神類型
    """
    day_wuxing = get_wuxing_from_stem(day_stem)
    other_wuxing = get_wuxing_from_stem(other_stem)
    day_yinyang = is_yin_yang(day_stem)
    other_yinyang = is_yin_yang(other_stem)

    same_yinyang = (day_yinyang == other_yinyang)

    # 比肩劫財 (Same element)
    if day_wuxing == other_wuxing:
        return TenGods.BI_JIAN if same_yinyang else TenGods.JIE_CAI

    # 食傷 (Day generates)
    if WUXING_GENERATES[day_wuxing] == other_wuxing:
        return TenGods.SHI_SHEN if same_yinyang else TenGods.SHANG_GUAN

    # 財星 (Day controls)
    if WUXING_CONTROLS[day_wuxing] == other_wuxing:
        return TenGods.ZHENG_CAI if not same_yinyang else TenGods.PIAN_CAI

    # 官殺 (Controls day)
    if WUXING_CONTROLS[other_wuxing] == day_wuxing:
        return TenGods.ZHENG_GUAN if not same_yinyang else TenGods.QI_SHA

    # 印綬 (Generates day)
    if WUXING_GENERATES[other_wuxing] == day_wuxing:
        return TenGods.ZHENG_YIN if not same_yinyang else TenGods.PIAN_YIN

    return TenGods.BI_JIAN  # 默認返回比肩

# ============================================
# 城市經緯度數據庫 (City Coordinates Database)
# ============================================

CITY_COORDINATES = {
    # 台灣主要城市
    "台北": {"lat": 25.0330, "lon": 121.5654, "tz": "Asia/Taipei"},
    "台中": {"lat": 24.1477, "lon": 120.6736, "tz": "Asia/Taipei"},
    "台南": {"lat": 22.9997, "lon": 120.2270, "tz": "Asia/Taipei"},
    "高雄": {"lat": 22.6273, "lon": 120.3014, "tz": "Asia/Taipei"},
    "新竹": {"lat": 24.8138, "lon": 120.9675, "tz": "Asia/Taipei"},
    "苗栗": {"lat": 24.5602, "lon": 120.8214, "tz": "Asia/Taipei"},
    "miaoli": {"lat": 24.5602, "lon": 120.8214, "tz": "Asia/Taipei"},

    # 中國主要城市
    "北京": {"lat": 39.9042, "lon": 116.4074, "tz": "Asia/Shanghai"},
    "上海": {"lat": 31.2304, "lon": 121.4737, "tz": "Asia/Shanghai"},
    "廣州": {"lat": 23.1291, "lon": 113.2644, "tz": "Asia/Shanghai"},
    "深圳": {"lat": 22.5431, "lon": 114.0579, "tz": "Asia/Shanghai"},
    "成都": {"lat": 30.5728, "lon": 104.0668, "tz": "Asia/Shanghai"},
    "重慶": {"lat": 29.5630, "lon": 106.5516, "tz": "Asia/Shanghai"},
    "杭州": {"lat": 30.2741, "lon": 120.1551, "tz": "Asia/Shanghai"},
    "南京": {"lat": 32.0603, "lon": 118.7969, "tz": "Asia/Shanghai"},
    "汕頭": {"lat": 23.3540, "lon": 116.6819, "tz": "Asia/Shanghai"},
    "shantou": {"lat": 23.3540, "lon": 116.6819, "tz": "Asia/Shanghai"},

    # 其他華人地區
    "香港": {"lat": 22.3193, "lon": 114.1694, "tz": "Asia/Hong_Kong"},
    "澳門": {"lat": 22.1987, "lon": 113.5439, "tz": "Asia/Macau"},
    "新加坡": {"lat": 1.3521, "lon": 103.8198, "tz": "Asia/Singapore"},
}

def get_city_info(city_name: str) -> Optional[Dict]:
    """
    獲取城市資訊（經緯度和時區）

    Args:
        city_name: 城市名稱

    Returns:
        城市資訊字典，如果找不到則返回 None
    """
    return CITY_COORDINATES.get(city_name)


# ============================================
# 西洋占星系統 (Western Astrology)
# ============================================

# 黃道十二星座 (Twelve Zodiac Signs)
ZODIAC_SIGNS = [
    "白羊座",  # Aries (0°-30°)
    "金牛座",  # Taurus (30°-60°)
    "雙子座",  # Gemini (60°-90°)
    "巨蟹座",  # Cancer (90°-120°)
    "獅子座",  # Leo (120°-150°)
    "處女座",  # Virgo (150°-180°)
    "天秤座",  # Libra (180°-210°)
    "天蠍座",  # Scorpio (210°-240°)
    "射手座",  # Sagittarius (240°-270°)
    "摩羯座",  # Capricorn (270°-300°)
    "水瓶座",  # Aquarius (300°-330°)
    "雙魚座"   # Pisces (330°-360°)
]

# 行星列表 (Planets)
PLANETS = [
    "太陽",    # Sun
    "月亮",    # Moon
    "水星",    # Mercury
    "金星",    # Venus
    "火星",    # Mars
    "木星",    # Jupiter
    "土星",    # Saturn
    "天王星",  # Uranus
    "海王星",  # Neptune
    "冥王星"   # Pluto
]

# 相位類型 (Aspects)
ASPECTS = {
    "合相": 0,      # Conjunction
    "六分相": 60,   # Sextile
    "四分相": 90,   # Square
    "三分相": 120,  # Trine
    "對分相": 180   # Opposition
}

# 十二宮位 (Twelve Houses)
HOUSES = [
    "第1宮",   # 自我宮 (House of Self)
    "第2宮",   # 財帛宮 (House of Value)
    "第3宮",   # 溝通宮 (House of Communication)
    "第4宮",   # 家庭宮 (House of Home)
    "第5宮",   # 娛樂宮 (House of Pleasure)
    "第6宮",   # 工作宮 (House of Health)
    "第7宮",   # 伴侶宮 (House of Partnership)
    "第8宮",   # 轉化宮 (House of Transformation)
    "第9宮",   # 旅行宮 (House of Philosophy)
    "第10宮",  # 事業宮 (House of Career)
    "第11宮",  # 朋友宮 (House of Friendship)
    "第12宮"   # 靈性宮 (House of Spirituality)
]

# 星座元素 (Zodiac Elements)
ZODIAC_ELEMENTS = {
    "白羊座": "火", "獅子座": "火", "射手座": "火",  # Fire signs
    "金牛座": "土", "處女座": "土", "摩羯座": "土",  # Earth signs
    "雙子座": "風", "天秤座": "風", "水瓶座": "風",  # Air signs
    "巨蟹座": "水", "天蠍座": "水", "雙魚座": "水"   # Water signs
}

# 星座特質 (Zodiac Modalities)
ZODIAC_MODALITIES = {
    "白羊座": "基本", "巨蟹座": "基本", "天秤座": "基本", "摩羯座": "基本",  # Cardinal
    "金牛座": "固定", "獅子座": "固定", "天蠍座": "固定", "水瓶座": "固定",  # Fixed
    "雙子座": "變動", "處女座": "變動", "射手座": "變動", "雙魚座": "變動"   # Mutable
}

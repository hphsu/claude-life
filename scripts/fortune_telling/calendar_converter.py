"""
曆法轉換引擎 (Calendar Converter Engine)
========================================

專業級曆法轉換模組，提供：
1. 公曆轉農曆（精確到時辰）
2. 二十四節氣精確計算
3. 真太陽時校正
4. 時區處理（包含夏令時）
5. 六十甲子干支計算

準確度：專業級（使用天文曆法數據）
"""

from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import pytz
from lunarcalendar import Converter, Solar, Lunar
import ephem
from .utils import (
    HEAVENLY_STEMS,
    EARTHLY_BRANCHES,
    SOLAR_TERMS,
    SOLAR_TERM_TO_MONTH,
    calculate_hour_branch,
    get_stem_branch_by_index,
    get_city_info,
    BirthInfo,
    LunarDate
)


class CalendarConverter:
    """
    曆法轉換器

    負責所有曆法相關的轉換和計算，確保專業級準確度。
    """

    def __init__(self):
        """初始化曆法轉換器"""
        self._solar_term_cache = {}  # 節氣計算緩存

    def convert_to_lunar(
        self,
        birth_date: datetime,
        location: str,
        use_true_solar_time: bool = True
    ) -> Dict:
        """
        將公曆日期轉換為農曆，並計算相關命理資訊

        Args:
            birth_date: 出生日期時間（公曆，已含時區資訊）
            location: 出生地點
            use_true_solar_time: 是否使用真太陽時校正

        Returns:
            包含農曆資訊和命理計算所需數據的字典
        """
        # 1. 獲取地點資訊（經緯度和時區）
        city_info = get_city_info(location)
        if not city_info:
            raise ValueError(f"無法識別的地點: {location}")

        longitude = city_info["lon"]
        latitude = city_info["lat"]
        timezone_str = city_info["tz"]

        # 2. 確保日期有時區資訊
        if birth_date.tzinfo is None:
            tz = pytz.timezone(timezone_str)
            birth_date = tz.localize(birth_date)
        else:
            # 轉換到正確的時區
            tz = pytz.timezone(timezone_str)
            birth_date = birth_date.astimezone(tz)

        # 3. 真太陽時校正（如果啟用）
        adjusted_time = birth_date
        if use_true_solar_time:
            adjusted_time = self._adjust_true_solar_time(birth_date, longitude)

        # 4. 公曆轉農曆
        solar = Solar(birth_date.year, birth_date.month, birth_date.day)
        lunar = Converter.Solar2Lunar(solar)

        # 5. 計算節氣
        solar_term = self._get_solar_term(birth_date)

        # 6. 計算時辰地支
        hour_branch = calculate_hour_branch(adjusted_time.hour, adjusted_time.minute)

        # 7. 計算四柱干支
        year_stem, year_branch = self._calculate_year_pillar(birth_date, solar_term)
        month_stem, month_branch = self._calculate_month_pillar(
            birth_date, year_stem, solar_term
        )
        day_stem, day_branch = self._calculate_day_pillar(birth_date)
        hour_stem, hour_branch_final = self._calculate_hour_pillar(
            day_stem, hour_branch
        )

        # 8. 組裝返回結果
        result = {
            # 原始公曆資訊
            "gregorian": {
                "datetime": birth_date,
                "year": birth_date.year,
                "month": birth_date.month,
                "day": birth_date.day,
                "hour": birth_date.hour,
                "minute": birth_date.minute,
                "timezone": timezone_str
            },

            # 農曆資訊
            "lunar": {
                "year": lunar.year,
                "month": lunar.month,
                "day": lunar.day,
                "is_leap_month": lunar.isleap,
                "year_cn": f"{lunar.year}年",
                "month_cn": f"{lunar.month}月",
                "day_cn": f"{lunar.day}日"
            },

            # 真太陽時資訊
            "true_solar_time": {
                "original_time": birth_date,
                "adjusted_time": adjusted_time,
                "difference_minutes": (adjusted_time - birth_date).total_seconds() / 60,
                "used": use_true_solar_time
            },

            # 節氣資訊
            "solar_term": {
                "current": solar_term["current"],
                "next": solar_term["next"],
                "current_time": solar_term["current_time"],
                "next_time": solar_term["next_time"]
            },

            # 四柱八字
            "four_pillars": {
                "year": {"stem": year_stem, "branch": year_branch, "pillar": f"{year_stem}{year_branch}"},
                "month": {"stem": month_stem, "branch": month_branch, "pillar": f"{month_stem}{month_branch}"},
                "day": {"stem": day_stem, "branch": day_branch, "pillar": f"{day_stem}{day_branch}"},
                "hour": {"stem": hour_stem, "branch": hour_branch_final, "pillar": f"{hour_stem}{hour_branch_final}"}
            },

            # 地點資訊
            "location": {
                "name": location,
                "longitude": longitude,
                "latitude": latitude,
                "timezone": timezone_str
            }
        }

        return result

    def _adjust_true_solar_time(
        self,
        local_time: datetime,
        longitude: float
    ) -> datetime:
        """
        真太陽時校正

        真太陽時 = 平太陽時 + 均時差 + 經度時差

        Args:
            local_time: 當地標準時間
            longitude: 經度（東經為正）

        Returns:
            校正後的真太陽時
        """
        # 計算經度時差（每15度經度相差1小時）
        # 中國標準時間基準經度為東經120度
        standard_longitude = 120.0  # 東八區標準經度
        longitude_diff = (longitude - standard_longitude) * 4  # 每度4分鐘

        # 計算均時差（Equation of Time）
        equation_of_time = self._calculate_equation_of_time(local_time)

        # 總時差（分鐘）
        total_difference = longitude_diff + equation_of_time

        # 應用校正
        adjusted_time = local_time + timedelta(minutes=total_difference)

        return adjusted_time

    def _calculate_equation_of_time(self, dt: datetime) -> float:
        """
        計算均時差（分鐘）

        均時差是真太陽時與平太陽時的差值，由地球橢圓軌道和自轉軸傾斜造成。

        Args:
            dt: 日期時間

        Returns:
            均時差（分鐘），範圍約為 -16 到 +14 分鐘
        """
        # 使用 ephem 計算精確的均時差
        observer = ephem.Observer()
        observer.date = dt

        sun = ephem.Sun()
        sun.compute(observer)

        # 真太陽時與平太陽時的差值
        equation_of_time = float(sun.ra - observer.sidereal_time()) * 12.0 / ephem.pi

        # 轉換為分鐘
        return equation_of_time * 4.0

    def _get_solar_term(self, dt: datetime) -> Dict:
        """
        獲取當前日期的節氣資訊

        Args:
            dt: 日期時間

        Returns:
            包含當前節氣和下一個節氣的資訊
        """
        year = dt.year

        # 檢查緩存
        if year not in self._solar_term_cache:
            self._solar_term_cache[year] = self._calculate_solar_terms_for_year(year)

        solar_terms = self._solar_term_cache[year]

        # 找到當前和下一個節氣
        current_term = None
        next_term = None

        for i, (term_name, term_time) in enumerate(solar_terms):
            if dt >= term_time:
                current_term = (term_name, term_time)
                if i + 1 < len(solar_terms):
                    next_term = solar_terms[i + 1]
                else:
                    # 如果是最後一個節氣，下一個是明年第一個
                    next_year_terms = self._calculate_solar_terms_for_year(year + 1)
                    next_term = next_year_terms[0] if next_year_terms else None
            else:
                if current_term is None:
                    # 在第一個節氣之前，需要查找去年最後一個
                    prev_year_terms = self._calculate_solar_terms_for_year(year - 1)
                    current_term = prev_year_terms[-1] if prev_year_terms else None
                next_term = (term_name, term_time)
                break

        return {
            "current": current_term[0] if current_term else "未知",
            "current_time": current_term[1] if current_term else None,
            "next": next_term[0] if next_term else "未知",
            "next_time": next_term[1] if next_term else None
        }

    def _calculate_solar_terms_for_year(self, year: int) -> list:
        """
        計算一年中所有24個節氣的精確時刻

        使用天文計算方法，基於太陽黃經。

        Args:
            year: 年份

        Returns:
            [(節氣名稱, 時刻), ...] 列表，按時間排序
        """
        solar_terms = []

        # 24節氣對應的太陽黃經（度）
        # 春分為0度，每個節氣相差15度
        solar_longitudes = {
            "春分": 0, "清明": 15, "穀雨": 30,
            "立夏": 45, "小滿": 60, "芒種": 75,
            "夏至": 90, "小暑": 105, "大暑": 120,
            "立秋": 135, "處暑": 150, "白露": 165,
            "秋分": 180, "寒露": 195, "霜降": 210,
            "立冬": 225, "小雪": 240, "大雪": 255,
            "冬至": 270, "小寒": 285, "大寒": 300,
            "立春": 315, "雨水": 330, "驚蟄": 345
        }

        # 使用 ephem 計算太陽到達特定黃經的時刻
        for term_name in SOLAR_TERMS:
            if term_name in solar_longitudes:
                longitude = solar_longitudes[term_name]
                term_time = self._find_solar_longitude_time(year, longitude)
                if term_time:
                    solar_terms.append((term_name, term_time))

        # 按時間排序
        solar_terms.sort(key=lambda x: x[1])

        return solar_terms

    def _find_solar_longitude_time(
        self,
        year: int,
        target_longitude: float
    ) -> Optional[datetime]:
        """
        查找太陽到達特定黃經的時刻

        Args:
            year: 年份
            target_longitude: 目標黃經（度，0-360）

        Returns:
            太陽到達該黃經的時刻
        """
        # 估算起始日期（根據黃經粗略估算月份）
        # 立春(315°)、雨水(330°)、驚蟄(345°)在冬春之交，屬於當年而非次年
        month = int(target_longitude / 30) + 3
        if month > 12:
            month -= 12
            # 只有當黃經在春分(0°)到立冬(225°)之間時才需要增加年份
            # 立春(315°)、雨水(330°)、驚蟄(345°)都是當年的節氣
            if target_longitude < 300:
                year += 1

        start_date = datetime(year, month, 1)

        # 使用二分法查找精確時刻
        observer = ephem.Observer()
        sun = ephem.Sun()

        # 搜索範圍：前後30天
        left = start_date - timedelta(days=15)
        right = start_date + timedelta(days=45)

        # 二分查找
        while (right - left).total_seconds() > 60:  # 精確到分鐘
            mid = left + (right - left) / 2
            observer.date = mid

            sun.compute(observer)
            current_longitude = float(sun.hlon) * 180.0 / ephem.pi

            # 處理360度邊界
            if target_longitude < 30 and current_longitude > 330:
                current_longitude -= 360

            if current_longitude < target_longitude:
                left = mid
            else:
                right = mid

        # 轉換為 UTC 時間，然後轉為北京時間
        utc_time = left
        beijing_tz = pytz.timezone('Asia/Shanghai')
        result_time = pytz.utc.localize(utc_time).astimezone(beijing_tz)

        return result_time

    def _calculate_year_pillar(
        self,
        dt: datetime,
        solar_term: Dict
    ) -> Tuple[str, str]:
        """
        計算年柱干支

        注意：年柱以立春為界，立春前屬於前一年

        Args:
            dt: 日期時間
            solar_term: 節氣資訊

        Returns:
            (年柱天干, 年柱地支)
        """
        year = dt.year

        # 判斷是否在立春之前
        # 如果在立春之前，使用上一年的干支
        current_term = solar_term["current"]
        current_term_time = solar_term["current_time"]

        # 獲取本年立春時刻
        lichun_time = self._get_lichun_time(year)

        if dt < lichun_time:
            # 在立春之前，使用上一年干支
            year -= 1

        # 計算年柱干支（以1984年甲子年為基準）
        # 1984年是甲子年（六十甲子的第1年）
        base_year = 1984
        offset = (year - base_year) % 60

        stem, branch = get_stem_branch_by_index(offset)

        return stem, branch

    def _get_lichun_time(self, year: int) -> datetime:
        """獲取指定年份的立春時刻"""
        if year not in self._solar_term_cache:
            self._solar_term_cache[year] = self._calculate_solar_terms_for_year(year)

        solar_terms = self._solar_term_cache[year]
        for term_name, term_time in solar_terms:
            if term_name == "立春":
                return term_time

        # 如果找不到（不應該發生），返回近似值
        return datetime(year, 2, 4, 6, 0, 0)

    def _calculate_month_pillar(
        self,
        dt: datetime,
        year_stem: str,
        solar_term: Dict
    ) -> Tuple[str, str]:
        """
        計算月柱干支

        月柱以節氣為界，不以農曆月為準

        Args:
            dt: 日期時間
            year_stem: 年柱天干（用於推算月干）
            solar_term: 節氣資訊

        Returns:
            (月柱天干, 月柱地支)
        """
        # 根據當前節氣確定月支
        current_term = solar_term["current"]

        month_branch = None
        for term, branch in SOLAR_TERM_TO_MONTH.items():
            if current_term == term or (
                SOLAR_TERMS.index(current_term) > SOLAR_TERMS.index(term) and
                (SOLAR_TERMS.index(current_term) - SOLAR_TERMS.index(term)) <= 1
            ):
                month_branch = branch
                break

        if not month_branch:
            # 默認根據公曆月份估算
            month_branches_by_gregorian = [
                "丑", "寅", "卯", "辰", "巳", "午",
                "未", "申", "酉", "戌", "亥", "子"
            ]
            month_branch = month_branches_by_gregorian[dt.month - 1]

        # 計算月干（五虎遁月訣）
        # 甲己之年丙作首，乙庚之年戊為頭，
        # 丙辛之歲尋庚上，丁壬壬寅順水流，
        # 戊癸之年何方起，甲寅之上好追求。

        year_stem_index = HEAVENLY_STEMS.index(year_stem)
        month_branch_index = EARTHLY_BRANCHES.index(month_branch)

        # 五虎遁推算
        month_stem_start = {
            0: 2,  # 甲年從丙開始（寅月）
            1: 4,  # 乙年從戊開始
            2: 6,  # 丙年從庚開始
            3: 8,  # 丁年從壬開始
            4: 0,  # 戊年從甲開始
            5: 2,  # 己年從丙開始
            6: 4,  # 庚年從戊開始
            7: 6,  # 辛年從庚開始
            8: 8,  # 壬年從壬開始
            9: 0   # 癸年從甲開始
        }

        # 寅月是地支的第3位（索引2）
        yin_index = 2
        month_offset = month_branch_index - yin_index

        month_stem_index = (month_stem_start[year_stem_index] + month_offset) % 10
        month_stem = HEAVENLY_STEMS[month_stem_index]

        return month_stem, month_branch

    def _calculate_day_pillar(self, dt: datetime) -> Tuple[str, str]:
        """
        計算日柱干支

        使用公元前2000年11月21日（儒略歷）為甲子日起算

        Args:
            dt: 日期時間

        Returns:
            (日柱天干, 日柱地支)
        """
        # 使用1900年1月1日作為基準日（此日為丙戌日）
        # 1900-01-01 是六十甲子的第23天（丙戌）
        base_date = datetime(1900, 1, 1)
        base_offset = 22  # 丙戌是第23個（索引22）

        # 計算天數差
        days_diff = (dt.date() - base_date.date()).days

        # 計算干支索引
        ganzhi_index = (base_offset + days_diff) % 60

        stem, branch = get_stem_branch_by_index(ganzhi_index)

        return stem, branch

    def _calculate_hour_pillar(
        self,
        day_stem: str,
        hour_branch: str
    ) -> Tuple[str, str]:
        """
        計算時柱干支

        時干根據日干推算（五鼠遁日訣）

        Args:
            day_stem: 日柱天干
            hour_branch: 時辰地支

        Returns:
            (時柱天干, 時柱地支)
        """
        # 五鼠遁日訣：
        # 甲己還加甲，乙庚丙作初，
        # 丙辛從戊起，丁壬庚子居，
        # 戊癸何方發，壬子是真途。

        day_stem_index = HEAVENLY_STEMS.index(day_stem)
        hour_branch_index = EARTHLY_BRANCHES.index(hour_branch)

        # 子時是地支的第1位（索引0）
        hour_stem_start = {
            0: 0,  # 甲日從甲開始（子時）
            1: 2,  # 乙日從丙開始
            2: 4,  # 丙日從戊開始
            3: 6,  # 丁日從庚開始
            4: 8,  # 戊日從壬開始
            5: 0,  # 己日從甲開始
            6: 2,  # 庚日從丙開始
            7: 4,  # 辛日從戊開始
            8: 6,  # 壬日從庚開始
            9: 8   # 癸日從壬開始
        }

        hour_stem_index = (hour_stem_start[day_stem_index] + hour_branch_index) % 10
        hour_stem = HEAVENLY_STEMS[hour_stem_index]

        return hour_stem, hour_branch


# ============================================
# 便捷函數 (Convenience Functions)
# ============================================

def quick_convert(
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    location: str = "台北"
) -> Dict:
    """
    快速轉換函數

    Args:
        year: 年
        month: 月
        day: 日
        hour: 時
        minute: 分
        location: 地點（默認台北）

    Returns:
        完整的轉換結果

    Example:
        >>> result = quick_convert(1990, 5, 15, 14, 30, "台北")
        >>> print(result["four_pillars"]["day"]["pillar"])
    """
    birth_date = datetime(year, month, day, hour, minute)
    converter = CalendarConverter()
    return converter.convert_to_lunar(birth_date, location)


if __name__ == "__main__":
    # 測試代碼
    print("=" * 60)
    print("曆法轉換引擎測試")
    print("=" * 60)

    # 測試案例：1990年5月15日 14:30 台北出生
    result = quick_convert(1990, 5, 15, 14, 30, "台北")

    print("\n📅 公曆資訊:")
    print(f"  日期: {result['gregorian']['year']}-{result['gregorian']['month']}-{result['gregorian']['day']}")
    print(f"  時間: {result['gregorian']['hour']}:{result['gregorian']['minute']:02d}")

    print("\n🌙 農曆資訊:")
    print(f"  日期: {result['lunar']['year_cn']}{result['lunar']['month_cn']}{result['lunar']['day_cn']}")
    print(f"  閏月: {'是' if result['lunar']['is_leap_month'] else '否'}")

    print("\n☀️ 節氣資訊:")
    print(f"  當前節氣: {result['solar_term']['current']}")
    print(f"  下個節氣: {result['solar_term']['next']}")

    print("\n🎋 四柱八字:")
    print(f"  年柱: {result['four_pillars']['year']['pillar']}")
    print(f"  月柱: {result['four_pillars']['month']['pillar']}")
    print(f"  日柱: {result['four_pillars']['day']['pillar']}")
    print(f"  時柱: {result['four_pillars']['hour']['pillar']}")

    print("\n⏰ 真太陽時:")
    print(f"  原始時間: {result['true_solar_time']['original_time'].strftime('%H:%M:%S')}")
    print(f"  校正時間: {result['true_solar_time']['adjusted_time'].strftime('%H:%M:%S')}")
    print(f"  時差: {result['true_solar_time']['difference_minutes']:.2f} 分鐘")

    print("\n" + "=" * 60)

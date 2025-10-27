"""
西洋占星計算器 (Western Astrology Calculator) - 精簡版
=======================================================

核心功能：
1. 行星位置計算（使用 Swiss Ephemeris）
2. 宮位系統（Placidus 分宮法）
3. 重要相位分析
4. 基本星盤解讀

使用專業天文曆表確保計算精度
"""

from typing import Dict, List, Tuple
from datetime import datetime
import pytz
import swisseph as swe
from .utils import ZODIAC_SIGNS, PLANETS, ASPECTS, HOUSES


class AstrologyCalculator:
    """西洋占星計算器 - 精簡實用版"""

    def __init__(self, birth_datetime: datetime, latitude: float, longitude: float):
        """
        初始化占星計算器

        Args:
            birth_datetime: 出生日期時間（含時區）
            latitude: 出生地緯度
            longitude: 出生地經度
        """
        self.birth_datetime = birth_datetime
        self.latitude = latitude
        self.longitude = longitude

        # 轉換為 UTC 時間（Swiss Ephemeris 使用 UTC）
        if birth_datetime.tzinfo is None:
            # 如果沒有時區信息，假設為 UTC
            self.birth_datetime_utc = birth_datetime
        else:
            self.birth_datetime_utc = birth_datetime.astimezone(pytz.UTC)

        # 計算 Julian Day
        self.julian_day = self._calculate_julian_day()

    def _calculate_julian_day(self) -> float:
        """計算 Julian Day Number"""
        dt = self.birth_datetime_utc
        year = dt.year
        month = dt.month
        day = dt.day
        hour = dt.hour + dt.minute / 60.0 + dt.second / 3600.0

        return swe.julday(year, month, day, hour)

    def analyze(self) -> Dict:
        """完整占星分析"""
        # 1. 計算行星位置
        planets = self._calculate_planets()

        # 2. 計算宮位
        houses = self._calculate_houses()

        # 3. 計算相位
        aspects = self._calculate_aspects(planets)

        # 4. 基本解讀
        interpretations = self._interpret_chart(planets, houses, aspects)

        # 5. 生成摘要
        summary = self._generate_summary(planets, houses)

        return {
            "birth_info": {
                "datetime": self.birth_datetime.isoformat(),
                "latitude": self.latitude,
                "longitude": self.longitude,
                "julian_day": self.julian_day
            },
            "planets": planets,
            "houses": houses,
            "aspects": aspects,
            "interpretations": interpretations,
            "summary": summary
        }

    def _calculate_planets(self) -> Dict:
        """
        計算主要行星位置

        包括：太陽、月亮、水星、金星、火星、木星、土星、天王星、海王星、冥王星
        以及上升點、天頂
        """
        planets_data = {}

        # 主要行星（Swiss Ephemeris 編號）
        planet_ids = {
            "太陽": swe.SUN,
            "月亮": swe.MOON,
            "水星": swe.MERCURY,
            "金星": swe.VENUS,
            "火星": swe.MARS,
            "木星": swe.JUPITER,
            "土星": swe.SATURN,
            "天王星": swe.URANUS,
            "海王星": swe.NEPTUNE,
            "冥王星": swe.PLUTO
        }

        for planet_name, planet_id in planet_ids.items():
            # 計算行星位置
            result, ret = swe.calc_ut(self.julian_day, planet_id)

            longitude = result[0]  # 黃經
            latitude = result[1]   # 黃緯
            distance = result[2]   # 距離
            speed = result[3]      # 速度

            # 判斷星座
            sign_index = int(longitude / 30)
            sign_degree = longitude % 30

            # 判斷逆行
            is_retrograde = speed < 0

            planets_data[planet_name] = {
                "longitude": round(longitude, 4),
                "latitude": round(latitude, 4),
                "sign": ZODIAC_SIGNS[sign_index],
                "degree": round(sign_degree, 2),
                "speed": round(speed, 4),
                "retrograde": is_retrograde,
                "position_text": f"{ZODIAC_SIGNS[sign_index]} {int(sign_degree)}°{int((sign_degree % 1) * 60)}'"
            }

        return planets_data

    def _calculate_houses(self) -> Dict:
        """
        計算宮位（使用 Placidus 分宮法）

        返回 12 宮位的起始點以及重要點（上升、天頂、下降、天底）
        """
        # Placidus 分宮法（'P'）
        cusps, ascmc = swe.houses(
            self.julian_day,
            self.latitude,
            self.longitude,
            b'P'  # Placidus
        )

        houses_data = {}

        # 12 宮位
        for i in range(12):
            house_num = i + 1
            cusp_longitude = cusps[i]

            sign_index = int(cusp_longitude / 30)
            sign_degree = cusp_longitude % 30

            houses_data[f"第{house_num}宮"] = {
                "cusp": round(cusp_longitude, 4),
                "sign": ZODIAC_SIGNS[sign_index],
                "degree": round(sign_degree, 2),
                "position_text": f"{ZODIAC_SIGNS[sign_index]} {int(sign_degree)}°{int((sign_degree % 1) * 60)}'"
            }

        # 重要點
        # ascmc[0] = 上升點 (Ascendant)
        # ascmc[1] = 天頂 (MC - Medium Coeli)
        # ascmc[2] = ARMC (直接在赤道上的 MC)
        # ascmc[3] = 頂點 (Vertex)

        asc_longitude = ascmc[0]
        mc_longitude = ascmc[1]

        asc_sign_index = int(asc_longitude / 30)
        asc_degree = asc_longitude % 30

        mc_sign_index = int(mc_longitude / 30)
        mc_degree = mc_longitude % 30

        houses_data["上升點"] = {
            "longitude": round(asc_longitude, 4),
            "sign": ZODIAC_SIGNS[asc_sign_index],
            "degree": round(asc_degree, 2),
            "position_text": f"{ZODIAC_SIGNS[asc_sign_index]} {int(asc_degree)}°{int((asc_degree % 1) * 60)}'"
        }

        houses_data["天頂"] = {
            "longitude": round(mc_longitude, 4),
            "sign": ZODIAC_SIGNS[mc_sign_index],
            "degree": round(mc_degree, 2),
            "position_text": f"{ZODIAC_SIGNS[mc_sign_index]} {int(mc_degree)}°{int((mc_degree % 1) * 60)}'"
        }

        # 計算下降點（上升點對面）
        desc_longitude = (asc_longitude + 180) % 360
        desc_sign_index = int(desc_longitude / 30)
        desc_degree = desc_longitude % 30

        houses_data["下降點"] = {
            "longitude": round(desc_longitude, 4),
            "sign": ZODIAC_SIGNS[desc_sign_index],
            "degree": round(desc_degree, 2),
            "position_text": f"{ZODIAC_SIGNS[desc_sign_index]} {int(desc_degree)}°{int((desc_degree % 1) * 60)}'"
        }

        # 計算天底（天頂對面）
        ic_longitude = (mc_longitude + 180) % 360
        ic_sign_index = int(ic_longitude / 30)
        ic_degree = ic_longitude % 30

        houses_data["天底"] = {
            "longitude": round(ic_longitude, 4),
            "sign": ZODIAC_SIGNS[ic_sign_index],
            "degree": round(ic_degree, 2),
            "position_text": f"{ZODIAC_SIGNS[ic_sign_index]} {int(ic_degree)}°{int((ic_degree % 1) * 60)}'"
        }

        return houses_data

    def _calculate_aspects(self, planets: Dict) -> List[Dict]:
        """
        計算行星相位

        主要相位：
        - 合相 (0°, ±8°)
        - 六分相 (60°, ±6°)
        - 四分相 (90°, ±8°)
        - 三分相 (120°, ±8°)
        - 對分相 (180°, ±8°)
        """
        aspects_list = []

        # 相位定義（角度和容許度）
        aspect_definitions = {
            "合相": (0, 8),
            "六分相": (60, 6),
            "四分相": (90, 8),
            "三分相": (120, 8),
            "對分相": (180, 8)
        }

        planet_names = list(planets.keys())

        # 計算所有行星對之間的相位
        for i, planet1 in enumerate(planet_names):
            for planet2 in planet_names[i + 1:]:
                lon1 = planets[planet1]["longitude"]
                lon2 = planets[planet2]["longitude"]

                # 計算角度差
                angle = abs(lon1 - lon2)
                if angle > 180:
                    angle = 360 - angle

                # 檢查是否形成相位
                for aspect_name, (target_angle, orb) in aspect_definitions.items():
                    diff = abs(angle - target_angle)

                    if diff <= orb:
                        # 形成相位
                        aspects_list.append({
                            "planet1": planet1,
                            "planet2": planet2,
                            "aspect": aspect_name,
                            "angle": round(angle, 2),
                            "orb": round(diff, 2),
                            "applying": self._is_applying(planets[planet1], planets[planet2], angle),
                            "strength": self._calculate_aspect_strength(diff, orb)
                        })

        # 按相位強度排序
        aspects_list.sort(key=lambda x: x["strength"], reverse=True)

        return aspects_list

    def _is_applying(self, planet1: Dict, planet2: Dict, current_angle: float) -> bool:
        """
        判斷相位是入相位（applying）還是離相位（separating）

        入相位：兩行星正在接近精確相位
        離相位：兩行星正在遠離精確相位
        """
        speed1 = planet1["speed"]
        speed2 = planet2["speed"]

        # 簡化判斷：速度差為正表示正在接近
        return (speed1 - speed2) > 0

    def _calculate_aspect_strength(self, orb_diff: float, max_orb: float) -> float:
        """計算相位強度（0-1）"""
        return 1.0 - (orb_diff / max_orb)

    def _interpret_chart(self, planets: Dict, houses: Dict, aspects: List[Dict]) -> Dict:
        """
        基本星盤解讀

        包括：
        1. 太陽星座特質
        2. 月亮星座特質
        3. 上升星座特質
        4. 重要相位解讀
        5. 行星落宮位解讀
        """
        interpretations = {}

        # 太陽星座解讀
        sun_sign = planets["太陽"]["sign"]
        interpretations["太陽星座"] = {
            "sign": sun_sign,
            "meaning": self._interpret_sun_sign(sun_sign),
            "importance": "核心人格，自我表達方式"
        }

        # 月亮星座解讀
        moon_sign = planets["月亮"]["sign"]
        interpretations["月亮星座"] = {
            "sign": moon_sign,
            "meaning": self._interpret_moon_sign(moon_sign),
            "importance": "情感需求，內在自我"
        }

        # 上升星座解讀
        asc_sign = houses["上升點"]["sign"]
        interpretations["上升星座"] = {
            "sign": asc_sign,
            "meaning": self._interpret_ascendant_sign(asc_sign),
            "importance": "外在形象，人生態度"
        }

        # 重要相位解讀（只解讀前5個最強的相位）
        top_aspects = aspects[:5]
        interpretations["重要相位"] = []

        for aspect in top_aspects:
            interpretation = self._interpret_aspect(
                aspect["planet1"],
                aspect["planet2"],
                aspect["aspect"]
            )
            interpretations["重要相位"].append({
                "aspect_info": f"{aspect['planet1']} {aspect['aspect']} {aspect['planet2']}",
                "strength": f"{aspect['strength']:.0%}",
                "interpretation": interpretation
            })

        # 行星落宮位（只解讀內行星和上升守護星）
        interpretations["行星落宮"] = {}
        key_planets = ["太陽", "月亮", "水星", "金星", "火星"]

        for planet_name in key_planets:
            planet_lon = planets[planet_name]["longitude"]
            house = self._find_house_for_planet(planet_lon, houses)

            interpretations["行星落宮"][planet_name] = {
                "house": house,
                "interpretation": self._interpret_planet_in_house(planet_name, house)
            }

        return interpretations

    def _interpret_sun_sign(self, sign: str) -> str:
        """太陽星座基本解讀"""
        sun_interpretations = {
            "白羊座": "充滿活力與熱情，勇於開創，直接坦率",
            "金牛座": "穩重踏實，重視物質安全，堅持己見",
            "雙子座": "機智靈活，善於溝通，好奇心強",
            "巨蟹座": "情感豐富，重視家庭，善於照顧他人",
            "獅子座": "自信大方，富有創造力，喜歡成為焦點",
            "處女座": "細心謹慎，追求完美，善於分析",
            "天秤座": "追求和諧，重視關係，具有美感",
            "天蠍座": "深沉專注，洞察力強，情感深刻",
            "射手座": "樂觀開朗，熱愛自由，追求真理",
            "摩羯座": "務實負責，有野心，重視成就",
            "水瓶座": "獨立創新，思想前衛，重視友誼",
            "雙魚座": "敏感夢幻，富有同情心，直覺力強"
        }
        return sun_interpretations.get(sign, "基本人格特質")

    def _interpret_moon_sign(self, sign: str) -> str:
        """月亮星座基本解讀"""
        moon_interpretations = {
            "白羊座": "情緒直接，需要行動來釋放情感",
            "金牛座": "情感穩定，需要安全感和舒適",
            "雙子座": "情緒多變，需要智識刺激",
            "巨蟹座": "情感深刻，需要歸屬感",
            "獅子座": "需要被認可，情感表達戲劇化",
            "處女座": "情感內斂，需要有序的環境",
            "天秤座": "需要和諧關係，情感尋求平衡",
            "天蠍座": "情感強烈，需要深度連結",
            "射手座": "情感樂觀，需要自由空間",
            "摩羯座": "情感克制，需要穩定",
            "水瓶座": "情感超然，需要獨立",
            "雙魚座": "情感敏銳，需要精神寄託"
        }
        return moon_interpretations.get(sign, "情感需求特質")

    def _interpret_ascendant_sign(self, sign: str) -> str:
        """上升星座基本解讀"""
        asc_interpretations = {
            "白羊座": "給人積極主動的印象，生命態度直接",
            "金牛座": "給人穩重可靠的印象，重視實際",
            "雙子座": "給人機智活潑的印象，善於交際",
            "巨蟹座": "給人溫柔體貼的印象，較為保守",
            "獅子座": "給人自信大方的印象，具有領導氣質",
            "處女座": "給人謹慎細心的印象，注重細節",
            "天秤座": "給人優雅和善的印象，社交能力強",
            "天蠍座": "給人神秘深沉的印象，具有魅力",
            "射手座": "給人開朗樂觀的印象，熱愛探索",
            "摩羯座": "給人成熟穩重的印象，有責任感",
            "水瓶座": "給人獨特前衛的印象，思想自由",
            "雙魚座": "給人溫柔夢幻的印象，富有同情心"
        }
        return asc_interpretations.get(sign, "外在形象特質")

    def _interpret_aspect(self, planet1: str, planet2: str, aspect: str) -> str:
        """相位解讀（簡化版）"""
        # 相位基本含義
        aspect_meanings = {
            "合相": "能量融合，強化特質",
            "六分相": "和諧相處，機會之相",
            "四分相": "挑戰相位，需要整合",
            "三分相": "順暢和諧，天賦之相",
            "對分相": "對立張力，需要平衡"
        }

        base_meaning = aspect_meanings.get(aspect, "")
        return f"{planet1}與{planet2}形成{aspect}，{base_meaning}"

    def _find_house_for_planet(self, planet_lon: float, houses: Dict) -> int:
        """找出行星落在哪個宮位"""
        # 獲取12宮位的界線
        cusps = []
        for i in range(1, 13):
            cusps.append(houses[f"第{i}宮"]["cusp"])

        # 找出行星所在宮位
        for i in range(12):
            cusp_start = cusps[i]
            cusp_end = cusps[(i + 1) % 12]

            if cusp_end < cusp_start:
                # 跨越 0° 的情況
                if planet_lon >= cusp_start or planet_lon < cusp_end:
                    return i + 1
            else:
                if cusp_start <= planet_lon < cusp_end:
                    return i + 1

        return 1  # 默認第1宮

    def _interpret_planet_in_house(self, planet: str, house: int) -> str:
        """行星落宮位解讀（簡化版）"""
        house_meanings = {
            1: "自我認同與人格表現",
            2: "物質資源與價值觀",
            3: "溝通學習與鄰里關係",
            4: "家庭根基與情感基礎",
            5: "創造表現與戀愛娛樂",
            6: "工作健康與日常習慣",
            7: "伴侶關係與合作事務",
            8: "深度轉化與共享資源",
            9: "哲學信仰與遠行教育",
            10: "事業成就與社會地位",
            11: "友誼團體與未來願景",
            12: "潛意識與靈性超越"
        }

        return f"{planet}落{house}宮，影響{house_meanings.get(house, '生命領域')}"

    def _generate_summary(self, planets: Dict, houses: Dict) -> Dict:
        """生成星盤摘要"""
        return {
            "核心三要素": {
                "太陽星座": planets["太陽"]["position_text"],
                "月亮星座": planets["月亮"]["position_text"],
                "上升星座": houses["上升點"]["position_text"]
            },
            "個人行星": {
                "水星": planets["水星"]["position_text"],
                "金星": planets["金星"]["position_text"],
                "火星": planets["火星"]["position_text"]
            },
            "社會行星": {
                "木星": planets["木星"]["position_text"],
                "土星": planets["土星"]["position_text"]
            },
            "世代行星": {
                "天王星": planets["天王星"]["position_text"],
                "海王星": planets["海王星"]["position_text"],
                "冥王星": planets["冥王星"]["position_text"]
            },
            "四軸點": {
                "上升點": houses["上升點"]["position_text"],
                "天頂": houses["天頂"]["position_text"],
                "下降點": houses["下降點"]["position_text"],
                "天底": houses["天底"]["position_text"]
            }
        }


def quick_astrology_analysis(
    birth_datetime: datetime,
    latitude: float,
    longitude: float
) -> Dict:
    """快速占星分析"""
    calculator = AstrologyCalculator(birth_datetime, latitude, longitude)
    return calculator.analyze()


if __name__ == "__main__":
    print("西洋占星計算器 - 精簡版")
    print("配合 Swiss Ephemeris 使用")

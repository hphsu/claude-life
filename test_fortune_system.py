"""
綜合命理系統快速測試腳本
====================

測試三個計算引擎的功能
"""

import sys
from pathlib import Path

# 添加project root到路徑，這樣才能導入scripts.fortune_telling
sys.path.insert(0, str(Path(__file__).parent))

from datetime import datetime
import pytz

print("="*80)
print("🔮 綜合命理系統測試")
print("="*80)

# 測試導入
print("\n📦 測試模組導入...")

try:
    from scripts.fortune_telling.calendar_converter import CalendarConverter
    print("   ✅ calendar_converter 導入成功")
except Exception as e:
    print(f"   ❌ calendar_converter 導入失敗: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    from scripts.fortune_telling.bazi_calculator import BaziCalculator
    print("   ✅ bazi_calculator 導入成功")
except Exception as e:
    print(f"   ❌ bazi_calculator 導入失敗: {e}")
    sys.exit(1)

try:
    from scripts.fortune_telling.ziwei_calculator import ZiweiCalculator
    print("   ✅ ziwei_calculator 導入成功")
except Exception as e:
    print(f"   ❌ ziwei_calculator 導入失敗: {e}")
    sys.exit(1)

try:
    from scripts.fortune_telling.astrology_calculator import AstrologyCalculator
    print("   ✅ astrology_calculator 導入成功")
except Exception as e:
    print(f"   ❌ astrology_calculator 導入失敗: {e}")
    sys.exit(1)

try:
    from scripts.fortune_telling.utils import get_city_info
    print("   ✅ utils 導入成功")
except Exception as e:
    print(f"   ❌ utils 導入失敗: {e}")
    sys.exit(1)

print("\n✅ 所有模組導入成功！")

# 測試基本功能
print("\n" + "="*80)
print("🧪 測試基本功能")
print("="*80)

# 測試城市資訊
print("\n1. 測試城市資訊...")
city_info = get_city_info("台北")
if city_info:
    print(f"   ✅ 台北: 緯度{city_info['lat']}, 經度{city_info['lon']}, 時區{city_info['tz']}")
else:
    print("   ❌ 無法獲取台北城市資訊")

# 測試曆法轉換
print("\n2. 測試曆法轉換...")
try:
    location = "台北"
    city_info = get_city_info(location)
    tz = pytz.timezone(city_info['tz'])
    birth_dt = tz.localize(datetime(1990, 5, 15, 14, 30))

    converter = CalendarConverter()
    calendar_data = converter.convert_to_lunar(
        birth_date=birth_dt,
        location=location,
        use_true_solar_time=True
    )

    print(f"   ✅ 陽曆: {calendar_data['gregorian']['year']}-{calendar_data['gregorian']['month']}-{calendar_data['gregorian']['day']}")
    print(f"   ✅ 農曆: {calendar_data['lunar']['year']}年{calendar_data['lunar']['month_cn']}{calendar_data['lunar']['day_cn']}")
    print(f"   ✅ 四柱:")
    print(f"      年: {calendar_data['four_pillars']['year']['stem']}{calendar_data['four_pillars']['year']['branch']}")
    print(f"      月: {calendar_data['four_pillars']['month']['stem']}{calendar_data['four_pillars']['month']['branch']}")
    print(f"      日: {calendar_data['four_pillars']['day']['stem']}{calendar_data['four_pillars']['day']['branch']}")
    print(f"      時: {calendar_data['four_pillars']['hour']['stem']}{calendar_data['four_pillars']['hour']['branch']}")

except Exception as e:
    print(f"   ❌ 曆法轉換失敗: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 測試八字計算
print("\n3. 測試八字計算...")
try:
    bazi_calc = BaziCalculator(calendar_data=calendar_data)
    bazi_result = bazi_calc.analyze(gender="男", include_luck_pillars=True)

    print(f"   ✅ 八字: {bazi_result['basic_chart']['year']['pillar']} {bazi_result['basic_chart']['month']['pillar']} {bazi_result['basic_chart']['day']['pillar']} {bazi_result['basic_chart']['hour']['pillar']}")
    print(f"   ✅ 日元: {bazi_result['basic_chart']['day']['stem']}")
    print(f"   ✅ 五行平衡度: {bazi_result['wuxing_analysis']['balance_score']:.0%}")
    print(f"   ✅ 八字計算完成，包含 {len(bazi_result.keys())} 個分析維度")

except Exception as e:
    print(f"   ❌ 八字計算失敗: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 測試紫微斗數
print("\n4. 測試紫微斗數...")
try:
    ziwei_calc = ZiweiCalculator(calendar_data=calendar_data, gender="男")
    ziwei_result = ziwei_calc.analyze()

    print(f"   ✅ 命宮: {ziwei_result['palaces']['命宮']['branch']}")
    stars = ziwei_result['palaces']['命宮']['major_stars']
    print(f"   ✅ 命宮主星: {', '.join(stars) if stars else '無主星'}")
    print(f"   ✅ 命格: {ziwei_result['chart_summary']['命格特徵']}")

except Exception as e:
    print(f"   ❌ 紫微斗數失敗: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 測試占星計算
print("\n5. 測試占星計算...")
try:
    astrology_calc = AstrologyCalculator(
        birth_datetime=birth_dt,
        latitude=city_info['lat'],
        longitude=city_info['lon']
    )
    astrology_result = astrology_calc.analyze()

    print(f"   ✅ 太陽: {astrology_result['planets']['太陽']['position_text']}")
    print(f"   ✅ 月亮: {astrology_result['planets']['月亮']['position_text']}")
    print(f"   ✅ 上升: {astrology_result['houses']['上升點']['position_text']}")

except Exception as e:
    print(f"   ❌ 占星計算失敗: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 總結
print("\n" + "="*80)
print("🎉 所有測試通過！")
print("="*80)
print("\n✅ 綜合命理系統運行正常")
print("\n下一步：執行 /fortune-tell 命令開始使用")
print("="*80 + "\n")

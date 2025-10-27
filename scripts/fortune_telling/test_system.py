"""
綜合命理系統測試腳本
====================

測試三個計算引擎的功能和整合
"""

from datetime import datetime
import pytz
import json
from pathlib import Path
import sys

# 添加當前目錄到 Python 路徑
sys.path.insert(0, str(Path(__file__).parent))

# 使用絕對導入
import sys
import importlib.util

# 動態載入模組
def load_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# 獲取當前目錄
current_dir = Path(__file__).parent

# 載入所有需要的模組
utils = load_module('utils', current_dir / 'utils.py')
calendar_converter = load_module('calendar_converter', current_dir / 'calendar_converter.py')
bazi_calculator = load_module('bazi_calculator', current_dir / 'bazi_calculator.py')
ziwei_calculator = load_module('ziwei_calculator', current_dir / 'ziwei_calculator.py')
astrology_calculator = load_module('astrology_calculator', current_dir / 'astrology_calculator.py')

CalendarConverter = calendar_converter.CalendarConverter
BaziCalculator = bazi_calculator.BaziCalculator
ZiweiCalculator = ziwei_calculator.ZiweiCalculator
AstrologyCalculator = astrology_calculator.AstrologyCalculator
get_city_info = utils.get_city_info


def test_calendar_conversion():
    """測試曆法轉換"""
    print("\n" + "="*60)
    print("🧪 測試 1：曆法轉換 (Calendar Conversion)")
    print("="*60)

    try:
        # 創建測試案例
        test_date = datetime(1990, 5, 15, 14, 30)
        location = "台北"

        # 獲取城市資訊
        city_info = get_city_info(location)
        tz = pytz.timezone(city_info['tz'])
        birth_dt = tz.localize(test_date)

        # 轉換為農曆
        converter = CalendarConverter()
        calendar_data = converter.convert_to_lunar(
            birth_date=birth_dt,
            location=location,
            use_true_solar_time=True
        )

        # 顯示結果
        print(f"\n📅 陽曆：{calendar_data['gregorian']['year']}年{calendar_data['gregorian']['month']}月{calendar_data['gregorian']['day']}日")
        print(f"📅 農曆：{calendar_data['lunar']['year']}年{calendar_data['lunar']['month_chinese']}{calendar_data['lunar']['day_chinese']}")
        print(f"📅 四柱：")
        print(f"   年柱：{calendar_data['four_pillars']['year']['stem']}{calendar_data['four_pillars']['year']['branch']}")
        print(f"   月柱：{calendar_data['four_pillars']['month']['stem']}{calendar_data['four_pillars']['month']['branch']}")
        print(f"   日柱：{calendar_data['four_pillars']['day']['stem']}{calendar_data['four_pillars']['day']['branch']}")
        print(f"   時柱：{calendar_data['four_pillars']['hour']['stem']}{calendar_data['four_pillars']['hour']['branch']}")

        print("\n✅ 曆法轉換測試通過")
        return True, calendar_data

    except Exception as e:
        print(f"\n❌ 曆法轉換測試失敗：{str(e)}")
        import traceback
        traceback.print_exc()
        return False, None


def test_bazi_calculator(calendar_data):
    """測試八字計算器"""
    print("\n" + "="*60)
    print("🧪 測試 2：八字計算 (BaZi Calculator)")
    print("="*60)

    try:
        # 初始化八字計算器
        bazi_calc = BaziCalculator(
            calendar_data=calendar_data,
            gender="男"
        )

        # 執行分析
        bazi_result = bazi_calc.analyze(
            gender="男",
            include_luck_pillars=True
        )

        # 顯示核心結果
        print(f"\n📊 八字：")
        print(f"   {bazi_result['basic_chart']['year_pillar']} (年)")
        print(f"   {bazi_result['basic_chart']['month_pillar']} (月)")
        print(f"   {bazi_result['basic_chart']['day_pillar']} (日)")
        print(f"   {bazi_result['basic_chart']['hour_pillar']} (時)")

        print(f"\n🌟 五行分析：")
        for element, count in bazi_result['wuxing_analysis']['element_count'].items():
            print(f"   {element}：{count}")
        print(f"   平衡度：{bazi_result['wuxing_analysis']['balance_score']:.2%}")

        print(f"\n🎯 格局：{bazi_result['pattern']['name']}")
        print(f"   強度：{bazi_result['strength']['overall_strength']}")
        print(f"   用神：{bazi_result['yongshen']['primary']}")

        print(f"\n💼 事業：{bazi_result['destiny_features']['career']['overall']}")
        print(f"💰 財運：{bazi_result['destiny_features']['wealth']['overall']}")
        print(f"💖 感情：{bazi_result['destiny_features']['relationship']['overall']}")

        print("\n✅ 八字計算測試通過")
        return True, bazi_result

    except Exception as e:
        print(f"\n❌ 八字計算測試失敗：{str(e)}")
        import traceback
        traceback.print_exc()
        return False, None


def test_ziwei_calculator(calendar_data):
    """測試紫微計算器"""
    print("\n" + "="*60)
    print("🧪 測試 3：紫微斗數 (Ziwei Calculator)")
    print("="*60)

    try:
        # 初始化紫微計算器
        ziwei_calc = ZiweiCalculator(
            calendar_data=calendar_data,
            gender="男"
        )

        # 執行分析
        ziwei_result = ziwei_calc.analyze()

        # 顯示核心結果
        print(f"\n🏠 命宮：{ziwei_result['palaces']['命宮']['branch']}")
        print(f"   主星：{', '.join(ziwei_result['palaces']['命宮']['major_stars']) if ziwei_result['palaces']['命宮']['major_stars'] else '無主星'}")

        print(f"\n⭐ 紫微星位置：{ziwei_result['ziwei_position']}")

        print(f"\n✨ 四化：")
        for transform_type, star in ziwei_result['four_transformations'].items():
            print(f"   {transform_type}：{star}")

        print(f"\n📋 命盤摘要：")
        print(f"   命宮主星：{', '.join(ziwei_result['chart_summary']['命宮主星'])}")
        print(f"   財帛主星：{', '.join(ziwei_result['chart_summary']['財帛主星'])}")
        print(f"   官祿主星：{', '.join(ziwei_result['chart_summary']['官祿主星'])}")
        print(f"   命格特徵：{ziwei_result['chart_summary']['命格特徵']}")

        print("\n✅ 紫微斗數測試通過")
        return True, ziwei_result

    except Exception as e:
        print(f"\n❌ 紫微斗數測試失敗：{str(e)}")
        import traceback
        traceback.print_exc()
        return False, None


def test_astrology_calculator():
    """測試占星計算器"""
    print("\n" + "="*60)
    print("🧪 測試 4：西洋占星 (Astrology Calculator)")
    print("="*60)

    try:
        # 創建測試案例
        location = "台北"
        city_info = get_city_info(location)
        tz = pytz.timezone(city_info['tz'])
        birth_dt = tz.localize(datetime(1990, 5, 15, 14, 30))

        # 初始化占星計算器
        astrology_calc = AstrologyCalculator(
            birth_datetime=birth_dt,
            latitude=city_info['lat'],
            longitude=city_info['lon']
        )

        # 執行分析
        astrology_result = astrology_calc.analyze()

        # 顯示核心結果
        print(f"\n☀️ 太陽：{astrology_result['planets']['太陽']['position_text']}")
        print(f"🌙 月亮：{astrology_result['planets']['月亮']['position_text']}")
        print(f"⬆️ 上升：{astrology_result['houses']['上升點']['position_text']}")

        print(f"\n🌍 個人行星：")
        print(f"   水星：{astrology_result['planets']['水星']['position_text']}")
        print(f"   金星：{astrology_result['planets']['金星']['position_text']}")
        print(f"   火星：{astrology_result['planets']['火星']['position_text']}")

        print(f"\n🔭 社會行星：")
        print(f"   木星：{astrology_result['planets']['木星']['position_text']}")
        print(f"   土星：{astrology_result['planets']['土星']['position_text']}")

        print(f"\n⚡ 重要相位（前3個）：")
        for i, aspect in enumerate(astrology_result['aspects'][:3], 1):
            print(f"   {i}. {aspect['planet1']} {aspect['aspect']} {aspect['planet2']}")
            print(f"      強度：{aspect['strength']:.0%}，容許度：{aspect['orb']:.2f}°")

        print(f"\n📖 核心解讀：")
        print(f"   太陽星座：{astrology_result['interpretations']['太陽星座']['sign']}")
        print(f"   {astrology_result['interpretations']['太陽星座']['meaning']}")
        print(f"\n   月亮星座：{astrology_result['interpretations']['月亮星座']['sign']}")
        print(f"   {astrology_result['interpretations']['月亮星座']['meaning']}")
        print(f"\n   上升星座：{astrology_result['interpretations']['上升星座']['sign']}")
        print(f"   {astrology_result['interpretations']['上升星座']['meaning']}")

        print("\n✅ 西洋占星測試通過")
        return True, astrology_result

    except Exception as e:
        print(f"\n❌ 西洋占星測試失敗：{str(e)}")
        import traceback
        traceback.print_exc()
        return False, None


def test_full_system():
    """完整系統測試"""
    print("\n" + "="*80)
    print("🔮 綜合命理系統完整測試")
    print("="*80)

    results = {}

    # 測試 1：曆法轉換
    success, calendar_data = test_calendar_conversion()
    results['calendar'] = success

    if not success or calendar_data is None:
        print("\n❌ 曆法轉換失敗，無法繼續測試")
        return

    # 測試 2：八字計算
    success, bazi_result = test_bazi_calculator(calendar_data)
    results['bazi'] = success

    # 測試 3：紫微斗數
    success, ziwei_result = test_ziwei_calculator(calendar_data)
    results['ziwei'] = success

    # 測試 4：西洋占星
    success, astrology_result = test_astrology_calculator()
    results['astrology'] = success

    # 總結
    print("\n" + "="*80)
    print("📊 測試結果總結")
    print("="*80)

    all_passed = all(results.values())

    for test_name, passed in results.items():
        status = "✅ 通過" if passed else "❌ 失敗"
        print(f"{test_name.upper():<15} : {status}")

    print("\n" + "="*80)

    if all_passed:
        print("🎉 所有測試通過！系統運行正常。")
        print("\n下一步：")
        print("1. 執行命令：/fortune-tell")
        print("2. 跟隨互動式輸入提示")
        print("3. 查看完整分析報告")
    else:
        print("⚠️ 部分測試失敗，請檢查錯誤訊息並修正。")

    print("="*80 + "\n")


if __name__ == "__main__":
    test_full_system()

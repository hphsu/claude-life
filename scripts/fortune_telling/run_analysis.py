"""
綜合命理分析執行腳本
====================

為 jirline 執行完整的三合一命理分析
"""

from datetime import datetime
import pytz
import json
from pathlib import Path
import sys

# 添加父目錄到 Python 路徑以支持包導入
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# 使用標準包導入
from fortune_telling.utils import get_city_info
from fortune_telling.calendar_converter import CalendarConverter
from fortune_telling.bazi_calculator import BaziCalculator
from fortune_telling.ziwei_calculator import ZiweiCalculator
from fortune_telling.astrology_calculator import AstrologyCalculator
from fortune_telling import bazi_interpretation
from fortune_telling import ziwei_interpretation
from fortune_telling import astrology_interpretation
from fortune_telling import synthesis_engine
from fortune_telling.html_report_generator import generate_html_report


def main():
    """執行完整分析"""

    # ========================================
    # 基本資訊
    # ========================================
    name = "jirline"
    birth_date_str = "1994-04-14 21:40"
    location = "台北"  # taipei -> 台北
    gender = "女"
    use_true_solar_time = False

    print("=" * 80)
    print("🔮 綜合命理分析系統")
    print("=" * 80)
    print(f"\n📋 基本資訊：")
    print(f"   姓名：{name}")
    print(f"   出生：{birth_date_str}（陽曆）")
    print(f"   地點：{location}")
    print(f"   性別：{gender}")
    print(f"   真太陽時修正：{'是' if use_true_solar_time else '否'}")

    # ========================================
    # 階段 1：準備計算資料
    # ========================================
    print("\n" + "=" * 80)
    print("📊 階段 1：準備計算資料")
    print("=" * 80)

    try:
        # 解析出生時間
        birth_dt = datetime.strptime(birth_date_str, "%Y-%m-%d %H:%M")

        # 獲取城市資訊
        city_info = get_city_info(location)
        if not city_info:
            raise ValueError(f"找不到城市：{location}")

        print(f"✅ 城市資訊：{location}")
        print(f"   經度：{city_info['lon']}")
        print(f"   緯度：{city_info['lat']}")
        print(f"   時區：{city_info['tz']}")

        # 設定時區
        tz = pytz.timezone(city_info['tz'])
        birth_dt = tz.localize(birth_dt)

        # 轉換為農曆並獲取四柱
        print(f"\n🔄 正在進行曆法轉換...")
        converter = CalendarConverter()
        calendar_data = converter.convert_to_lunar(
            birth_date=birth_dt,
            location=location,
            use_true_solar_time=use_true_solar_time
        )

        print(f"✅ 曆法轉換完成")
        print(f"   陽曆：{calendar_data['gregorian']['year']}年{calendar_data['gregorian']['month']}月{calendar_data['gregorian']['day']}日 {calendar_data['gregorian']['hour']}時{calendar_data['gregorian']['minute']}分")
        print(f"   農曆：{calendar_data['lunar']['year']}年{calendar_data['lunar']['month']}月{calendar_data['lunar']['day']}日")
        print(f"   四柱：")
        print(f"      年柱：{calendar_data['four_pillars']['year']['pillar']}")
        print(f"      月柱：{calendar_data['four_pillars']['month']['pillar']}")
        print(f"      日柱：{calendar_data['four_pillars']['day']['pillar']}")
        print(f"      時柱：{calendar_data['four_pillars']['hour']['pillar']}")

    except Exception as e:
        print(f"❌ 資料準備失敗：{str(e)}")
        import traceback
        traceback.print_exc()
        return

    # ========================================
    # 階段 2：執行三個分析引擎
    # ========================================
    print("\n" + "=" * 80)
    print("🔬 階段 2：執行三大命理分析")
    print("=" * 80)

    # 2.1 八字分析
    print("\n📚 正在執行八字分析...")
    try:
        bazi_calc = BaziCalculator(calendar_data=calendar_data)
        bazi_result = bazi_calc.analyze(gender=gender, include_luck_pillars=True)
        print("✅ 八字分析完成")
    except Exception as e:
        print(f"❌ 八字分析失敗：{str(e)}")
        import traceback
        traceback.print_exc()
        bazi_result = None

    # 2.2 紫微斗數分析
    print("\n🌟 正在執行紫微斗數分析...")
    try:
        ziwei_calc = ZiweiCalculator(calendar_data=calendar_data, gender=gender)
        ziwei_result = ziwei_calc.analyze()
        print("✅ 紫微斗數分析完成")
    except Exception as e:
        print(f"❌ 紫微斗數分析失敗：{str(e)}")
        import traceback
        traceback.print_exc()
        ziwei_result = None

    # 2.3 占星分析
    print("\n⭐ 正在執行西洋占星分析...")
    try:
        astrology_calc = AstrologyCalculator(
            birth_datetime=birth_dt,
            latitude=city_info['lat'],
            longitude=city_info['lon']
        )
        astrology_result = astrology_calc.analyze()
        print("✅ 西洋占星分析完成")
    except Exception as e:
        print(f"❌ 西洋占星分析失敗：{str(e)}")
        import traceback
        traceback.print_exc()
        astrology_result = None

    # ========================================
    # 階段 3：深度解釋
    # ========================================
    print("\n" + "=" * 80)
    print("💡 階段 3：深度解釋")
    print("=" * 80)

    # 3.1 八字深度解釋
    if bazi_result:
        print("\n📖 正在進行八字深度解釋...")
        try:
            # 八字解釋需要分別調用各領域函數
            bazi_interp = {
                'personality': bazi_interpretation.interpret_personality(bazi_result),
                'career': bazi_interpretation.interpret_career(bazi_result),
                'wealth': bazi_interpretation.interpret_wealth(bazi_result),
                'relationship': bazi_interpretation.interpret_relationship(bazi_result, gender='female' if gender == '女' else 'male'),
                'health': bazi_interpretation.interpret_health(bazi_result)
            }
            print("✅ 八字深度解釋完成")
        except Exception as e:
            print(f"❌ 八字解釋失敗：{str(e)}")
            import traceback
            traceback.print_exc()
            bazi_interp = None
    else:
        bazi_interp = None

    # 3.2 紫微深度解釋
    if ziwei_result:
        print("\n📖 正在進行紫微斗數深度解釋...")
        try:
            ziwei_interp = ziwei_interpretation.interpret_ziwei_palaces(ziwei_result)
            print("✅ 紫微斗數深度解釋完成")
        except Exception as e:
            print(f"❌ 紫微解釋失敗：{str(e)}")
            ziwei_interp = None
    else:
        ziwei_interp = None

    # 3.3 占星深度解釋
    if astrology_result:
        print("\n📖 正在進行心理占星深度解釋...")
        try:
            astro_interp = astrology_interpretation.interpret_natal_chart(astrology_result)
            print("✅ 心理占星深度解釋完成")
        except Exception as e:
            print(f"❌ 占星解釋失敗：{str(e)}")
            astro_interp = None
    else:
        astro_interp = None

    # ========================================
    # 階段 4：跨方法綜合分析
    # ========================================
    print("\n" + "=" * 80)
    print("🧩 階段 4：跨方法綜合分析")
    print("=" * 80)

    if bazi_interp and ziwei_interp and astro_interp:
        print("\n🔄 正在進行三方法綜合分析...")
        try:
            synthesis = synthesis_engine.synthesize_three_methods(
                bazi_result=bazi_interp,
                ziwei_result=ziwei_interp,
                astro_result=astro_interp
            )
            print("✅ 綜合分析完成")
        except Exception as e:
            print(f"❌ 綜合分析失敗：{str(e)}")
            import traceback
            traceback.print_exc()
            synthesis = None
    else:
        print("⚠️ 跳過綜合分析（缺少必要的解釋結果）")
        synthesis = None

    # ========================================
    # 階段 5：生成完整報告
    # ========================================
    print("\n" + "=" * 80)
    print("📝 階段 5：生成完整報告")
    print("=" * 80)

    # 組裝完整結果
    full_report = {
        "basic_info": {
            "name": name,
            "birth_gregorian": birth_date_str,
            "birth_lunar": f"{calendar_data['lunar']['year']}年{calendar_data['lunar']['month']}月{calendar_data['lunar']['day']}日",
            "location": location,
            "gender": gender,
            "true_solar_time": use_true_solar_time
        },
        "calendar_data": calendar_data,
        "bazi": {
            "calculation": bazi_result,
            "interpretation": bazi_interp
        },
        "ziwei": {
            "calculation": ziwei_result,
            "interpretation": ziwei_interp
        },
        "astrology": {
            "calculation": astrology_result,
            "interpretation": astro_interp
        },
        "synthesis": synthesis
    }

    # 儲存結果
    output_dir = Path(__file__).parent.parent.parent / "data" / "fortune-telling"
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 保存 JSON 格式
    json_file = output_dir / f"fortune_tell_{name}_{timestamp}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(full_report, f, ensure_ascii=False, indent=2, default=str)
    print(f"✅ JSON報告已儲存：{json_file}")

    # 生成 HTML 格式報告
    html_file = output_dir / f"fortune_tell_{name}_{timestamp}.html"
    try:
        generate_html_report(full_report, str(html_file))
        print(f"✅ HTML報告已儲存：{html_file}")
    except Exception as e:
        print(f"⚠️  HTML報告生成失敗：{str(e)}")
        import traceback
        traceback.print_exc()

    # 返回結果供後續處理
    return full_report


if __name__ == "__main__":
    result = main()
    print("\n" + "=" * 80)
    print("✨ 分析完成！")
    print("=" * 80)

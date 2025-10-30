"""
命理分析通用執行腳本 - 接受命令行參數
"""

from datetime import datetime
import pytz
import json
from pathlib import Path
import sys
import argparse

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
from fortune_telling.progress_tracker import init_tracker


def parse_arguments():
    """解析命令行參數"""
    parser = argparse.ArgumentParser(
        description='綜合命理分析系統 - 整合八字、紫微、占星',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('name', help='姓名')
    parser.add_argument('birth_date', help='出生日期 (YYYY-MM-DD)')
    parser.add_argument('birth_time', help='出生時間 (HH:MMam/pm，例如: 06:00am)')
    parser.add_argument('location', help='出生地點 (城市名稱，例如: miaoli 或 taipei)')
    parser.add_argument('gender', choices=['male', 'female'], help='性別 (male 或 female)')
    parser.add_argument('--true-solar-time', action='store_true',
                       help='是否使用真太陽時修正 (預設: 否)')

    return parser.parse_args()


def parse_birth_datetime(date_str, time_str):
    """
    解析出生日期和時間

    Args:
        date_str: YYYY-MM-DD 格式
        time_str: HH:MMam/pm 格式，例如 06:00am 或 11:30pm

    Returns:
        datetime_str: YYYY-MM-DD HH:MM 格式字串
    """
    # 移除 time_str 中的空格
    time_str = time_str.replace(' ', '').lower()

    # 分離時間和 am/pm
    if 'am' in time_str:
        time_part = time_str.replace('am', '')
        is_pm = False
    elif 'pm' in time_str:
        time_part = time_str.replace('pm', '')
        is_pm = True
    else:
        raise ValueError("時間必須包含 am 或 pm，例如: 06:00am")

    # 解析時間
    try:
        hour, minute = map(int, time_part.split(':'))
    except ValueError:
        raise ValueError(f"無效的時間格式: {time_str}，應該是 HH:MM 格式")

    # 轉換為24小時制
    if is_pm and hour != 12:
        hour += 12
    elif not is_pm and hour == 12:
        hour = 0

    # 組合完整時間字串
    datetime_str = f"{date_str} {hour:02d}:{minute:02d}"
    return datetime_str


def extract_city_name(location_str):
    """
    從位置字串中提取城市名稱

    Args:
        location_str: 可能包含 "城市, 地區" 或只有 "城市" 的字串

    Returns:
        city_name: 城市名稱（小寫）
    """
    # 移除引號
    location_str = location_str.strip('"').strip("'")

    # 如果包含逗號，取第一部分
    if ',' in location_str:
        city_name = location_str.split(',')[0].strip()
    else:
        city_name = location_str.strip()

    return city_name.lower()


def convert_gender(gender_en):
    """將英文性別轉換為中文"""
    return "男" if gender_en.lower() == "male" else "女"


def main():
    """執行完整分析"""

    # 初始化進度追蹤器
    tracker = init_tracker()

    # 註冊所有分析階段
    tracker.add_stage('parse', '解析輸入參數', '📝')
    tracker.add_stage('prepare', '準備計算資料', '📊')
    tracker.add_stage('bazi', '執行八字分析', '📚')
    tracker.add_stage('ziwei', '執行紫微斗數分析', '🌟')
    tracker.add_stage('astrology', '執行西洋占星分析', '⭐')
    tracker.add_stage('assemble', '組裝分析結果', '📝')
    tracker.add_stage('save', '儲存計算結果', '💾')

    # 解析命令行參數
    tracker.start_stage('parse')
    args = parse_arguments()

    # 轉換參數
    name = args.name
    birth_date_str = parse_birth_datetime(args.birth_date, args.birth_time)
    location = extract_city_name(args.location)
    gender = convert_gender(args.gender)
    use_true_solar_time = args.true_solar_time

    print("=" * 80)
    print("🔮 綜合命理分析系統")
    print("=" * 80)
    print(f"\n📋 基本資訊：")
    print(f"   姓名：{name}")
    print(f"   出生：{birth_date_str}（陽曆）")
    print(f"   地點：{location}")
    print(f"   性別：{gender}")
    print(f"   真太陽時修正：{'是' if use_true_solar_time else '否'}")

    tracker.complete_stage('parse')

    # ========================================
    # 階段 1：準備計算資料
    # ========================================
    tracker.start_stage('prepare')
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

        tracker.complete_stage('prepare')

    except Exception as e:
        print(f"❌ 資料準備失敗：{str(e)}")
        tracker.fail_stage('prepare', str(e))
        import traceback
        traceback.print_exc()
        return None

    # ========================================
    # 階段 2：執行三個分析引擎
    # ========================================
    print("\n" + "=" * 80)
    print("🔬 階段 2：執行三大命理分析")
    print("=" * 80)

    # 2.1 八字分析
    tracker.start_stage('bazi')
    print("\n📚 正在執行八字分析...")
    try:
        bazi_calc = BaziCalculator(calendar_data=calendar_data)
        bazi_result = bazi_calc.analyze(gender=gender, include_luck_pillars=True)
        print("✅ 八字分析完成")
        tracker.complete_stage('bazi')
    except Exception as e:
        print(f"❌ 八字分析失敗：{str(e)}")
        tracker.fail_stage('bazi', str(e))
        import traceback
        traceback.print_exc()
        bazi_result = None

    # 2.2 紫微斗數分析
    tracker.start_stage('ziwei')
    print("\n🌟 正在執行紫微斗數分析...")
    try:
        ziwei_calc = ZiweiCalculator(calendar_data=calendar_data, gender=gender)
        ziwei_result = ziwei_calc.analyze()
        print("✅ 紫微斗數分析完成")
        tracker.complete_stage('ziwei')
    except Exception as e:
        print(f"❌ 紫微斗數分析失敗：{str(e)}")
        tracker.fail_stage('ziwei', str(e))
        import traceback
        traceback.print_exc()
        ziwei_result = None

    # 2.3 占星分析
    tracker.start_stage('astrology')
    print("\n⭐ 正在執行西洋占星分析...")
    try:
        astrology_calc = AstrologyCalculator(
            birth_datetime=birth_dt,
            latitude=city_info['lat'],
            longitude=city_info['lon']
        )
        astrology_result = astrology_calc.analyze()
        print("✅ 西洋占星分析完成")
        tracker.complete_stage('astrology')
    except Exception as e:
        print(f"❌ 西洋占星分析失敗：{str(e)}")
        tracker.fail_stage('astrology', str(e))
        import traceback
        traceback.print_exc()
        astrology_result = None

    # ========================================
    # 階段 3：組裝完整結果 (不包含深度解釋和綜合分析)
    # ========================================
    tracker.start_stage('assemble')
    print("\n" + "=" * 80)
    print("📝 階段 3：組裝分析結果")
    print("=" * 80)

    print("\nℹ️  注意：深度解釋和綜合分析將由 AI 專家代理執行")

    # 組裝完整結果（僅包含計算結果，不包含解釋）
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
            "calculation": bazi_result
        },
        "ziwei": {
            "calculation": ziwei_result
        },
        "astrology": {
            "calculation": astrology_result
        }
    }

    tracker.complete_stage('assemble')

    # ========================================
    # 階段 4：儲存計算結果
    # ========================================
    tracker.start_stage('save')
    print("\n" + "=" * 80)
    print("💾 階段 4：儲存計算結果")
    print("=" * 80)

    # 儲存結果
    output_dir = Path(__file__).parent.parent.parent / "data" / "fortune-telling"
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 保存 JSON 格式
    json_file = output_dir / f"fortune_tell_{name}_{timestamp}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(full_report, f, ensure_ascii=False, indent=2, default=str)
    print(f"✅ 計算結果已儲存：{json_file}")

    tracker.complete_stage('save')

    # 顯示進度總結
    tracker.show_summary()

    # 返回文件路徑和結果
    print(f"\n📦 JSON 文件路徑：{json_file}")

    return {
        'json_file': str(json_file),
        'timestamp': timestamp,
        'report': full_report
    }


if __name__ == "__main__":
    result = main()
    if result:
        print("\n" + "=" * 80)
        print("✨ 計算完成！")
        print("=" * 80)
        print(f"\n📂 結果文件：{result['json_file']}")
        print("\n下一步：使用 /fortune-analyze 命令運行 AI 專家分析")
    else:
        print("\n" + "=" * 80)
        print("❌ 計算失敗！")
        print("=" * 80)
        sys.exit(1)

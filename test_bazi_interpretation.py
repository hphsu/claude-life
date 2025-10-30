"""
測試八字深度詮釋引擎
"""

import json
from scripts.fortune_telling.calendar_converter import CalendarConverter
from scripts.fortune_telling.bazi_calculator import BaziCalculator
from scripts.fortune_telling.bazi_interpretation import (
    interpret_personality,
    interpret_career,
    interpret_wealth,
    interpret_relationship,
    interpret_health
)


def test_bazi_interpretation():
    """測試八字詮釋功能"""

    print("=" * 60)
    print("測試八字深度詮釋引擎")
    print("=" * 60)

    # 使用測試數據：1994年4月14日 下午2點，汕頭
    year = 1994
    month = 4
    day = 14
    hour = 14
    minute = 0
    city_name = "汕頭"
    gender = "女"

    print(f"\n測試對象：{year}年{month}月{day}日 {hour}:{minute:02d} {city_name} {gender}命")
    print("-" * 60)

    # 1. 曆法轉換
    print("\n步驟 1：曆法轉換...")
    converter = CalendarConverter(
        year, month, day, hour, minute,
        city_name=city_name
    )
    calendar_data = converter.convert()
    print("✓ 曆法轉換完成")

    # 2. 八字計算
    print("\n步驟 2：八字計算...")
    calculator = BaziCalculator(calendar_data)
    bazi_data = calculator.analyze(gender=gender)
    print("✓ 八字計算完成")

    # 顯示基本命盤
    print(f"\n基本命盤：")
    print(f"  年柱：{bazi_data['basic_chart']['year']['pillar']}")
    print(f"  月柱：{bazi_data['basic_chart']['month']['pillar']}")
    print(f"  日柱：{bazi_data['basic_chart']['day']['pillar']}")
    print(f"  時柱：{bazi_data['basic_chart']['hour']['pillar']}")
    print(f"  日主：{bazi_data['basic_chart']['day_master']}")
    print(f"  身強弱：{bazi_data['strength']['level']}")

    # 3. 性格詮釋
    print("\n" + "=" * 60)
    print("步驟 3：性格詮釋")
    print("=" * 60)
    personality = interpret_personality(bazi_data)
    print("\n【日主本質】")
    print(personality['core_personality']['day_master_essence'])
    print(f"\n【優勢】：{', '.join(personality['core_personality']['strengths'])}")
    print(f"【挑戰】：{', '.join(personality['core_personality']['challenges'])}")
    print(f"【成長路徑】：{personality['core_personality']['growth_path']}")

    # 4. 事業詮釋
    print("\n" + "=" * 60)
    print("步驟 4：事業詮釋")
    print("=" * 60)
    career = interpret_career(bazi_data)
    print(f"\n【事業評分】：{career['overall_rating']}/10")
    print(f"\n【總結】")
    print(career['summary'])

    if career['aptitude_assessment']['natural_talents']:
        print(f"\n【天賦才能】")
        for talent in career['aptitude_assessment']['natural_talents']:
            print(f"  - {talent['talent']}")
            print(f"    來源：{talent['source']}")
            print(f"    表現：{talent['manifestation']}")

    # 5. 財富詮釋
    print("\n" + "=" * 60)
    print("步驟 5：財富詮釋")
    print("=" * 60)
    wealth = interpret_wealth(bazi_data)
    print(f"\n【財富評分】：{wealth['overall_rating']}/10")

    if wealth['wealth_capacity']['earning_potential']:
        print(f"\n【賺錢能力】")
        print(wealth['wealth_capacity']['earning_potential'])

    if wealth['specific_recommendations']:
        print(f"\n【財富建議】")
        for rec in wealth['specific_recommendations']:
            print(f"  - {rec['recommendation']}")

    # 6. 感情詮釋
    print("\n" + "=" * 60)
    print("步驟 6：感情詮釋")
    print("=" * 60)
    relationship = interpret_relationship(bazi_data, gender=gender)
    print(f"\n【感情評分】：{relationship['overall_rating']}/10")
    print(f"\n【理想伴侶】")
    print(relationship['spouse_characteristics']['ideal_partner_profile'])

    # 7. 健康詮釋
    print("\n" + "=" * 60)
    print("步驟 7：健康詮釋")
    print("=" * 60)
    health = interpret_health(bazi_data)
    print(f"\n【健康評分】：{health['overall_rating']:.1f}/10")

    print(f"\n【五行健康對應】")
    for wx, info in health['elemental_health_mapping'].items():
        print(f"  {wx}：{info['status']} - {info['implications']}")

    # 8. 生成完整報告
    print("\n" + "=" * 60)
    print("步驟 8：生成完整詮釋報告")
    print("=" * 60)

    full_interpretation = {
        "basic_info": {
            "birth_date": f"{year}-{month:02d}-{day:02d} {hour}:{minute:02d}",
            "location": city_name,
            "gender": gender,
            "four_pillars": {
                "year": bazi_data['basic_chart']['year']['pillar'],
                "month": bazi_data['basic_chart']['month']['pillar'],
                "day": bazi_data['basic_chart']['day']['pillar'],
                "hour": bazi_data['basic_chart']['hour']['pillar']
            },
            "day_master": bazi_data['basic_chart']['day_master'],
            "strength": bazi_data['strength']['level']
        },
        "personality": personality,
        "career": career,
        "wealth": wealth,
        "relationship": relationship,
        "health": health
    }

    # 保存到文件
    output_file = "data/fortune-telling/test_bazi_interpretation_result.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(full_interpretation, f, ensure_ascii=False, indent=2)

    print(f"✓ 完整詮釋報告已保存至：{output_file}")

    print("\n" + "=" * 60)
    print("✅ 測試完成！")
    print("=" * 60)

    return full_interpretation


if __name__ == "__main__":
    test_bazi_interpretation()

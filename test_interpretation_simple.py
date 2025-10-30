"""
簡化版測試 - 測試八字詮釋引擎的核心邏輯
"""

import sys
import json
from pathlib import Path

# 添加 scripts 目錄到路徑
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

# 模擬八字分析數據（簡化版）
mock_bazi_data = {
    "basic_chart": {
        "year": {"pillar": "甲戌", "stem": "甲", "branch": "戌"},
        "month": {"pillar": "戊辰", "stem": "戊", "branch": "辰"},
        "day": {"pillar": "甲寅", "stem": "甲", "branch": "寅"},
        "hour": {"pillar": "辛未", "stem": "辛", "branch": "未"},
        "day_master": "甲",
        "day_master_wuxing": "木"
    },
    "wuxing_analysis": {
        "counts": {"木": 4, "火": 2, "土": 5, "金": 3, "水": 1},
        "total": 15,
        "average": 3.0,
        "missing": [],
        "weak": ["水"],
        "strong": ["土", "木"],
        "balance_score": 0.65
    },
    "ten_gods_analysis": {
        "year": "比肩",
        "month": "正印",
        "day": "比肩",
        "hour": "正財",
        "distribution": {
            "比肩": 1,
            "劫財": 0,
            "食神": 0,
            "傷官": 0,
            "偏財": 0,
            "正財": 1,
            "七殺": 0,
            "正官": 0,
            "偏印": 0,
            "正印": 1
        },
        "dominant": ["比肩", "正印"],
        "interpretation": {}
    },
    "strength": {
        "level": "身中和",
        "score": 1.1,
        "description": "日主力量適中，平衡穩定"
    },
    "yongshen": {
        "yongshen": ["水", "金"],
        "xishen": [],
        "jishen": ["土"],
        "day_master_wuxing": "木"
    },
    "luck_pillars": [
        {
            "sequence": 1,
            "age_range": "3-12歲",
            "pillar": "己巳",
            "stem": "己",
            "branch": "巳"
        },
        {
            "sequence": 2,
            "age_range": "13-22歲",
            "pillar": "庚午",
            "stem": "庚",
            "branch": "午"
        }
    ]
}


def test_interpretation_functions():
    """測試各個詮釋函數"""

    print("=" * 60)
    print("測試八字深度詮釋引擎（簡化版）")
    print("=" * 60)

    try:
        # 直接導入詮釋模組文件（避免 __init__.py 的依賴）
        import importlib.util

        module_path = Path(__file__).parent / "scripts" / "fortune_telling" / "bazi_interpretation.py"
        spec = importlib.util.spec_from_file_location("bazi_interpretation", module_path)
        bazi_interp = importlib.util.module_from_spec(spec)

        # 同時需要載入 utils.py 因為 bazi_interpretation 依賴它
        utils_path = Path(__file__).parent / "scripts" / "fortune_telling" / "utils.py"
        utils_spec = importlib.util.spec_from_file_location("utils", utils_path)
        utils_module = importlib.util.module_from_spec(utils_spec)
        sys.modules['utils'] = utils_module
        utils_spec.loader.exec_module(utils_module)

        # 執行 bazi_interpretation
        spec.loader.exec_module(bazi_interp)

        # 導入需要的函數
        interpret_personality = bazi_interp.interpret_personality
        interpret_career = bazi_interp.interpret_career
        interpret_wealth = bazi_interp.interpret_wealth
        interpret_relationship = bazi_interp.interpret_relationship
        interpret_health = bazi_interp.interpret_health

        print("\n✓ 成功導入詮釋模組")

        # 測試 1：性格詮釋
        print("\n" + "-" * 60)
        print("測試 1：性格詮釋")
        print("-" * 60)
        personality = interpret_personality(mock_bazi_data)
        print(f"✓ 性格詮釋完成")
        print(f"  日主本質長度：{len(personality['core_personality']['day_master_essence'])} 字")
        print(f"  優勢特質數：{len(personality['core_personality']['strengths'])}")
        print(f"  預覽：{personality['core_personality']['day_master_essence'][:100]}...")

        # 測試 2：事業詮釋
        print("\n" + "-" * 60)
        print("測試 2：事業詮釋")
        print("-" * 60)
        career = interpret_career(mock_bazi_data)
        print(f"✓ 事業詮釋完成")
        print(f"  事業評分：{career['overall_rating']}/10")
        print(f"  天賦才能數：{len(career['aptitude_assessment']['natural_talents'])}")
        print(f"  推薦行業數：{len(career['industry_recommendations']['highly_suitable'])}")

        # 測試 3：財富詮釋
        print("\n" + "-" * 60)
        print("測試 3：財富詮釋")
        print("-" * 60)
        wealth = interpret_wealth(mock_bazi_data)
        print(f"✓ 財富詮釋完成")
        print(f"  財富評分：{wealth['overall_rating']}/10")
        print(f"  建議數量：{len(wealth['specific_recommendations'])}")

        # 測試 4：感情詮釋
        print("\n" + "-" * 60)
        print("測試 4：感情詮釋")
        print("-" * 60)
        relationship = interpret_relationship(mock_bazi_data, gender="女")
        print(f"✓ 感情詮釋完成")
        print(f"  感情評分：{relationship['overall_rating']}/10")
        print(f"  挑戰數量：{len(relationship['relationship_challenges'])}")

        # 測試 5：健康詮釋
        print("\n" + "-" * 60)
        print("測試 5：健康詮釋")
        print("-" * 60)
        health = interpret_health(mock_bazi_data)
        print(f"✓ 健康詮釋完成")
        print(f"  健康評分：{health['overall_rating']:.1f}/10")
        print(f"  五行分析：{len(health['elemental_health_mapping'])} 個元素")

        # 顯示詳細示例
        print("\n" + "=" * 60)
        print("詳細示例輸出")
        print("=" * 60)

        print("\n【性格分析 - 日主本質】")
        print(personality['core_personality']['day_master_essence'])

        print("\n【事業分析 - 總結】")
        print(career['summary'])

        print("\n【健康分析 - 五行健康對應】")
        for wx, info in health['elemental_health_mapping'].items():
            print(f"  {wx} ({info['status']}): {info['implications']}")

        # 保存結果
        result = {
            "personality": personality,
            "career": career,
            "wealth": wealth,
            "relationship": relationship,
            "health": health
        }

        output_file = "test_interpretation_result.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print("\n" + "=" * 60)
        print("✅ 所有測試通過！")
        print(f"✓ 結果已保存至：{output_file}")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"\n❌ 測試失敗：{str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_interpretation_functions()
    sys.exit(0 if success else 1)

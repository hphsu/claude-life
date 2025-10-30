#!/usr/bin/env python3
"""
Convert fortune-telling markdown analyses to HTML and generate final report
"""

import json
import markdown
from datetime import datetime
from pathlib import Path

def read_file(filepath):
    """Read file content"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def convert_markdown_to_html(md_content):
    """Convert markdown to HTML with extensions"""
    return markdown.markdown(md_content, extensions=['extra', 'nl2br', 'tables'])

def main():
    # File paths
    base_dir = Path("/Users/frank/src/life")
    data_dir = base_dir / "data/fortune-telling"
    template_path = base_dir / "scripts/fortune_telling/templates/agent_report_template_dark.html"

    # Input files
    json_path = data_dir / "fortune_tell_Frank_20251029_105037.json"
    bazi_md_path = data_dir / "八字命理分析報告_Frank_20251029.md"
    ziwei_md_path = data_dir / "紫微斗數分析報告_Frank_20251029.md"
    astrology_md_path = data_dir / "心理占星分析報告_Frank_20251029.md"
    synthesis_md_path = data_dir / "綜合分析報告_Frank_20251029.md"

    print("📖 Reading analysis files...")

    # Read JSON for metadata
    with open(json_path, 'r', encoding='utf-8') as f:
        fortune_data = json.load(f)

    # Read template
    template_html = read_file(template_path)

    # Read all markdown files
    bazi_md = read_file(bazi_md_path)
    ziwei_md = read_file(ziwei_md_path)
    astrology_md = read_file(astrology_md_path)
    synthesis_md = read_file(synthesis_md_path)

    print("🔄 Converting markdown to HTML...")

    # Convert markdown to HTML
    bazi_html = convert_markdown_to_html(bazi_md)
    ziwei_html = convert_markdown_to_html(ziwei_md)
    astrology_html = convert_markdown_to_html(astrology_md)
    synthesis_html = convert_markdown_to_html(synthesis_md)

    # Extract metadata from JSON
    basic_info = fortune_data['basic_info']
    name = basic_info['name']
    birth_date = basic_info['birth_gregorian'].split()[0]
    birth_time = basic_info['birth_gregorian'].split()[1] if len(basic_info['birth_gregorian'].split()) > 1 else '06:00'
    location = basic_info.get('location', '苗栗')
    gender = basic_info.get('gender', '男')
    timestamp = datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')

    print("✏️ Replacing template placeholders...")

    # Replace placeholders in template
    final_html = template_html
    final_html = final_html.replace('{{NAME}}', name)
    final_html = final_html.replace('{{BIRTH_DATE}}', birth_date)
    final_html = final_html.replace('{{BIRTH_TIME}}', birth_time)
    final_html = final_html.replace('{{LOCATION}}', location)
    final_html = final_html.replace('{{GENDER}}', gender)
    final_html = final_html.replace('{{TIMESTAMP}}', timestamp)
    final_html = final_html.replace('{{BAZI_CONTENT}}', bazi_html)
    final_html = final_html.replace('{{ZIWEI_CONTENT}}', ziwei_html)
    final_html = final_html.replace('{{ASTROLOGY_CONTENT}}', astrology_html)
    final_html = final_html.replace('{{SYNTHESIS_CONTENT}}', synthesis_html)

    # Save final HTML
    output_path = data_dir / "fortune_tell_Frank_20251029_105037.html"

    print(f"💾 Saving HTML report...")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print(f"\n✅ HTML報告生成成功！")
    print(f"📄 輸出文件: {output_path}")
    print(f"📏 文件大小: {len(final_html):,} 字符")
    print(f"\n📊 報告包含：")
    print(f"   🧩 綜合分析（{len(synthesis_html):,} 字符）")
    print(f"   📿 八字命理（{len(bazi_html):,} 字符）")
    print(f"   ⭐ 紫微斗數（{len(ziwei_html):,} 字符）")
    print(f"   🌟 心理占星（{len(astrology_html):,} 字符）")

    return str(output_path)

if __name__ == "__main__":
    main()

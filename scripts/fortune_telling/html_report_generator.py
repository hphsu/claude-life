"""
HTML 報告生成器 (Comprehensive 8-Method Analysis)
================

為綜合命理分析生成美觀的HTML報告，整合八大命理體系：
- 八字命理 (Bazi)
- 紫微斗數 (Ziwei)
- 西洋占星 (Astrology)
- 梅花易數 (Plum Blossom)
- 奇門遁甲 (Qimen Dunjia)
- 六爻占卜 (Liuyao)
- 生命靈數 (Numerology)
- 姓名學 (Name Analysis)

功能特色：
- 信心度指標與色彩編碼
- 三方法對比可視化
- 時間軸可視化
- LLM深度分析展示
- 完整八方法詳細報告
"""

from typing import Dict, List, Optional
from datetime import datetime


def _render_confidence_badge(confidence_data: Dict) -> str:
    """
    渲染信心度徽章（帶顏色編碼）

    Args:
        confidence_data: 信心度數據 {'level': '極高', 'percentage': 96.0, 'emoji': '🟢'}

    Returns:
        HTML徽章代碼
    """
    if not confidence_data or not isinstance(confidence_data, dict):
        return '<span class="confidence-badge confidence-unknown">信心度：不明</span>'

    level = confidence_data.get('level', '不明')
    percentage = confidence_data.get('percentage', 0)
    emoji = confidence_data.get('emoji', '')

    # 根據信心度級別設置CSS class
    level_class_map = {
        '極高': 'confidence-very-high',
        '高': 'confidence-high',
        '中等': 'confidence-medium',
        '較低': 'confidence-low',
        '不確定': 'confidence-uncertain'
    }
    css_class = level_class_map.get(level, 'confidence-unknown')

    return f'''
        <span class="confidence-badge {css_class}">
            {emoji} {level} ({percentage}%)
        </span>
    '''


def _render_method_comparison(synthesis_data: Dict, domain_name: str) -> str:
    """
    渲染三方法對比可視化

    Args:
        synthesis_data: 綜合分析數據
        domain_name: 領域名稱 (personality_synthesis, career_synthesis等)

    Returns:
        HTML對比表格代碼
    """
    domain_data = synthesis_data.get(domain_name, {})
    if not domain_data:
        return ''

    convergent_traits = domain_data.get('convergent_traits', [])
    bazi_perspective = domain_data.get('bazi_perspective', [])
    ziwei_perspective = domain_data.get('ziwei_perspective', [])
    astro_perspective = domain_data.get('astro_perspective', [])

    html = '''
        <div class="method-comparison">
            <h4 class="comparison-title">🔍 三方法對比分析</h4>

            <!-- 三方一致特質 -->
    '''

    if convergent_traits:
        html += f'''
            <div class="convergent-section">
                <div class="convergent-header">
                    <span class="convergent-icon">🎯</span>
                    <span class="convergent-title">三方一致特質（信心度極高）</span>
                </div>
                <div class="trait-tags">
                    {''.join(f'<span class="trait-tag convergent">{trait}</span>' for trait in convergent_traits)}
                </div>
            </div>
        '''

    # 各方法獨特視角
    html += '''
            <div class="perspectives-grid">
    '''

    perspectives = [
        ('八字命理', 'bazi', bazi_perspective, '📚'),
        ('紫微斗數', 'ziwei', ziwei_perspective, '🌟'),
        ('西洋占星', 'astro', astro_perspective, '⭐')
    ]

    for method_name, method_key, traits, icon in perspectives:
        if traits:
            # Pre-process traits to avoid f-string slicing issues
            limited_traits = traits[:5] if isinstance(traits, list) else list(traits)[:5]
            trait_tags = ''.join(f'<span class="trait-tag {method_key}">{trait}</span>' for trait in limited_traits)

            html += f'''
                <div class="perspective-card perspective-{method_key}">
                    <div class="perspective-header">
                        <span class="perspective-icon">{icon}</span>
                        <span class="perspective-name">{method_name}</span>
                    </div>
                    <div class="trait-tags">
                        {trait_tags}
                    </div>
                </div>
            '''

    html += '''
            </div>
        </div>
    '''

    return html


def _render_timeline_visualization(bazi_data: Dict) -> str:
    """
    渲染時間軸可視化（大運）

    Args:
        bazi_data: 八字計算數據

    Returns:
        HTML時間軸代碼
    """
    luck_pillars = bazi_data.get('calculation', {}).get('luck_pillars', [])
    if not luck_pillars:
        return ''

    html = '''
        <div class="timeline-section">
            <h4 class="timeline-title">📅 人生大運時間軸</h4>
            <div class="timeline-container">
    '''

    for pillar in luck_pillars[:10]:  # 顯示前10個大運
        start_age = pillar.get('start_age', 0)
        end_age = pillar.get('end_age', 0)
        heavenly_stem = pillar.get('heavenly_stem', '')
        earthly_branch = pillar.get('earthly_branch', '')
        pillar_str = f"{heavenly_stem}{earthly_branch}"

        # 根據五行分配顏色
        element_colors = {
            '木': '#4CAF50',
            '火': '#FF5722',
            '土': '#FFC107',
            '金': '#9E9E9E',
            '水': '#2196F3'
        }
        element = pillar.get('element', '土')
        color = element_colors.get(element, '#9E9E9E')

        html += f'''
                <div class="timeline-item" style="border-left-color: {color};">
                    <div class="timeline-marker" style="background-color: {color};"></div>
                    <div class="timeline-content">
                        <div class="timeline-pillar">{pillar_str}</div>
                        <div class="timeline-age">{start_age}-{end_age}歲</div>
                        <div class="timeline-element" style="color: {color};">{element}運</div>
                    </div>
                </div>
        '''

    html += '''
            </div>
        </div>
    '''

    return html


def _render_llm_analysis(analysis_data: Dict, section_title: str) -> str:
    """
    渲染LLM深度分析內容

    Args:
        analysis_data: 分析數據
        section_title: 區塊標題

    Returns:
        HTML LLM分析代碼
    """
    llm_analysis = analysis_data.get('llm_analysis', '')
    analysis_method = analysis_data.get('analysis_method', '')

    if not llm_analysis or 'LLM' not in analysis_method:
        return ''

    html = f'''
        <div class="llm-analysis-section">
            <div class="llm-badge">
                <span class="llm-icon">🤖</span>
                <span class="llm-label">AI深度分析</span>
            </div>
            <div class="llm-content">
                {llm_analysis.replace(chr(10), '<br>')}
            </div>
        </div>
    '''

    return html


def generate_html_report(data: Dict, output_path: str) -> str:
    """
    生成HTML格式的綜合命理分析報告（Phase 4 Enhanced）

    Args:
        data: 完整的分析數據
        output_path: 輸出文件路徑

    Returns:
        HTML報告文件路徑
    """

    # 提取基本信息
    basic_info = data.get('basic_info', {})
    calendar_data = data.get('calendar_data', {})
    four_pillars = calendar_data.get('four_pillars', {})

    # 提取分析結果
    bazi = data.get('bazi', {})
    ziwei = data.get('ziwei', {})
    astrology = data.get('astrology', {})
    synthesis = data.get('synthesis', {})

    # 生成HTML
    html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{basic_info.get('name', 'Unknown')} 命理綜合分析報告</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: "PingFang TC", "Microsoft JhengHei", "Heiti TC", sans-serif;
            line-height: 1.8;
            color: #e0e0e0;
            background: #000000;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: #1a1a1a;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}

        .birth-info {{
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            backdrop-filter: blur(10px);
        }}

        .birth-info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}

        .info-item {{
            text-align: center;
        }}

        .info-label {{
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 5px;
        }}

        .info-value {{
            font-size: 1.3em;
            font-weight: bold;
        }}

        .four-pillars {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}

        .pillar {{
            background: rgba(255,255,255,0.15);
            padding: 15px 25px;
            border-radius: 10px;
            text-align: center;
            min-width: 100px;
        }}

        .pillar-label {{
            font-size: 0.9em;
            margin-bottom: 8px;
            opacity: 0.9;
        }}

        .pillar-value {{
            font-size: 1.8em;
            font-weight: bold;
            letter-spacing: 3px;
        }}

        .content {{
            padding: 40px;
            background: #1a1a1a;
        }}

        .section {{
            margin-bottom: 50px;
        }}

        .section-title {{
            font-size: 2em;
            color: #8b9cff;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #8b9cff;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .subsection {{
            margin: 30px 0;
            padding: 25px;
            background: #2a2a2a;
            border-radius: 15px;
            border-left: 5px solid #8b9cff;
        }}

        .subsection-title {{
            font-size: 1.5em;
            color: #a5b4fc;
            margin-bottom: 15px;
        }}

        /* Phase 4: Enhanced Confidence Badges */
        .confidence-badge {{
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
            margin: 5px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        .confidence-very-high {{
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
        }}

        .confidence-high {{
            background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
            color: white;
        }}

        .confidence-medium {{
            background: linear-gradient(135deg, #FFC107 0%, #FFA000 100%);
            color: white;
        }}

        .confidence-low {{
            background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%);
            color: white;
        }}

        .confidence-uncertain {{
            background: linear-gradient(135deg, #9E9E9E 0%, #757575 100%);
            color: white;
        }}

        /* Phase 4: Method Comparison */
        .method-comparison {{
            background: #2a2a2a;
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }}

        .comparison-title {{
            font-size: 1.3em;
            color: #8b9cff;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .convergent-section {{
            background: linear-gradient(135deg, #1a4d2e 0%, #2d5f3f 100%);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 5px solid #4CAF50;
        }}

        .convergent-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 15px;
            font-weight: bold;
            color: #a5d6a7;
        }}

        .convergent-icon {{
            font-size: 1.5em;
        }}

        .convergent-title {{
            font-size: 1.1em;
        }}

        .trait-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}

        .trait-tag {{
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.95em;
            font-weight: 500;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}

        .trait-tag.convergent {{
            background: #1a1a1a;
            color: #a5d6a7;
            border: 2px solid #4CAF50;
        }}

        .perspectives-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}

        .perspective-card {{
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid;
        }}

        .perspective-card.perspective-bazi {{
            background: #2a1f00;
            border-left-color: #FF9800;
        }}

        .perspective-card.perspective-ziwei {{
            background: #1a1a2e;
            border-left-color: #673AB7;
        }}

        .perspective-card.perspective-astro {{
            background: #001f2a;
            border-left-color: #03A9F4;
        }}

        .perspective-header {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 10px;
            font-weight: bold;
        }}

        .perspective-icon {{
            font-size: 1.2em;
        }}

        .trait-tag.bazi {{
            background: #1a1a1a;
            color: #ffb74d;
            border: 2px solid #FF9800;
        }}

        .trait-tag.ziwei {{
            background: #1a1a1a;
            color: #9575cd;
            border: 2px solid #673AB7;
        }}

        .trait-tag.astro {{
            background: #1a1a1a;
            color: #4fc3f7;
            border: 2px solid #03A9F4;
        }}

        /* Phase 4: Timeline Visualization */
        .timeline-section {{
            background: #2a2a2a;
            padding: 25px;
            border-radius: 15px;
            margin: 20px 0;
        }}

        .timeline-title {{
            font-size: 1.3em;
            color: #8b9cff;
            margin-bottom: 20px;
        }}

        .timeline-container {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 15px;
        }}

        .timeline-item {{
            background: #1f1f1f;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            position: relative;
        }}

        .timeline-marker {{
            position: absolute;
            left: -8px;
            top: 20px;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            border: 3px solid #000;
        }}

        .timeline-content {{
            text-align: center;
        }}

        .timeline-pillar {{
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 5px;
            letter-spacing: 2px;
        }}

        .timeline-age {{
            font-size: 0.9em;
            color: #b0b0b0;
            margin-bottom: 5px;
        }}

        .timeline-element {{
            font-size: 0.85em;
            font-weight: bold;
        }}

        /* Phase 4: LLM Analysis */
        .llm-analysis-section {{
            background: linear-gradient(135deg, #1a2a3a 0%, #2d3d4d 100%);
            padding: 25px;
            border-radius: 15px;
            margin: 20px 0;
            border-left: 5px solid #2196F3;
        }}

        .llm-badge {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: #1a1a1a;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            color: #64b5f6;
            margin-bottom: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }}

        .llm-icon {{
            font-size: 1.2em;
        }}

        .llm-content {{
            background: #2a2a2a;
            padding: 20px;
            border-radius: 10px;
            line-height: 2;
            color: #e0e0e0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }}

        .score-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            margin: 20px 0;
        }}

        .score-value {{
            font-size: 3em;
            font-weight: bold;
            margin: 10px 0;
        }}

        .score-label {{
            font-size: 1.2em;
            opacity: 0.9;
        }}

        .domain-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}

        .domain-card {{
            background: #2a2a2a;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        .domain-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.4);
        }}

        .domain-icon {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .domain-name {{
            font-size: 1.3em;
            font-weight: bold;
            color: #8b9cff;
            margin-bottom: 15px;
        }}

        .domain-rating {{
            font-size: 2em;
            font-weight: bold;
            color: #a5b4fc;
            margin: 10px 0;
        }}

        .narrative-box {{
            background: #2a2a2a;
            border: 2px solid #3a3a3a;
            border-radius: 10px;
            padding: 25px;
            margin: 20px 0;
            line-height: 2;
            color: #e0e0e0;
        }}

        .insight-list {{
            list-style: none;
            padding: 0;
        }}

        .insight-list li {{
            padding: 15px;
            margin: 10px 0;
            background: #2a2a2a;
            border-radius: 10px;
            border-left: 4px solid #8b9cff;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            color: #e0e0e0;
        }}

        .insight-list li strong {{
            color: #8b9cff;
        }}

        .footer {{
            background: #0a0a0a;
            padding: 30px;
            text-align: center;
            color: #b0b0b0;
            border-top: 1px solid #333;
        }}

        .timestamp {{
            font-size: 0.9em;
            color: #808080;
            margin-top: 10px;
        }}

        @media print {{
            body {{
                background: #000000;
                padding: 0;
            }}
            .container {{
                box-shadow: none;
                border-radius: 0;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🔮 綜合命理分析報告</h1>
            <div class="birth-info">
                <div class="birth-info-grid">
                    <div class="info-item">
                        <div class="info-label">姓名</div>
                        <div class="info-value">{basic_info.get('name', 'N/A')}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">出生日期</div>
                        <div class="info-value">{basic_info.get('birth_gregorian', 'N/A')}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">農曆</div>
                        <div class="info-value">{basic_info.get('birth_lunar', 'N/A')}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">出生地</div>
                        <div class="info-value">{basic_info.get('location', 'N/A')}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">性別</div>
                        <div class="info-value">{basic_info.get('gender', 'N/A')}</div>
                    </div>
                </div>

                <!-- Four Pillars -->
                <div class="four-pillars">
                    <div class="pillar">
                        <div class="pillar-label">年柱</div>
                        <div class="pillar-value">{four_pillars.get('year', {}).get('pillar', 'N/A')}</div>
                    </div>
                    <div class="pillar">
                        <div class="pillar-label">月柱</div>
                        <div class="pillar-value">{four_pillars.get('month', {}).get('pillar', 'N/A')}</div>
                    </div>
                    <div class="pillar">
                        <div class="pillar-label">日柱</div>
                        <div class="pillar-value">{four_pillars.get('day', {}).get('pillar', 'N/A')}</div>
                    </div>
                    <div class="pillar">
                        <div class="pillar-label">時柱</div>
                        <div class="pillar-value">{four_pillars.get('hour', {}).get('pillar', 'N/A')}</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Content -->
        <div class="content">
"""

    # ========================================
    # 綜合分析（Comprehensive Synthesis）
    # ========================================
    if synthesis:
        html += """
            <!-- Comprehensive Synthesis Section -->
            <div class="section">
                <h2 class="section-title">🎯 綜合分析總覽</h2>
                <p style="font-size: 1.1em; color: #666; margin-bottom: 30px;">
                    整合<strong>八字命理</strong>、<strong>紫微斗數</strong>、<strong>西洋占星</strong>、<strong>梅花易數</strong>、<strong>奇門遁甲</strong>、<strong>六爻占卜</strong>、<strong>生命靈數</strong>、<strong>姓名學</strong>八大命理體系的綜合分析
                </p>
"""

        # 生命領域卡片
        domains = {
            'personality_synthesis': ('💫', '核心人格'),
            'career_synthesis': ('💼', '事業發展'),
            'wealth_synthesis': ('💰', '財富運勢'),
            'relationship_synthesis': ('💖', '感情關係'),
            'health_synthesis': ('🏥', '健康狀況')
        }

        html += '<div class="domain-grid">'

        for domain_key, (icon, name) in domains.items():
            domain_data = synthesis.get(domain_key, {})
            if domain_data:
                rating = domain_data.get('overall_rating', 'N/A')
                confidence_data = domain_data.get('confidence_level', {})

                confidence_badge = _render_confidence_badge(confidence_data)

                html += f"""
                <div class="domain-card">
                    <div class="domain-icon">{icon}</div>
                    <div class="domain-name">{name}</div>
                    <div class="domain-rating">{rating}/10</div>
                    {confidence_badge}
                </div>
"""

        html += '</div>'

        # 性格綜合分析 - 詳細展開（含三方法對比）
        personality = synthesis.get('personality_synthesis', {})
        if personality:
            confidence_data = personality.get('confidence_level', {})
            narrative = personality.get('synthesis_narrative', '')

            html += f"""
                <div class="subsection">
                    <h3 class="subsection-title">💫 核心人格詳細分析</h3>
                    <div class="score-card">
                        <div class="score-label">綜合評分</div>
                        <div class="score-value">{personality.get('overall_rating', 'N/A')}/10</div>
                        {_render_confidence_badge(confidence_data)}
                    </div>

                    <!-- Phase 4: Three-Method Comparison -->
                    {_render_method_comparison(synthesis, 'personality_synthesis')}

                    <div class="narrative-box">
                        <h4 style="color: #667eea; margin-bottom: 15px;">📝 綜合敘事</h4>
                        {narrative.replace(chr(10), '<br>')}
                    </div>

                    <!-- Phase 4: LLM Analysis (if available) -->
                    {_render_llm_analysis(personality, '核心人格')}
                </div>
"""

        # 事業發展詳細分析
        career = synthesis.get('career_synthesis', {})
        if career:
            confidence_data = career.get('confidence_level', {})
            narrative = career.get('synthesis_narrative', '')

            html += f"""
                <div class="subsection">
                    <h3 class="subsection-title">💼 事業發展詳細分析</h3>
                    <div class="score-card">
                        <div class="score-label">綜合評分</div>
                        <div class="score-value">{career.get('overall_rating', 'N/A')}/10</div>
                        {_render_confidence_badge(confidence_data)}
                    </div>

                    {_render_method_comparison(synthesis, 'career_synthesis')}

                    <div class="narrative-box">
                        <h4 style="color: #667eea; margin-bottom: 15px;">📝 綜合敘事</h4>
                        {narrative.replace(chr(10), '<br>')}
                    </div>

                    {_render_llm_analysis(career, '事業發展')}
                </div>
"""

        html += """
            </div>
"""

    # ========================================
    # 八字分析部分（Phase 4 Enhanced）
    # ========================================
    bazi_interp = bazi.get('interpretation', {})
    if bazi_interp:
        html += """
            <div class="section">
                <h2 class="section-title">📚 八字命理分析</h2>
"""

        # 性格分析
        personality = bazi_interp.get('personality', {})
        if personality:
            confidence_data = personality.get('confidence_level', {})
            analysis_method = personality.get('analysis_method', '')

            day_master_essence = personality.get('day_master_essence', {})
            if isinstance(day_master_essence, dict):
                core_essence = day_master_essence.get('core_essence', '')
            else:
                core_essence = str(day_master_essence)

            html += f"""
                <div class="subsection">
                    <h3 class="subsection-title">性格特質</h3>
                    {_render_confidence_badge(confidence_data)}
                    <span style="margin-left: 10px; font-size: 0.9em; color: #666;">分析方法: {analysis_method}</span>

                    <div class="narrative-box">
                        {core_essence[:1000].replace(chr(10), '<br>')}
                    </div>

                    {_render_llm_analysis(personality, '八字性格')}
                </div>
"""

        # 事業分析
        career = bazi_interp.get('career', {})
        if career:
            confidence_data = career.get('confidence_level', {})

            html += f"""
                <div class="subsection">
                    <h3 class="subsection-title">事業發展</h3>
                    {_render_confidence_badge(confidence_data)}

                    {_render_llm_analysis(career, '八字事業')}
                </div>
"""

        # Phase 4: Timeline Visualization (大運)
        timeline_html = _render_timeline_visualization(bazi)
        if timeline_html:
            html += timeline_html

        html += """
            </div>
"""

    # ========================================
    # 紫微斗數分析（Phase 4 Enhanced）
    # ========================================
    ziwei_interp = ziwei.get('interpretation', {})
    if ziwei_interp:
        palace_interp = ziwei_interp.get('palace_interpretations', {})
        destiny_palace = palace_interp.get('命宮', {})

        if destiny_palace:
            confidence_data = destiny_palace.get('confidence_level', {})

            html += f"""
            <div class="section">
                <h2 class="section-title">🌟 紫微斗數分析</h2>
                <div class="subsection">
                    <h3 class="subsection-title">命宮</h3>
                    {_render_confidence_badge(confidence_data)}

                    <ul class="insight-list">
                        <li><strong>位置</strong>：{destiny_palace.get('position', 'N/A')}</li>
                        <li><strong>主星</strong>：{', '.join(destiny_palace.get('major_stars', []))}</li>
                    </ul>

                    {_render_llm_analysis(destiny_palace, '紫微命宮')}
                </div>
            </div>
"""

    # ========================================
    # 西洋占星分析（Phase 4 Enhanced）
    # ========================================
    astro_interp = astrology.get('interpretation', {})
    if astro_interp:
        psych_profile = astro_interp.get('psychological_profile', {})
        if psych_profile:
            core_self = psych_profile.get('core_self', {})
            confidence_data = astro_interp.get('confidence_level', {})

            html += f"""
            <div class="section">
                <h2 class="section-title">⭐ 西洋占星分析</h2>
                <div class="subsection">
                    <h3 class="subsection-title">核心星座配置</h3>
                    {_render_confidence_badge(confidence_data)}

                    <ul class="insight-list">
                        <li><strong>太陽星座</strong>：{core_self.get('sun_sign', 'N/A')}</li>
                        <li><strong>月亮星座</strong>：{core_self.get('moon_sign', 'N/A')}</li>
                        <li><strong>上升星座</strong>：{core_self.get('ascendant_sign', 'N/A')}</li>
                    </ul>

                    {_render_llm_analysis(astro_interp, '西洋占星')}
                </div>
            </div>
"""

    # ========================================
    # 梅花易數分析（Plum Blossom）
    # ========================================
    plum = data.get('plum_blossom', {})
    plum_interp = plum.get('interpretation', {})
    if plum_interp:
        confidence_data = plum_interp.get('confidence_level', {})

        html += f"""
            <div class="section">
                <h2 class="section-title">🌸 梅花易數分析</h2>
"""

        # 卦象分析
        hexagram_analysis = plum_interp.get('hexagram_analysis', {})
        if hexagram_analysis:
            html += f"""
                <div class="subsection">
                    <h3 class="subsection-title">卦象解析</h3>
                    {_render_confidence_badge(confidence_data)}

                    <div class="narrative-box">
                        {str(hexagram_analysis).replace(chr(10), '<br>')}
                    </div>
                </div>
"""

        # 時間卦分析
        time_hexagram = plum_interp.get('time_hexagram', {})
        if time_hexagram:
            html += f"""
                <div class="subsection">
                    <h3 class="subsection-title">時間卦分析</h3>
                    <div class="narrative-box">
                        {str(time_hexagram).replace(chr(10), '<br>')}
                    </div>
                </div>
"""

        # 整體解讀
        overall = plum_interp.get('overall_interpretation', '')
        if overall:
            html += f"""
                <div class="subsection">
                    <h3 class="subsection-title">整體解讀</h3>
                    <div class="narrative-box">
                        {overall.replace(chr(10), '<br>')}
                    </div>

                    {_render_llm_analysis(plum_interp, '梅花易數')}
                </div>
"""

        html += """
            </div>
"""

    # ========================================
    # 奇門遁甲分析（Qimen Dunjia）
    # ========================================
    qimen = data.get('qimen', {})
    qimen_interp = qimen.get('interpretation', {})
    if qimen_interp:
        confidence_data = qimen_interp.get('confidence_level', {})

        html += f"""
            <div class="section">
                <h2 class="section-title">🗺️ 奇門遁甲分析</h2>
"""

        # 局盤分析
        bureau_analysis = qimen_interp.get('bureau_analysis', {})
        if bureau_analysis:
            html += f"""
                <div class="subsection">
                    <h3 class="subsection-title">奇門局盤</h3>
                    {_render_confidence_badge(confidence_data)}

                    <div class="narrative-box">
                        {str(bureau_analysis).replace(chr(10), '<br>')}
                    </div>
                </div>
"""

        # 用神分析
        deity_analysis = qimen_interp.get('deity_analysis', {})
        if deity_analysis:
            html += f"""
                <div class="subsection">
                    <h3 class="subsection-title">用神分析</h3>
                    <div class="narrative-box">
                        {str(deity_analysis).replace(chr(10), '<br>')}
                    </div>
                </div>
"""

        # 吉凶預測
        prediction = qimen_interp.get('prediction', '')
        if prediction:
            html += f"""
                <div class="subsection">
                    <h3 class="subsection-title">吉凶預測</h3>
                    <div class="narrative-box">
                        {prediction.replace(chr(10), '<br>')}
                    </div>

                    {_render_llm_analysis(qimen_interp, '奇門遁甲')}
                </div>
"""

        html += """
            </div>
"""

    # ========================================
    # 六爻分析（Liuyao）
    # ========================================
    liuyao = data.get('liuyao', {})
    liuyao_interp = liuyao.get('interpretation', {})
    if liuyao_interp:
        confidence_data = liuyao_interp.get('confidence_level', {})

        html += f"""
            <div class="section">
                <h2 class="section-title">☯️ 六爻占卜分析</h2>
"""

        # 本卦分析
        primary_hexagram = liuyao_interp.get('primary_hexagram', {})
        if primary_hexagram:
            html += f"""
                <div class="subsection">
                    <h3 class="subsection-title">本卦分析</h3>
                    {_render_confidence_badge(confidence_data)}

                    <div class="narrative-box">
                        {str(primary_hexagram).replace(chr(10), '<br>')}
                    </div>
                </div>
"""

        # 變卦分析
        changed_hexagram = liuyao_interp.get('changed_hexagram', {})
        if changed_hexagram:
            html += f"""
                <div class="subsection">
                    <h3 class="subsection-title">變卦分析</h3>
                    <div class="narrative-box">
                        {str(changed_hexagram).replace(chr(10), '<br>')}
                    </div>
                </div>
"""

        # 世應分析
        world_response = liuyao_interp.get('world_response_analysis', {})
        if world_response:
            html += f"""
                <div class="subsection">
                    <h3 class="subsection-title">世應分析</h3>
                    <div class="narrative-box">
                        {str(world_response).replace(chr(10), '<br>')}
                    </div>
                </div>
"""

        # 綜合判斷
        overall = liuyao_interp.get('overall_judgment', '')
        if overall:
            html += f"""
                <div class="subsection">
                    <h3 class="subsection-title">綜合判斷</h3>
                    <div class="narrative-box">
                        {overall.replace(chr(10), '<br>')}
                    </div>

                    {_render_llm_analysis(liuyao_interp, '六爻占卜')}
                </div>
"""

        html += """
            </div>
"""

    # ========================================
    # 生命靈數分析（Numerology）
    # ========================================
    numerology = data.get('numerology', {})
    num_interp = numerology.get('interpretation', {})
    if num_interp:
        confidence_data = num_interp.get('confidence_level', {})

        html += f"""
            <div class="section">
                <h2 class="section-title">🔢 生命靈數分析</h2>
"""

        # 生命靈數
        life_path = num_interp.get('life_path_number', {})
        if life_path:
            html += f"""
                <div class="subsection">
                    <h3 class="subsection-title">生命靈數</h3>
                    {_render_confidence_badge(confidence_data)}

                    <div class="narrative-box">
                        {str(life_path).replace(chr(10), '<br>')}
                    </div>
                </div>
"""

        # 天賦數
        destiny_number = num_interp.get('destiny_number', {})
        if destiny_number:
            html += f"""
                <div class="subsection">
                    <h3 class="subsection-title">天賦數</h3>
                    <div class="narrative-box">
                        {str(destiny_number).replace(chr(10), '<br>')}
                    </div>
                </div>
"""

        # 靈魂數
        soul_number = num_interp.get('soul_number', {})
        if soul_number:
            html += f"""
                <div class="subsection">
                    <h3 class="subsection-title">靈魂數</h3>
                    <div class="narrative-box">
                        {str(soul_number).replace(chr(10), '<br>')}
                    </div>
                </div>
"""

        # 綜合解析
        overall = num_interp.get('overall_analysis', '')
        if overall:
            html += f"""
                <div class="subsection">
                    <h3 class="subsection-title">綜合解析</h3>
                    <div class="narrative-box">
                        {overall.replace(chr(10), '<br>')}
                    </div>

                    {_render_llm_analysis(num_interp, '生命靈數')}
                </div>
"""

        html += """
            </div>
"""

    # ========================================
    # 姓名學分析（Name Analysis）
    # ========================================
    name_analysis = data.get('name_analysis', {})
    name_interp = name_analysis.get('interpretation', {})
    if name_interp:
        confidence_data = name_interp.get('confidence_level', {})

        html += f"""
            <div class="section">
                <h2 class="section-title">📝 姓名學分析</h2>
"""

        # 五格剖象
        five_grids = name_interp.get('five_grids', {})
        if five_grids:
            html += f"""
                <div class="subsection">
                    <h3 class="subsection-title">五格剖象</h3>
                    {_render_confidence_badge(confidence_data)}

                    <div class="narrative-box">
                        {str(five_grids).replace(chr(10), '<br>')}
                    </div>
                </div>
"""

        # 三才配置
        three_talents = name_interp.get('three_talents', {})
        if three_talents:
            html += f"""
                <div class="subsection">
                    <h3 class="subsection-title">三才配置</h3>
                    <div class="narrative-box">
                        {str(three_talents).replace(chr(10), '<br>')}
                    </div>
                </div>
"""

        # 81數理
        eighty_one = name_interp.get('eighty_one_number', {})
        if eighty_one:
            html += f"""
                <div class="subsection">
                    <h3 class="subsection-title">81數理</h3>
                    <div class="narrative-box">
                        {str(eighty_one).replace(chr(10), '<br>')}
                    </div>
                </div>
"""

        # 姓名綜評
        overall = name_interp.get('overall_evaluation', '')
        if overall:
            html += f"""
                <div class="subsection">
                    <h3 class="subsection-title">姓名綜評</h3>
                    <div class="narrative-box">
                        {overall.replace(chr(10), '<br>')}
                    </div>

                    {_render_llm_analysis(name_interp, '姓名學')}
                </div>
"""

        html += """
            </div>
"""

    # Footer
    html += f"""
        </div>

        <!-- Footer -->
        <div class="footer">
            <p><strong>重要提醒</strong></p>
            <p>本報告整合<strong>八字命理</strong>、<strong>紫微斗數</strong>、<strong>西洋占星</strong>、<strong>梅花易數</strong>、<strong>奇門遁甲</strong>、<strong>六爻占卜</strong>、<strong>生命靈數</strong>、<strong>姓名學</strong>八大命理方法的綜合分析。</p>
            <p><strong>命理分析僅供參考，您的人生由自己掌握。</strong></p>
            <p class="timestamp">分析時間：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}</p>
            <p class="timestamp">SuperClaude Fortune-Telling System v2.0 (Comprehensive 8-Method Analysis)</p>
        </div>
    </div>
</body>
</html>
"""

    # 寫入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return output_path


def generate_html_from_markdown_files(analysis_dir: str, output_path: str) -> str:
    """
    從Markdown分析文件生成完整的HTML報告

    Args:
        analysis_dir: 包含calculations.json和分析.md文件的目錄
        output_path: 輸出HTML文件路徑

    Returns:
        生成的HTML文件路徑
    """
    import json
    import os

    # 讀取基本信息
    calc_path = os.path.join(analysis_dir, 'calculations.json')
    with open(calc_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    basic_info = data.get('basic_info', {})
    name = basic_info.get('name', '未知')
    birth_gregorian = basic_info.get('birth_gregorian', '')
    location = basic_info.get('location', '')
    gender = basic_info.get('gender', '')

    # 獲取四柱
    calendar_data = data.get('calendar_data', {})
    four_pillars = calendar_data.get('four_pillars', {})
    year_pillar = four_pillars.get('year_pillar', '')
    month_pillar = four_pillars.get('month_pillar', '')
    day_pillar = four_pillars.get('day_pillar', '')
    hour_pillar = four_pillars.get('hour_pillar', '')

    # 讀取各個分析markdown文件
    def read_md_file(filename):
        filepath = os.path.join(analysis_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        return None

    synthesis = read_md_file('synthesis_report.md')
    bazi = read_md_file('bazi_analysis.md')
    ziwei = read_md_file('ziwei_analysis.md')
    astrology = read_md_file('astrology_analysis.md')
    plum = read_md_file('plum_analysis.md')
    qimen = read_md_file('qimen_analysis.md')
    liuyao = read_md_file('liuyao_analysis.md')
    numerology = read_md_file('numerology_analysis.md')
    name_analysis = read_md_file('name_analysis.md')

    # 轉換markdown到HTML的簡單函數（保留換行和格式）
    def md_to_html(md_text):
        if not md_text:
            return ''
        # 簡單處理：轉換標題、粗體、換行
        html = md_text
        # ### 標題
        html = html.replace('### ', '<h4 style="color: #a5b4fc; margin: 20px 0 10px 0; font-size: 1.2em;">')
        html = html.replace('\n##', '</h4>\n##')
        # ## 標題
        html = html.replace('## ', '<h3 style="color: #8b9cff; margin: 25px 0 15px 0; font-size: 1.4em;">')
        html = html.replace('\n#', '</h3>\n#')
        # # 標題
        html = html.replace('# ', '<h2 style="color: #667eea; margin: 30px 0 20px 0; font-size: 1.6em;">')
        # 粗體
        import re
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        # 換行
        html = html.replace('\n\n', '</p><p style="margin: 15px 0; line-height: 1.8; color: #e0e0e0;">')
        html = html.replace('\n', '<br>')
        # 包裝在段落中
        html = f'<p style="margin: 15px 0; line-height: 1.8; color: #e0e0e0;">{html}</p>'
        return html

    # 開始生成HTML
    html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} 命理綜合分析報告</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: "PingFang TC", "Microsoft JhengHei", "Heiti TC", sans-serif;
            line-height: 1.8;
            color: #e0e0e0;
            background: #000000;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: #1a1a1a;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}

        .birth-info {{
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            backdrop-filter: blur(10px);
        }}

        .birth-info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}

        .info-item {{
            text-align: center;
        }}

        .info-label {{
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 5px;
        }}

        .info-value {{
            font-size: 1.3em;
            font-weight: bold;
        }}

        .four-pillars {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}

        .pillar {{
            background: rgba(255,255,255,0.15);
            padding: 15px 25px;
            border-radius: 10px;
            text-align: center;
            min-width: 100px;
        }}

        .pillar-label {{
            font-size: 0.9em;
            margin-bottom: 8px;
            opacity: 0.9;
        }}

        .pillar-value {{
            font-size: 1.8em;
            font-weight: bold;
            letter-spacing: 3px;
        }}

        .content {{
            padding: 40px;
            background: #1a1a1a;
        }}

        .section {{
            margin-bottom: 50px;
            background: #2a2a2a;
            border-radius: 15px;
            padding: 30px;
            border-left: 5px solid #8b9cff;
        }}

        .section-title {{
            font-size: 2em;
            color: #8b9cff;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #8b9cff;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .analysis-content {{
            background: #1f1f1f;
            padding: 25px;
            border-radius: 10px;
            margin-top: 20px;
            line-height: 2;
            color: #e0e0e0;
        }}

        .footer {{
            background: #0a0a0a;
            padding: 30px;
            text-align: center;
            color: #b0b0b0;
            border-top: 1px solid #333;
        }}

        .timestamp {{
            color: #808080;
            font-size: 0.9em;
            margin-top: 10px;
        }}

        .nav-menu {{
            background: rgba(255,255,255,0.15);
            padding: 25px;
            border-radius: 10px;
            margin-top: 25px;
            backdrop-filter: blur(10px);
        }}

        .nav-menu h3 {{
            font-size: 1.3em;
            margin-bottom: 15px;
            text-align: center;
            color: white;
        }}

        .nav-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
        }}

        .nav-link {{
            display: block;
            padding: 12px 15px;
            background: rgba(255,255,255,0.1);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            text-align: center;
            transition: all 0.3s ease;
            font-size: 0.95em;
        }}

        .nav-link:hover {{
            background: rgba(255,255,255,0.25);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}

        html {{
            scroll-behavior: smooth;
        }}
    </style>
</head>
<body>
<div class="container">
    <!-- Header -->
    <div class="header">
        <h1>✨ {name} 命理綜合分析報告</h1>

        <div class="birth-info">
            <div class="birth-info-grid">
                <div class="info-item">
                    <div class="info-label">出生時間</div>
                    <div class="info-value">{birth_gregorian}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">出生地</div>
                    <div class="info-value">{location}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">性別</div>
                    <div class="info-value">{gender}</div>
                </div>
            </div>

            <!-- Four Pillars -->
            <div class="four-pillars">
                <div class="pillar">
                    <div class="pillar-label">年柱</div>
                    <div class="pillar-value">{year_pillar}</div>
                </div>
                <div class="pillar">
                    <div class="pillar-label">月柱</div>
                    <div class="pillar-value">{month_pillar}</div>
                </div>
                <div class="pillar">
                    <div class="pillar-label">日柱</div>
                    <div class="pillar-value">{day_pillar}</div>
                </div>
                <div class="pillar">
                    <div class="pillar-label">時柱</div>
                    <div class="pillar-value">{hour_pillar}</div>
                </div>
            </div>

            <!-- Navigation Menu -->
            <div class="nav-menu">
                <h3>📑 報告導航</h3>
                <div class="nav-grid">
                    <a href="#synthesis" class="nav-link">🎯 綜合分析總覽</a>
                    <a href="#bazi" class="nav-link">📿 八字命理分析</a>
                    <a href="#ziwei" class="nav-link">⭐ 紫微斗數分析</a>
                    <a href="#astrology" class="nav-link">🌟 心理占星分析</a>
                    <a href="#plum" class="nav-link">🌸 梅花易數分析</a>
                    <a href="#qimen" class="nav-link">🗺️ 奇門遁甲分析</a>
                    <a href="#liuyao" class="nav-link">☯️ 六爻占卜分析</a>
                    <a href="#numerology" class="nav-link">🔢 生命靈數分析</a>
                    <a href="#name" class="nav-link">📝 姓名學分析</a>
                </div>
            </div>
        </div>
    </div>

    <!-- Content -->
    <div class="content">
"""

    # 綜合分析
    if synthesis:
        html += f"""
        <div class="section" id="synthesis">
            <h2 class="section-title">🎯 綜合分析總覽</h2>
            <div class="analysis-content">
                {md_to_html(synthesis)}
            </div>
        </div>
"""

    # 八字命理
    if bazi:
        html += f"""
        <div class="section" id="bazi">
            <h2 class="section-title">📿 八字命理分析</h2>
            <div class="analysis-content">
                {md_to_html(bazi)}
            </div>
        </div>
"""

    # 紫微斗數
    if ziwei:
        html += f"""
        <div class="section" id="ziwei">
            <h2 class="section-title">⭐ 紫微斗數分析</h2>
            <div class="analysis-content">
                {md_to_html(ziwei)}
            </div>
        </div>
"""

    # 西洋占星
    if astrology:
        html += f"""
        <div class="section" id="astrology">
            <h2 class="section-title">🌟 心理占星分析</h2>
            <div class="analysis-content">
                {md_to_html(astrology)}
            </div>
        </div>
"""

    # 梅花易數
    if plum:
        html += f"""
        <div class="section" id="plum">
            <h2 class="section-title">🌸 梅花易數分析</h2>
            <div class="analysis-content">
                {md_to_html(plum)}
            </div>
        </div>
"""

    # 奇門遁甲
    if qimen:
        html += f"""
        <div class="section" id="qimen">
            <h2 class="section-title">🗺️ 奇門遁甲分析</h2>
            <div class="analysis-content">
                {md_to_html(qimen)}
            </div>
        </div>
"""

    # 六爻
    if liuyao:
        html += f"""
        <div class="section" id="liuyao">
            <h2 class="section-title">☯️ 六爻占卜分析</h2>
            <div class="analysis-content">
                {md_to_html(liuyao)}
            </div>
        </div>
"""

    # 生命靈數
    if numerology:
        html += f"""
        <div class="section" id="numerology">
            <h2 class="section-title">🔢 生命靈數分析</h2>
            <div class="analysis-content">
                {md_to_html(numerology)}
            </div>
        </div>
"""

    # 姓名學
    if name_analysis:
        html += f"""
        <div class="section" id="name">
            <h2 class="section-title">📝 姓名學分析</h2>
            <div class="analysis-content">
                {md_to_html(name_analysis)}
            </div>
        </div>
"""

    # Footer
    html += f"""
    </div>

    <!-- Footer -->
    <div class="footer">
        <p><strong>重要提醒</strong></p>
        <p>本報告整合<strong>八字命理</strong>、<strong>紫微斗數</strong>、<strong>西洋占星</strong>、<strong>梅花易數</strong>、<strong>奇門遁甲</strong>、<strong>六爻占卜</strong>、<strong>生命靈數</strong>、<strong>姓名學</strong>八大命理方法的綜合分析。</p>
        <p><strong>命理分析僅供參考，您的人生由自己掌握。</strong></p>
        <p class="timestamp">分析時間：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}</p>
        <p class="timestamp">SuperClaude Fortune-Telling System v2.0 (Comprehensive 8-Method Analysis)</p>
    </div>
</div>
</body>
</html>
"""

    # 寫入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return output_path

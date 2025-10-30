"""
HTML 報告生成器 (Enhanced with Phase 4 Features)
================

為綜合命理分析生成美觀的HTML報告
- 信心度指標與色彩編碼
- 三方法對比可視化
- 時間軸可視化
- LLM分析展示
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
            color: #333;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
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
        }}

        .section {{
            margin-bottom: 50px;
        }}

        .section-title {{
            font-size: 2em;
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .subsection {{
            margin: 30px 0;
            padding: 25px;
            background: #f8f9fa;
            border-radius: 15px;
            border-left: 5px solid #667eea;
        }}

        .subsection-title {{
            font-size: 1.5em;
            color: #764ba2;
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
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }}

        .comparison-title {{
            font-size: 1.3em;
            color: #667eea;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .convergent-section {{
            background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
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
            color: #2E7D32;
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
            background: white;
            color: #2E7D32;
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
            background: #fff3e0;
            border-left-color: #FF9800;
        }}

        .perspective-card.perspective-ziwei {{
            background: #e8eaf6;
            border-left-color: #673AB7;
        }}

        .perspective-card.perspective-astro {{
            background: #e1f5fe;
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
            background: white;
            color: #E65100;
            border: 2px solid #FF9800;
        }}

        .trait-tag.ziwei {{
            background: white;
            color: #4527A0;
            border: 2px solid #673AB7;
        }}

        .trait-tag.astro {{
            background: white;
            color: #01579B;
            border: 2px solid #03A9F4;
        }}

        /* Phase 4: Timeline Visualization */
        .timeline-section {{
            background: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
            margin: 20px 0;
        }}

        .timeline-title {{
            font-size: 1.3em;
            color: #667eea;
            margin-bottom: 20px;
        }}

        .timeline-container {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 15px;
        }}

        .timeline-item {{
            background: white;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            position: relative;
        }}

        .timeline-marker {{
            position: absolute;
            left: -8px;
            top: 20px;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            border: 3px solid white;
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
            color: #666;
            margin-bottom: 5px;
        }}

        .timeline-element {{
            font-size: 0.85em;
            font-weight: bold;
        }}

        /* Phase 4: LLM Analysis */
        .llm-analysis-section {{
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            padding: 25px;
            border-radius: 15px;
            margin: 20px 0;
            border-left: 5px solid #2196F3;
        }}

        .llm-badge {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            color: #1976D2;
            margin-bottom: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        .llm-icon {{
            font-size: 1.2em;
        }}

        .llm-content {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            line-height: 2;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
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
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        .domain-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.12);
        }}

        .domain-icon {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .domain-name {{
            font-size: 1.3em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 15px;
        }}

        .domain-rating {{
            font-size: 2em;
            font-weight: bold;
            color: #764ba2;
            margin: 10px 0;
        }}

        .narrative-box {{
            background: #ffffff;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 25px;
            margin: 20px 0;
            line-height: 2;
        }}

        .insight-list {{
            list-style: none;
            padding: 0;
        }}

        .insight-list li {{
            padding: 15px;
            margin: 10px 0;
            background: white;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }}

        .insight-list li strong {{
            color: #667eea;
        }}

        .footer {{
            background: #f8f9fa;
            padding: 30px;
            text-align: center;
            color: #666;
            border-top: 1px solid #e0e0e0;
        }}

        .timestamp {{
            font-size: 0.9em;
            color: #999;
            margin-top: 10px;
        }}

        @media print {{
            body {{
                background: white;
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
    # 三方法綜合分析（Phase 4 Enhanced）
    # ========================================
    if synthesis:
        html += """
            <!-- Comprehensive Synthesis Section -->
            <div class="section">
                <h2 class="section-title">🎯 三方法綜合分析</h2>
                <p style="font-size: 1.1em; color: #666; margin-bottom: 30px;">
                    整合<strong>八字命理</strong>、<strong>紫微斗數</strong>、<strong>西洋占星</strong>三大傳統命理方法的深度分析
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

    # Footer
    html += f"""
        </div>

        <!-- Footer -->
        <div class="footer">
            <p><strong>重要提醒</strong></p>
            <p>本報告整合<strong>八字命理</strong>、<strong>紫微斗數</strong>、<strong>西洋占星</strong>三大傳統命理方法。</p>
            <p><strong>命理分析僅供參考，您的人生由自己掌握。</strong></p>
            <p class="timestamp">分析時間：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}</p>
            <p class="timestamp">SuperClaude Fortune-Telling System v2.0 (Phase 4 Enhanced)</p>
        </div>
    </div>
</body>
</html>
"""

    # 寫入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return output_path

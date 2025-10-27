"""
命理分析系統 (Fortune-Telling System)
=====================================

專業級命理分析計算引擎，整合：
- 八字命理 (BaZi / Four Pillars)
- 紫微斗數 (Zi Wei Dou Shu)
- 占星學 (Astrology)

版本: 1.0.0
作者: SuperClaude Framework
日期: 2025-10-26
"""

__version__ = "1.0.0"
__author__ = "SuperClaude Framework"

# 導出主要計算類別
from .calendar_converter import CalendarConverter
from .bazi_calculator import BaziCalculator
from .ziwei_calculator import ZiweiCalculator
from .astrology_calculator import AstrologyCalculator

__all__ = [
    "CalendarConverter",
    "BaziCalculator",
    "ZiweiCalculator",
    "AstrologyCalculator",
]

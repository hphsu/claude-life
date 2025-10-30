"""
LLM分析引擎
LLM Analyzer for Fortune-Telling Deep Analysis

支持Claude Code、OpenAI GPT-4和Anthropic Claude進行深度命理分析
"""

import os
import json
import logging
import subprocess
import shlex
from typing import Dict, Optional, Callable
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


class LLMProvider(Enum):
    """LLM服務提供商"""
    CLAUDE_CODE = "claude_code"  # Use Claude Code Task agents (no API key needed)
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    NONE = "none"


class LLMAnalyzer:
    """
    LLM輔助分析器

    支持多個LLM提供商，自動fallback到規則引擎
    """

    def __init__(
        self,
        provider: LLMProvider = LLMProvider.OPENAI,
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ):
        """
        初始化LLM分析器

        Args:
            provider: LLM提供商
            api_key: API密鑰（如果為None則從環境變量讀取）
            model: 模型名稱（如果為None則使用默認模型）
        """
        self.provider = provider
        self.api_key = api_key or self._get_api_key_from_env()
        self.model = model or self._get_default_model()
        self.client = None

        # 初始化客戶端
        if self.provider == LLMProvider.CLAUDE_CODE:
            # Claude Code doesn't need API key
            self.client = "claude_code_available"
            logger.info("Claude Code提供商初始化成功")
        elif self.api_key and provider != LLMProvider.NONE:
            self._initialize_client()

    def _get_api_key_from_env(self) -> Optional[str]:
        """從環境變量獲取API密鑰"""
        if self.provider == LLMProvider.CLAUDE_CODE:
            return "claude_code"  # No real API key needed
        elif self.provider == LLMProvider.OPENAI:
            return os.getenv('OPENAI_API_KEY')
        elif self.provider == LLMProvider.ANTHROPIC:
            return os.getenv('ANTHROPIC_API_KEY')
        return None

    def _get_default_model(self) -> str:
        """獲取默認模型"""
        if self.provider == LLMProvider.OPENAI:
            return "gpt-4-turbo-preview"  # or "gpt-4"
        elif self.provider == LLMProvider.ANTHROPIC:
            return "claude-3-opus-20240229"  # or "claude-3-sonnet-20240229"
        return ""

    def _initialize_client(self):
        """初始化LLM客戶端"""
        try:
            if self.provider == LLMProvider.OPENAI:
                import openai
                self.client = openai.OpenAI(api_key=self.api_key)
                logger.info(f"OpenAI客戶端初始化成功，模型: {self.model}")

            elif self.provider == LLMProvider.ANTHROPIC:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.api_key)
                logger.info(f"Anthropic客戶端初始化成功，模型: {self.model}")

        except ImportError as e:
            logger.error(f"LLM庫導入失敗: {e}")
            logger.info("提示: pip install openai anthropic")
            self.client = None
        except Exception as e:
            logger.error(f"LLM客戶端初始化失敗: {e}")
            self.client = None

    def is_available(self) -> bool:
        """檢查LLM是否可用"""
        return self.client is not None and self.api_key is not None

    def analyze_with_prompt(
        self,
        system_prompt: str,
        analysis_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> Optional[str]:
        """
        使用LLM進行分析

        Args:
            system_prompt: 系統提示詞
            analysis_prompt: 分析提示
            temperature: 溫度參數（0-1）
            max_tokens: 最大token數

        Returns:
            分析結果，失敗返回None
        """
        if not self.is_available():
            logger.warning("LLM不可用，跳過AI分析")
            return None

        try:
            if self.provider == LLMProvider.CLAUDE_CODE:
                return self._analyze_with_claude_code(
                    system_prompt,
                    analysis_prompt,
                    max_tokens
                )
            elif self.provider == LLMProvider.OPENAI:
                return self._analyze_with_openai(
                    system_prompt,
                    analysis_prompt,
                    temperature,
                    max_tokens
                )
            elif self.provider == LLMProvider.ANTHROPIC:
                return self._analyze_with_anthropic(
                    system_prompt,
                    analysis_prompt,
                    max_tokens
                )
        except Exception as e:
            logger.error(f"LLM分析失敗: {e}")
            return None

    def _analyze_with_openai(
        self,
        system_prompt: str,
        analysis_prompt: str,
        temperature: float,
        max_tokens: int
    ) -> Optional[str]:
        """使用OpenAI進行分析"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": analysis_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )

        result = response.choices[0].message.content
        logger.info(f"OpenAI分析完成，返回{len(result)}字")
        return result

    def _analyze_with_anthropic(
        self,
        system_prompt: str,
        analysis_prompt: str,
        max_tokens: int
    ) -> Optional[str]:
        """使用Anthropic Claude進行分析"""
        message = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[
                {"role": "user", "content": analysis_prompt}
            ]
        )

        result = message.content[0].text
        logger.info(f"Claude分析完成，返回{len(result)}字")
        return result

    def _analyze_with_claude_code(
        self,
        system_prompt: str,
        analysis_prompt: str,
        max_tokens: int
    ) -> Optional[str]:
        """使用Claude Code進行分析

        注意：此方法需要通過 /sc:implement 等命令手動調用
        因為 Task tool 無法在 Python 執行期間調用（會產生遞迴）
        建議直接使用 OPENAI 或 ANTHROPIC provider
        """
        logger.warning(
            "CLAUDE_CODE provider 無法在運行時自動調用。"
            "請改用 OPENAI 或 ANTHROPIC provider，"
            "或手動使用 /fortune-tell 命令調用分析。"
        )
        return None

    def analyze_with_fallback(
        self,
        system_prompt: str,
        analysis_prompt: str,
        fallback_func: Callable,
        fallback_args: tuple = (),
        min_length: int = 300,
        **llm_kwargs
    ) -> str:
        """
        使用LLM分析，失敗則fallback到傳統方法

        Args:
            system_prompt: 系統提示詞
            analysis_prompt: 分析提示
            fallback_func: fallback函數
            fallback_args: fallback函數參數
            min_length: 最低字數要求
            **llm_kwargs: LLM額外參數

        Returns:
            分析結果（LLM或fallback）
        """
        # 嘗試使用LLM
        if self.is_available():
            try:
                result = self.analyze_with_prompt(
                    system_prompt,
                    analysis_prompt,
                    **llm_kwargs
                )

                if result:
                    # 驗證長度
                    actual_length = len(result.replace(' ', '').replace('\n', ''))
                    if actual_length >= min_length:
                        logger.info(f"✅ LLM分析成功 ({actual_length}字)")
                        return result
                    else:
                        logger.warning(
                            f"⚠️ LLM輸出{actual_length}字，未達{min_length}字標準，使用fallback"
                        )
            except Exception as e:
                logger.error(f"❌ LLM分析異常: {e}，使用fallback")
        else:
            logger.info("ℹ️ LLM不可用，使用傳統分析方法")

        # Fallback到傳統方法
        logger.info("🔄 執行fallback分析...")
        return fallback_func(*fallback_args)


# 全局LLM分析器實例（延遲初始化）
_global_analyzer: Optional[LLMAnalyzer] = None


def get_llm_analyzer(
    force_reload: bool = False,
    provider: Optional[LLMProvider] = None
) -> LLMAnalyzer:
    """
    獲取全局LLM分析器實例

    Args:
        force_reload: 強制重新加載
        provider: 指定提供商（僅在首次初始化或force_reload時有效）

    Returns:
        LLM分析器實例
    """
    global _global_analyzer

    if _global_analyzer is None or force_reload:
        # 自動檢測可用的LLM提供商
        if provider is None:
            # 優先使用Claude Code（無需API密鑰）
            try:
                result = subprocess.run(
                    ["claude", "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    provider = LLMProvider.CLAUDE_CODE
                    logger.info("檢測到Claude Code，使用Claude Code作為LLM提供商")
                else:
                    raise FileNotFoundError("claude command not working")
            except (FileNotFoundError, subprocess.TimeoutExpired):
                # Claude Code不可用，檢查其他提供商
                if os.getenv('OPENAI_API_KEY'):
                    provider = LLMProvider.OPENAI
                    logger.info("檢測到OPENAI_API_KEY，使用OpenAI")
                elif os.getenv('ANTHROPIC_API_KEY'):
                    provider = LLMProvider.ANTHROPIC
                    logger.info("檢測到ANTHROPIC_API_KEY，使用Anthropic")
                else:
                    provider = LLMProvider.NONE
                    logger.info("未檢測到LLM提供商，使用傳統分析方法")

        _global_analyzer = LLMAnalyzer(provider=provider)

    return _global_analyzer


def construct_bazi_personality_prompt(bazi_data: Dict) -> str:
    """
    構建八字性格分析提示

    Args:
        bazi_data: 八字計算數據

    Returns:
        分析提示文本
    """
    return f"""
請根據以下八字命盤數據，進行深度的性格分析（≥300字）：

## 四柱資料
{json.dumps(bazi_data.get('four_pillars', {}), ensure_ascii=False, indent=2)}

## 五行力量
{json.dumps(bazi_data.get('five_elements', {}), ensure_ascii=False, indent=2)}

## 日主分析
{json.dumps(bazi_data.get('day_master', {}), ensure_ascii=False, indent=2)}

## 十神配置
{json.dumps(bazi_data.get('ten_gods', {}), ensure_ascii=False, indent=2)}

請嚴格按照系統提示詞中「性格特質」的分析框架，提供：
1. **日主特性分析**（根據日主天干的核心特質）
2. **十神配置解讀**（通過十神組合看性格側面）
3. **神煞影響**（考慮重要神煞的作用）
4. **五行偏頗影響**（分析五行缺失或過旺的心理影響）
5. **具體行為模式**（給出具體的行為表現和心理特點）
6. **性格改善建議**（針對性的修正建議）

輸出格式：專業的Markdown格式，清晰分層，≥300字。
"""


def construct_bazi_career_prompt(bazi_data: Dict) -> str:
    """構建八字事業分析提示"""
    return f"""
請根據以下八字命盤數據，進行深度的事業發展分析（≥300字）：

## 四柱資料
{json.dumps(bazi_data.get('four_pillars', {}), ensure_ascii=False, indent=2)}

## 官星分析
{json.dumps(bazi_data.get('career_stars', {}), ensure_ascii=False, indent=2)}

## 大運流年
{json.dumps(bazi_data.get('luck_pillars', {}), ensure_ascii=False, indent=2)}

請按照系統提示詞中「事業發展」的分析框架，提供：
1. **適合行業**（根據五行和格局推薦）
2. **發展模式**（打工/創業/自由職業）
3. **權力地位**（官運和領導能力）
4. **職業轉折**（關鍵的事業轉折期）
5. **發展建議**（具體的職業規劃）

輸出格式：專業的Markdown格式，≥300字。
"""


def construct_ziwei_palace_prompt(palace_name: str, palace_data: Dict) -> str:
    """構建紫微宮位分析提示"""
    min_chars = 250 if palace_name in ['命宮', '官祿宮', '財帛宮', '夫妻宮', '福德宮'] else 150

    return f"""
請深度分析紫微斗數【{palace_name}】（≥{min_chars}字）：

## 宮位資料
{json.dumps(palace_data, ensure_ascii=False, indent=2)}

請按照系統提示詞中的分析框架提供：
1. **主星特質**（詳細解讀主星特性）
2. **輔煞影響**（六吉六煞的作用）
3. **四化效應**（四化對該宮的影響）
4. **三方四正**（綜合其他相關宮位）
5. **具體建議**（實用的指引）
6. **信心度評估**（標註分析的可靠程度）

輸出格式：專業的Markdown格式，≥{min_chars}字。
"""


def construct_astrology_area_prompt(area_name: str, astro_data: Dict) -> str:
    """構建占星領域分析提示"""
    return f"""
請進行【{area_name}】的心理占星深度分析（≥300字）：

## 星盤資料
{json.dumps(astro_data, ensure_ascii=False, indent=2)}

請按照系統提示詞提供：
1. **行星/上升點的星座特質**
2. **宮位位置的意義**
3. **主要相位的心理動力**
4. **發展課題和成長方向**
5. **整合建議**（使用賦能式語言）

輸出格式：專業的Markdown格式，使用心理學術語，≥300字。
"""


def construct_synthesis_prompt(
    domain_name: str,
    bazi_data: Dict,
    ziwei_data: Dict,
    astro_data: Dict
) -> str:
    """構建三方法綜合分析提示"""
    return f"""
請進行【{domain_name}】的三方法綜合分析（≥400字）：

## 八字數據
{json.dumps(bazi_data, ensure_ascii=False, indent=2)}

## 紫微數據
{json.dumps(ziwei_data, ensure_ascii=False, indent=2)}

## 占星數據
{json.dumps(astro_data, ensure_ascii=False, indent=2)}

請按照系統提示詞提供：
1. **識別共振點**（三方一致的特質，這些是信心度最高的結論）
2. **跨方法整合洞察**（從不同角度理解同一特質）
3. **信心度評估**（極高/高/中等，基於方法一致性）
4. **整合建議**（綜合三方的實用建議）
5. **矛盾點說明**（如有不一致，誠實說明）

輸出格式：按照系統提示詞中的Markdown模板，≥400字。
"""

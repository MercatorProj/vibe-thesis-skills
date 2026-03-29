#!/usr/bin/env python3
"""
AIGC 写作模式检测器 · 学术文本（academic-writing 技能）

检测学术文本中的 AI 生成痕迹：
- 句长过于均匀、节奏单一
- 机械过渡词滥用（中文：首先、其次、此外、综上所述、值得注意的是 等）
- 抽象套话（在……方面、多种因素、诸多方面 等）
- 词汇多样性不足、段落开头雷同

支持 --lang zh | en | auto，中文默认按。！？；分句，可选 jieba 分词。
"""

import re
import sys
import json
import argparse
from collections import Counter
from typing import List, Dict, Tuple, Optional
import statistics


def _detect_lang(text: str) -> str:
    """Detect language: if >30% of non-space chars in first 500 are CJK, return 'zh' else 'en'."""
    sample = (text.strip() or text)[:500].replace(" ", "").replace("\n", "")
    if not sample:
        return "en"
    cjk = sum(1 for c in sample if "\u4e00" <= c <= "\u9fff")
    return "zh" if cjk / len(sample) > 0.3 else "en"


def _split_sentences_zh(text: str) -> List[str]:
    """Split Chinese text into sentences by 。！？； and newline."""
    normalized = re.sub(r"[。！？；]\s*", "\\g<0>\n", text)
    normalized = re.sub(r"\n+", "\n", normalized)
    raw = re.split(r"(?<=[。！？；])\s*|\n+", normalized)
    return [s.strip() for s in raw if s.strip()]


def _split_sentences_en(text: str) -> List[str]:
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z])", text)
    return [s.strip() for s in sentences if s.strip()]


def _word_count_zh(sentence: str) -> int:
    try:
        import jieba
        return len(list(jieba.cut(sentence)))
    except ImportError:
        return max(1, len(re.sub(r"\s+", "", re.sub(r"[^\u4e00-\u9fff\w]", "", sentence))))


def _word_count_en(sentence: str) -> int:
    return len(sentence.split())


class AIDetector:
    """Detects AI writing patterns in academic text. 中文理工类优先。"""

    AI_TRANSITIONS_EN = [
        "moreover", "furthermore", "additionally", "in addition",
        "it is important to note that", "it should be noted that",
        "it is worth noting that", "notably", "significantly",
    ]

    AI_TRANSITIONS_ZH = [
        "首先", "其次", "再次", "此外", "另外", "同时",
        "综上所述", "总之", "因此", "值得注意的是", "需要指出的是",
        "第一", "第二", "最后", "然后", "接着",
    ]

    ABSTRACT_PHRASES_EN = [
        "various aspects", "multiple factors", "different perspectives",
        "in terms of", "with regard to", "with respect to",
        "it can be seen that", "it has been shown that",
        "plays an important role", "plays a crucial role",
        "serves as", "acts as", "functions as",
    ]

    ABSTRACT_PHRASES_ZH = [
        "从……角度来看", "在……方面", "多种因素", "诸多方面",
        "不同的角度", "各个方面", "在一定程度上", "起着重要作用",
        "具有重要意义", "值得注意的是", "需要说明的是",
        "一方面", "另一方面", "多种方法", "各种因素",
    ]

    def __init__(self, text: str, lang: Optional[str] = None):
        self.text = text
        self.lang = (lang or _detect_lang(text)).lower()
        if self.lang not in ("en", "zh"):
            self.lang = "en"
        self.paragraphs = self._split_paragraphs()
        self.sentences = self._split_sentences()
        self._word_count_fn = _word_count_zh if self.lang == "zh" else _word_count_en

    def _split_paragraphs(self) -> List[str]:
        paragraphs = [p.strip() for p in self.text.split("\n\n") if p.strip()]
        if not paragraphs:
            paragraphs = [self.text.strip()]
        return paragraphs

    def _split_sentences(self) -> List[str]:
        if self.lang == "zh":
            return _split_sentences_zh(self.text)
        return _split_sentences_en(self.text)

    def _get_word_count(self, sentence: str) -> int:
        return self._word_count_fn(sentence)

    def _get_total_words(self) -> int:
        if self.lang == "zh":
            try:
                import jieba
                return len(list(jieba.cut(self.text)))
            except ImportError:
                return max(1, len(re.sub(r"\s+", "", self.text)))
        return len(self.text.split())

    def analyze_sentence_uniformity(self) -> Dict:
        if len(self.sentences) < 3:
            return {"score": 0, "details": "Too few sentences to analyze"}
        word_counts = [self._get_word_count(s) for s in self.sentences]
        avg_length = statistics.mean(word_counts)
        std_dev = statistics.stdev(word_counts) if len(word_counts) > 1 else 0
        variance_ratio = std_dev / avg_length if avg_length > 0 else 0
        if variance_ratio < 0.25:
            score, issue = 0.8, "high_uniformity"
        elif variance_ratio < 0.35:
            score, issue = 0.5, "moderate_uniformity"
        else:
            score, issue = 0.1, "good_variation"
        unit = "字/词" if self.lang == "zh" else "words"
        return {
            "score": score,
            "avg_length": round(avg_length, 1),
            "std_dev": round(std_dev, 1),
            "variance_ratio": round(variance_ratio, 2),
            "issue": issue,
            "details": f"平均句长: {avg_length:.1f} {unit}, 标准差: {std_dev:.1f} (变异比: {variance_ratio:.2f})",
        }

    def detect_transition_overuse(self) -> Dict:
        sentence_starts = [s.strip().lower()[:60] for s in self.sentences]
        transition_count = 0
        found_transitions = []
        if self.lang == "zh":
            for start in sentence_starts:
                for trans in self.AI_TRANSITIONS_ZH:
                    if start.startswith(trans) or start.startswith(trans.strip()):
                        transition_count += 1
                        found_transitions.append(trans)
                        break
        else:
            for start in sentence_starts:
                for trans in self.AI_TRANSITIONS_EN:
                    if start.startswith(trans):
                        transition_count += 1
                        found_transitions.append(trans)
                        break
        transition_pct = (transition_count / len(self.sentences)) * 100 if self.sentences else 0
        if transition_pct > 25:
            score, issue = 0.9, "excessive_transitions"
        elif transition_pct > 15:
            score, issue = 0.6, "high_transitions"
        elif transition_pct > 8:
            score, issue = 0.3, "moderate_transitions"
        else:
            score, issue = 0.1, "appropriate_transitions"
        return {
            "score": score,
            "count": transition_count,
            "percentage": round(transition_pct, 1),
            "found": found_transitions,
            "issue": issue,
            "details": f"{transition_count} 句 ({transition_pct:.1f}%) 以机械过渡词开头",
        }

    def detect_abstract_language(self) -> Dict:
        text_lower = self.text.lower() if self.lang == "en" else self.text
        phrases = self.ABSTRACT_PHRASES_ZH if self.lang == "zh" else self.ABSTRACT_PHRASES_EN
        found_phrases = []
        total_count = 0
        for phrase in phrases:
            if "……" in phrase:
                pattern = phrase.replace("……", r".{0,8}")
                matches = re.findall(pattern, text_lower)
                count = len(matches)
            else:
                count = text_lower.count(phrase)
            if count > 0:
                found_phrases.append([phrase, count])
                total_count += count
        word_count = self._get_total_words()
        density = (total_count / word_count) * 100 if word_count > 0 else 0
        if density > 2.0:
            score, issue = 0.9, "excessive_abstraction"
        elif density > 1.0:
            score, issue = 0.6, "high_abstraction"
        elif density > 0.5:
            score, issue = 0.3, "moderate_abstraction"
        else:
            score, issue = 0.1, "appropriate_specificity"
        return {
            "score": score,
            "total_count": total_count,
            "density": round(density, 2),
            "found": found_phrases,
            "issue": issue,
            "details": f"共 {total_count} 处抽象套话 (密度: {density:.2f} / 100 单位)",
        }

    def calculate_vocabulary_diversity(self) -> Dict:
        if self.lang == "zh":
            try:
                import jieba
                words = list(jieba.cut(self.text))
                words = [w.strip() for w in words if len(w.strip()) > 0]
            except ImportError:
                words = [c for c in self.text if c.strip() and not c.isspace()]
        else:
            words = re.findall(r"\b[a-z]+\b", self.text.lower())
        if len(words) < 10:
            return {"score": 0, "details": "Too few tokens to analyze"}
        unique_words = set(words)
        ttr = len(unique_words) / len(words)
        if ttr < 0.40:
            score, issue = 0.8, "low_diversity"
        elif ttr < 0.50:
            score, issue = 0.5, "moderate_diversity"
        else:
            score, issue = 0.2, "good_diversity"
        return {
            "score": score,
            "ttr": round(ttr, 3),
            "unique_words": len(unique_words),
            "total_words": len(words),
            "issue": issue,
            "details": f"型例比 TTR: {ttr:.3f} ({len(unique_words)} 型 / {len(words)} 例)",
        }

    def detect_passive_voice_overuse(self) -> Dict:
        if self.lang == "zh":
            return {
                "score": 0.1,
                "count": 0,
                "percentage": 0,
                "issue": "appropriate_voice_mix",
                "details": "中文不检测被动语态；英文文本请用 --lang en。",
            }
        passive_patterns = [
            r"\b(is|are|was|were|been|be|being)\s+\w+ed\b",
            r"\b(is|are|was|were|been|be|being)\s+(shown|demonstrated|observed|found|noted|seen|considered|analyzed)\b",
        ]
        passive_count = sum(len(re.findall(p, self.text.lower())) for p in passive_patterns)
        passive_pct = (passive_count / len(self.sentences)) * 100 if self.sentences else 0
        if passive_pct > 50:
            score, issue = 0.7, "excessive_passive"
        elif passive_pct > 35:
            score, issue = 0.5, "high_passive"
        elif passive_pct > 20:
            score, issue = 0.2, "moderate_passive"
        else:
            score, issue = 0.1, "appropriate_voice_mix"
        return {
            "score": score,
            "count": passive_count,
            "percentage": round(passive_pct, 1),
            "issue": issue,
            "details": f"{passive_count} 处被动结构 ({passive_pct:.1f}% 句子)",
        }

    def analyze_paragraph_patterns(self) -> Dict:
        if len(self.paragraphs) < 3:
            return {"score": 0, "details": "Too few paragraphs to analyze"}
        para_starts = []
        for para in self.paragraphs:
            if self.lang == "zh":
                sents = _split_sentences_zh(para)
            else:
                sents = re.split(r"(?<=[.!?])\s+", para)
            if sents:
                para_starts.append((sents[0].lower() if self.lang == "en" else sents[0])[:30])
        similar_count = 0
        for i in range(len(para_starts)):
            for j in range(i + 1, len(para_starts)):
                if para_starts[i][:20] == para_starts[j][:20]:
                    similar_count += 1
        similarity_ratio = similar_count / len(self.paragraphs) if self.paragraphs else 0
        if similarity_ratio > 0.3:
            score, issue = 0.7, "repetitive_openings"
        elif similarity_ratio > 0.15:
            score, issue = 0.4, "some_repetition"
        else:
            score, issue = 0.1, "varied_openings"
        return {
            "score": score,
            "similar_count": similar_count,
            "total_paragraphs": len(self.paragraphs),
            "issue": issue,
            "details": f"{len(self.paragraphs)} 段中有 {similar_count} 处段落开头雷同",
        }

    def calculate_overall_score(self, metrics: Dict) -> float:
        weights = {
            "sentence_uniformity": 0.25,
            "transition_overuse": 0.20,
            "abstract_language": 0.20,
            "vocabulary_diversity": 0.15,
            "passive_voice": 0.10,
            "paragraph_patterns": 0.10,
        }
        return sum(
            (metrics.get(k, {}).get("score", 0) * w for k, w in weights.items())
        )

    def analyze(self) -> Dict:
        metrics = {
            "sentence_uniformity": self.analyze_sentence_uniformity(),
            "transition_overuse": self.detect_transition_overuse(),
            "abstract_language": self.detect_abstract_language(),
            "vocabulary_diversity": self.calculate_vocabulary_diversity(),
            "passive_voice": self.detect_passive_voice_overuse(),
            "paragraph_patterns": self.analyze_paragraph_patterns(),
        }
        overall_score = self.calculate_overall_score(metrics)
        if overall_score > 0.7:
            probability = "Very High"
            recommendation = "文本 AI 痕迹明显，建议大幅改写。"
        elif overall_score > 0.5:
            probability = "High"
            recommendation = "文本存在多处 AI 模式，建议改写。"
        elif overall_score > 0.35:
            probability = "Moderate"
            recommendation = "文本存在部分 AI 模式，建议针对性改写。"
        else:
            probability = "Low"
            recommendation = "文本相对自然，可做小幅调整。"
        if self.lang == "zh":
            probability_zh = {"Very High": "很高", "High": "较高", "Moderate": "中等", "Low": "较低"}.get(probability, probability)
            recommendation = f"{recommendation} (AI 痕迹: {probability_zh})"
        return {
            "lang": self.lang,
            "overall_score": round(overall_score, 3),
            "probability": probability,
            "recommendation": recommendation,
            "metrics": metrics,
            "text_stats": {
                "paragraphs": len(self.paragraphs),
                "sentences": len(self.sentences),
                "words": self._get_total_words(),
            },
        }

    def _score_indicator(self, score: float) -> str:
        if score > 0.7:
            return "需关注"
        if score > 0.4:
            return "建议改进"
        return "尚可"

    def format_report(self, results: Dict, detailed: bool = False) -> str:
        report = []
        report.append("=" * 70)
        report.append("AIGC 写作模式检测报告 (academic-writing)" + (f" [语言: {'中文' if self.lang == 'zh' else '英文'}]"))
        report.append("=" * 70)
        report.append("")
        report.append(f"综合 AI 痕迹: {results['probability']} ({results['overall_score']:.1%})")
        report.append(f"建议: {results['recommendation']}")
        report.append("")
        stats = results["text_stats"]
        report.append("文本统计:")
        report.append(f"  段落: {stats['paragraphs']}  句子: {stats['sentences']}  词/字: {stats['words']}")
        report.append("")
        report.append("分项分析:")
        report.append("-" * 70)
        metrics = results["metrics"]
        m = metrics["sentence_uniformity"]
        report.append(f"\n1. 句长均匀度: {self._score_indicator(m['score'])}")
        report.append(f"   {m['details']}")
        if detailed and m["score"] > 0.4:
            report.append("   -> 建议: 短、中、长句交替。")
        m = metrics["transition_overuse"]
        report.append(f"\n2. 机械过渡词: {self._score_indicator(m['score'])}")
        report.append(f"   {m['details']}")
        if detailed and m.get("found"):
            report.append(f"   出现: {', '.join(list(dict.fromkeys(m['found']))[:10])}")
        m = metrics["abstract_language"]
        report.append(f"\n3. 抽象套话: {self._score_indicator(m['score'])}")
        report.append(f"   {m['details']}")
        if detailed and m.get("found"):
            top = sorted(m["found"], key=lambda x: x[1], reverse=True)[:5]
            report.append(f"   高频: {', '.join([f'{p[0]}({p[1]}次)' for p in top])}")
        m = metrics["vocabulary_diversity"]
        report.append(f"\n4. 词汇多样性: {self._score_indicator(m['score'])}")
        report.append(f"   {m['details']}")
        m = metrics["passive_voice"]
        report.append(f"\n5. 被动语态: {self._score_indicator(m['score'])}")
        report.append(f"   {m['details']}")
        m = metrics["paragraph_patterns"]
        report.append(f"\n6. 段落开头: {self._score_indicator(m['score'])}")
        report.append(f"   {m['details']}")
        report.append("")
        report.append("=" * 70)
        return "\n".join(report)


def _json_serializable(obj: Dict) -> Dict:
    if isinstance(obj, dict):
        return {k: _json_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_json_serializable(x) for x in obj]
    if isinstance(obj, tuple):
        return list(obj)
    return obj


def main():
    if sys.platform == "win32":
        import codecs
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
        sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")
    parser = argparse.ArgumentParser(
        description="学术文本 AIGC 写作模式检测 (academic-writing)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python ai_detector.py input.txt
  python ai_detector.py input.txt --lang zh --detailed
  python ai_detector.py input.txt --json > results.json
        """,
    )
    parser.add_argument("input_file", help="待检测文本文件")
    parser.add_argument("--lang", choices=("en", "zh", "auto"), default="auto", help="语言: zh 中文 / en 英文 / auto 自动")
    parser.add_argument("--detailed", action="store_true", help="输出详细改写建议")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()
    try:
        with open(args.input_file, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"错误: 找不到文件 '{args.input_file}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"读取文件出错: {e}", file=sys.stderr)
        sys.exit(1)
    if not text.strip():
        print("错误: 文件为空", file=sys.stderr)
        sys.exit(1)
    lang = None if args.lang == "auto" else args.lang
    detector = AIDetector(text, lang=lang)
    results = detector.analyze()
    if args.json:
        print(json.dumps(_json_serializable(results), indent=2, ensure_ascii=False))
    else:
        print(detector.format_report(results, detailed=args.detailed))


if __name__ == "__main__":
    main()

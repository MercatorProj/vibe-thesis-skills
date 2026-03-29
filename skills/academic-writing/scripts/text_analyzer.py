#!/usr/bin/env python3
"""
学术文本质量分析器（academic-writing 技能）

提供句长分布、词汇丰富度(TTR)、过渡词密度、被动语态(英文)等指标。
支持 --lang zh | en | auto；中文按。！？；分句，可选 jieba 分词。
"""

import re
import sys
import argparse
from collections import Counter
from typing import List, Dict, Optional
import statistics


def _detect_lang(text: str) -> str:
    sample = (text.strip() or text)[:500].replace(" ", "").replace("\n", "")
    if not sample:
        return "en"
    cjk = sum(1 for c in sample if "\u4e00" <= c <= "\u9fff")
    return "zh" if cjk / len(sample) > 0.3 else "en"


def _split_sentences_zh(text: str) -> List[str]:
    normalized = re.sub(r"[。！？；]\s*", "\\g<0>\n", text)
    normalized = re.sub(r"\n+", "\n", normalized)
    raw = re.split(r"(?<=[。！？；])\s*|\n+", normalized)
    return [s.strip() for s in raw if s.strip()]


def _split_sentences_en(text: str) -> List[str]:
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z])", text)
    return [s.strip() for s in sentences if s.strip()]


def _words_zh(text: str) -> List[str]:
    try:
        import jieba
        return list(jieba.cut(text))
    except ImportError:
        return [c for c in text if c.strip() and not c.isspace()]


def _words_en(text: str) -> List[str]:
    return re.findall(r"\b[a-z]+\b", text.lower())


class TextAnalyzer:
    """学术文本质量分析（工学/社科通用）。"""

    TRANSITIONS_ZH = ["首先", "其次", "此外", "同时", "综上所述", "因此", "然而", "另外", "值得注意的是", "最后"]

    TRANSITIONS_EN = {
        "additive": ["moreover", "furthermore", "additionally", "also", "besides"],
        "adversative": ["however", "nevertheless", "nonetheless", "yet", "still"],
        "causal": ["therefore", "thus", "consequently", "hence", "accordingly"],
        "sequential": ["first", "second", "finally", "subsequently", "meanwhile"],
    }

    def __init__(self, text: str, lang: Optional[str] = None):
        self.text = text
        self.lang = (lang or _detect_lang(text)).lower()
        if self.lang not in ("en", "zh"):
            self.lang = "en"
        self.sentences = _split_sentences_zh(self.text) if self.lang == "zh" else _split_sentences_en(self.text)
        self.words = _words_zh(self.text) if self.lang == "zh" else _words_en(self.text)

    def sentence_length_stats(self) -> Dict:
        if not self.sentences:
            return {"error": "未检测到句子"}
        if self.lang == "zh":
            lengths = [len(_words_zh(s)) for s in self.sentences]
        else:
            lengths = [len(s.split()) for s in self.sentences]
        unit = "词" if self.lang == "zh" else "words"
        short_thresh, long_thresh = (8, 25) if self.lang == "zh" else (12, 22)
        short = sum(1 for l in lengths if l < short_thresh)
        medium = sum(1 for l in lengths if short_thresh <= l <= long_thresh)
        long_c = sum(1 for l in lengths if l > long_thresh)
        total = len(lengths)
        return {
            "count": len(lengths),
            "min": min(lengths),
            "max": max(lengths),
            "mean": round(statistics.mean(lengths), 2),
            "median": round(statistics.median(lengths), 2),
            "stdev": round(statistics.stdev(lengths), 2) if len(lengths) > 1 else 0,
            "unit": unit,
            "distribution": {
                "short": short,
                "short_pct": round(short / total * 100, 1) if total > 0 else 0,
                "medium": medium,
                "medium_pct": round(medium / total * 100, 1) if total > 0 else 0,
                "long": long_c,
                "long_pct": round(long_c / total * 100, 1) if total > 0 else 0,
            },
        }

    def vocabulary_metrics(self) -> Dict:
        if not self.words:
            return {"error": "未检测到词/字"}
        unique = set(self.words)
        ttr = len(unique) / len(self.words)
        word_freq = Counter(self.words)
        most_common = word_freq.most_common(10)
        return {
            "total_words": len(self.words),
            "unique_words": len(unique),
            "type_token_ratio": round(ttr, 3),
            "most_common": most_common,
        }

    def transition_word_analysis(self) -> Dict:
        if self.lang == "zh":
            total = sum(self.text.count(t) for t in self.TRANSITIONS_ZH)
            density = (total / len(self.words)) * 100 if self.words else 0
            return {
                "total_transitions": total,
                "density_per_100_words": round(density, 2),
                "by_category": {"中文连接词": total},
            }
        text_lower = self.text.lower()
        results = {}
        total_transitions = 0
        for category, words in self.TRANSITIONS_EN.items():
            count = sum(text_lower.count(f" {w} ") + text_lower.count(f"{w}, ") for w in words)
            results[category] = count
            total_transitions += count
        density = (total_transitions / len(self.words)) * 100 if self.words else 0
        return {
            "total_transitions": total_transitions,
            "density_per_100_words": round(density, 2),
            "by_category": results,
        }

    def passive_voice_analysis(self) -> Dict:
        if self.lang == "zh":
            return {"passive_constructions": 0, "per_sentence": 0, "percentage": 0}
        passive_patterns = [
            r"\b(is|are|was|were|been|be|being)\s+\w+ed\b",
            r"\b(is|are|was|were|been|be|being)\s+(shown|demonstrated|observed|found|noted|seen|considered|analyzed)\b",
        ]
        passive_count = sum(len(re.findall(p, self.text.lower())) for p in passive_patterns)
        per_sent = passive_count / len(self.sentences) if self.sentences else 0
        pct = (passive_count / len(self.sentences)) * 100 if self.sentences else 0
        return {
            "passive_constructions": passive_count,
            "per_sentence": round(per_sent, 2),
            "percentage": round(pct, 1),
        }

    def readability_metrics(self) -> Dict:
        if not self.sentences or not self.words:
            return {"error": "文本不足"}
        avg_sent = len(self.words) / len(self.sentences)
        avg_word_len = sum(len(w) for w in self.words) / len(self.words)
        complex_w = sum(1 for w in self.words if len(w) > 6) if self.lang == "en" else 0
        complex_pct = (complex_w / len(self.words)) * 100 if self.words else 0
        return {
            "avg_sentence_length": round(avg_sent, 2),
            "avg_word_length": round(avg_word_len, 2),
            "complex_words": complex_w,
            "complex_word_pct": round(complex_pct, 1),
        }

    def analyze(self) -> Dict:
        return {
            "lang": self.lang,
            "sentence_stats": self.sentence_length_stats(),
            "vocabulary": self.vocabulary_metrics(),
            "transitions": self.transition_word_analysis(),
            "passive_voice": self.passive_voice_analysis(),
            "readability": self.readability_metrics(),
        }

    def format_report(self, results: Dict) -> str:
        report = []
        report.append("=" * 70)
        report.append("文本质量分析报告 (academic-writing)" + (f" [语言: {'中文' if results.get('lang') == 'zh' else '英文'}]"))
        report.append("=" * 70)
        report.append("")
        stats = results["sentence_stats"]
        if "error" in stats:
            report.append("句长统计: " + stats["error"])
        else:
            unit = stats.get("unit", "词")
            report.append("句长统计")
            report.append("-" * 70)
            report.append(f"句子数: {stats['count']}  范围: {stats['min']}-{stats['max']} {unit}")
            report.append(f"均值: {stats['mean']} {unit}  标准差: {stats['stdev']}")
            d = stats["distribution"]
            report.append(f"短句: {d['short']}({d['short_pct']}%)  中句: {d['medium']}({d['medium_pct']})  长句: {d['long']}({d['long_pct']}%)")
        report.append("")
        vocab = results["vocabulary"]
        if "error" in vocab:
            report.append("词汇: " + vocab["error"])
        else:
            report.append("词汇丰富度")
            report.append("-" * 70)
            report.append(f"总词数: {vocab['total_words']}  型数: {vocab['unique_words']}  TTR: {vocab['type_token_ratio']}")
            report.append("高频: " + ", ".join([f"{w}({c})" for w, c in vocab["most_common"][:5]]))
        report.append("")
        trans = results["transitions"]
        report.append("过渡词")
        report.append("-" * 70)
        report.append(f"总数: {trans['total_transitions']}  每百单位密度: {trans['density_per_100_words']}")
        report.append("")
        passive = results["passive_voice"]
        report.append("被动语态")
        report.append("-" * 70)
        report.append(f"数量: {passive['passive_constructions']}  占比: {passive['percentage']}%")
        report.append("")
        read = results["readability"]
        if "error" not in read:
            report.append("可读性")
            report.append("-" * 70)
            report.append(f"平均句长: {read['avg_sentence_length']}  平均词长: {read['avg_word_length']}")
        report.append("")
        report.append("=" * 70)
        return "\n".join(report)

    @staticmethod
    def compare_texts(text1: str, text2: str, lang: Optional[str] = None) -> str:
        a1 = TextAnalyzer(text1, lang=lang)
        a2 = TextAnalyzer(text2, lang=lang)
        r1 = a1.analyze()
        r2 = a2.analyze()
        report = []
        report.append("=" * 70)
        report.append("改写前后对比 (academic-writing)")
        report.append("=" * 70)
        s1 = r1["sentence_stats"]
        s2 = r2["sentence_stats"]
        if "error" not in s1 and "error" not in s2:
            report.append("句长: 均值 " + str(s1["mean"]) + " -> " + str(s2["mean"]) + ", 标准差 " + str(s1["stdev"]) + " -> " + str(s2["stdev"]))
        v1 = r1["vocabulary"]
        v2 = r2["vocabulary"]
        if "error" not in v1 and "error" not in v2:
            report.append("TTR: " + str(v1["type_token_ratio"]) + " -> " + str(v2["type_token_ratio"]))
        t1 = r1["transitions"]
        t2 = r2["transitions"]
        report.append("过渡词密度/100: " + str(t1["density_per_100_words"]) + " -> " + str(t2["density_per_100_words"]))
        report.append("=" * 70)
        return "\n".join(report)


def main():
    if sys.platform == "win32":
        import codecs
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
        sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")
    parser = argparse.ArgumentParser(
        description="学术文本质量分析 (academic-writing)",
        epilog="示例: python text_analyzer.py input.txt  |  python text_analyzer.py 原文.txt 改写.txt --compare",
    )
    parser.add_argument("input_file", help="输入文本文件")
    parser.add_argument("input_file2", nargs="?", help="第二文件（用于对比）")
    parser.add_argument("--compare", action="store_true", help="对比两文件")
    parser.add_argument("--lang", choices=("en", "zh", "auto"), default="auto", help="语言")
    args = parser.parse_args()
    try:
        with open(args.input_file, "r", encoding="utf-8") as f:
            text1 = f.read()
    except FileNotFoundError:
        print(f"错误: 找不到文件 '{args.input_file}'", file=sys.stderr)
        sys.exit(1)
    if not text1.strip():
        print("错误: 文件为空", file=sys.stderr)
        sys.exit(1)
    lang = None if args.lang == "auto" else args.lang
    if args.compare or args.input_file2:
        if not args.input_file2:
            print("错误: 对比模式需提供两个文件", file=sys.stderr)
            sys.exit(1)
        try:
            with open(args.input_file2, "r", encoding="utf-8") as f:
                text2 = f.read()
        except FileNotFoundError:
            print(f"错误: 找不到文件 '{args.input_file2}'", file=sys.stderr)
            sys.exit(1)
        print(TextAnalyzer.compare_texts(text1, text2, lang=lang))
    else:
        analyzer = TextAnalyzer(text1, lang=lang)
        print(analyzer.format_report(analyzer.analyze()))


if __name__ == "__main__":
    main()

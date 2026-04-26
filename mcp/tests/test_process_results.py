"""Tests for process_results: dedup, filtering, ranking, output formats."""

import json
import os
import tempfile

import pytest

from litrev_mcp.tools.search import (
    _check_relevance,
    process_results,
    deduplicate_results,
    generate_search_summary,
)


def _write_results(results):
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    json.dump(results, f)
    f.close()
    return f.name


SAMPLE_RESULTS = [
    {
        "pmid": "1",
        "title": "Study Alpha",
        "authors": ["Smith, J", "Jones, A"],
        "year": 2020,
        "journal": "Journal A",
        "citations": 50,
        "doi": "10.1000/alpha",
        "source": "PubMed",
        "study_type": "RCT",
    },
    {
        "pmid": "2",
        "title": "Study Beta",
        "authors": "Lee, B and Park, C",
        "year": 2019,
        "journal": "Journal B",
        "citations": 100,
        "doi": "10.1000/beta",
        "source": "Semantic Scholar",
        "study_type": "meta-analysis",
    },
    {
        "pmid": "3",
        "title": "Study Gamma",
        "authors": ["Chen, D"],
        "year": 2021,
        "journal": "Journal C",
        "citations": 10,
        "doi": "10.1000/gamma",
        "source": "PubMed",
        "study_type": "RCT",
    },
]


class TestGenerateSearchSummary:
    def test_basic_summary(self):
        summary = generate_search_summary(SAMPLE_RESULTS)
        assert summary["total_results"] == 3
        assert summary["sources"]["PubMed"] == 2
        assert summary["sources"]["Semantic Scholar"] == 1
        assert summary["total_citations"] == 160
        assert summary["avg_citations"] == pytest.approx(160 / 3)

    def test_empty_results(self):
        summary = generate_search_summary([])
        assert summary["total_results"] == 0
        assert summary["total_citations"] == 0

    def test_missing_citations(self):
        results = [{"title": "No citations"}, {"citations": "bad"}]
        summary = generate_search_summary(results)
        assert summary["total_citations"] == 0

    def test_year_distribution(self):
        summary = generate_search_summary(SAMPLE_RESULTS)
        assert summary["year_distribution"][2020] == 1
        assert summary["year_distribution"][2019] == 1
        assert summary["year_distribution"][2021] == 1


class TestProcessResults:
    def test_markdown_output(self):
        path = _write_results(SAMPLE_RESULTS)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "results.md")
            try:
                result = process_results(
                    path, output_format="markdown", output_path=out
                )
                assert result["total_results"] == 3
                assert os.path.isfile(out)
                with open(out) as f:
                    content = f.read()
                assert "Study Alpha" in content
                assert "Study Beta" in content
            finally:
                os.unlink(path)

    def test_json_output(self):
        path = _write_results(SAMPLE_RESULTS)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "results.json")
            try:
                result = process_results(path, output_format="json", output_path=out)
                with open(out) as f:
                    data = json.load(f)
                assert len(data) == 3
                assert "_original_idx" not in data[0]
            finally:
                os.unlink(path)

    def test_bibtex_output(self):
        path = _write_results(SAMPLE_RESULTS)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "results.bib")
            try:
                process_results(path, output_format="bibtex", output_path=out)
                with open(out) as f:
                    content = f.read()
                assert "@article{" in content
                assert "10.1000/alpha" in content
            finally:
                os.unlink(path)

    def test_ris_output(self):
        path = _write_results(SAMPLE_RESULTS)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "results.ris")
            try:
                process_results(path, output_format="ris", output_path=out)
                with open(out) as f:
                    content = f.read()
                assert "TY  - JOUR" in content
                assert "DO  - 10.1000/alpha" in content
            finally:
                os.unlink(path)

    def test_unknown_format_returns_error(self):
        path = _write_results(SAMPLE_RESULTS)
        try:
            result = process_results(path, output_format="xml")
            assert "error" in result
        finally:
            os.unlink(path)

    def test_invalid_json_returns_error(self):
        path = _write_results({"not": "a list"})
        try:
            result = process_results(path)
            assert "error" in result
        finally:
            os.unlink(path)

    def test_deduplication(self):
        duped = SAMPLE_RESULTS + [
            {
                "pmid": "1",
                "title": "Study Alpha duplicate",
                "year": 2020,
                "abstract": "Extra abstract",
            }
        ]
        path = _write_results(duped)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "results.json")
            try:
                result = process_results(
                    path, output_format="json", output_path=out, deduplicate=True
                )
                assert result["total_results"] == 3
                assert "Deduplicated: 4 -> 3" in result["log"]
            finally:
                os.unlink(path)

    def test_no_deduplication(self):
        duped = SAMPLE_RESULTS + [{"pmid": "1", "title": "Dup"}]
        path = _write_results(duped)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "results.json")
            try:
                result = process_results(
                    path,
                    output_format="json",
                    output_path=out,
                    deduplicate=False,
                )
                assert result["total_results"] == 4
            finally:
                os.unlink(path)

    def test_year_filter(self):
        path = _write_results(SAMPLE_RESULTS)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "results.json")
            try:
                result = process_results(
                    path,
                    output_format="json",
                    output_path=out,
                    year_start=2020,
                )
                assert result["total_results"] == 2
            finally:
                os.unlink(path)

    def test_year_filter_end(self):
        path = _write_results(SAMPLE_RESULTS)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "results.json")
            try:
                result = process_results(
                    path,
                    output_format="json",
                    output_path=out,
                    year_end=2019,
                )
                assert result["total_results"] == 1
            finally:
                os.unlink(path)

    def test_study_type_filter(self):
        path = _write_results(SAMPLE_RESULTS)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "results.json")
            try:
                result = process_results(
                    path,
                    output_format="json",
                    output_path=out,
                    study_types=["RCT"],
                )
                assert result["total_results"] == 2
            finally:
                os.unlink(path)

    def test_rank_by_citations(self):
        path = _write_results(SAMPLE_RESULTS)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "results.json")
            try:
                process_results(
                    path,
                    output_format="json",
                    output_path=out,
                    rank_by="citations",
                )
                with open(out) as f:
                    data = json.load(f)
                assert data[0]["title"] == "Study Beta"
                assert data[-1]["title"] == "Study Gamma"
            finally:
                os.unlink(path)

    def test_rank_by_year(self):
        path = _write_results(SAMPLE_RESULTS)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "results.json")
            try:
                process_results(
                    path,
                    output_format="json",
                    output_path=out,
                    rank_by="year",
                )
                with open(out) as f:
                    data = json.load(f)
                assert data[0]["year"] == 2021
            finally:
                os.unlink(path)

    def test_publication_type_list_does_not_crash(self):
        results_with_list_pubtype = [
            {
                "pmid": "10",
                "title": "PubMed style record",
                "year": 2022,
                "journal": "J Test",
                "citations": 5,
                "source": "PubMed",
                "publication_type": ["Journal Article", "Randomized Controlled Trial"],
            },
            {
                "pmid": "11",
                "title": "Another record",
                "year": 2023,
                "journal": "J Test",
                "citations": 3,
                "source": "PubMed",
                "publication_type": [],
            },
        ]
        path = _write_results(results_with_list_pubtype)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "results.md")
            try:
                result = process_results(
                    path, output_format="markdown", output_path=out
                )
                assert result["total_results"] == 2
                assert "error" not in result
            finally:
                os.unlink(path)

    def test_study_type_filter_with_publication_type_list(self):
        results_with_list_pubtype = [
            {
                "pmid": "10",
                "title": "RCT record",
                "year": 2022,
                "source": "PubMed",
                "publication_type": ["Journal Article", "Randomized Controlled Trial"],
            },
            {
                "pmid": "11",
                "title": "Review record",
                "year": 2023,
                "source": "PubMed",
                "publication_type": ["Review"],
            },
        ]
        path = _write_results(results_with_list_pubtype)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "results.json")
            try:
                result = process_results(
                    path,
                    output_format="json",
                    output_path=out,
                    study_types=["Review"],
                )
                assert result["total_results"] == 1
            finally:
                os.unlink(path)


class TestDeduplicateResults:
    def test_basic_dedup(self):
        duped = [
            {"pmid": "1", "title": "A", "doi": ""},
            {"pmid": "1", "title": "A copy", "doi": "10.1000/x"},
            {"pmid": "2", "title": "B"},
        ]
        path = _write_results(duped)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "deduped.json")
            try:
                result = deduplicate_results(path, output_path=out)
                assert result["before"] == 3
                assert result["after"] == 2
                assert result["removed"] == 1
                assert result["duplicates_by_pmid"] == 1
                assert result["duplicates_by_doi"] == 0
                assert result["duplicates_by_title"] == 0
                with open(out) as f:
                    data = json.load(f)
                assert len(data) == 2
            finally:
                os.unlink(path)

    def test_author_string_split(self):
        results = [{"pmid": "1", "title": "A", "authors": "Smith, J, Jones, A"}]
        path = _write_results(results)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "deduped.json")
            try:
                deduplicate_results(path, output_path=out)
                with open(out) as f:
                    data = json.load(f)
                assert isinstance(data[0]["authors"], list)
            finally:
                os.unlink(path)

    def test_in_place_dedup(self):
        results = [{"pmid": "1", "title": "A"}]
        path = _write_results(results)
        try:
            result = deduplicate_results(path)
            assert result["output_path"] == path
            with open(path) as f:
                data = json.load(f)
            assert len(data) == 1
        finally:
            os.unlink(path)


class TestRelevanceGate:
    RELEVANT = [
        {
            "title": "Melatonin improves sleep in autism",
            "abstract": "RCT of melatonin in children with ASD.",
            "source": "PubMed-search",
            "year": 2022,
            "citations": 10,
        },
        {
            "title": "Sleep latency and melatonin in ASD",
            "abstract": "Crossover trial of melatonin vs placebo.",
            "source": "PubMed-search",
            "year": 2021,
            "citations": 5,
        },
        {
            "title": "Melatonin for insomnia in autism spectrum disorder",
            "abstract": "Systematic review of melatonin efficacy.",
            "source": "S2-search",
            "year": 2023,
            "citations": 20,
        },
    ]

    NOISY_S2 = [
        {
            "title": "Gut microbiota and autism",
            "abstract": "Probiotics in ASD children.",
            "source": "S2-search",
            "year": 2022,
            "citations": 100,
        },
        {
            "title": "ADHD genetics meta-analysis",
            "abstract": "Genome-wide association study.",
            "source": "S2-search",
            "year": 2020,
            "citations": 200,
        },
        {
            "title": "Eating disorders in children",
            "abstract": "Prevalence survey.",
            "source": "S2-search",
            "year": 2019,
            "citations": 150,
        },
    ]

    def test_check_relevance_all_on_topic(self):
        result = _check_relevance(self.RELEVANT, ["melatonin"])
        assert result["passed"] is True
        assert result["blocked_sources"] == []
        assert result["source_stats"]["PubMed-search"]["off_topic_pct"] == 0.0

    def test_check_relevance_blocks_noisy_source(self):
        data = self.RELEVANT + self.NOISY_S2
        result = _check_relevance(data, ["melatonin"], max_offtopic_pct=25.0)
        assert result["passed"] is False
        assert "S2-search" in result["blocked_sources"]
        assert "PubMed-search" not in result["blocked_sources"]
        assert result["source_stats"]["S2-search"]["off_topic_pct"] == 75.0

    def test_check_relevance_custom_threshold(self):
        data = self.RELEVANT + self.NOISY_S2
        result = _check_relevance(data, ["melatonin"], max_offtopic_pct=80.0)
        assert result["passed"] is True

    def test_check_relevance_matches_in_abstract(self):
        articles = [
            {
                "title": "Sleep in children",
                "abstract": "We studied melatonin effects.",
                "source": "OA",
            }
        ]
        result = _check_relevance(articles, ["melatonin"])
        assert result["source_stats"]["OA"]["on_topic"] == 1

    def test_check_relevance_case_insensitive(self):
        articles = [
            {
                "title": "MELATONIN and Sleep",
                "abstract": "",
                "source": "PM",
            }
        ]
        result = _check_relevance(articles, ["melatonin"])
        assert result["source_stats"]["PM"]["on_topic"] == 1

    def test_process_results_blocked_by_relevance(self):
        data = self.RELEVANT + self.NOISY_S2
        path = _write_results(data)
        try:
            result = process_results(
                path,
                deduplicate=False,
                required_terms=["melatonin"],
                max_offtopic_pct=25.0,
            )
            assert result["status"] == "blocked"
            assert result["reason"] == "relevance_gate"
            assert "S2-search" in result["blocked_sources"]
        finally:
            os.unlink(path)

    def test_process_results_passes_relevance(self):
        path = _write_results(self.RELEVANT)
        try:
            result = process_results(
                path,
                deduplicate=False,
                required_terms=["melatonin"],
                max_offtopic_pct=25.0,
            )
            assert "status" not in result or result.get("status") != "blocked"
            assert result["total_results"] == 3
        finally:
            os.unlink(path)

    def test_process_results_no_terms_skips_gate(self):
        data = self.RELEVANT + self.NOISY_S2
        path = _write_results(data)
        try:
            result = process_results(path, deduplicate=False)
            assert result.get("status") != "blocked"
            assert result["total_results"] == 6
        finally:
            os.unlink(path)

    def test_relevance_log_contains_stats(self):
        path = _write_results(self.RELEVANT)
        try:
            result = process_results(
                path,
                deduplicate=False,
                required_terms=["melatonin"],
            )
            log = " ".join(result.get("log", []))
            assert "Relevance check" in log
            assert "melatonin" in log
        finally:
            os.unlink(path)

    def test_filter_mode_keeps_on_topic_from_blocked_source(self):
        data = self.RELEVANT + self.NOISY_S2
        path = _write_results(data)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "results.json")
            try:
                result = process_results(
                    path,
                    output_format="json",
                    output_path=out,
                    deduplicate=False,
                    required_terms=["melatonin"],
                    max_offtopic_pct=25.0,
                    relevance_mode="filter",
                )
                assert result.get("status") != "blocked"
                assert result["total_results"] == 3
                with open(out) as f:
                    articles = json.load(f)
                sources = {a["source"] for a in articles}
                assert "S2-search" in sources
                assert "PubMed-search" in sources
                titles = {a["title"] for a in articles}
                assert "Melatonin for insomnia in autism spectrum disorder" in titles
                assert "Gut microbiota and autism" not in titles
            finally:
                os.unlink(path)

    def test_filter_mode_log_reports_removals(self):
        data = self.RELEVANT + self.NOISY_S2
        path = _write_results(data)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "results.json")
            try:
                result = process_results(
                    path,
                    output_format="json",
                    output_path=out,
                    deduplicate=False,
                    required_terms=["melatonin"],
                    max_offtopic_pct=25.0,
                    relevance_mode="filter",
                )
                log = " ".join(result.get("log", []))
                assert "Relevance filter" in log
                assert "3" in log
            finally:
                os.unlink(path)

    def test_filter_mode_noop_when_all_pass(self):
        path = _write_results(self.RELEVANT)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "results.json")
            try:
                result = process_results(
                    path,
                    output_format="json",
                    output_path=out,
                    deduplicate=False,
                    required_terms=["melatonin"],
                    relevance_mode="filter",
                )
                assert result["total_results"] == 3
                log = " ".join(result.get("log", []))
                assert "Relevance filter" not in log
            finally:
                os.unlink(path)

    def test_check_relevance_returns_detail(self):
        data = self.RELEVANT + self.NOISY_S2
        result = _check_relevance(data, ["melatonin"], max_offtopic_pct=25.0)
        assert "source_stats_detail" in result
        s2_detail = result["source_stats_detail"]["S2-search"]
        assert len(s2_detail["off_topic_indices"]) == 3
        assert s2_detail["on_topic"] == 1

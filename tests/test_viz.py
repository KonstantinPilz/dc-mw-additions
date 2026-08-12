import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"
DATA = ROOT / "docs" / "data.json"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.metas = []
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "meta":
            self.metas.append(values)
        elif tag == "script":
            self.scripts.append(values)


class VisualizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = INDEX.read_text(encoding="utf-8")
        cls.parser = PageParser()
        cls.parser.feed(cls.html)
        cls.data = json.loads(DATA.read_text(encoding="utf-8"))

    def test_required_noindex_meta_is_exact(self):
        self.assertIn(
            {"name": "robots", "content": "noindex, nofollow"},
            self.parser.metas,
        )

    def test_data_has_expected_shape(self):
        self.assertEqual(len(self.data["countries"]), 22)
        for country, values in self.data["countries"].items():
            self.assertEqual(set(values), {"2022", "2023", "2024", "2025", "2026"})
            for year, observation in values.items():
                self.assertGreater(observation["mw"], 0, (country, year))
                self.assertRegex(observation["reasoning"], r"\[[^]]+\]\(https?://")

    def test_page_fetches_sibling_data_and_uses_d3_only(self):
        self.assertRegex(self.html, r"fetch\(\s*['\"]data\.json['\"]\s*\)")
        external_scripts = [s.get("src", "") for s in self.parser.scripts if s.get("src")]
        self.assertEqual(len(external_scripts), 1)
        self.assertRegex(external_scripts[0], r"^https://[^/]*jsdelivr\.net/npm/d3@")

    def test_required_interactions_are_present(self):
        for token in (
            'value="annual"',
            'value="cumulative"',
            'value="linear"',
            'value="log"',
            'value="all"',
            'id="legend"',
            'id="tooltip"',
        ):
            self.assertIn(token, self.html)
        self.assertIn("appendMarkdownLinks", self.html)

    def test_title_and_footer_copy(self):
        self.assertIn("Data-center capacity additions by country, 2022–2026", self.html)
        self.assertIn(
            "Data: Konstantin's Claude research team, 2026-08-12. Medians; 2026 is a full-year estimate. Definitions: IT (critical) MW, colo + hyperscale + AI campuses.",
            self.html,
        )
        self.assertIn(
            "China 2024–25 partly reflects a statistical series change; US 2026 follows SemiAnalysis's construction-backed forecast.",
            self.html,
        )

    def test_index_is_the_only_html_page(self):
        self.assertEqual(list((ROOT / "docs").glob("*.html")), [INDEX])


if __name__ == "__main__":
    unittest.main()

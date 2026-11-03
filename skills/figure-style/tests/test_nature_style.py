"""Behavioral checks for fixed-canvas exports, failure handling, and mappings.

Run: python -m unittest discover -s <SKILL_DIR>/tests -v
Requires Matplotlib, PyYAML, Pillow; PyMuPDF enables PDF inspection.
"""

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import nature_style as ns


class NatureStyleTests(unittest.TestCase):
    def setUp(self):
        self.style = ns.load_style()
        self.context = matplotlib.rc_context()
        self.context.__enter__()

    def tearDown(self):
        plt.close("all")
        self.context.__exit__(None, None, None)

    def test_explicit_font_failure(self):
        self.style["defaults"]["font"] = "DefinitelyMissingFigureStyleFont1234"
        with self.assertRaises(ValueError):
            ns.apply_style(self.style)

    def test_project_then_figure_mapping_and_unknown_entity(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "project.yaml"
            figure = Path(temp) / "figure.yaml"
            project.write_text("colors:\n  entities:\n    Control: '#0072B2'\n    Treatment: '#E69F00'\n")
            figure.write_text("colors:\n  entities:\n    Treatment: '#CC79A7'\n")
            style = ns.load_style(overrides=[project, figure])
        self.assertEqual(ns.entity_colors(["Treatment", "Control"], style=style),
                         {"Treatment": "#CC79A7", "Control": "#0072B2"})
        with self.assertRaises(ValueError):
            ns.entity_colors(["Undefined"], style=style)
        with self.assertRaises(ValueError):
            ns.entity_colors(list("abcdefgh"))

    def test_fixed_canvas_even_under_global_tight_setting(self):
        with tempfile.TemporaryDirectory() as temp:
            fig, ax = plt.subplots(figsize=ns.figsize_mm(89, 65))
            ax.plot([0, 1], [0, 1])
            matplotlib.rcParams["savefig.bbox"] = "tight"
            files = ns.save_figure(fig, Path(temp) / "new" / "plot.v2",
                                   formats=["png", "pdf"], check=False)
            self.assertEqual(files[0].name, "plot.v2.png")
            with Image.open(files[0]) as im:
                self.assertAlmostEqual(im.width / 450 * 25.4, 89, delta=.06)
                self.assertAlmostEqual(im.height / 450 * 25.4, 65, delta=.06)
            self.assertEqual(matplotlib.rcParams["savefig.bbox"], "tight")
            if importlib.util.find_spec("fitz"):
                import fitz
                with fitz.open(files[1]) as doc:
                    self.assertAlmostEqual(doc[0].rect.width / 72 * 25.4, 89, places=3)
                    self.assertTrue(doc[0].get_text().strip())
                    self.assertTrue(doc[0].get_drawings())
                    self.assertNotIn("Type3", [font[2] for font in doc[0].get_fonts()])

    def test_export_errors_propagate(self):
        fig = plt.figure(figsize=ns.figsize_mm(89, 65))
        with tempfile.TemporaryDirectory() as temp:
            with patch.object(fig, "savefig", side_effect=OSError("simulated disk error")):
                with self.assertRaisesRegex(OSError, "simulated disk error"):
                    ns.save_figure(fig, Path(temp) / "plot", check=False)

    def test_raster_dpi_not_capped_for_pdf(self):
        fig = plt.figure(figsize=ns.figsize_mm(89, 65))
        self.style["defaults"]["raster_dpi"] = 600
        with tempfile.TemporaryDirectory() as temp:
            with patch.object(fig, "savefig", wraps=fig.savefig) as save:
                ns.save_figure(fig, Path(temp) / "plot", style=self.style,
                               formats=["pdf"], check=False)
            self.assertEqual(save.call_args.kwargs["dpi"], 600)

    def test_font_size_and_bounds_are_checked(self):
        # DejaVu is intentionally noncompliant, making this check portable in CI.
        fig, ax = plt.subplots(figsize=ns.figsize_mm(89, 65))
        ax.text(.5, .5, "Too small", fontsize=4)
        fig.text(1.1, .5, "Outside", fontsize=6)
        errors = ns.validate_figure(fig)
        self.assertTrue(any("Too small" in error and "4 pt" in error for error in errors))
        self.assertTrue(any("Outside" in error and "outside the canvas" in error for error in errors))

    def test_ticks_outside_the_view_are_not_exported(self):
        self.style["defaults"]["font"] = "DejaVu Sans"
        self.style["requirements"]["font_families"] = ["DejaVu Sans"]
        ns.apply_style(self.style)
        fig, ax = plt.subplots(figsize=ns.figsize_mm(89, 65))
        ax.set_xticks([-100, 0, 1, 100])
        ax.set_xlim(0, 1)
        self.assertEqual(ns.validate_figure(fig, style=self.style), [])

    def test_oversize_or_invalid_formats_fail_before_writing(self):
        fig = plt.figure(figsize=ns.figsize_mm(89, 180))
        self.assertTrue(any("Height" in e for e in ns.validate_figure(fig)))
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                ns.save_figure(fig, Path(temp) / "bad", formats=["not-a-format"], check=False)
            self.assertEqual(list(Path(temp).iterdir()), [])


if __name__ == "__main__":
    unittest.main()

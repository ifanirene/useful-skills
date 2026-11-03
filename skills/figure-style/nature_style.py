"""Local Nature preset and fixed-canvas exporter; see references/sources.md.

Requires Matplotlib and PyYAML. Import explicitly from this skill's directory.
All output belongs in the requesting project, never in the skill directory.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import matplotlib as mpl
from matplotlib import font_manager
from matplotlib.text import Text
import yaml


STYLE_PATH = Path(__file__).resolve().with_name("house_style.yaml")


def _merge(base, update):
    result = deepcopy(base)
    for key, value in update.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _merge(result[key], value)
        else:
            result[key] = deepcopy(value)
    return result


def load_style(path=None, *, overrides=()):
    """Load the shared preset, then explicitly supplied project/figure YAMLs.

    Overrides may set `defaults` and `colors`; requirements remain the dated
    source reference. Callers can record their departures in project provenance.
    No config is auto-discovered or written back.
    """
    with Path(path or STYLE_PATH).open(encoding="utf-8") as handle:
        style = yaml.safe_load(handle)
    if not isinstance(style, dict) or style.get("schema_version") != 1:
        raise ValueError("Expected a figure-style YAML with schema_version: 1")
    for path in overrides:
        with Path(path).open(encoding="utf-8") as handle:
            layer = yaml.safe_load(handle)
        if not isinstance(layer, dict) or set(layer) - {"defaults", "colors"}:
            raise ValueError(f"Override {path} must contain only defaults and/or colors")
        for section, values in layer.items():
            if not isinstance(values, dict) or set(values) - set(style[section]):
                raise ValueError(f"Unknown or invalid {section} settings in {path}")
        style = _merge(style, layer)
    return style


def apply_style(style=None):
    """Apply configured defaults, failing when the requested font is unavailable.

    The returned font path makes the resolved choice inspectable. Project font
    overrides are allowed but are not automatically Nature-compliant.
    """
    style = style if style is not None else load_style()
    d, c = style["defaults"], style["colors"]
    font_path = font_manager.findfont(
        font_manager.FontProperties(family=[d["font"]]), fallback_to_default=False
    )
    if d["frame"] not in {"open", "boxed", "none"}:
        raise ValueError("frame must be open, boxed, or none")
    mpl.rcParams.update({
        "font.family": "sans-serif", "font.sans-serif": [d["font"]],
        "font.size": d["body_pt"], "text.color": c["text"],
        "axes.labelsize": d["axis_label_pt"], "axes.titlesize": d["body_pt"],
        "axes.labelcolor": c["text"], "axes.edgecolor": c["text"],
        "axes.labelweight": "normal", "axes.titleweight": "normal",
        "figure.titlesize": d["body_pt"], "figure.titleweight": "normal",
        "xtick.labelsize": d["tick_label_pt"], "ytick.labelsize": d["tick_label_pt"],
        "xtick.color": c["text"], "ytick.color": c["text"],
        "legend.fontsize": d["legend_pt"], "legend.title_fontsize": d["legend_pt"],
        "legend.frameon": False, "axes.linewidth": d["axis_line_pt"],
        "xtick.major.width": d["tick_line_pt"], "ytick.major.width": d["tick_line_pt"],
        "xtick.minor.width": d["tick_line_pt"], "ytick.minor.width": d["tick_line_pt"],
        "xtick.direction": "out", "ytick.direction": "out",
        "xtick.major.size": 2.5, "ytick.major.size": 2.5,
        "axes.spines.top": d["frame"] == "boxed",
        "axes.spines.right": d["frame"] == "boxed",
        "axes.spines.left": d["frame"] != "none",
        "axes.spines.bottom": d["frame"] != "none",
        "axes.grid": d["grid"], "lines.linewidth": d["data_line_pt"],
        "lines.markersize": d["marker_pt"],
        "axes.prop_cycle": mpl.cycler(color=c["categorical"]), "image.cmap": c["sequential"],
        "figure.facecolor": c["background"], "axes.facecolor": c["background"],
        "figure.dpi": d["display_dpi"], "savefig.dpi": d["raster_dpi"],
        "savefig.bbox": None, "savefig.facecolor": c["background"],
        "savefig.transparent": False, "pdf.fonttype": d["pdf_fonttype"],
        "ps.fonttype": d["pdf_fonttype"], "svg.fonttype": "none",
        "pdf.use14corefonts": False, "ps.useafm": False, "text.usetex": False,
        "mathtext.fontset": "custom", "mathtext.rm": d["font"],
        "mathtext.it": f"{d['font']}:italic", "mathtext.bf": f"{d['font']}:bold",
    })
    return font_path


def figsize_mm(width, height):
    """Return inches for an explicit physical canvas; no inferred aspect ratio."""
    if width <= 0 or height <= 0:
        raise ValueError("Figure dimensions must be positive")
    return width / 25.4, height / 25.4


def entity_colors(labels, *, style=None):
    """Return a label→hex mapping; reject undefined entities or hue recycling."""
    style = style if style is not None else load_style()
    labels = list(dict.fromkeys(labels))
    configured = style["colors"]["entities"]
    if configured:
        missing = set(labels) - set(configured)
        if missing:
            raise ValueError(f"Entities missing from color mapping: {sorted(missing)}")
        return {label: configured[label] for label in labels}
    palette = style["colors"]["categorical"]
    if len(labels) > len(palette):
        raise ValueError("Too many categories: provide a mapping, facets, or grouping")
    return dict(zip(labels, palette))


def panel_label(ax, letter, *, style=None, xy=(-0.12, 1.04)):
    """Add an 8 pt lowercase Nature panel label; reserve space and inspect it."""
    style = style if style is not None else load_style()
    if len(letter) != 1 or not letter.isascii() or not letter.isalpha():
        raise ValueError("Panel letter must be one ASCII alphabetic character")
    return ax.text(*xy, letter.lower(), transform=ax.transAxes,
                   fontsize=style["defaults"]["panel_label_pt"], weight="bold",
                   color=style["colors"]["text"], ha="left", va="bottom",
                   gid="figure-style-panel-label")


def validate_figure(fig, *, style=None):
    """Return live-figure size/font/bounds errors, not scientific or PDF validity.

    Does not detect all overlaps, raster sampling quality, or embedded font type.
    Inspect the actual saved vector file as well as the preview.
    """
    style = style if style is not None else load_style()
    requirements = style["requirements"]
    errors = []
    width, height = fig.get_size_inches() * 25.4
    if not any(abs(width - w) <= 0.1 for w in requirements["widths_mm"]):
        errors.append(f"Width {width:.2f} mm is outside this preset's standard widths")
    if height > requirements["max_height_mm"] + 0.1:
        errors.append(f"Height {height:.2f} mm exceeds the main-figure allocation")
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    low, high = requirements["ordinary_text_pt"]
    hidden = set()
    for ax in fig.axes:
        if not ax.get_visible():
            hidden.update(ax.findobj(match=Text))
        for axis, limits in ((ax.xaxis, ax.get_xlim()), (ax.yaxis, ax.get_ylim())):
            axis_hidden = not ax.axison or not axis.get_visible()
            if axis_hidden:
                hidden.update((axis.label, axis.get_offset_text()))
            lower, upper = sorted(limits)
            tolerance = max(1, abs(lower), abs(upper)) * 1e-10
            for tick in (*axis.get_major_ticks(), *axis.get_minor_ticks()):
                # Matplotlib retains visible Text objects for ticks beyond the
                # view interval, but the axis renderer does not draw them.
                if axis_hidden or not lower - tolerance <= tick.get_loc() <= upper + tolerance:
                    hidden.update((tick.label1, tick.label2))
    for text in fig.findobj(match=Text):
        if text in hidden or not text.get_visible() or not text.get_text().strip():
            continue
        # Artists on hidden axes and tick-label sides do not enter the export.
        if text.axes is not None and not text.axes.get_visible():
            continue
        label = text.get_text()[:45]
        panel = text.get_gid() == "figure-style-panel-label"
        size = text.get_fontsize()
        if panel:
            if abs(size - requirements["panel_label_pt"]) > 0.01:
                errors.append(f"Panel label {label!r} must be 8 pt")
        elif not low <= size <= high:
            errors.append(f"Text {label!r} is {size:g} pt; ordinary type must be {low}–{high}")
        try:
            font_path = font_manager.findfont(text.get_fontproperties(), fallback_to_default=False)
            family = font_manager.FontProperties(fname=font_path).get_name()
            if family not in requirements["font_families"]:
                errors.append(f"Text {label!r} resolves to {family}, outside the preset fonts")
        except ValueError as exc:
            errors.append(f"Text {label!r} font unavailable: {exc}")
        box = text.get_window_extent(renderer)
        if box.x0 < -1 or box.y0 < -1 or box.x1 > fig.bbox.width + 1 or box.y1 > fig.bbox.height + 1:
            errors.append(f"Text {label!r} extends outside the canvas")
    return errors


def save_figure(fig, path, *, style=None, formats=None, check=True):
    """Save exact-canvas files, create destination parents, propagate failures.

    Validation occurs before any save. On a later write failure, previously
    written formats may remain; the exception means the export is incomplete.
    `check=False` permits a documented draft or project deviation, not a claim
    of Nature compliance. No raster DPI reduction is applied inside vector files.
    """
    style = style if style is not None else load_style()
    formats = list(style["defaults"]["formats"] if formats is None else formats)
    allowed = {"pdf", "svg", "png", "tiff"}
    if not formats or any(fmt not in allowed for fmt in formats):
        raise ValueError(f"Choose one or more formats from {sorted(allowed)}")
    if check:
        errors = validate_figure(fig, style=style)
        if errors:
            raise ValueError("Figure checks failed:\n" + "\n".join(errors))
    path = Path(path)
    base = path.with_suffix("") if path.suffix.lstrip(".").lower() in allowed else path
    base.parent.mkdir(parents=True, exist_ok=True)
    outputs = []
    # rc_context defeats a stale global 'tight' crop even when bbox_inches=None.
    with mpl.rc_context({"savefig.bbox": None, "pdf.fonttype": 42,
                         "pdf.use14corefonts": False, "svg.fonttype": "none"}):
        for fmt in formats:
            destination = Path(f"{base}.{fmt}")
            fig.savefig(destination, format=fmt, bbox_inches=None,
                        dpi=style["defaults"]["raster_dpi"],
                        facecolor=style["colors"]["background"], transparent=False)
            if not destination.is_file() or destination.stat().st_size == 0:
                raise OSError(f"Export missing or empty: {destination}")
            outputs.append(destination.resolve())
    return outputs

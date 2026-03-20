#!/usr/bin/env python3
"""
FACS Gating Viz Style
Parse FCS files and produce publication-ready flow cytometry gating plots.
Supports scatter, density, and contour plot styles.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional, Tuple

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# FCS parsing helpers
# ---------------------------------------------------------------------------

def _try_fcsparser(fcs_path: str, x_channel: str, y_channel: str) -> Tuple[np.ndarray, np.ndarray, str, str]:
    """Parse FCS file with fcsparser (FCS 2.0-3.1)."""
    import fcsparser  # type: ignore
    meta, data = fcsparser.parse(fcs_path, reformat_meta=True)
    channels = list(data.columns)
    x_col = _resolve_channel(channels, x_channel)
    y_col = _resolve_channel(channels, y_channel)
    return data[x_col].values, data[y_col].values, x_col, y_col


def _try_flowio(fcs_path: str, x_channel: str, y_channel: str) -> Tuple[np.ndarray, np.ndarray, str, str]:
    """Parse FCS file with flowio (FCS 3.0+)."""
    import flowio  # type: ignore
    fcs = flowio.FlowData(fcs_path)
    n_events = fcs.event_count
    n_channels = fcs.channel_count
    raw = np.reshape(list(fcs.events), (n_events, n_channels))
    channels = [fcs.channels[str(i + 1)]["PnN"] for i in range(n_channels)]
    x_col = _resolve_channel(channels, x_channel)
    y_col = _resolve_channel(channels, y_channel)
    xi = channels.index(x_col)
    yi = channels.index(y_col)
    return raw[:, xi], raw[:, yi], x_col, y_col


def _resolve_channel(channels: list, requested: str) -> str:
    """Return the best matching channel name, or fall back to first channel."""
    if requested in channels:
        return requested
    # Case-insensitive match
    for ch in channels:
        if ch.lower() == requested.lower():
            return ch
    # Partial match
    for ch in channels:
        if requested.lower() in ch.lower():
            return ch
    # Fallback: warn and use first channel
    print(
        f"Warning: Channel '{requested}' not found. "
        f"Available: {channels}. Defaulting to '{channels[0]}'.",
        file=sys.stderr,
    )
    return channels[0]


def parse_fcs(fcs_path: str, x_channel: str, y_channel: str) -> Tuple[np.ndarray, np.ndarray, str, str]:
    """Auto-detect and parse FCS file using fcsparser or flowio."""
    errors = []
    for parser_fn in (_try_fcsparser, _try_flowio):
        try:
            return parser_fn(fcs_path, x_channel, y_channel)
        except ImportError as e:
            errors.append(str(e))
            continue
        except Exception as e:
            errors.append(str(e))
            continue

    print(
        "Error: Could not parse FCS file. Install fcsparser or flowio.\n"
        + "\n".join(errors),
        file=sys.stderr,
    )
    sys.exit(1)


# ---------------------------------------------------------------------------
# Demo data generator
# ---------------------------------------------------------------------------

def generate_demo_data() -> Tuple[np.ndarray, np.ndarray, str, str]:
    """Generate synthetic FSC/SSC data with two populations (1000 events each)."""
    rng = np.random.default_rng(42)
    # Population 1: lymphocytes (low FSC, low SSC)
    pop1_x = rng.normal(2e5, 3e4, 1000)
    pop1_y = rng.normal(5e4, 1e4, 1000)
    # Population 2: monocytes (higher FSC, higher SSC)
    pop2_x = rng.normal(4e5, 4e4, 1000)
    pop2_y = rng.normal(2e5, 3e4, 1000)
    x = np.concatenate([pop1_x, pop2_x])
    y = np.concatenate([pop1_y, pop2_y])
    return x, y, "FSC-A", "SSC-A"


# ---------------------------------------------------------------------------
# Plot functions
# ---------------------------------------------------------------------------

def plot_scatter(ax: plt.Axes, x: np.ndarray, y: np.ndarray, x_label: str, y_label: str) -> None:
    ax.scatter(x, y, s=1, alpha=0.3, color="#2166ac", rasterized=True)
    ax.set_xlabel(x_label, fontsize=11)
    ax.set_ylabel(y_label, fontsize=11)
    ax.set_title(f"{x_label} vs {y_label} — Scatter", fontsize=12)


def plot_density(ax: plt.Axes, x: np.ndarray, y: np.ndarray, x_label: str, y_label: str, fig: plt.Figure) -> None:
    from scipy.stats import gaussian_kde  # type: ignore
    xy = np.vstack([x, y])
    try:
        kde = gaussian_kde(xy)
        xmin, xmax = x.min(), x.max()
        ymin, ymax = y.min(), y.max()
        xi, yi = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
        zi = kde(np.vstack([xi.ravel(), yi.ravel()])).reshape(xi.shape)
        pcm = ax.pcolormesh(xi, yi, zi, cmap="Blues", shading="auto")
        fig.colorbar(pcm, ax=ax, label="Density")
    except Exception:
        # Fallback to 2D histogram if KDE fails
        h, xedges, yedges = np.histogram2d(x, y, bins=80)
        pcm = ax.pcolormesh(xedges, yedges, h.T, cmap="Blues")
        fig.colorbar(pcm, ax=ax, label="Count")
    ax.set_xlabel(x_label, fontsize=11)
    ax.set_ylabel(y_label, fontsize=11)
    ax.set_title(f"{x_label} vs {y_label} — Density", fontsize=12)


def plot_contour(ax: plt.Axes, x: np.ndarray, y: np.ndarray, x_label: str, y_label: str) -> None:
    h, xedges, yedges = np.histogram2d(x, y, bins=80)
    xc = (xedges[:-1] + xedges[1:]) / 2
    yc = (yedges[:-1] + yedges[1:]) / 2
    ax.contourf(xc, yc, h.T, levels=10, cmap="Blues", alpha=0.7)
    ax.contour(xc, yc, h.T, levels=10, colors="navy", linewidths=0.5, alpha=0.6)
    ax.set_xlabel(x_label, fontsize=11)
    ax.set_ylabel(y_label, fontsize=11)
    ax.set_title(f"{x_label} vs {y_label} — Contour", fontsize=12)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="FACS Gating Viz Style — publication-ready flow cytometry plots"
    )
    parser.add_argument("--input", "-i", default=None, help="FCS file path")
    parser.add_argument("--output", "-o", default="output.png", help="Output plot path (default: output.png)")
    parser.add_argument("--x-channel", default="FSC-A", help="X axis channel (default: FSC-A)")
    parser.add_argument("--y-channel", default="SSC-A", help="Y axis channel (default: SSC-A)")
    parser.add_argument(
        "--style",
        "-s",
        default="scatter",
        choices=["scatter", "density", "contour"],
        help="Plot style: scatter, density, contour (default: scatter)",
    )
    parser.add_argument("--demo", action="store_true", help="Generate synthetic demo data — no FCS file required")
    # Legacy alias kept for backward compat
    parser.add_argument("--data", "-d", default=None, help=argparse.SUPPRESS)
    args = parser.parse_args()

    # Resolve input path (support both --input and legacy --data)
    input_path: Optional[str] = args.input or args.data

    if not args.demo:
        if not input_path:
            print("Error: --input is required unless --demo is used.", file=sys.stderr)
            sys.exit(1)
        if not os.path.exists(input_path):
            print(f"Error: File not found: {input_path}", file=sys.stderr)
            sys.exit(1)

    # Load data
    if args.demo:
        x, y, x_label, y_label = generate_demo_data()
    else:
        x, y, x_label, y_label = parse_fcs(str(input_path), args.x_channel, args.y_channel)

    if len(x) == 0:
        print("Error: FCS file contains 0 events.", file=sys.stderr)
        sys.exit(1)

    # Plot
    fig, ax = plt.subplots(figsize=(7, 6))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#f8f8f8")
    for spine in ax.spines.values():
        spine.set_linewidth(0.8)
        spine.set_color("#cccccc")
    ax.tick_params(labelsize=9)

    style = args.style
    if style == "scatter":
        plot_scatter(ax, x, y, x_label, y_label)
    elif style == "density":
        plot_density(ax, x, y, x_label, y_label, fig)
    elif style == "contour":
        plot_contour(ax, x, y, x_label, y_label)

    n_events = len(x)
    ax.text(
        0.98, 0.02,
        f"n = {n_events:,}",
        transform=ax.transAxes,
        ha="right", va="bottom",
        fontsize=8, color="#555555",
    )

    plt.tight_layout()
    plt.savefig(args.output, dpi=150, bbox_inches="tight")
    plt.close()
    print(args.output)


if __name__ == "__main__":
    main()

"""
BDF to MNE (FIF) conversion app for Brainlife.io

Converts BioSemi BDF raw EEG/MEG files to MNE FIF format.
Generates QC plots: raw trace, PSD, events, channel layout.

Inputs:  raw BDF file
Outputs: out_dir/raw.fif, out_report/report.html, product.json
"""

# Copyright (c) 2026 brainlife.io

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'brainlife_utils'))

import mne
import numpy as np
import matplotlib.pyplot as plt

from brainlife_utils import (
    load_config,
    setup_matplotlib_backend,
    ensure_output_dirs,
    create_product_json,
    add_info_to_product,
    add_image_to_product,
    add_raw_info_to_product,
)

setup_matplotlib_backend()
config = load_config()
ensure_output_dirs('out_dir', 'out_figs', 'out_report')

# ── Config params ─────────────────────────────────────────────────────────────
bdf_file = config.get('bdf') or config.get('eeg') or config.get('meg')
stim_ch  = config.get('stim_channel') or 'Status'

if not bdf_file or not os.path.exists(bdf_file):
    raise FileNotFoundError(f"BDF file not found: {bdf_file!r}. Set 'bdf' in config.json.")

# ── Load BDF ──────────────────────────────────────────────────────────────────
print(f"Loading BDF: {bdf_file}")
raw = mne.io.read_raw_bdf(bdf_file, preload=True, verbose=True)

print(f"  {len(raw.ch_names)} channels, {raw.info['sfreq']:.1f} Hz, {raw.times[-1]:.1f} s")

# ── Detect events ─────────────────────────────────────────────────────────────
events     = None
events_msg = "No events found"

stim_picks = mne.pick_types(raw.info, stim=True)
if len(stim_picks) > 0:
    try:
        events = mne.find_events(raw, stim_channel=stim_ch, verbose=True)
        if len(events) > 0:
            n_unique   = len(np.unique(events[:, 2]))
            events_msg = f"{len(events)} events, {n_unique} unique IDs: {sorted(np.unique(events[:, 2]).tolist())}"
            print(f"  Events: {events_msg}")
    except Exception as e:
        events_msg = f"Event detection failed: {e}"
        print(f"  Warning: {events_msg}")
else:
    events_msg = "No stim channel found"
    print(f"  {events_msg}")

# ── Save FIF ──────────────────────────────────────────────────────────────────
out_fif = os.path.join('out_dir', 'raw.fif')
raw.save(out_fif, overwrite=True)
print(f"Saved: {out_fif}")

# ── MNE Report ────────────────────────────────────────────────────────────────
report = mne.Report(title='BDF → FIF Conversion Report')

# ── Plot 1: Raw trace (first 20 s) ───────────────────────────────────────────
raw_path = None
try:
    t_plot  = min(20.0, raw.times[-1])
    fig_raw = raw.plot(duration=t_plot, n_channels=min(30, len(raw.ch_names)),
                       scalings='auto', show=False,
                       title=f'Raw trace (first {t_plot:.0f} s)')
    raw_path = os.path.join('out_figs', 'raw_trace.png')
    fig_raw.savefig(raw_path, dpi=150, bbox_inches='tight')
    plt.close(fig_raw)
    report.add_image(raw_path, title='Raw Trace')
except Exception as e:
    print(f"Could not plot raw trace: {e}")

# ── Plot 2: PSD ───────────────────────────────────────────────────────────────
psd_path = None
try:
    fig_psd  = raw.plot_psd(fmax=min(100.0, raw.info['sfreq'] / 2 - 1), show=False)
    psd_path = os.path.join('out_figs', 'psd.png')
    fig_psd.savefig(psd_path, dpi=150, bbox_inches='tight')
    plt.close(fig_psd)
    report.add_image(psd_path, title='Power Spectral Density')
except Exception as e:
    print(f"Could not plot PSD: {e}")

# ── Plot 3: Sensor layout ─────────────────────────────────────────────────────
layout_path = None
if len(mne.pick_types(raw.info, eeg=True, meg=False)) > 0:
    try:
        fig_sens    = mne.viz.plot_sensors(raw.info, show_names=False, show=False)
        layout_path = os.path.join('out_figs', 'sensor_layout.png')
        fig_sens.savefig(layout_path, dpi=150, bbox_inches='tight')
        plt.close(fig_sens)
        report.add_image(layout_path, title='Sensor Layout')
    except Exception as e:
        print(f"Could not plot sensor layout: {e}")

# ── Plot 4: Events ────────────────────────────────────────────────────────────
events_path = None
if events is not None and len(events) > 0:
    try:
        event_ids    = {str(v): v for v in np.unique(events[:, 2])}
        fig_ev       = mne.viz.plot_events(
            events, sfreq=raw.info['sfreq'],
            event_id=event_ids if len(event_ids) <= 20 else None,
            show=False)
        events_path  = os.path.join('out_figs', 'events.png')
        fig_ev.savefig(events_path, dpi=150, bbox_inches='tight')
        plt.close(fig_ev)
        report.add_image(events_path, title='Events')
    except Exception as e:
        print(f"Could not plot events: {e}")

# ── Save HTML report ──────────────────────────────────────────────────────────
report.save(os.path.join('out_report', 'report.html'), overwrite=True)

# ── product.json ──────────────────────────────────────────────────────────────
product_items = []

add_info_to_product(product_items, f"File: {os.path.basename(bdf_file)}")
add_raw_info_to_product(product_items, raw)
add_info_to_product(product_items, f"Events: {events_msg}")

for label, path in [
    ('Raw Trace',     raw_path),
    ('PSD',           psd_path),
    ('Sensor Layout', layout_path),
    ('Events',        events_path),
]:
    if path and os.path.exists(path):
        add_image_to_product(product_items, label, filepath=path)

create_product_json(product_items)
print("Done.")

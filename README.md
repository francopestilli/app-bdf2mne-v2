# app-bdf2mne

[![Brainlife.io](https://img.shields.io/badge/brainlife.io-app-blue)](https://brainlife.io)

## Description

Converts BioSemi BDF raw EEG/MEG files to MNE-Python FIF format for use in downstream Brainlife.io apps.

## Inputs

| File | Description |
|------|-------------|
| `bdf` | Raw BDF file from BioSemi ActiveTwo system |

## Outputs

| File | Description |
|------|-------------|
| `out_dir/raw.fif` | Raw data in MNE FIF format |
| `out_report/report.html` | HTML QC report with plots |
| `out_figs/raw_trace.png` | Raw signal trace (first 20 s) |
| `out_figs/psd.png` | Power spectral density |
| `out_figs/sensor_layout.png` | Electrode positions (if available) |
| `out_figs/events.png` | Event timing plot (if stim channel found) |
| `product.json` | Brainlife.io UI metadata (runtime-generated) |

## Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `bdf` | string | `""` | Path to input BDF file |
| `stim_channel` | string | `"Status"` | Stimulus channel name for event detection |
| `preload` | boolean | `false` | Load data into memory on open (unused, always loaded) |

## Usage

Set `bdf` in `config.json` to the path of your BDF file, then run:

```bash
singularity exec docker://brainlife/mne:1.8.0 python3 main.py
```

## Technical Details

- Reads BDF using `mne.io.read_raw_bdf()`
- Saves to FIF using `raw.save()` with `overwrite=True`
- Event detection via `mne.find_events()` on the `Status` stim channel (BioSemi default)
- PSD computed up to 100 Hz or Nyquist − 1, whichever is lower
- Sensor layout plot generated if EEG channel positions are present

## Authors

- Brainlife.io Team

## Citations

Gramfort, A. et al. (2013). MEG and EEG data analysis with MNE-Python. *Frontiers in Neuroscience*, 7, 267.

## Funding

Supported by NIH grants R01EB020407 and R01MH116922.

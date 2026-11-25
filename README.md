# app-bdf2mne

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Converts a BioSemi BDF EEG recording to MNE-Python Raw (.fif) with mne.io.read_raw_bdf, detects events on the stimulus channel and produces raw-trace, PSD, sensor-layout and event QC figures.**

Reads the BDF file with MNE-Python, saves it as raw.fif and, when a stimulus channel is present, finds events on it (Status by default). Adds a raw trace of the first 20 s, a power spectral density up to 100 Hz, electrode layout and event plots to an HTML report and the brainlife product. Use it to bring BioSemi ActiveTwo recordings into brainlife MNE pipelines. The BIDS channels, electrodes and events sidecars of the input are not applied.

| | |
|---|---|
| 📥 **Inputs** | `neuro/eeg/bdf` |
| 📤 **Outputs** | `neuro/meeg/mne/raw` |
| 🐳 **Container** | `brainlife/mne:1.0.2` |
| ⚙️ **Resources** | 1 CPUs · 16 GB memory · 1 h walltime |
| 🔗 **Run it** | [doi.org/10.25663/brainlife.app.895](https://doi.org/10.25663/brainlife.app.895) |

#### 📥 Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `bdf` | `neuro/eeg/bdf` | yes | BioSemi BDF recording with optional BIDS sidecars (channels, electrodes, coordsystem, events). |

#### 📤 Outputs

| Output | Datatype | Description |
|---|---|---|
| `out_dir` | `neuro/meeg/mne/raw` | Raw EEG/MEG data converted from BDF to MNE FIF format |

<details>
<summary><b>⚙️ Parameters</b> (1)</summary>

| Parameter | Type | Default | Description |
|---|---|---|---|
| `stim_channel` | string | `Status` | Name of the stimulus channel used for event detection with mne.find_events; empty means auto-detect (BioSemi default Status). |

</details>

📚 **References used by this App:**
- Gramfort A. et al. MEG and EEG data analysis with MNE-Python. Frontiers in Neuroscience 7:267 (2013). [doi:10.3389/fnins.2013.00267](https://doi.org/10.3389/fnins.2013.00267)

<!-- brainlife-app:end -->

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

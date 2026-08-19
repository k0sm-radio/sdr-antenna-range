# Pluto Antenna Range

A GNU Radio flowgraph for measuring antenna performance using the ADALM Pluto SDR with audio feedback.

## Description

This flowgraph receives signals from an ADALM Pluto SDR and provides real-time signal strength measurements with both visual and audio feedback. The audio tone frequency changes based on signal strength, making it useful for antenna alignment and range testing.

## Features

- Real-time FFT spectrum analysis for aid in tuning the signal source
- Signal strength measurement in dB
- Audio tone feedback with logarithmic frequency mapping
  - 200 Hz at -10 dB (or lower)
  - 5000 Hz at +40 dB (or higher)
  - Exponential frequency scaling for better sensitivity at low signal levels
- Phase-continuous audio generation (no clicks or pops)
- Smooth frequency transitions (25ms interpolation time by default)
- Adjustable reference antenna calibration
- Qt GUI with spectrum display and numerical readout

## Requirements

- GNU Radio 3.10+ (with the `gr-iio` module)
- ADALM Pluto SDR connected via USB (clones should work)
- One of: Ubuntu 24.04 (or similar Linux), or macOS 12 (Monterey) or later, Apple Silicon or Intel

### Ubuntu / Linux

```bash
sudo apt install gnuradio libgnuradio-iio3.10.9t64 libiio-utils python3-libiio libad9361-0
```

### macOS

macOS has no single-command package equivalent to `apt install`. Two options, in order of preference:

**Option A - conda-forge / radioconda (recommended).** This is the only macOS path that's both current and pre-built for both Intel and Apple Silicon Macs. `gr-iio` ships as the `gnuradio-iio` conda-forge package.

```bash
# If you don't already have conda/mamba, install Miniforge first:
#   https://github.com/conda-forge/miniforge
conda create -n gnuradio -c conda-forge gnuradio gnuradio-iio
conda activate gnuradio
```

On Apple Silicon, make sure your conda installation is running natively as `osx-arm64` (the default with a current Miniforge install) rather than under Rosetta - it's faster and avoids a class of subtle library-mismatch problems. Check with:

```bash
conda info | grep platform
```

You can also use [radioconda](https://github.com/ryanvolz/radioconda), a ready-made GNU Radio conda distribution, instead of building the environment up from conda-forge by hand.

**Option B - Homebrew (alternative).** Homebrew's core `gnuradio` formula does **not** include `gr-iio` (the module that talks to the Pluto):

```bash
brew install gnuradio
```

You'll then need `gr-iio` separately, either via the community tap [`ttrftech/homebrew-adalm-pluto`](https://github.com/ttrftech/homebrew-adalm-pluto) (last verified against macOS Sierra 10.12 - treat as unmaintained/experimental on current macOS) or by building `libiio`, `libad9361-iio`, and `gr-iio` from source against your Homebrew GNU Radio install. Expect more troubleshooting on this path than with Option A.

## Hardware Setup

1. Connect ADALM Pluto to USB.
2. On macOS, confirm the Pluto's Ethernet compatibility mode is **USB CDC-NCM** (the default on current firmware). The device will then show up in System Settings -> Network, in addition to appearing as a USB serial port and a mass-storage volume. See Analog Devices' [Mac OS X driver notes](https://wiki.analog.com/university/tools/pluto/drivers/osx) if it doesn't appear automatically.
3. Verify connection: `ping 192.168.2.1`
4. Check IIO device: `iio_info -n 192.168.2.1`

## Usage

### Running the flowgraph

The easiest way to run the flowgraph is to use the provided script:

```bash
./run.sh
```

Or manually:
```bash
grcc pluto-antenna-range.grc && python3 fix_msg_connection.py && python3 pluto.py
```

### Using GNU Radio Companion

```bash
gnuradio-companion pluto-antenna-range.grc
```

After editing and saving, regenerate the Python file:
```bash
grcc pluto-antenna-range.grc
python3 fix_msg_connection.py
python3 pluto.py
```

## Configuration

### Frequency Settings
- Default LO frequency: 2073.62 MHz (this is near 10.368 GHz using a 5x subharmonic) for 10 GHz operation.  Other freuqnecies should be tuned directly through the GUI control

### Audio Feedback
- **Frequency mapping**: Logarithmic (exponential frequency vs. dB)
  - Minimum: 200 Hz at -10 dB or lower
  - Maximum: 5000 Hz at +40 dB or higher
  - Formula: `freq = 200 * 25^((dB + 10) / 50)`
- **Interpolation time**: 25ms (adjustable via `interpolation_samples` parameter)
  - Provides smooth frequency transitions without clicks
  - Can be reduced for faster response or increased for smoother transitions
- **Why logarithmic?**
  - Better sensitivity at low signal levels
  - Matches human pitch perception
  - Easier to distinguish small changes in weak signals

### Signal Processing
- Sample rate: 500 kHz
- FFT size: 512
- Decimation: 4
- Moving average: 100 samples for amplitude estimation

## Files

- `pluto-antenna-range.grc` - Main GNU Radio Companion flowgraph
- `pluto.py` - Generated Python script (auto-generated, do not edit directly)
- `pluto_audio_tone_gen_0.py` - Audio tone generator block (auto-generated from GRC)
- `pluto_epy_block_0.py` - Vector sum block (auto-generated from GRC)
- `pluto_stream_to_msg_0.py` - Stream to message converter (auto-generated from GRC)
- `fix_msg_connection.py` - Adds the async message connection to generated `pluto.py` (cross-platform: macOS, Linux, Windows)
- `fix_msg_connection.sh` - Thin compatibility shim that calls `fix_msg_connection.py`, kept for anything still invoking the old script name
- `run.sh` - Convenience script to run the flowgraph
- `pluto.block.yml` - Block definition file

## Troubleshooting

### Pluto not detected

**Linux:**
```bash
# Check USB connection
lsusb | grep -i analog

# Check network interface
ip addr show | grep 192.168.2

# Test IIO connection
iio_info -n 192.168.2.1
```

**macOS:**
```bash
# Check USB connection
system_profiler SPUSBDataType | grep -i -A3 analog

# Check network interface (interface name varies - grep across all of them)
ifconfig | grep -B4 192.168.2

# Test IIO connection
iio_info -n 192.168.2.1
```

### No audio output
- Check system audio settings
- Verify audio device is not muted
- Check that messages are being received (look for "Received dB" in terminal output)
- If using WSL, ensure audio is properly configured (this is often a pain point)
- On macOS, GNU Radio's audio sink uses CoreAudio automatically - if you hear nothing, check System Settings -> Sound for the correct output device and confirm your GNU Radio build (conda-forge/radioconda builds do) includes audio support

### Message connection errors
If you see "connect called on already connected edge", regenerate the flowgraph:
```bash
grcc pluto-antenna-range.grc
python3 fix_msg_connection.py
python3 pluto.py
```

## Notes

- The `fix_msg_connection.py` script is required because GNU Radio Companion doesn't properly generate message connections for embedded Python blocks
- Audio tone changes are smoothed over 25ms to prevent clicking
- The flowgraph uses a throttle block which may cause warnings - this is expected for audio output synchronization

## Revision History

### v1.1 - 2026-08-19 - macOS compatibility

*Rus Healy, K2UA*

- Replaced `fix_msg_connection.sh`'s `sed -i` patch logic with `fix_msg_connection.py`, a plain Python 3 script that behaves identically on macOS (BSD sed), Linux (GNU sed), and Windows. The old GNU-sed-only `-i` syntax would error or silently misbehave under macOS's BSD sed.
- Fixed `fix_msg_connection.sh` and `pluto.block.yml`, both of which had the original author's absolute Ubuntu path (`/home/aflowers/...`) hardcoded in - broken on any machine but the original author's, not just macOS. `fix_msg_connection.sh` is now a thin shim that resolves its own directory and calls `fix_msg_connection.py`; `pluto.block.yml`'s `documentation:`/`grc_source:` fields now use relative paths.
- Added a shebang and `set -e` to `run.sh`, and made it `cd` to its own directory first so it works regardless of the caller's working directory.
- Documented a macOS install path: conda-forge/radioconda (recommended, current, prebuilt for both Intel and Apple Silicon) and Homebrew (alternative, requires a community tap or a from-source build of `gr-iio` since it isn't in Homebrew core).
- Documented macOS hardware setup (USB CDC-NCM Ethernet compatibility mode) and macOS-specific troubleshooting commands (`ifconfig`/`system_profiler` in place of `ip addr`/`lsusb`).
- No changes to the flowgraph, embedded Python DSP blocks, or signal processing - this release is packaging/tooling/documentation only.

### v1.0 - Baseline

*Andrew T. Flowers, K0SM*

- Initial Ubuntu 24.04 / GNU Radio 3.10 release of the Pluto Antenna Range flowgraph.

## License

(MIT)

Copyright 2026 Andrew T. Flowers, K0SM

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

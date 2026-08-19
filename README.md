# Pluto Antenna Range

A GNU Radio flowgraph for measuring antenna performance using the ADALM Pluto SDR with audio feedback.

## Description

This flowgraph receives signals from an ADALM Pluto SDR and provides real-time signal strength measurements with both visual and audio feedback. The audio tone frequency changes based on signal strength, making it useful for antenna alignment and range testing.

## Features

- Real-time FFT spectrum analysis for aid in tuning the signal source.
- Signal strength measurement in dB
- Audio tone feedback
- Phase-continuous audio generation (no clicks or pops)
- Adjustable reference antenna calibration
- Qt GUI with spectrum display and numerical readout

## Requirements

- Ubuntu 24.04 (or similar)
- GNU Radio 3.10+
- ADALM Pluto SDR connected via USB (clones should work)
- Required packages:
  ```bash
  sudo apt install gnuradio libgnuradio-iio3.10.9t64 libiio-utils python3-libiio libad9361-0
  ```

## Hardware Setup

1. Connect ADALM Pluto to USB
2. Verify connection: `ping 192.168.2.1`
3. Check IIO device: `iio_info -n 192.168.2.1`

## Usage

### Running the flowgraph

The easiest way to run the flowgraph is to use the provided script:

```bash
./run.sh
```

Or manually:
```bash
grcc pluto-antenna-range.grc && ./fix_msg_connection.sh && python3 pluto.py
```

### Using GNU Radio Companion

```bash
gnuradio-companion pluto-antenna-range.grc
```

After editing and saving, regenerate the Python file:
```bash
grcc pluto-antenna-range.grc
./fix_msg_connection.sh
python3 pluto.py
```

## Configuration

### Frequency Settings
- Default LO frequency: 2073.62 MHz (this is near 10.368 GHz using a 5x subharmonic) for 10 GHz operation.  Other freuqnecies should be tuned directly through the GUI control

### Audio Feedback
- Minimum frequency: 200 Hz (at 0 dB or lower)
- Maximum frequency: 5000 Hz (at 40 dB or higher)
- Interpolation time: 25ms (adjustable in `pluto-antenna-range.grc`)

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
- `fix_msg_connection.sh` - Script to add message connections to generated Python
- `run.sh` - Convenience script to run the flowgraph
- `pluto.block.yml` - Block definition file

## Troubleshooting

### Pluto not detected
```bash
# Check USB connection
lsusb | grep -i analog

# Check network interface
ip addr show | grep 192.168.2

# Test IIO connection
iio_info -n 192.168.2.1
```

### No audio output
- Check system audio settings
- Verify audio device is not muted
- Check that messages are being received (look for "Received dB" in terminal output)
- If using WSL, ensure audio is properly configured (this is often a pain point)

### Message connection errors
If you see "connect called on already connected edge", regenerate the flowgraph:
```bash
grcc pluto-antenna-range.grc
./fix_msg_connection.sh
python3 pluto.py
```

## Notes

- The `fix_msg_connection.sh` script is required because GNU Radio Companion doesn't properly generate message connections for embedded Python blocks
- Audio tone changes are smoothed over 25ms to prevent clicking
- The flowgraph uses a throttle block which may cause warnings - this is expected for audio output synchronization

## License

(MIT)

Copyright 2026 Andrew T. Flowers, K0SM

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


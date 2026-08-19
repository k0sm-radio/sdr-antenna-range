"""
Audio Tone Generator Block

Generates a phase-continuous audio tone whose frequency is controlled
by an input dB value. Maps dB range [0, 40] to frequency range [200, 5000] Hz.
"""

import numpy as np
from gnuradio import gr


class blk(gr.interp_block):
    """
    Phase-continuous audio tone generator controlled by dB values.
    
    Input: float stream (dB values at low rate)
    Output: float stream (audio samples at audio_samplerate)
    """
    
    def __init__(self, audio_samplerate=48000, min_freq=200, max_freq=5000, 
                 min_db=0, max_db=40, interpolation_samples=4800):
        """
        Args:
            audio_samplerate: Output sample rate in Hz (default: 48000)
            min_freq: Frequency in Hz for min_db or lower (default: 200)
            max_freq: Frequency in Hz for max_db or higher (default: 5000)
            min_db: Minimum dB value for mapping (default: 0)
            max_db: Maximum dB value for mapping (default: 40)
            interpolation_samples: Number of samples over which to smooth frequency changes (default: 4800 = 100ms at 48kHz)
        """
        gr.interp_block.__init__(
            self,
            name='Audio Tone Generator',
            in_sig=[np.float32],
            out_sig=[np.float32],
            interp=audio_samplerate  # We'll adjust this dynamically
        )
        
        self.audio_samplerate = float(audio_samplerate)
        self.min_freq = float(min_freq)
        self.max_freq = float(max_freq)
        self.min_db = float(min_db)
        self.max_db = float(max_db)
        self.interpolation_samples = int(interpolation_samples)
        
        # Phase accumulator for continuous phase
        self.phase = 0.0
        
        # Current and target frequencies
        self.current_freq = min_freq
        self.target_freq = min_freq
        
        # Interpolation state
        self.interp_counter = 0
        self.freq_step = 0.0
        
    def db_to_freq(self, db_value):
        """Convert dB value to frequency, with clamping."""
        # Clamp dB to valid range
        db_clamped = np.clip(db_value, self.min_db, self.max_db)
        
        # Linear mapping from dB to frequency
        freq = self.min_freq + (db_clamped - self.min_db) * \
               (self.max_freq - self.min_freq) / (self.max_db - self.min_db)
        
        return freq
    
    def work(self, input_items, output_items):
        """
        Generate audio samples with phase-continuous frequency changes.
        """
        in_db = input_items[0]
        out_audio = output_items[0]
        
        # Calculate how many output samples we need per input sample
        samples_per_input = len(out_audio) // len(in_db)
        
        out_idx = 0
        
        for db_value in in_db:
            # Convert dB to target frequency
            new_target_freq = self.db_to_freq(db_value)
            
            # If target frequency changed, set up interpolation
            if abs(new_target_freq - self.target_freq) > 0.1:
                self.target_freq = new_target_freq
                self.interp_counter = self.interpolation_samples
                self.freq_step = (self.target_freq - self.current_freq) / self.interpolation_samples
            
            # Generate audio samples for this input sample
            for _ in range(samples_per_input):
                if out_idx >= len(out_audio):
                    break
                
                # Interpolate frequency if needed
                if self.interp_counter > 0:
                    self.current_freq += self.freq_step
                    self.interp_counter -= 1
                else:
                    self.current_freq = self.target_freq
                
                # Generate sine wave sample
                out_audio[out_idx] = np.sin(2.0 * np.pi * self.phase)
                
                # Update phase accumulator
                self.phase += self.current_freq / self.audio_samplerate
                
                # Keep phase in [0, 1) to prevent overflow
                if self.phase >= 1.0:
                    self.phase -= 1.0
                
                out_idx += 1
        
        return len(out_audio)

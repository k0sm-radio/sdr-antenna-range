import numpy as np
from gnuradio import gr
import pmt


class blk(gr.sync_block):
    """
    Free-running phase-continuous audio tone generator.
    Frequency is controlled asynchronously via message input.
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
        gr.sync_block.__init__(
            self,
            name='Audio Tone Generator',
            in_sig=None,  # No input stream, only message port
            out_sig=[np.float32]
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
        
        # Register message port for receiving dB values
        self.message_port_register_in(pmt.intern("db_in"))
        self.set_msg_handler(pmt.intern("db_in"), self.handle_db_msg)
        
    def handle_db_msg(self, msg):
        """Handle incoming dB value messages."""
        try:
            # Extract the dB value from the message
            db_value = pmt.to_double(msg)
            
            # Convert dB to frequency
            new_target_freq = self.db_to_freq(db_value)
            
            # Debug output
            print(f"Received dB: {db_value:.2f}, Target freq: {new_target_freq:.1f} Hz")
            
            # If target frequency changed significantly, set up interpolation
            if abs(new_target_freq - self.target_freq) > 0.1:
                self.target_freq = new_target_freq
                self.interp_counter = self.interpolation_samples
                if self.interpolation_samples > 0:
                    self.freq_step = (self.target_freq - self.current_freq) / self.interpolation_samples
                else:
                    self.current_freq = self.target_freq
        except Exception as e:
            print(f"Error handling dB message: {e}")
        
    def db_to_freq(self, db_value):
        """Convert dB value to frequency, with clamping."""
        db_clamped = np.clip(db_value, self.min_db, self.max_db)
        freq = self.min_freq + (db_clamped - self.min_db) * \
               (self.max_freq - self.min_freq) / (self.max_db - self.min_db)
        return freq
    
    def work(self, input_items, output_items):
        """
        Generate audio samples continuously with phase-continuous frequency changes.
        """
        out_audio = output_items[0]
        
        # Generate audio samples
        for i in range(len(out_audio)):
            # Interpolate frequency if needed
            if self.interp_counter > 0:
                self.current_freq += self.freq_step
                self.interp_counter -= 1
            else:
                self.current_freq = self.target_freq
            
            # Generate sine wave sample
            out_audio[i] = 0.3 * np.sin(2.0 * np.pi * self.phase)
            
            # Update phase accumulator
            self.phase += self.current_freq / self.audio_samplerate
            
            # Keep phase in [0, 1) to prevent overflow
            if self.phase >= 1.0:
                self.phase -= 1.0
        
        return len(out_audio)

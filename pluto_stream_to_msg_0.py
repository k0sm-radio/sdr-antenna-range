"""
Stream to Message converter
Converts float stream samples to PMT messages
"""

import numpy as np
from gnuradio import gr
import pmt


class blk(gr.sync_block):
    """
    Converts stream samples to messages.
    Decimates the stream and sends every Nth sample as a message.
    """
    
    def __init__(self, decimation=100):
        """
        Args:
            decimation: Send a message every N samples (default: 100)
        """
        gr.sync_block.__init__(
            self,
            name='Stream to Message',
            in_sig=[np.float32],
            out_sig=None
        )
        
        self.decimation = int(decimation)
        self.counter = 0
        
        # Register message output port
        self.message_port_register_out(pmt.intern("msg_out"))
        
    def work(self, input_items, output_items):
        """
        Convert stream samples to messages.
        """
        in_data = input_items[0]
        
        for value in in_data:
            self.counter += 1
            if self.counter >= self.decimation:
                self.counter = 0
                # Send the value as a PMT message
                msg = pmt.from_double(float(value))
                self.message_port_pub(pmt.intern("msg_out"), msg)
                print(f"Stream->Msg: Sent dB value: {value:.2f}")
        
        return len(in_data)

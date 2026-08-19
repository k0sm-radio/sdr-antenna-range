"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr




class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""
    
    def __init__(self, vectorSize=512):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='vector sum',   # will show up in GRC
            in_sig=[(np.float32,vectorSize)],
            out_sig=[(np.float32)]

        )
        self.vectorSize = vectorSize
        self.maxbin = 0;
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        #self.example_param = example_param

    def work(self, input_items, output_items):
        for vectorIndex in range(len(input_items[0])):
            #sum = np.sum(input_items[0][vectorIndex])
            
            maxValue = np.max(input_items[0][vectorIndex])
            maxbin = np.argmax(input_items[0][vectorIndex])

            #
            start = maxbin - 4
            stop = maxbin + 5
            if start < 0:
                start = 0
            if (stop > len(input_items[0][vectorIndex])):
                stop = input_items[0][vectorIndex] -1
            sum = 0
            for i in range(start,stop):
                sum += input_items[0][vectorIndex][i]

            output_items[0][0] = sum
          #  sum = (input_items[0][maxbin-2]) + (input_items[0][maxbin-1]) + (input_items[0][maxbin]) + (input_items[0][maxbin+1]) + (input_items[0][maxbin+2])
            #print(f'{maxbin}  {sum}')
          #  for sampleIndex in range(len(input_items[0][vectorIndex])):
           #     output_items[0][vectorIndex][sampleIndex] = sum
        """example: multiply with constant"""
        #output_items[0][:] = np.sum(input_items)
        #output_items[0][:] = input_items[0] 
        

        return 1 #

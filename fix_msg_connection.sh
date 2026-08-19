#!/bin/bash
# Script to add message connection to generated pluto.py

# Check if the message connection already exists
if grep -q "msg_connect.*stream_to_msg_0.*audio_tone_gen_0" /home/aflowers/Desktop/pluto/pluto.py; then
    echo "Message connection already exists in pluto.py"
else
    # Add the message connection after the stream connections
    sed -i '/self.connect((self.blocks_add_const_vxx_0, 0), (self.stream_to_msg_0, 0))/a\        \n        ##################################################\n        # Asynch Message Connections\n        ##################################################\n        self.msg_connect((self.stream_to_msg_0, '\''msg_out'\''), (self.audio_tone_gen_0, '\''db_in'\''))' /home/aflowers/Desktop/pluto/pluto.py
    echo "Message connection added to pluto.py"
fi

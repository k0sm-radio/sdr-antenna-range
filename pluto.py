#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Pluto Antenna Range
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import audio
from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import iio
import pluto_audio_tone_gen_0 as audio_tone_gen_0  # embedded python block
import pluto_epy_block_0 as epy_block_0  # embedded python block
import pluto_stream_to_msg_0 as stream_to_msg_0  # embedded python block
import sip
import threading



class pluto(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Pluto Antenna Range", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Pluto Antenna Range")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "pluto")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        self._lock = threading.RLock()

        ##################################################
        # Variables
        ##################################################
        self.transition_bw = transition_bw = 1000
        self.sample_rate = sample_rate = 500000
        self.rx_gain = rx_gain = 71
        self.rf_lo_freq = rf_lo_freq = 2073620000
        self.fft_size = fft_size = 512
        self.decimation = decimation = 4
        self.db_ref = db_ref = 0
        self.audio_samplerate = audio_samplerate = 48000
        self.audio_freq = audio_freq = 1000

        ##################################################
        # Blocks
        ##################################################

        self._rx_gain_range = qtgui.Range(0, 71, 1, 71, 200)
        self._rx_gain_win = qtgui.RangeWidget(self._rx_gain_range, self.set_rx_gain, "RX Gain", "counter", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._rx_gain_win, 1, 4, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 5):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._rf_lo_freq_msgdigctl_win = qtgui.MsgDigitalNumberControl(lbl='LO frequency (Hz)', min_freq_hz=70000000, max_freq_hz=6000000000, parent=self, thousands_separator=",", background_color="black", fontColor="white", var_callback=self.set_rf_lo_freq, outputmsgname='rf_lo_freq')
        self._rf_lo_freq_msgdigctl_win.setValue(2073620000)
        self._rf_lo_freq_msgdigctl_win.setReadOnly(False)
        self.rf_lo_freq = self._rf_lo_freq_msgdigctl_win

        self.top_grid_layout.addWidget(self._rf_lo_freq_msgdigctl_win, 1, 1, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._db_ref_range = qtgui.Range(-100, +100, .1, 0, 200)
        self._db_ref_win = qtgui.RangeWidget(self._db_ref_range, self.set_db_ref, "Reference antenna (dB)", "counter", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._db_ref_win, 0, 4, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 5):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.stream_to_msg_0 = stream_to_msg_0.blk(decimation=10)
        self.qtgui_vector_sink_f_0_0_0 = qtgui.vector_sink_f(
            fft_size,
            0,
            .1,
            "Freq",
            "dB",
            "Spectrum",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_0_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_0_0.set_y_axis((-80), 60)
        self.qtgui_vector_sink_f_0_0_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_0_0.enable_grid(True)
        self.qtgui_vector_sink_f_0_0_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_0_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_0_0.set_ref_level(db_ref)


        labels = ["", '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_0_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_0_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_0_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_0_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_vector_sink_f_0_0_0_win, 0, 1, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_VERT,
            1,
            None # parent
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title("dBref")

        labels = ['dB', '', '', '', '',
            '', '', '', '', '']
        units = ['dB', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0.set_min(i, -50)
            self.qtgui_number_sink_0.set_max(i, 50)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_win, 0, 0, 3, 1)
        for r in range(0, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.iio_pluto_source_0 = iio.fmcomms2_source_fc32('ip:192.168.2.1' if 'ip:192.168.2.1' else iio.get_pluto_uri(), [True, True], 32768)
        self.iio_pluto_source_0.set_len_tag_key('packet_len')
        self.iio_pluto_source_0.set_frequency(rf_lo_freq)
        self.iio_pluto_source_0.set_samplerate(sample_rate)
        self.iio_pluto_source_0.set_gain_mode(0, 'manual')
        self.iio_pluto_source_0.set_gain(0, rx_gain)
        self.iio_pluto_source_0.set_quadrature(False)
        self.iio_pluto_source_0.set_rfdc(True)
        self.iio_pluto_source_0.set_bbdc(True)
        self.iio_pluto_source_0.set_filter_params('Auto', '', 0, 0)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(decimation,  firdes.low_pass(1,sample_rate,sample_rate/(4*decimation), transition_bw), 100000, sample_rate)
        self.fft_vxx_0 = fft.fft_vcc(fft_size, True, window.flattop(fft_size), True, 1)
        self.epy_block_0 = epy_block_0.blk(vectorSize=fft_size)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fft_size)
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_float*fft_size)
        self.blocks_nlog10_ff_0_0_0 = blocks.nlog10_ff(10, fft_size, 0)
        self.blocks_nlog10_ff_0_0 = blocks.nlog10_ff(10, 1, 0)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(100, (1/50), 1, fft_size)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(fft_size)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff((-db_ref))
        self.audio_tone_gen_0 = audio_tone_gen_0.blk(audio_samplerate=audio_samplerate, min_freq=200, max_freq=5000, min_db=0, max_db=40, interpolation_samples=2)
        self.audio_sink_0 = audio.sink(audio_samplerate, '', True)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.audio_tone_gen_0, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.stream_to_msg_0, 0))
        
        ##################################################
        # Asynch Message Connections
        ##################################################
        self.msg_connect((self.stream_to_msg_0, 'msg_out'), (self.audio_tone_gen_0, 'db_in'))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_nlog10_ff_0_0_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.epy_block_0, 0))
        self.connect((self.blocks_nlog10_ff_0_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_nlog10_ff_0_0_0, 0), (self.blocks_null_sink_0_0, 0))
        self.connect((self.blocks_nlog10_ff_0_0_0, 0), (self.qtgui_vector_sink_f_0_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.epy_block_0, 0), (self.blocks_nlog10_ff_0_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "pluto")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_transition_bw(self):
        return self.transition_bw

    def set_transition_bw(self, transition_bw):
        with self._lock:
            self.transition_bw = transition_bw
            self.freq_xlating_fir_filter_xxx_0.set_taps( firdes.low_pass(1,self.sample_rate,self.sample_rate/(4*self.decimation), self.transition_bw))

    def get_sample_rate(self):
        return self.sample_rate

    def set_sample_rate(self, sample_rate):
        with self._lock:
            self.sample_rate = sample_rate
            self.freq_xlating_fir_filter_xxx_0.set_taps( firdes.low_pass(1,self.sample_rate,self.sample_rate/(4*self.decimation), self.transition_bw))
            self.iio_pluto_source_0.set_samplerate(self.sample_rate)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        with self._lock:
            self.rx_gain = rx_gain
            self.iio_pluto_source_0.set_gain(0, self.rx_gain)

    def get_rf_lo_freq(self):
        return self.rf_lo_freq

    def set_rf_lo_freq(self, rf_lo_freq):
        with self._lock:
            self.rf_lo_freq = rf_lo_freq
            self.iio_pluto_source_0.set_frequency(self.rf_lo_freq)

    def get_fft_size(self):
        return self.fft_size

    def set_fft_size(self, fft_size):
        with self._lock:
            self.fft_size = fft_size
            self.epy_block_0.vectorSize = self.fft_size

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        with self._lock:
            self.decimation = decimation
            self.freq_xlating_fir_filter_xxx_0.set_taps( firdes.low_pass(1,self.sample_rate,self.sample_rate/(4*self.decimation), self.transition_bw))

    def get_db_ref(self):
        return self.db_ref

    def set_db_ref(self, db_ref):
        with self._lock:
            self.db_ref = db_ref
            self.blocks_add_const_vxx_0.set_k((-self.db_ref))
            self.qtgui_vector_sink_f_0_0_0.set_ref_level(self.db_ref)

    def get_audio_samplerate(self):
        return self.audio_samplerate

    def set_audio_samplerate(self, audio_samplerate):
        with self._lock:
            self.audio_samplerate = audio_samplerate
            self.audio_tone_gen_0.audio_samplerate = self.audio_samplerate

    def get_audio_freq(self):
        return self.audio_freq

    def set_audio_freq(self, audio_freq):
        with self._lock:
            self.audio_freq = audio_freq




def main(top_block_cls=pluto, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()

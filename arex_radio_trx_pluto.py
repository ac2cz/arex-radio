#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: AREX Radio Demonstration
# Author: Chris Thompson VE2TCP
# Description: Based on the Langstone radio by G4EML
# GNU Radio version: 3.10.5.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import iio
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore



from gnuradio import qtgui

class arex_radio_trx_pluto(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "AREX Radio Demonstration", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("AREX Radio Demonstration")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
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

        self.settings = Qt.QSettings("GNU Radio", "arex_radio_trx_pluto")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.rx_freq = rx_freq = 10450200000
        self.RxOffset = RxOffset = 100000
        self.Tx_Mode = Tx_Mode = 4
        self.Tx_LO = Tx_LO = 5660000000
        self.Tx_Gain = Tx_Gain = 0
        self.Tx_Filt_Low = Tx_Filt_Low = -7500
        self.Tx_Filt_High = Tx_Filt_High = 7500
        self.ToneBurst = ToneBurst = False
        self.Rx_Mute = Rx_Mute = False
        self.Rx_Monitor = Rx_Monitor = True
        self.Rx_Mode = Rx_Mode = 4
        self.Rx_LO = Rx_LO = int(rx_freq - 9750000000 - RxOffset)
        self.Rx_Gain = Rx_Gain = 30
        self.Rx_Filt_Low = Rx_Filt_Low = -7500
        self.Rx_Filt_High = Rx_Filt_High = 7500
        self.PTT = PTT = True
        self.MicGain = MicGain = 5.0
        self.KEY = KEY = False
        self.FMMIC = FMMIC = 1
        self.FFT_SEL = FFT_SEL = 0
        self.CTCSS = CTCSS = 0
        self.AMMIC = AMMIC = 5
        self.AFGain = AFGain = 50

        ##################################################
        # Blocks
        ##################################################

        self._rx_freq_range = Range(10450100000, 10450300000, 1, 10450200000, 200)
        self._rx_freq_win = RangeWidget(self._rx_freq_range, self.set_rx_freq, "Receiver Freq", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._rx_freq_win)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=11,
                decimation=1,
                taps=[],
                fractional_bw=0.4)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN, #wintype
            0, #fc
            48000, #bw
            "Baseband after PLL capture", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0_0.enable_grid(True)
        self.qtgui_freq_sink_x_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(True)
        self.qtgui_freq_sink_x_0_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN, #wintype
            (Rx_LO + 9750000000), #fc
            528000, #bw
            "RX SDR", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(True)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.low_pass_filter_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                48000,
                3000,
                1000,
                window.WIN_HAMMING,
                6.76))
        self.iio_pluto_source_0 = iio.fmcomms2_source_fc32('ip:pluto.local' if 'ip:pluto.local' else iio.get_pluto_uri(), [True, True], 0x800)
        self.iio_pluto_source_0.set_len_tag_key('packet_len')
        self.iio_pluto_source_0.set_frequency(Rx_LO)
        self.iio_pluto_source_0.set_samplerate(528000)
        self.iio_pluto_source_0.set_gain_mode(0, 'slow_attack')
        self.iio_pluto_source_0.set_gain(0, 64)
        self.iio_pluto_source_0.set_quadrature(True)
        self.iio_pluto_source_0.set_rfdc(True)
        self.iio_pluto_source_0.set_bbdc(True)
        self.iio_pluto_source_0.set_filter_params('Auto', '', 0, 0)
        self.iio_pluto_sink_0 = iio.fmcomms2_sink_fc32('ip:pluto.local' if 'ip:pluto.local' else iio.get_pluto_uri(), [True, True], 0x800, False)
        self.iio_pluto_sink_0.set_len_tag_key('')
        self.iio_pluto_sink_0.set_bandwidth(20000000)
        self.iio_pluto_sink_0.set_frequency(Tx_LO)
        self.iio_pluto_sink_0.set_samplerate(528000)
        self.iio_pluto_sink_0.set_attenuation(0, Tx_Gain)
        self.iio_pluto_sink_0.set_filter_params('Auto', '', 0, 0)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(11, firdes.low_pass(1,529200,23000,2000), RxOffset, 528000)
        self.blocks_mute_xx_0_0_0 = blocks.mute_cc(bool((not PTT) or (Tx_Mode==2 and not KEY) or (Tx_Mode==3 and not KEY)))
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_4 = blocks.multiply_const_cc((Tx_Mode < 4) or (Tx_Mode==5))
        self.blocks_multiply_const_vxx_3 = blocks.multiply_const_cc(Tx_Mode==4)
        self.blocks_multiply_const_vxx_2_1_0 = blocks.multiply_const_ff((1.0 + (Rx_Mode==5)))
        self.blocks_multiply_const_vxx_2_1 = blocks.multiply_const_ff(Rx_Mode==5)
        self.blocks_multiply_const_vxx_2_0 = blocks.multiply_const_ff(((Rx_Mode==4) * 0.2))
        self.blocks_multiply_const_vxx_2 = blocks.multiply_const_ff(Rx_Mode<4)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_ff(((AFGain/100.0) *  (not Rx_Mute)))
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_ff((FMMIC/5.0))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(((MicGain)*(int(Tx_Mode==0)) + (MicGain)*(int(Tx_Mode==1)) + (AMMIC/10.0)*(int(Tx_Mode==5)) ))
        self.blocks_float_to_complex_0_0 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_real_0_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_add_xx_2 = blocks.add_vcc(1)
        self.blocks_add_xx_1_0 = blocks.add_vff(1)
        self.blocks_add_xx_1 = blocks.add_vff(1)
        self.blocks_add_xx_0_0 = blocks.add_vff(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.blocks_add_const_vxx_0_0 = blocks.add_const_ff(((0.5 * int(Tx_Mode==5)) + int(Tx_Mode==2) +int(Tx_Mode==3)))
        self.band_pass_filter_1 = filter.fir_filter_fff(
            1,
            firdes.band_pass(
                1,
                48000,
                10,
                3500,
                100,
                window.WIN_HAMMING,
                6.76))
        self.band_pass_filter_0_0 = filter.fir_filter_ccc(
            1,
            firdes.complex_band_pass(
                1,
                48000,
                Tx_Filt_Low,
                Tx_Filt_High,
                100,
                window.WIN_HAMMING,
                6.76))
        self.band_pass_filter_0 = filter.fir_filter_ccc(
            1,
            firdes.complex_band_pass(
                1,
                48000,
                Rx_Filt_Low,
                Rx_Filt_High,
                100,
                window.WIN_HAMMING,
                6.76))
        self.audio_source_0 = audio.source(48000, "plughw:2,0,1", True)
        self.audio_sink_0 = audio.sink(48000, "plughw:2,0,0", False)
        self.analog_sig_source_x_1_0 = analog.sig_source_f(48000, analog.GR_SIN_WAVE, (CTCSS/10.0), (0.15 * (CTCSS >0)), 0, 0)
        self.analog_sig_source_x_1 = analog.sig_source_f(48000, analog.GR_COS_WAVE, 1750, (1.0*ToneBurst), 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(48000, analog.GR_COS_WAVE, 0, 1, 0, 0)
        self.analog_rail_ff_0_0 = analog.rail_ff((-0.99), 0.99)
        self.analog_rail_ff_0 = analog.rail_ff((-1), 1)
        self.analog_pll_carriertracking_cc_0 = analog.pll_carriertracking_cc(0.02, 1.9635, (-1.9635))
        self.analog_nbfm_tx_0 = analog.nbfm_tx(
        	audio_rate=48000,
        	quad_rate=48000,
        	tau=(75e-6),
        	max_dev=5000,
        	fh=(-1),
                )
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=48000,
        	quad_rate=48000,
        	tau=(75e-6),
        	max_dev=5e3,
          )
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0)
        self.analog_agc3_xx_0 = analog.agc3_cc((1e-2), (5e-7), 0.1, 1.0, 1)
        self.analog_agc3_xx_0.set_max_gain(1000)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc3_xx_0, 0), (self.blocks_complex_to_real_0_0, 0))
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_float_to_complex_0_0, 1))
        self.connect((self.analog_nbfm_rx_0, 0), (self.blocks_multiply_const_vxx_2_0, 0))
        self.connect((self.analog_nbfm_tx_0, 0), (self.blocks_multiply_const_vxx_3, 0))
        self.connect((self.analog_pll_carriertracking_cc_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.analog_rail_ff_0, 0), (self.band_pass_filter_1, 0))
        self.connect((self.analog_rail_ff_0_0, 0), (self.blocks_float_to_complex_0_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.analog_sig_source_x_1_0, 0), (self.blocks_add_xx_0_0, 0))
        self.connect((self.audio_source_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.audio_source_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.analog_nbfm_rx_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.band_pass_filter_0_0, 0), (self.blocks_mute_xx_0_0_0, 0))
        self.connect((self.band_pass_filter_1, 0), (self.blocks_add_xx_0_0, 1))
        self.connect((self.blocks_add_const_vxx_0_0, 0), (self.analog_rail_ff_0_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.analog_rail_ff_0, 0))
        self.connect((self.blocks_add_xx_0_0, 0), (self.analog_nbfm_tx_0, 0))
        self.connect((self.blocks_add_xx_1, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_add_xx_1_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_add_xx_2, 0), (self.band_pass_filter_0_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_multiply_const_vxx_2_1, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_multiply_const_vxx_2, 0))
        self.connect((self.blocks_complex_to_real_0_0, 0), (self.blocks_multiply_const_vxx_2_1_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.analog_agc3_xx_0, 0))
        self.connect((self.blocks_float_to_complex_0_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_const_vxx_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_multiply_const_vxx_2, 0), (self.blocks_add_xx_1_0, 0))
        self.connect((self.blocks_multiply_const_vxx_2_0, 0), (self.blocks_add_xx_1, 1))
        self.connect((self.blocks_multiply_const_vxx_2_1, 0), (self.blocks_add_xx_1_0, 1))
        self.connect((self.blocks_multiply_const_vxx_2_1_0, 0), (self.blocks_add_xx_1, 0))
        self.connect((self.blocks_multiply_const_vxx_3, 0), (self.blocks_add_xx_2, 0))
        self.connect((self.blocks_multiply_const_vxx_4, 0), (self.blocks_add_xx_2, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_multiply_const_vxx_4, 0))
        self.connect((self.blocks_mute_xx_0_0_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_pll_carriertracking_cc_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.audio_sink_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.iio_pluto_sink_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "arex_radio_trx_pluto")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        self.rx_freq = rx_freq
        self.set_Rx_LO(int(self.rx_freq - 9750000000 - self.RxOffset))

    def get_RxOffset(self):
        return self.RxOffset

    def set_RxOffset(self, RxOffset):
        self.RxOffset = RxOffset
        self.set_Rx_LO(int(self.rx_freq - 9750000000 - self.RxOffset))
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.RxOffset)

    def get_Tx_Mode(self):
        return self.Tx_Mode

    def set_Tx_Mode(self, Tx_Mode):
        self.Tx_Mode = Tx_Mode
        self.blocks_add_const_vxx_0_0.set_k(((0.5 * int(self.Tx_Mode==5)) + int(self.Tx_Mode==2) +int(self.Tx_Mode==3)))
        self.blocks_multiply_const_vxx_0.set_k(((self.MicGain)*(int(self.Tx_Mode==0)) + (self.MicGain)*(int(self.Tx_Mode==1)) + (self.AMMIC/10.0)*(int(self.Tx_Mode==5)) ))
        self.blocks_multiply_const_vxx_3.set_k(self.Tx_Mode==4)
        self.blocks_multiply_const_vxx_4.set_k((self.Tx_Mode < 4) or (self.Tx_Mode==5))
        self.blocks_mute_xx_0_0_0.set_mute(bool((not self.PTT) or (self.Tx_Mode==2 and not self.KEY) or (self.Tx_Mode==3 and not self.KEY)))

    def get_Tx_LO(self):
        return self.Tx_LO

    def set_Tx_LO(self, Tx_LO):
        self.Tx_LO = Tx_LO
        self.iio_pluto_sink_0.set_frequency(self.Tx_LO)

    def get_Tx_Gain(self):
        return self.Tx_Gain

    def set_Tx_Gain(self, Tx_Gain):
        self.Tx_Gain = Tx_Gain
        self.iio_pluto_sink_0.set_attenuation(0,self.Tx_Gain)

    def get_Tx_Filt_Low(self):
        return self.Tx_Filt_Low

    def set_Tx_Filt_Low(self, Tx_Filt_Low):
        self.Tx_Filt_Low = Tx_Filt_Low
        self.band_pass_filter_0_0.set_taps(firdes.complex_band_pass(1, 48000, self.Tx_Filt_Low, self.Tx_Filt_High, 100, window.WIN_HAMMING, 6.76))

    def get_Tx_Filt_High(self):
        return self.Tx_Filt_High

    def set_Tx_Filt_High(self, Tx_Filt_High):
        self.Tx_Filt_High = Tx_Filt_High
        self.band_pass_filter_0_0.set_taps(firdes.complex_band_pass(1, 48000, self.Tx_Filt_Low, self.Tx_Filt_High, 100, window.WIN_HAMMING, 6.76))

    def get_ToneBurst(self):
        return self.ToneBurst

    def set_ToneBurst(self, ToneBurst):
        self.ToneBurst = ToneBurst
        self.analog_sig_source_x_1.set_amplitude((1.0*self.ToneBurst))

    def get_Rx_Mute(self):
        return self.Rx_Mute

    def set_Rx_Mute(self, Rx_Mute):
        self.Rx_Mute = Rx_Mute
        self.blocks_multiply_const_vxx_1.set_k(((self.AFGain/100.0) *  (not self.Rx_Mute)))

    def get_Rx_Monitor(self):
        return self.Rx_Monitor

    def set_Rx_Monitor(self, Rx_Monitor):
        self.Rx_Monitor = Rx_Monitor

    def get_Rx_Mode(self):
        return self.Rx_Mode

    def set_Rx_Mode(self, Rx_Mode):
        self.Rx_Mode = Rx_Mode
        self.blocks_multiply_const_vxx_2.set_k(self.Rx_Mode<4)
        self.blocks_multiply_const_vxx_2_0.set_k(((self.Rx_Mode==4) * 0.2))
        self.blocks_multiply_const_vxx_2_1.set_k(self.Rx_Mode==5)
        self.blocks_multiply_const_vxx_2_1_0.set_k((1.0 + (self.Rx_Mode==5)))

    def get_Rx_LO(self):
        return self.Rx_LO

    def set_Rx_LO(self, Rx_LO):
        self.Rx_LO = Rx_LO
        self.iio_pluto_source_0.set_frequency(self.Rx_LO)
        self.qtgui_freq_sink_x_0.set_frequency_range((self.Rx_LO + 9750000000), 528000)

    def get_Rx_Gain(self):
        return self.Rx_Gain

    def set_Rx_Gain(self, Rx_Gain):
        self.Rx_Gain = Rx_Gain

    def get_Rx_Filt_Low(self):
        return self.Rx_Filt_Low

    def set_Rx_Filt_Low(self, Rx_Filt_Low):
        self.Rx_Filt_Low = Rx_Filt_Low
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, 48000, self.Rx_Filt_Low, self.Rx_Filt_High, 100, window.WIN_HAMMING, 6.76))

    def get_Rx_Filt_High(self):
        return self.Rx_Filt_High

    def set_Rx_Filt_High(self, Rx_Filt_High):
        self.Rx_Filt_High = Rx_Filt_High
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, 48000, self.Rx_Filt_Low, self.Rx_Filt_High, 100, window.WIN_HAMMING, 6.76))

    def get_PTT(self):
        return self.PTT

    def set_PTT(self, PTT):
        self.PTT = PTT
        self.blocks_mute_xx_0_0_0.set_mute(bool((not self.PTT) or (self.Tx_Mode==2 and not self.KEY) or (self.Tx_Mode==3 and not self.KEY)))

    def get_MicGain(self):
        return self.MicGain

    def set_MicGain(self, MicGain):
        self.MicGain = MicGain
        self.blocks_multiply_const_vxx_0.set_k(((self.MicGain)*(int(self.Tx_Mode==0)) + (self.MicGain)*(int(self.Tx_Mode==1)) + (self.AMMIC/10.0)*(int(self.Tx_Mode==5)) ))

    def get_KEY(self):
        return self.KEY

    def set_KEY(self, KEY):
        self.KEY = KEY
        self.blocks_mute_xx_0_0_0.set_mute(bool((not self.PTT) or (self.Tx_Mode==2 and not self.KEY) or (self.Tx_Mode==3 and not self.KEY)))

    def get_FMMIC(self):
        return self.FMMIC

    def set_FMMIC(self, FMMIC):
        self.FMMIC = FMMIC
        self.blocks_multiply_const_vxx_0_0.set_k((self.FMMIC/5.0))

    def get_FFT_SEL(self):
        return self.FFT_SEL

    def set_FFT_SEL(self, FFT_SEL):
        self.FFT_SEL = FFT_SEL

    def get_CTCSS(self):
        return self.CTCSS

    def set_CTCSS(self, CTCSS):
        self.CTCSS = CTCSS
        self.analog_sig_source_x_1_0.set_frequency((self.CTCSS/10.0))
        self.analog_sig_source_x_1_0.set_amplitude((0.15 * (self.CTCSS >0)))

    def get_AMMIC(self):
        return self.AMMIC

    def set_AMMIC(self, AMMIC):
        self.AMMIC = AMMIC
        self.blocks_multiply_const_vxx_0.set_k(((self.MicGain)*(int(self.Tx_Mode==0)) + (self.MicGain)*(int(self.Tx_Mode==1)) + (self.AMMIC/10.0)*(int(self.Tx_Mode==5)) ))

    def get_AFGain(self):
        return self.AFGain

    def set_AFGain(self, AFGain):
        self.AFGain = AFGain
        self.blocks_multiply_const_vxx_1.set_k(((self.AFGain/100.0) *  (not self.Rx_Mute)))




def main(top_block_cls=arex_radio_trx_pluto, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
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

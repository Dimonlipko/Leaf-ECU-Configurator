#!/usr/bin/python
# -*- coding: utf-8 -*-
import platform
import math

try:
    import PyQt5.QtGui as gui
    import PyQt5.QtCore as core
    import PyQt5.QtWidgets as widgets
    if platform.system() == 'Darwin':
        import PyQt5.QtWebEngine as webkit
        import PyQt5.QtWebEngineWidgets as webkitwidgets
    else:
        import PyQt5.QtWebKit as webkit
        import PyQt5.QtWebKitWidgets as webkitwidgets
    def utf8(string):
        return string
    qt5 = True
except:
    import PyQt4.QtGui as gui
    import PyQt4.QtGui as widgets
    import PyQt4.QtCore as core
    import PyQt4.QtWebKit as webkit
    import PyQt4.QtWebKit as webkitwidgets
    def utf8(string):
        return string
        # return unicode(string.toUtf8(), encoding="UTF-8")
    qt5 = False

import ecu
import options
import elm
import os
import time

_ = options.translator('ddt4all')

plugin_name = _("Firmware Update")
category = _("Firmware")
need_hw = True

class FirmwareReceiverUpdate(widgets.QDialog):

    def __init__(self):
        super(FirmwareReceiverUpdate, self).__init__()
        layout = widgets.QVBoxLayout()
        info = widgets.QLabel(_(utf8("FIRMWARE UPDATE")))
        info.setAlignment(core.Qt.AlignHCenter)
        layout.addWidget(info)

        self.open_button = widgets.QPushButton(_("Open file..."))
        self.open_button.clicked.connect(self.read_file)
        layout.addWidget(self.open_button)

        info = widgets.QLabel(_(utf8("CAN request id (hex):")))
        layout.addWidget(info)
        # TODO: filter input to hex digits
        self.canbase_input = widgets.QLineEdit("79b")
        layout.addWidget(self.canbase_input)
        
        info = widgets.QLabel(_(utf8("CAN answer id (hex):")))
        layout.addWidget(info)
        # TODO: filter input to hex digits
        self.cananswer_input = widgets.QLineEdit("7bb")
        layout.addWidget(self.cananswer_input)

        info = widgets.QLabel(_(utf8("Device token (hex):")))
        layout.addWidget(info)
        self.devtoken_input = widgets.QLineEdit("cafeface")
        layout.addWidget(self.devtoken_input)

        #self.hex_count_label = widgets.QLabel()
        self.program_size_label = widgets.QLabel()
        #self.eeprom_size_label = widgets.QLabel()
        #self.confbit_size_label = widgets.QLabel()
        #self.userid_size_label = widgets.QLabel()
        self.frames_label = widgets.QLabel()
        self.sent_frames_label = widgets.QLabel()
        #self.error_frames_label = widgets.QLabel()
        #layout.addWidget(self.hex_count_label)
        layout.addWidget(self.program_size_label)
        #layout.addWidget(self.eeprom_size_label)
        #layout.addWidget(self.confbit_size_label)
        #layout.addWidget(self.userid_size_label)
        layout.addWidget(self.frames_label)
        layout.addWidget(self.sent_frames_label)
        #layout.addWidget(self.error_frames_label)

        self.progress = widgets.QProgressBar()
        layout.addWidget(self.progress)

        self.flash_button = widgets.QPushButton(_("Flash"))
        self.flash_button.clicked.connect(self.flash_firmware)
        self.flash_button.setEnabled(False)
        layout.addWidget(self.flash_button)
        self.setLayout(layout)

        self.set_sent_frames(0)
        #self.set_error_frames(0)

    def update_firmware_size(self):
        # TODO: proper localization?
        framecount = math.ceil(float(len(self.firmware_data)) / 4)
        self.frames_label.setText(_("CAN frames: %d" % framecount))
        self.progress.setMaximum(framecount)
        self.program_size_label.setText(_("FLASH: %d bytes" % len(self.firmware_data)))

    def set_sent_frames(self, framecount):
        self.sent_frames_label.setText(_("Sent: %d" % framecount))
        self.progress.setValue(framecount)

    #def set_error_frames(self, errorcount):
        #self.error_frames_label.setText(_("Errors: %d" % errorcount))

    def read_file(self):
        fname = widgets.QFileDialog.getOpenFileName(self, "Open File", os.getcwd(), "Arduino binary (*.bin)")
        if fname:
            try:
                with open(str(fname.toUtf8()), 'rb') as fp:
                    # TODO: test with python3
                    self.firmware_data = fp.read()
                self.update_firmware_size()
                self.flash_button.setEnabled(True)
            except Exception as e:
                widgets.QMessageBox.critical(self, "Error", str(e))

    def _send_can(self, request_id, request, response_id, response):
        if options.simulation_mode:
            options.main_window.logview.append(_("Sending request: {:x} {} Expecting response: {:x} {}").format(request_id, request, response_id, response))
        else:
            options.elm.send_raw('atsh {:x}'.format(request_id))
            rsp = options.elm.send_raw(request)
            # TODO: check response
            print(rsp)

    def _invert_bytes(self, s):
        return ''.join([ s[i:i+2] for i in range(0, 8, 2) ][::-1])

    def flash_firmware(self):
        self.flash_button.setEnabled(False)
        self.open_button.setEnabled(False)

        #try:

        # TODO: do we need to restore it?
        if not options.simulation_mode:
            # Disable ISOTP
            options.elm.send_raw('atcaf0')
            # Allow 8 byte packets
            options.elm.send_raw('atal')

        # Might be excessive but we make sure it's a valid hex
        canbase = int(str(self.canbase_input.text()), 16)
        cananswer = int(str(self.cananswer_input.text()), 16)
        devtoken = int(str(self.devtoken_input.text()), 16)

        options.main_window.logview.append(_("Initiating boot mode"))

        payload = self._invert_bytes('deadbeef') + self._invert_bytes('{:04x}'.format(devtoken))
        response = self._invert_bytes('deafdead') + self._invert_bytes('{:04x}'.format(devtoken))
        self._send_can(canbase, payload, cananswer, payload)

        # TODO async?
        time_to_sleep = 5
        options.main_window.logview.append(_("Waiting {} seconds for device to reboot").format(time_to_sleep))
        time.sleep(time_to_sleep)

        for block, chunk in enumerate(self.firmware_data[i:i+4] for i in range(0, len(self.firmware_data), 4)):
            # Pad with zeroes if needed
            chunk += '\00' * (4 - len(chunk))
            addrh = block / 256
            addrl = block % 256
            self._send_can(canbase, ('{:02x}'*7).format(0xff, addrl, addrh, *(ord(i) for i in chunk)),
                            cananswer, ('{:02x}'*2).format(addrl, addrh))
            self.set_sent_frames(block +1)

        options.main_window.logview.append(_("Finalizing flashing"))
        self._send_can(canbase, self._invert_bytes('c0defade'), 0, '')

        #except:
            # TODO message boxes about errors and stuff
            #pass

        self.flash_button.setEnabled(True)
        self.open_button.setEnabled(True)

def plugin_entry():
    v = FirmwareReceiverUpdate()
    v.exec_()

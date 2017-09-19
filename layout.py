import os
import custom_logging as logging
import time

import urwid

class Log:

    def __init__(self, pipe):
            logging.add("Initiating Urwid")
            self.palette = [('logs', 'light red', 'light gray', 'standout'),
                            ('logs-focus', 'white', 'light red', 'bold'),
                            ('bg', 'light red', 'light gray')]

            self.logList = urwid.SimpleListWalker([])
            self.logListBox = urwid.ListBox(self.logList)
            self.logListBox = urwid.AttrWrap(self.logListBox, 'logs')
            self.filler = urwid.Filler(self.logListBox, height=("relative", 80))
            self.info = urwid.Text("Info")
            self.info = urwid.Filler(self.info)
            self.cols = urwid.Columns([self.filler, self.info])
            self.cols = urwid.AttrMap(self.cols, 'logs')
            self.background = urwid.SolidFill('X')
            self.background = urwid.AttrMap(self.background, 'bg')
            self.header = urwid.Text("Island")
            self.header = urwid.AttrWrap(self.header, 'logs')
            self.frame = urwid.Frame(header=self.header, body=self.cols)
            self.overlay = urwid.Overlay(self.frame, self.background, align='center',
            width=('relative', 90), valign='middle', height=('relative', 90))
            self.main = urwid.MainLoop(self.overlay, self.palette)
            self.pipeListen = pipe

    def addLog(self, str):
        #self.logList.append(str)
        txt = urwid.Text(str)
        txt = urwid.AttrMap(txt, 'logs', 'logs-focus')
        txt = urwid.Padding(txt, left=4)
        self.logList.append(txt)
        if len(self.logList) > 50:
            del self.logList[0]
        self.logListBox.set_focus(len(self.logList)-1)

    def run(self):
        self.main.run()

    def start(self):
        self.main.start()

    def stop(self):
        self.main.stop()

    def draw(self):
        self.main.draw_screen()
        raw = self.main.screen.get_available_raw_input()
        parsed, rawUnused = self.main.screen.parse_input(None, None, raw)
        for i in parsed:
            if i in('q', 'Q'):
                return False
        txt = self.pipeListen.recv()
        if txt:
            self.addLog(txt)
        return True

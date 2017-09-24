import os
import custom_logging as logging
import time

import urwid

class Log:

    def __init__(self, pipe):
            logging.add("Initiating Urwid")
            self.palette = [('logs', 'light red', 'light gray', '', '#f06', '#ddd'),
                            ('logs-focus', 'white', 'light red', '', '#ddd', '#f06'),
                            ('bg', 'light red', 'light gray', '', '#f06', '#ddd'),
                            ('title', 'white', 'light red', 'bold', '#ddd', '#f06')]

            self.logList = urwid.SimpleListWalker([])
            self.logListBox = urwid.ListBox(self.logList)
            self.logListBox = urwid.AttrWrap(self.logListBox, 'logs')
            self.logListBoxOuter = urwid.Padding(self.logListBox, align='left', width=('relative', 90))
            self.logListBoxOuter = urwid.Filler(self.logListBoxOuter, height=('relative', 90))
            self.logHeader = urwid.Filler(urwid.Text("People"))
            self.logHeader = urwid.AttrMap(self.logHeader, 'title')
            self.logHeader = urwid.Padding(self.logHeader, align='center', width=('relative', 90))
            self.logHeader = urwid.Filler(self.logHeader, height=('relative', 90))
            self.logPile = urwid.Pile([('weight', 1,self.logHeader), ('weight', 9, self.logListBoxOuter)])
            #self.filler = urwid.Filler(self.logPile, height=("relative", 50))
            self.logPile = urwid.LineBox(self.logPile)

            self.infoTitle = urwid.Text("\nInfo\n")
            self.infoTitle = urwid.AttrMap(urwid.Padding(self.infoTitle, align='left', left = 1), 'title')
            self.infoName = urwid.Text("Name: ")
            self.infoLocation = urwid.Text("Location: ")
            self.infoHunger = urwid.Text("Hunger: ")
            self.infoFood = urwid.Text("Food: ")
            self.infoBody = urwid.Pile([self.infoName,
                self.infoLocation, self.infoHunger,self.infoFood])
            self.infoPile = urwid.Pile([self.infoTitle, self.infoBody])
            self.info = urwid.Padding(self.infoPile, align='left', left = 1, right =1)
            self.info = urwid.Filler(self.info, valign='top')
            self.info = urwid.LineBox(self.info)

            self.highlightTitle = urwid.Text("\nHighlight\n")
            self.highlightTitle = urwid.AttrMap(urwid.Padding(self.highlightTitle, align='left', left = 1), 'title')
            self.highlightText = urwid.Text("Hightlight Text")
            self.highlightPile = urwid.Pile([self.highlightTitle, self.highlightText])
            self.highlight = urwid.Padding(self.highlightPile, align='left', left=1, right =1)
            self.highlight = urwid.Filler(self.highlight, valign='top')
            self.highlight = urwid.LineBox(self.highlight)

            self.right = urwid.Pile([self.info, self.highlight])

            self.cols = urwid.Columns([self.logPile, self.right])
            self.cols = urwid.AttrMap(self.cols, 'logs')

            self.background = urwid.SolidFill('{')
            self.background = urwid.AttrMap(self.background, 'bg')

            headerText = """\n# Social Simulation at the End of the World #\n"""

            self.header = urwid.Text(headerText, align='center')
            self.header = urwid.AttrWrap(self.header, 'title')


            self.frame = urwid.Frame(header=self.header, body=self.cols)
            self.overlay = urwid.Overlay(self.frame, self.background, align='center',
            width=('relative', 90), valign='middle', height=('relative', 90))

            screen = urwid.raw_display.Screen()
            screen.set_terminal_properties(colors=256)
            screen.reset_default_terminal_palette()
            screen.register_palette(self.palette)
            self.main = urwid.MainLoop(self.overlay, self.palette)
            self.main.screen.set_terminal_properties(colors=256)
            self.pipeListen = pipe

    def addLog(self, str):
        txt = urwid.Text(str)
        txt = urwid.AttrMap(txt, 'logs', 'logs-focus')
        txt = urwid.Padding(txt, left=4)
        self.logList.append(txt)
        if len(self.logList) > 50:
            del self.logList[0]
        self.logListBox.set_focus(len(self.logList)-1)

    def setHighlight(self, str):
        self.highlightText.set_text(str)

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
            if txt[0] == '1':
                self.addLog(txt[1:])
            elif txt[0] == '2':
                self.setHighlight(txt[1:])
        return True

#!/usr/bin/env python
# Boa:App:BoaApp

# import Frame1
from xlog import getLogger
from MainFrame import MainFrame
import wx
import time

import json

from pynput import mouse
from pynput import keyboard
from pynput.mouse import Button
from pynput.keyboard import Key, KeyCode

logger = getLogger()
# modules = {'Frame1': [1, 'Main frame of Application', u'Frame1.py']}


# class BoaApp(wx.App):
#     def __init__(self, parent=None):
#         super().__init__()
#         # def OnInit(self):
#         self.main = Frame1.create(parent)
#         self.main.Show()
#         self.SetTopWindow(self.main)
#         # return True


def main():
    logger.info('run')
    logger.debug('debug')
    application = wx.App()
    frame = MainFrame()
    frame.Show()
    application.MainLoop()


def single_run(script_path, run_times=1):

    # python KeymouseGo.py scripts/0416_2342.txt 10
    # KeymouseGo.exe scripts\0416_2342.txt

    s = open(script_path, 'r').read()
    s = json.loads(s)
    steps = len(s)

    mouse_ctl = mouse.Controller()
    keyboard_ctl = keyboard.Controller()

    j = 0
    while j < run_times or run_times == 0:
        j += 1

        # Keep the same with Frame1.py:455, and remove code include `self`
        for i in range(steps):

            print(s[i])

            # for old style script
            if isinstance(s[i][0], str) and isinstance(s[i][3], int):
                s[i].insert(0, s[i][3])

            delay = s[i][0]
            event_type = s[i][1]
            message = s[i][2]
            action = s[i][3]

            message = message.lower()

            time.sleep(delay / 1000.0)

            if event_type == 'EM':
                x, y = action
                mouse_ctl.position = (x, y)
                if message == 'mouse left down':
                    mouse_ctl.press(Button.left)
                elif message == 'mouse left up':
                    mouse_ctl.release(Button.left)
                elif message == 'mouse right down':
                    mouse_ctl.press(Button.right)
                elif message == 'mouse right up':
                    mouse_ctl.release(Button.right)
                else:
                    print('unknow mouse event:', message)

            elif event_type == 'EK':
                key_name = action

                if len(key_name) == 1:
                    key = key_name
                else:
                    key = getattr(Key, key_name)

                if message == 'key down':
                    keyboard_ctl.press(key)
                elif message == 'key up':
                    keyboard_ctl.release(key)
                else:
                    print('unknow keyboard event:', message)

    print('script run finish!')


if __name__ == '__main__':

    print(sys.argv)

    if len(sys.argv) > 1:
        script_path = sys.argv[1]
        run_times = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        single_run(script_path, run_times)
    else:
        main()

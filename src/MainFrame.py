# Boa:Frame:MainFrame

# import os
# import sys
from xlog import getLogger
# from xlog import func_call_decorator
import wx
import time
import threading
from datetime import datetime
import json
# import traceback

from pynput import mouse
from pynput import keyboard
from pynput.mouse import Button
from pynput.keyboard import Key, KeyCode

import pathlib

import io
from wx.adv import TaskBarIcon as wxTaskBarIcon
from wx.adv import EVT_TASKBAR_LEFT_DCLICK


# # anther way to resolve DPI Scaling on win10
# try:
#     import ctypes
#     ctypes.c_int()
#     ctypes.windll.shcore.SetProcessDpiAwareness(2)
# except Exception as e:
#     print(e)

logger = getLogger()

wx.NO_3D = 0


KEYS = ['F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12']


def MB_Event():
    mb = {
        "name": "mouse",
        "event": "click",
        "button": "left",
        "action": "down",
        "location": {
            "x": "0",
            "y": "0"
        }
    }
    return mb


def GetMondrianStream():
    data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x06\x00\x00\x00szz\xf4\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00qIDATX\x85\xed\xd6;\n\x800\x10E\xd1{\xc5\x8d\xb9r\x97\x16\x0b\xad$\x8a\x82:\x16o\xda\x84pB2\x1f\x81Fa\x8c\x9c\x08\x04Z{\xcf\xa72\xbcv\xfa\xc5\x08 \x80r\x80\xfc\xa2\x0e\x1c\xe4\xba\xfaX\x1d\xd0\xde]S\x07\x02\xd8>\xe1wa-`\x9fQ\xe9\x86\x01\x04\x10\x00\\(Dk\x1b-\x04\xdc\x1d\x07\x14\x98;\x0bS\x7f\x7f\xf9\x13\x04\x10@\xf9X\xbe\x00\xc9 \x14K\xc1<={\x00\x00\x00\x00IEND\xaeB`\x82'
    stream = io.BytesIO(data)
    return stream


def GetMondrianBitmap():
    stream = GetMondrianStream()
    image = wx.Image(stream)
    return wx.Bitmap(image)


def GetMondrianIcon():
    icon = wx.Icon()
    icon.CopyFromBitmap(GetMondrianBitmap())
    return icon


def create(parent):
    return MainFrame(parent)


[wxID_MAINFRAME, wxID_MAINFRAME_BTNRECORD, wxID_MAINFRAME_BTRUN, wxID_MAINFRAME_BTPAUSE, wxID_MAINFRAME_BUTTON1,
 wxID_MAINFRAME_CHOICE_SCRIPT, wxID_MAINFRAME_CHOICE_START, wxID_MAINFRAME_CHOICE_STOP,
 wxID_MAINFRAME_PANEL1, wxID_MAINFRAME_STATICTEXT1, wxID_MAINFRAME_STATICTEXT2,
 wxID_MAINFRAME_STATICTEXT3, wxID_MAINFRAME_STATICTEXT4, wxID_MAINFRAME_STIMES,
 wxID_MAINFRAME_TEXTCTRL1, wxID_MAINFRAME_TEXTCTRL2, wxID_MAINFRAME_INDICATOR,
 wxID_MAINFRAME_TSTOP, wxID_MAINFRAME_STATICTEXT5, wxID_MAINFRAME_TEXTCTRL3,
 ] = [wx.NewId() for _init_ctrls in range(20)]


class MainFrame(wx.Frame):
    # @func_call_decorator
    def _init_ctrls(self, parent):
        # logger.debug('{} run'.format(__name__))
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_MAINFRAME, name='', parent=parent,
                          pos=wx.Point(506, 283), size=wx.Size(366, 201),
                          style=wx.STAY_ON_TOP | wx.DEFAULT_FRAME_STYLE,
                          title='Keymouse Go')
        # self.SetClientSize(wx.Size(350, 205))
        self.SetClientSize(wx.Size(480, 360))

        self.panel1 = wx.Panel(id=wxID_MAINFRAME_PANEL1, name='panel1', parent=self,
                               pos=wx.Point(0, 0), size=wx.Size(350, 205),
                               style=wx.NO_3D | wx.CAPTION)

        self.btnRecord = wx.Button(id=wxID_MAINFRAME_BTNRECORD, label='录制',
                                   name='btnRecord', parent=self.panel1, pos=wx.Point(202, 12),
                                   size=wx.Size(56, 32), style=0)
        self.btnRecord.Bind(wx.EVT_BUTTON, self.on_BtnRecord,
                            id=wxID_MAINFRAME_BTNRECORD)

        self.btnRun = wx.Button(id=wxID_MAINFRAME_BTRUN, label='启动',
                                name='btnRun', parent=self.panel1, pos=wx.Point(274, 12),
                                size=wx.Size(56, 32), style=0)
        self.btnRun.Bind(wx.EVT_BUTTON, self.OnBtrunButton,
                         id=wxID_MAINFRAME_BTRUN)

        # 暂停/继续 功能不适合用按钮的形式来做，所以暂时隐去
        # self.btnpause = wx.Button(id=wxID_MAINFRAME_BTPAUSE, label=u'\u6682\u505c',
        #       name='btpause', parent=self.panel1, pos=wx.Point(274, 141),
        #       size=wx.Size(56, 32), style=0)
        # self.btnpause.Bind(wx.EVT_BUTTON, self.OnBtpauseButton, id=wxID_MAINFRAME_BTPAUSE)

        self.stIndicator = wx.StaticText(id=wxID_MAINFRAME_INDICATOR, label=u'ready..',
                                         name='stIndicator', parent=self.panel1, pos=wx.Point(17, 175),
                                         size=wx.Size(100, 36), style=0)

        # self.button1 = wx.Button(id=wxID_MAINFRAME_BUTTON1, label=u'测试111',
        #                          name='button1', parent=self.panel1, pos=wx.Point(128, 296),
        #                          size=wx.Size(75, 24), style=0)
        # self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
        #                   id=wxID_MAINFRAME_BUTTON1)

        self.tstop = wx.StaticText(id=wxID_MAINFRAME_TSTOP,
                                   label=u'If you want to stop it, Press F12', name='tstop',
                                   parent=self.panel1, pos=wx.Point(25, 332), size=wx.Size(183, 18),
                                   style=0)
        self.tstop.Show(False)

        self.stimes = wx.SpinCtrl(id=wxID_MAINFRAME_STIMES, initial=0, max=1000,
                                  min=0, name='stimes', parent=self.panel1, pos=wx.Point(206, 101),
                                  size=wx.Size(45, 18), style=wx.SP_ARROW_KEYS)
        self.stimes.SetValue(1)

        self.label_run_times = wx.StaticText(id=wxID_MAINFRAME_STATICTEXT2,
                                             label=u'执行次数(0为无限循环)',
                                             name='label_run_times', parent=self.panel1, pos=wx.Point(203, 61),
                                             size=wx.Size(136, 26), style=0)

        # self.textCtrl1 = wx.TextCtrl(id=wxID_MAINFRAME_TEXTCTRL1, name='textCtrl1',
        #                              parent=self.panel1, pos=wx.Point(24, 296), size=wx.Size(40, 22),
        #                              style=0, value='119')

        # self.textCtrl2 = wx.TextCtrl(id=wxID_MAINFRAME_TEXTCTRL2, name='textCtrl2',
        #                              parent=self.panel1, pos=wx.Point(80, 296), size=wx.Size(36, 22),
        #                              style=0, value='123')

        self.label_script = wx.StaticText(id=wxID_MAINFRAME_STATICTEXT3,
                                          label=u'脚本', name='label_script', parent=self.panel1,
                                          pos=wx.Point(17, 20), size=wx.Size(40, 32), style=0)

        self.choice_script = wx.Choice(choices=[], id=wxID_MAINFRAME_CHOICE_SCRIPT,
                                       name=u'choice_script', parent=self.panel1, pos=wx.Point(79, 15),
                                       size=wx.Size(108, 25), style=0)

        self.label_start_key = wx.StaticText(id=wxID_MAINFRAME_STATICTEXT1,
                                             label=u'启动热键', name='label_start_key',
                                             parent=self.panel1, pos=wx.Point(16, 63), size=wx.Size(56, 24),
                                             style=0)

        self.label_stop_key = wx.StaticText(id=wxID_MAINFRAME_STATICTEXT4,
                                            label=u'终止热键', name='label_stop_key',
                                            parent=self.panel1, pos=wx.Point(16, 102), size=wx.Size(56, 32),
                                            style=0)

        self.choice_start = wx.Choice(choices=[], id=wxID_MAINFRAME_CHOICE_START,
                                      name=u'choice_start', parent=self.panel1, pos=wx.Point(79, 58),
                                      size=wx.Size(108, 25), style=0)
        self.choice_start.SetLabel(u'')
        self.choice_start.SetLabelText(u'')
        self.choice_start.Bind(wx.EVT_CHOICE, self.OnChoice_startChoice,
                               id=wxID_MAINFRAME_CHOICE_START)

        self.choice_stop = wx.Choice(choices=[], id=wxID_MAINFRAME_CHOICE_STOP,
                                     name=u'choice_stop', parent=self.panel1, pos=wx.Point(79, 98),
                                     size=wx.Size(108, 25), style=0)
        self.choice_stop.Bind(wx.EVT_CHOICE, self.OnChoice_stopChoice,
                              id=wxID_MAINFRAME_CHOICE_STOP)

        # ===== if use SetProcessDpiAwareness, comment below =====
        self.label_scale = wx.StaticText(id=wxID_MAINFRAME_STATICTEXT5,
                                         label='屏幕缩放', name='staticText5',
                                         parent=self.panel1, pos=wx.Point(16, 141), size=wx.Size(56, 32),
                                         style=0)
        self.text_scale = wx.TextCtrl(id=wxID_MAINFRAME_TEXTCTRL3, name='textCtrl3',
                                      parent=self.panel1, pos=wx.Point(79, 138), size=wx.Size(108, 22),
                                      style=0, value='100%')
        # =========================================================

    def __init__(self, parent=None):

        # logger.debug('{} run'.format(__name__))

        self._init_ctrls(parent)

        self.SetIcon(GetMondrianIcon())
        self.taskBarIcon = TaskBarIcon(self)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_ICONIZE, self.OnIconfiy)

        # 当前脚本的父路径
        script_path = pathlib.Path(__file__).with_name("..").resolve()
        # print(script_path)
        self.script_path = script_path / 'scripts'
        # print(self.script_path)

        self.script_path.mkdir(parents=True, exist_ok=True)
        self.scripts = [s.name for s in self.script_path.glob('*.txt')]

        self.choice_script.SetItems(self.scripts)
        # self.scripts = list(filter(lambda s: s.endswith('.txt'), self.scripts))
        if self.scripts:
            self.choice_script.SetSelection(0)

        self.choice_start.SetItems(KEYS)
        self.choice_start.SetSelection(3)

        self.choice_stop.SetItems(KEYS)
        self.choice_stop.SetSelection(6)

        self.running = False
        self.recording = False
        self.record = []
        self.ttt = self.now_ts

        # for pause-resume feature
        self.paused = False
        self.pause_event = threading.Event()

        # =========== create mouse listener for record ===========
        # @func_call_decorator
        def on_move(x, y):
            # logger.debug('{} run'.format(__name__))
            if not self.recording or self.running:
                return True

        # @func_call_decorator
        def on_scroll(x, y, dx, dy):
            # logger.debug('{} run'.format(__name__))
            if not self.recording or self.running:
                return True

        # @func_call_decorator
        def on_click(x, y, button, pressed):
            # logger.debug('{} run'.format(__name__))

            if not self.recording or self.running:
                return True

            # ===== if use SetProcessDpiAwareness, comment below =====
            try:
                scale = self.text_scale.GetValue()
                scale = scale.replace('%', '').replace('-', '').strip()
                scale = float(scale)
                scale = scale / 100.0
            except:
                scale = 1
            x = int(x / scale)
            y = int(y / scale)
            # =========================================================

            logger.debug('mouse click: ({},{}) {} {}'.format(
                x, y, button.name, pressed))

            delay = self.now_ts - self.ttt
            self.ttt = self.now_ts
            if not self.record:
                delay = 0

            pos = (x, y)
            if button.name == 'left':
                message = 'mouse left '
            elif button.name == 'right':
                message = 'mouse right '
            else:
                return True
            if pressed:
                message += 'down'
            else:
                message += 'up'
            self.record.append([delay, 'EM', message, pos])
            text = self.stIndicator.GetLabel()
            text = text.replace(' actions recorded', '')
            text = str(eval(text)+1)
            text = text + ' actions recorded'
            self.stIndicator.SetLabel(text)
            return True

        # =========== create keyboard listener for record ===========
        # @func_call_decorator
        def key_event(key, is_press):
            if not self.recording or self.running:
                return True

            if is_press:
                logger.debug('keyboard press:{}'.format(key))
                message = 'key down'
            else:
                logger.debug('keyboard release:{}'.format(key))
                message = 'key up'

            if isinstance(key, Key):
                logger.debug('Key: {}({})'.format(key.name, key.value.vk))
                name = key.name
            elif isinstance(key, KeyCode):
                logger.debug('KeyCode: {}({})'.format(key.char, key.vk))
                name = key.char
            else:
                assert False

            delay = self.now_ts - self.ttt
            self.ttt = self.now_ts
            if not self.record:
                delay = 0

            self.record.append([delay, 'EK', message, name])

            text = self.stIndicator.GetLabel()
            text = text.replace(' actions recorded', '')
            text = str(eval(text) + 1)
            text = text + ' actions recorded'
            self.stIndicator.SetLabel(text)
            return True

        # @func_call_decorator
        def on_press(key):
            return key_event(key, True)

        # @func_call_decorator
        def on_release(key):
            logger.debug('===== {}'.format(key))
            if not self.recording:
                # listen for start/stop script
                start_name = 'f6'
                stop_name = 'f9'
                start_index = self.choice_start.GetSelection()
                start_name = KEYS[start_index].lower()
                stop_index = self.choice_stop.GetSelection()
                stop_name = KEYS[stop_index].lower()

                logger.debug("{}->{} : {}".format(start_name, stop_name, key))

                if not isinstance(key, Key):
                    return True

                if key.name == start_name and not self.running:
                    logger.debug('script start')
                    t = RunScriptClass(self, self.pause_event)
                    t.start()
                elif key.name == stop_name and self.running:
                    logger.debug('script stop')
                    self.stIndicator.SetLabel('broken')
            return key_event(key, False)

        self.mouse_listener = mouse.Listener(
            on_move=on_move,
            on_scroll=on_scroll,
            on_click=on_click
        )
        self.keyboard_listener = keyboard.Listener(
            on_press=on_press,
            on_release=on_release)

        self.mouse_listener.start()
        self.keyboard_listener.start()

    @property
    def now_ts(self):
        return int(time.time() * 1000)

    def get_script_path(self):
        i = self.choice_script.GetSelection()
        if i < 0:
            return ''
        script = self.scripts[i]
        # path = os.path.join(os.getcwd(), 'scripts', script)

        return self.script_path / script

    def new_script_path(self):
        now = datetime.now()
        script = now.strftime('%m%d_%H%M.txt')
        if script in self.scripts:
            script = now.strftime('%m%d_%H%M%S.txt')
        self.scripts.insert(0, script)
        self.choice_script.SetItems(self.scripts)
        self.choice_script.SetSelection(0)
        return self.get_script_path()

    def OnHide(self, event):
        self.Hide()
        event.Skip()

    def OnIconfiy(self, event):
        self.Hide()
        event.Skip()

    def OnClose(self, event):
        try:
            self.mouse_listener.stop()
            self.keyboard_listener.stop()
        except:
            pass
        self.taskBarIcon.Destroy()
        self.Destroy()
        event.Skip()

    def OnButton1Button(self, event):
        event.Skip()

    def on_BtnRecord(self, event):

        if self.recording:
            logger.debug('record stop')
            self.recording = False
            del self.record[-2]
            del self.record[-1]
            output = json.dumps(self.record, indent=1)
            output = output.replace('\r\n', '\n').replace('\r', '\n')
            output = output.replace('\n   ', '').replace('\n  ', '')
            output = output.replace('\n ]', ']')
            open(self.new_script_path(), 'w').write(output)
            self.btnRecord.SetLabel(u'录制')
            self.stIndicator.SetLabel('finished')
            self.record = []
        else:
            logger.debug('record start')
            self.recording = True
            self.ttt = self.now_ts
            status = self.stIndicator.GetLabel()
            if 'running' in status or 'recorded' in status:
                return
            self.btnRecord.SetLabel(u'\u7ed3\u675f')  # 结束
            self.stIndicator.SetLabel('0 actions recorded')
            self.choice_script.SetSelection(-1)
            self.record = []

        event.Skip()

    def OnBtrunButton(self, event):
        logger.debug('script start by btn')
        t = RunScriptClass(self, self.pause_event)
        t.start()
        event.Skip()

    def OnBtpauseButton(self, event):
        logger.debug('script pause button pressed')
        if self.paused:
            logger.debug('script is resumed')
            self.pause_event.set()
            self.paused = False
            self.btnpause.SetLabel(u'暂停')  # 暂停
        else:
            logger.debug('script is paused')
            self.pause_event.clear()
            self.paused = True
            self.btnpause.SetLabel(u'继续')  # 继续
        event.Skip()

    def OnChoice_startChoice(self, event):
        event.Skip()

    def OnChoice_stopChoice(self, event):
        event.Skip()


class RunScriptClass(threading.Thread):

    def __init__(self, frame: MainFrame, event: threading.Event):
        self.frame = frame
        self.event = event
        self.event.set()
        super(RunScriptClass, self).__init__()

    def run(self):

        status = self.frame.stIndicator.GetLabel()
        if self.frame.running or self.frame.recording:
            return

        if 'running' in status or 'recorded' in status:
            return

        script_path = self.frame.get_script_path()
        if not script_path:
            self.frame.stIndicator.SetLabel(
                'script not found, please self.record first!')
            return

        self.frame.running = True

        s = None
        try:
            with script_path.open('r', encoding='utf-8') as fp:
                s = json.load(fp)
        except Exception as e:
            logger.debug('Exception: {}'.format(e))
            # traceback.print_exc()
            self.frame.stIndicator.SetLabel('载入脚本失败！')
            self.frame.tstop.Shown = False
            self.frame.running = False
        else:
            steps = len(s)
            run_times = self.frame.stimes.Value
            running_text = '%s running..' % script_path.name
            self.frame.stIndicator.SetLabel(running_text)
            self.frame.tstop.Shown = True
            mouse_ctl = mouse.Controller()
            keyboard_ctl = keyboard.Controller()
            j = 0
            while j < run_times or run_times == 0:
                start_time = time.time()
                j += 1
                if self.frame.stIndicator.GetLabel() == 'broken' or self.frame.stIndicator.GetLabel() == 'finished':
                    self.frame.running = False
                    break
                for i in range(steps):
                    self.event.wait()
                    logger.debug(s[i])
                    # for old style script
                    if isinstance(s[i][0], str) and isinstance(s[i][3], int):
                        s[i].insert(0, s[i][3])
                    delay = s[i][0]
                    event_type = s[i][1]
                    message = s[i][2]
                    action = s[i][3]
                    message = message.lower()
                    time.sleep(delay / 1000.0)
                    if self.frame.stIndicator.GetLabel() == 'broken' or self.frame.stIndicator.GetLabel() == 'finished':
                        break
                    text = '%s  [%d/%d %d/%d]' % (running_text,
                                                  i+1, steps, j, run_times)
                    self.frame.stIndicator.SetLabel(text)
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
                            logger.debug('unknow mouse event:', message)
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
                            logger.debug('unknow keyboard event:', message)
                end_time = time.time()
                logger.debug('耗时：{}'.format(end_time-start_time))
            self.frame.stIndicator.SetLabel('finished')
            self.frame.tstop.Shown = False
            self.frame.running = False
            logger.debug('script run finish!')

        # except Exception as e:
        #     print('run error', e)
        #     traceback.print_exc()
        #     self.frame.stIndicator.SetLabel('failed')
        #     self.frame.tstop.Shown = False
        #     self.frame.running = False


class TaskBarIcon(wxTaskBarIcon):
    ID_About = wx.NewId()
    ID_Closeshow = wx.NewId()

    def __init__(self, frame):
        wxTaskBarIcon.__init__(self)
        self.frame = frame
        self.SetIcon(GetMondrianIcon())
        self.Bind(EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBarLeftDClick)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=self.ID_About)
        self.Bind(wx.EVT_MENU, self.OnCloseshow, id=self.ID_Closeshow)

    def OnTaskBarLeftDClick(self, event):
        if self.frame.IsIconized():
            self.frame.Iconize(False)
        if not self.frame.IsShown():
            self.frame.Show(True)
        self.frame.Raise()

    def OnAbout(self, event):
        wx.MessageBox('https://github.com/taojy123/KeymouseGo', 'KeymouseGo')
        event.Skip()

    def OnCloseshow(self, event):
        self.frame.Close(True)
        event.Skip()

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(self.ID_About, 'About')
        menu.Append(self.ID_Closeshow, 'Exit')
        return menu

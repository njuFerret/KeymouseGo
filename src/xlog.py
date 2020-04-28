import pathlib
from datetime import datetime
import logging


START = datetime.now()


# @Singleton      # 如需打印不同路径的日志（运行日志、审计日志），则不能使用单例模式（注释或删除此行）。此外，还需设定参数name。
class Logger:
    def __init__(self):
        self.__logger = logging.getLogger("key_mouse")
        self.setupLogger()

    def setupLogger(self,  logLevel=logging.DEBUG):

        logFileName = pathlib.Path(__file__).with_name("..").resolve()
        logFileName = logFileName / 'logs'
        logFileName.mkdir(parents=True, exist_ok=True)
        self.logFileName = logFileName / \
            format(START, 'keymouse_%Y%m%d-%H%M%S.log')

        self.__logger.setLevel(logLevel)
        self.setLevel(logLevel)  # 设置日志级别
        self.propagate = False
        fh = logging.FileHandler(self.logFileName, 'w', 'utf-8')
        ch = logging.StreamHandler()
        if logLevel == logging.DEBUG:
            fmtStr = '%(filename)15s(%(lineno)04d) [%(levelname)-8s]: %(message)s'
        else:
            fmtStr = '%(message)s'
        logFmt = logging.Formatter(fmt=fmtStr, datefmt='%Y-%m-%d %H:%M:%S')
        fh.setFormatter(logFmt)
        ch.setFormatter(logFmt)
        self.__logger.addHandler(fh)
        self.__logger.addHandler(ch)

    def __getattr__(self, item):
        return getattr(self.logger, item)

    @property
    def logger(self):
        return self.__logger

    @logger.setter
    def logger(self, func):
        self.__logger = func

    def __del__(self):
        for hdl in self.handlers[:]:
            hdl.close()
            self.removeHandler(hdl)


class EnterExitLog():
    def __init__(self, funcName):
        self.funcName = funcName

    def __enter__(self):
        global xlog
        xlog.debug('[Call Begin]: %s' % self.funcName)
        # self.init_time = datetime.datetime.now()
        return self

    def __exit__(self, type, value, tb):
        global xlog
        xlog.debug('[ Call End ]: %s ' % (self.funcName))


def func_call_decorator(func):
    def func_wrapper(*args, **kwargs):
        with EnterExitLog(func.__name__):
            return func(*args, **kwargs)

    return func_wrapper


def getLogger():
    global xlog
    return xlog


xlog = Logger()

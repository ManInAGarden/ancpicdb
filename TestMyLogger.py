import unittest
import mylogger as mylo
import tempfile
import os
import shutil
import datetime as dt
import queue

class TestMyLogger(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self._filestack = queue.SimpleQueue()

    def tearDown(self):
        while not self._filestack.empty():
            fname = self._filestack.get()
            try: 
                os.remove(fname) 
            except Exception as exc:
                pass

        return super().tearDown()


    def _get_tempfile(self, name):
        tmpdir = tempfile.gettempdir()
        tfname = os.path.join(tmpdir, name)
        self._filestack.put(tfname)

        return tfname
    
    def test_logger_initiation(self):
        logger = mylo.Logger(mylo.LogLevelEnum.DEBUG)

        assert logger.level == mylo.LogLevelEnum.DEBUG

        handler = logger.add_handler(mylo.StreamHandler()) #creates a handler logging to stderror
        assert handler is not None
        assert type(handler) is mylo.StreamHandler
        logger.info("my first message is '{}.'", "Hi!")

    def test_stream_handler(self):
        sh = mylo.StreamHandler() #std stream handler writes to stderr
        sh.write("Hello world!")

    def test_rotating_file_handler(self):
        tfname = self._get_tempfile("testrot.log")
        rfh = mylo.RotatingFileHandler(tfname)

        msg = "Hallo Welt!"
        rfh.write(msg)

        with open(tfname, "r") as f:
            msg_rs = f.readlines()

        msg_r = msg_rs[-1]
        assert msg + "\n" == msg_r

    def test_logger_rotating(self):
        tfname = self._get_tempfile("testrotlogger.log")
        logger = mylo.Logger(mylo.LogLevelEnum.DEBUG)
        logger.add_handler(mylo.RotatingFileHandler(tfname))
        logger.info("Hi there")
        logger.warning("Oh my god it's already {:%H:%M:%S}", dt.datetime.now())
        logger.debug("I just wanted to tell you that this is the second line in the file")
        val = 7
        logger.error("You should'nt have startet this test. Value is<{}>", val)

        with open(tfname, "r") as f:
            lines = f.readlines()
            
        assert lines[-4].endswith("Hi there\n")
        assert lines[-3].find("WARNING: Oh my god it's already") >= 0
        assert lines[-2].endswith("DEBUG: I just wanted to tell you that this is the second line in the file\n")
        assert lines[-1].endswith("ERROR: You should'nt have startet this test. Value is<7>\n")

    def test_logger_two_handlers(self):
        tfname = self._get_tempfile("testrotlogger2.log")
        logger = mylo.Logger(mylo.LogLevelEnum.DEBUG)
        logger.add_handler(mylo.RotatingFileHandler(tfname))
        logger.add_handler(mylo.StreamHandler())
        logger.info("Hi there")
        logger.warning("Oh my god it's already {:%H:%M:%S}", dt.datetime.now())
        logger.debug("I just wanted to tell you that this is the second line in the file")
        val = 7
        logger.error("You should'nt have startet this test. Value is<{}>", val)

        with open(tfname, "r") as f:
            lines = f.readlines()
            
        assert lines[-4].endswith("Hi there\n")
        assert lines[-3].find("WARNING: Oh my god it's already") >= 0
        assert lines[-2].endswith("DEBUG: I just wanted to tell you that this is the second line in the file\n")
        assert lines[-1].endswith("ERROR: You should'nt have startet this test. Value is<7>\n")

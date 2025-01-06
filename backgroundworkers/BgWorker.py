from threading import Thread

class BgWorker(Thread):
    def __init__(self, notifywin):
        super().__init__()
        self.notifywin = notifywin
        self.abortreq = False

    def run(self):
        raise Exception("Override method 'run' in your derived background worker class!")
    
    def requestabort(self):
        """request thread to be aborted when possible"""
        self.abortreq = True

    @property
    def abortrequested(self):
        """check wether abort has been requested"""
        return self.abortreq == True
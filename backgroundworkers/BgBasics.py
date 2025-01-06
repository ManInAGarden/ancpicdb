import wx


# Define notification event for thread completion
EVT_RESULT_ID = wx.NewId()
EVT_NOTIFYPERC_ID = wx.NewId()

def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)

def EVT_NOTIFY_PERC(win, func):
    """Define Notification Event."""
    win.Connect(-1, -1, EVT_NOTIFYPERC_ID, func)

class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data):
      """Init Result Event."""
      wx.PyEvent.__init__(self)
      self.SetEventType(EVT_RESULT_ID)
      self.data = data

class NotifyPercentEvent(wx.PyEvent):
    def __init__(self, perc):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_NOTIFYPERC_ID)
        self.data = perc













        



        

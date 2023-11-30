import wx
import logging

class GuiHelper:
    """ class to help with ever repeating gui oprations"""

    @classmethod
    def get_selected_item(cls, lstctrl : wx.ListCtrl, lst : list):
        """ get the selected item from lst according to the selected item in lstctrl
            returns None when nothing was selected"""

        if lst is None or len(lst)==0:
            return None

        sitm = lstctrl.GetFirstSelected()
        if sitm == wx.NOT_FOUND:
            return None
        
        lidx = lstctrl.GetItemData(sitm)
        if lidx is None:
            raise Exception("No item data found for item in listctrl")
        
        if type(lidx) is not int:
            raise Exception("Item data must be int to address items in list")

        if lidx < 0 or lidx > len(lst):
            raise Exception("Index <{}> found in item data is out of range for list of length <{}>".format(lidx, len(lst)))

        return lst[lidx]

    @classmethod
    def show_error(cls, message, *args):
        logger = logging.getLogger("mainprog")
        if logger is not None:
            logformstr = cls._get_loggerformstr(message)
            logger.error(logformstr, *args)

        wx.MessageBox(message.format(*args))

    @classmethod
    def _get_loggerformstr(cls, msg):
        return msg.replace("{}", "%s")
    
    @classmethod
    def ask_user(cls, par : any, mesg : str) ->int :
        msb = wx.MessageDialog(message=mesg, caption="Rückfrage", parent=par, style=wx.YES_NO)
        return msb.ShowModal()
    
    @classmethod
    def set_val(cls, ctrl, val):
        """set value to the ctrl if not none"""

        ct = type(ctrl)
        if ct is wx.TextCtrl:
            if val is not None:
                ctrl.SetValue(val)
            else:
                ctrl.SetValue("")
        elif ct is wx.adv.DatePickerCtrl:
            if val is not None:
                ctrl.SetValue(wx.pydate2wxdate(val))
            else:
                ctrl.SetValue(wx.InvalidDateTime)
        else:
            raise Exception("Unknown control type in _set_val")
        
    @classmethod
    def get_val(cls, ctrl):
        """get value from the ctrl"""
        
        ctt = type(ctrl)
        if ctt is wx.adv.DatePickerCtrl:
            val = ctrl.GetValue()
            if val is wx.InvalidDateTime:
                return None
            else:
                return wx.wxdate2pydate(val)
        elif ctt is wx.TextCtrl:
            val = ctrl.GetValue()
            if val is None or len(val)==0:
                return None
            else:
                return val
        else:
            raise Exception("Unknown type {} in _get_val()".format(ctt))
        
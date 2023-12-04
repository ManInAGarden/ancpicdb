import wx
import logging
import sqlitepersist as sqp

class GuiHelper:
    """ class to help with ever repeating gui oprations"""

    @classmethod 
    def get_selected_fromlb(cls, lstbox : wx.ListBox, lst : list):
        """get the currently selected item of a ListBox. Returns None when nothing was selected"""
        if lst is None or len(lst)==0:
            return None, None

        lidx = lstbox.GetSelection()
        if lidx == wx.NOT_FOUND:
            return None, None
        
        if lidx < 0 or lidx > len(lst):
            raise Exception("Index <{}> found in item data is out of range for list of length <{}>".format(lidx, len(lst)))

        return lst[lidx], lidx
        
    @classmethod
    def get_selected_fromlctrl(cls, lstctrl : wx.ListCtrl, lst : list):
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
    def set_val(cls, ctrl, val, fullcat=None):
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
        elif ct is wx.ComboBox:
            if issubclass(type(val), sqp.PCatalog):
                itemss = list(map(lambda p: p.value, fullcat))
                ctrl.AppendItems(itemss)
                ct = 0
                for s in itemss:
                    if s == val.value:
                        ctrl.SetSelection(ct)
                        break
                    ct += 1
                    
            else:
                raise Exception("Combobox with non catalog not yet handled in GUIHelper.SetVal")
        else:
            raise Exception("Unknown control type in _set_val")
        
    @classmethod
    def get_val(cls, ctrl, datal : list=None):
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
        elif ctt is wx.ComboBox:
            selpo = ctrl.GetSelection()
            if selpo != wx.NOT_FOUND:
                return datal[selpo]
        else:
            raise Exception("Unknown type {} in _get_val()".format(ctt))
        
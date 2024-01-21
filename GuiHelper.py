import os, subprocess, platform
import wx
import logging
import sqlitepersist as sqp

class GuiHelper:
    """ class to help with ever repeating gui oprations. Uses a formstr when given."""

    @classmethod
    def get_eos(cls, val, formstr = None):
        """Get string repr. for val or an empty string when val is None"""
        if val is None:
            return ""
        
        if formstr is not None:
            formstr.format(val)

        return val.__str__()
    
    @classmethod 
    def get_selected_fromlb(cls, lstbox : wx.ListBox, lst : list) -> (object, int):
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

        #return the selected data object
        return lst[lidx]

    @classmethod
    def show_error(cls, message, *args):
        logger = logging.getLogger("mainprog")
        if logger is not None:
            logformstr = cls._get_loggerformstr(message)
            logger.error(logformstr, *args)

        wx.MessageBox(message.format(*args))

    @classmethod
    def show_message(cls, message, *args):
        logger = logging.getLogger("mainprog")
        if logger is not None:
            logformstr = cls._get_loggerformstr(message)
            logger.info(logformstr, *args)

        wx.MessageBox(message.format(*args))

    @classmethod
    def _get_loggerformstr(cls, msg):
        return msg.replace("{}", "%s")
    
    @classmethod
    def ask_user(cls, par : any, mesg : str) ->int :
        msb = wx.MessageDialog(message=mesg, caption="Rückfrage", parent=par, style=wx.YES_NO)
        return msb.ShowModal()
    
    @classmethod
    def set_sqp_objval(cls, ctrl, val, strfunc, fullcat=None):
        """set value to the ctrl assuming val is an sqp-objeck and its str representation shall be displayed"""

        ct = type(ctrl)
        if ct is wx.ComboBox:
            if val is None:
                itemss = list(map(lambda p: strfunc(p), fullcat))
                ctrl.AppendItems(itemss)
                ctrl.SetSelection(wx.NOT_FOUND)
            elif issubclass(type(val), sqp.PBase):
                itemss = list(map(lambda p: strfunc(p), fullcat))
                ctrl.AppendItems(itemss)
                ct = 0
                for obj in fullcat:
                    if obj._id == val._id:
                        ctrl.SetSelection(ct)
                        break
                    ct += 1
   
            else:
                raise Exception("Combobox with non sqlite persist data type value not yet handled in GUIHelper.set_sqp_objval")
        else:
            raise Exception("Unhandled control type in set_sqp_objval")
        
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
        elif ct is wx.SpinCtrl:
            if val is not None:
                ctrl.SetValue(val)
            else:
                ctrl.SetValue(0)
        elif ct is wx.CheckBox:
            if val is not None:
                if type(val) is bool:
                    ctrl.SetValue(val)
                else:
                    raise Exception("Unknown data type in GuiHelper.SetVal for a wx.CtrlBox")
            else:
                ctrl.SetVal(False)
        elif ct is wx.ComboBox:
            if val is None:
                itemss = list(map(lambda p: p.value, fullcat))
                ctrl.AppendItems(itemss)
                ctrl.SetSelection(wx.NOT_FOUND)
            elif issubclass(type(val), sqp.PCatalog):
                itemss = list(map(lambda p: p.value, fullcat))
                ctrl.AppendItems(itemss)
                ct = 0
                for s in itemss:
                    if s == val.value:
                        ctrl.SetSelection(ct)
                        break
                    ct += 1
   
            else:
                raise Exception("Combobox with non catalog data value not yet handled in GUIHelper.SetVal")
        elif ct is wx.FilePickerCtrl:
            if val is not None:
                ctrl.SetPath(val)
            else:
                ctrl.SetPath("")
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
        elif ctt is wx.SpinCtrl:
            val = ctrl.GetValue()
            return val
        elif ctt is wx.CheckBox:
            val = ctrl.GetValue()
            return val
        elif ctt is wx.FilePickerCtrl:
            return ctrl.GetPath()
        else:
            raise Exception("Unknown type {} in _get_val()".format(ctt))
        
    @classmethod
    def get_sqp_objval(cls, ctrl, datal : list=None):
        """get value from the ctrl assuming its a sqp object"""
        
        ctt = type(ctrl)
        if ctt is wx.ComboBox:
            selpo = ctrl.GetSelection()
            if selpo != wx.NOT_FOUND:
                return datal[selpo]
            else:
                return None
        else:
            raise Exception("Unknown control type {} in get_sqp_objval()".format(ctt))
        
    @classmethod
    def _add_node(cls, ctrl, topnode, under):
        if under is None:
            return
        
        if type(under) is dict:
            for key, val in under.items():
                node = ctrl.AppendItem(topnode, key)
                cls._add_node(ctrl, node, val)
        else:
            raise Exception("Unhandled datatype in node hierarchy")

    @classmethod
    def add_nodes(cls, ctrl, strdict : dict):
        root = ctrl.AddRoot('invisible root')
        for key, val in strdict.items():
            partnode = ctrl.AppendItem(root, key)
            cls._add_node(ctrl, partnode, val)

    @classmethod
    def openbysys(cls, filepath):
        if not os.path.isfile(filepath):
            cls.show_error("Der Dateipfad %s kann nicht geöffnet werden.", filepath)
            return
        
        """let the operating system open a file"""
        if platform.system() == 'Darwin':       # macOS
            subprocess.call(('open', filepath))
        elif platform.system() == 'Windows':    # Windows
            os.startfile(filepath)
        else:                                   # linux variants
            subprocess.call(('xdg-open', filepath))
#===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.    If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import wx
from gui.bitmapLoader import BitmapLoader
import service
from wx.lib.intctrl import IntCtrl
from gui.utils.clipboard import toClipboard, fromClipboard
from service.damagePattern import ImportError
from gui.builtinViews.entityEditor import EntityEditor, BaseValidator
###########################################################################
## Class DmgPatternEditorDlg
###########################################################################

class DmgPatternTextValidor(BaseValidator):
    def __init__(self):
        BaseValidator.__init__(self)

    def Clone(self):
        return DmgPatternTextValidor()

    def Validate(self, win):
        entityEditor = win.parent
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue().strip()

        try:
            if len(text) == 0:
                raise ValueError("You must supply a name for your Damage Profile!")
            elif text in [x.name for x in entityEditor.choices]:
                raise ValueError("Damage Profile name already in use, please choose another.")

            return True
        except ValueError, e:
            wx.MessageBox(u"{}".format(e), "Error")
            textCtrl.SetFocus()
            return False


class DmgPatternEntityEditor(EntityEditor):
    def __init__(self, parent):
        EntityEditor.__init__(self, parent, "Damage Profile")
        self.SetEditorValidator(DmgPatternTextValidor)

    def getEntitiesFromContext(self):
        sDP = service.DamagePattern.getInstance()
        choices = sorted(sDP.getDamagePatternList(), key=lambda p: p.name)
        return [c for c in choices if c.name != "Selected Ammo"]

    def DoNew(self, name):
        sDP = service.DamagePattern.getInstance()
        return sDP.newPattern(name)

    def DoRename(self, entity, name):
        sDP = service.DamagePattern.getInstance()
        sDP.renamePattern(entity, name)

    def DoCopy(self, entity, name):
        sDP = service.DamagePattern.getInstance()
        copy = sDP.copyPattern(entity)
        sDP.renamePattern(copy, name)
        return copy

    def DoDelete(self, entity):
        sDP = service.DamagePattern.getInstance()
        sDP.deletePattern(entity)

class DmgPatternEditorDlg(wx.Dialog):
    DAMAGE_TYPES = ("em", "thermal", "kinetic", "explosive")

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id = wx.ID_ANY, title = u"Damage Pattern Editor", size = wx.Size( 400,240 ))

        self.block = False
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.entityEditor = DmgPatternEntityEditor(self)
        mainSizer.Add(self.entityEditor, 0, wx.ALL | wx.EXPAND, 2)

        self.sl = wx.StaticLine(self)
        mainSizer.Add(self.sl, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        contentSizer = wx.BoxSizer(wx.VERTICAL)
        self.embitmap = BitmapLoader.getBitmap("em_big", "gui")
        self.thermbitmap = BitmapLoader.getBitmap("thermal_big", "gui")
        self.kinbitmap = BitmapLoader.getBitmap("kinetic_big", "gui")
        self.expbitmap = BitmapLoader.getBitmap("explosive_big", "gui")

        dmgeditSizer = wx.FlexGridSizer(2, 6, 0, 2)
        dmgeditSizer.AddGrowableCol(0)
        dmgeditSizer.AddGrowableCol(5)
        dmgeditSizer.SetFlexibleDirection(wx.BOTH)
        dmgeditSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        width = -1
        defSize = wx.Size(width,-1)

        for i, type in enumerate(self.DAMAGE_TYPES):
            bmp = wx.StaticBitmap(self, wx.ID_ANY, BitmapLoader.getBitmap("%s_big"%type, "gui"))
            if i%2:
                style = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.LEFT
                border = 20
            else:
                style = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT
                border = 5

            # set text edit
            setattr(self, "%sEdit"%type, IntCtrl(self, wx.ID_ANY, 0, wx.DefaultPosition, defSize))
            setattr(self, "%sPerc"%type, wx.StaticText(self, wx.ID_ANY, u"0%"))
            editObj = getattr(self, "%sEdit"%type)

            dmgeditSizer.Add(bmp, 0, style, border)
            dmgeditSizer.Add(editObj, 0, wx.BOTTOM | wx.TOP | wx.ALIGN_CENTER_VERTICAL, 5)
            dmgeditSizer.Add(getattr(self, "%sPerc"%type), 0,  wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 5)

            editObj.Bind(wx.EVT_TEXT, self.ValuesUpdated)
            editObj.SetLimited(True)
            editObj.SetMin(0)
            editObj.SetMax(2000000)

        contentSizer.Add(dmgeditSizer, 1, wx.EXPAND | wx.ALL, 5)
        self.slfooter = wx.StaticLine(self)
        contentSizer.Add(self.slfooter, 0, wx.EXPAND | wx.TOP, 5)

        footerSizer = wx.BoxSizer(wx.HORIZONTAL)
        perSizer = wx.BoxSizer(wx.VERTICAL)

        self.stNotice = wx.StaticText(self, wx.ID_ANY, u"")
        self.stNotice.Wrap(-1)
        perSizer.Add(self.stNotice, 0, wx.BOTTOM | wx.TOP | wx.LEFT, 5)

        footerSizer.Add(perSizer, 1,  wx.ALIGN_CENTER_VERTICAL, 5)

        self.totSizer = wx.BoxSizer(wx.VERTICAL)

        contentSizer.Add(footerSizer, 0, wx.EXPAND, 5)

        mainSizer.Add(contentSizer, 1, wx.EXPAND, 0)

        if "wxGTK" in wx.PlatformInfo:
            self.closeBtn = wx.Button( self, wx.ID_ANY, u"Close", wx.DefaultPosition, wx.DefaultSize, 0 )
            mainSizer.Add( self.closeBtn, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
            self.closeBtn.Bind(wx.EVT_BUTTON, self.closeEvent)

        self.SetSizer(mainSizer)

        importExport = (("Import", wx.ART_FILE_OPEN, "from"),
                        ("Export", wx.ART_FILE_SAVE_AS, "to"))

        for name, art, direction in importExport:
                bitmap = wx.ArtProvider.GetBitmap(art, wx.ART_BUTTON)
                btn = wx.BitmapButton(self, wx.ID_ANY, bitmap)

                btn.SetMinSize( btn.GetSize() )
                btn.SetMaxSize( btn.GetSize() )

                btn.Layout()
                setattr(self, name, btn)
                btn.Enable(True)
                btn.SetToolTipString("%s patterns %s clipboard" % (name, direction) )
                footerSizer.Add(btn, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_RIGHT)
                btn.Bind(wx.EVT_BUTTON, getattr(self, "{}Patterns".format(name.lower())))

        self.Layout()
        bsize = self.GetBestSize()
        self.SetSize((-1, bsize.height))
        self.CenterOnParent()

        self.Bind(wx.EVT_CHOICE, self.patternChanged)

        self.patternChanged()

    def closeEvent(self, event):
        self.Destroy()

    def ValuesUpdated(self, event=None):
        if self.block:
            return

        p = self.entityEditor.getActiveEntity()
        total = sum(map(lambda attr: getattr(self, "%sEdit"%attr).GetValue(), self.DAMAGE_TYPES))
        for type in self.DAMAGE_TYPES:
                editObj = getattr(self, "%sEdit"%type)
                percObj = getattr(self, "%sPerc"%type)
                setattr(p, "%sAmount"%type, editObj.GetValue())
                percObj.SetLabel("%.1f%%"%(float(editObj.GetValue())*100/total if total > 0 else 0))

        self.totSizer.Layout()

        if event is not None:
            event.Skip()

        service.DamagePattern.getInstance().saveChanges(p)

    def restrict(self):
        for type in self.DAMAGE_TYPES:
            editObj = getattr(self, "%sEdit"%type)
            editObj.Enable(False)
        self.entityEditor.btnRename.Enable(False)
        self.entityEditor.btnDelete.Enable(False)

    def unrestrict(self):
        for type in self.DAMAGE_TYPES:
            editObj = getattr(self, "%sEdit"%type)
            editObj.Enable()
        self.entityEditor.btnRename.Enable()
        self.entityEditor.btnDelete.Enable()

    def patternChanged(self, event=None):
        p = self.entityEditor.getActiveEntity()

        if p is None:
            return

        if p.name == "Uniform" or p.name == "Selected Ammo":
            self.restrict()
        else:
            self.unrestrict()

        self.block = True

        for field in self.DAMAGE_TYPES:
            edit = getattr(self, "%sEdit" % field)
            amount = int(round(getattr(p, "%sAmount" % field)))
            edit.SetValue(amount)

        self.block = False
        self.ValuesUpdated()

    def __del__(self):
        pass

    def importPatterns(self, event):
        text = fromClipboard()
        if text:
            sDP = service.DamagePattern.getInstance()
            try:
                sDP.importPatterns(text)
                self.stNotice.SetLabel("Patterns successfully imported from clipboard")
            except service.damagePattern.ImportError, e:
                self.stNotice.SetLabel(str(e))
            except Exception, e:
                self.stNotice.SetLabel("Could not import from clipboard: unknown errors")
            finally:
                self.entityEditor.refreshEntityList()
        else:
            self.stNotice.SetLabel("Could not import from clipboard")

    def exportPatterns(self, event):
        sDP = service.DamagePattern.getInstance()
        toClipboard( sDP.exportPatterns() )
        self.stNotice.SetLabel("Patterns exported to clipboard")

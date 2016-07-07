#===============================================================================
# Copyright (C) 2014 Ryan Holmes
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
from gui.utils.clipboard import toClipboard, fromClipboard
from service.targetResists import ImportError
from gui.builtinViews.entityEditor import EntityEditor, BaseValidator


class TargetResistsTextValidor(BaseValidator):
    def __init__(self):
        BaseValidator.__init__(self)

    def Clone(self):
        return TargetResistsTextValidor()

    def Validate(self, win):
        entityEditor = win.parent
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue().strip()

        try:
            if len(text) == 0:
                raise ValueError("You must supply a name for your Target Resist Profile!")
            elif text in [x.name for x in entityEditor.choices]:
                raise ValueError("Target Resist Profile name already in use, please choose another.")

            return True
        except ValueError, e:
            wx.MessageBox(u"{}".format(e), "Error")
            textCtrl.SetFocus()
            return False


class TargetResistsEntityEditor(EntityEditor):
    def __init__(self, parent):
        EntityEditor.__init__(self, parent, "Target Resist Profile")
        self.SetEditorValidator(TargetResistsTextValidor)

    def getEntitiesFromContext(self):
        sTR = service.TargetResists.getInstance()
        choices = sorted(sTR.getTargetResistsList(), key=lambda p: p.name)
        return choices

    def DoNew(self, name):
        sTR = service.TargetResists.getInstance()
        return sTR.newPattern(name)

    def DoRename(self, entity, name):
        sTR = service.TargetResists.getInstance()
        sTR.renamePattern(entity, name)

    def DoCopy(self, entity, name):
        sTR = service.TargetResists.getInstance()
        copy = sTR.copyPattern(entity)
        sTR.renamePattern(copy, name)
        return copy

    def DoDelete(self, entity):
        sTR = service.TargetResists.getInstance()
        sTR.deletePattern(entity)

class ResistsEditorDlg(wx.Dialog):

    DAMAGE_TYPES = ("em", "thermal", "kinetic", "explosive")

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id = wx.ID_ANY, title = u"Target Resists Editor", size = wx.Size( 350,240 ))

        self.block = False
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.entityEditor = TargetResistsEntityEditor(self)
        mainSizer.Add(self.entityEditor, 0, wx.ALL | wx.EXPAND, 2)

        self.sl = wx.StaticLine(self)
        mainSizer.Add(self.sl, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        contentSizer = wx.BoxSizer(wx.VERTICAL)

        resistEditSizer = wx.FlexGridSizer(2, 6, 0, 2)
        resistEditSizer.AddGrowableCol(0)
        resistEditSizer.AddGrowableCol(5)
        resistEditSizer.SetFlexibleDirection(wx.BOTH)
        resistEditSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        width = -1
        defSize = wx.Size(50,-1)

        for i, type in enumerate(self.DAMAGE_TYPES):
            if i%2:
                style = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.LEFT
                border = 25
            else:
                style = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT
                border = 5

            bmp = wx.StaticBitmap(self, wx.ID_ANY, BitmapLoader.getBitmap("%s_big"%type, "gui"))
            resistEditSizer.Add(bmp, 0, style, border)
            # set text edit
            setattr(self, "%sEdit"%type, wx.TextCtrl(self, wx.ID_ANY, "", wx.DefaultPosition, defSize))
            editObj = getattr(self, "%sEdit"%type)
            resistEditSizer.Add(editObj, 0, wx.BOTTOM | wx.TOP | wx.ALIGN_CENTER_VERTICAL, 5)
            resistEditSizer.Add(wx.StaticText( self, wx.ID_ANY, u"%", wx.DefaultPosition, wx.DefaultSize, 0 ), 0, wx.BOTTOM | wx.TOP | wx.ALIGN_CENTER_VERTICAL, 5)
            editObj.Bind(wx.EVT_TEXT, self.ValuesUpdated)

        # Color we use to reset invalid value color
        self.colorReset = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)

        contentSizer.Add(resistEditSizer, 1, wx.EXPAND | wx.ALL, 5)
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

        if not self.entityEditor.checkEntitiesExist():
            self.Destroy()
            return

        self.Layout()
        bsize = self.GetBestSize()
        self.SetSize((-1, bsize.height))
        self.CenterOnParent()

        self.Bind(wx.EVT_CHOICE, self.patternChanged)

        self.patternChanged()

        self.ShowModal()

    def closeEvent(self, event):
        self.Destroy()

    def ValuesUpdated(self, event=None):
        '''
        Event that is fired when resists values change. Iterates through all
        resist edit fields. If blank, sets it to 0.0. If it is not a proper
        decimal value, sets text color to red and refuses to save changes until
        issue is resolved
        '''
        if self.block:
            return

        try:
            p = self.entityEditor.getActiveEntity()

            for type in self.DAMAGE_TYPES:
                editObj = getattr(self, "%sEdit"%type)

                if editObj.GetValue() == "":
                    # if we are blank, overwrite with 0
                    editObj.ChangeValue("0.0")
                    editObj.SetInsertionPointEnd()

                value = float(editObj.GetValue())

                # assertion, because they're easy
                assert 0 <= value <= 100

                # if everything checks out, set resist attribute
                setattr(p, "%sAmount"%type, value/100)
                editObj.SetForegroundColour(self.colorReset)

            self.stNotice.SetLabel("")
            self.totSizer.Layout()

            if event is not None:
                event.Skip()

            service.TargetResists.getInstance().saveChanges(p)

        except ValueError:
            editObj.SetForegroundColour(wx.RED)
            self.stNotice.SetLabel("Incorrect Formatting (decimals only)")
        except AssertionError:
            editObj.SetForegroundColour(wx.RED)
            self.stNotice.SetLabel("Incorrect Range (must be 0-100)")
        finally:  # Refresh for color changes to take effect immediately
            self.Refresh()

    def patternChanged(self, event=None):
        "Event fired when user selects pattern. Can also be called from script"

        if not self.entityEditor.checkEntitiesExist():
            self.Destroy()
            return

        p = self.entityEditor.getActiveEntity()
        if p is None:
            return

        self.block = True
        # Set new values
        for field in self.DAMAGE_TYPES:
            edit = getattr(self, "%sEdit" % field)
            amount = getattr(p, "%sAmount" % field)*100
            edit.ChangeValue(str(amount))

        self.block = False
        self.ValuesUpdated()

    def __del__( self ):
        pass

    def importPatterns(self, event):
        "Event fired when import from clipboard button is clicked"

        text = fromClipboard()
        if text:
            sTR = service.TargetResists.getInstance()
            try:
                sTR.importPatterns(text)
                self.stNotice.SetLabel("Patterns successfully imported from clipboard")
            except service.targetResists.ImportError, e:
                self.stNotice.SetLabel(str(e))
            except Exception, e:
                self.stNotice.SetLabel("Could not import from clipboard: unknown errors")
            finally:
                self.entityEditor.refreshEntityList()
        else:
            self.stNotice.SetLabel("Could not import from clipboard")

    def exportPatterns(self, event):
        "Event fired when export to clipboard button is clicked"
        sTR = service.TargetResists.getInstance()
        toClipboard( sTR.exportPatterns() )
        self.stNotice.SetLabel("Patterns exported to clipboard")

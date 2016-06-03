import wx
import os

from gui.preferenceView import PreferenceView
from gui.bitmapLoader import BitmapLoader

import gui.mainFrame
import service
import gui.globalEvents as GE


class PFHTMLExportPref ( PreferenceView):
    title = "HTML Export"
    desc  = "HTML Export (File > Export HTML) allows you to export your entire fitting "+\
            "database into an HTML file at the specified location. This file can be "+\
            "used in the in-game browser to easily open and import your fits, or used "+\
            "in a regular web browser to open them at NULL-SEC.com or Osmium."
    desc2 = "Enabling automatic exporting will update the HTML file after any change "+\
            "to a fit is made. Under certain circumstance, this may cause performance issues."
    desc3 = "Preferred website to view fits while not using in-game browser can be selected below."
    desc4 = "Export Fittings in a minmal HTML Version, just containing the Fittingslinks " +\
            "without any visual styling or javscript features"

    def populatePanel( self, panel ):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.HTMLExportSettings = service.settings.HTMLExportSettings.getInstance()
        self.dirtySettings = False
        dlgWidth = panel.GetParent().GetParent().ClientSize.width
        mainSizer = wx.BoxSizer( wx.VERTICAL )

        self.stTitle = wx.StaticText( panel, wx.ID_ANY, self.title, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stTitle.Wrap( -1 )
        self.stTitle.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
        mainSizer.Add( self.stTitle, 0, wx.ALL, 5 )

        self.m_staticline1 = wx.StaticLine( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        mainSizer.Add( self.m_staticline1, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5 )

        self.stDesc = wx.StaticText( panel, wx.ID_ANY, self.desc, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stDesc.Wrap(dlgWidth - 50)
        mainSizer.Add( self.stDesc, 0, wx.ALL, 5 )

        self.PathLinkCtrl = wx.HyperlinkCtrl( panel, wx.ID_ANY, self.HTMLExportSettings.getPath(), u'file:///{}'.format(self.HTMLExportSettings.getPath()), wx.DefaultPosition, wx.DefaultSize, wx.HL_ALIGN_LEFT|wx.NO_BORDER|wx.HL_CONTEXTMENU )
        mainSizer.Add( self.PathLinkCtrl, 0, wx.ALL|wx.EXPAND, 5)

        self.fileSelectDialog = wx.FileDialog(None, "Save Fitting As...", wildcard = "EVE IGB HTML fitting file (*.html)|*.html", style = wx.FD_SAVE)
        self.fileSelectDialog.SetPath(self.HTMLExportSettings.getPath())
        self.fileSelectDialog.SetFilename(os.path.basename(self.HTMLExportSettings.getPath()));

        self.fileSelectButton = wx.Button(panel, -1, "Set export destination", pos=(0,0))
        self.fileSelectButton.Bind(wx.EVT_BUTTON, self.selectHTMLExportFilePath)
        mainSizer.Add( self.fileSelectButton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        self.stDesc2 = wx.StaticText( panel, wx.ID_ANY, self.desc2, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stDesc2.Wrap(dlgWidth - 50)
        mainSizer.Add( self.stDesc2, 0, wx.ALL, 5 )

        self.exportEnabled = wx.CheckBox( panel, wx.ID_ANY, u"Enable automatic HTML export", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.exportEnabled.SetValue(self.HTMLExportSettings.getEnabled())
        self.exportEnabled.Bind(wx.EVT_CHECKBOX, self.OnExportEnabledChange)
        mainSizer.Add( self.exportEnabled, 0, wx.ALL|wx.EXPAND, 5 )
        
        
        
        self.stDesc4 = wx.StaticText( panel, wx.ID_ANY, self.desc4, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stDesc4.Wrap(dlgWidth - 50)
        mainSizer.Add( self.stDesc4, 0, wx.ALL, 5 )        
        
        self.exportMinimal = wx.CheckBox( panel, wx.ID_ANY, u"Enable minimal export Format", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.exportMinimal.SetValue(self.HTMLExportSettings.getMinimalEnabled())
        self.exportMinimal.Bind(wx.EVT_CHECKBOX, self.OnMinimalEnabledChange)
        mainSizer.Add( self.exportMinimal, 0, wx.ALL|wx.EXPAND, 5 )

        self.stDesc3 = wx.StaticText( panel, wx.ID_ANY, self.desc3, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stDesc3.Wrap(dlgWidth - 50)
        mainSizer.Add( self.stDesc3, 0, wx.ALL, 5 )

        websiteSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.stWebsite = wx.StaticText( panel, wx.ID_ANY, u"Website:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stWebsite.Wrap( -1 )
        websiteSizer.Add( self.stWebsite, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.chWebsiteChoices = [ "o.smium.org", "null-sec.com" ]
        self.chWebsiteType = wx.Choice( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, self.chWebsiteChoices, 0 )
        self.chWebsiteType.SetStringSelection( self.HTMLExportSettings.getWebsite() )
        websiteSizer.Add( self.chWebsiteType, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        self.chWebsiteType.Bind(wx.EVT_CHOICE, self.OnCHWebsiteTypeSelect)

        mainSizer.Add( websiteSizer, 0, wx.EXPAND, 5 )

        panel.SetSizer( mainSizer )
        panel.Layout()

    def setPathLinkCtrlValues(self, path):
        self.PathLinkCtrl.SetLabel(self.HTMLExportSettings.getPath())
        self.PathLinkCtrl.SetURL(u'file:///{}'.format(self.HTMLExportSettings.getPath()))
        self.PathLinkCtrl.SetSize(wx.DefaultSize);
        self.PathLinkCtrl.Refresh()

    def selectHTMLExportFilePath(self, event):
        if self.fileSelectDialog.ShowModal() == wx.ID_OK:
            self.HTMLExportSettings.setPath(self.fileSelectDialog.GetPath())
            self.dirtySettings = True
            self.setPathLinkCtrlValues(self.HTMLExportSettings.getPath())

    def OnExportEnabledChange(self, event):
        self.HTMLExportSettings.setEnabled(self.exportEnabled.GetValue())
        
    def OnMinimalEnabledChange(self, event):
        self.HTMLExportSettings.setMinimalEnabled(self.exportMinimal.GetValue())

    def OnCHWebsiteTypeSelect(self, event):
        choice = self.chWebsiteType.GetStringSelection()
        self.HTMLExportSettings.setWebsite(choice)

    def getImage(self):
        return BitmapLoader.getBitmap("prefs_html", "gui")

PFHTMLExportPref.register()

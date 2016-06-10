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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import wx
import gui.mainFrame
from gui.boosterView import BoosterView
from gui.droneView import DroneView
from gui.fighterView import FighterView
from gui.cargoView import CargoView
from gui.implantView import ImplantView
from gui.projectedView import ProjectedView
from gui.pyfatogglepanel import TogglePanel
from gui.gangView import GangView
from gui.bitmapLoader import BitmapLoader

import gui.chromeTabs

class AdditionsPane(TogglePanel):

    def __init__(self, parent):

        TogglePanel.__init__(self, parent, forceLayout = 1)

        self.SetLabel(_("additionsPane_Additions"))
        pane = self.GetContentPane()

        baseSizer = wx.BoxSizer(wx.HORIZONTAL)
        pane.SetSizer(baseSizer)

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        self.notebook = gui.chromeTabs.PFNotebook(pane, False)
        self.notebook.SetMinSize((-1, 1000))

        baseSizer.Add(self.notebook, 1, wx.EXPAND)

        droneImg = BitmapLoader.getImage("drone_small", "gui")
        fighterImg = BitmapLoader.getImage("fighter_small", "gui")
        implantImg = BitmapLoader.getImage("implant_small", "gui")
        boosterImg = BitmapLoader.getImage("booster_small", "gui")
        projectedImg = BitmapLoader.getImage("projected_small", "gui")
        gangImg = BitmapLoader.getImage("fleet_fc_small", "gui")
        cargoImg = BitmapLoader.getImage("cargo_small", "gui")

        self.notebook.AddPage(DroneView(self.notebook), _("additionsPane_Drones"), tabImage = droneImg, showClose = False)
        self.notebook.AddPage(FighterView(self.notebook), _("additionsPane_Fighters"), tabImage = fighterImg, showClose = False)
        self.notebook.AddPage(CargoView(self.notebook), _("additionsPane_Cargo"), tabImage = cargoImg, showClose = False)
        self.notebook.AddPage(ImplantView(self.notebook), _("additionsPane_Implants"), tabImage = implantImg, showClose = False)
        self.notebook.AddPage(BoosterView(self.notebook), _("additionsPane_Boosters"), tabImage = boosterImg, showClose = False)

        self.projectedPage = ProjectedView(self.notebook)
        self.notebook.AddPage(self.projectedPage, _("additionsPane_Projected"), tabImage = projectedImg, showClose = False)

        self.gangPage = GangView(self.notebook)
        self.notebook.AddPage(self.gangPage, _("additionsPane_Fleet"), tabImage = gangImg, showClose = False)
        self.notebook.SetSelection(0)

    PANES = [_("additionsPane_Drones"), _("additionsPane_Fighters"), _("additionsPane_Cargo"), _("additionsPane_Implants"), _("additionsPane_Boosters"), _("additionsPane_Projected"), _("additionsPane_Fleet")]
    def select(self, name):
        self.notebook.SetSelection(_("additionsPane_" + self.PANES.index(name)))

    def getName(self, idx):
        return self.PANES[idx]

    def toggleContent(self, event):
        TogglePanel.toggleContent(self, event)
        h = self.headerPanel.GetSize()[1]+4

        if self.IsCollapsed():
            self.old_pos = self.parent.GetSashPosition()
            self.parent.SetMinimumPaneSize(h)
            self.parent.SetSashPosition(h*-1, True)
            # only available in >= wx2.9
            if getattr(self.parent, "SetSashInvisible", None):
                self.parent.SetSashInvisible(True)
        else:
            if getattr(self.parent, "SetSashInvisible", None):
                self.parent.SetSashInvisible(False)
            self.parent.SetMinimumPaneSize(200)
            self.parent.SetSashPosition(self.old_pos, True)


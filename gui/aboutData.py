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
import config

versionString = "{0} {1} - {2} {3}".format(config.version, config.tag, config.expansionName, config.expansionVersion)
licenses = (
    _("aboutData_license_line_1"),
    _("aboutData_license_line_2"),
    _("aboutData_license_line_3"),
    _("aboutData_license_line_4")
)
developers = (
    "blitzmann \t(Sable Blitzmann) (maintainer)",
    "cncfanatics \t(Sakari Orisi)" ,
    "DarkPhoenix \t(Kadesh Priestess)",
    "Darriele \t\t(Darriele)")
credits = (
    "Entity (Entity) \tCapacitor calculations / EVEAPI python lib / Reverence",
    "Aurora \t\tMaths",
    "Corollax (Aamrr) \tVarious EOS / pyfa improvements",
    "Dreae (Dreae)\tPyCrest")
description = (
    _("aboutData_description_line_1"),
    _("aboutData_description_line_2"),
    _("aboutData_description_line_3")
)

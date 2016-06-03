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

import cPickle
import os.path
import config
import urllib2

class SettingsProvider():
    BASE_PATH = os.path.join(config.savePath, "settings")
    settings = {}
    _instance = None
    @classmethod
    def getInstance(cls):
        if cls._instance == None:
            cls._instance = SettingsProvider()

        return cls._instance

    def __init__(self):
        if not os.path.exists(self.BASE_PATH):
            os.mkdir(self.BASE_PATH);

    def getSettings(self, area, defaults=None):

        s = self.settings.get(area)
        if s is None:
            p = os.path.join(self.BASE_PATH, area)

            if not os.path.exists(p):
                info = {}
                if defaults:
                    for item in defaults:
                        info[item] = defaults[item]

            else:
                try:
                    f = open(p, "rb")
                    info = cPickle.load(f)
                    for item in defaults:
                        if item not in info:
                            info[item] = defaults[item]

                except:
                    info = {}
                    if defaults:
                        for item in defaults:
                            info[item] = defaults[item]

            self.settings[area] = s = Settings(p, info)

        return s

    def saveAll(self):
        for settings in self.settings.itervalues():
            settings.save()

class Settings():
    def __init__(self, location, info):
        self.location = location
        self.info = info

    def save(self):
        f = open(self.location, "wb")
        cPickle.dump(self.info, f, cPickle.HIGHEST_PROTOCOL)

    def __getitem__(self, k):
        try:
            return self.info[k]
        except KeyError:
            return None

    def __setitem__(self, k, v):
        self.info[k] = v

    def __iter__(self):
        return self.info.__iter__()

    def iterkeys(self):
        return self.info.iterkeys()

    def itervalues(self):
        return self.info.itervalues()

    def iteritems(self):
        return self.info.iteritems()

    def keys(self):
        return self.info.keys()

    def values(self):
        return self.info.values()

    def items(self):
        return self.info.items()


class NetworkSettings():
    _instance = None
    @classmethod
    def getInstance(cls):
        if cls._instance == None:
            cls._instance = NetworkSettings()

        return cls._instance

    def __init__(self):

        # mode
        # 0 - No proxy
        # 1 - Auto-detected proxy settings
        # 2 - Manual proxy settings
        serviceNetworkDefaultSettings = {"mode": 1, "type": "https", "address": "", "port": "", "access": 15}

        self.serviceNetworkSettings = SettingsProvider.getInstance().getSettings("pyfaServiceNetworkSettings", serviceNetworkDefaultSettings)

    def isEnabled(self, type):
        if type & self.serviceNetworkSettings["access"]:
            return True
        return False

    def toggleAccess(self, type, toggle=True):
        bitfield = self.serviceNetworkSettings["access"]

        if toggle:  # Turn bit on
            self.serviceNetworkSettings["access"] = type | bitfield
        else:  # Turn bit off
            self.serviceNetworkSettings["access"] = ~type & bitfield

    def getMode(self):
        return self.serviceNetworkSettings["mode"]

    def getAddress(self):
        return self.serviceNetworkSettings["address"]

    def getPort(self):
        return self.serviceNetworkSettings["port"]

    def getType(self):
        return self.serviceNetworkSettings["type"]

    def getAccess(self):
        return self.serviceNetworkSettings["access"]

    def setMode(self, mode):
        self.serviceNetworkSettings["mode"] = mode

    def setAddress(self, addr):
        self.serviceNetworkSettings["address"] = addr

    def setPort(self, port):
        self.serviceNetworkSettings["port"] = port

    def setType(self, type):
        self.serviceNetworkSettings["type"] = type

    def setAccess(self, access):
        self.serviceNetworkSettings["access"] = access

    def autodetect(self):

        proxy = None
        proxAddr = proxPort = ""
        proxydict = urllib2.ProxyHandler().proxies
        txt = "Auto-detected: "

        validPrefixes = ("http", "https")

        for prefix in validPrefixes:
            if not prefix in proxydict:
                continue
            proxyline = proxydict[prefix]
            proto = "{0}://".format(prefix)
            if proxyline[:len(proto)] == proto:
                proxyline = proxyline[len(proto):]
            proxAddr, proxPort = proxyline.split(":")
            proxPort = int(proxPort.rstrip("/"))
            proxy = (proxAddr, proxPort)
            break

        return proxy

    def getProxySettings(self):

        if self.getMode() == 0:
            return None
        if self.getMode() == 1:
            return self.autodetect()
        if self.getMode() == 2:
            return (self.getAddress(), int(self.getPort()))



"""
Settings used by the HTML export feature.
"""
class HTMLExportSettings():
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance == None:
            cls._instance = HTMLExportSettings()

        return cls._instance

    def __init__(self):
        serviceHTMLExportDefaultSettings = {"enabled": False, "path": config.pyfaPath + os.sep + 'pyfaFits.html', "website": "null-sec.com", "minimal": False }
        self.serviceHTMLExportSettings = SettingsProvider.getInstance().getSettings("pyfaServiceHTMLExportSettings", serviceHTMLExportDefaultSettings)

    def getEnabled(self):
        return self.serviceHTMLExportSettings["enabled"]

    def setEnabled(self, enabled):
        self.serviceHTMLExportSettings["enabled"] = enabled
        
        
    def getMinimalEnabled(self):
        return self.serviceHTMLExportSettings["minimal"]

    def setMinimalEnabled(self, minimal):
        self.serviceHTMLExportSettings["minimal"] = minimal


    def getPath(self):
        return self.serviceHTMLExportSettings["path"]

    def setPath(self, path):
        self.serviceHTMLExportSettings["path"] = path

    def getWebsite(self):
        return self.serviceHTMLExportSettings["website"]

    def setWebsite(self, website):
        self.serviceHTMLExportSettings["website"] = website

"""
Settings used by update notification
"""
class UpdateSettings():
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance == None:
            cls._instance = UpdateSettings()

        return cls._instance

    def __init__(self):
        # Settings
        # Updates are completely suppressed via network settings
        # prerelease - If True, suppress prerelease notifications
        # version    - Set to release tag that user does not want notifications for
        serviceUpdateDefaultSettings = {"prerelease": True, 'version': None }
        self.serviceUpdateSettings = SettingsProvider.getInstance().getSettings("pyfaServiceUpdateSettings", serviceUpdateDefaultSettings)

    def get(self, type):
        return self.serviceUpdateSettings[type]

    def set(self, type, value):
        self.serviceUpdateSettings[type] = value

class CRESTSettings():
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = CRESTSettings()

        return cls._instance

    def __init__(self):

        # mode
        # 0 - Implicit authentication
        # 1 - User-supplied client details
        serviceCRESTDefaultSettings = {"mode": 0, "server": 0, "clientID": "", "clientSecret": "", "timeout": 60}

        self.serviceCRESTSettings = SettingsProvider.getInstance().getSettings("pyfaServiceCRESTSettings", serviceCRESTDefaultSettings)

    def get(self, type):
        return self.serviceCRESTSettings[type]

    def set(self, type, value):
        self.serviceCRESTSettings[type] = value


# @todo: migrate fit settings (from fit service) here?

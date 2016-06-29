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

import eos.db
import eos.types

class ImportError(Exception):
    pass

class DefaultDatabaseValues():
    instance = None

    @classmethod
    def importDamageProfileDefaults(self):
        damageProfileList = []
        damageProfileList.append(["Uniform", "25", "25", "25", "25"])
        damageProfileList.append(["[Generic]EM", "100", "0", "0", "0"])
        damageProfileList.append(["[Generic]Thermal", "0", "100", "0", "0"])
        damageProfileList.append(["[Generic]Kinetic", "0", "0", "100", "0"])
        damageProfileList.append(["[Generic]Explosive", "0", "0", "0", "100"])
        damageProfileList.append(["[NPC][Asteroid] Blood Raiders", "5067", "4214", "0", "0"])
        damageProfileList.append(["[Bombs]Concussion Bomb", "0", "0", "6400", "0"])
        damageProfileList.append(["[Bombs]Electron Bomb", "6400", "0", "0", "0"])
        damageProfileList.append(["[Bombs]Scorch Bomb", "0", "6400", "0", "0"])
        damageProfileList.append(["[Bombs]Shrapnel Bomb", "0", "0", "0", "6400"])
        damageProfileList.append(["[Frequency Crystals][T2] Gleam", "56", "56", "0", "0"])
        damageProfileList.append(["[Frequency Crystals][T2] Aurora", "40", "24", "0", "0"])
        damageProfileList.append(["[Frequency Crystals][T2] Scorch", "72", "16", "0", "0"])
        damageProfileList.append(["[Frequency Crystals][T2] Conflagration", "61.6", "61.6", "0", "0"])
        damageProfileList.append(["[Frequency Crystals]Gamma", "61.6", "35.2", "0", "0"])
        damageProfileList.append(["[Frequency Crystals]Infrared", "44", "17.6", "0", "0"])
        damageProfileList.append(["[Frequency Crystals]Microwave", "35.2", "17.6", "0", "0"])
        damageProfileList.append(["[Frequency Crystals]Multifrequency", "61.6", "44", "0", "0"])
        damageProfileList.append(["[Frequency Crystals]Radio", "44", "0", "0", "0"])
        damageProfileList.append(["[Frequency Crystals]Standard", "44", "26.4", "0", "0"])
        damageProfileList.append(["[Frequency Crystals]Ultraviolet", "52.8", "26.4", "0", "0"])
        damageProfileList.append(["[Frequency Crystals]Xray", "52.8", "35.2", "0", "0"])
        damageProfileList.append(["[Hybrid Charges][T2] Void", "0", "61.6", "61.6", "0"])
        damageProfileList.append(["[Hybrid Charges][T2] Null", "0", "48", "40", "0"])
        damageProfileList.append(["[Hybrid Charges][T2] Javelin", "0", "64", "48", "0"])
        damageProfileList.append(["[Hybrid Charges][T2] Spike", "0", "32", "32", "0"])
        damageProfileList.append(["[Hybrid Charges]Antimatter", "0", "48", "67.2", "0"])
        damageProfileList.append(["[Hybrid Charges]Iridium", "0", "28.8", "38.4", "0"])
        damageProfileList.append(["[Hybrid Charges]Iron", "0", "19.2", "28.8", "0"])
        damageProfileList.append(["[Hybrid Charges]Lead", "0", "28.8", "48", "0"])
        damageProfileList.append(["[Hybrid Charges]Plutonium", "0", "48", "57.6", "0"])
        damageProfileList.append(["[Hybrid Charges]Thorium", "0", "38.4", "48", "0"])
        damageProfileList.append(["[Hybrid Charges]Tungsten", "0", "19.2", "38.4", "0"])
        damageProfileList.append(["[Hybrid Charges]Uranium", "0", "38.4", "57.6", "0"])
        damageProfileList.append(["[Missiles]Mjolnir", "100", "0", "0", "0"])
        damageProfileList.append(["[Missiles]Inferno", "0", "100", "0", "0"])
        damageProfileList.append(["[Missiles]Scourge", "0", "0", "100", "0"])
        damageProfileList.append(["[Missiles]Nova", "0", "0", "0", "100"])
        damageProfileList.append(["[Missiles][Structure) Standup Missile", "100", "100", "100", "100"])
        damageProfileList.append(["[Projectile Ammo][T2] Tremor", "0", "0", "24", "40"])
        damageProfileList.append(["[Projectile Ammo][T2] Quake", "0", "0", "40", "72"])
        damageProfileList.append(["[Projectile Ammo][T2] Hail", "0", "0", "26.4", "96.8"])
        damageProfileList.append(["[Projectile Ammo][T2] Barrage", "0", "0", "40", "48"])
        damageProfileList.append(["[Projectile Ammo]Carbonized Lead", "0", "0", "35.2", "8.8"])
        damageProfileList.append(["[Projectile Ammo]Depleted Uranium", "0", "26.4", "17.6", "26.4"])
        damageProfileList.append(["[Projectile Ammo]EMP", "79.2", "0", "8.8", "17.6"])
        damageProfileList.append(["[Projectile Ammo]Fusion", "0", "0", "17.6", "88"])
        damageProfileList.append(["[Projectile Ammo]Nuclear", "0", "0", "8.8", "35.2"])
        damageProfileList.append(["[Projectile Ammo]Phased Plasma", "0", "88", "17.6", "0"])
        damageProfileList.append(["[Projectile Ammo]Proton", "26.4", "0", "17.6", "0"])
        damageProfileList.append(["[Projectile Ammo]Titanium Sabot", "0", "0", "52.8", "176"])
        damageProfileList.append(["[NPC][Burner] Cruor (Blood Raiders)", "90", "90", "0", "0"])
        damageProfileList.append(["[NPC][Burner] Dramiel (Angel)", "55", "0", "20", "96"])
        damageProfileList.append(["[NPC][Burner] Daredevil (Serpentis)", "0", "110", "154", "0"])
        damageProfileList.append(["[NPC][Burner] Succubus (Sanshas Nation)", "135", "30", "0", "0"])
        damageProfileList.append(["[NPC][Burner] Worm (Guristas)", "0", "0", "228", "0"])
        damageProfileList.append(["[NPC][Burner] Enyo", "0", "147", "147", "0"])
        damageProfileList.append(["[NPC][Burner] Hawk", "0", "0", "247", "0"])
        damageProfileList.append(["[NPC][Burner] Jaguar", "36", "0", "50", "182"])
        damageProfileList.append(["[NPC][Burner] Vengeance", "232", "0", "0", "0"])
        damageProfileList.append(["[NPC][Burner] Ashimmu (Blood Raiders)", "260", "100", "0", "0"])
        damageProfileList.append(["[NPC][Burner] Talos", "0", "413", "413", "0"])
        damageProfileList.append(["[NPC][Burner] Sentinel", "0", "75", "0", "90"])
        damageProfileList.append(["[NPC][Asteroid] Angel Cartel", "1838", "562", "2215", "3838"])
        damageProfileList.append(["[NPC][Deadspace] Angel Cartel", "369", "533", "1395", "3302"])
        damageProfileList.append(["[NPC][Deadspace] Blood Raiders", "6040", "5052", "10", "15"])
        damageProfileList.append(["[NPC][Asteroid] Guristas", "0", "1828", "7413", "0"])
        damageProfileList.append(["[NPC][Deadspace] Guristas", "0", "1531", "9680", "0"])
        damageProfileList.append(["[NPC][Asteroid] Rogue Drone", "394", "666", "1090", "1687"])
        damageProfileList.append(["[NPC][Deadspace] Rogue Drone", "276", "1071", "1069", "871"])
        damageProfileList.append(["[NPC][Asteroid] Sanshas Nation", "5586", "4112", "0", "0"])
        damageProfileList.append(["[NPC][Deadspace] Sanshas Nation", "3009", "2237", "0", "0"])
        damageProfileList.append(["[NPC][Asteroid] Serpentis", "0", "5373", "4813", "0"])
        damageProfileList.append(["[NPC][Deadspace] Serpentis", "0", "3110", "1929", "0"])
        damageProfileList.append(["[NPC][Mission] Amarr Empire", "4464", "3546", "97", "0"])
        damageProfileList.append(["[NPC][Mission] Caldari State", "0", "2139", "4867", "0"])
        damageProfileList.append(["[NPC][Mission] CONCORD", "336", "134", "212", "412"])
        damageProfileList.append(["[NPC][Mission] Gallente Federation", "9", "3712", "2758", "0"])
        damageProfileList.append(["[NPC][Mission] Khanid", "612", "483", "43", "6"])
        damageProfileList.append(["[NPC][Mission] Minmatar Republic", "1024", "388", "1655", "4285"])
        damageProfileList.append(["[NPC][Mission] Mordus Legion", "25", "262", "625", "0"])
        damageProfileList.append(["[NPC][Mission] Thukker", "0", "52", "10", "79"])
        damageProfileList.append(["[NPC][Other] Sleepers", "1472", "1472", "1384", "1384"])
        damageProfileList.append(["[NPC][Other] Sansha Incursion", "1682", "1347", "3678", "3678"])

        for damageProfileRow in damageProfileList:
            name, em, therm, kin, exp = damageProfileRow
            damageProfile = eos.db.getDamagePattern(name)
            if damageProfile is None:
                damageProfile = eos.types.DamagePattern(em, therm, kin, exp)
                damageProfile.name = name
                eos.db.save(damageProfile)

    @classmethod
    def importResistProfileDefaults(self):
        targetResistProfileList = []
        targetResistProfileList.append(["Uniform (25%)", "0.25", "0.25", "0.25", "0.25"])
        targetResistProfileList.append(["Uniform (50%)", "0.50", "0.50", "0.50", "0.50"])
        targetResistProfileList.append(["Uniform (75%)", "0.75", "0.75", "0.75", "0.75"])
        targetResistProfileList.append(["[T1 Resist]Shield", "0.0", "0.20", "0.40", "0.50"])
        targetResistProfileList.append(["[T1 Resist]Armor", "0.50", "0.45", "0.25", "0.10"])
        targetResistProfileList.append(["[T1 Resist]Hull", "0.33", "0.33", "0.33", "0.33"])
        targetResistProfileList.append(["[T1 Resist]Shield (+T2 DCU)", "0.125", "0.30", "0.475", "0.562"])
        targetResistProfileList.append(["[T1 Resist]Armor (+T2 DCU)", "0.575", "0.532", "0.363", "0.235"])
        targetResistProfileList.append(["[T1 Resist]Hull (+T2 DCU)", "0.598", "0.598", "0.598", "0.598"])
        targetResistProfileList.append(["[NPC][Asteroid] Angel Cartel", "0.54", "0.42", "0.37", "0.32"])
        targetResistProfileList.append(["[NPC][Asteroid] Blood Raiders", "0.34", "0.39", "0.45", "0.52"])
        targetResistProfileList.append(["[NPC][Asteroid] Guristas", "0.55", "0.35", "0.3", "0.48"])
        targetResistProfileList.append(["[NPC][Asteroid] Rogue Drones", "0.35", "0.38", "0.44", "0.49"])
        targetResistProfileList.append(["[NPC][Asteroid] Sanshas Nation", "0.35", "0.4", "0.47", "0.53"])
        targetResistProfileList.append(["[NPC][Asteroid] Serpentis", "0.49", "0.38", "0.29", "0.51"])
        targetResistProfileList.append(["[NPC][Deadspace] Angel Cartel", "0.59", "0.48", "0.4", "0.32"])
        targetResistProfileList.append(["[NPC][Deadspace] Blood Raiders", "0.31", "0.39", "0.47", "0.56"])
        targetResistProfileList.append(["[NPC][Deadspace] Guristas", "0.57", "0.39", "0.31", "0.5"])
        targetResistProfileList.append(["[NPC][Deadspace] Rogue Drones", "0.42", "0.42", "0.47", "0.49"])
        targetResistProfileList.append(["[NPC][Deadspace] Sanshas Nation", "0.31", "0.39", "0.47", "0.56"])
        targetResistProfileList.append(["[NPC][Deadspace] Serpentis", "0.49", "0.38", "0.29", "0.56"])
        targetResistProfileList.append(["[NPC][Mission] Amarr Empire", "0.34", "0.38", "0.42", "0.46"])
        targetResistProfileList.append(["[NPC][Mission] Caldari State", "0.51", "0.38", "0.3", "0.51"])
        targetResistProfileList.append(["[NPC][Mission] CONCORD", "0.47", "0.46", "0.47", "0.47"])
        targetResistProfileList.append(["[NPC][Mission] Gallente Federation", "0.51", "0.38", "0.31", "0.52"])
        targetResistProfileList.append(["[NPC][Mission] Khanid", "0.51", "0.42", "0.36", "0.4"])
        targetResistProfileList.append(["[NPC][Mission] Minmatar Republic", "0.51", "0.46", "0.41", "0.35"])
        targetResistProfileList.append(["[NPC][Mission] Mordus Legion", "0.32", "0.48", "0.4", "0.62"])
        targetResistProfileList.append(["[NPC][Other] Sleeper", "0.61", "0.61", "0.61", "0.61"])
        targetResistProfileList.append(["[NPC][Other] Sansha Incursion", "0.65", "0.63", "0.64", "0.65"])
        targetResistProfileList.append(["[NPC][Burner] Cruor (Blood Raiders)", "0.8", "0.73", "0.69", "0.67"])
        targetResistProfileList.append(["[NPC][Burner] Dramiel (Angel)", "0.35", "0.48", "0.61", "0.68"])
        targetResistProfileList.append(["[NPC][Burner] Daredevil (Serpentis)", "0.69", "0.59", "0.59", "0.43"])
        targetResistProfileList.append(["[NPC][Burner] Succubus (Sanshas Nation)", "0.35", "0.48", "0.61", "0.68"])
        targetResistProfileList.append(["[NPC][Burner] Worm (Guristas)", "0.48", "0.58", "0.69", "0.74"])
        targetResistProfileList.append(["[NPC][Burner] Enyo", "0.58", "0.72", "0.86", "0.24"])
        targetResistProfileList.append(["[NPC][Burner] Hawk", "0.3", "0.86", "0.79", "0.65"])
        targetResistProfileList.append(["[NPC][Burner] Jaguar", "0.78", "0.65", "0.48", "0.56"])
        targetResistProfileList.append(["[NPC][Burner] Vengeance", "0.66", "0.56", "0.75", "0.86"])
        targetResistProfileList.append(["[NPC][Burner] Ashimmu (Blood Raiders)", "0.8", "0.76", "0.68", "0.7"])
        targetResistProfileList.append(["[NPC][Burner] Talos", "0.68", "0.59", "0.59", "0.43"])
        targetResistProfileList.append(["[NPC][Burner] Sentinel", "0.58", "0.45", "0.52", "0.66"])

        for targetResistProfileRow in targetResistProfileList:
            name, em, therm, kin, exp = targetResistProfileRow
            resistsProfile = eos.db.eos.db.getTargetResists(name)
            if resistsProfile is None:
                resistsProfile = eos.types.TargetResists(em, therm, kin, exp)
                resistsProfile.name = name
                eos.db.save(resistsProfile)

    @classmethod
    def importRequiredDefaults(self):
        damageProfileList = []
        damageProfileList.append(["Uniform", "25", "25", "25", "25"])

        for damageProfileRow in damageProfileList:
            name, em, therm, kin, exp = damageProfileRow
            damageProfile = eos.db.getDamagePattern(name)
            if damageProfile is None:
                damageProfile = eos.types.DamagePattern(em, therm, kin, exp)
                damageProfile.name = name
                eos.db.save(damageProfile)

# shipScanResolutionBonusOnline
#
# Used by:
# Modules from group: Signal Amplifier (7 of 7)
# Module: QA Damage Module
type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("scanResolution", module.getModifiedItemAttr("scanResolutionBonus"),
                           stackingPenalties = True)

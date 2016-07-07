# entityECMFalloff
#
# Used by:
# Drones named like: EC (3 of 3)
type = "projected", "active"
def handler(fit, module, context):
    if "projected" in context:
        # jam formula: 1 - (1- (jammer str/ship str))^(# of jam mods with same str))
        strModifier = 1 - module.getModifiedItemAttr("scan{0}StrengthBonus".format(fit.scanType))/fit.scanStrength

        fit.ecmProjectedStr *= strModifier

# systemNeutBombs
#
# Used by:
# Celestials named like: Red Giant Beacon Class (6 of 6)
runTime = "early"
type = ("projected", "passive")
def handler(fit, beacon, context):
    fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Bomb Deployment"),
                                       "energyNeutralizerAmount", beacon.getModifiedItemAttr("smartbombDamageMultiplier"),
                                       stackingPenalties=True, penaltyGroup="postMul")

# shipBonusSupercarrierRole1NumWarfareLinks
#
# Used by:
# Ships from group: Supercarrier (6 of 6)
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Leadership"), "maxGroupActive", src.getModifiedItemAttr("shipBonusRole1"))

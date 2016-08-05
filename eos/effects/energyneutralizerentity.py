# energyNeutralizerEntity
#
# Used by:
# Drones from group: Energy Neutralizer Drone (3 of 3)
from eos.types import State
type = "active", "projected"


def handler(fit, src, context):
    if "projected" in context and ((hasattr(src, "state") and src.state >= State.ACTIVE) or hasattr(src, "amountActive")):
        amount = src.getModifiedItemAttr("energyNeutralizerAmount")
        time = src.getModifiedItemAttr("duration")

        fit.addDrain(src, time, amount, 0)

from lib.utilities import load_bool, load_variable


class HamCycle:
    SUBSECTION_SIZE: int = int(load_variable("HAMCYCLE_SUBSECTION_SIZE", 20))
    SHUFFLE: bool = load_bool("HAMCYCLE_SHUFFLE", True)
    RISK: int = int(load_variable("HAMCYCLE_RISK", 5))

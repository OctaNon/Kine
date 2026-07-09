import numpy as np
from ..classes.karacter import Karacter


def sign(karacter: Karacter) -> None:
    diff = karacter.nacc.astype(np.int64) - karacter.oacc.astype(np.int64)
    karacter.sacc[:] = diff >= 0

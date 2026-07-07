from ..classes.karacter import Karacter
from ..classes.kmatrix import Kmatrix


def create_motion(karacter: Karacter, frames_number: int) -> Kmatrix:
    return Kmatrix(column=int(karacter.dof_count), row=frames_number)

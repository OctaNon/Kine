from ..classes.karacter import Karacter
from ..classes.kinematrix import Kinematrix


def create_motion(karacter: Karacter, frames_number: int) -> Kinematrix:
    return Kinematrix(row=int(karacter.dof_count), column=frames_number)

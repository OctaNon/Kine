from ..classes.karacter import Karacter
from ..classes.kframe import Kframe
from .update import update
from .clear import clear


def updatc(karacter: Karacter, kframe: Kframe) -> None:
    update(karacter, kframe)
    clear(kframe)

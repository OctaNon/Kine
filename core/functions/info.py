from ..classes.karacter import Karacter
from ..classes.kmatrix import Kmatrix
from ..classes.kimage import Kimage
from ..classes.kframe import Kframe


def info(obj) -> None:
    if isinstance(obj, Karacter):
        print(f"Karacter : {obj.model_name}")
        print(f"Degrees  : {obj.dof_count}")
        print(f"Accumulat: shape={obj.accumulator.shape}, dtype={obj.accumulator.dtype}")

    elif isinstance(obj, Kmatrix):
        print(f"Kmatrix  : row={obj.row}, column={obj.column}")
        print(f"Data     : shape={obj.kmatrix.shape}, dtype={obj.kmatrix.dtype}")

    elif isinstance(obj, Kimage):
        print(f"Kimage   : row={obj.row}, column={obj.column}")
        print(f"Data     : shape={obj.kimage.shape}, dtype={obj.kimage.dtype}")

    elif isinstance(obj, Kframe):
        print(f"Kframe   : dof={obj.dof_count}")
        print(f"Values   : {obj}")

    else:
        raise TypeError(f"info() does not support objects of type {type(obj).__name__}")

from solid2.core.builtins.openscad_primitives import _OpenSCADObject
from solid2 import cube

def combine(l: list[_OpenSCADObject]) -> _OpenSCADObject:
    accumulator: _OpenSCADObject = cube(0, 0, 0)
    for obj in l:
        accumulator += obj
    return accumulator

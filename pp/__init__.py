""" pp Photonics package provides some GDS useful

functions:

    - pp.show(): writes and shows the GDS in Klayout using klive
    - pp.plotgds(): plots GDS in matplotlib (good for notebooks)
    - pp.import_gds(): returns a component from a GDS

classes:

    - pp.Component
    - pp.Port
    - CONFIG

modules:

    - c: components
    - routing
    - Klive: send to klayout
    - layer: use layers
"""
from phidl import quickplot as qp

from pp.config import CONFIG
from pp.config import call_if_func
from pp.component import Component
from pp.component import ComponentReference
from pp.component import Port
from pp.name import autoname
from pp.layers import LAYER

from pp.write_component import get_component_type
from pp.write_component import show
from pp.write_component import write_gds
from pp.write_component import write_component_type
from pp.write_component import write_component

from pp.components import component_type2factory
from pp.import_gds import import_gds

import pp.components as c
import pp.klive as klive

__all__ = [
    "CONFIG",
    "Component",
    "ComponentReference",
    "LAYER",
    "Port",
    "autoname",
    "c",
    "call_if_func",
    "component_factory",
    "component_type2factory",
    "get_component_type",
    "import_gds",
    "klive",
    "preview_layerset",
    "qp",
    "show",
    "write_component",
    "write_component_type",
    "write_gds",
]
__version__ = "1.1.9"


if __name__ == "__main__":
    print(__all__)

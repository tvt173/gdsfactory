import functools
import csv
from pp import klive
import phidl.geometry as pg
import pp


def deco_rename_ports(component_factory):
    @functools.wraps(component_factory)
    def auto_named_component_factory(*args, **kwargs):
        device = component_factory(*args, **kwargs)
        auto_rename_ports(device)
        return device

    return auto_named_component_factory


def _rename_ports_facing_side(direction_ports, prefix=""):
    for direction, list_ports in list(direction_ports.items()):

        if direction in ["E", "W"]:
            # first sort along x then y
            list_ports.sort(key=lambda p: p.x)
            list_ports.sort(key=lambda p: p.y)

        if direction in ["S", "N"]:
            # first sort along y then x
            list_ports.sort(key=lambda p: p.y)
            list_ports.sort(key=lambda p: p.x)

        for i, p in enumerate(list_ports):
            lbl = prefix + direction + str(i)
            p.name = lbl


def rename_ports_by_orientation(device, layers_excluded=[]):
    """
    Assign standard port names based on the layer of the port
    """

    # Naming functions

    direction_ports = {x: [] for x in ["E", "N", "W", "S"]}

    ports_on_process = [
        p for p in device.ports.values() if p.layer not in layers_excluded
    ]

    for p in ports_on_process:
        # Make sure we can backtrack the parent component from the port
        p.parent = device

        angle = p.orientation % 360
        if angle <= 45 or angle >= 315:
            direction_ports["E"].append(p)
        elif angle <= 135 and angle >= 45:
            direction_ports["N"].append(p)
        elif angle <= 225 and angle >= 135:
            direction_ports["W"].append(p)
        else:
            direction_ports["S"].append(p)

    _rename_ports_facing_side(direction_ports)
    device.ports = {p.name: p for p in device.ports.values()}
    return device


def auto_rename_ports(device):
    """
    Assign standard port names based on the layer of the port
    """

    def _counter_clockwise(_direction_ports, prefix=""):

        east_ports = _direction_ports["E"]
        east_ports.sort(key=lambda p: p.y)  # sort south to north

        north_ports = _direction_ports["N"]
        north_ports.sort(key=lambda p: -p.x)  # sort east to west

        west_ports = _direction_ports["W"]
        west_ports.sort(key=lambda p: -p.y)  # sort north to south

        south_ports = _direction_ports["S"]
        south_ports.sort(key=lambda p: p.x)  # sort west to east

        ports = east_ports + north_ports + west_ports + south_ports

        for i, p in enumerate(ports):
            p.name = "{}{}".format(prefix, i)

    type_to_ports_naming_functions = {
        "optical": _rename_ports_facing_side,
        "heater": lambda _d: _counter_clockwise(_d, "H_"),
        "dc": lambda _d: _counter_clockwise(_d, "E_"),
        "superconducting": lambda _d: _counter_clockwise(_d, "SC_"),
    }

    type_to_ports = {}

    for p in device.ports.values():
        if p.port_type not in type_to_ports:
            type_to_ports[p.port_type] = []
        type_to_ports[p.port_type] += [p]

    for port_type, port_group in type_to_ports.items():
        if port_type in type_to_ports_naming_functions:
            _func_name_ports = type_to_ports_naming_functions[port_type]
        else:
            raise ValueError(
                "Unknown port type <{}> in device {}, port {}".format(
                    port_type, device.name, p
                )
            )

        # Make sure we can backtrack the parent component from the port

        direction_ports = {x: [] for x in ["E", "N", "W", "S"]}
        for p in port_group:
            p.parent = device
            angle = p.orientation % 360
            if angle <= 45 or angle >= 315:
                direction_ports["E"].append(p)
            elif angle <= 135 and angle >= 45:
                direction_ports["N"].append(p)
            elif angle <= 225 and angle >= 135:
                direction_ports["W"].append(p)
            else:
                direction_ports["S"].append(p)

        _func_name_ports(direction_ports)

    # Set the port dictionnary with the new names
    device.ports = {p.name: p for p in device.ports.values()}
    return device


def read_port_markers(gdspath, layer=69):
    """ loads a GDS and read port

    Args:
        gdspath:
        layer: GDS layer
    """
    D = pg.import_gds(gdspath)
    D = pg.extract(D, layers=[layer])
    for e in D.elements:
        print(e.x, e.y)


def csv2port(csvpath):
    """ loads and reads ports from a CSV file
    returns a dict
    """
    ports = {}
    with open(csvpath, "r") as csvfile:
        rows = csv.reader(csvfile, delimiter=",", quotechar="|")
        for row in rows:
            ports[row[0]] = row[1:]

    return ports


def is_electrical_port(port):
    return port.port_type in ["dc", "rf"]


def select_ports(ports, port_type):
    """
    Args:
        ports: a port dictionnary {port name: port} (as returned by Component.ports)
        layers: a list of port layer or a port type (layer or string)

    Returns:
        Dictionnary containing only the ports with the wanted type(s)
        {port name: port}
    """

    # Make it accept Component or ComponentReference
    if isinstance(ports, pp.Component) or isinstance(ports, pp.ComponentReference):
        ports = ports.ports

    return {p_name: p for p_name, p in ports.items() if p.port_type == port_type}


def select_heater_ports(ports):
    return select_ports(ports, port_type="heater")


def select_optical_ports(ports):
    return select_ports(ports, port_type="optical")


def get_optical_ports(ports):
    return select_optical_ports(ports)


def select_electrical_ports(ports):
    d = select_ports(ports, port_type="dc")
    d.update(select_ports(ports, port_type="electrical"))
    return d


def select_dc_ports(ports):
    return select_ports(ports, port_type="dc")


def select_rf_ports(ports):
    return select_ports(ports, port_type="rf")


def select_superconducting_ports(ports):
    d = select_ports(ports, port_type="detector")
    d.update(select_ports(ports, port_type="superconducting"))
    return d


def flipped(port):
    _port = port._copy()
    _port.orientation = (_port.orientation + 180) % 360
    return _port


def move_copy(port, x=0, y=0):
    _port = port._copy()
    _port.midpoint += (x, y)
    return _port


def get_ports_facing(ports, direction="W"):
    if isinstance(ports, dict):
        ports = list(ports.values())
    elif isinstance(ports, pp.Component) or isinstance(ports, pp.ComponentReference):
        ports = list(ports.ports.values())

    direction_ports = {x: [] for x in ["E", "N", "W", "S"]}

    for p in ports:
        angle = p.orientation % 360
        if angle <= 45 or angle >= 315:
            direction_ports["E"].append(p)
        elif angle <= 135 and angle >= 45:
            direction_ports["N"].append(p)
        elif angle <= 225 and angle >= 135:
            direction_ports["W"].append(p)
        else:
            direction_ports["S"].append(p)

    return direction_ports[direction]


def get_non_optical_ports(ports):
    if isinstance(ports, dict):
        ports = list(ports.values())
    elif isinstance(ports, pp.Component) or isinstance(ports, pp.ComponentReference):
        ports = list(ports.ports.values())
    res = [p for p in ports if p.port_type not in ["optical"]]
    return res


if __name__ == "__main__":
    import os
    from pp import CONFIG

    name = "mmi1x2_WM1"
    gdspath = os.path.join(CONFIG["lib"], name, name + ".gds")
    csvpath = os.path.join(CONFIG["lib"], name, name + ".ports")
    klive.show(gdspath)
    # read_port_markers(gdspath, layer=66)
    p = csv2port(csvpath)
    print(p)

import numpy as np
from phidl import device_layout as pd
import pp
from pp.layers import LAYER
from pp.name import autoname


DIRECTION_TO_ANGLE = {"W": 180, "E": 0, "N": 90, "S": 270}


@pp.autoname
def rectangle(
    size=(4, 2), layer=0, centered=False, ports_parameters={}, **port_settings
):
    """ rectangle

    Args:
        size: (tuple) Width and height of rectangle.
        layer: (int, array-like[2], or set) Specific layer(s) to put polygon geometry on.
        ports: {direction: [(x_or_y, width), ...]} direction: 'W', 'E', 'N' or 'S'

    .. plot::
      :include-source:

      import pp

      c = pp.c.rectangle(size=(4, 2), layer=0)
      pp.plotgds(c)
    """

    c = pp.Component()
    w, h = size

    if centered:
        points = [
            [-w / 2.0, -h / 2.0],
            [-w / 2.0, h / 2],
            [w / 2, h / 2],
            [w / 2, -h / 2.0],
        ]
    else:
        points = [[w, h], [w, 0], [0, 0], [0, h]]
    c.add_polygon(points, layer=layer)

    i = 0
    for direction, list_port_params in ports_parameters.items():
        angle = DIRECTION_TO_ANGLE[direction]
        for x_or_y, width in list_port_params:
            if direction == "W":
                position = (0, x_or_y)

            elif direction == "E":
                position = (w, x_or_y)

            elif direction == "S":
                position = (x_or_y, 0)

            elif direction == "N":
                position = (x_or_y, h)

            c.add_port(
                name="{}".format(i),
                orientation=angle,
                midpoint=position,
                width=width,
                layer=layer,
                **port_settings
            )
            i += 1

    pp.ports.auto_rename_ports(c)
    return c


@pp.autoname
def rectangle_centered(w=1, h=1, x=None, y=None, layer=0):
    """ a rectangle size (x, y) in layer
        bad naming with x and y. Replaced with w and h. Keeping x and y
        for now for backwards compatibility

    .. plot::
      :include-source:

      import pp

      c = pp.c.rectangle_centered(w=1, h=1, layer=0)
      pp.plotgds(c)
    """
    c = pp.Component()
    if x:
        w = x
    if y:
        h = y

    points = [
        [-w / 2.0, -h / 2.0],
        [-w / 2.0, h / 2],
        [w / 2, h / 2],
        [w / 2, -h / 2.0],
    ]
    c.add_polygon(points, layer=layer)
    return c


@pp.autoname
def hline(length=10, width=0.5, layer=LAYER.WG):
    """ horizonal line waveguide, with ports on east and west sides

    .. plot::
      :include-source:

      import pp
      c = pp.c.hline()
      pp.plotgds(c)

    """
    c = pp.Component()
    a = width / 2
    if length > 0 and width > 0:
        c.add_polygon([(0, -a), (length, -a), (length, a), (0, a)], layer=layer)

    c.add_port(name="W0", midpoint=[0, 0], width=width, orientation=180, layer=layer)
    c.add_port(name="E0", midpoint=[length, 0], width=width, orientation=0, layer=layer)

    c.width = width
    c.length = length
    return c


@autoname
def waveguide(
    length=10,
    width=0.5,
    layer=pp.LAYER.WG,
    layers_cladding=[pp.LAYER.WGCLAD],
    cladding_offset=3,
):
    """ straight waveguide

    Args:
        length: in X direction
        width: in Y direction

    .. plot::
      :include-source:

      import pp

      c = pp.c.waveguide(length=10, width=0.5)
      pp.plotgds(c)

    """
    c = pp.Component()
    w = width / 2
    c.add_polygon([(0, -w), (length, -w), (length, w), (0, w)], layer=layer)

    wc = w + cladding_offset

    for layer_cladding in layers_cladding:
        c.add_polygon(
            [(0, -wc), (length, -wc), (length, wc), (0, wc)], layer=layer_cladding
        )

    c.add_port(name="W0", midpoint=[0, 0], width=width, orientation=180, layer=layer)
    c.add_port(name="E0", midpoint=[length, 0], width=width, orientation=0, layer=layer)

    c.width = width
    c.length = length
    return c


def label(text="abc", position=(0, 0), layer=pp.LAYER.TEXT):

    gds_layer_label, gds_datatype_label = pd._parse_layer(layer)

    label_ref = pd.Label(
        text=text,
        position=position,
        anchor="o",
        layer=gds_layer_label,
        texttype=gds_datatype_label,
    )
    return label_ref


@pp.autoname
def verniers(width_min=0.1, width_max=0.5, gap=0.1, size_max=11):
    c = pp.Component()
    y = 0

    widths = np.linspace(width_min, width_max, int(size_max / (width_max + gap)))

    for width in widths:
        w = c << pp.c.waveguide(width=width, length=size_max, layers_cladding=[])
        y += width / 2
        w.y = y
        c.add(pp.c.label(str(int(width * 1e3)), position=(0, y)))
        y += width / 2 + gap

    return c


component_type2factory = dict(rectangle=rectangle, waveguide=waveguide, label=label)

if __name__ == "__main__":
    c = verniers()
    # c = rectangle_centered()
    # c = rectangle()
    # print(c.ports)
    pp.show(c)

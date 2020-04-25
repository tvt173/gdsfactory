"""
In this example we change the layer of the waveguide
"""

import pp


@pp.autoname
def wg(layer=pp.LAYER.WG, **kwargs):
    return pp.c.waveguide(layer=layer, **kwargs)


def bend(layers_cladding=[pp.LAYER.WGCLAD, pp.LAYER.WGCLAD2]):
    c = pp.c.bend_circular(layers_cladding=layers_cladding)
    c = pp.add_padding(c)
    return c


if __name__ == "__main__":
    c = wg()
    c = bend()
    pp.show(c)

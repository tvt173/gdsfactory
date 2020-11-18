import klayout.db as pya


def check_exclusion(
    gdspath,
    layer1=(1, 0),
    layer2=(2, 0),
    min_space=0.150,
    dbu=1e3,
    ignore_angle_deg=80,
    whole_edges=False,
    metrics=None,
    min_projection=None,
    max_projection=None,
):
    """reads layer from top cell and returns a the area that violates min exclusion
    if 0 no area violates exclusion

    Args:
        gdspath: path to GDS
        layer1: tuple
        layer2: tuple
        min_space: in um
        dbu: database units (1000 um/nm)
        ignore_angle_deg: The angle above which no check is performed
        other: The other region against which to check
        whole_edges: If true, deliver the whole edges
        metrics: Specify the metrics type
        min_projection The lower threshold of the projected length of one edge onto another
        max_projection The upper limit of the projected length of one edge onto another
    """
    from pp.component import Component
    from pp.write_component import write_gds

    if isinstance(gdspath, Component):
        gdspath.flatten()
        gdspath = write_gds(gdspath)
    layout = pya.Layout()
    layout.read(str(gdspath))
    cell = layout.top_cell()
    a = pya.Region(cell.begin_shapes_rec(layout.layer(layer1[0], layer1[1])))
    b = pya.Region(cell.begin_shapes_rec(layout.layer(layer2[0], layer2[1])))

    d = a.separation_check(
        b,
        min_space * dbu,
        whole_edges,
        metrics,
        ignore_angle_deg,
        min_projection,
        max_projection,
    )
    # print(d.polygons().area())
    return d.polygons().area()


if __name__ == "__main__":
    import pp

    w = 0.5
    space = 0.1
    min_space = 0.11
    dbu = 1000
    layer = (1, 0)
    c = pp.Component()
    r1 = c << pp.c.rectangle(size=(w, w), layer=(1, 0))
    r2 = c << pp.c.rectangle(size=(w, w), layer=(2, 0))
    r1.xmax = 0
    r2.xmin = space
    gdspath = c
    pp.show(gdspath)
    print(check_exclusion(c))

    # if isinstance(gdspath, pp.Component):
    #     gdspath.flatten()
    #     gdspath = pp.write_gds(gdspath)
    # layout = pya.Layout()
    # layout.read(str(gdspath))
    # cell = layout.top_cell()
    # region = pya.Region(cell.begin_shapes_rec(layout.layer(layer[0], layer[1])))

    # d = region.space_check(min_space * dbu)
    # print(d.polygons().area())

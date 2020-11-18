import pp
from pp.drc import check_width


def test_wmin_failing(layer=(1, 0)):
    w = 50
    min_width = 50 + 10  # device edges are smaller than min_width
    c = pp.c.rectangle(size=(w, w), layer=layer)
    gdspath = pp.write_gds(c, "wmin.gds")

    # print(check_width(gdspath, min_width=min_width, layer=layer))
    # print(len(check_width(gdspath, min_width=min_width, layer=layer)))
    assert len(check_width(gdspath, min_width=min_width, layer=layer)) == 2
    assert len(check_width(c, min_width=min_width, layer=layer)) == 2


def test_wmin_passing(layer=(1, 0)):
    w = 50
    min_width = 50 - 10  # device edges are bigger than the min_width
    c = pp.c.rectangle(size=(w, w), layer=layer)
    gdspath = pp.write_gds(c, "wmin.gds")

    # print(check_width(gdspath, min_width=min_width, layer=layer))
    # print(check_width(c, min_width=min_width, layer=layer))
    # print(len(check_width(gdspath, min_width=min_width, layer=layer)))
    # assert check_width(gdspath, min_width=min_width, layer=layer) is None
    # assert check_width(c, min_width=min_width, layer=layer) is None
    assert len(check_width(gdspath, min_width=min_width, layer=layer)) == 0
    assert len(check_width(c, min_width=min_width, layer=layer)) == 0


if __name__ == "__main__":
    test_wmin_passing()

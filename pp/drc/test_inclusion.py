import pytest
import numpy as np
import pp
from pp.drc import check_inclusion


def get_device(inclusion, width=0.5, layer1=(1, 0), layer2=(2, 0)):
    c = pp.Component()
    r1 = c << pp.c.rectangle(size=(width, width), layer=layer1)
    r2 = c << pp.c.rectangle(
        size=(width - 2 * inclusion, width - 2 * inclusion), layer=layer2
    )
    r1.x = 0
    r1.y = 0
    r2.x = 0
    r2.y = 0
    return c


@pytest.mark.parametrize(
    "inclusion,min_inclusion,area_expected", [(0.1, 0.11, 138400), (0.1, 0.01, 0)]
)
def test_inclusion(inclusion, min_inclusion, area_expected):
    c = get_device(inclusion=inclusion)
    area = check_inclusion(c, min_inclusion=min_inclusion)
    assert np.isclose(area, area_expected)


if __name__ == "__main__":
    test_inclusion()

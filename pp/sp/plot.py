import matplotlib.pyplot as plt
import numpy as np
import pp
from pp.sp.write import write


def plot(component_or_results_dict, logscale=True, keys=None, height_nm=220, **kwargs):
    """ plots Sparameters

    Args:
        component_or_results_dict:
        logscale: plots 20*log10(results)
        keys: list of keys to plot
        height_nm: nm height
        **kwargs:
            dirpath: where to store the simulations
            session: you can pass a session=lumapi.FDTD() for debugging
            run: True-> runs Lumerical , False -> only draws simulation
            layer2nm: dict of {(1,0): 220}
            layer2material: dict of {(1,0): "Silicon ..."
            remove_layers: list of tuples (layers to remove)
            background_material: for the background
            port_width: port width (m)
            port_height: port height (m)
            port_extension_um: port extension (um)
            mesh_accuracy: 2 (1: coarse, 2: fine, 3: superfine)
            zmargin: for the FDTD region 1e-6 (m)
            ymargin: for the FDTD region 2e-6 (m)

    """
    r = component_or_results_dict
    if isinstance(r, pp.Component):
        r = write(component=r, height_nm=height_nm, **kwargs)
    w = r["wavelength_nm"]

    if keys:
        assert isinstance(keys, list)
        for key in keys:
            assert key in r, f"{key} not in {r.keys()}"
    else:
        keys = [key for key in r.keys() if key.startswith("S") and key.endswith("m")]

    for key in keys:
        if logscale:
            y = 20 * np.log10(r[key])
        else:
            y = r[key]

        plt.plot(w, y, label=key[:-1])
    plt.legend()
    plt.xlabel("wavelength (nm)")
    if logscale:
        plt.ylabel("Transmission (dB)")
    else:
        plt.ylabel("Transmission")


if __name__ == "__main__":
    remove_layers = []
    layer2nm = {(1, 0): 220}

    # r = write(component=pp.c.waveguide(), layer2nm=layer2nm)
    # r = write(component=pp.c.mmi2x2(), layer2nm=layer2nm)
    # r = write(component=pp.c.mmi1x2(), layer2nm=layer2nm)
    r = write(component=pp.c.coupler(), layer2nm=layer2nm)
    # r = write(component=pp.c.bend_circular(), layer2nm=layer2nm)
    plot(r, logscale=True)
    plt.show()

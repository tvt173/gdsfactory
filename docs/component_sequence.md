# 3. Connect component_sequence

This is a convenience function for cascading components such as cutbacks

The idea is to associate one symbol per type of section.
A section is uniquely defined by the component, its selected input and its selected output.

The mapping between symbols and components is supplied by a dictionnary.
The actual chain of components is supplied by a string or a list



- **Cutback heater**

```eval_rst

.. plot::
    :include-source:

    import pp
    from pp.components import bend_circular
    from pp.components.waveguide import waveguide
    from pp.components.waveguide_heater import waveguide_heater
    from pp.components.component_sequence import component_sequence

    @pp.autoname
    def test():
        # Define sub components
        bend_radius=10.0
        bend180 = bend_circular(radius=bend_radius, start_angle=-90, theta=180)
        wg = waveguide(length=5.0)
        wg_heater = waveguide_heater(length=20.0)

        # Define a map between symbols and (component, input port, output port)
        string_to_device_in_out_ports = {
            "A": (bend180, "W0", "W1"),
            "B": (bend180, "W1", "W0"),
            "H": (wg_heater, "W0", "E0"),
            "-": (wg, "W0", "E0"),
        }

        # Generate a sequence
        # This is simply a chain of characters. Each of them represents a component
        # with a given input and and a given output

        sequence = "AB-H-H-H-H-BA"
        component = component_sequence(sequence, string_to_device_in_out_ports)

        return component

    c = test()
    pp.plotgds(c)

```

- **Cutback phase**

```eval_rst

.. plot::
    :include-source:

    import pp
    from pp.components import bend_circular
    from pp.components.waveguide import _arbitrary_straight_waveguide
    from pp.components.waveguide import waveguide
    from pp.components.waveguide_heater import waveguide_heater
    from pp.components.taper import taper_strip_to_ridge as _taper

    from pp.layers import LAYER

    from pp.components.component_sequence import component_sequence

    @pp.autoname
    def phase_modulator_waveguide(length, wg_width=0.5, cladding=3.0, si_outer_clad=1.0):
        """
        Phase modulator waveguide mockup
        """
        a = wg_width / 2
        b = a + cladding
        c = b + si_outer_clad

        windows = [
            (-c, -b, LAYER.WG),
            (-b, -a, LAYER.SLAB90),
            (-a, a, LAYER.WG),
            (a, b, LAYER.SLAB90),
            (b, c, LAYER.WG),
        ]

        component = _arbitrary_straight_waveguide(length=length, windows=windows)
        return component


    def phase_mod_arm(straight_length=100.0, bend_radius=10.0, n=2):

        # Define sub components
        bend180 = bend_circular(radius=bend_radius, start_angle=-90, theta=180)
        pm_wg = phase_modulator_waveguide(length=straight_length)
        wg_short = waveguide(length=1.0)
        wg_short2 = waveguide(length=2.0)
        wg_heater = waveguide_heater(length=10.0)
        taper=_taper()

        # Define a map between symbols and (component, input port, output port)
        string_to_device_in_out_ports = {
            "I": (taper, "1", "wg_2"),
            "O": (taper, "wg_2", "1"),
            "S": (wg_short, "W0", "E0"),
            "P": (pm_wg, "W0", "E0"),
            "A": (bend180, "W0", "W1"),
            "B": (bend180, "W1", "W0"),
            "H": (wg_heater, "W0", "E0"),
            "-": (wg_short2, "W0", "E0"),
        }

        # Generate a sequence
        # This is simply a chain of characters. Each of them represents a component
        # with a given input and and a given output

        repeated_sequence="SIPOSASIPOSB"
        heater_seq = "-H-H-H-H-"
        sequence = repeated_sequence * n + "SIPO" + heater_seq
        component = component_sequence(sequence, string_to_device_in_out_ports)

        return component

    c = phase_mod_arm()
    pp.plotgds(c)


```

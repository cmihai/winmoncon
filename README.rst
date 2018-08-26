winmoncon
=========

A Python interface to the Windows Monitor Configuration API.

Controls the display parameters like brightness, contrast, and color temperature, through DCC/CI, using the Windows
Monitor Configuration functions.

The original documentation can be found on MSDN_.

Example
-------
::

    from winmoncon import PhysicalMonitors

    monitors = PhysicalMonitors.all
    for m in monitors:
        print m.description, m.brightness, m.contrast, m.color_temperature

See also the `examples` directory. `brux.py` contains a bare-bones program
that adjusts the brightness of the monitor based on the time of the day and
the configured brightness graph:

.. image:: /examples/brux.png

.. _MSDN: https://msdn.microsoft.com/en-us/library/dd692933(v=vs.85).aspx
mom-utils
=========


This is a collection of Python utilities for the MOM, a numerical model
developed by GFDL/NOAA


Support and Documentation
-------------------------

Quick howto use
---------------

To install:

    pip install mom-utils

Some uses:

* The input.nml do not require any order, so it is usually not fun to compare two different input.nml. This command is different then a regular diff, since it doesn't care abour the order of the variables. The output show what is different, or what is present in only one of the files.

    mom4_namelist compare input.nml input2.nml

License
-------

``mom-utils`` is offered under the PSFL.

Authors
-------

Guilherme Castelão <guilherme@castelao.net>
Luiz Irber <luiz.irber@gmail.com>

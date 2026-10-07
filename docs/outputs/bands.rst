===================================
bands — band structure along a path
===================================

Every run writes ``bands_<material>.dat``: the eigenvalues of the Wannier Hamiltonian along a path in the Brillouin
zone. Use it to check that the model was read correctly and to choose ``Nfermi`` and ``Bandlist``;
``Response = bands`` writes only this file and stops.

.. figure:: ../images/ges_bands.png
   :width: 60%
   :align: center

   GeS (``GeS_wannier_04062024_tb.dat``, ``Nfermi = 20``, ``Bandlist = -1 0 1 2``) on the default rectangular
   path :math:`\Gamma`-X-S-Y-:math:`\Gamma`, plotted with ``tools/plot_bands.py --emin -6 --emax 4``: the window
   bands in colour, energies relative to the VBM along the path.

Path
====

The path is the :ref:`kw-kpath` block of the input: vertices in reduced coordinates along the reciprocal lattice
vectors, each with the number of points to the next vertex (``1`` = the vertex alone, then a jump). Without it,
a default for the lattice is used: :math:`\Gamma`-M-K-:math:`\Gamma` for a hexagonal 2D lattice (K is found as the
zone corner), :math:`\Gamma`-X-S-Y-:math:`\Gamma` for other 2D lattices, plus :math:`\Gamma`-Z in 3D, and
:math:`\Gamma`-X in 1D, about 300 points in all. The k-points are built from all reciprocal lattice vectors, so 1D
and 3D models are handled as well.

Format
======

A header, then one row per k-point:

.. code-block:: text

   # bands along a k-path. Columns: kx ky kz (bohr^-1, Cartesian), s (path length, bohr^-1),
   # E_1 ... E_norb (eV, eigenvalues of the Wannier model, not shifted)
   # vertex  label  row  s  (reduced coordinates along the reciprocal lattice vectors)
   # vertex   1  G                     1    0.00000000   0.0000000   0.0000000   0.0000000
   # vertex   2  M                   111    0.60290282   0.5000000   0.0000000   0.0000000
   # vertex   3  K                   174    0.95098892   0.3333333   0.3333333   0.0000000
   # vertex   4  G                   301    1.64716113   0.0000000   0.0000000   0.0000000
   # Nfermi = 26; Bandlist window bands: 25 26 27 28
   # along the path: VBM (band Nfermi)    -3.926980 eV at s =     0.950989; CBM    -1.329255 eV at s =     0.950989
   # along the path: gap     2.597725 eV; smallest direct gap     2.597725 eV at s =     0.950989
   kx   ky   kz   s   E_1   E_2   ...   E_norb

``kx ky kz``
   Cartesian k-point in :math:`\text{bohr}^{-1}`.

``s``
   Accumulated path length in :math:`\text{bohr}^{-1}`; it does not advance across a jump. Use it as the x-axis,
   with the vertex positions of the header as ticks.

``E_1 ... E_norb``
   All ``norb`` eigenvalues in eV, in ascending order. Band ``E_Nfermi`` is the highest valence band, i.e.
   ``Bandlist`` entry ``0``. The energies are those of the Wannier90 model, **not** shifted to put the Fermi level
   at zero; the header gives the VBM and CBM along the path.

The header line ``Bandlist window bands`` gives the band numbers that enter the optical transitions, and the gap
lines show at a glance whether ``Nfermi`` puts the Fermi level in a gap along the path.

.. code-block:: bash

   python3 tools/plot_bands.py bands_MoS2_spin_wannier_07032024.dat --emin -3 --emax 3

``tools/plot_bands.py`` reads the header: vertex labels for the ticks, the window bands in colour and the VBM at
zero (``--absolute`` keeps the model's energies).

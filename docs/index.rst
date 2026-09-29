.. OptiX documentation master file

.. _Xatu: https://github.com/xatu-code/xatu

==========================================================
OptiX: linear and nonlinear optics of crystals
==========================================================

**OptiX** (executable: ``opticx``) is a Fortran code that computes the **linear and second-order optical
response of crystals**. It works both in the independent-particle approximation (IPA) and with
**excitonic effects** included. You give it a Wannier90 tight-binding model and, optionally, exciton
eigenstates from `Xatu`_. It evaluates:

* the **linear optical conductivity** :math:`\sigma^{ab}(\omega)`, from which the absorbance follows;
* the **shift conductivity** :math:`\sigma^{abc}(0;\omega,-\omega)`, the bulk photovoltaic (shift-current) response.

Each response comes as a single-particle result and, when Xatu excitons are supplied, as an excitonic
result too. That lets you see directly how the electron–hole interaction reshapes the spectrum.

.. note::

   📄 **Reference paper** (citation required when using the code):
   J. J. Esteve-Paredes, M. A. García-Blázquez, A. J. Uría-Álvarez, M. Camarasa-Gómez and J. J. Palacios,
   `Excitons in nonlinear optical responses: shift current in MoS2 and GeS monolayers,
   npj Computational Materials 11, 13 (2025) <https://doi.org/10.1038/s41524-024-01504-2>`_

.. image:: images/ges_shift_sp.png
   :width: 80%
   :align: center

How a calculation works
=======================

A run is driven by one plain-text input file, and every run follows the same pipeline:

.. code-block:: text

   input file ──► Wannier90 _tb.dat ──► k-mesh and bands ──► optical matrix elements ──► optical response
                  (+ Xatu .eigval/.states)                   (single-particle, excitonic)  (σ(ω) written to .dat)

Computing the optical matrix elements is usually the expensive step. They are stored on disk, so you can
compute them once and then reuse them for different frequency windows or broadenings (see
:doc:`workflows`).

Documentation contents
======================

.. toctree::
   :maxdepth: 1
   :caption: Getting started

   installation
   quickstart
   input_file
   workflows

.. toctree::
   :maxdepth: 1
   :caption: Outputs

   outputs/overview
   outputs/linear_conductivity
   outputs/shift_conductivity
   outputs/bands
   outputs/matrix_elements

.. toctree::
   :maxdepth: 1
   :caption: Theory and conventions

   theory/conventions
   theory/linear_response
   theory/shift_current

.. toctree::
   :maxdepth: 1
   :caption: Help and miscellaneous

   troubleshooting
   misc/citing
   misc/license

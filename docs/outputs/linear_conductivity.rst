==========================================
sigma_first — linear optical conductivity
==========================================

Written when ``Response = absorbance``:

.. code-block:: text

   sigma_first_sp_real_<material>.dat     # independent particles
   sigma_first_sp_imag_<material>.dat
   sigma_first_ex_real_<material>.dat     # with excitons (Xatu_interface = true only)
   sigma_first_ex_imag_<material>.dat

Format
======

One row per frequency, ten columns:

.. code-block:: text

   ħω(eV)   σxx   σxy   σxz   σyx   σyy   σyz   σzx   σzy   σzz

The ``_real`` file holds the real parts of these components and the ``_imag`` file the imaginary parts.

Units
=====

Conductivities are in **Hartree atomic units** (:math:`e = \hbar = m_e = 1`, lengths in bohr).

For a **2D** material, the cell "volume" is the unit-cell **area**. The result is then a sheet
conductivity, whose atomic unit is :math:`e^2/\hbar`:

.. math::

   \sigma\,[\text{S}] = \sigma\,[\text{a.u.}] \times \frac{e^2}{\hbar}
   \approx \sigma\,[\text{a.u.}] \times 2.434\times10^{-4}\ \text{S}.

For a 3D material, the atomic unit of conductivity is :math:`e^2/(\hbar a_0)`
(:math:`\approx 4.60\times10^{6}` S/m).

What is computed
================

OptiX evaluates the **absorptive (resonant) part** of the Kubo conductivity: the energy-conserving
:math:`\delta` function is replaced by the broadening function of :ref:`kw-broadening`. See
:doc:`../theory/linear_response` for the formulas. As a consequence:

* :math:`\mathrm{Re}\,\sigma^{aa}` (the diagonal of the ``_real`` file) is the absorption along direction :math:`a`. **This
  is the quantity usually wanted.**
* The ``_imag`` file is the imaginary part of the transition-strength tensor
  :math:`\propto v^a_{cv}v^b_{vc}`. It is antisymmetric (:math:`\sigma^{xy} = -\sigma^{yx}`), vanishes
  on the diagonal, and is non-zero only when time-reversal symmetry is broken (circular dichroism /
  optical Hall response).

.. warning::

   ``sigma_first_*_imag`` is **not** the reactive (dispersive) part of :math:`\sigma^{aa}` related to
   :math:`\mathrm{Re}\,\sigma` by Kramers–Kronig. To get that part, apply a Kramers–Kronig transform to
   :math:`\mathrm{Re}\,\sigma^{aa}(\omega)` yourself.

No spin-degeneracy factor is applied. If your Wannier model has no explicit spin (one orbital per
spatial Wannier function), multiply by 2 for a spin-degenerate system.

From conductivity to absorbance
===============================

For a freestanding 2D layer at normal incidence, with light polarised along :math:`a`, the fraction of
light absorbed is, to lowest order in :math:`\sigma`:

.. math::

   A(\omega) = \frac{4\pi}{c}\,\mathrm{Re}\,\sigma^{aa}(\omega)
   \qquad (\text{atomic units},\ c \approx 137.036).

Equivalently, in SI units, :math:`A = \mathrm{Re}\,\sigma^{aa}/(\varepsilon_0 c)`. For example:

.. code-block:: python

   import numpy as np
   s = np.loadtxt("sigma_first_ex_real_hBN.dat")
   absorbance_x = 4*np.pi/137.035999 * s[:, 1]

Single-particle vs excitonic files
==================================

Both files use the same frequency grid and units and can be plotted together. The ``sp`` file comes from
interband transitions on the k-mesh. The ``ex`` file comes from transitions from the ground state to
each of the ``Exciton_cutoff`` exciton states. Above the energy of the highest exciton included, the
``ex`` spectrum is incomplete.

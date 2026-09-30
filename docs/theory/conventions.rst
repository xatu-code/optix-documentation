===========
Conventions
===========

This page collects the conventions OptiX follows. Read it before comparing its numbers with a paper or
with another code: most "discrepancies" come from one of the points below.

Units
=====

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Quantity
     - Unit
   * - Wannier90 input (lattice, hoppings, positions)
     - Angstrom and eV (the Wannier90 defaults)
   * - Xatu input (k-points, exciton energies)
     - :math:`\text{Angstrom}^{-1}` and eV (the Xatu defaults)
   * - ``Energy_variables``
     - eV
   * - Internal calculations
     - Hartree atomic units (:math:`e=\hbar=m_e=1`; 1 Ha = 27.211385 eV, 1 bohr = 0.529177 Angstrom)
   * - Photon energy column in all spectra
     - eV
   * - Linear conductivity :math:`\sigma^{ab}`
     - atomic units (:math:`e^2/\hbar` for 2D sheets)
   * - Shift conductivity :math:`\sigma^{abc}`
     - :math:`\mu\text{A nm/V}^2` (2D sheet)
   * - Band structure
     - k in :math:`\text{bohr}^{-1}`, energies in eV
   * - Matrix-element files
     - atomic units

Dimensionality and cell volume
==============================

Every response carries a factor :math:`1/(N_k V_\text{cell})`, where :math:`N_k` is the number of k-points
and :math:`V_\text{cell}` is:

* the **length** of the lattice vector in 1D,
* the **area** :math:`|\mathbf{a}_1\times\mathbf{a}_2|` in 2D,
* the **volume** in 3D.

In 2D, the conductivities are therefore **sheet** conductivities: no layer thickness is assumed. To
get a bulk-like value, divide by an effective thickness of your choice.

Frequency axis
==============

* Column 1 of every spectrum is the photon energy :math:`\hbar\omega` of the driving field, in eV.
* The grid has ``n_w`` points starting at ``E_min`` with step ``(E_max - E_min)/n_w``, so ``E_max``
  itself is **not** included.
* For the shift current, :math:`\omega` is the frequency of the incoming light. The response is at zero
  frequency (DC).

Broadening
==========

The energy-conserving delta function of Fermi's golden rule is replaced by a normalised Lorentzian
(default) or Gaussian of width ``eta``:

.. math::

   \delta(x) \to \frac{1}{\pi}\frac{\eta}{x^2+\eta^2}
   \qquad\text{or}\qquad
   \delta(x) \to \frac{1}{\sqrt{2\pi}\,\eta}\,e^{-x^2/2\eta^2}.

For the Lorentzian, ``eta`` is the half width at half maximum. For the Gaussian, it is the standard
deviation (FWHM :math:`= 2.355\,\eta`). The two shapes at the same ``eta`` are **not** equally wide.
Keep this in mind when comparing spectra.

OptiX computes only the **resonant (absorptive)** part of each response: the terms proportional to the
broadened :math:`\delta`. Principal-value (dispersive) parts are not computed.

Occupations and spin
====================

* The system is an **insulator at zero temperature**: bands at or below ``Nfermi`` are full and bands
  above are empty. Metals and finite temperature are not supported.
* **No spin-degeneracy factor** is included anywhere. If the Wannier model is spinless, multiply all
  responses by 2 for a spin-degenerate material. If spin is explicit in the Wannier basis, the result is
  already complete.

k-mesh
======

The Brillouin zone is sampled with a :math:`\Gamma`-centred Monkhorst–Pack mesh, identical to the one Xatu uses.
With ``N = Ncells``, along each reciprocal lattice vector the fractional coordinates are
:math:`u = c/N - 1/2`, :math:`c = 0,\dots,N-1`. For odd :math:`N` they are shifted by :math:`1/(2N)`.
The first reciprocal direction runs fastest.

Derivatives with respect to :math:`\mathbf{k}` (needed for second-order responses) are taken by finite
differences, with a step of :math:`10^{-6}\,\text{bohr}^{-1}` for single-particle quantities. For the exciton
envelopes they are taken on the mesh itself, with periodic wrap-around.

Optical matrix elements
=======================

* The **velocity** matrix elements come from the Wannier Hamiltonian *and* the Wannier90 position matrix
  elements, i.e. the full tight-binding velocity
  :math:`\hat{\mathbf v} = \partial_{\mathbf k}\hat H + i[\hat H,\hat{\mathbf A}]`, including
  intra-cell dipoles. The Wannier functions are assumed orthonormal.
* Second-order responses are evaluated in the **length gauge** (hence the ``lengthgauge`` in the file
  names).
* Eigenvectors from separate diagonalisations carry arbitrary k-dependent phases. OptiX fixes the gauge
  locally before differentiating, and rotates degenerate multiplets into a smooth basis. The Xatu exciton
  envelopes are carried into that same basis.

Sign of the shift current
=========================

The shift conductivity follows the sign convention of Esteve-Paredes *et al.*, npj Comput. Mater. 11, 13
(2025), Eqs. 9 (IPA) and 10 (excitonic). The single-particle and excitonic results use the same
convention, and they agree in the non-interacting limit. Other codes and papers may differ by an overall
sign or by factors of 2 in the definition of the field amplitude.

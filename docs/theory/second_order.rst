.. _second-order:

================================
Second-order response in general
================================

Every second-order process OptiX computes is one branch of a single two-frequency expression,

.. math::

   \sigma^{abc}(\omega_1+\omega_2;\,\omega_1,\omega_2),

evaluated in the length gauge. ``Response`` and ``Frequency_ratio`` choose the branch;
``Energy_variables_2`` opens the full two-dimensional map.

.. list-table::
   :header-rows: 1
   :widths: 24 16 28 32

   * - ``Response``
     - :math:`r=\omega_2/\omega_1`
     - Process
     - Output
   * - ``shg``
     - 1
     - :math:`\sigma(2\omega;\omega,\omega)`, second-harmonic generation
     - ``shg_{sp,ex}_lengthgauge_*.dat``
   * - ``electrooptic``
     - 0
     - :math:`\sigma(\omega;\omega,0)`, the linear electro-optic (Pockels) response
     - ``second_{,ex_}electrooptic_lengthgauge_*.dat``
   * - ``rectification``
     - -1
     - :math:`\sigma(0;\omega,-\omega)`, optical rectification
     - ``second_{,ex_}rectification_lengthgauge_*.dat``
   * - ``general``
     - any
     - arbitrary :math:`r`, or a 2D map
     - ``second_{,ex_}general_lengthgauge_*.dat``

.. _second-order-normalisation:

Normalisation and sign
======================

All second-order outputs use the convention of [Taghizadeh2018]_ and of [EsteveParedes2025]_:

.. math::

   E(t) = \tfrac12\sum_p E(\omega_p)\,e^{-i\omega_p t},\qquad
   J^{(2)a}(t) = \tfrac14\sum_{pq}\sigma^{abc}(\omega_p,\omega_q)\,E^b(\omega_p)E^c(\omega_q)\,
   e^{-i(\omega_p+\omega_q)t}.

For a field :math:`E_0\cos\omega t` along :math:`x` this gives a DC current
:math:`\tfrac14\left[\sigma(0;\omega,-\omega)+\sigma(0;-\omega,\omega)\right]E_0^2` and a
second-harmonic current :math:`\tfrac12\mathrm{Re}\left[\sigma(2\omega;\omega,\omega)e^{-2i\omega t}\right]E_0^2`.
[Taghizadeh2017]_ writes :math:`J^{(2)}` without the :math:`\tfrac14`, so its :math:`\sigma` is four
times smaller for the same current. OptiX converts it.

The sign is the physical one, for the electron charge :math:`e=-|e|`. It is fixed by an independent
**real-time simulation** rather than by derivation. On two-band hBN the position operator is just the
Wannier centres, so minimal coupling :math:`\mathbf k\to\mathbf k+\mathbf A(t)` is exact.
``tools/check_realtime_sign.py`` propagates the density matrix under
:math:`sE_0\cos(\omega t+\phi)e^{\eta t}`. The second-order current is the part even in :math:`s`,
and its dependence on :math:`\phi` separates the DC and :math:`2\omega` responses. ``make
check_realtime_sign`` requires the SHG and the rectification to match this current at 4 and 8 eV, and
the shift current to have its sign on resonance. Measured at :math:`\eta = 0.15` eV, 4–9 eV:

* SHG, single-particle (both methods) and excitonic in the non-interacting limit: :math:`\sim10^{-4}`;
* single-particle rectification: 0.2%;
* ``general`` at :math:`(\hbar\omega_1,\hbar\omega_2) = (6, 3)` eV: :math:`10^{-4}`;
* shift current: equal to the real-time DC current on resonance (1–2%), with the same sign. Below the gap
  it leaves out an off-resonant part that vanishes as :math:`\eta\to0`;
* excitonic rectification: in the non-interacting limit equal to the single-particle rectification to
  :math:`5\times10^{-4}` (``make check_sp_shift``), and hence to the real-time current.

Bookkeeping, for anyone reading the source: the kernels of [Taghizadeh2017]_ and [Taghizadeh2018]_
already contain the electron charge, and the writers multiply them by :math:`-1` (the electron charge
cubed) only to undo the shared :math:`e^3=-1` in ``constants_math::sigma2_au_to_si``. The shift
kernels follow npj Eq. (9), written with :math:`e=1`, and take that factor as it is. The excitonic
``rectification`` is a causal output like ``shg`` and ``general`` and carries the same :math:`-1`
(:ref:`dc-excitonic-rectification`).

Broadening convention
=====================

Every frequency carries :math:`+i\eta`, and the sum frequency is the **sum of the two complex
frequencies**:

.. math::

   \hbar\omega_p = \hbar\omega + i\eta,\qquad
   \hbar\omega_q = r\,\hbar\omega + i\eta,\qquad
   \hbar\omega_\Sigma = \hbar\omega_p + \hbar\omega_q .

For SHG this means :math:`\hbar\omega_\Sigma = 2\hbar\omega + 2i\eta`, not
:math:`2\hbar\omega + i\eta`. Building :math:`\omega_\Sigma` as an independent frequency with a single
:math:`\eta` breaks the equality between the two evaluation methods below.

This holds on the DC line :math:`r = -1` too: ``rectification`` is the whole causal
:math:`\sigma(0;\omega,-\omega)`, with :math:`\hbar\omega_\Sigma = 2i\eta`. The one route with a different
convention is ``Response = shift``, which evaluates the shift current of [EsteveParedes2025]_ with
:math:`\omega_q = -(\omega + i\eta)` and :math:`\omega_\Sigma = 0` (:ref:`dc-limit`).

Independent particles
=====================

The default, ``Sp_method = covariant`` (:ref:`kw-sp-method`), evaluates Eq. (B1b) of [Taghizadeh2018]_
in the independent-particle limit, with every transition :math:`(c,v,\mathbf k)` as a non-interacting
exciton and a generalised derivative that is covariant over groups of nearly degenerate bands. It is
described in :ref:`shg-covariant`. It covers every branch, including the DC line, where it uses the
causal frequencies :math:`\omega_q=-\omega+i\eta`, :math:`\omega_\Sigma=2i\eta`. With these Eq. (B1b)'s
prefactor :math:`i\hbar\omega_\Sigma` does not vanish, and the result follows the real-time current,
including the injection and off-resonant terms. On models without degenerate bands it equals the per-band
route below: hBN to :math:`10^{-10}` (SHG) and :math:`4\times10^{-5}` (rectification).

Eq. (A3a), ``Sp_method = per_band``
-----------------------------------

The per-band route evaluates Eq. (A3a) of [Taghizadeh2017]_ (method A, length gauge,
direct generalised derivative), specialised to a cold intrinsic semiconductor. Two of its four terms
survive, because the two containing :math:`\partial f/\partial\mathbf k` vanish for OptiX's occupation
model (occupations depend on the band index only):

* **term 1**, a three-band term summed over an intermediate band :math:`\lambda`, excluding
  :math:`\lambda = n` and :math:`\lambda = m`;
* **term 2**, the generalised-derivative piece with :math:`n \neq m`.

.. note::

   Term 1 does **not** exclude :math:`n = m`. The exclusions the paper writes for Eq. (A3a) are
   :math:`n \neq \lambda \neq m`, deliberately different from the cyclic condition of Eq. (A3b). At
   :math:`n = m` the factor :math:`p^\lambda_{nn}` is the group velocity and :math:`E_{mn} = 0` is not
   singular. This piece is the intraband contribution whose :math:`1/(\hbar\omega_\Sigma)` becomes the
   **injection current** as :math:`\omega_\Sigma \to 0`; it is also why
   :math:`\hbar\omega_\Sigma = 0` is a genuine singularity for the single-particle branches, and OptiX
   stops rather than returning ``NaN`` if a grid point lands there exactly.

   Its size follows the injection selection rule of [Sipe2000]_: it is :math:`3\times10^{-15}` on hBN
   (class :math:`\bar 6m2`, injection forbidden) and 0.0032% of the peak on In\ :sub:`2`\ Se\ :sub:`3` (class :math:`3m`,
   allowed).

Term 2 needs the **generalised derivative** :math:`(p^\alpha_{nm})_{;k^\beta}` as a gauge-fixed
(parallel-transported) complex quantity. The sum-rule form used by ``shift_sumrule`` is not reliable
here, and the modulus derivative used by ``shift_shiftvector`` is not enough, so OptiX computes it
directly on a four-point k-stencil.

.. warning::

   Term 2 is gauge covariant only if its two momentum factors carry **opposite** band-index order,
   :math:`p^\lambda_{nm}\,g^\alpha_{mn}`. Using the same order makes :math:`\sigma` scale as
   :math:`e^{2i(\phi_m-\phi_n)}`, i.e. gauge dependent and unphysical, for any number of bands. No test
   that does not *vary the gauge* can detect this, which is why gauge invariance under a random
   per-band phase is part of the test suite.

Excitons: Eqs. (B1a) and (B1b)
==============================

The excitonic branches evaluate Appendix B of [Taghizadeh2018]_. The two forms differ in the observable
used for the current:

**Method B, Eq. (B1b)** — the position observable. It needs only the position matrix elements
:math:`X_N` (ground-state-to-exciton) and :math:`X_{NN'}` (exciton-to-exciton), and it is the production
route for every branch except the DC line. Its prefactor is :math:`i\hbar\omega_2`.

**Method A, Eq. (B1a)** — the Heisenberg-momentum observable :math:`\Pi`. OptiX uses it where the DC line
is on the frequency grid: ``rectification`` and any 2D map containing :math:`\omega_1+\omega_2=0` points.
There its term 3, the exciton populations and coherences, reads the bare exciton-exciton current instead
of :math:`\Pi_{nm}`, so that the injection current and the non-interacting limit are resolved on the mesh
(:ref:`dc-excitonic-rectification`).

.. important::

   :math:`\Pi` is **not** the bare momentum. Eq. (10) of [Taghizadeh2018]_ gives
   :math:`\Pi_n = P_n - iF_n`, with :math:`F_n \neq 0` whenever there is an electron–hole interaction;
   on hBN the two differ by 34%, independently of the k-mesh. Anything needing :math:`\Pi` must build it
   from the position elements,

   .. math::

      \Pi_n = -i E_n X_n, \qquad \Pi_{nm} = i(E_n - E_m)\,X_{nm}.

   OptiX does this internally. The Supplementary Information of [EsteveParedes2025]_ uses the same two
   identities to get its Eq. (10) from Eq. (9).

The two methods agree exactly for the diagonal tensor components. Off-diagonal components agree only
after symmetrising the field indices, and then only to the discretisation error of the k-derivative of
:math:`X_{NN'}` — the position components commute only approximately on a finite mesh. On hBN that
residual is :math:`1.8\times10^{-3}`, :math:`8.6\times10^{-4}` and :math:`5.7\times10^{-4}` on 30x30,
45x45 and 60x60 grids, i.e. :math:`\sim 1/N^2`. On a model with near-degenerate bands it is much larger
and converges from further away.

Symmetrisation
==============

OptiX averages over the pair swap
:math:`(\alpha,\omega_p)\leftrightarrow(\beta,\omega_q)`,

.. math::

   \sigma^{abc} \to \tfrac12\left[\sigma^{abc}(\omega_p,\omega_q) + \sigma^{acb}(\omega_q,\omega_p)\right],

which is the intrinsic permutation symmetry the physical tensor must have. The raw kernels are one
ordering each and are deliberately *not* symmetric on their own, so the averaged tensor — not the raw
one — is what OptiX writes and what should be compared with symmetry predictions.

This includes the DC line, where both orderings are evaluated explicitly (the swapped one is not the complex
conjugate of the first there); the averaged tensor then has a :math:`b\leftrightarrow c` symmetric real and
an antisymmetric imaginary part, as the reality of the current requires (:ref:`dc-excitonic-rectification`).

Electro-optic: check convergence before trusting it
===================================================

``electrooptic`` (:math:`r = 0`) is the most grid-hungry branch, on the excitonic path. Terms 1–2 of
Eq. (B1b) contain :math:`\omega_2` and :math:`\omega_q` but **not** :math:`\omega_p`, so in the swapped
pass both poles of term 1 land on resonance together as :math:`\omega_p \to 0`: a near-double pole. It
does not break the formula — it amplifies the discretisation error of :math:`X_{NN'}` by roughly
:math:`1/\eta^2` on top of the usual :math:`1/N^2`.

Verified on hBN: the symmetry violation falls as :math:`1/N^2` (x4.21 from 30x30 to 60x60) and as
:math:`\eta^2`, and at :math:`\eta = 0.6` eV the excitonic result reproduces the single-particle one
with :math:`|\mathrm{corr}| = 0.9999`. Eq. (A3a) has no analogue, because there :math:`\omega_q` enters
only through :math:`\omega_\Sigma`, which is why the single-particle branch is unaffected.

**In practice:** check your system's own symmetry, or the convergence with ``Ncells`` and ``eta``,
before trusting an electro-optic number at small :math:`\eta` — and likewise for the small-:math:`\omega_2`
strip of a 2D map.

Validation
==========

* Gauge invariance under a random per-band phase :math:`\phi_n(\mathbf k)`: machine precision.
* hBN :math:`D_{3h}`, :math:`\sigma^{xxx}=-\sigma^{xyy}=-\sigma^{yxy}=-\sigma^{yyx}`: :math:`6\times10^{-6}`
  on 30x30, 60x60 and 120x120.
* Against an independent NumPy evaluation of Eq. (A3a) on hBN, in absolute value:
  :math:`5\times10^{-7}`.
* ``general`` at :math:`r = 1` against the dedicated SHG path: :math:`4\times10^{-16}` (single particle),
  :math:`8\times10^{-17}` (excitonic).
* The :math:`r \leftrightarrow 1/r` identity
  :math:`\sigma_{1/r}^{abc} = \sigma_r^{acb}` at the same frequency pair: exact.

References
==========

.. [Taghizadeh2017] A. Taghizadeh, F. Hipolito and T. G. Pedersen, *Linear and nonlinear optical
   response of crystals using length and velocity gauges: Effect of basis truncation*,
   Phys. Rev. B **96**, 195413 (2017). Eq. (A3a) is the second-order independent-particle expression
   OptiX evaluates.

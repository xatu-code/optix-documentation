.. _dc-limit:

=================================================================
The DC limit: rectification, shift current, and the anti-diagonal
=================================================================

OptiX can reach the zero-frequency response :math:`\sigma^{abc}(0;\omega,-\omega)` by three different
routes. **Two of them agree to round-off. The third does not, and is not a shift current.** This page
explains why, because the difference is a deliberate convention choice rather than a bug, and reading
the wrong route can flip the sign of your answer.

.. list-table::
   :header-rows: 1
   :widths: 34 34 32

   * - Route
     - What it computes
     - Use it for the shift current?
   * - ``Response = shift`` (``shift_covariant``, ``shift_shiftvector``)
     - Eqs. (9)–(11) of [EsteveParedes2025]_
     - **yes** — the reference implementation
   * - ``Response = rectification``, or ``general`` with ``Frequency_ratio = -1``
     - excitonic: Eq. (B1a) of [Taghizadeh2018]_ under the *DC convention* below;
       single-particle: the full causal response (see :ref:`dc-single-particle`)
     - **yes** — excitonic agrees with the above; single-particle on resonance, plus terms
       that vanish as :math:`\eta\to0`
   * - the line :math:`\omega_2 = -\omega_1` of a 2D map (``Energy_variables_2``)
     - Eq. (B1a) under the *resonant convention*
     - **no** — see :ref:`dc-antidiagonal`

Two conventions for one line
============================

Every second-order response in OptiX is evaluated at complex frequencies. Each field frequency carries
:math:`+i\eta`, and the sum frequency is built as the **sum of the two complex numbers**:

.. math::

   \hbar\omega_p = \hbar\omega + i\eta, \qquad
   \hbar\omega_q = r\,\hbar\omega + i\eta, \qquad
   \hbar\omega_\Sigma = \hbar\omega_p + \hbar\omega_q .

This is the convention of [Taghizadeh2018]_, and it is what makes their method A (the momentum
observable, Eq. B1a) and method B (the position observable, Eq. B1b) agree. Call it the **resonant
convention**. It is correct everywhere the two photons are independent.

The DC line :math:`\omega_q = -\omega_p` is special. Physically the *same* field appears twice, once as
:math:`+\omega` and once as :math:`-\omega`, so the two complex frequencies are not independent: they
are one complex number :math:`z = \omega + i\eta` used as :math:`+z` and :math:`-z`. Then

.. math::

   \hbar\omega_q = -\hbar\omega_p, \qquad \hbar\omega_\Sigma = 0 \;\;\text{exactly}.

Call this the **DC convention**. The excitonic ``Response = rectification`` and any one-dimensional
``general`` scan with ``Frequency_ratio = -1`` use it. The single-particle path does not; see
:ref:`dc-single-particle`.

Why the distinction changes the answer
======================================

Term 3 of Eq. (B1a) of [Taghizadeh2018]_ runs over pairs of excitons :math:`n, m` with the denominator

.. math::

   D_{nm} = (\hbar\omega_q + E_n)(\hbar\omega_p - E_m).

Under the DC convention, :math:`\hbar\omega_q = -\hbar\omega_p = -z`, so
:math:`D_{nm} = (E_n - z)(z - E_m)`, which is **symmetric under** :math:`n \leftrightarrow m` up to a
sign. That symmetry is exactly what time reversal needs in order to cancel term 3: summed over the pair,
the contributions of :math:`(n,m)` and :math:`(m,n)` annihilate. Measured on hBN, term 3 is
:math:`1.8\times10^{-7}` of terms 1 + 2 — i.e. zero.

Under the resonant convention, :math:`\hbar\omega_q = -\hbar\omega + i\eta`, which is :math:`-\bar z`,
not :math:`-z`. The denominator becomes :math:`D_{nm} = (E_n - \bar z)(z - E_m)`, and the
:math:`n \leftrightarrow m` symmetry is broken by the :math:`2i\eta` mismatch. Term 3 then survives —
and it does not survive quietly. Near-degenerate exciton pairs, :math:`E_n \simeq E_m`, put both factors
on resonance at the same :math:`\omega`, giving a **double pole of order** :math:`1/\eta^2`. On hBN the
surviving term 3 is **1.95x larger than terms 1 + 2 combined**, so it does not perturb the answer, it
replaces it.

The symptoms, measured on hBN before the DC convention was adopted, were:

* the magnitude wrong by a factor 2.95 against the single-particle result;
* the :math:`D3h` relation :math:`\sigma^{xxx} = -\sigma^{xyy}` violated by
  :math:`|\sigma^{xxx}/\sigma^{xyy}| = 5.69` instead of 1;
* a spurious peak at 6.35 eV, where no exciton sits;
* :math:`\mathrm{Im}\,\sigma \neq 0`, which [Sipe2000]_ (Sec. VII) forbids.

With the DC convention all four disappear. ``rectification`` then reproduces the independent
implementation of Eqs. (10)–(11) to :math:`3.4\times10^{-9}` on hBN and :math:`8.8\times10^{-8}` in the
non-interacting limit, and :math:`\mathrm{Im}\,\sigma` is identically zero.

.. warning::

   **Do not expect** :math:`\mathrm{Im}\,\sigma = 0` **on every material.** [Sipe2000]_ gives that zero
   only where the **injection current is forbidden by symmetry** — classes :math:`\bar 6 m2`,
   :math:`\bar 6` and :math:`\bar 4 3m`. hBN is :math:`\bar 6 m2`, which is why it is zero there.

   On a lower-symmetry model, injection is *allowed* and a nonzero :math:`\mathrm{Im}\,\sigma` on the
   **single-particle** DC branch is physics, not a defect: on a :math:`C_1` bilayer it reaches 17% of
   :math:`\max|\mathrm{Re}\,\sigma|`. The controlled demonstration is a flat/buckled pair of the same
   two-band model — identical bands, :math:`\bar 6 m2` against :math:`3m` — whose ratio of
   :math:`\mathrm{Im}` to :math:`\mathrm{Re}` differs by up to :math:`3\times10^{5}`.

   The **excitonic** branch reports :math:`\mathrm{Im}\,\sigma = 0` on every material, so it is not
   independent evidence of the selection rule: it takes the real part at the end. And what it discards
   there is *not* an injection current either — that part fails the :math:`\tau` test described in
   :ref:`dc-imaginary-part`, because the excitonic expression has no denominator that can vanish.

What the DC convention does, precisely
--------------------------------------

For ``Response = rectification`` and ``general`` at ``Frequency_ratio = -1``, OptiX:

#. sets :math:`\hbar\omega_q = -\hbar\omega_p` (the same complex :math:`z`, used as :math:`\pm z`) and
   :math:`\hbar\omega_\Sigma = 0` exactly — no :math:`\eta` on the sum-frequency pole;
#. evaluates Eq. (B1a) (method A), because Eq. (B1b) carries a prefactor :math:`i\hbar\omega_2` that
   vanishes identically at :math:`\omega_\Sigma = 0` and would return zero;
#. pairs the field indices at fixed frequencies, each element with the complex conjugate of its
   index-swapped partner, :math:`\sigma^{abc}\to\frac12(\sigma^{abc}+\sigma^{acb\,*})` — the partner that
   the reality of the current requires on this line. It does **not** average over the
   :math:`(\alpha,\omega_p)\leftrightarrow(\beta,\omega_q)` pair swap used off the DC line, which at
   :math:`\omega_q = -\omega_p` would annihilate the result;
#. takes :math:`\mathrm{Re}\,\sigma` at the end, following Supplementary Note 5 of [EsteveParedes2025]_.

The log states which branch was taken::

   400 frequency pairs, 400 excitons  [method A, Eq. (B1a): omega_2 = 0 is in range]
   DC branch: w_q = -w_p, w_2 = 0, b<->c symmetrisation only

.. _dc-single-particle:

The single-particle DC line
---------------------------

The single-particle rectification (default ``Sp_method = covariant``) does **not** use the DC convention.
It uses the causal frequencies of the physical problem, :math:`\hbar\omega_p=\hbar\omega+i\eta`,
:math:`\hbar\omega_q=-\hbar\omega+i\eta`, :math:`\hbar\omega_\Sigma=2i\eta`, so Eq. (B1b)'s
prefactor stays finite and method B can be used. Its result is the DC current of a real-time simulation,
to 0.2% on hBN (:ref:`second-order-normalisation`). That current contains more than the shift current:

* on resonance it **equals the shift current** (hBN, :math:`\sigma^{xxx}` at the peak: ratio 0.995, same
  sign, correlation over 3–11 eV 0.9999 at :math:`\eta = 0.05` eV);
* below the gap it adds an off-resonant part. That part is proportional to :math:`\eta` (hBN, largest
  deviation below 6 eV: :math:`1.2\times10^{-2}`, :math:`6.1\times10^{-3}`, :math:`3.1\times10^{-3}`
  at :math:`\eta` = 0.2, 0.1, 0.05 eV), so it vanishes in the clean limit;
* its antisymmetric imaginary part is the **injection current** (below).

The DC convention would make Eq. (B1b) vanish, and the excitonic path then needs method A and its
:math:`\Pi` elements. The independent-particle problem does not need them, which is why the two paths
differ here. In the non-interacting limit the excitonic rectification therefore equals the *shift* part
of the single-particle one, not all of it.

.. _dc-antidiagonal:

The anti-diagonal of a 2D map is not a shift current
====================================================

A two-dimensional map (``Energy_variables_2``) crosses the DC line along its anti-diagonal
:math:`\omega_2 = -\omega_1`. **OptiX deliberately does not switch convention there.** Changing the
prescription on a single line of a two-dimensional grid would put an :math:`O(1)` discontinuity along
that line, and the map would no longer be a continuous function of :math:`(\omega_1,\omega_2)`. The map
is a sum-frequency response, evaluated consistently with the resonant convention everywhere, and its
anti-diagonal inherits the surviving term 3 described above.

The size of the effect is not subtle. Measured on an AB-stacked ReS\ :sub:`2` bilayer (2700 excitons,
:math:`\eta = 0.05` eV), comparing the map's anti-diagonal against ``Response = rectification`` on the
same frequencies and the same exciton basis:

.. list-table::
   :header-rows: 1
   :widths: 20 26 26 28

   * - Component
     - ``rectification``, max
     - map anti-diagonal, max
     - correlation
   * - :math:`\sigma^{zzz}`
     - 9.42
     - 9.62
     - **-0.983**
   * - :math:`\sigma^{xzz}`
     - 6.96
     - 8.42
     - **-0.993**
   * - :math:`\sigma^{zxz}`
     - 7.00
     - 6.42
     - **-0.963**
   * - :math:`\sigma^{yyy}`
     - 3.54
     - 3.46
     - **-0.472**

The magnitudes are comparable and, over the tensor as a whole, the correlation is close to :math:`-1`
(**-0.920** across all 27 components, least-squares scale **-0.925**): along the anti-diagonal the map
is approximately the **negative** of the shift current. Slicing it and calling it a shift current does
not give you a noisy answer, it gives you a sign-flipped one. The map slice also carries
:math:`\mathrm{Im}\,\sigma` up to 4.00 in these units, where the true DC response has
:math:`\mathrm{Im}\,\sigma = 0` identically — a quick way to tell the two apart in your own data.

.. note::

   The sign flip is an **aggregate** property, not a per-component identity. The :math:`\sigma^{yyy}`
   row above makes the point: the anti-correlation runs from -0.993 on the largest components down to
   -0.104 on the smallest, so a weak component's anti-diagonal may bear little resemblance to its shift
   current in either sign. Do not use "it is minus the shift current" as a correction factor.

   These numbers were regenerated on 2026-09-30 with the corrected conduction-band order
   :math:`c = [60, 61]`; an earlier version of this table quoted values computed with the bands
   swapped.

.. warning::

   Do not read :math:`\sigma^{abc}(0;\omega,-\omega)` off the anti-diagonal of a 2D map. Use
   ``Response = rectification`` (or ``shift_shiftvector``), which costs one extra one-dimensional run.

A tempting fix that does not work
=================================

The obvious way to remove the special case is to make the broadening follow the sign of the frequency
everywhere, :math:`\omega_j \to \omega_j + i\,\mathrm{sgn}(\omega_j)\,\eta`, so that
:math:`\omega_q = -\omega_p` comes out automatically. **This was tried and rejected.** For
:math:`\omega_p > 0 > \omega_q` the two broadenings cancel in the sum,

.. math::

   \hbar\omega_\Sigma = \hbar\omega_p + \hbar\omega_q
   = \hbar(\omega_p + \omega_q) + i\eta - i\eta ,
   \qquad \mathrm{Im}\,\hbar\omega_\Sigma = 0 \;\;\text{exactly},

so terms 1 and 2 of Eq. (B1a) acquire an **undamped** two-photon pole wherever
:math:`\omega_p + \omega_q = \pm E_n`. Measured: :math:`|\sigma|` jumps to 107.6 against a background of
4.67, with the height set only by how close the grid lands to the pole, and ``Inf``/``NaN`` on an exact
hit — over the whole :math:`\omega_p\omega_q < 0` half of the map, plus a 2.5x jump across
:math:`\omega_q = 0`. The DC line itself is safe only because :math:`\omega_\Sigma = 0` lies in the gap,
where no exciton is resonant. The special case is therefore kept on purpose.

How well the two good routes agree
==================================

The agreement between ``rectification`` and the shift-current implementation is limited by the **time
reversal symmetry of your tight-binding model**, not by the k-mesh or the exciton count. Term 3 cancels
by time reversal, so a Wannier model that breaks it leaves a residue. Measured across four materials,
as the raw :math:`\max|\Delta\sigma| / \max|\sigma|` between the two routes:

.. list-table::
   :header-rows: 1
   :widths: 20 20 28 32

   * - Material
     - Point group
     - :math:`\max|E_n(-\mathbf k)-E_n(\mathbf k)|`
     - agreement
   * - hBN
     - :math:`D_{3h}`
     - exact
     - :math:`3.4\times10^{-9}`
   * - ReS\ :sub:`2` (AB bilayer)
     - :math:`C_1` (none)
     - :math:`3.1\times10^{-4}` meV
     - :math:`1.2\times10^{-6}`
   * - In\ :sub:`2`\ Se\ :sub:`3`
     - :math:`C_{3v}`
     - 13.8 meV
     - :math:`9.5\times10^{-2}`
   * - MoSe\ :sub:`2`
     - :math:`D_{3h}`
     - 121.4 meV
     - :math:`6.4\times10^{-1}`

Note that ReS\ :sub:`2` has **no point symmetry at all** and still agrees to :math:`10^{-6}`, while MoSe\ :sub:`2` is in
the same crystal class as hBN and is the worst of the four. The controlling quantity is time reversal.
If the two routes disagree on your material, check
:math:`E_n(-\mathbf k) = E_n(\mathbf k)` on your production mesh before suspecting the code.

References
==========

.. [Taghizadeh2018] A. Taghizadeh and T. G. Pedersen, *Gauge invariance of excitonic linear and
   nonlinear optical response*, Phys. Rev. B **97**, 205432 (2018). Appendix B: Eq. (B1a) is the
   momentum-observable form (method A), Eq. (B1b) the position-observable form (method B).

.. [EsteveParedes2025] J. J. Esteve-Paredes, M. A. García-Blázquez, A. J. Uría-Álvarez,
   M. Camarasa-Gómez and J. J. Palacios, *Excitons in nonlinear optical responses: shift current in
   MoS2 and GeS monolayers*, npj Comput. Mater. **11**, 13 (2025). Main Eqs. (8)–(11);
   Supplementary Note 5 for the real part of the static factor.

.. _dc-imaginary-part:

The DC tensor contains both the shift and the injection current
----------------------------------------------------------------

The quadratic DC photocurrent splits into a **shift** and an **injection** contribution, and following
the symmetry classification of Wang and Qian they couple to different parts of the field bilinear:

.. math::

   J^a = \big[\sigma^{abc} + \eta_M^{abc}\big]\,\mathrm{Re}\{E^bE^{c*}\}
       + i\big[\sigma_M^{abc} + \eta^{abc}\big]\,\mathrm{Im}\{E^bE^{c*}\}.

:math:`\mathrm{Re}\{E^bE^{c*}\}` is **symmetric** under :math:`b\leftrightarrow c` and
:math:`\mathrm{Im}\{E^bE^{c*}\}` is **antisymmetric**, so with the reality constraint both live in
:math:`\mathrm{Re}\,\sigma_T`:

* **shift** = the :math:`b\leftrightarrow c` **symmetric** part,
* **injection** = the :math:`b\leftrightarrow c` **antisymmetric** part.

The two paths treat these parts differently. The **single-particle** output keeps both: its
symmetrisation (below) removes only what cannot couple to any field, and the injection current stays in
the antisymmetric imaginary part. The **excitonic** DC branch writes the real part only, i.e. the shift
current; the antisymmetric imaginary part, which it computes, is discarded by that projection. That is
not a loss, because what the excitonic expression puts there is not an injection current (see the warning
below).

How large the antisymmetric part is, by point group (determined by explicit search over operations that
preserve the lattice, the Wannier centres and :math:`H(\mathbf R)`):

.. list-table::
   :header-rows: 1
   :widths: 30 14 20 20 16

   * - model
     - group
     - independent of 27
     - antisym (injection)
     - measured
   * - flat hBN
     - :math:`D_{3h}`
     - 1
     - **0** — forbidden
     - 0.2 % (noise)
   * - buckled hBN
     - :math:`C_{3v}`
     - 5
     - 1
     - 154 %
   * - in-plane-displaced hBN
     - :math:`C_1`
     - 27
     - 9
     - 98 %

The computed tensors land in the allowed subspace: buckled's antisymmetric part lies in its single
allowed injection channel to 2e-6 (single-particle) and 0.6 % (excitonic, k-grid discretisation).

.. _dc-why-symmetrised:

Why the DC output is symmetrised
--------------------------------

The current is :math:`J^a=\sum_{pq}\sigma^{abc}(\omega_p,\omega_q)\,E^b(\omega_p)E^c(\omega_q)`, summed over
both orderings of the two fields. For the DC response the terms :math:`(\omega,-\omega)` and
:math:`(-\omega,\omega)` multiply the same pair of field components, so only the combination

.. math::

   \tfrac12\left[\sigma^{abc}(0;\omega,-\omega) + \sigma^{acb}(0;-\omega,\omega)\right]

ever reaches the current. Any part of a kernel that changes sign under that swap gives **zero current for
every field**. Such a part is also not unique: Eqs. (B1a) and (B1b) of [Taghizadeh2018]_, or the same formula
with its terms in another order, give different unsymmetrised tensors but the same symmetrised one. On
buckled hBN the unsymmetrised single-particle kernel has an antisymmetric real part of 3.17 (at
:math:`\eta=0.05` eV), while the physical tensor of a time-reversal-symmetric system has none. Left in
the output, such a part would make component-by-component comparisons with symmetry predictions, or with
another code, fail for no physical reason. The symmetrisation removes exactly that part and nothing else.

* **Single particle** — the pair average above, with both frequencies swapped. The output keeps the shift
  current (symmetric real part) **and** the injection current (antisymmetric imaginary part).
* **Excitons** — the pair average cancels the result identically when :math:`\omega_q=-\omega_p`, so the
  branch pairs the indices at fixed frequencies instead, with the complex-conjugate partner (step 3 above).
  That gives the same real part, which is all it writes.

Two cases where symmetrising **would** discard something real, and why they do not apply:

* the antisymmetric part couples only to circularly polarised light, since
  :math:`\mathrm{Im}\{E^bE^{c*}\}=0` for linear polarisation. For circular light, the injection current
  is in the single-particle output; the excitonic expressions cannot produce one (warning below);
* a circular *shift* current, antisymmetric but not growing with the relaxation time, exists only when time
  reversal is broken. The excitonic DC branch relies on time reversal (its term 3 cancels only then), so it
  does not describe such materials either way.

Extracting the injection current
---------------------------------

The two contributions separate by **where they sit in the complex tensor**, not merely by
:math:`b\leftrightarrow c` parity:

.. math::

   \text{shift} = \text{sym}_{bc}\big[\mathrm{Re}\,\sigma\big],
   \qquad
   \text{injection} = \text{antisym}_{bc}\big[\mathrm{Im}\,\sigma\big].

The injection term arises from taking the imaginary part of *every* denominator. For
:math:`n \neq m` that vanishes as the scattering time :math:`\tau` grows, but where a denominator
itself vanishes (:math:`n = m`, the intraband/group-velocity term) it produces a factor
:math:`\tau`. **That** :math:`\tau` **scaling is the signature**, and it is what distinguishes an
injection current from any other antisymmetric response.

**The single-particle injection current is already in the output.** ``Response = rectification``
writes ``second_rectification_lengthgauge_<material>.dat`` with real and imaginary parts, and the
single-particle path applies no real-part projection. Take the :math:`b\leftrightarrow c`
antisymmetric part of the imaginary columns. Both ``Sp_method`` values give the same injection current
(buckled hBN). Verified on a model pair with identical bands (values in the units used before
2026-10-06; today's output is :math:`-4` times larger, which leaves the ratios unchanged):

* it obeys the selection rule — 1.4e-5 where injection is forbidden (:math:`\bar 6 m2`) against 3.75
  where it is allowed (:math:`3m`), a ratio of :math:`2.8\times10^{5}`;
* its integrated weight scales as :math:`1/\eta` to three digits (ratios 2.002 and 2.000 across
  :math:`\eta` = 0.025, 0.05, 0.10 eV), i.e. :math:`\propto\tau`, as an injection *rate* must.

The intraband term that generates it is 44 % of the raw tensor on a low-symmetry model, and is
numerically zero (2.7e-5) where symmetry forbids it.

.. warning::

   **The excitonic branch does not provide an injection current.** Its antisymmetric imaginary part
   does **not** scale as :math:`\tau` (ratios 1.23 and 1.27 against the single-particle 2.00), because
   Eq. (B1a) as implemented contains only denominators :math:`(\hbar\omega_2 - E_n)` and
   :math:`(\hbar\omega_q - E_m)` — no :math:`(E_n - E_m)` that can vanish and supply the
   :math:`\tau`. The excitonic formalism replaces the single-particle triple sum over states with a
   double sum over :math:`Q=0` exciton states, so the analogue of the injection-generating term would
   be the :math:`\chi = \chi'` diagonal of that double sum, which the present expression does not
   carry.

   This is an absence in the formalism as implemented, not a corrupted result: the excitonic **shift**
   current is unaffected. Use the single-particle branch for injection.

.. [Sipe2000] J. E. Sipe and A. I. Shkrebtii, *Second-order optical response in semiconductors*,
   Phys. Rev. B **61**, 5337 (2000). Sec. VII derives
   :math:`\mathrm{Im}\,\sigma(0;\omega,-\omega) = 0` and the selection rule that forbids the injection
   current in classes :math:`\bar 6 m2`, :math:`\bar 6` and :math:`\bar 4 3m`.

.. [Ahn2020] J. Ahn, G.-Y. Guo and N. Nagaosa, *Low-frequency divergence and quantum geometry of the
   bulk photovoltaic effect in topological semimetals*, Phys. Rev. X **10**, 041041 (2020). Sign
   convention of the shift vector used by OptiX.

===================
Shift conductivity
===================

The shift current is a DC photocurrent that appears in non-centrosymmetric crystals under uniform
illumination. It is the zero-frequency part of the second-order response,
:math:`\sigma^{abc}(0;\omega,-\omega)`. OptiX evaluates it in the length gauge, following Esteve-Paredes
*et al.*, npj Comput. Mater. **11**, 13 (2025). This page summarises the expressions; the paper and its
Supplementary Information have the full derivation and conventions.

Independent-particle approximation
==================================

Let :math:`r^a_{nm} = v^a_{nm}/(i\,\varepsilon_{nm})` (:math:`n\ne m`) be the interband position matrix
elements, and :math:`r^{b;a}_{nm}` their generalised derivatives. The shift conductivity is

.. math::

   \sigma^{abc}(0;\omega,-\omega) = -\frac{\pi}{2 N_k V}\sum_{\mathbf k}\sum_{nm} f_{nm}\;
   K^{abc}_{nm}(\mathbf k)\;\delta(\omega-\varepsilon_{nm}),
   \qquad f_{nm} = f_n - f_m,

and :math:`\mathrm{Re}\,\sigma^{abc}` is written to ``shift_sp_lengthgauge_<material>.dat``. The kernel
:math:`K^{abc}_{nm}`, a combination of :math:`r^b_{nm}r^{c;a}_{mn}` and :math:`r^c_{nm}r^{b;a}_{mn}`,
can be evaluated in several equivalent ways. ``Response`` chooses which:

``shift_shiftvector``
   Writes the generalised derivative through the **shift vector**

   .. math::

      R^{a,b}_{nm} = \partial_{k^a}\phi^b_{nm} - \mathcal{A}^a_{nn} + \mathcal{A}^a_{mm},

   where :math:`\phi^b_{nm}` is the phase of :math:`r^b_{nm}` and :math:`\mathcal{A}` the Berry
   connection. The kernel then has two pieces:

   * the **shift-vector term** :math:`\propto (R^{a,b}_{mn}-R^{a,c}_{nm})\,v^c_{nm}v^b_{mn}/\varepsilon_{nm}^2`.
     For :math:`b = c` it reduces to the textbook expression
     :math:`\sigma^{abb}\propto\sum f_{nm}R^{a,b}_{nm}|r^b_{nm}|^2\delta(\omega-\varepsilon_{mn})`;
   * an **amplitude-gradient term**
     :math:`\propto \sin(\phi^b-\phi^c)\,(\rho_b\,\partial_a\rho_c-\rho_c\,\partial_a\rho_b)`, with
     :math:`\rho_b = |r^b_{nm}|`. It vanishes for :math:`b = c` but is required for the other components.

   Only gauge-invariant quantities are differentiated (:math:`R` and :math:`|v|`), which makes this the
   most robust option.

``shift_sumrule``
   Writes the generalised derivative through the sum rule over intermediate bands
   :math:`p`, which involves :math:`r^b_{np}r^a_{pm}` and similar terms. This converges only when
   ``Bandlist`` includes many remote bands.

Excitonic shift current
=======================

With excitons, the transitions go through exciton states :math:`|N\rangle`. The response involves the
ground-state-to-exciton position elements :math:`X^a_N` and the exciton-to-exciton elements
:math:`X^a_{NN'}`. The latter include the k-derivative of the exciton envelopes, and are built from the
Xatu eigenvectors when ``OME_ex = nonlinear``. Schematically,

.. math::

   \sigma^{abc}_\text{ex}(0;\omega,-\omega) = \frac{\pi}{N_k V}\sum_{NN'}
   \mathrm{Re}\,S^{abc}_{NN'}\;\delta(\omega - E_N),

where :math:`S_{NN'}` combines :math:`X_N`, :math:`X_{NN'}` and energy denominators (Eq. 10 of the
reference paper). Following the paper's Supplementary Note 5, the real part of :math:`S` is used. The
result is symmetrised over the field indices,
:math:`\sigma^{abc}\to\frac12(\sigma^{abc}+\sigma^{acb})`, before it is written.

The double sum over excitons scales as :math:`N^2`, which is why ``Exciton_cutoff`` dominates the cost
of these runs.

Non-interacting limit
=====================

With the electron–hole interaction turned off in Xatu, the excitonic shift current reduces to the
single-particle one (after :math:`b\leftrightarrow c` symmetrisation).
This is a useful check of a new setup.

References
==========

* J. E. Sipe and A. I. Shkrebtii, Phys. Rev. B **61**, 5337 (2000) — length-gauge second-order response.
* B. M. Fregoso, T. Morimoto and J. E. Moore, Phys. Rev. B **96**, 075421 (2017).
* J. Ahn, G.-Y. Guo and N. Nagaosa, Phys. Rev. X **10**, 041041 (2020) — shift-vector formulation.
* A. Taghizadeh and T. G. Pedersen, Phys. Rev. B **97**, 205432 (2018) — excitonic matrix elements.
* J. J. Esteve-Paredes *et al.*, npj Comput. Mater. **11**, 13 (2025).

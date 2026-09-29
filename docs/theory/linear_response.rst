===========================
Linear optical conductivity
===========================

This page gives the expressions OptiX evaluates for ``Response = absorbance``, in atomic units
(:math:`e = \hbar = 1`). See :doc:`conventions` for the broadening, occupations and cell volume
:math:`V`.

Independent-particle approximation
==================================

With Bloch states :math:`|n\mathbf{k}\rangle` of energy :math:`\varepsilon_{n\mathbf k}`, occupations
:math:`f_n \in \{0,1\}` and velocity matrix elements :math:`v^a_{nm}(\mathbf k)`, OptiX evaluates the
absorptive part of the Kubo formula:

.. math::

   \sigma^{ab}_\text{sp}(\omega) = -\frac{\pi}{N_k V}\sum_{\mathbf k}\sum_{n\neq m}
   \frac{f_n - f_m}{\varepsilon_{nm}}\; v^a_{nm}\,v^b_{mn}\;
   \delta(\omega - \varepsilon_{nm}),
   \qquad \varepsilon_{nm} = \varepsilon_{n\mathbf k}-\varepsilon_{m\mathbf k}.

Only the resonant term (:math:`n` = conduction, :math:`m` = valence) contributes at positive
frequency, so this reduces to the familiar

.. math::

   \sigma^{ab}_\text{sp}(\omega) \simeq \frac{\pi}{N_k V}\sum_{\mathbf k}\sum_{c,v}
   \frac{v^a_{cv}\,v^b_{vc}}{\varepsilon_{cv}}\;\delta(\omega-\varepsilon_{cv}).

The sums run over the bands in ``Bandlist``.

Excitonic response
==================

With excitons from Xatu, :math:`|N\rangle = \sum_{vc\mathbf k}\psi^{N}_{vc}(\mathbf k)\,
c^\dagger_{c\mathbf k}c_{v\mathbf k}|0\rangle`, of energy :math:`E_N`, the transitions go from the
ground state to each exciton. The single-particle velocity is replaced by

.. math::

   P^a_N = \sum_{vc\mathbf k}\psi^N_{vc}(\mathbf k)\;v^a_{vc}(\mathbf k),

and the conductivity becomes a sum over the ``Exciton_cutoff`` lowest excitons:

.. math::

   \sigma^{ab}_\text{ex}(\omega) = \frac{\pi}{N_k V}\sum_{N}
   \frac{\left(P^a_N\right)^{*}P^b_N}{E_N}\;\delta(\omega - E_N).

:math:`P^a_N` are the values stored in ``ome_linear_ex_<material>.omeex``. Excitons with
:math:`P_N \approx 0` are dark.

If the electron–hole interaction is switched off in Xatu, :math:`E_N` becomes the band-to-band energy
and :math:`\psi^N` a single :math:`(v,c,\mathbf k)` pair. :math:`\sigma_\text{ex}` then reduces to
:math:`\sigma_\text{sp}`. This is a useful sanity check.

References
==========

* F. Wooten, *Optical Properties of Solids* (Academic Press, 1972) — Kubo formula in the IPA.
* A. Taghizadeh and T. G. Pedersen, Phys. Rev. B **97**, 205432 (2018) — excitonic optical matrix
  elements.
* J. J. Esteve-Paredes *et al.*, npj Comput. Mater. **11**, 13 (2025).

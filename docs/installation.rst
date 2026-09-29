============
Installation
============

OptiX is written in Fortran 90. It needs:

* a Fortran compiler (``gfortran`` is the default and the tested one),
* OpenMP (shipped with ``gfortran``),
* BLAS/LAPACK, either through **OpenBLAS** (default) or **Intel MKL**.

Getting the code
================

.. code-block:: bash

   git clone https://github.com/xatu-code/opticx.git
   cd opticx

The repository layout is:

.. code-block:: text

   opticx/
   ├── main/opticx.f90            # main program
   ├── src/                       # modules (parsers, matrix elements, conductivities)
   ├── bin/                       # executable + example input files
   ├── wannier90_files_input/     # example Wannier90 models (GeS, hBN)
   ├── tests/                     # validation programs
   └── Makefile

Build
=====

.. tab-set::

   .. tab-item:: Ubuntu / Debian / WSL

      Install the compiler and OpenBLAS, then build:

      .. code-block:: bash

         sudo apt-get install gfortran libopenblas-dev
         make

   .. tab-item:: macOS (Homebrew)

      Install the dependencies with Homebrew, using its ``gcc`` rather than the system compiler:

      .. code-block:: bash

         brew install gcc openblas

      Then set the compiler and library location at the top of the ``Makefile`` and run ``make``:

      .. code-block:: make

         FC     = gfortran-13
         LIBS   = -L/opt/homebrew/opt/openblas/lib -lopenblas -fopenmp -lgfortran

   .. tab-item:: Intel MKL

      To link against MKL instead of OpenBLAS:

      .. code-block:: bash

         make USE_MKL=1

      This assumes a system-wide MKL (e.g. ``sudo apt-get install intel-mkl``), linked with
      ``-lmkl_rt -fopenmp -lpthread -lm -ldl``. If MKL is installed elsewhere, uncomment the ``MKLROOT``
      and ``LIBS`` lines in the MKL block of the ``Makefile`` and adjust the path.

The executable is ``bin/opticx``.

Compiler flags
==============

The compiler and flags are set by ``FC`` and ``FFLAGS`` in the ``Makefile``. You can also override them
on the command line:

.. code-block:: bash

   make FFLAGS="-O3 -ffree-line-length-none"

The default ``FFLAGS`` include ``-g -fcheck=all``. That is convenient during development, but runtime
bound checking slows production runs noticeably. For large calculations, consider removing
``-fcheck=all``.

.. note::

   If compilation stops with ``Line truncated ... [-Werror=line-truncation]``, add
   ``-ffree-line-length-none`` to ``FFLAGS`` as shown above.

To start over from a clean tree:

.. code-block:: bash

   make clean

Running
=======

A calculation is launched by passing the input file as the only argument:

.. code-block:: bash

   /path/to/opticx/bin/opticx input.txt

All output files are written to the **current working directory**, so run OptiX from the directory
where you want the results. The file paths inside the input file can be absolute or relative to that
directory.

Parallelism and memory
----------------------

OptiX is parallelised with OpenMP over k-points and excitons. Set the number of threads with:

.. code-block:: bash

   export OMP_NUM_THREADS=8

Several routines put mesh-sized arrays on the stack. For medium or large meshes, raise the stack
limits before running, or the program may crash with a segmentation fault:

.. code-block:: bash

   ulimit -s unlimited
   export OMP_STACKSIZE=512M

Tests
=====

The ``tests/`` directory holds validation programs that reuse the compiled modules. For example,
the shift-kernel equivalence check:

.. code-block:: bash

   make test
   bin/test_shift_kernel_equivalence

Each test prints ``ALL TESTS PASSED`` (or ``ALL CHECKS PASSED``) on success.

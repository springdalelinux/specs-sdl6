# The blacs packages should probably provide these.
%global _blacs_openmpi_load \
 . /etc/profile.d/modules.sh; \
 module load blacs-openmpi-%{_arch}; \
 export CFLAGS="$CFLAGS %{optflags}";
%global _blacs_openmpi_unload \
 . /etc/profile.d/modules.sh; \
 module unload blacs-openmpi-%{_arch};

%global _blacs_mpich2_load \
 . /etc/profile.d/modules.sh; \
 module load blacs-mpich2-%{_arch}; \
 export CFLAGS="$CFLAGS %{optflags}";
%global _blacs_mpich2_unload \
 . /etc/profile.d/modules.sh; \
 module unload blacs-mpich2-%{_arch};

Summary: A subset of LAPACK routines redesigned for heterogenous computing
Name: scalapack
Version: 1.7.5
Release: 10%{?dist}
# This is freely distributable without any restrictions.
License: Public Domain
Group: Development/Libraries
URL: http://www.netlib.org/lapack-dev/
Source0: http://www.netlib.org/scalapack/scalapack-%{version}.tgz
BuildRequires: lapack-devel, blas-devel
BuildRequires: gcc-gfortran, glibc-devel
BuildRequires: blacs-mpich2-devel, mpich2-devel-static
BuildRequires: blacs-openmpi-devel, openmpi-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch0: scalapack-1.7-fedora.patch

%description
The ScaLAPACK (or Scalable LAPACK) library includes a subset 
of LAPACK routines redesigned for distributed memory MIMD 
parallel computers. It is currently written in a 
Single-Program-Multiple-Data style using explicit message 
passing for interprocessor communication. It assumes 
matrices are laid out in a two-dimensional block cyclic 
decomposition.

ScaLAPACK is designed for heterogeneous computing and is 
portable on any computer that supports MPI or PVM.

Like LAPACK, the ScaLAPACK routines are based on 
block-partitioned algorithms in order to minimize the frequency 
of data movement between different levels of the memory hierarchy. 
(For such machines, the memory hierarchy includes the off-processor 
memory of other processors, in addition to the hierarchy of registers, 
cache, and local memory on each processor.) The fundamental building 
blocks of the ScaLAPACK library are distributed memory versions (PBLAS) 
of the Level 1, 2 and 3 BLAS, and a set of Basic Linear Algebra 
Communication Subprograms (BLACS) for communication tasks that arise 
frequently in parallel linear algebra computations. In the ScaLAPACK 
routines, all interprocessor communication occurs within the PBLAS and the 
BLACS. One of the design goals of ScaLAPACK was to have the ScaLAPACK 
routines resemble their LAPACK equivalents as much as possible. 

%package common
Summary: Common files for scalapack
Group: Development/Libraries

%description common
The ScaLAPACK (or Scalable LAPACK) library includes a subset
of LAPACK routines redesigned for distributed memory MIMD
parallel computers. It is currently written in a
Single-Program-Multiple-Data style using explicit message
passing for interprocessor communication. It assumes
matrices are laid out in a two-dimensional block cyclic
decomposition.

ScaLAPACK is designed for heterogeneous computing and is
portable on any computer that supports MPI or PVM.

Like LAPACK, the ScaLAPACK routines are based on
block-partitioned algorithms in order to minimize the frequency
of data movement between different levels of the memory hierarchy.
(For such machines, the memory hierarchy includes the off-processor
memory of other processors, in addition to the hierarchy of registers,
cache, and local memory on each processor.) The fundamental building
blocks of the ScaLAPACK library are distributed memory versions (PBLAS)
of the Level 1, 2 and 3 BLAS, and a set of Basic Linear Algebra
Communication Subprograms (BLACS) for communication tasks that arise
frequently in parallel linear algebra computations. In the ScaLAPACK
routines, all interprocessor communication occurs within the PBLAS and the
BLACS. One of the design goals of ScaLAPACK was to have the ScaLAPACK
routines resemble their LAPACK equivalents as much as possible.

This package contains common files which are not specific to any MPI implementation.

%package mpich2
Summary: ScaLAPACK libraries compiled against mpich2
Group: Development/Libraries
Requires: %{name}-common = %{version}-%{release}
Requires: environment-modules
# This is a lie, but something needs to obsolete it.
Provides: %{name}-lam = %{version}-%{release}
Obsoletes: %{name}-lam <= 1.7.5-7

%description mpich2
The ScaLAPACK (or Scalable LAPACK) library includes a subset
of LAPACK routines redesigned for distributed memory MIMD
parallel computers. It is currently written in a
Single-Program-Multiple-Data style using explicit message
passing for interprocessor communication. It assumes
matrices are laid out in a two-dimensional block cyclic
decomposition.

ScaLAPACK is designed for heterogeneous computing and is
portable on any computer that supports MPI or PVM.

Like LAPACK, the ScaLAPACK routines are based on
block-partitioned algorithms in order to minimize the frequency
of data movement between different levels of the memory hierarchy.
(For such machines, the memory hierarchy includes the off-processor
memory of other processors, in addition to the hierarchy of registers,
cache, and local memory on each processor.) The fundamental building
blocks of the ScaLAPACK library are distributed memory versions (PBLAS)
of the Level 1, 2 and 3 BLAS, and a set of Basic Linear Algebra
Communication Subprograms (BLACS) for communication tasks that arise
frequently in parallel linear algebra computations. In the ScaLAPACK
routines, all interprocessor communication occurs within the PBLAS and the
BLACS. One of the design goals of ScaLAPACK was to have the ScaLAPACK
routines resemble their LAPACK equivalents as much as possible.

This package contains ScaLAPACK	libraries compiled with	mpich2.

%package mpich2-devel
Summary: Development libraries for ScaLAPACK (mpich2)
Group: Development/Libraries
Requires: %{name}-mpich2 = %{version}-%{release}
Provides: %{name}-lam-devel = %{version}-%{release}
Obsoletes: %{name}-lam-devel <= 1.7.5-7

%description mpich2-devel
This package contains development libraries for ScaLAPACK, compiled against mpich2.

%package mpich2-static
Summary: Static libraries for ScaLAPACK (mpich2)
Group: Development/Libraries
Provides: %{name}-lam-static = %{version}-%{release}
Obsoletes: %{name}-lam-static <= 1.7.5-7
Requires: %{name}-mpich2-devel = %{version}-%{release}

%description mpich2-static
This package contains static libraries for ScaLAPACK, compiled against mpich2.

%package openmpi
Summary: ScaLAPACK libraries compiled against openmpi
Group: Development/Libraries
Requires: %{name}-common = %{version}-%{release}
Requires: environment-modules

%description openmpi
The ScaLAPACK (or Scalable LAPACK) library includes a subset
of LAPACK routines redesigned for distributed memory MIMD
parallel computers. It is currently written in a
Single-Program-Multiple-Data style using explicit message
passing for interprocessor communication. It assumes
matrices are laid out in a two-dimensional block cyclic
decomposition.

ScaLAPACK is designed for heterogeneous computing and is
portable on any computer that supports MPI or PVM.

Like LAPACK, the ScaLAPACK routines are based on
block-partitioned algorithms in order to minimize the frequency
of data movement between different levels of the memory hierarchy.
(For such machines, the memory hierarchy includes the off-processor
memory of other processors, in addition to the hierarchy of registers,
cache, and local memory on each processor.) The fundamental building
blocks of the ScaLAPACK library are distributed memory versions (PBLAS)
of the Level 1, 2 and 3 BLAS, and a set of Basic Linear Algebra
Communication Subprograms (BLACS) for communication tasks that arise
frequently in parallel linear algebra computations. In the ScaLAPACK
routines, all interprocessor communication occurs within the PBLAS and the
BLACS. One of the design goals of ScaLAPACK was to have the ScaLAPACK
routines resemble their LAPACK equivalents as much as possible.

This package contains ScaLAPACK	libraries compiled with	openmpi.

%package openmpi-devel
Summary: Development libraries for ScaLAPACK (openmpi)
Group: Development/Libraries
Requires: %{name}-openmpi = %{version}-%{release}

%description openmpi-devel
This package contains development libraries for ScaLAPACK, compiled against openmpi.

%package openmpi-static
Summary: Static libraries for ScaLAPACK (openmpi)
Group: Development/Libraries
Requires: %{name}-openmpi-devel = %{version}-%{release}

%description openmpi-static
This package contains static libraries for ScaLAPACK, compiled against openmpi.

%prep
%setup -q -c -n %{name}-%{version}
%patch0 -p1
cd %{name}-%{version}/
sed -i 's!BLACSdir      =.*!BLACSdir      = %{_libdir}!' SLmake.inc
cd ..
for i in mpich2 openmpi; do
  cp -a %{name}-%{version} %{name}-%{version}-$i
  sed -i "s|FOO|$i|g" %{name}-%{version}-$i/SLmake.inc
done

%build
%define dobuild() \
cd %{name}-%{version}-$MPI_COMPILER_NAME ; \
make lib ; \
cd ..

# Build mpich2 version
export MPI_COMPILER_NAME=mpich2
%{_mpich2_load}
%{_blacs_mpich2_load}
RPM_OPT_FLAGS=`echo $CFLAGS`
%dobuild
%{_blacs_mpich2_unload}
%{_mpich2_unload}

# Build OpenMPI version
export MPI_COMPILER_NAME=openmpi
%{_openmpi_load}
%{_blacs_openmpi_load}
RPM_OPT_FLAGS=`echo $CFLAGS`
%dobuild
%{_blacs_openmpi_unload}
%{_openmpi_unload}

%install
rm -fr ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}

for i in mpich2 openmpi; do
  mkdir -p %{buildroot}%{_libdir}/scalapack-$i/
  pushd %{name}-%{version}-$i
  for f in *.a *.so*; do
    cp -f $f %{buildroot}%{_libdir}/scalapack-$i/$f
  done
  popd
  pushd %{buildroot}%{_libdir}/scalapack-$i/
  ln -fs libscalapack.so.1.0.0 libscalapack.so.1
  ln -s libscalapack.so.1.0.0 libscalapack.so
  popd
# Generate environment module file
mkdir -p %{buildroot}%{_datadir}/Modules/modulefiles/
cat << EOF > %{buildroot}%{_datadir}/Modules/modulefiles/scalapack-$i-%{_arch}
#%Module 1.0
#
#  Blacs libraries compiled with $i support
#
prepend-path            LD_LIBRARY_PATH         %{_libdir}/scalapack-$i
setenv                  LDFLAGS                 -L%{_libdir}/scalapack-$i
EOF
done

# Copy docs
cd %{name}-%{version}
cp -f INSTALL/scalapack_install.ps ../
cp -f README ../

#cp -f TESTING/x* ${RPM_BUILD_ROOT}%{_bindir}

%clean
rm -fr ${RPM_BUILD_ROOT}

%files common
%defattr(-,root,root,-)
%doc scalapack_install.ps README
# %{_bindir}/x*

%files mpich2
%defattr(-,root,root,-)
%dir %{_libdir}/scalapack-mpich2/
%{_datadir}/Modules/modulefiles/scalapack-mpich2-%{_arch}
%{_libdir}/scalapack-mpich2/libscalapack.so.*

%files mpich2-devel
%defattr(-,root,root,-)
%{_libdir}/scalapack-mpich2/libscalapack.so

%files mpich2-static
%defattr(-,root,root,-)
%{_libdir}/scalapack-mpich2/libscalapack.a

%files openmpi
%defattr(-,root,root,-)
%dir %{_libdir}/scalapack-openmpi/
%{_datadir}/Modules/modulefiles/scalapack-openmpi-%{_arch}
%{_libdir}/scalapack-openmpi/libscalapack.so.*

%files openmpi-devel
%defattr(-,root,root,-)
%{_libdir}/scalapack-openmpi/libscalapack.so

%files openmpi-static
%defattr(-,root,root,-)
%{_libdir}/scalapack-openmpi/libscalapack.a

%changelog
* Wed Jul  7 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.7.5-10
- Move all BuildRequires to the top of the spec file
- -static packages now Require matching -devel package, they're not very useful otherwise

* Wed Dec 15 2009 Deji Akingunola <dakingun@gmail.com> - 1.7.5-9
- Buildrequire mpich2-devel-static

* Wed Dec  9 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.7.5-8
- drop lam support (Provides/Obsoletes by mpich2, which is a hack, but something's gotta do it)
- move static libs to static subpackages (resolves bz 545150)

* Thu Aug  6 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.7.5-7
- rework package to handle all supported MPI environments in Fedora

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Sep 23 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.7.5-4
- incorporate Deji Akingunola's changes (bz 462424)
- build against openmpi instead of lam

* Tue Jul  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.7.5-3
- fix compile against new lam paths

* Wed Feb 13 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.7.5-2
- rebuild for new gcc

* Mon Aug 27 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.7.5-1.1
- rebuild for BuildID

* Thu Jan 18 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.7.5-1
- bump to 1.7.5

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.7.4-4
- I said "BR" not "R". Stupid packager.

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.7.4-3
- fix BR: lam-devel

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.7.4-2
- fix 64bit patch

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.7.4-1
- bump to 1.7.4

* Wed Mar  8 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-13
- lam moved into _libdir/lam... need to fix patches

* Wed Mar  8 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-12
- set -fPIC as NOOPT

* Sun Feb 26 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-11
- fix 64 bit builds
- enable shared libraries
- split package into base and devel

* Tue Feb 14 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-10
- Incorporate Andrew Gormanly's fixes

* Mon Jan  9 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-9
- fix BR

* Mon Dec 19 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-8
- rebuild for gcc4.1

* Sun May 15 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-7
- 64 bit library fix

* Mon May  9 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-6
- remove hardcoded dist tags

* Sun May  8 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-4
- fix broken patch for fc-3 branch

* Sun Apr 24 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-3
- use dist tag
- fix fc3 BuildRequires

* Tue Apr 19 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-2
- fix buildroot
- add gcc-gfortran to BuildRequires (gcc-g77 for fc3)

* Mon Apr 18 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-1
- initial package creation

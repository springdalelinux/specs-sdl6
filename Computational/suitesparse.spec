Name:           suitesparse
Version:        3.4.0
Release:        2%{?dist}
Summary:        A collection of sparse matrix libraries

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.cise.ufl.edu/research/sparse/SuiteSparse
Source0:        http://www.cise.ufl.edu/research/sparse/SuiteSparse/SuiteSparse-%{version}.tar.gz
Patch0:         suitesparse_build.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  atlas-devel
%ifarch %{ix86} x86_64 ia64
BuildRequires:  tbb-devel
%endif
Obsoletes:      umfpack <= 5.0.1
Obsoletes:      ufsparse <= 2.1.1
Provides:       ufsparse = %{version}-%{release}

%description
suitesparse is a collection of libraries for computations involving sparse
matrices.  The package includes the following libraries:
  AMD         approximate minimum degree ordering
  BTF         permutation to block triangular form (beta)
  CAMD        constrained approximate minimum degree ordering
  COLAMD      column approximate minimum degree ordering
  CCOLAMD     constrained column approximate minimum degree ordering
  CHOLMOD     sparse Cholesky factorization
  CSparse     a concise sparse matrix package
  CXSparse    CSparse extended: complex matrix, int and long int support
  KLU         sparse LU factorization, primarily for circuit simulation
  LDL         a simple LDL' factorization
  SQPR        a multithread, multifrontal, rank-revealing sparse QR
              factorization method
  UMFPACK     sparse LU factorization
  UFconfig    configuration file for all the above packages.


%package devel
Summary:        Development headers for SuiteSparse
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Obsoletes:      umfpack-devel <= 5.0.1
Obsoletes:      ufsparse-devel <= 2.1.1
Provides:       ufsparse-devel = %{version}-%{release}

%description devel
The suitesparse-devel package contains files needed for developing
applications which use the suitesparse libraries.


%package static
Summary:        Static version of SuiteSparse libraries
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}
Provides:       ufsparse-static = %{version}-%{release}

%description static
The suitesparse-static package contains the statically linkable
version of the suitesparse libraries.

%package doc
Summary:        Documentation files for SuiteSparse
Group:          Documentation
BuildArch:      noarch

Requires:       %{name} = %{version}-%{release}

%description doc
This package contains documentation files for %{name}.


%prep
%setup -q -n SuiteSparse
%patch0 -p0 -b .build

%build
%define amd_version 2.2.0
%define amd_version_major 2
%define btf_version 1.1.0
%define btf_version_major 1
%define camd_version 2.2.0
%define camd_version_major 2
%define ccolamd_version 2.7.1
%define ccolamd_version_major 2
%define cholmod_version 1.7.1
%define cholmod_version_major 1
%define colamd_version 2.7.1
%define colamd_version_major 2
%define csparse_version 2.2.3
%define csparse_version_major 2
%define cxsparse_version 2.2.3
%define cxsparse_version_major 2
%define klu_version 1.1.0
%define klu_version_major 1
%define ldl_version 2.0.1
%define ldl_version_major 2
%define umfpack_version 5.4.0
%define umfpack_version_major 5
%define spqr_version 1.1.2
%define spqr_version_major 1
### CHOLMOD can also be compiled to use the METIS library, but it is not
### used here because its licensing terms exclude it from Fedora Extras.
### To compile with METIS, define enable_metis as 1 below.
%define enable_metis 0
### CXSparse is a superset of CSparse, and the two share common header
### names, so it does not make sense to build both. CXSparse is built
### by default, but CSparse can be built instead by defining
### enable_csparse as 1 below.
%define enable_csparse 0

mkdir -p Doc/{AMD,BTF,CAMD,CCOLAMD,CHOLMOD,COLAMD,KLU,LDL,UMFPACK,SPQR} Lib Include

pushd AMD
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS -fPIC"
  popd
  pushd ../Lib
    gcc -shared -Wl,-soname,libamd.so.%{amd_version_major} -o \
        libamd.so.%{amd_version} ../AMD/Lib/*.o -lm
    ln -sf libamd.so.%{amd_version} libamd.so.%{amd_version_major}
    ln -sf libamd.so.%{amd_version} libamd.so
    cp -p ../AMD/Lib/*.a ./
  popd
  cp -p Include/*.h ../Include
  cp -p README.txt Doc/License Doc/ChangeLog Doc/*.pdf ../Doc/AMD
popd

pushd BTF
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS -fPIC"
  popd
  pushd ../Lib
    gcc -shared -Wl,-soname,libbtf.so.%{btf_version_major} -o \
        libbtf.so.%{btf_version} ../BTF/Lib/*.o
    ln -sf libbtf.so.%{btf_version} libbtf.so.%{btf_version_major}
    ln -sf libbtf.so.%{btf_version} libbtf.so
    cp -p ../BTF/Lib/*.a ./
  popd
  cp -p Include/*.h ../Include
  cp -p README.txt Doc/* ../Doc/BTF
popd

pushd CAMD
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS -fPIC" 
  popd
  pushd ../Lib
    gcc -shared -Wl,-soname,libcamd.so.%{camd_version_major} -o \
        libcamd.so.%{camd_version} ../CAMD/Lib/*.o -lm
    ln -sf libcamd.so.%{camd_version} libcamd.so.%{camd_version_major}
    ln -sf libcamd.so.%{camd_version} libcamd.so
    cp -p ../CAMD/Lib/*.a ./
  popd
  cp -p Include/*.h ../Include
  cp -p README.txt Doc/ChangeLog Doc/License Doc/*.pdf ../Doc/CAMD
popd

pushd CCOLAMD
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS -fPIC" 
  popd
  pushd ../Lib
    gcc -shared -Wl,-soname,libccolamd.so.%{ccolamd_version_major} -o \
        libccolamd.so.%{ccolamd_version} ../CCOLAMD/Lib/*.o -lm
    ln -sf libccolamd.so.%{ccolamd_version} libccolamd.so.%{ccolamd_version_major}
    ln -sf libccolamd.so.%{ccolamd_version} libccolamd.so
    cp -p ../CCOLAMD/Lib/*.a ./
  popd
  cp -p Include/*.h ../Include
  cp -p README.txt Doc/* ../Doc/CCOLAMD
popd

pushd COLAMD
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS -fPIC"
  popd
  pushd ../Lib
    gcc -shared -Wl,-soname,libcolamd.so.%{colamd_version_major} -o \
        libcolamd.so.%{colamd_version} ../COLAMD/Lib/*.o -lm
    ln -sf libcolamd.so.%{colamd_version} libcolamd.so.%{colamd_version_major}
    ln -sf libcolamd.so.%{colamd_version} libcolamd.so
    cp -p ../COLAMD/Lib/*.a ./
  popd
  cp -p Include/*.h ../Include
  cp -p README.txt Doc/* ../Doc/COLAMD
popd

%if "%{?enable_metis}" == "1"
CHOLMOD_FLAGS="$RPM_OPT_FLAGS -I%{_includedir}/metis -fPIC"
%else
CHOLMOD_FLAGS="$RPM_OPT_FLAGS -DNPARTITION -fPIC"
%endif
pushd CHOLMOD
  pushd Lib
    make CFLAGS="$CHOLMOD_FLAGS"
  popd
  pushd ../Lib
    gcc -shared -Wl,-soname,libcholmod.so.%{cholmod_version_major} -o \
        libcholmod.so.%{cholmod_version} ../CHOLMOD/Lib/*.o \
        -L%{_libdir}/atlas -lcblas -llapack libamd.so.%{amd_version_major} \
        libcamd.so.%{camd_version_major} libcolamd.so.%{colamd_version_major} \
        libccolamd.so.%{ccolamd_version_major} -lm
    ln -sf libcholmod.so.%{cholmod_version} libcholmod.so.%{cholmod_version_major}
    ln -sf libcholmod.so.%{cholmod_version} libcholmod.so
    cp -p ../CHOLMOD/Lib/*.a ./
  popd
  cp -p Include/*.h ../Include
  cp -p README.txt Doc/*.pdf ../Doc/CHOLMOD
  cp -p Cholesky/License.txt ../Doc/CHOLMOD/Cholesky_License.txt
  cp -p Core/License.txt ../Doc/CHOLMOD/Core_License.txt
  cp -p MatrixOps/License.txt ../Doc/CHOLMOD/MatrixOps_License.txt
  cp -p Partition/License.txt ../Doc/CHOLMOD/Partition_License.txt
  cp -p Supernodal/License.txt ../Doc/CHOLMOD/Supernodal_License.txt
popd

%if "%{?enable_csparse}" == "1"
pushd CSparse
  pushd Source
    make CFLAGS="$RPM_OPT_FLAGS -fPIC"
    cp -p cs.h ../../Include
  popd
  pushd ../Lib
    gcc -shared -Wl,-soname,libcsparse.so.%{csparse_version_major} -o \
        libcsparse.so.%{csparse_version} ../CSparse/Source/*.o -lm
    ln -sf libcsparse.so.%{csparse_version} libcsparse.so.%{csparse_version_major}
    ln -sf libcsparse.so.%{csparse_version} libcsparse.so
    cp -p ../CSparse/Source/*.a ./
  popd
  mkdir ../Doc/CSparse/
  cp -p Doc/* ../Doc/CSparse
popd

%else
pushd CXSparse
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS -fPIC"
  popd
  pushd ../Lib
    gcc -shared -Wl,-soname,libcxsparse.so.%{cxsparse_version_major} -o \
        libcxsparse.so.%{cxsparse_version} ../CXSparse/Lib/*.o -lm
    ln -sf libcxsparse.so.%{cxsparse_version} libcxsparse.so.%{cxsparse_version_major}
    ln -sf libcxsparse.so.%{cxsparse_version} libcxsparse.so
    cp -p ../CXSparse/Lib/*.a ./
  popd
  cp -p Include/cs.h ../Include
  mkdir ../Doc/CXSparse/
  cp -p Doc/* ../Doc/CXSparse
popd
%endif

pushd KLU
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS -fPIC"
  popd
  pushd ../Lib
    gcc -shared -Wl,-soname,libklu.so.%{klu_version_major} -o \
        libklu.so.%{klu_version} ../KLU/Lib/*.o \
        libamd.so.%{amd_version_major} libcolamd.so.%{colamd_version_major} \
        libbtf.so.%{btf_version_major} libcholmod.so.%{cholmod_version_major}
    ln -sf libklu.so.%{klu_version} libklu.so.%{klu_version_major}
    ln -sf libklu.so.%{klu_version} libklu.so
    cp -p ../KLU/Lib/*.a ./
  popd
  cp -p Include/*.h ../Include
  cp -p README.txt Doc/lesser.txt ../Doc/KLU
popd

pushd LDL
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS -fPIC"
  popd
  pushd ../Lib
    gcc -shared -Wl,-soname,libldl.so.%{ldl_version_major} -o \
        libldl.so.%{ldl_version} ../LDL/Lib/*.o
    ln -sf libldl.so.%{ldl_version} libldl.so.%{ldl_version_major}
    ln -sf libldl.so.%{ldl_version} libldl.so
    cp -p ../LDL/Lib/*.a ./
  popd
  cp -p Include/*.h ../Include
  cp -p README.txt Doc/ChangeLog Doc/lesser.txt Doc/*.pdf ../Doc/LDL
popd

pushd UMFPACK
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS -fPIC" 
  popd
  pushd ../Lib
    gcc -shared -Wl,-soname,libumfpack.so.%{umfpack_version_major} -o \
        libumfpack.so.%{umfpack_version} ../UMFPACK/Lib/*.o \
        -L%{_libdir}/atlas -lcblas -llapack libamd.so.%{amd_version_major} -lm
    ln -sf libumfpack.so.%{umfpack_version} libumfpack.so.%{umfpack_version_major}
    ln -sf libumfpack.so.%{umfpack_version} libumfpack.so
    cp -p ../UMFPACK/Lib/*.a ./
  popd
  cp -p Include/*.h ../Include
  cp -p README.txt Doc/License Doc/ChangeLog Doc/gpl.txt Doc/*.pdf ../Doc/UMFPACK
popd

pushd SPQR
  pushd Lib
%ifarch %{ix86} x86_64 ia64
    make CFLAGS="$RPM_OPT_FLAGS -DHAVE_TBB -DNPARTITION -fPIC"
%else
    make CFLAGS="$RPM_OPT_FLAGS -DNPARTITION -fPIC"
%endif
  popd
  pushd ../Lib
    g++ -shared -Wl,-soname,libspqr.so.%{spqr_version_major} -o \
        libspqr.so.%{spqr_version} ../SPQR/Lib/*.o \
        -L%{_libdir}/atlas -lcblas -llapack \
        libcholmod.so.%{cholmod_version_major} -lm
    ln -sf libspqr.so.%{spqr_version} libspqr.so.%{spqr_version_major}
    ln -sf libspqr.so.%{spqr_version} libspqr.so
    cp -p ../SPQR/Lib/*.a ./
  popd
  cp -p Include/*.h* ../Include
  cp -p README{,_SPQR}.txt
  cp -p README_SPQR.txt Doc/* ../Doc/SPQR
popd

cp -p UFconfig/UFconfig.h Include

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}/%{name}
pushd Lib
  for f in *.a *.so*; do
    cp -a $f ${RPM_BUILD_ROOT}%{_libdir}/$f
  done
popd
pushd Include
  for f in *.h;  do
    cp -a $f ${RPM_BUILD_ROOT}%{_includedir}/%{name}/$f
  done
popd


%clean
rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}
%{_libdir}/lib*.so

%files static
%defattr(-,root,root)
%{_libdir}/lib*.a

%files doc
%defattr(-,root,root)
%doc Doc/*

%changelog
* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 27 2009 Deji Akingunola <dakingun@gmail.com> - 3.4.0-1
- Update to version 3.4.0.

* Tue May 19 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 3.3.0-2
- Split documentation into separate -doc subpackage (resolves BZ#492451).

* Mon Apr 27 2009 Deji Akingunola <dakingun@gmail.com> - 3.3.0-1
- Update to release 3.3.0.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 16 2009 Deji Akingunola <dakingun@gmail.com> - 3.2.0-5
- More fixes for the undefined symbol issue (BZ #475411)

* Sat Dec 20 2008 Deji Akingunola <dakingun@gmail.com> - 3.2.0-4
- Also build SPQR
- Further fixes for BZ #475411

* Wed Dec 17 2008 Deji Akingunola <dakingun@gmail.com> - 3.2.0-3
- Rearrange the spec
- Link in necessary libs when making shared CHOLMOD lib (BZ #475411)
- Link with ATLAS' blas and lapack libs

* Wed Dec 17 2008 Deji Akingunola <dakingun@gmail.com> - 3.2.0-2
- Rebuild for updated atlas

* Mon Dec 15 2008 Deji Akingunola <dakingun@gmail.com> - 3.2.0-1
- New upstream version

* Mon Mar  3 2008 Quentin Spencer <qspencer@users.sourceforge.net> 3.1.0-1
- Update to release 3.1.0. 

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.0.0-4
- Autorebuild for GCC 4.3

* Tue Oct 16 2007 Quentin Spencer <qspencer@users.sourceforge.net> 3.0.0-3
- Update license tag. Fix minor issues found by rpmlint.

* Fri Aug 24 2007 Quentin Spencer <qspencer@users.sourceforge.net> 3.0.0-2
- Rebuild for F8.

* Tue Jul  3 2007 Quentin Spencer <qspencer@users.sourceforge.net> 3.0.0-1
- Change package name to match upstream, including provides and obsoletes.
- New release. Numerous changes in build to reflect source reorganization.
- Moved static libs into separate package.

* Mon Oct 16 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.1.1-1
- New release, and package name change from UFsparse to SuiteSparse. Fixes
  bug #210846. Keep the ufsparse package name for now.

* Thu Sep  7 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.1.0-1
- New release. Increment versions of some libraries.
- Rearrange and clean up spec file so all definitions are in one place.

* Mon Aug  7 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.0.0-1
- New release.
- Build newly added CAMD library.
- Misc minor spec changes.

* Tue Mar  7 2006 Quentin Spencer <qspencer@users.sourceforge.net> 1.2-1
- New release.
- Build newly added library CXSparse (but not CSparse--see comments
  in build section).

* Wed Feb 15 2006 Quentin Spencer <qspencer@users.sourceforge.net> 0.93-2
- Rebuild for Fedora Extras 5.

* Thu Feb  9 2006 Quentin Spencer <qspencer@users.sourceforge.net> 0.93-1
- New release. Remove old patch.

* Wed Dec 14 2005 Quentin Spencer <qspencer@users.sourceforge.net> 0.92-2
- Add patch0--fixes LDL/Makefile so CFLAGS are used when compiling ldl.a.

* Wed Dec 14 2005 Quentin Spencer <qspencer@users.sourceforge.net> 0.92-1
- Update to Dec 8 2005 version.

* Tue Oct 25 2005 Quentin Spencer <qspencer@users.sourceforge.net> 0.91-2
- Rebuild.

* Tue Oct 18 2005 Quentin Spencer <qspencer@users.sourceforge.net> 0.91-1
- New upstream release, incorporating previous patches
- chmod the build directory to ensure all headers are world readable

* Fri Oct 07 2005 Quentin Spencer <qspencer@users.sourceforge.net> 0.9-3
- Build cholmod, but disable METIS using -DNPARTITION flag.

* Sat Oct 01 2005 Quentin Spencer <qspencer@users.sourceforge.net> 0.9-2
- Modify description, other modifications for import into FE.
- Add dist tag, cosmetic changes.

* Tue Sep 08 2005 David Bateman <dbateman@free.fr> 0.9-1
- First version.

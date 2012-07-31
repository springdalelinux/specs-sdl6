Summary: Basic Linear Algebra Communication Subprograms
Name: blacs
Version: 1.1
Release: 39%{?dist}.1
License: Public Domain
Group: Development/Libraries
URL: http://www.netlib.org/blacs
Source0: http://www.netlib.org/blacs/mpiblacs.tgz
Source1: Bmake.inc
Source2: http://www.netlib.org/blacs/mpi_prop.ps
Source3: http://www.netlib.org/blacs/blacs_install.ps
Source4: http://www.netlib.org/blacs/mpiblacs_issues.ps
Source5: http://www.netlib.org/blacs/f77blacsqref.ps
Source6: http://www.netlib.org/blacs/cblacsqref.ps
Source7: http://www.netlib.org/blacs/lawn94.ps
BuildRequires: gcc-gfortran
BuildRequires: lapack, blas
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch0: blacs-fedora.patch

%description
The BLACS (Basic Linear Algebra Communication Subprograms) project is 
an ongoing investigation whose purpose is to create a linear algebra 
oriented message passing interface that may be implemented efficiently 
and uniformly across a large range of distributed memory platforms.

The length of time required to implement efficient distributed memory 
algorithms makes it impractical to rewrite programs for every new 
parallel machine. The BLACS exist in order to make linear algebra 
applications both easier to program and more portable. 

%package common
Summary: Common files for blacs
Group: Development/Libraries
Requires: lapack, blas

%description common
The BLACS (Basic Linear Algebra Communication Subprograms) project is
an ongoing investigation whose purpose is to create a linear algebra
oriented message passing interface that may be implemented efficiently
and uniformly across a large range of distributed memory platforms.

The length of time required to implement efficient distributed memory
algorithms makes it impractical to rewrite programs for every new
parallel machine. The BLACS exist in order to make linear algebra
applications both easier to program and more portable.

This file contains common files which are not specific to any MPI implementation.

%package mpich2
Summary: BLACS libraries compiled against mpich2
Group: Development/Libraries
BuildRequires: mpich2-devel-static
Requires: %{name}-common = %{version}-%{release}
Requires: environment-modules
# This is a dirty lie, but something needs to reap these dead subpackages.
Provides: blacs-lam = %{version}-%{release}
Obsoletes: blacs-lam < 1.1-34

%description mpich2
The BLACS (Basic Linear Algebra Communication Subprograms) project is
an ongoing investigation whose purpose is to create a linear algebra
oriented message passing interface that may be implemented efficiently
and uniformly across a large range of distributed memory platforms.

The length of time required to implement efficient distributed memory
algorithms makes it impractical to rewrite programs for every new
parallel machine. The BLACS exist in order to make linear algebra
applications both easier to program and more portable.

This package contains BLACS libraries compiled with mpich2.

%package mpich2-devel
Summary: Development libraries for blacs (mpich2)
Group: Development/Libraries
Requires: %{name}-mpich2 = %{version}-%{release}
# This is a dirty lie, but something needs to reap these dead subpackages.
Provides: blacs-lam-devel = %{version}-%{release}
Obsoletes: blacs-lam-devel < 1.1-34

%description mpich2-devel
This package contains development libraries for blacs, compiled against mpich2.

%package mpich2-static
Summary: Static libraries for blacs (mpich2)
Group: Development/Libraries

%description mpich2-static
This package contains static libraries for blacs, compiled against mpich2.

%package openmpi
Summary: BLACS libraries compiled against openmpi
Group: Development/Libraries
Requires: %{name}-common = %{version}-%{release}
Requires: environment-modules

%description openmpi
The BLACS (Basic Linear Algebra Communication Subprograms) project is
an ongoing investigation whose purpose is to create a linear algebra
oriented message passing interface that may be implemented efficiently
and uniformly across a large range of distributed memory platforms.

The length of time required to implement efficient distributed memory
algorithms makes it impractical to rewrite programs for every new
parallel machine. The BLACS exist in order to make linear algebra
applications both easier to program and more portable.

This package contains BLACS libraries compiled with openmpi.

%package openmpi-devel
Summary: Development libraries for blacs (openmpi)
Group: Development/Libraries
BuildRequires: openmpi-devel
Requires: %{name}-openmpi = %{version}-%{release}

%description openmpi-devel
This package contains development libraries for blacs, compiled	against openmpi.

%package openmpi-static
Summary: Static libraries for blacs (openmpi)
Group: Development/Libraries

%description openmpi-static
This package contains static libraries for blacs, compiled against openmpi.

%prep
%setup -q -c -n %{name}
%patch0 -p1
for i in mpich2 openmpi; do
	cp -ap BLACS BLACS-$i
	cp -fp %{SOURCE1} BLACS-$i/
	sed -i "s|FOO|$i|g" BLACS-$i/Bmake.inc
done

# openmpi doesn't use TRANSCOMM = -DUseMpich
sed -i "s|-DUseMpich||g" BLACS-openmpi/Bmake.inc

# copy in docs:
cp -p %{SOURCE2} mpi_prop.ps
cp -p %{SOURCE3} blacs_install.ps
cp -p %{SOURCE4} mpiblacs_issues.ps
cp -p %{SOURCE5} f77blacsqref.ps
cp -p %{SOURCE6} cblacsqref.ps
cp -p %{SOURCE7} lawn94.ps

%build
# CFLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-fstack-protector//g'`
# RPM_OPT_FLAGS=`echo $CFLAGS`

# To avoid replicated code define a build macro
%define dobuild() \
cd BLACS-$MPI_COMPILER_NAME; \
make mpi ; \
cd ..

# Build mpich2 version
export MPI_COMPILER_NAME=mpich2
%{_mpich2_load}
RPM_OPT_FLAGS=`echo $CFLAGS`
%dobuild
%{_mpich2_unload}

# Build OpenMPI version
export MPI_COMPILER_NAME=openmpi
%{_openmpi_load}
RPM_OPT_FLAGS=`echo $CFLAGS`
%dobuild
%{_openmpi_unload}

# cd TESTING/
# make
# cd ../..

%install
# mkdir -p ${RPM_BUILD_ROOT}%{_bindir}

for i in mpich2 openmpi; do 
  mkdir -p %{buildroot}%{_libdir}/$i/lib/
  mkdir -p %{buildroot}%{_includedir}/$i-%{_arch}/
  mkdir -p %{buildroot}%{_includedir}/blacs/
  pushd BLACS-$i/LIB
  for f in *.a *.so*; do
    cp -f $f %{buildroot}%{_libdir}/$i/lib/$f
  done
  popd
  # This file is independent of the MPI compiler used, but it is poorly named
  # So we'll put it in %{_includedir}/blacs/
  install -p BLACS-$i/SRC/MPI/Bdef.h %{buildroot}%{_includedir}/blacs/
  pushd %{buildroot}%{_libdir}/$i/lib/
  for l in libmpiblacs libmpiblacsF77init libmpiblacsCinit; do
    ln -fs $l.so.1.0.0 $l.so.1
    ln -s $l.so.1.0.0 $l.so
  done
  popd
done

# cd ../TESTING/EXE
# cp -f x*test_MPI-LINUX-0 ${RPM_BUILD_ROOT}%{_bindir}

%clean
rm -fr ${RPM_BUILD_ROOT}

%files common
%defattr(-,root,root,0755)
%doc mpi_prop.ps blacs_install.ps mpiblacs_issues.ps f77blacsqref.ps cblacsqref.ps lawn94.ps
%{_includedir}/blacs/
# %{_bindir}/x*test_MPI-LINUX-0

%files mpich2
%defattr(-,root,root,0755)
%{_libdir}/mpich2/lib/*.so.*

%files mpich2-devel
%defattr(-,root,root,0755)
%{_includedir}/mpich2-%{_arch}/
%{_libdir}/mpich2/lib/*.so

%files mpich2-static
%defattr(-,root,root,0755)
%{_libdir}/mpich2/lib/*.a

%files openmpi
%defattr(-,root,root,0755)
%{_libdir}/openmpi/lib/*.so.*

%files openmpi-devel
%defattr(-,root,root,0755)
%{_includedir}/openmpi-%{_arch}/
%{_libdir}/openmpi/lib/*.so

%files openmpi-static
%defattr(-,root,root,0755)
%{_libdir}/openmpi/lib/*.a

%changelog
* Sat Apr 17 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1-39.1
- f12 still needs provides/obsoletes for old lam ghosts

* Tue Apr 13 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1-39
- openmpi doesn't use TRANSCOMM	= -DUseMpich
- put libraries in $MPI_LIB, not $MPI_HOME

* Wed Feb 24 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1-38
- get rid of environment module files altogether (the openmpi/mpich2 env modules are sufficient)

* Fri Feb 19 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1-37
- fix environment module files

* Tue Feb 16 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1-36
- put libraries in appropriate locations
- put include files in appropriate locations
- put environment module files in appropriate location
- use -p with every cp invocation
- drop Provides/Obsoletes for blacs-lam-*

* Thu Dec 10 2009 Deji Akingunola <dakingun@gmail.com> - 1.1-35
- Buildrequire mpich2-devel-static
- Adjust obsolete versioning

* Mon Dec  7 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1-34
- drop lam subpackages (fixes FTBFS, 539057)
- blacs-mpich2-* now Provides/Obsoletes blacs-lam-*, this is a dirty lie, but we need something to do it
- move static bits to -static subpackages (resolves 545142)
- package up Bdef.h for other dependent packages to use (resolves 533929, thanks to Deji Akingunola)

* Thu Aug  6 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1-33
- rework package to handle all supported MPI environments in Fedora

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Sep 23 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1-30
- incorporate Deji Akingunola's changes
- use openmpi rather than lam

* Tue Jul  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1-29
- fix lam paths

* Tue Jul  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1-28
- rebuild

* Tue May 13 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1-27
- ia64 doesn't use /usr/lib64

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1-26.1
- Autorebuild for GCC 4.3

* Thu Aug 23 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-25.1
- fix shared patch in devel

* Thu Aug 23 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-25
- rebuild for BuildID

* Wed Dec 20 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-24.1
- updated bmake files to include new lam-devel header path

* Mon Sep 11 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-24
- FC-5+ needs lam-devel as a BR

* Mon Sep 11 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-23
- bump for FC-6

* Fri Apr  7 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-22
- FC-5+ also needs -L libdir/lam

* Fri Apr  7 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-21
- FC-5+ needs includedir/lam

* Fri Apr  7 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-20
- fix lam BR

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-19
- fix broken bits in shared lib (no -fstack-protector for us)

* Mon Dec 19 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-18
- rebuild for gcc4.1

* Sun Jul 31 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-17
- fix g77 for FC-3 spec

* Fri Jul 29 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-16
- remove ppc hack

* Fri Jul 29 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-15
- Fix typo in fix. :/

* Fri Jul 29 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-12
- fix INTFACE for FC-4+

* Fri Jul 29 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-11
- bump for new tag

* Mon Jun 27 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-10
- split static lib and .so into -devel package
- fix Bmake files for shared library support
- build shared libraries

* Tue May 10 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-8
- g77 needs some special compile flags, edited Bmake.inc*

* Mon May  9 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-7
- remove hardcoded dist tags

* Thu May  5 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-6
- fix 64bit issues

* Sun Apr 24 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-5
- use dist tag
- fix fc3 package sources and dependencies

* Tue Apr 19 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-4
- fix buildroot
- add gcc-gfortran as a BuildRequires (gcc-g77)

* Mon Apr 18 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-3
- backout shared patch

* Mon Apr 18 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-2
- rename libs to what scalapack thinks they should be called

* Mon Apr 18 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-1
- initial package creation

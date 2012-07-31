Summary: Fortran77 subroutines for solving large scale eigenvalue problems
Name: arpack
Version: 2.1
Release: 13%{?dist}
License: BSD
Group: Development/Libraries
URL: http://www.caam.rice.edu/software/ARPACK/
Source0: http://www.caam.rice.edu/software/ARPACK/SRC/arpack96.tar.gz
Source1: http://www.caam.rice.edu/software/ARPACK/SRC/patch.tar.gz
Source2: http://www.caam.rice.edu/software/ARPACK/RiceBSD.txt
Patch0: arpack-2.1-redhat.patch
# see http://www.ann.jussieu.fr/pipermail/freefempp/2006/000213.html
Patch1: arpack-second-bug.patch
Patch2: arpack-etime.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: gcc-gfortran
BuildRequires: lapack-devel

%description
ARPACK is a collection of Fortran77 subroutines designed to solve large 
scale eigenvalue problems. 

The package is designed to compute a few eigenvalues and corresponding
eigenvectors of a general n by n matrix A. It is most appropriate for
large sparse or structured matrices A where structured means that a
matrix-vector product w <- Av requires order n rather than the usual
order n**2 floating point operations. This software is based upon an
algorithmic variant of the Arnoldi process called the Implicitly
Restarted Arnoldi Method (IRAM).

%package devel
Summary: Files needed for developing arpack based applications
Group: Development/Libraries
Requires: arpack = %{version}-%{release}

%description devel
ARPACK is a collection of Fortran77 subroutines designed to solve
large scale eigenvalue problems. This package contains the so
library links used for building arpack based applications.

%package static
Summary: Static library for developing arpack based applications
Group: Development/Libraries
Requires: arpack-devel = %{version}-%{release}

%description static
ARPACK is a collection of Fortran77 subroutines designed to solve
large scale eigenvalue problems. This package contains the static
library and so links used for building arpack based applications.

%prep
%setup -q -b 1 -n ARPACK
%patch0 -p1 -b .rh
%patch1 -p1 -b .sb
%patch2 -p1 -b .etime
mkdir static shared

%build
cd shared
for dir in ../SRC ../UTIL; do
  make -f $dir/Makefile VPATH=$dir srcdir=$dir \
       FC=gfortran FFLAGS="%{optflags} -fPIC" \
       single double complex complex16
done
gcc -shared -llapack -Wl,-soname,libarpack.so.2 -o libarpack.so.2.1 *.o
cd ..
cd static
for dir in ../SRC ../UTIL; do
  make -f $dir/Makefile VPATH=$dir srcdir=$dir \
       FC=gfortran FFLAGS="%{optflags}" LDFLAGS="-s" \
       all
done
ar rv libarpack.a *.o
ranlib libarpack.a
cd ..

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}
install -p -m644 static/libarpack.a %{buildroot}%{_libdir}
install -p -m755 shared/libarpack.so.2.1 %{buildroot}%{_libdir}
ln -s libarpack.so.2.1 %{buildroot}%{_libdir}/libarpack.so.2
ln -s libarpack.so.2 %{buildroot}%{_libdir}/libarpack.so
cp -p %{SOURCE2} .

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc RiceBSD.txt
%{_libdir}/libarpack.so.*

%files devel
%defattr(-,root,root,-)
%doc DOCUMENTS EXAMPLES
%{_libdir}/libarpack.so

%files static
%{_libdir}/libarpack.a

%changelog
* Wed Jul  7 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 2.1-13
- Get rid of build conditionals related to EPEL 3/4 for which have not been
  branched.
- Bump spec to fix update path.

* Wed Apr  7 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.1-11
- Change license to BSD (see RH bugs #234191 and #578873).

* Wed Sep 24 2008 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> 2.1-10
- fix libarpack.so: undefined reference to `etime_' with recent gfortran

* Mon Aug 25 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.1-9
- Patch0 and %%patch make recent rpm silenty fail.

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.1-8
- fix license tag

* Wed Oct 24 2007 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> 2.1-7
- apply Frederic Hecht's patch for eigenvalue bug
- move static libs to separate package

* Mon Mar 26 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.1-6
- Add license and clarification note
- Add lapack support

* Thu Nov  9 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.1-4
- Freshen up for submitting to fedora extras.
- Fix permissions of so file.
- Add forgotten ldconfig
- Remove dot from summaries.

* Wed Jul 16 2003 Axel Thimm <Axel.Thimm@ATrpms.net>
- Initial build.

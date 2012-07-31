# compiler for which we are doing this
%{!?compiler: %define compiler intel}
%{!?compilermajor: %define compilermajor 12}
%{!?compilerminor: %define compilerminor 1}
%define compilerversion %{compilermajor}.%{compilerminor}
%define compilerversionnum %{compilermajor}%{compilerminor}

# 32 or 64?
%ifarch %{ix86}
%define modulebits 32
%else
%define modulebits 64
%endif

# now, depending on the compiler we need different things - place them all here for eacy access/changing
#
# GCC Compiler
%if "%{compiler}" == "gcc"
%define compilershort gcc
%define compilerruntimesection BuildRequires: gcc-gfortran openmpi-gcc-devel >= 1.4.5 sgi-mpt >= 2.05 intel-mpi-modules-devel intel-mpi-modules-gcc
%define compilerdevelsection Requires: gcc-gfortran
%define compilerdocsection #nothing here
%define localdir /usr/local
# do nothing special for gcc for build prep
%define compilerbuildprep F77=gfortran FC=gfortran F90=gfortran;. /etc/profile.d/modules.sh
# and this is a list of conflicting modules
%define modulempt mpt
%endif
#
# Intel compiler
%if "%{compiler}" == "intel"
%define compilershort intel
%define compilerruntimesection BuildRequires: openmpi-intel%{compilerversionnum}-devel >= 1.4.5 sgi-mpt-intel%{compilerversionnum}-devel >= 2.05 intel-mpi-modules-devel intel-mpi-modules-intel \
Provides: fftw2-intel = %{version}-%{intelprovides}.%{release}
%define compilerdevelsection Provides: fftw2-intel-devel = %{version}-%{intelprovides}.%{release}
%define compilerdocsection Provides: fftw2-intel-doc = %{version}-%{intelprovides}.%{release}
%define localdir /usr/local/intel
# for intel we need to just specify our compilers
%define compilerbuildprep export LDFLAGS="-Wl,--build-id" CC=icc CXX=icpc F77=ifort FC=ifort F90=ifort; . /etc/profile.d/modules.sh
%define cflags -O3 -g -pipe -Wall
%define cxxflags %{cflags}
%define f77flags %{cflags}
%define fcflags  %{cflags}
%define modulempt mpt/intel-%{compilerversion}
%endif
#
# PGI compiler
%if "%{compiler}" == "pgi"
%define compilershort pgi
%define compilerruntimesection BuildRequires: openmpi-pgi-devel
Provides: fftw2-pgi = %{version}-070.%{release}
%define compilerdevelsection Requires: pgi-workstation70\
Provides: fftw2-pgi-devel = %{version}-070.%{release}
%define compilerdocsection Provides: fftw2-pgi-doc = %{version}-070.%{release}
%define localdir /usr/local/pgi
# for pgi we need to just specify our compilers
# we also need to force -fPIC flag to get shared libraries and other things
%define compilerbuildprep export CC=pgcc CXX=pgCC F77=pgf77 FC=pgf90 F90=pgf90 lt_cv_prog_cc_pic=-fPIC lt_cv_prog_cc_wl='-Wl,' lt_cv_prog_cc_static='-static'; . /etc/profile.d/modules.sh 
%define cflags -fast
%define cxxflags %{cflags}
%define f77flags %{cflags}
%define fcflags  %{cflags}
#define ldflags  -lpthread
%endif
#
# PGI compiler
%if "%{compiler}" == "pathscale"
%define compilershort pathscale
%define compilerruntimesection BuildRequires: openmpi-pathscale-devel
Provides: fftw2-pathscale = %{version}-070.%{release}
%define compilerdevelsection Requires: pathscale-workstation70\
Provides: fftw2-pathscale-devel = %{version}-070.%{release}
%define compilerdocsection Provides: fftw2-pathscale-doc = %{version}-070.%{release}
%define localdir /usr/local/pathscale
# for pathscale we need to just specify our compilers
# we also need to force -fPIC flag to get shared libraries and other things
%define compilerbuildprep export LDFLAGS="-Wl,--build-id" CC=pathcc CXX=pathCC F77=pathf90 FC=pathf90 F90=pathf90 lt_cv_prog_cc_pic=-fPIC lt_cv_prog_cc_wl='-Wl,' lt_cv_prog_cc_static='-static'; . /etc/profile.d/modules.sh 
%define cflags -O3
%define cxxflags %{cflags}
%define f77flags %{cflags}
%define fcflags  %{cflags}
#define ldflags  -lpthread
%endif

Name:           fftw2-%{compiler}
Version:        2.1.5
Release:        22%{?dist}
Summary:        Fast Fourier Transform library
%define 	real_name fftw

Group:          System Environment/Libraries
License:        GPL
URL:            http://www.fftw.org/
Source0:        ftp://ftp.fftw.org/pub/fftw/fftw-%{version}.tar.gz
Patch0:         rfftw_f77_mpi.c.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  rsync
%{compilerruntimesection}

%description
FFTW is a C subroutine library for computing the Discrete Fourier Transform
(DFT) in one or more dimensions, of both real and complex data, and of
arbitrary input size. We believe that FFTW, which is free software, should
become the FFT library of choice for most applications. Our benchmarks,
performed on on a variety of platforms, show that FFTW's performance is
typically superior to that of other publicly available FFT software.

This rpm was compiled with %{compiler} family of compilers.

%package        devel
Summary:        Headers, libraries and docs for the FFTW library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
FFTW is a C subroutine library for computing the Discrete Fourier Transform
(DFT) in one or more dimensions, of both real and complex data, and of
arbitrary input size. We believe that FFTW, which is free software, should
become the FFT library of choice for most applications. Our benchmarks,
performed on on a variety of platforms, show that FFTW's performance is
typically superior to that of other publicly available FFT software.

This package contains header files and development libraries needed to
develop programs using the FFTW fast Fourier transform library.

This rpm was compiled with %{compiler} family of compilers.

%package        openmpi
Summary:        Libraries for the FFTW library for openmpi
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    openmpi
FFTW is a C subroutine library for computing the Discrete Fourier Transform
(DFT) in one or more dimensions, of both real and complex data, and of
arbitrary input size. We believe that FFTW, which is free software, should
become the FFT library of choice for most applications. Our benchmarks,
performed on on a variety of platforms, show that FFTW's performance is
typically superior to that of other publicly available FFT software.

This package contains header files and development libraries needed to
develop programs using the FFTW fast Fourier transform library.

This rpm was compiled with %{compiler} family of compilers and contains
mpi related material compiled with openmpi.

%package        openmpi-devel
Summary:        Development Libraries and docs for the FFTW library for openmpi
Group:          Development/Libraries
Requires:       %{name}-openmpi = %{version}-%{release}

%description    openmpi-devel
FFTW is a C subroutine library for computing the Discrete Fourier Transform
(DFT) in one or more dimensions, of both real and complex data, and of
arbitrary input size. We believe that FFTW, which is free software, should
become the FFT library of choice for most applications. Our benchmarks,
performed on on a variety of platforms, show that FFTW's performance is
typically superior to that of other publicly available FFT software.

This package contains header files and development libraries needed to
develop programs using the FFTW fast Fourier transform library.

This rpm was compiled with %{compiler} family of compilers and contains
mpi related material compiled with openmpi necessary for development work.


%package        mpt
Summary:        Libraries for the FFTW library for mpt
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    mpt
FFTW is a C subroutine library for computing the Discrete Fourier Transform
(DFT) in one or more dimensions, of both real and complex data, and of
arbitrary input size. We believe that FFTW, which is free software, should
become the FFT library of choice for most applications. Our benchmarks,
performed on on a variety of platforms, show that FFTW's performance is
typically superior to that of other publicly available FFT software.

This package contains header files and development libraries needed to
develop programs using the FFTW fast Fourier transform library.

This rpm was compiled with %{compiler} family of compilers and contains
mpi related material compiled with mpt.

%package        mpt-devel
Summary:        Development Libraries and docs for the FFTW library for mpt
Group:          Development/Libraries
Requires:       %{name}-mpt = %{version}-%{release}

%description    mpt-devel
FFTW is a C subroutine library for computing the Discrete Fourier Transform
(DFT) in one or more dimensions, of both real and complex data, and of
arbitrary input size. We believe that FFTW, which is free software, should
become the FFT library of choice for most applications. Our benchmarks,
performed on on a variety of platforms, show that FFTW's performance is
typically superior to that of other publicly available FFT software.

This package contains header files and development libraries needed to
develop programs using the FFTW fast Fourier transform library.

This rpm was compiled with %{compiler} family of compilers and contains
mpi related material compiled with mpt necessary for development work.


%package        impi
Summary:        Libraries for the FFTW library for intel mpi
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    impi
FFTW is a C subroutine library for computing the Discrete Fourier Transform
(DFT) in one or more dimensions, of both real and complex data, and of
arbitrary input size. We believe that FFTW, which is free software, should
become the FFT library of choice for most applications. Our benchmarks,
performed on on a variety of platforms, show that FFTW's performance is
typically superior to that of other publicly available FFT software.

This package contains header files and development libraries needed to
develop programs using the FFTW fast Fourier transform library.

This rpm was compiled with %{compiler} family of compilers and contains
mpi related material compiled with intel mpi

%package        impi-devel
Summary:        Development Libraries and docs for the FFTW library for intel mpi
Group:          Development/Libraries
Requires:       %{name}-impi = %{version}-%{release}

%description    impi-devel
FFTW is a C subroutine library for computing the Discrete Fourier Transform
(DFT) in one or more dimensions, of both real and complex data, and of
arbitrary input size. We believe that FFTW, which is free software, should
become the FFT library of choice for most applications. Our benchmarks,
performed on on a variety of platforms, show that FFTW's performance is
typically superior to that of other publicly available FFT software.

This package contains header files and development libraries needed to
develop programs using the FFTW fast Fourier transform library.

This rpm was compiled with %{compiler} family of compilers and contains
mpi related material compiled with intel mpi necessary for development work.

%prep
%setup -q -c %{real_name}-%{version}
mv %{real_name}-%{version} single
cd single
%patch0 -p0
cd ..
cp -a single double

%build
build_one() {
mkdir $1
rsync -arH single double $1/
pushd $1
pushd double
	%ifarch i386
		%configure \
			--prefix=%{localdir} \
			--libdir=%{localdir}/%{_lib} \
			--includedir=%{localdir}/include \
			--infodir=%{localdir}/share/info \
			--enable-shared \
			--enable-threads \
			--enable-mpi \
			--enable-i386-hacks
	%else
		%configure \
			--prefix=%{localdir} \
			--libdir=%{localdir}/%{_lib} \
			--includedir=%{localdir}/include \
			--infodir=%{localdir}/share/info \
			--enable-shared \
			--enable-mpi \
			--enable-threads
	%endif
	make %{?_smp_mflags}
popd
pushd single
	%configure \
		--prefix=%{localdir} \
		--libdir=%{localdir}/%{_lib} \
		--includedir=%{localdir}/include \
		--infodir=%{localdir}/share/info \
		--enable-shared \
		--enable-type-prefix \
		--enable-threads \
		--enable-mpi \
		--enable-float
	make %{?_smp_mflags}
popd
popd
module purge
}

CFLAGS="%{?cflags:%{cflags}}%{!?cflags:$RPM_OPT_FLAGS}"
CXXFLAGS="%{?cxxflags:%{cxxflags}}%{!?cxxflags:$RPM_OPT_FLAGS}"
F77FLAGS="%{?f77flags:%{f77flags}}%{!?f77flags:$RPM_OPT_FLAGS}"
FFLAGS="%{?f77flags:%{f77flags}}%{!?f77flags:$RPM_OPT_FLAGS}"
FCFLAGS="%{?fcflags:%{fcflags}}%{!?fcflags:$RPM_OPT_FLAGS}"
LDFLAGS="%{?ldflags:%{ldflags}}"

export CFLAGS CXXFLAGS F77FLAGS FCFLAGS FFLAGS LDFLAGS

%{compilerbuildprep}

module load openmpi/%{compiler}
build_one openmpi

%if "%{compiler}" == "intel"
module load intel
%endif
module load %{modulempt}
build_one mpt

%if "%{compiler}" == "intel"
module load intel
%endif
module load intel-mpi/%{compiler}
build_one intel-mpi

%install
rm -rf ${RPM_BUILD_ROOT}

install_one() {
pushd $1
pushd double
	make install DESTDIR=${RPM_BUILD_ROOT}
	# we only need this once
	if [ ! -e ../../AUTHORS ]; then
		cp -a AUTHORS COPYING COPYRIGHT ChangeLog NEWS README* TODO ../../
		mkdir -p $RPM_BUILD_ROOT/%{localdir}/share/doc/fftw2
		cp -a FAQ/fftw-faq.html/ doc/ $RPM_BUILD_ROOT/%{localdir}/share/doc/fftw2/
		rm -f $RPM_BUILD_ROOT/%{localdir}/share/doc/fftw2/Makefile*
	fi
	if [ ! -e $RPM_BUILD_ROOT/%{localdir}/include/fftw_f77.i ]; then
		install -m 644 fortran/fftw_f77.i $RPM_BUILD_ROOT/%{localdir}/include/fftw_f77.i
	fi
popd
pushd single
	make install DESTDIR=${RPM_BUILD_ROOT}
popd
mkdir ${RPM_BUILD_ROOT}/%{localdir}/%{_lib}/$1
mv ${RPM_BUILD_ROOT}/%{localdir}/%{_lib}/lib*mpi* ${RPM_BUILD_ROOT}/%{localdir}/%{_lib}/$1
popd
module purge
}

%{compilerbuildprep}

module load openmpi/%{compiler}
install_one openmpi

%if "%{compiler}" == "intel"
module load intel
%endif
module load %{modulempt}
install_one mpt

%if "%{compiler}" == "intel"
module load intel
%endif
module load intel-mpi/%{compiler}
install_one intel-mpi

rm -f doc/Makefile*
find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'

## move info files under %{localdir}
#mkdir -p $RPM_BUILD_ROOT/%{localdir}/share/info
#mv  $RPM_BUILD_ROOT/%{_prefix}/share/info/fftw*info* $RPM_BUILD_ROOT/%{localdir}/share/info/

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYRIGHT ChangeLog NEWS README* TODO
%{localdir}/%{_lib}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc  %{localdir}/share/doc/fftw2
%doc  %{localdir}/share/info/*
%{localdir}/include/*.h
%{localdir}/include/*.i
%{localdir}/%{_lib}/*.a
%{localdir}/%{_lib}/*.so

%files openmpi
%defattr(-,root,root,-)
%{localdir}/%{_lib}/openmpi/*.so.*

%files openmpi-devel
%defattr(-,root,root,-)
%{localdir}/%{_lib}/openmpi/*.a
%{localdir}/%{_lib}/openmpi/*.so

%files mpt
%defattr(-,root,root,-)
%dir %{localdir}/%{_lib}/mpt
%{localdir}/%{_lib}/mpt/*.so.*

%files mpt-devel
%defattr(-,root,root,-)
%{localdir}/%{_lib}/mpt/*.a
%{localdir}/%{_lib}/mpt/*.so

%files impi
%defattr(-,root,root,-)
%dir %{localdir}/%{_lib}/intel-mpi
%{localdir}/%{_lib}/intel-mpi/*.so.*

%files impi-devel
%defattr(-,root,root,-)
%{localdir}/%{_lib}/intel-mpi/*.a
%{localdir}/%{_lib}/intel-mpi/*.so

%changelog
* Sun Apr 08 2012 Josko Plazonic <plazonic@math.princeton.edu>
- add support for intel mpi
 
* Mon Mar 12 2012 Josko Plazonic <plazonic@math.princeton.edu>
- add support for SGI's mpt

* Mon Mar 17 2008 Josko Plazonic <plazonic@math.princeton.edu>
- adapt to artemis, i.e. suse

* Tue Aug 29 2006 José Matos <jamatos[AT]fc.up.pt> - 2.1.5-13
- Rebuild for FE6

* Sat Feb 18 2006 José Matos <jamatos[AT]fc.up.pt> - 2.1.5-12
- Rebuild for FC-5.

* Wed Feb  1 2006 José Matos <jamatos[AT]fc.up.pt> - 2.1.5-11
- Fix incomplete substitution

* Wed Feb  1 2006 José Matos <jamatos[AT]fc.up.pt> - 2.1.5-10
- Add disttag to release.

* Wed Feb  1 2006 José Matos <jamatos[AT]fc.up.pt> - 2.1.5-9
- Rename package to fftw2.

* Mon May 23 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 2.1.5-8
- BuildReq gcc-gfortran (#156490).

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 2.1.5-7
- rebuild on all arches
- buildrequire compat-gcc-32-g77

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Wed Nov 10 2004 Matthias Saou <http://freshrpms.net/> 2.1.5-5
- Bump release to provide Extras upgrade path.

* Tue Apr 06 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:2.1.5-0.fdr.4
- BuildReq gcc-g77.

* Mon Sep 22 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:2.1.5-0.fdr.3
- Dropped post/preun scripts for info.

* Wed Sep 17 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:2.1.5-0.fdr.2
- Remove aesthetic comments.
- buildroot -> RPM_BUILD_ROOT.
- post/preun for info files.

* Mon Apr 07 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:2.1.5-0.fdr.1
- Updated to 2.1.5.

* Tue Apr 01 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:2.1.4-0.fdr.2
- Added Epoch:0.
- Added ldconfig to post and postun.

* Sun Mar 22 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 2.1.4-0.fdr.1
- Updated to 2.1.4.

* Fri Mar 14 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 2.1.3-0.fdr.1
- Fedorafied.

* Mon Oct 21 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Initial RPM release.


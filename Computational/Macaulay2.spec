%global svn r12617

%global emacs_sitelisp  %{_datadir}/emacs/site-lisp/
%global xemacs_sitelisp %{_datadir}/xemacs/site-packages/lisp/

%global INFO_FILES BeginningMacaulay2 Benchmark BGG BoijSoederberg Browse Bruns ChainComplexExtras Classic ConvexInterface ConwayPolynomials Depth Dmodules EdgeIdeals Elimination FirstPackage FourierMotzkin FourTiTwo GenericInitialIdeal gfanInterface HyperplaneArrangements IntegralClosure InvolutiveBases LexIdeals LLLBases LocalRings Macaulay2Doc MapleInterface Markov NoetherNormalization Normaliz NumericalAlgebraicGeometry OpenMath PackageTemplate Parsing PieriMaps Points Polyhedra Polymake Posets PrimaryDecomposition RationalPoints ReesAlgebra Regularity Schubert2 SchurFunctors SchurRings SimpleDoc SimplicialComplexes SRdeformations StatePolytope Style SymmetricPolynomials TangentCone Text XML
 
Summary: System for algebraic geometry and commutative algebra
Name:    Macaulay2
Version: 1.4
Release: 2%{?dist}

License: GPLv2
Group:   Applications/Engineering
URL:     http://www.math.uiuc.edu/Macaulay2/
# the SVN revision is being used as a unique ID
Source0: http://www.math.uiuc.edu/Macaulay2/Downloads/SourceCode/Macaulay2-%{version}-%{svn}-src.tar.bz2
#Source0: Macaulay2-%{version}-%{pre}.tar.bz2
#Source1: Macaulay2-svn_checkout.sh
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source10: Macaulay2.png
Source11: Macaulay2.desktop
Source20: etags.sh

# support files
Source101: 4ti2-1.3.2.tar.gz
Source102: blas.tgz
Source103: cdd+-077a.tar.gz
Source104: cddlib-094f.tar.gz
Source106: factory-3-1-1.tar.gz
Source107: frobby_v0.8.2.tar.gz
Source108: gc-7.2.2010.2.16.tar.gz
Source109: gc-7.2alpha5-2010-09-03.tar.gz
Source110: gc-7.2alpha7-2011-07-25.tar.gz
Source111: gdbm-1.8.3.tar.gz
Source112: gfan0.4plus.tar.gz
Source113: glpk-4.44.tar.gz
Source114: lapack-3.2.2.tgz
Source115: libfac-3-1-1.tar.gz
Source116: libtool-2.2.6a.tar.gz
Source117: lrslib-042c.tar.gz
Source127: mpfr-3.0.0.tar.gz
Source128: mpir-2.1.1.tar.gz
Source129: mpir-2.1.2.tar.gz
Source130: nauty24r2.tar.gz
Source131: normaliz2.5Source.zip
Source132: Normaliz2.5.zip
Source133: ntl-5.5.2.tar.gz
Source134: pari-2.3.5.tar.gz
Source135: polymake-2.9.8.tar.bz2
Source136: readline61-001
Source137: readline61-002
Source138: readline-6.1.tar.gz
Source139: scscp-0.6.1.tar.gz


Patch0: Macaulay2-1.1-optflags.patch
Patch1: Macaulay2-1.2-xdg_open.patch
# Use the Fedora versions of Normaliz and 4ti2
Patch8: Macaulay2-1.3.1-fedora.patch
Patch9: Macaulay2-1.3.1-dso.patch
Patch201739: Macaulay2-0.9.95-bz201739.patch

BuildRequires: autoconf
BuildRequires: bison
BuildRequires: blas-devel
BuildRequires: desktop-file-utils
# etags
BuildRequires: emacs-common
BuildRequires: flex
BuildRequires: gawk
BuildRequires: gc-devel 
BuildRequires: gcc-gfortran
BuildRequires: gdbm-devel
BuildRequires: info
BuildRequires: factory-static
BuildRequires: factory-devel >= 3.1
BuildRequires: libfac-static
BuildRequires: libfac-devel >= 3.1
BuildRequires: lapack-devel
BuildRequires: mpfr-devel
BuildRequires: mpir-devel
BuildRequires: ntl-devel >= 5.4.1
BuildRequires: pari-devel
BuildRequires: compat-readline5-devel 
BuildRequires: ncurses-devel
BuildRequires: time
BuildRequires: libxml2-devel
BuildRequires: mpfr-devel
BuildRequires: glpk-devel
BuildRequires: cddlib-devel
BuildRequires: gfan
BuildRequires: normaliz
BuildRequires: 4ti2
# Runtime deps that RPM didn't pick up
Requires: gfan
Requires: normaliz
Requires: 4ti2

Obsoletes: Macaulay2-common < %{version}-%{release}
Provides:  Macaulay2-common = %{version}-%{release}
Obsoletes: Macaulay2-doc < %{version}-%{release} 
Provides:  Macaulay2-doc = %{version}-%{release}
Obsoletes: Macaulay2-emacs < %{version}-%{release}
Provides:  Macaulay2-emacs = %{version}-%{release}

Provides:  macaulay2 = %{version}-%{release}

# M2-help
Requires: xdg-utils
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description
Macaulay 2 is a new software system devoted to supporting research in
algebraic geometry and commutative algebra written by Daniel R. Grayson
and Michael E. Stillman

%prep
%setup -q  -n %{name}-%{version}-%{svn}

install -p -m755 %{SOURCE20} ./etags

#%patch0 -p1 -b .optflags
#%patch1 -p1 -b .xdg_open
#%patch201739 -p1 -b .bz201739
#%patch8 -p1 -b .fedora
# SVN revision 10971
#%patch9 -p1 -b .dso
# 4ti2 binaries are tucked away in %{_libdir}/4ti2/bin/
# and are thus arch dependant
sed -i "s|@@LIBDIR@@|%{_libdir}|g" Macaulay2/packages/FourTiTwo.m2 

# make a build directory and copy the tarfiles into there
mkdir -p BUILD/normal || echo
mkdir -p BUILD/tarfiles || echo
cp %SOURCE101 BUILD/tarfiles
cp %SOURCE102 BUILD/tarfiles
cp %SOURCE103 BUILD/tarfiles
cp %SOURCE104 BUILD/tarfiles
cp %SOURCE106 BUILD/tarfiles
cp %SOURCE107 BUILD/tarfiles
cp %SOURCE108 BUILD/tarfiles
cp %SOURCE109 BUILD/tarfiles
cp %SOURCE110 BUILD/tarfiles
cp %SOURCE111 BUILD/tarfiles
cp %SOURCE112 BUILD/tarfiles
cp %SOURCE113 BUILD/tarfiles
cp %SOURCE114 BUILD/tarfiles
cp %SOURCE115 BUILD/tarfiles
cp %SOURCE116 BUILD/tarfiles
cp %SOURCE117 BUILD/tarfiles
cp %SOURCE127 BUILD/tarfiles
cp %SOURCE128 BUILD/tarfiles
cp %SOURCE129 BUILD/tarfiles
cp %SOURCE130 BUILD/tarfiles
cp %SOURCE131 BUILD/tarfiles
cp %SOURCE132 BUILD/tarfiles
cp %SOURCE133 BUILD/tarfiles
cp %SOURCE134 BUILD/tarfiles
cp %SOURCE135 BUILD/tarfiles
cp %SOURCE136 BUILD/tarfiles
cp %SOURCE137 BUILD/tarfiles
cp %SOURCE138 BUILD/tarfiles
cp %SOURCE139 BUILD/tarfiles

[ -f configure -a -f include/config.h ] || make 

%build

# We need /sbin:. in PATH to find install-info,etags
PATH=/sbin:$(pwd):$PATH; export PATH

## configure macro currently broken, probably fixable -- Rex
cd BUILD/normal
CFLAGS="%{optflags}" \
CXXFLAGS="%{optflags}" \
CPPFLAGS="-I%{_includedir}/readline5" \
LDFLAGS="-L%{_libdir}/readline5" \
../../configure \
  --prefix=%{_prefix} \
  --libdir="\${prefix}/%{_lib}"
#  --enable-shared

#  --disable-dumpdata \
#  --disable-building \
#  --disable-fc-lib-ldflags \
#  --disable-strip \
#  --with-unbuilt-programs="gfan 4ti2 normaliz" \
#  --disable-frobby

# Not smp-safe
make -j 1


%check 
cd BUILD/normal
make -k check ||:


%install
rm -rf %{buildroot}

# FIXME/TODO: a few examples fail on 64bit/mock, mostly harmless, but still...
cd BUILD/normal
make install DESTDIR=%{buildroot} \
  IgnoreExampleErrors=true

# app img
install -p -m644 -D %{SOURCE10} \
  %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/Macaulay2.png

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  --vendor="fedora" \
  %{SOURCE11}

# Make a new home for emacs files
mkdir -p %{buildroot}%{_datadir}/Macaulay2/emacs
mv %{buildroot}%{emacs_sitelisp}/M2*.el %{buildroot}%{_datadir}/Macaulay2/emacs/
 
for dir in %{emacs_sitelisp} %{xemacs_sitelisp} ; do
  install -d -m755 %{buildroot}$dir
  pushd %{buildroot}%{_datadir}/Macaulay2/emacs
  for file in M2*.el ; do
    ln -s %{_datadir}/Macaulay2/emacs/$file %{buildroot}$dir
    touch %{buildroot}$dir/`basename $file .el`.elc
  done
  popd
done

# unpackaged files
rm -f %{buildroot}%{_infodir}/dir

# Empty files - indicating test passes
rm -f %{buildroot}%{_datadir}/%{name}/Macaulay2Doc/basictests/*.okay

%clean
rm -rf %{buildroot}


%post
touch --no-create %{_datadir}/icons/hicolor ||:
for info_file in %{INFO_FILES} 
do
  /sbin/install-info --quiet %{_infodir}/${info_file}.info %{_infodir}/dir ||:
done

%preun
if [ $1 -eq 0 ]; then
  for info_file in %{INFO_FILES} 
  do
    /sbin/install-info --delete --quiet %{_infodir}/${info_file}.info %{_infodir}/dir ||:
  done
fi

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor > /dev/null 2>&1 ||:
fi

%posttrans
gtk-update-icon-cache -q %{_datadir}/icons/hicolor > /dev/null 2>&1 ||:

%triggerin -- emacs-common
if [ -d %{emacs_sitelisp} ]; then 
  for file in %{_datadir}/Macaulay2/emacs/M2*.el ; do
    ln -sf $file %{emacs_sitelisp}/ ||:
  done
fi

%triggerin -- xemacs-common
if [ -d %{xemacs_sitelisp} ]; then
  for file in %{_datadir}/Macaulay2/emacs/M2*.el ; do
    ln -sf $file %{xemacs_sitelisp}/ ||:
  done
fi

%triggerun -- emacs-common
[ $2 -eq 0 ] && rm -f %{emacs_sitelisp}/M2*.el* || :

%triggerun -- xemacs-common
[ $2 -eq 0 ] && rm -f %{xemacs_sitelisp}/M2*.el* || :


%files
%defattr(-,root,root,-)
%doc Macaulay2/COPYING-GPL-2 Macaulay2/COPYING-GPL-3 Macaulay2/README.in Macaulay2/LAYOUT
%{_bindir}/M2
%{_libexecdir}/%{name}/program-licenses
%{_libexecdir}/%{name}/%{_target_cpu}-Linux-*
%{_datadir}/applications/*Macaulay2.desktop
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/Macaulay2/
%{_docdir}/Macaulay2/
%{_infodir}/*.info*
%{_libdir}/Macaulay2/
%{_mandir}/man1/*
%ghost %{emacs_sitelisp} 
%ghost %{xemacs_sitelisp}


%changelog
* Tue Oct 02 2012 Thomas Uphill <uphill@ias.edu> - 1.4-5
- initial build on 1.4

* Tue Mar 16 2010 Mark Chappell <tremble@fedoraproject.org> - 1.3.1-5
- Run install-info on all of the .info files we installed
- Re-enable the now functional ppc64 build

* Wed Mar 10 2010 Mark Chappell <tremble@fedoraproject.org> - 1.3.1-4
- Add in missing Requires runtime dependancies

* Wed Mar 10 2010 Mark Chappell <tremble@fedoraproject.org> - 1.3.1-3
- GPLv3/GPLv2 conflict, use compat-readline5 - bz#511299

* Tue Mar 09 2010 Mark Chappell <tremble@fedoraproject.org> - 1.3.1-2
- Replace DSO patch with one accepted upstream
- Completely disable static linking

* Wed Feb 24 2010 Mark Chappell <tremble@fedoraproject.org> - 1.3.1-1
- Upstream version increment
- Remove unused patch
- Remove patch applied upstream
- Ensure consistent use of buildroot macro instead of RPM_BUILD_ROOT
- Fix implicit linking DSO failure
- Don't package empty .okay files which simply indicate test passes

* Tue Dec  8 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.2-7
- Explicitly BR factory-static and libfac-static in accordance with the
  Packaging Guidelines (factory-devel/libfac-devel are still static-only).

* Tue Sep 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.2-6
- fixup/optimize scriplets

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.2-4
- rebuild for ntl-devel (shared)

* Wed Feb 25 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.2-3
- BR: libfac-devel,factory-devel >= 3.1
- restore ExcludeArch: ppc64 (#253847)

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 13 2009 Rex Dieter <rdieter@fedoraproject.org> 1.2-1
- Macaulay-1.2

* Thu Oct 02 2008 Rex Dieter <rdieter@fedoraproject.org> 1.1-2
- respin (factory/libfac)

* Tue Mar 11 2008 Rex Dieter <rdieter@fedoraproject.org> 1.1-1
- Macaulay2-1.1
- Obsoletes/Provides: Macaulay2-common (upstream compatibility)
- re-enable ppc64 (#253847)
- IgnoreExampleErrors=true

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.95-10
- Autorebuild for GCC 4.3

* Tue Dec 18 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.95-9
- Provides: macaulay2
- respin against new(er) factory,libfac,ntl

* Wed Aug 22 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.95-8
- ExcludeArch: ppc64 (#253847)

* Tue Aug 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.95-7
- BR: gawk

* Tue Aug 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.95-6
- gc-7.0 patches

* Sat Aug 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.95-5
- License: GPLv2

* Mon Jan 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.95-4
- Ob/Pr: Macaulay2-doc, not -docs (#222609)

* Sat Jan 06 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.95-3
- re-enable ppc build (#201739)

* Tue Jan 02 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.95-2
- ./configure --disable-strip, for usable -debuginfo (#220893)

* Mon Dec 18 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.95-1
- Macaulay2-0.9.95

* Wed Nov 22 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.20-0.5.20060808svn
- .desktop Categories: -Application,Scientific,X-Fedora +ConsoleOnly

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.20-0.4.20060808svn
- fc6 respin

* Tue Aug 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.20-0.3.20060808svn
- ExcludeArch: ppc (bug #201739)
- %ghost (x)emacs site-lisp bits (using hints from fedora-rpmdevtools)

* Tue Aug 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.20-0.2.20060808svn
- 20060808 snapshot

* Mon Jul 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.20-0.1.20060724svn
- 2006-07-15-0.9.20

* Wed Jul 12 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.10-0.6.20060710svn
- 0.9.10

-* Mon Jul 10 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.8-0.6.cvs20060327
- BR: ncurses-devel

* Fri May 05 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.8-0.4.cvs20060327
- 64bit patch (#188709)

* Wed Apr 12 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.8-0.3.cvs20060327 
- omit x86_64, for now (#188709)

* Tue Apr 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.8-0.2.cvs20060327
- 0.9.8 (cvs, no tarball yet)
- drop -doc subpkg (in main now)

* Mon Apr 10 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.2-22
- fix icon location (#188384)

* Thu Mar 30 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.2-21
- really disable %%check (fails on fc5+ anyway) 

* Fri Jan 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.2-20
- .desktop: drop Category=Development
- app icon: follow icon spec
- drop -emacs subpkg (in main now) 

* Fri Sep 16 2005 Rex Dieter <rexdieter[AT]users.sf.net> - 0.9.2-19
- disable 'make check' (fc5/buildsystem error), besides, we get a 
  good consistency check when M2 builds all the doc examples.

* Wed Sep 14 2005 Rex Dieter <rexdieter[AT]users.sf.net> - 0.9.2-18
- rebuild against gc-6.6

* Thu May 26 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.9.2-17
- rebuild (build system x86_64 repository access failed for 0.9.2-16)
- fix build for GCC 4 (#156223)

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.9.2-15
- rebuilt

* Mon Feb 21 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0:0.9.2-14
- x86_64 issues (%%_libdir -> %%_prefix/lib )
- remove desktop_file macro usage

* Sat Oct 23 2004 Rex Dieter <rexdieter at sf.net> 0:0.9.2-0.fdr.13
- BR: time (again)
- omit m2_dir/setup (not needed/wanted)

* Mon Oct 18 2004 Rex Dieter <rexdieter at sf.net> 0:0.9.2-0.fdr.12
- actually *apply* gcc34 patch this time.

* Mon Oct 18 2004 Rex Dieter <rexdieter at sf.net> 0:0.9.2-0.fdr.11
- gcc34 patch

* Fri Oct 1 2004 Rex Dieter <rexdieter at sf.net> 0:0.9.2-0.fdr.10
- explicit BR versions for gc-devel, libfac-devel, factory-devel

* Tue Aug 10 2004 Rex Dieter <rexdieter at sf.net> 0:0.9.2-0.fdr.9
- BR: time

* Thu Jun 03 2004 Rex Dieter <rexdieter at sf.net> 0:0.9.2-0.fdr.8
- .desktop: remove Terminaloptions to be desktop agnostic
- .desktop: Categories += Education;Math;Development (Devel only
  added so it shows *somewhere* in gnome menus)

* Tue Jun 01 2004 Rex Dieter <rexdieter at sf.net> 0:0.9.2-0.fdr.7
- disable default 'make check' (util/screen fails on fc2)

* Tue Mar 30 2004 Rex Dieter <rexdieter at sf.net> 0:0.9.2-0.fdr.6
- desktop-file is now on by default
- use separate (not inline) .desktop file

* Mon Jan 05 2004 Rex Dieter <rexdieter at sf.net> 0:0.9.2-0.fdr.5
- fix BuildRequires: desktop-file-utils to satisfy rpmlint.
- put emacs files in emacs subdir too (to follow supplied docs)
- *really* nuke .cvsignore files
- fix desktop-file-install --add-cateagories usage

* Tue Dec 23 2003 Rex Dieter <rexdieter at sf.net> 0:0.9.2-0.fdr.4
- -emacs: use %%defattr
- -emacs: fix M2-init.el

* Mon Nov 17 2003 Rex Dieter <rexdieter at sf.net> 0:0.9.2-0.fdr.3
- update/simplify macros
- desktop_file support.
- emacs subpkg.
- relax Req's on subpkgs to just: Requires: %%name = %%epoch:%%version
- use non-versioned BuildRequires
- remove redundant BuildRequires: gmp-devel
- remove gc patch, no longer needed.
- delete/not-package a bunch of unuseful files.
- use --disable-strip when debug_package is in use.

* Thu Nov 13 2003 Rex Dieter <rexdieter at sf.net> 0:0.9.2-0.fdr.2
- no longer explictly Requires: emacs

* Wed Nov 05 2003 Rex Dieter <rexdieter at sf.net> 0:0.9.2-0.fdr.1
- missing Epoch: 0

* Fri Sep 12 2003 Rex Dieter <rexdieter at sf.net> 0.9.2-0.fdr.0
- fedora'ize


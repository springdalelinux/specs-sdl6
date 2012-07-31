# Note: perl-Math-Pari has a strict version dependency on pari, and
# needs to be updated simultaneously with pari in the event of a version change

Name:           pari
Version:        2.3.5
Release:        2%{?dist}
Summary:        Number Theory-oriented Computer Algebra System
Group:          System Environment/Libraries
# No version is specified
License:        GPL+
URL:            http://pari.math.u-bordeaux.fr/
Source0:        http://pari.math.u-bordeaux.fr/pub/pari/unix/pari-%{version}.tar.gz
Source1:        pari-init.el
Source2:        gp.desktop
Patch0:         pari-2.3.4-xdgopen.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  emacs
BuildRequires:  readline-devel
BuildRequires:  gmp-devel
BuildRequires:  tex(tex)
BuildRequires:  tex(dvips)
BuildRequires:  desktop-file-utils
BuildRequires:  libX11-devel

# Avoid doc-file dependencies and provides
%{?filter_setup:
 %filter_provides_in %{_datadir}/pari/PARI/
 %filter_requires_in %{_datadir}/pari/PARI/
 %filter_setup
 }

%description
PARI is a widely used computer algebra system designed for fast
computations in number theory (factorizations, algebraic number
theory, elliptic curves...), but also contains a large number of other
useful functions to compute with mathematical entities such as
matrices, polynomials, power series, algebraic numbers, etc., and a
lot of transcendental functions.

This package contains the shared libraries. The interactive
calculator PARI/GP is in package %{name}-gp.


%package devel
Summary:        Header files and libraries for PARI development
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Header files and libraries for PARI development.


%package gp
Summary:        PARI calculator
Group:          Applications/Engineering
Requires:       %{name} = %{version}-%{release}
Requires:       gzip
Requires:       xdg-utils
Requires:       mimehandler(application/x-dvi)

%description gp
PARI/GP is an advanced programmable calculator, which computes
symbolically as long as possible, numerically where needed, and
contains a wealth of number-theoretic functions.


%package emacs
Summary:        Emacs mode for PARI/GP
Group:          Applications/Engineering
Requires:       emacs-common
Requires:       %{name}-gp = %{version}-%{release}

%description emacs
Emacs mode for PARI/GP.


%prep
%setup -q

# Use xdg-open rather than xdvi to display DVI files (#530565)
%patch0 -p1 -b .xdgopen

sed -i "s|runpathprefix='.*'|runpathprefix=''|" config/get_ld
sed -e 's|@DATADIR@|%{_datadir}|' %{SOURCE1} > pari-init.el
sed -e 's|@DATADIR@|%{_datadir}|' %{SOURCE2} > gp.desktop


%build
./Configure \
    --prefix=%{_prefix} \
    --share-prefix=%{_datadir} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir}/man1 \
    --datadir=%{_datadir}/pari \
    --includedir=%{_includedir} \
    --with-gmp
make %{?_smp_mflags} gp CFLAGS="-fPIC $RPM_OPT_FLAGS -fno-strict-aliasing"


%check
make dobench
make dotest-compat
make dotest-intnum
make dotest-qfbsolve
make dotest-rfrac
make dotest-round4


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT STRIP=/bin/true

# we move pari.cfg to the docdir
rm -fr $RPM_BUILD_ROOT%{_prefix}/lib/pari

install -D -m 644 pari-init.el $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d/pari-init.el

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install \
    --vendor fedora \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications \
    gp.desktop

find $RPM_BUILD_ROOT -name xgp -exec rm '{}' ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGES* COPYING COMPAT NEW README
%doc Olinux-*/pari.cfg
%{_libdir}/*.so.*


%files gp
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/*
%dir %{_datadir}/pari/
%doc %{_datadir}/pari/PARI/
%doc %{_datadir}/pari/doc/
%doc %{_datadir}/pari/examples/
%{_datadir}/pari/misc/
%{_datadir}/pari/pari.desc
%{_datadir}/applications/*
%{_mandir}/man*/*


%files devel
%defattr(-,root,root,-)
%{_includedir}/pari/
%{_libdir}/*.so


%files emacs
%defattr(-,root,root,-)
%dir %{_datadir}/emacs/site-lisp/pari/
%doc %{_datadir}/emacs/site-lisp/pari/pariemacs.txt
%{_datadir}/emacs/site-lisp/pari/*.el*
%{_datadir}/emacs/site-lisp/site-start.d/pari-init.el


%changelog
* Fri Oct  1 2010 Mark Chappell <tremble@fedoraproject.org> - 2.3.5-2
- Switch the latex dependencies over to tex(...)

* Fri Jul  9 2010 Paul Howarth <paul@city-fan.org> - 2.3.5-1
- update to 2.3.5 (see CHANGES for details)
- filter out perl dependencies from %%{_datadir}/pari/PARI/

* Thu Jul  8 2010 Paul Howarth <paul@city-fan.org> - 2.3.4-5
- various clean-ups to pacify rpmlint:
  - uses spaces instead of tabs consistently
  - mark %%{_datadir}/emacs/site-lisp/pari/pariemacs.txt as %%doc
  - mark %%{_datadir}/pari/{PARI,doc,examples} as %%doc
  - fix permissions of gp
- don't strip gp so we get debuginfo for it
- move here documents out to separate source files
- make gp subpackage require same version-release of main package

* Wed Jul  7 2010 Paul Howarth <paul@city-fan.org> - 2.3.4-4
- apply patch from Patrice Dumas to use xdg-open rather than xdvi to display
  DVI content, and move the xdg-open requirement from the main package to the
  gp sub-package (#530565)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 22 2008 Gerard Milmeister <gemi@bluewin.ch> - 2.3.4-1
- new release 2.3.4

* Wed Aug 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.3.3-2
- fix license tag

* Sat Feb 23 2008 Gerard Milmeister <gemi@bluewin.ch> - 2.3.3-1
- new release 2.3.3

* Sat Feb 23 2008 Gerard Milmeister <gemi@bluewin.ch> - 2.3.1-3
- corrected desktop file

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.3.1-2
- Autorebuild for GCC 4.3

* Fri Dec 29 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.3.1-1
- new version 2.3.1

* Fri Dec 29 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.3.0-5
- added -fno-strict-aliasing to CFLAGS and enabled ppc build

* Mon Aug 28 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.3.0-4
- Rebuild for FE6

* Fri May 26 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.3.0-3
- Exclude ppc for now, since test fails

* Fri May 26 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.3.0-2
- added %%check section
- use gmp

* Thu May 25 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.3.0-1
- new version 2.3.0

* Fri May 19 2006 Orion Poplawski <orion@cora.nwra.com> - 2.1.7-4
- Fix shared library builds

* Fri Dec  2 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.1.7-3
- Use none for architecture to guarantee working 64bit builds

* Fri Oct 21 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.1.7-2
- some cleanup

* Fri Sep 30 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.1.7-1
- New Version 2.1.7

* Sun Mar  6 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.1.6-1
- New Version 2.1.6

* Mon Nov 22 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:2.1.5-0.fdr.2
- Fixed problem with readline

* Wed Nov 12 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:2.1.5-0.fdr.x
- First Fedora release

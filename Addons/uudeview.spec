Name:           uudeview
Version:        0.5.20
Release:        19%{?dist}

License:        GPLv2+
Group:          Applications/File
Source:         http://www.fpx.de/fp/Software/UUDeview/download/uudeview-0.5.20.tar.gz
Source1:        xdeview.desktop
Patch:          uudeview-debian-patches.patch
URL:            http://www.fpx.de/fp/Software/UUDeview/
Summary:        Applications for uuencoding, uudecoding, ...
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  inews, tcl, tk
BuildRequires:  tex(latex), transfig, desktop-file-utils
BuildRequires:  %{_includedir}/tcl.h, %{_includedir}/tk.h
Requires:       %{_sbindir}/sendmail

%description
Handles uuencoding, xxencoding, yEnc, and base-64 encoding (MIME). Can do
automatic splitting of large encodes, automatic posting.  A must for
anyone serious encoding/decoding.

%package        -n uulib-devel
Summary:        Binary news message decoding library
Group:          Development/Libraries
Provides:       uulib = %{version}-%{release}
Provides:       uulib-static = %{version}-%{release}
Obsoletes:      uulib < 0.5.20-11
Obsoletes:      uulib-static < 0.5.20-16


%description    -n uulib-devel
uulib is a library of functions for decoding uuencoded, xxencoded,
Base64-encoded, and BinHex-encoded data. It is also capable of
encoding data in any of these formats except BinHex.

This package contains header files and static libraries for uulib.


%prep
%setup -q
%patch -p1
%{__sed} -i -e "s,psfig,epsfig,g" doc/library.ltx
%{__sed} -i -e "s,for ff_subdir in lib,for ff_subdir in %{_lib},g" configure

%build
%configure --enable-sendmail=%{_sbindir}/sendmail
make %{?_smp_mflags}
cd doc
make
pdflatex library.ltx

%install
rm -rf $RPM_BUILD_ROOT
sed -i -e "s,xdeview.1,xdeview.1 uuwish.1,g" Makefile
make install BINDIR=$RPM_BUILD_ROOT/%{_bindir} MANDIR=$RPM_BUILD_ROOT/%{_mandir}
desktop-file-install \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --mode 644 \
  --vendor fedora \
  --add-category X-Fedora \
  %{SOURCE1}
mkdir -p $RPM_BUILD_ROOT/%{_includedir}
install -p -m 0644 uulib/uudeview.h $RPM_BUILD_ROOT/%{_includedir}/
mkdir -p $RPM_BUILD_ROOT/%{_libdir}
install -p -m 0644 uulib/libuu.a $RPM_BUILD_ROOT/%{_libdir}/


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING HISTORY IAFA-PACKAGE README uudeview.lsm
%{_mandir}/man1/*.1*
%{_bindir}/uudeview
%{_bindir}/uuenview
%{_bindir}/uuwish
%{_bindir}/xdeview
%{_datadir}/applications/*.desktop

%files -n uulib-devel
%defattr(-,root,root,-)
%doc COPYING HISTORY doc/library.pdf
%{_includedir}/*.h
%{_libdir}/*.a

%changelog
* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.20-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.20-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jun 11 2008 Adrian Reber <adrian@lisas.de> - 0.5.20-17
- updated to newest debian patch
- removed the other patches which are part of the debian patchset
- fixes "uudeview fails to decode any files" (#447664)

* Sun Apr 27 2008 Patrice Dumas <pertusus@free.fr> - 0.5.20-16
- rename uulib-static to uulib-devel
- use tex(latex) provides

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.5.20-15
- Autorebuild for GCC 4.3

* Thu Jan 03 2008 Adrian Reber <adrian@lisas.de> - 0.5.20-14
- rebuilt for tcl-8.5
- added patch from debian
- changed BR from tetex-latex to texlive-latex

* Thu Oct 11 2007 Adrian Reber <adrian@lisas.de> - 0.5.20-13
- rebuilt for BuildID
- updated license tag

* Wed Apr 25 2007 Adrian Reber <adrian@lisas.de> - 0.5.20-12
- fix typo in uulib-devel provides (bz #237836)
- and also renamed uulib-devel to uulib-static

* Wed Feb 14 2007 Adrian Reber <adrian@lisas.de> - 0.5.20-11
- rebuilt
- fix for multi-lib conflict (bz #228390)
  renamed uulib to uulib-devel

* Mon Feb 05 2007 Adrian Reber <adrian@lisas.de> - 0.5.20-10
- rebuilt

* Fri Sep 15 2006 Adrian Reber <adrian@lisas.de> - 0.5.20-9
- rebuilt

* Mon Mar 13 2006 Adrian Reber <adrian@lisas.de> - 0.5.20-8
- make it also build on x86_64

* Mon Mar 13 2006 Adrian Reber <adrian@lisas.de> - 0.5.20-7
- rebuilt

* Fri Apr 29 2005 Adrian Reber <adrian@lisas.de> - 0.5.20-6
- renamed psfig to epsfig in library.ltx (#156249)

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Mon Apr 19 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.5.20-0.fdr.4
- Don't require %%{_sbindir}/sendmail at build time, require at install time.
- Use full URL to source tarball.

* Mon Apr 19 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.5.20-0.fdr.3
- Fixed description for uulib package (bug 1432).
- Added COPYING and HISTORY to uulib package (bug 1432).
- Added EVR to uulib-devel provides (bug 1432).

* Mon Apr 19 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.5.20-0.fdr.2
- Include uulib library in a subpackage.

* Tue Mar 30 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.5.20-0.fdr.1
- Update to 0.5.20 (security).
- Fix tcl.h and tk.h build dependencies.
- Include menu entry for xdeview.

* Tue May 06 2003 Adrian Reber <adrian@lisas.de> - 0:0.5.18-0.fdr.5
- extended the patch uudeview-tempname.patch to fix and remove
  all the remaining security warnings

* Tue May 06 2003 Adrian Reber <adrian@lisas.de> - 0:0.5.18-0.fdr.4
- applied tempnam patch from Michael Schwendt to fix security
  warnings about the usage of the function tempnam()

* Fri May 02 2003 Adrian Reber <adrian@lisas.de> - 0:0.5.18-0.fdr.3
- documentation pdfs created with pdflatex instead of dvipdf and
  therefore ghostscript is no longer a BuildRequire.
- library.ps not created anymore
- added XFree86-devel to BuildRequires

* Fri May 02 2003 Adrian Reber <adrian@lisas.de> - 0:0.5.18-0.fdr.2
- updated BuildRoot to conform with fedora spec template
- capitalized the summary
- added Buildrequires: inews, tcl, tk, /usr/sbin/sendmail, tetex-latex,
  ghostscript, transfig
- changed Group to an official rpm group
- added rm -rf RPM_BUILD_ROOT in install section and removed it from
  prep section
- added _smp_mflags to make
- removed directory doc from package
- doc/library.tex is transformed to ps and pdf and added to package

* Tue Feb 25 2003 Adrian Reber <adrian@lisas.de> - 0.5.18-0.fdr.1
- applied fedora naming conventions

* Sun Dec 22 2002 Adrian Reber <adrian@lisas.de>
- updated to 0.5.18
- demandrakefied

* Wed Mar 27 2002 Lenny Cartier <lenny@mandrakesoft.com> 0.5.17-1mdk
- 0.5.17

* Wed Sep 05 2001 Lenny Cartier <lenny@mandrakesoft.com> 0.5.15-1mdk
- 0.5.15

* Wed Feb 14 2001 Lenny Cartier <lenny@mandrakesoft.com> 0.5.13-4mdk
- rebuild

* Thu Oct 05 2000 Lenny Cartier <lenny@mandrakesoft.com> 0.5.13-3mdk
- used - even if i'm sux ;) - the srpm from Alexander Skwar <ASkwar@linux-mandrake.com> :
	Wed Oct  4 2000 Alexander Skwar <ASkwar@Linux-Mandrake.com> 0.5.13-3mdk
	- Ever wondered why the binary package is so small?  Well, some of us may
	like to have the executable, dunno about you.... (lenny sux)

* Tue Sep 19 2000 Lenny Cartier <lenny@mandrakesoft.com> 0.5.13-2mdk
- bm & macros

* Tue Jun 13 2000 John Johnson <jjohnson@linux-mandrake.com> 0.5.13-1mdk
- Made Mandrake rpm


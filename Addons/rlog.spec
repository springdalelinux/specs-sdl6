Name:		rlog
Summary:	Runtime Logging for C++
Version:	1.4
Release:	8%{?dist}
License:	LGPLv2+
Group:		Development/Libraries
Url:		http://arg0.net/rlog
Source0:	http://rlog.googlecode.com/files/%{name}-%{version}.tar.gz
Source1:	http://rlog.googlecode.com/files/%{name}-%{version}.tar.gz.asc
%ifnarch s390 s390x
%if 0%{?el6}%{?fedora}
BuildRequires:	valgrind-devel
%else
BuildRequires:	valgrind
%endif
%endif
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
RLog provides a flexible message logging facility for C++ programs and
libraries.  It is meant to be fast enough to leave in production code.

%package devel
Summary:	Runtime Logging for C++ - development files
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig
BuildRequires:	doxygen tetex-latex

%description devel
Files needed for developing apps using rlog

%prep
%setup -q
# Disabled: rebuilding docs fails on latex
#%{__rm} -rf docs/html
#%{__rm} -rf docs/latex

%build
%configure --disable-static --enable-valgrind
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install
%{__rm} -f %{buildroot}%{_libdir}/*.la
%{__rm} -rf %{buildroot}%{_docdir}/rlog

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_libdir}/librlog.so.*
%doc README AUTHORS COPYING

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/librlog.so
%doc docs/html docs/latex/refman.pdf

%changelog
* Sun Jun 20 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.4-8
- No valgrind for s390/s390x
- Drop support for Fedora < 8
- Enable valgrind on EL-6

* Sun Sep 27 2009 Peter Lemenkov <lemenkov@gmail.com> - 1.4-7
- Fixed building against valgrind

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 29 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 1.4-5
- Fix FTBFS: do not rebuild docs as it fails on latex

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec  8 2008 Peter Lemenkov <lemenkov@gmail.com> 1.4-3
- Fixed url (BZ# 472665)

* Tue Sep  2 2008 Peter Lemenkov <lemenkov@gmail.com> 1.4-2
- Fix build for F-8
- Fixed license header (LGLV21+ -> LGPLv2+)

* Sat Jul 12 2008 Peter Lemenkov <lemenkov@gmail.com> 1.4-1
- Ver. 1.4
- Dropped upstreamed patch
- Enabled valgrind on all supported platforms

* Fri Jun  6 2008 Peter Lemenkov <lemenkov@gmail.com> 1.3.7-7
- Get rid of whitespaces (cosmetic)
- Note about patch status (applied upstream)

* Fri Feb 22 2008 Peter Lemenkov <lemenkov@gmail.com> 1.3.7-6
- Changed source paths
- Fixed build with GCC 4.3

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3.7-5
- Autorebuild for GCC 4.3

* Sat Feb  9 2008 Peter Lemenkov <lemenkov@gmail.com> 1.3.7-4
- Proper license header (LGPL v 2.1 or any later version)

* Tue Sep 12 2006 Peter Lemenkov <lemenkov@gmail.com> 1.3.7-3%{?dist}
- Rebuild for FC6

* Wed Mar 29 2006 Peter Lemenkov <lemenkov@newmail.ru> 1.3.7-2
- rebuild

* Sun Nov 13 2005 Peter Lemenkov <lemenkov@newmail.ru> 1.3.7-1
- Initial build for FC-Extras
- Release v1.3.7

* Mon Nov 8 2004 Valient Gough <vgough@pobox.com>
- Release v1.3.5
- Add initial attempt at Win32 support (due to help from Vadim Zeitlin)
- Fixes to build on Suse 9.2 (replaced old KDE based autoconf scripts)
- Add "info" channel, and rInfo() macro.
* Mon May 31 2004 Valient Gough <vgough@pobox.com>
- Release v1.3.4
- Portibility changes to allow rlog to build with older C++ compilers and on
  non-x86 computers.
- Add extra ERROR_FMT() macro which allows format string to be passed on Error
  construction.
- Add valgrind support to allow valgrind trace from any assert when running
  under valgrind.
- Update admin dir.
* Sat Mar 13 2004 Valient Gough <vgough@pobox.com>
- Release v1.3.1
- added pkg-config file librlog.pc
- changed license to LGPL
- added rAssertSilent macro
- fixes for special case checks of printf attribute
* Sat Feb 8 2004 Valient Gough <vgough@pobox.com>
- Release v1.3

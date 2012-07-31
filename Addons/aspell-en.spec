%define lang en
%define langrelease 0
%define aspellversion 6
Summary: English dictionaries for Aspell
Name: aspell-%{lang}
Epoch: 50
Version: 6.0
Release: 11%{?dist}
License: MIT and BSD
Group: Applications/Text
URL: http://aspell.net/
Source: ftp://ftp.gnu.org/gnu/aspell/dict/%{lang}/aspell%{aspellversion}-%{lang}-%{version}-%{langrelease}.tar.bz2
Patch: aspell6-en-6.0-practise.patch
Buildrequires: aspell >= 12:0.60
Requires: aspell >= 12:0.60
Obsoletes: aspell-en-gb <= 0.33.7.1
Obsoletes: aspell-en-ca <= 0.33.7.1
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%define debug_package %{nil}

%description
Provides the word list/dictionaries for the following: English, Canadian
English, British English

%prep
%setup -q -n aspell%{aspellversion}-%{lang}-%{version}-%{langrelease}
%patch -p1 -b .ice

%build
./configure
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc Copyright
%{_libdir}/aspell-0.60/*

%changelog
* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 50:6.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 50:6.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 50:6.0-9
- Autorebuild for GCC 4.3

* Thu Aug 30 2007 Ivana Varekova <varekova@redhat.com> - 50:6.0-8
- fix #62225 - add practice to gb world lists

* Fri Mar 30 2007 Ivana Varekova <varekova@redhat.com> - 50:6.0-7
- add version to obstolete flag

* Thu Mar 29 2007 Ivana Varekova <varekova@redhat.com> - 50:6.0-5
- add documentation
- change license tag

* Thu Mar 29 2007 Ivana Varekova <varekova@redhat.com> - 50:6.0-4
- update default buildroot

* Thu Mar 29 2007 Ivana Varekova <varekova@redhat.com> - 50:6.0-3
- update to aspell6
- use configure script to create Makefile
- some minor spec changes

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 50:6.0-2.1
- rebuild

* Fri Mar  3 2006 Ivana Varekova <varekova@redhat.com> - 50:6.0-2
- removed "offencive" (#154352), add "practice" (#62225)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 50:6.0-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 50:6.0-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Jul 18 2005 Ivana Varekova <varekova@redhat.com> 50:6.0-1
- update to aspell5-en-6.0
- build with aspell-0.60.3

* Mon Apr 11 2005 Ivana Varekova <varekova@redhat.com> 50:0.51-12
- rebuilt

* Wed Sep 29 2004 Adrian Havill <havill@redhat.com> 50:0.51-11
- remove debuginfo

* Thu Aug 26 2004 Adrian Havill <havill@redhat.com> 50:0.51-10
- obsolete -en-gb and -en-ca for upgrades

* Wed Aug 11 2004 Adrian Havill <havill@redhat.com> 50:0.51-9
- sync epoch with other aspell dicts, upgrade to 0.51-1

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun 23 2003 Adrian Havill <havill@redhat.com> 0.51-6
- data files are not arch independent

* Fri Jun 20 2003 Adrian Havill <havill@redhat.com> 0.51-5
- first build for new aspell (0.50)

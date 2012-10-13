Summary: Real-time Game Server Status for FPS game servers
Name: qstat
Version: 2.11
Release: 9.20080912svn311%{?dist}
License: Artistic 2.0
Group: Amusements/Games
URL: http://sourceforge.net/projects/qstat/
Source: http://downloads.sourceforge.net/qstat/qstat-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch0: qstat-2.11-20080912svn311.patch

%description
QStat is a command-line program that gathers real-time statistics
from Internet game servers. Most supported games are of the first
person shooter variety (Quake, Half-Life, etc)

%prep
%setup -q
%patch0 -p1

%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make DESTDIR=%{buildroot} install

# Rename binary as discussed in https://bugzilla.redhat.com/show_bug.cgi?id=472750
mv %{buildroot}%{_bindir}/qstat %{buildroot}%{_bindir}/quakestat

# prepare for including to documentation
find template -name "Makefile*" -type f | xargs rm -f

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGES.txt LICENSE.txt
%doc contrib.cfg info/*.txt qstatdoc.html template/
%config(noreplace) %{_sysconfdir}/qstat.cfg
%{_bindir}/quakestat

%changelog
* Sun Nov 08 2009 Andy Shevchenko <andy@smile.org.ua> - 2.11-9.20080912svn311
- rename /usr/bin/qstat to /usr/bin/quakestat (#472750)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-8.20080912svn311
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-7.20080912svn311
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep 12 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.11-6.20080912svn311
- update to latest svn
- upstream relicensed to Artistic 2.0

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.11-5
- Autorebuild for GCC 4.3

* Wed Jan 23 2008 Andy Shevchenko <andy@smile.org.ua> 2.11-4
- fix Source0 URL

* Tue Aug 21 2007 Andy Shevchenko <andy@smile.org.ua> 2.11-3
- Mass rebuild

* Tue Jul 24 2007 Andy Shevchenko <andy@smile.org.ua> 2.11-2.1
- Do not use -delete for find

* Wed May 23 2007 Andy Shevchenko <andy@smile.org.ua> 2.11-2
- Fix URL tag

* Fri Dec 01 2006 Andy Shevchenko <andy@smile.org.ua> 2.11-1
- update to version 2.11
- do not use __make and makeinstall macros

* Tue Aug 29 2006 Andy Shevchenko <andriy@asplinux.com.ua> 2.10-6
- http://fedoraproject.org/wiki/Extras/Schedule/FC6MassRebuild

* Thu Aug 10 2006 Andy Shevchenko <andriy@asplinux.com.ua> 2.10-5
- add Conflicts with torque-client (#201279)

* Mon Jul 31 2006 Andy Shevchenko <andriy@asplinux.com.ua> 2.10-4
- do not pack COMPILE.txt
- no need Makefile* in the documentation

* Fri Jul 28 2006 Andy Shevchenko <andriy@asplinux.com.ua> 2.10-3
- drop check for "/" in install and clean sections
- drop -n for setup macro
- do not use attr macro in files section
- qstat can be used not only for Quake, so change Summary

* Thu Jul 27 2006 Andy Shevchenko <andriy@asplinux.com.ua> 2.10-2
- preparing for Fedora Extras
- correct BuildRoot tag

* Mon Nov 07 2005 Andy Shevchenko <andriy@asplinux.ru>
- update to 2.10
- use full URL for source

* Fri Oct 15 2004 Evgeniy Bolshakov <ben@asplinux.ru>
- update to 2.6

* Fri Jul 09 2004 Alexandr D. Kanevskiy <kad@asplinux.ru>
- cvs patches from XQF project

* Wed Oct 22 2003 Alexandr D. Kanevskiy <kad@asplinux.ru>
- rebuild 

* Thu Jul 10 2003 Alexandr D. Kanevskiy <kad@asplinux.ru>
- build for ASPLinux

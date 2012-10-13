Summary: RADIUS protocol client library
Name: radiusclient-ng
Version: 0.5.6
Release: 5%{?dist}
License: BSD
Group: Applications/Internet
URL: http://developer.berlios.de/projects/radiusclient-ng/
Source0: http://download.berlios.de/%{name}/%{name}-%{version}.tar.gz
Patch0: radiusclient-ng-0.5.6-etc-install.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool

%description
Portable, easy-to-use and standard compliant library suitable for
developing free and commercial software that need support for a RADIUS
protocol (RFCs 2128 and 2139).

%package devel
Summary: Development files for radiusclient-ng
Group: Development/Libraries
Requires: radiusclient-ng = %{version}-%{release}

%description devel
Development files for radiusclient-ng.

%package utils
Summary: Utility programs for radiusclient-ng
Group: Applications/Internet
Requires: radiusclient-ng = %{version}-%{release}

%description utils
Utility programs for radiusclient-ng.

%prep
%setup0 -q
%patch0 -p1

%build
# Need to re-run autconf & automake so that --disable-rpath works and
# the patches to various autoconf/automake files get picked up.
libtoolize --force
aclocal
autoconf
autoheader
automake --add-missing --copy

%configure --disable-static --disable-rpath
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_sbindir}/radexample

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc BUGS CHANGES COPYRIGHT doc/instop.html README

%dir %{_sysconfdir}/radiusclient-ng
%config(noreplace) %{_sysconfdir}/radiusclient-ng/issue
%config(noreplace) %{_sysconfdir}/radiusclient-ng/port-id-map
%config(noreplace) %{_sysconfdir}/radiusclient-ng/radiusclient.conf
%config(noreplace) %{_sysconfdir}/radiusclient-ng/servers

%{_libdir}/libradiusclient-ng.so.*

%dir %{_datadir}/radiusclient-ng/
%{_datadir}/radiusclient-ng/dictionary
%{_datadir}/radiusclient-ng/dictionary.ascend
%{_datadir}/radiusclient-ng/dictionary.compat
%{_datadir}/radiusclient-ng/dictionary.merit
%{_datadir}/radiusclient-ng/dictionary.sip

%files devel
%defattr(-,root,root,-)
%doc COPYRIGHT

%{_includedir}/radiusclient-ng.h
%{_libdir}/libradiusclient-ng.so

%files utils
%defattr(-,root,root,-)
%doc COPYRIGHT

%{_sbindir}/login.radius
%{_sbindir}/radacct
%{_sbindir}/radiusclient
%{_sbindir}/radlogin
%{_sbindir}/radstatus

%changelog
* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb  2 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.5.6-3
- Update patch to properly perform substitutions. (BZ#236350)

* Wed Aug 15 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.5.6-2
- Update to 0.5.6

* Fri May 25 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.5.5.1-1
- Update to 0.5.5.1

* Mon Aug 28 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.5.2-4
- Bump release and rebuild.

* Tue Jul 11 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.5.2-3
- Own /etc/radiusclient-ng

* Tue Jul 11 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.5.2-2
- Add BR so that building in minimal buildroot works
- Run libtoolize.

* Mon May 29 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.5.2-1
- First version for Fedora Extras


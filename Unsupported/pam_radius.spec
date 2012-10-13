Name: pam_radius
Summary: PAM Module for RADIUS Authentication
Version: 1.3.17
Release: 2%{?dist}
Source: ftp://ftp.freeradius.org/pub/radius/pam_radius-%{version}.tar.gz
URL: http://www.freeradius.org/pam_radius_auth/
Group: System Environment/Libraries
BuildRoot: (mktemp -ud %{_tmppath}/%{name}-%{version}-%{release})
License: GPLv2+
Requires: pam
BuildRequires: pam-devel
# patches inconsistencies in debug output 
# Sent upstream via email 20100106
Patch1: pam_radius_auth-debug-consistency.patch
# patches Makefile to ensure shared library builds properly in Fedora
# Sent upstream via email 20100114
Patch2: Makefile-build-shared-library.patch
# patch adds ability to accommodate high-order bit first for Power PC
# Sent upstream via email 20100114
Patch3: pam_radius-md5-ppc-fix.patch
# patches default location of configuration file in pam_radius_auth.h 
# Sent upstream via email 20100114
Patch4: pam_radius_auth-conffile-location.patch
# patches default location of configuration file in radius.h  
# Sent upstream via email 20100114
Patch5: radius-conffile-location.patch
# patches default location of configuration file in pam_radius.conf
# Sent upstream via email 20100221
Patch6: pam_radius_auth-conf-inlinedoc.patch
# patches default location of configuration file in INSTALL documentation file
# Sent upstream via email 20100221
Patch7: INSTALL-doc.patch

%description
pam_radius is a PAM module which allows user authentication using 
a radius server.

%prep
%setup -q
%patch1 
%patch2
%patch3
%patch4
%patch5
%patch6
%patch7

%build
make %{?_smp_mflags} CFLAGS="%{optflags} -Wall -fPIC"

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_lib}/security
install -p pam_radius_auth.so %{buildroot}/%{_lib}/security
mkdir -p %{buildroot}%{_sysconfdir}
install -p pam_radius_auth.conf %{buildroot}%{_sysconfdir}/pam_radius.conf

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README INSTALL USAGE LICENSE Changelog
%config(noreplace) %attr(0600, root, root) %{_sysconfdir}/pam_radius.conf
/%{_lib}/security/pam_radius_auth.so

%changelog
* Tue Feb 21 2010 Tim Lank <timlank@timlank.com> 1.3.17-2
- everything it takes to get this accepted for Fedora 

* Mon Oct 26 2009 Richard Monk <rmonk@redhat.com> 1.3.17-0
- Bump for new version
- spec fixes for x86_64 builds

* Mon Jun 03 2002 Richie Laager <rlaager@wiktel.com> 1.3.15-0
- Inital RPM Version

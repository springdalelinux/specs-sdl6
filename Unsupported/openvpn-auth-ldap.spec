Summary: OpenVPN plugin for LDAP authentication
Name: openvpn-auth-ldap
Version: 2.0.3
Release: 6%{?dist}
License: BSD
Group: Applications/Internet
URL: http://code.google.com/p/openvpn-auth-ldap/
Source0: http://openvpn-auth-ldap.googlecode.com/files/auth-ldap-%{version}.tar.gz
Source1: openvpn-plugin.h
Patch0: auth-ldap-2.0.3-top_builddir.patch
Patch1: auth-ldap-2.0.3-README.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
# This is a plugin not linked against a lib, so hardcode the requirement
# since we require the parent configuration and plugin directories
Requires: openvpn >= 2.0
BuildRequires: re2c
Buildrequires: doxygen
Buildrequires: openldap-devel
BuildRequires: check-devel
BuildRequires: gcc-objc

%description
The OpenVPN Auth-LDAP Plugin implements username/password authentication via
LDAP for OpenVPN 2.x.


%prep
%setup -q -n auth-ldap-%{version}
%patch0 -p1 -b .top_builddir
%patch1 -p1 -b .README
# Fix plugin from the instructions in the included README
%{__sed} -i 's|^plugin .*| plugin %{_libdir}/openvpn/plugin/lib/openvpn-auth-ldap.so "/etc/openvpn/auth/ldap.conf"|g' README
# Install the one required OpenVPN plugin header
%{__install} -p -m 0644 %{SOURCE1} .


%build
%configure \
    --libdir=%{_libdir}/openvpn/plugin/lib \
    --with-openvpn="`pwd`"
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
# Main plugin
%{__mkdir_p} %{buildroot}%{_libdir}/openvpn/plugin/lib
%{__make} install DESTDIR=%{buildroot}
# Example config file
%{__install} -D -p -m 0600 auth-ldap.conf \
    %{buildroot}%{_sysconfdir}/openvpn/auth/ldap.conf


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE README auth-ldap.conf
%dir %{_sysconfdir}/openvpn/auth/
%config(noreplace) %{_sysconfdir}/openvpn/auth/ldap.conf
%{_libdir}/openvpn/plugin/lib/openvpn-auth-ldap.so


%changelog
* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Matthias Saou <http://freshrpms.net/> 2.0.3-5
- Update URL and Source locations.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb  3 2008 Matthias Saou <http://freshrpms.net/> 2.0.3-3
- No longer use the full openvpn sources for the build, as only the
  openvpn-plugin.h file is required, so just include it alone.
- Fix check to check-devel build requirement (it needs the header).

* Thu Jun 21 2007 Matthias Saou <http://freshrpms.net/> 2.0.3-2
- Patch and change README to remove build instructions and have the proper
  line to be added to openvpn's configuration.
- Move config file to a sub-dir since it gets picked up by openvpn otherwise.

* Wed Jun 20 2007 Matthias Saou <http://freshrpms.net/> 2.0.3-1
- Initial RPM release.


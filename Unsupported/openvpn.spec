#define prerelease rc22

%define plugins down-root auth-pam

Name:              openvpn
Version:           2.2.1
Release:           1%{?prerelease:.%{prerelease}}%{?dist}
Summary:           A full-featured SSL VPN solution
URL:               http://openvpn.net/
#Source0:           http://openvpn.net/beta/%{name}-%{version}%{?prerelease:_%{prerelease}}.tar.gz
#Source0:           https://secure.openvpn.net/beta/%{name}-%{version}%{?prerelease:_%{prerelease}}.tar.gz
Source0:           http://openvpn.net/release/%{name}-%{version}%{?prerelease:_%{prerelease}}.tar.gz
#Source1:           https://secure.openvpn.net/beta/signatures/%{name}-%{version}%{?prerelease:_%{prerelease}}.tar.gz.asc
Source1:           http://openvpn.net/signatures/%{name}-%{version}%{?prerelease:_%{prerelease}}.tar.gz.asc
# Sample 2.0 config files
Source2:           roadwarrior-server.conf
Source3:           roadwarrior-client.conf
# Don't start openvpn by default.
Patch0:            openvpn-init.patch
Patch1:            openvpn-script-security.patch
Patch2:            openvpn-2.1.1-init.patch
Patch3:            openvpn-2.1.1-initinfo.patch
License:           GPLv2
Group:             Applications/Internet
BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-%(id -un)
BuildRequires:     lzo-devel
BuildRequires:     openssl-devel
BuildRequires:     pam-devel
BuildRequires:     pkcs11-helper-devel
# For /sbin/ip.
BuildRequires:     iproute
# We need /dev/net/tun.
# This will work with RH9+ dev or udev.
Requires:          dev >= 0:3.3.2-5
# For /sbin/ip.
Requires:          iproute
# For ifconfig and route.
Requires:          net-tools
Requires(pre):     /usr/sbin/useradd
Requires(post):    /sbin/chkconfig
Requires(preun):   /sbin/chkconfig, /sbin/service
Requires(postun):  /sbin/service

# Filter out the perl(Authen::PAM) dependency.
# No perl dependency is really needed at all.
%define __perl_requires sh -c 'cat > /dev/null'

%description
OpenVPN is a robust and highly flexible tunneling application that uses all
of the encryption, authentication, and certification features of the
OpenSSL library to securely tunnel IP networks over a single UDP or TCP
port.  It can use the Marcus Franz Xaver Johannes Oberhumer's LZO library
for compression.

%prep
%setup -q -n %{name}-%{version}%{?prerelease:_%{prerelease}}
%patch0 -p0
%patch1 -p1
%patch2 -p0
%patch3 -p0

sed -i -e 's,%{_datadir}/openvpn/plugin,%{_libdir}/openvpn/plugin,' openvpn.8

# %%doc items shouldn't be executable.
find contrib sample-config-files sample-keys sample-scripts -type f -perm +100 \
    -exec chmod a-x {} \;

%build
#  --enable-pthread        Enable pthread support (Experimental for OpenVPN 2.0)
#  --enable-password-save  Allow --askpass and --auth-user-pass passwords to be
#                          read from a file
#  --enable-iproute2       Enable support for iproute2
#  --with-ifconfig-path=PATH   Path to ifconfig tool
#  --with-iproute-path=PATH    Path to iproute tool
#  --with-route-path=PATH  Path to route tool
%configure \
    --enable-pthread \
    --enable-password-save \
    --enable-iproute2 \
    --with-ifconfig-path=/sbin/ifconfig \
    --with-iproute-path=/sbin/ip \
    --with-route-path=/sbin/route
%{__make}

# Build plugins
for plugin in %{plugins} ; do
    %{__make} -C plugin/$plugin
done

%check
# Test Crypto:
./openvpn --genkey --secret key
./openvpn --test-crypto --secret key

# Randomize ports for tests to avoid conflicts on the build servers.
cport=$[ 50000 + ($RANDOM % 15534) ]
sport=$[ $cport + 1 ]
sed -e 's/^\(rport\) .*$/\1 '$sport'/' \
    -e 's/^\(lport\) .*$/\1 '$cport'/' \
    < sample-config-files/loopback-client \
    > %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u})-loopback-client
sed -e 's/^\(rport\) .*$/\1 '$cport'/' \
    -e 's/^\(lport\) .*$/\1 '$sport'/' \
    < sample-config-files/loopback-server \
    > %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u})-loopback-server

# Test SSL/TLS negotiations (runs for 2 minutes):
./openvpn --config \
    %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u})-loopback-client &
./openvpn --config \
    %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u})-loopback-server
wait

rm -f %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u})-loopback-client \
    %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u})-loopback-server

%install
rm -rf $RPM_BUILD_ROOT

install -D -m 0644 %{name}.8 $RPM_BUILD_ROOT%{_mandir}/man8/%{name}.8
install -D -m 0755 %{name} $RPM_BUILD_ROOT%{_sbindir}/%{name}
install -D -m 0755 sample-scripts/%{name}.init \
    $RPM_BUILD_ROOT%{_initrddir}/%{name}
install -d -m 0755 $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pR easy-rsa $RPM_BUILD_ROOT%{_datadir}/%{name}/
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/easy-rsa/Windows
cp %{SOURCE2} %{SOURCE3} sample-config-files/

mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{name}/plugin/lib
for plugin in %{plugins} ; do
    install -m 0755 plugin/$plugin/openvpn-$plugin.so \
        $RPM_BUILD_ROOT%{_libdir}/%{name}/plugin/lib/openvpn-$plugin.so
    cp plugin/$plugin/README plugin/$plugin.txt
done

mkdir -m 755 -p $RPM_BUILD_ROOT%{_var}/run/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group openvpn &>/dev/null || groupadd -r openvpn
getent passwd openvpn &>/dev/null || \
    /usr/sbin/useradd -r -g openvpn -s /sbin/nologin -c OpenVPN \
        -d /etc/openvpn openvpn

%post
/sbin/chkconfig --add %{name}

%preun
if [ "$1" = 0 ]; then
    /sbin/service %{name} stop
    /sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" -ge 1 ]; then
    /sbin/service %{name} condrestart >/dev/null 2>&1
fi

%files
%defattr(-,root,root,0755)
%doc AUTHORS COPYING COPYRIGHT.GPL INSTALL PORTS README
# Add NEWS when it isn't zero-length.
%doc plugin/*.txt
%doc contrib sample-config-files sample-keys sample-scripts
%{_mandir}/man8/%{name}.8*
%{_sbindir}/%{name}
%{_datadir}/%{name}/
%{_libdir}/%{name}/
%{_initrddir}/%{name}
%{_var}/run/%{name}/
%config %dir %{_sysconfdir}/%{name}/

%changelog
* Fri Jul 08 2011 Jon Ciesla <limb@jcomserv.net> 2.2.1-1
- Update to 2.2.1.

* Fri Jun 17 2011 Jon Ciesla <limb@jcomserv.net> 2.2.0-2
- Bump and rebuild for BZ 712251.

* Thu May 19 2011 Jon Ciesla <limb@jcomserv.net> 2.2.0-1
- Update to 2.2.0.

* Thu Mar 17 2011 Jon Ciesla <limb@jcomserv.net> 2.1.4-1
- Update to 2.1.4.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 07 2010 Jon Ciesla <limb@jcomserv.net> 2.1.3-1
- Update to 2.1.3.

* Thu Aug 19 2010 Steven Pritchard <steve@kspei.com> 2.1.2-1
- Update to 2.1.2.

* Mon Jan 04 2010 Jon Ciesla <limb@jcomserv.net> 2.1.1-2
- Fix init script *.sh sourcing, BZ 498348.
- Added init script info block, BZ 392991, BZ 541219.

* Fri Dec 11 2009 Steven Pritchard <steve@kspei.com> 2.1.1-1
- Update to 2.1.1.

* Sat Nov 21 2009 Steven Pritchard <steve@kspei.com> 2.1-0.39.rc22
- Update to 2.1_rc22.

* Thu Nov 12 2009 Steven Pritchard <steve@kspei.com> 2.1-0.38.rc21
- Update to 2.1_rc21.

* Sun Oct 25 2009 Robert Scheck <robert@fedoraproject.org> 2.1-0.37.rc20
- Added script_security initialisation in initscript (#458594 #c20)

* Fri Oct 02 2009 Steven Pritchard <steve@kspei.com> 2.1-0.36.rc20
- Update to 2.1_rc20.

* Sun Sep 06 2009 Kalev Lember <kalev@smartlink.ee> - 2.1-0.35.rc19
- Update to 2.1_rc19
- Build with pkcs11-helper

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.1-0.34.rc15
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-0.33.rc15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-0.32.rc15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> 2.1-0.31.rc15
- rebuild with new openssl

* Thu Dec 11 2008 Steven Pritchard <steve@kspei.com> 2.1-0.30.rc15
- Attempt to fix BZ#476129.

* Sat Nov 29 2008 Robert Scheck <robert@fedoraproject.org> 2.1-0.29.rc15
- Update to 2.1_rc15

* Wed Aug 13 2008 Steven Pritchard <steve@kspei.com> 2.1-0.28.rc9
- Add "--script-security 2" by default for backwards compatibility
  (see bug #458594).

* Fri Aug 01 2008 Steven Pritchard <steve@kspei.com> 2.1-0.27.rc9
- Update to 2.1_rc9.

* Sat Jun 14 2008 Steven Pritchard <steve@kspei.com> 2.1-0.26.rc8
- Update to 2.1_rc8.
- Update License tag.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.1-0.25.rc7
- Autorebuild for GCC 4.3

* Tue Jan 29 2008 Steven Pritchard <steve@kspei.com> 2.1-0.24.rc7
- Update to 2.1_rc7
- Drop BETA21-userpriv-fixups.patch (upstream)

* Fri Jan 25 2008 Steven Pritchard <steve@kspei.com> 2.1-0.23.rc6
- Apply update to BETA21-userpriv-fixups.patch from Alon Bar-Lev

* Thu Jan 24 2008 Steven Pritchard <steve@kspei.com> 2.1-0.22.rc6
- Update to 2.1_rc6
- Pass paths to ifconfig, ip, and route to configure
- BR iproute and Require iproute and net-tools
- Add BETA21-userpriv-fixups.patch from Alon Bar-Lev

* Wed Jan 23 2008 Steven Pritchard <steve@kspei.com> 2.1-0.21.rc5
- Update to 2.1_rc5

* Wed Dec 05 2007 Steven Pritchard <steve@kspei.com> 2.1-0.20.rc4
- Remove check macro cruft.

* Thu Apr 26 2007 Steven Pritchard <steve@kspei.com> 2.1-0.19.rc4
- Update to 2.1_rc4

* Mon Apr 23 2007 Steven Pritchard <steve@kspei.com> 2.1-0.18.rc3
- Update to 2.1_rc3

* Fri Mar 02 2007 Steven Pritchard <steve@kspei.com> 2.1-0.17.rc2
- Update to 2.1_rc2

* Tue Feb 27 2007 Steven Pritchard <steve@kspei.com> 2.1-0.16.rc1
- Randomize ports for tests to avoid conflicts on the build servers

* Tue Feb 27 2007 Steven Pritchard <steve@kspei.com> 2.1-0.15.rc1
- Update to 2.1_rc1

* Mon Oct 02 2006 Steven Pritchard <steve@kspei.com> 2.1-0.14.beta16
- Update to 2.1_beta16
- Drop Paul's patch (in upstream)

* Tue Sep 12 2006 Steven Pritchard <steve@kspei.com> 2.1-0.13.beta15
- Update to 2.1_beta15
- Add openvpn-2.1_beta15-test-timeout.patch to avoid test hang
  (from Paul Howarth)

* Mon Aug 28 2006 Steven Pritchard <steve@kspei.com> 2.1-0.12.beta14
- Rebuild

* Mon Jul 31 2006 Steven Pritchard <steve@kspei.com> 2.1-0.11.beta14
- Rebuild

* Fri Apr 14 2006 Steven Pritchard <steve@kspei.com> 2.1-0.10.beta14
- Update to 2.1_beta14

* Wed Apr 12 2006 Steven Pritchard <steve@kspei.com> 2.1-0.9.beta13
- Update to 2.1_beta13

* Wed Apr 05 2006 Steven Pritchard <steve@kspei.com> 2.1-0.8.beta12
- Update to 2.1_beta12 (BZ#188050/CVE-2006-1629)

* Tue Feb 21 2006 Steven Pritchard <steve@kspei.com> 2.1-0.7.beta11
- Update to 2.1_beta11

* Tue Feb 14 2006 Steven Pritchard <steve@kspei.com> 2.1-0.6.beta8
- Update to 2.1_beta8

* Wed Jan 04 2006 Steven Pritchard <steve@kspei.com> 2.1-0.5.beta7
- Man page shouldn't be executable (BZ#176953)

* Tue Dec 06 2005 Steven Pritchard <steve@kspei.com> 2.1-0.4.beta7
- Rebuild

* Fri Nov 18 2005 Steven Pritchard <steve@kspei.com> 2.1-0.3.beta7
- Update to 2.1_beta7

* Tue Nov 08 2005 Steven Pritchard <steve@kspei.com> 2.1-0.2.beta6
- Make sample-scripts (etc.) non-executable to avoid some dependencies

* Wed Nov 02 2005 Steven Pritchard <steve@kspei.com> 2.1-0.1.beta6
- Update to 2.1_beta6

* Mon Oct 17 2005 Steven Pritchard <steve@kspei.com> 2.1-0.1.beta4
- Update to 2.1_beta4

* Thu Aug 25 2005 Steven Pritchard <steve@kspei.com> 2.0.2-1
- Update to 2.0.2
- Refine roadwarrior-server.conf a bit

* Mon Aug 22 2005 Steven Pritchard <steve@kspei.com> 2.0.1-1
- Update to 2.0.1

* Mon Jun 27 2005 Steven Pritchard <steve@kspei.com> 2.0-2
- Move the plugin directory to _libdir
- Drop the easy-rsa/Windows directory
- Comment cleanups
- Add "processname" header to init script
- The init script isn't a config file
- Tag contrib, sample-config-files, sample-keys, and sample-scripts as doc
- Create/own pid dir

* Sat Jun 25 2005 Steven Pritchard <steve@kspei.com> 2.0-1
- Update to 2.0 final
- Drop Epoch: 0 and rebuild for Fedora Extras

* Wed Feb 16 2005 Steven Pritchard <steve@kspei.com> 0:2.0-0.fdr.0.14.rc13
- Fix/add paths to useradd

* Mon Feb 14 2005 Steven Pritchard <steve@kspei.com> 0:2.0-0.fdr.0.13.rc13
- Update to 2.0_rc13
- More spec cleanup (suggestions from Matthias Saou)

* Tue Feb 08 2005 Steven Pritchard <steve@kspei.com> 0:2.0-0.fdr.0.12.rc12
- Update to 2.0_rc12
- Small spec cleanups
- Drop perl auto-requirements entirely

* Mon Dec 20 2004 Steven Pritchard <steve@kspei.com> 0:2.0-0.fdr.0.11.rc6
- Add down-root and auth-pam plugins
- Add --enable-password-save and --enable-iproute2
- Add crypto and loopback tests (somewhat time-consuming)

* Thu Dec 16 2004 Steven Pritchard <steve@kspei.com> 0:2.0-0.fdr.0.10.rc5
- Update to 2.0_rc5
- Change the port to 1194 in the roadwarrior-*.conf samples
- Change openvpn-init.patch to reformat the description in the init script
- Modify the Summary and description (OpenVPN isn't UDP-only)

* Tue Dec 14 2004 Steven Pritchard <steve@kspei.com> 0:2.0-0.fdr.0.9.rc1
- Remove the perl(Authen::PAM) dependency

* Thu Dec 09 2004 Steven Pritchard <steve@kspei.com> 0:2.0-0.fdr.0.8.rc1
- Update to 2.0_rc1

* Tue Nov 16 2004 Steven Pritchard <steve@kspei.com> 0:2.0-0.fdr.0.7.beta17
- Update to 2.0_beta17
- Require dev instead of /dev/net/tun (for udev compatibility)
- Change openvpn-init.patch to match upstream (starts even earlier now)

* Wed Aug 04 2004 Steven Pritchard <steve@kspei.com> 0:2.0-0.fdr.0.6.beta10
- Remove unnecessary BuildRequires: kernel-headers

* Tue Aug 03 2004 Steven Pritchard <steve@kspei.com> 0:2.0-0.fdr.0.5.beta10
- Update to 2.0_beta10
- Minor fix to configuration example
- Change the init script to start a little earlier and stop much later
  (after netfs) by default
- Remove a lot of unnecessary macro use (install/mkdir/cp)
- Don't create /dev/net/tun, use Requires instead

* Sat Jul 17 2004 Steven Pritchard <steve@kspei.com> 0:2.0-0.fdr.0.4.beta7
- Update to 2.0_beta7
- Include gpg signature in source rpm
- Include 2.0-style configuration examples
- Minor spec cleanup

* Wed Apr 28 2004 Steven Pritchard <steve@kspei.com> 0:2.0-0.fdr.0.3.test23
- Add openvpn-init.patch to leave the init script disabled by default

* Wed Apr 28 2004 Steven Pritchard <steve@kspei.com> 0:2.0-0.fdr.0.2.test23
- Fix URL and Source0
- Add an openvpn user

* Wed Apr 28 2004 Steven Pritchard <steve@kspei.com> 0:2.0-0.fdr.0.1.test23
- Update to 2.0_test23
- BuildRequires lzo-devel, kernel-headers, openssl-devel
- Lots of spec cleanup

* Sun Feb 23 2003 Matthias Andree <matthias.andree@gmx.de> 1.3.2.14-1
- Have the version number filled in by autoconf.

* Wed Jul 10 2002 James Yonan <jim@yonan.net> 1.3.1-1
- Fixed %%preun to only remove service on final uninstall

* Mon Jun 17 2002 bishop clark (LC957) <bishop@platypus.bc.ca> 1.2.2-1
- Added condrestart to openvpn.spec & openvpn.init.

* Wed May 22 2002 James Yonan <jim@yonan.net> 1.2.0-1
- Added mknod for Linux 2.4.

* Wed May 15 2002 Doug Keller <dsk@voidstar.dyndns.org> 1.1.1.16-2
- Added init scripts
- Added conf file support

* Mon May 13 2002 bishop clark (LC957) <bishop@platypus.bc.ca> 1.1.1.14-1
- Added new directories for config examples and such

* Sun May 12 2002 bishop clark (LC957) <bishop@platypus.bc.ca> 1.1.1.13-1
- Updated buildroot directive and cleanup command
- added easy-rsa utilities

* Mon Mar 25 2002 bishop clark (LC957) <bishop@platypus.bc.ca> 1.0-1
- Initial build.

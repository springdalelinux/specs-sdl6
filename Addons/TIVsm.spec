%define tivversion 6.2.2
%define tivrelease 0
Summary: Tivoli Storage Manager startup scripts
Name: TIVsm
Version: %{tivversion}
Release: %{tivrelease}.1%{?dist}
Group: Applications/Internet
Source0: tsmscheduler.init
License: GPL
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-root
# we require coreutils in hopes of fixing installation of
# TIVsm-API and TIVsm-BA, to see if it helps
Requires: TIVsm-API >= %{tivversion}-%{tivrelease}, TIVsm-BA >= %{tivversion}-%{tivrelease}
Requires: coreutils procps findutils
Requires: /sbin/chkconfig /sbin/service
# this is an attempt to ensure that our post install script runs AFTER all these
Requires(preun): TIVsm-API >= %{tivversion}-%{tivrelease}, TIVsm-BA >= %{tivversion}-%{tivrelease}
Requires(post): TIVsm-API >= %{tivversion}-%{tivrelease}, TIVsm-BA >= %{tivversion}-%{tivrelease}
Requires: ksh
BuildArch: noarch

%description
This rpm contains a simple startup script for IBM's
Tivoli Storage Manager backup scheduler client.

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_initrddir} $RPM_BUILD_ROOT/var/log/tsm
install -m 755 %{SOURCE0} $RPM_BUILD_ROOT%{_initrddir}/tsmscheduler

mkdir -p $RPM_BUILD_ROOT/opt/tivoli/tsm/client/ba/bin/
cat > $RPM_BUILD_ROOT/opt/tivoli/tsm/client/ba/bin/dsm.opt.sample <<ENDDSMOPT
SErvername TSM
subdir yes
ENDDSMOPT
cat > $RPM_BUILD_ROOT/opt/tivoli/tsm/client/ba/bin/dsm.sys.sample <<ENDDSMSYS
servername TSM
  commmethod        TCPip
  tcpport           160TSMSERVERNUMBER
  tcpserveraddress  tsmTSMSERVERNUMBER.princeton.edu
  schedlogname      /var/log/tsm/dsmsched
* prune and save to dsmsched.pru
  schedlogretention 30 S
  errorlogname      /var/log/tsm/dsmerlog
* prune and save to dsmerlog.pru
  errorlogretention 30 S
  nodename          NODENAMEPLEASESET
  passwordaccess    generate
* domain            / /usr /var/local
* inclexcl          /etc/inclexcl.def
  compression       on
  exclude.dir       /selinux
  exclude.dir       /sys
  exclude.dir       /proc
  exclude.file      /var/cache/yum/*/packages/*rpm
  exclude.file      /var/cache/yum/*/headers/*hdr
ENDDSMSYS

mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d/
cat > $RPM_BUILD_ROOT/etc/logrotate.d/tsm <<ENDLOG
/var/log/tsm/dsmsched.pru {
    compress
    dateext
    rotate 9999
    missingok
    notifempty
    daily
    create 0600 root root
}

/var/log/tsm/dsmerlog.pru {
    compress
    dateext
    rotate 9999
    missingok
    notifempty
    daily
    create 0600 root root
}
ENDLOG

%post
/sbin/chkconfig --add tsmscheduler
/sbin/service tsmscheduler condrestart >> /dev/null
/usr/sbin/semanage fcontext -a -t textrel_shlib_t '/usr/lib/lib(dmapi|gpfs).so$' >/dev/null 2>&1 || :
[ -e /usr/bin/ksh ] || ln -s /bin/ksh /usr/bin/ksh

%preun
if [ $1 = 0 ]; then
 /sbin/chkconfig --del tsmscheduler
 /sbin/service tsmscheduler stop >> /dev/null
 /usr/sbin/semanage fcontext -d -t textrel_shlib_t '/usr/lib/lib(dmapi|gpfs).so$' >/dev/null 2>&1 || :
fi
exit 0

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_initrddir}/tsmscheduler
%dir %attr(0700,root,root) /var/log/tsm
%attr(0600,root,root) /etc/logrotate.d/tsm
%attr(0600,root,root) /opt/tivoli/tsm/client/ba/bin/dsm.*sample

%changelog
* Thu Feb 02 2012 Josko Plazonic <plazonic@math.princeton.edu>
- add a dependency on ksh and also create a symlink to /usr/bin/ksh

* Thu Apr 19 2007 Josko Plazonic <plazonic@math.princeton.edu>
- initial build

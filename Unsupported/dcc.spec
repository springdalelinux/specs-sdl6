%define homedir %{_localstatedir}/dcc
%define cgibin %{_localstatedir}/dcc/cgibin
%define mylibexecdir %{_libexecdir}/dcc
Summary: A clients-server system for collecting checksums of mail messages
Name: dcc
Version: 1.3.141
Release: 26%{?dist}
URL: http://www.rhyolite.com/anti-spam/dcc/
Source0: http://www.rhyolite.com/anti-spam/dcc/source/dcc-%{version}.tar.Z
License: distributable for non-commercial use
Group: Applications/Internet
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: sendmail-devel

%description
The DCC or Distributed Checksum Clearinghouse is currently a system of
many clients and more than 120 servers that collects and count
checksums related to several million mail messages per day, most as
seen by Internet Service Providers. The counts can be used by SMTP
servers and mail user agents to detect and reject or filter spam or
unsolicited bulk mail. DCC servers exchange or "flood" common
checksums. The checksums include values that are constant across
common variations in bulk messages, including "personalizations."

%prep
%setup -q -n dcc-%{version}
find . -name Makefile.in -o -name make-dcc_conf.in | xargs sed -i -e's,chown,:,g'

%build
export CFLAGS="%{optflags}"
./configure \
  --with-installroot=%{buildroot} \
  %{?_without_dccm:--disable-dccm} \
  --homedir=%{homedir} \
  --with-cgibin=%{cgibin} \
  --libexecdir=%{mylibexecdir} \
  --bindir=%{_bindir} \
  --mandir=%{_mandir} \
  --with-uid=dccuser
make

%install
rm -rf %{buildroot}
make install \
  SET_BINOWN= SET_MANOWN= SET_DCCOWN=
perl -pi -e's,%{buildroot},,g' %{buildroot}%{homedir}/map.txt

%pre
/usr/sbin/useradd -r -d %{homedir} -r -s /bin/true dccuser >/dev/null 2>&1 || :

%postun
if [ $1 -eq 0 ]; then
	/usr/sbin/userdel dccuser 2>/dev/null || :
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE FAQ* CHANGES
%dir %attr(755,dccuser,root) %{homedir}
%dir %attr(750,dccuser,root) %{homedir}/log
%config(noreplace) %attr(644,dccuser,root) %{homedir}/dcc_conf
%config(noreplace) %attr(644,dccuser,root) %{homedir}/flod
%config(noreplace) %attr(644,dccuser,root) %{homedir}/grey_flod
%config(noreplace) %attr(644,dccuser,root) %{homedir}/grey_whitelist
%config(noreplace) %attr(600,dccuser,root) %{homedir}/ids
%config(noreplace) %attr(600,dccuser,root) %{homedir}/map
%config(noreplace) %attr(600,dccuser,root) %{homedir}/map.txt
%config(noreplace) %attr(644,dccuser,root) %{homedir}/whiteclnt
%config(noreplace) %attr(644,dccuser,root) %{homedir}/whitecommon
%config(noreplace) %attr(644,dccuser,root) %{homedir}/whitelist
%attr(4555,dccuser,root) %{_bindir}/cdcc
%attr(4555,dccuser,root) %{_bindir}/dccproc
%{_bindir}/dccif-test
%dir %attr(755,root,root) %{mylibexecdir}
%attr(755,root,root) %{mylibexecdir}/c*
%attr(755,root,root) %{mylibexecdir}/db*
%attr(755,root,root) %{mylibexecdir}/dcc-*
%attr(755,root,root) %{mylibexecdir}/dcc[d-m]*
%attr(4555,dccuser,root) %{mylibexecdir}/dccsight
%attr(755,root,root) %{mylibexecdir}/dns*
%attr(755,root,root) %{mylibexecdir}/dump*
%attr(755,root,root) %{mylibexecdir}/[f-w]*
%{cgibin}
%{_mandir}/man8/*

%changelog
* Sun Mar  1 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.3.103-23
- Update to 1.3.103.

* Wed Apr 30 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.3.90-22
- Update to 1.3.90.

* Wed Oct 17 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.3.66-20
- Update to 1.3.66.

* Sat Oct 13 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.3.64-19
- Update to 1.3.64.

* Wed Jun 13 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.3.57-18
- Update to 1.3.57.

* Wed May 23 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.3.56-17
- Update to 1.3.56.

* Mon Feb 12 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.3.50-16
- update to 1.3.50.

* Sun Oct 22 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.3.42-15
- Update to 1.3.42.

* Wed May 31 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.3.31.

* Sat Nov 26 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.3.21.

* Sun Apr  3 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.3.0.

* Sun Mar  6 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.2.71.

* Mon Jan 17 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.2.67.

* Fri Dec 17 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.2.64.

* Tue Nov  2 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.2.58.

* Fri Oct 22 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.2.57.

* Thu Sep 16 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.2.53.

* Mon May 31 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.2.49.

* Mon May  3 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Updated to 1.2.47.

* Sat Apr  3 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.2.39.

* Fri May  2 2003 Axel Thimm <Axel.Thimm@ATrpms.net>
- Initial build.




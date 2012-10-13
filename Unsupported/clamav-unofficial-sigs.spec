Name:           clamav-unofficial-sigs
Version:        3.7.1
Release:        5%{?dist}
Summary:        Scripts to download unoffical clamav signatures 
Group:          Applications/System
License:        BSD
URL:            http://www.inetmsg.com/pub/
Source0:        http://www.inetmsg.com/pub/clamav-unofficial-sigs-%{version}.tar.gz
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       clamav clamav-update rsync gnupg diffutils curl bind-utils

%description
This package contains scripts and configuration files
that provide the capability to download, test, and 
update the 3rd-party signature databases provide by 
Sanesecurity, SecuriteInfo, MalwarePatrol, OITC, 
INetMsg and ScamNailer.

%prep
%setup -q
iconv -f iso8859-1 -t utf-8 CHANGELOG > CHANGELOG.conv && mv -f CHANGELOG.conv CHANGELOG
sed -i 's:/usr/local/bin/:/usr/bin/:' clamav-unofficial-sigs-cron
sed -i 's:root:clamupdate:' clamav-unofficial-sigs-cron
sed -i 's:-c /usr/local/etc/clamav-unofficial-sigs.conf:\&>/dev/null:' clamav-unofficial-sigs-cron
sed -i 's:/var/log/clamav-unofficial-sigs.log:/var/log/clamav-unofficial-sigs/clamav-unofficial-sigs.log:' clamav-unofficial-sigs-logrotate
sed -i 's:/usr/unofficial-dbs:%{_localstatedir}/lib/%{name}:' clamav-unofficial-sigs.conf
sed -i 's:/var/log:%{_localstatedir}/log/%{name}:' clamav-unofficial-sigs.conf
sed -i 's:/path/to/ham-test/directory:%{_localstatedir}/lib/%{name}/ham-test:' clamav-unofficial-sigs.conf
sed -i 's:"clamav":"clamupdate":' clamav-unofficial-sigs.conf
sed -i 's:/var/run/clamd.pid:/var/run/clamd.scan/clamd.pid:' clamav-unofficial-sigs.conf
sed -i 's:user_configuration_complete="no":user_configuration_complete="yes":' clamav-unofficial-sigs.conf
sed -i 's:enable_logging="no":enable_logging="yes":' clamav-unofficial-sigs.conf
sed -i 's:root:clamupdate:g' clamav-unofficial-sigs-logrotate
sed -i 's:default_config="/etc/clamav-unofficial-sigs.conf":default_config="/etc/clamav-unofficial-sigs/clamav-unofficial-sigs.conf":' clamav-unofficial-sigs.sh

%build
#nothing to do here

%install
rm -rf $RPM_BUILD_ROOT
install -d -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install -d -p $RPM_BUILD_ROOT%{_sysconfdir}/cron.d
install -d -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -d -p $RPM_BUILD_ROOT%{_bindir}
install -d -p $RPM_BUILD_ROOT%{_mandir}/man8
install -d -p $RPM_BUILD_ROOT%{_localstatedir}/log/%{name}
install -d -p $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}
install -d -p $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/ham-test
install -p -m0755 clamav-unofficial-sigs.sh $RPM_BUILD_ROOT%{_bindir}/clamav-unofficial-sigs.sh
install -p -m0755 clamd-status.sh $RPM_BUILD_ROOT%{_bindir}/clamd-status.sh
install -p -m0644 clamav-unofficial-sigs-cron $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/clamav-unofficial-sigs
install -p -m0644 clamav-unofficial-sigs-logrotate $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/clamav-unofficial-sigs
install -p -m0644 clamav-unofficial-sigs.8 $RPM_BUILD_ROOT%{_mandir}/man8/clamav-unofficial-sigs.8
pushd $RPM_BUILD_ROOT%{_mandir}/man8/
ln -s clamav-unofficial-sigs.8 clamav-unofficial-sigs.sh.8
popd
install -p -m0644 clamav-unofficial-sigs.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/clamav-unofficial-sigs.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README CHANGELOG LICENSE
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/clamav-unofficial-sigs.conf
%config(noreplace) %{_sysconfdir}/cron.d/*
%config(noreplace) %{_sysconfdir}/logrotate.d/*
%{_bindir}/*
%{_mandir}/man8/*
%attr(0755,clamupdate,clamupdate) %dir %{_localstatedir}/log/%{name}
%attr(0755,clamupdate,clamupdate) %dir %{_localstatedir}/lib/%{name}
%attr(0755,clamupdate,clamupdate) %dir %{_localstatedir}/lib/%{name}/ham-test

%changelog
* Sat Apr 23 2011 Andrew Colin Kissa <andrew@topdog.za.net> - 3.7.1-5
- FIX: bugzilla #683139

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 02 2011 Andrew Colin Kissa <andrew@topdog.za.net> - 3.7.1-3
- Fixes requested by reviewer

* Thu Dec 23 2010 Andrew Colin Kissa <andrew@topdog.za.net> - 3.7.1-2
- Fixes requested by reviewer

* Tue Jul 20 2010 Andrew Colin Kissa <andrew@topdog.za.net> - 3.7.1-1
- upgraded to latest upstream

* Fri Apr 22 2010 Andrew Colin Kissa <andrew@topdog.za.net> - 3.7-3
- Fix sed error

* Mon Mar 15 2010 Andrew Colin Kissa <andrew@topdog.za.net> - 3.7-2
- Fix the cron entry

* Tue Mar 09 2010 Andrew Colin Kissa <andrew@topdog.za.net> - 3.7-1
- Initial packaging

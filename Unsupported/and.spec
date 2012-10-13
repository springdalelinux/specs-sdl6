Name:      and
Version:   1.2.2
Release:   8%{?dist}
Summary:   Auto nice daemon

License:   GPLv2
Group:     System Environment/Daemons

URL:       http://and.sourceforge.net
Source0:   http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:   and.init
Source2:   and.sysconf 
Patch1:    and-1.2.2-makefile.patch

Buildroot: %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)

Requires(post):  /sbin/chkconfig
Requires(postun):  /sbin/service
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service

%description
The auto nice daemon renices and even kills jobs according to their CPU time,
owner, and command name. This is especially useful on production machines with
lots of concurrent CPU-intensive jobs and users that tend to forget to
nice their jobs.

%prep            
%setup1 -q
%patch1 -p1 -b .org

%build
make %{?_smp_mflags} \
     CFLAGS='%{optflags}' \
     PREFIX=%{_prefix} \
     INSTALL_ETC=%{_sysconfdir} \
     INSTALL_SBIN=%{_sbindir} \
     INSTALL_MAN=%{_mandir}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man8
mkdir -p %{buildroot}%{_mandir}/man5
make PREFIX=%{buildroot}%{_prefix} \
     INSTALL_ETC=%{buildroot}%{_sysconfdir} \
     INSTALL_SBIN=%{buildroot}%{_sbindir} \
     INSTALL_MAN=%{buildroot}%{_mandir} install 

mkdir -p %{buildroot}%{_initrddir}
install -p -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/and

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/and

%clean
rm -rf %{buildroot}

%post
/sbin/chkconfig --add and

%preun
if [ $1 -eq 0 ]; then 
   /sbin/service and stop >/dev/null 2>&1 || :
   /sbin/chkconfig --del and
fi

%postun
if [ $1 -ge 1 ]; then
   /sbin/service and condrestart >/dev/null
fi

%files
%defattr(-,root,root)
%doc README LICENSE CHANGELOG
%config(noreplace) %{_sysconfdir}/and/
%config(noreplace) %{_sysconfdir}/sysconfig/and
%{_sbindir}/*
%attr(0755,root,root) %{_initrddir}/and
%{_mandir}/man5/*.gz
%{_mandir}/man8/*.gz

%changelog
* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 13 2008 Jochen Schmitt <Jochen herr-schmitt de> 1.2.2-6
- Rebuild for gcc-4.3

* Wed Jan 23 2008 Jochen Schmitt <Jochen herr-schmitt de> 1.2.2-5
- Rebuild

* Thu Aug  9 2007 Jochen Schmitt <Jochen herr-schmitt de> 1.2.2-4
- Changing license tag

* Mon Jul 30 2007 Jochen Schmitt <Jochen herr-schmitt de> 1.2.2-3
- Fix wrong postun requires

* Thu Jul 26 2007 Jochen Schmitt <Jochen herr-schmitt de> 1.2.2-2
- Adding sysconfig file template

* Tue Jul 24 2007 Jochen Schmitt <Jochen herr-schmitt de> 1.2.2-1
- Initial package for Fedora

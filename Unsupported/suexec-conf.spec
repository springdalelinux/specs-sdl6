Name:           suexec-conf
Version:        2.2.15
Release:        2%{?dist}
Summary:        Replacement suexec

Group:          System Environment/Daemons
License:        ASL 1.1
URL:            https://github.com/gerasiov/suexec-conf
Source0:        LICENSE
Source1:	README
Source2:	README.suexec+fastcgi+php
Source3:	suexec.c
Source4:	suexec.conf
Source5:	suexec.h
Patch1:		suexec-conf.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  httpd-devel >= 2.2.15 libconfuse-devel
Requires:	libconfuse

%description
A modified suexec that accepts some basic configurations

%prep
%setup -c -T
cp %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE5} .
%patch1 -p0 -b .original

%build
/usr/sbin/apxs -Wc,"%{optflags}" -c -o suexec.lo suexec.c
%{_libdir}/apr-1/build/libtool --silent --mode=link gcc %{optflags} -pie -lconfuse -o suexec suexec.lo

%install
mkdir -p %{buildroot}%{_sbindir}
cp suexec %{buildroot}%{_sbindir}/suexec-conf
mkdir -p %{buildroot}/var/www/suexec
install -m600 %{SOURCE4} %{buildroot}/var/www/suexec/

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE README*
%attr(4510,root,apache) %{_sbindir}/suexec-conf
%dir %attr(750,root,apache) /var/www/suexec
%config(noreplace) %attr(640,root,apache) /var/www/suexec/suexec.conf

%changelog
* Thu Jan 05 2012 Josko Plazonic <plazonic@math.princeton.edu>
- move configs to under /var/www because of selinux issues - easier 
  and safer then allowing suexec to read httpd conf files

* Wed Jan 04 2012 Josko Plazonic <plazonic@math.princeton.edu>
- initial build based on gerasiov's suexec-conf but simpler and
  adapted to suexec from apache 2.2.15

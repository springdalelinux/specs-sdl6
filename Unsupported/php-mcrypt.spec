%global php_apiver      %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%{!?php_extdir:         %{expand: %%global php_extdir %(php-config --extension-dir)}}

%define modname mcrypt

Summary: 	Mcrypt extension module for PHP
Name: 		php-%{modname}
Version: 	5.3.3
Release: 	1%{?dist}
License: 	PHP License
Group: 		Development/Languages

Source: 	php-%{modname}-%{version}.tar.bz2
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:	php-%{modname}
Requires:	php-api = %{php_apiver}
BuildRequires: 	php-devel = %{version}
BuildRequires:	libmcrypt-devel

#%if %{?php_zend_api}0
#Requires:       php(zend-abi) = %{php_zend_api}
#Requires:       php(api) = %{php_core_api}
#%else
#Requires:       php-api = %{php_apiver}
#%endif

%description
This is a dynamic shared object (DSO) for PHP that will add mcrypt support.

This is an interface to the mcrypt library, which supports a wide variety of
block algorithms such as DES, TripleDES, Blowfish (default), 3-WAY, SAFER-SK64,
SAFER-SK128, TWOFISH, TEA, RC2 and GOST in CBC, OFB, CFB and ECB cipher modes
and others.

%prep
%setup -c -q

%build
cd php*/ext/%{modname}
phpize
%configure --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
cd php*/ext/%{modname}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/%{modname}.ini << 'EOF'
; Enable %{modname} module
extension = %{modname}.so

[mcrypt]
;mcrypt.algorithms_dir =
;mcrypt.modes_dir =
EOF

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc php*/ext/%{modname}/CREDITS
%config(noreplace) %{_sysconfdir}/php.d/%{modname}.ini
%{php_extdir}/*so

%changelog
* Mon May 30 2011 Josko Plazonic <plazonic@math.princeton.edu> 5.3.3-1
- update to 5.3.3 version of php mcrypt to match the new 5.3.3 php
  present in rhel6.1

* Mon Feb 14 2011 Thomas Uphill <uphill@ias.edu> 5.3.2-1
- changed php requires to php-api as per php.spec

* Fri Dec 03 2010 Josko Plazonic <plazonic@math.princeton.edu>
- new version for 5.3.2 (rhel6)

* Tue Sep 29 2009 Josko Plazonic <plazonic@math.princeton.edu>
- sources did not change, rebuild for 5.2.10

* Tue Apr 24 2007 Josko Plazonic <plazonic@math.princeton.edu>
- initial build

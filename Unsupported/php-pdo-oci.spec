%global	php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%{!?php_extdir:	%{expand:	%%global php_extdir	%(php-config --extension-dir)}}

Summary:		Provides PDO extension for accessing oracle database
Name:		php-pdo-oci
Version:		5.3.3
Release:		0.2%{?dist}
License:		PHP
Group:			Development/Libraries
Source0:		%{name}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
URL:			http://www.php.net/manual/en/ref.pdo-oci.php
BuildRequires:		php-devel = 5.3.3
BuildRequires:		oracle-instantclient-devel
Requires:		php-pdo = %{version}
%if %{?php_zend_api}0
Requires:		php(zend-abi) = %{php_zend_api}
Requires:		php(api) = %{php_core_api}
%else
Requires:		php-api = %{php_apiver}
%endif

%description
php pdo oci extension

%prep
%setup -q -n pdo_oci
%ifarch x86_64
perl -pi -e 's|/client|/client64|' config.m4
%endif

%build
phpize
D=`ls -d /usr/lib/oracle/1*/client*/lib`
%configure --with-oci8=shared,instantclient,$D --with-pdo-oci=instantclient,/usr,`basename /usr/lib/oracle/1*`
%{__make}

%install
rm -rf %{buildroot}

%{__make} install INSTALL_ROOT=$RPM_BUILD_ROOT

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/pdo_oci.ini << 'EOF'
; Enable pdo_oci extension module
extension=pdo_oci.so
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CREDITS
%{_libdir}/php/modules/*so
%config(noreplace) %{_sysconfdir}/php.d/pdo_oci.ini

%changelog
* Mon Apr 16 2012 Josko Plazonic <plazonic@math.princeton.edu>
- initial build

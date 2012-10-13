%global	php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%{!?php_extdir:	%{expand:	%%global php_extdir	%(php-config --extension-dir)}}

%define	peclName	oci8

Summary:		Provides extension for accessing oracle database
Name:		php-pecl-%peclName
Version:		1.4.7
Release:		2%{?dist}
License:		PHP
Group:			Development/Libraries
Source0:		http://pecl.php.net/get/%peclName-%{version}.tgz
Source1:		%peclName.ini
BuildRoot:	%{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
URL:			http://pecl.php.net/package/%peclName
BuildRequires:		php-devel >= 5.1.3
BuildRequires:		oracle-instantclient-devel
%if %{?php_zend_api}0
Requires:		php(zend-abi) = %{php_zend_api}
Requires:		php(api) = %{php_core_api}
%else
Requires:		php-api = %{php_apiver}
%endif
Provides:		php-pecl(%peclName) = %{version}

%description
This extension allows you to access Oracle databases. It can be built with 
PHP 4.3.9 to 5.x. It can be linked with Oracle 9.2, 10.2, 11.1, or 11.2 
client libraries.

%prep
%setup -q -n %peclName-%{version}

%build
phpize
D=`ls -d /usr/lib/oracle/1*/client*/lib`
%configure --with-oci8=shared,instantclient,$D
%{__make}

%install
rm -rf %{buildroot}

%{__make} install INSTALL_ROOT=$RPM_BUILD_ROOT

install -d %{buildroot}%{_sysconfdir}/php.d/
install -m 0664 %{SOURCE1} %{buildroot}%{_sysconfdir}/php.d/%peclName.ini

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CREDITS README
%{_libdir}/php/modules/%peclName.so
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/php.d/%peclName.ini

%changelog
* Thu Apr 12 2012 Josko Plazonic <plazonic@math.princeton.edu>
- drop pecl dependency

* Tue Apr 10 2012 Josko Plazonic <plazonic@math.princeton.edu>
- initial build of php-oci8

%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}
%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}

%define pecl_name ncurses

Summary:      Terminal screen handling and optimization package
Name:         php-pecl-ncurses
Version:      1.0.1
Release:      1%{?dist}
License:      PHP
Group:        Development/Languages
URL:          http://pecl.php.net/package/ncurses

Source:       http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source2:      xml2changelog

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: php-devel, ncurses-devel, php-pear
Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Obsoletes:    php-ncurses < 5.3.0
Provides:     php-ncurses = 5.3.0
Provides:     php-pecl(%{pecl_name}) = %{version}-%{release}
Requires:     php(zend-abi) = %{php_zend_api}
Requires:     php(api) = %{php_core_api}

%description
ncurses (new curses) is a free software emulation of curses in
System V Rel 4.0 (and above). It uses terminfo format, supports
pads, colors, multiple highlights, form characters and function
key mapping. Because of the interactive nature of this library,
it will be of little use for writing Web applications, but may
be useful when writing scripts meant using PHP from the command
line.



%prep 
%setup -c -q
%{_bindir}/php -n %{SOURCE2} package.xml >CHANGELOG

cd %{pecl_name}-%{version}


%build
cd %{pecl_name}-%{version}
phpize
%configure --enable-ncursesw

%{__make} %{?_smp_mflags}


%install
cd %{pecl_name}-%{version}
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

# Install XML package description
# use 'name' rather than 'pecl_name' to avoid conflict with pear extensions
%{__mkdir_p} %{buildroot}%{pecl_xmldir}
%{__install} -m 644 ../package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%check
cd %{pecl_name}-%{version}
TEST_PHP_EXECUTABLE=$(which php) php run-tests.php \
    -n -q -d extension_dir=modules \
    -d extension=%{pecl_name}.so \


%clean
%{__rm} -rf %{buildroot}


%if 0%{?pecl_install:1}
%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
%endif


%if 0%{?pecl_uninstall:1}
%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%files
%defattr(-, root, root, -)
%doc CHANGELOG %{pecl_name}-%{version}/CREDITS %{pecl_name}-%{version}/example1.php
%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Sat Dec 19 2009 Remi Collet <Fedora@FamilleCollet.com> 1.0.1-1
- update to 1.0.1
- enable wide char support

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009 Remi Collet <Fedora@FamilleCollet.com> 1.0.0-2
- add %%check for minimal test.

* Sun Jul 12 2009 Remi Collet <Fedora@FamilleCollet.com> 1.0.0-1
- initial RPM (for php 5.3.0)
- ncurses-1.0.0-php53.patch 


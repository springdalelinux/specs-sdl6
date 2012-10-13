%global php_apiver	%((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%{!?__pecl:		%{expand: %%global __pecl     %{_bindir}/pecl}}
%{!?php_extdir:		%{expand: %%global php_extdir %(php-config --extension-dir)}}

%define pecl_name perl

Name:		php-pecl-perl
Version:	1.0.0
Release:	1%{?dist}
Summary:	Embedded perl
Group:		Development/Languages
License:	PHP
URL:		http://pecl.php.net/package/%{pecl_name}
Source0:	http://pecl.php.net/get/%{pecl_name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	php-devel php-pear >= 1:1.4.
BuildRequires:	perl(ExtUtils::Embed)
Requires(post):	%{__pecl}
Requires(postun):	%{__pecl}
Provides:	php-pecl(perl) = %{version}

%if %{?php_zend_api}0
Requires:	php(zend-abi) = %{php_zend_api}
Requires:	php(api) = %{php_core_api}
%else
Requires:	php-api = %{php_apiver}
%endif

%description
This extension embeds Perl Interpreter into PHP. It allows execute Perl 
files, evaluate Perl code, access Perl variables and instantiate Perl objects.

%prep
%setup -c -q
cd %{pecl_name}-%{version}
%{__mv} package.xml %{pecl_name}.xml

%build
cd %{pecl_name}-%{version}
phpize
%configure
%{__make} %{?_smp_mflags}

%install
cd %{pecl_name}-%{version}
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot} INSTALL="install -p"

%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/perl.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=perl.so
EOF

%{__mkdir_p} %{buildroot}%{pecl_xmldir}
%{__install} -p -m 644 %{pecl_name}.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%clean
%{__rm} -rf %{buildroot}

%if 0%{?pecl_install:1}
%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
%endif


%if 0%{?pecl_uninstall:1}
%postun
if [ $1 -eq 0 ]; then
%{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif

%files
%defattr(-,root,root,-)
%doc %{pecl_name}-%{version}/CREDITS
%config(noreplace) %{_sysconfdir}/php.d/perl.ini
%{php_extdir}/perl.so
%{pecl_xmldir}/%{name}.xml

%changelog
* Sun Jul 24 2011 Josko Plazonic <plazonic@math.princeton.edu>
- initial build based on php-pecl-lzf rpm

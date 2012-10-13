%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Console_Color

Name:           php-pear-Console-Color
Version:        1.0.3
Release:        3%{?dist}
Summary:        Easily use ANSI console colors from PHP applications
Summary(en_GB): Easily use ANSI console colours from PHP applications

Group:          Development/Libraries
License:        MIT
URL:            http://pear.php.net/package/Console_Color
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2

Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}


%description
The Console_Color class makes it easy to use ANSI color codes from CLI-based
applications written in PHP.

%description -l en_GB
The Console_Color class makes it easy to use ANSI colour codes from CLI-based
applications written in PHP.

%prep
%setup -q -c
# Create a "localized" php.ini to avoid build warning
cp /etc/php.ini .
echo "date.timezone=UTC" >>php.ini

cd %{pear_name}-%{version}
# package.xml is V2
mv ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, nothing required


%install
rm -rf $RPM_BUILD_ROOT
cd %{pear_name}-%{version}
PHPRC=../php.ini %{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%clean
rm -rf $RPM_BUILD_ROOT


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Console/Color.php


%changelog
* Wed Apr 06 2011 Remi Collet <Fedora@FamilleCollet.com> 1.0.3-3
- doc in /usr/share/doc/pear

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct 30 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.0.3-1
- Version 1.0.3 (stable) - API 1.0.0 (stable) - QA release
- set timezone during build
- rename Console_Color.xml to php-pear-Console-Color.xml

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Aug 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0.2-2
- fix license tag

* Sat Jan 27 2006 Tim Jackson <rpm@timj.co.uk> 1.0.2-1
- Update to 1.0.2
- Upstream now includes license file (changed to X11)
- Add en_GB summary/description

* Thu Jan 25 2006 Tim Jackson <rpm@timj.co.uk> 1.0.1-1
- Initial RPM build

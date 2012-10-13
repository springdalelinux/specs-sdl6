%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Console_Table

Name:           php-pear-Console-Table
Version:        1.1.4
Release:        2%{?dist}
Summary:        Class that makes it easy to build console style tables
Summary(fr):    Classe pour fabriquer facilement des tableaux en mode console

Group:          Development/Libraries
License:        BSD
URL:            http://pear.php.net/package/Console_Table
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
Source2:        xml2changelog

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
# For tests
BuildRequires:  php-pear(Console_Color)

Requires:       php-pear(PEAR)
Requires:       php-pear(Console_Color)
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}

%description
Provides methods such as addRow(), insertRow(), addCol() etc. to build
console tables with or without headers and with user defined table rules
and padding.
 
%description -l fr
Fournit les méthodes comme addRow(), insertRow(), addCol() etc.
pour construire des tableaux pour la console, avec ou sans entêtes et 
avec des règles de construction et d'alignement définies par l'utilisateur.

%prep
%setup -q -c
%{_bindir}/php -n %{SOURCE2} package.xml | tee CHANGELOG | head -n 10

# Create a "localized" php.ini to avoid build warning
cp /etc/php.ini .
echo "date.timezone=UTC" >>php.ini

cd %{pear_name}-%{version}
# package.xml is V2
mv ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
rm -rf $RPM_BUILD_ROOT docdir
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


%check
cd %{pear_name}-%{version}
PHPRC=../php.ini %{__pear} \
   run-tests \
   -i "-d include_path=%{buildroot}%{pear_phpdir}:%{pear_phpdir}" \
   tests | tee ../tests.log
# pear doesn't set return code
if grep -q "FAILED TESTS" ../tests.log; then
  for fic in tests/*.diff; do
    cat $fic; echo -e "\n"
  done
  exit 1
fi


%files
%defattr(-,root,root,-)
%doc CHANGELOG 
%{pear_phpdir}/Console/Table.php
%{pear_testdir}/Console_Table
%{pear_xmldir}/%{name}.xml


%changelog
* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 27 2010 Remi Collet <Fedora@FamilleCollet.com> 1.1.4-1
- Version 1.1.4 (stable) - API 1.1.1 (stable) - QA release
- set timezone during build
- run tests in %%check

* Fri May 21 2010 Remi Collet <Fedora@FamilleCollet.com> 1.1.3-4
- spec cleanup
- rename Console_Table.xml to php-pear-Console-Table.xml

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Oct 21 2008 Remi Collet <Fedora@FamilleCollet.com> 1.1.3-1
- update to 1.1.3
- Requires php-pear-Console-Color
- cleanup old fixe.

* Sun Jul 27 2008 Remi Collet <Fedora@FamilleCollet.com> 1.1.2-1
- update to 1.1.2

* Thu Apr 10 2008 Remi Collet <Fedora@FamilleCollet.com> 1.1.1-1
- update to 1.1.1

* Sun Mar 30 2008 Remi Collet <Fedora@FamilleCollet.com> 1.1.0-1
- update to 1.1.0

* Wed Jan 09 2008 Remi Collet <Fedora@FamilleCollet.com> 1.0.8-1
- update to 1.0.8
- fix tests, http://pear.php.net/bugs/bug.php?id=12863
- add %%check
- fixed xml2changelog

* Sat May 02 2007 Remi Collet <Fedora@FamilleCollet.com> 1.0.7-1
- update to 1.0.7

* Sat Jan 20 2007 Remi Collet <Fedora@FamilleCollet.com> 1.0.6-1
- update to 1.0.6
- add CHANGELOG (generated)

* Tue Sep 13 2006 Remi Collet <Fedora@FamilleCollet.com> 1.0.5-2.fc5.1
- FC5 rebuild

* Mon Sep 11 2006 Remi Collet <Fedora@FamilleCollet.com> 1.0.5-2
- don't own %%{pear_phpdir}/Console

* Sat Sep 09 2006 Remi Collet <Fedora@FamilleCollet.com> 1.0.5-1
- generated specfile (pear make-rpm-spec) + cleaning
- add french summary and description

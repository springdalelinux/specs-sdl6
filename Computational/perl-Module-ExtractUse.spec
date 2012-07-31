Name:           perl-Module-ExtractUse
Version:        0.23
Release:        3%{?dist}
Summary:        Find out what modules are used
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Module-ExtractUse/
Source0:        http://www.cpan.org/modules/by-module/Module/Module-ExtractUse-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Parse::RecDescent) >= 1.94
BuildRequires:  perl(Pod::Strip) >= 1.00
BuildRequires:  perl(Test::Deep) >= 0.087
BuildRequires:  perl(Test::NoWarnings)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(UNIVERSAL::require)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Module::ExtractUse is basically a Parse::RecDescent grammar to parse Perl
code. It tries very hard to find all modules (whether pragmas, Core, or
from CPAN) used by the parsed code.

%prep
%setup -q -n Module-ExtractUse-%{version}

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
rm -rf $RPM_BUILD_ROOT

./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
./Build test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README TODO
%dir %{perl_vendorlib}/Module
%{perl_vendorlib}/Module/ExtractUse.pm
%dir %{perl_vendorlib}/Module/ExtractUse/
%{perl_vendorlib}/Module/ExtractUse/Grammar.pm
%{_mandir}/man3/*.3pm*

%changelog
* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep  5 2008 Daniel P. Berrange <berrange@redhat.com> - 0.23-1
- Update to 0.23 release

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.22-2
- rebuild for new perl

* Fri Dec 21 2007 Daniel P. Berrange <berrange@redhat.com> 0.22-1.fc9
- Specfile autogenerated by cpanspec 1.73.
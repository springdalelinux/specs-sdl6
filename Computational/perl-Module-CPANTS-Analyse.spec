Name:           perl-Module-CPANTS-Analyse
Version:        0.85
Release:        5%{?dist}
Summary:        Generate Kwalitee ratings for a distribution
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Module-CPANTS-Analyse/
Source0:        http://www.cpan.org/authors/id/C/CH/CHORNY/Module-CPANTS-Analyse-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(Archive::Any) >= 0.06
BuildRequires:  perl(Archive::Tar) >= 1.30
BuildRequires:  perl(Array::Diff) >= 0.04
BuildRequires:  perl(Class::Accessor) >= 0.19
BuildRequires:  perl(CPAN::DistnameInfo) >= 0.06
BuildRequires:  perl(IO::Capture) >= 0.05
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Module::ExtractUse) >= 0.18
BuildRequires:  perl(Module::Pluggable) >= 2.96
BuildRequires:  perl(Pod::Simple::Checker) >= 2.02
BuildRequires:  perl(Test::YAML::Meta::Version) >= 0.11
BuildRequires:  perl(version) >= 0.73
BuildRequires:  perl(YAML::Syck) >= 0.95
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Test::Warn)
BuildRequires:  perl(Test::NoWarnings)
BuildRequires:  perl(File::Find::Rule)
BuildRequires:  perl(Readonly)
BuildRequires:  perl(List::MoreUtils)
BuildRequires:  perl(File::Slurp)
BuildRequires:  perl(LWP::Simple)
BuildRequires:  perl(Software::License)
BuildRequires:  perl(Text::CSV_XS)
Requires:       perl(Archive::Any) >= 0.06
Requires:       perl(Archive::Tar) >= 1.30
Requires:       perl(Array::Diff) >= 0.04
Requires:       perl(Class::Accessor) >= 0.19
Requires:       perl(CPAN::DistnameInfo) >= 0.06
Requires:       perl(IO::Capture) >= 0.05
Requires:       perl(Module::ExtractUse) >= 0.18
Requires:       perl(Module::Pluggable) >= 2.96
Requires:       perl(Pod::Simple::Checker) >= 2.02
Requires:       perl(Test::YAML::Meta::Version) >= 0.11
Requires:       perl(version) >= 0.73
Requires:       perl(YAML::Syck) >= 0.95
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
CPANTS is an acronym for CPAN Testing Service. The goals 
of the CPANTS project are to provide some sort of quality
measure (called "Kwalitee") and lots of metadata for all 
distributions on CPAN.

%prep
%setup -q -n Module-CPANTS-Analyse-%{version}

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
%dir %{perl_vendorlib}/Module/CPANTS
%{perl_vendorlib}/Module/CPANTS/Analyse.pm
%{perl_vendorlib}/Module/CPANTS/Kwalitee.pm
%dir %{perl_vendorlib}/Module/CPANTS/Kwalitee/
%{perl_vendorlib}/Module/CPANTS/Kwalitee/*.pm
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3pm*
%{_bindir}/cpants_lint.pl

%changelog
* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.85-5
- Mass rebuild with perl-5.12.0

* Tue Jan 12 2010 Daniel P. Berrange <berrange@redhat.com> - 0.85-4
- Fix source URL

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.85-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.85-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Daniel P. Berrange <berrange@redhat.com> - 0.85-1
- Update to 0.85 release

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.82-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Oct  3 2008 Daniel P. Berrange <berrange@redhat.com> - 0.82-2
- Added more new & missing BRs

* Fri Sep  5 2008 Daniel P. Berrange <berrange@redhat.com> - 0.82-1
- Update to 0.82 release

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.75-3
- rebuild for new perl

* Wed Dec 26 2007 Daniel P. Berrange <berrange@redhat.com> 0.75-2.fc9
- Added Test::Deep, Test::Pod, Test::Pod::Coverage build requires

* Fri Dec 21 2007 Daniel P. Berrange <berrange@redhat.com> 0.75-1.fc9
- Specfile autogenerated by cpanspec 1.73.
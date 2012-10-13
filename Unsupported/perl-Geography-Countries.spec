Name:           perl-Geography-Countries
Version:        2009041301
Release:        1%{?dist}
Summary:        2-letter, 3-letter, and numerical codes for countries
Group:          Development/Libraries
License:        MIT
URL:            http://search.cpan.org/dist/Geography-Countries/
Source0:        http://search.cpan.org/CPAN/authors/id/A/AB/ABIGAIL/Geography-Countries-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  perl(ExtUtils::MakeMaker), perl(Test::More)
BuildArch:      noarch
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module maps country names, and their 2-letter, 3-letter and numerical 
codes, as defined by the ISO-3166 maintenance agency, and defined by the UNSD.

%prep
%setup -q -n Geography-Countries-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{perl_vendorlib}/Geography
%{_mandir}/man3/*.3*

%changelog
* Tue Jun 29 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2009041301-1
- oh perl, you and your wacky versions. updating to *BARF*

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.4-7
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.4-6
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.4-3
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.4-2
- rebuild for new perl

* Mon Apr  2 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.4-1
- Initial package for Fedora

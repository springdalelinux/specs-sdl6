Name:           perl-Data-Section
Version:        0.101620
Release:        2%{?dist}
Summary:        Read multiple hunks of data out of your DATA section
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Data-Section/
Source0:        http://www.cpan.org/authors/id/R/RJ/RJBS/Data-Section-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Sub::Exporter) >= 0.979
BuildRequires:  perl(Test::More)
BuildRequires:  perl(MRO::Compat)
Requires:       perl(Sub::Exporter) >= 0.979
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Data::Section provides an easy way to access multiple named chunks of line-
oriented data in your module's DATA section. It was written to allow
modules to store their own templates, but probably has other uses.

%prep
%setup -q -n Data-Section-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Wed Jun 30 2010 Mark Chappell <tremble@fedoraproject.org> - 0.101620-2
- Add in missing BuildRequires MRO::Compat

* Wed Jun 30 2010 Mark Chappell <tremble@fedoraproject.org> - 0.101620-1
- Update for release 0.101620

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.093410-3
- Mass rebuild with perl-5.12.0

* Tue Jan 12 2010 Daniel P. Berrange <berrange@redhat.com> - 0.093410-2
- Fix source URL

* Thu Jan  7 2010 Daniel P. Berrange <berrange@redhat.com> - 0.093410-1
- Update to 0.093410 release

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.091820-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.091820-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Daniel P. Berrange <berrange@redhat.com> - 0.091820-1
- Update to 0.091820 release

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.005-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Sep 06 2008 Daniel P. Berrange <berrange@redhat.com> 0.005-2
- Add Test::More BR

* Fri Sep 05 2008 Daniel P. Berrange <berrange@redhat.com> 0.005-1
- Specfile autogenerated by cpanspec 1.77.

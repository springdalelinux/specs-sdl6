Name:           perl-IO-Capture
Version:        0.05
Release:        5%{?dist}
Summary:        Abstract Base Class to build modules to capture output

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/IO-Capture/
Source0:        http://www.cpan.org/authors/id/R/RE/REYNOLDS/IO-Capture-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
The IO::Capture Module defines an abstract base class that can be used
to create any number of useful sub-classes that capture output being
sent on a filehandle such as STDOUT or STDERR.


%prep
%setup -q -n IO-Capture-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


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
%doc BUGS Changes README
%{perl_vendorlib}/IO/
%{_mandir}/man3/*.3pm*


%changelog
* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.05-3
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.05-2.2
- add BR: perl(Test::More)

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.05-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Sun Dec 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.05-2
- find: fixed arguments order (#219956).

* Sun Dec 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.05-1
- First build.

Name:           perl-Pod-Strip
Version:        1.02
Release:        5%{?dist}
Summary:        Remove POD from Perl code

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Pod-Strip/
Source0:        http://www.cpan.org/authors/id/D/DO/DOMM/Pod-Strip-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Pod::Simple) >= 3.00
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Pod::Simple) >= 3.00

%description
Pod::Strip is a subclass of Pod::Simple that strips all POD from Perl Code.


%prep
%setup -q -n Pod-Strip-%{version}


%build
%{__perl} Build.PL installdirs=vendor
./Build


%install
rm -rf $RPM_BUILD_ROOT
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
chmod -R u+w $RPM_BUILD_ROOT/*


%check
./Build test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/Pod/
%{_mandir}/man3/*.3pm*


%changelog
* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.02-3
- rebuild for new perl

* Sun May  6 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.02-2
- Added missing requirement: perl(Pod::Simple) (see bug #239241).

* Sun Dec 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.02-1
- First build.

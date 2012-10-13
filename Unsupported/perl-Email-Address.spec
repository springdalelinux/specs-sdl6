Name:           perl-Email-Address
Version:        1.889
Release:        3%{?dist}
Summary:        RFC 2822 Address Parsing and Creation

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Email-Address/
Source0:        http://www.cpan.org/authors/id/R/RJ/RJBS/Email-Address-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.08
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This class implements a complete RFC 2822 parser that locates email
addresses in strings and returns a list of "Email::Address" objects
found. Alternatley you may construct objects manually. The goal of this
software is to be correct, and very very fast.


%prep
%setup -q -n Email-Address-%{version}
%{__perl} -pi -e 's|^#!/usr/local/bin/perl\b|#!%{__perl}|' bench/ea-vs-ma.pl


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
%doc Changes LICENSE README bench/
%{perl_vendorlib}/Email/
%{_mandir}/man3/*.3pm*


%changelog
* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.889-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.889-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 12 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.889-1
- Upstream update.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.888-3
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.888-2
- rebuild for new perl

* Sat Jun 23 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.888-1
- Update to 1.888.

* Thu Apr  5 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.887-1
- Update to 1.887.

* Sun Mar 18 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.886-1
- Update to 1.886.

* Tue Dec 12 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.884-1
- Update to 1.884.

* Sat Nov 25 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.883-1
- Update to 1.883.

* Wed Nov 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.882-1
- Update to 1.882.

* Sat Nov 11 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.880-1
- Update to 1.880.

* Fri Oct 13 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.871-1
- Update to 1.871.

* Sat Aug 12 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.870-1
- Update to 1.870.

* Sat Jul 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.86-1
- Update to 1.86.

* Tue Jul 11 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.85-1
- Update to 1.85.

* Thu Sep 08 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.80-1
- First build.

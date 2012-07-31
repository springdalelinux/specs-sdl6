Name:           perl-Log-Log4perl
Version:        1.30
Release:        1%{?dist}
Summary:        Log4j implementation for Perl
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Log-Log4perl/
Source0:        http://www.cpan.org/authors/id/M/MS/MSCHILLI/Log-Log4perl-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec) >= 0.82
BuildRequires:  perl(Test::More) >= 0.45

# Tests
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(IO::Socket::INET)
# Optional tests
BuildRequires:  perl(DBD::CSV)
BuildRequires:  perl(DBI)
BuildRequires:  perl(Log::Dispatch)
BuildRequires:  perl(Log::Dispatch::FileRotate)
BuildRequires:  perl(RRDs)
BuildRequires:  perl(SQL::Statement)
BuildRequires:  perl(XML::DOM)

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Log::Log4perl lets you remote-control and fine-tune the logging
behavior of your system from the outside. It implements the widely
popular (Java-based) Log4j logging package in pure Perl.

%prep
%setup -q -n Log-Log4perl-%{version}
find lib -name "*.pm" -exec chmod -c a-x {} ';'
%{__perl} -pi -e 's|^#!/usr/local/bin/perl|#!%{__perl}|' eg/newsyslog-test eg/benchmarks/simple

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test L4P_ALL_TESTS=1


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_bindir}/*


%changelog
* Wed Sep 08 2010 Petr Pisar <ppisar@redhat.com> - 1.30-1
- 1.30 bump
- l4p-tmpl executable added
- Add BuildRequires for tests
- Spelling in package description corrected

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.24-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.24-2
- rebuild against perl 5.10.1

* Thu Aug 06 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.24-1
- Fix mass rebuild breakdown: Upgrade to upstream 1.24.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 20 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.20-1
- Upstream update.
- Reactivate testsuite.
- Remove examples (eg, ldap) from %%doc.
- Don't chmod -x eg/*.
- Remove BR: perl(IPC::Shareable).

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.13-2
- rebuild for new perl

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.13-1.1
- disable tests

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.13-1
- bump to 1.13

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12-1.2
- add BR: perl(Test::More)

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Fri Jun 29 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.12-1
- Update to 1.12.

* Thu Jun  7 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.11-1
- Update to 1.11.

* Thu Apr  5 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.10-1
- Update to 1.10.

* Sun Feb 11 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.09-1
- Update to 1.09.

* Sat Nov 25 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.08-1
- Update to 1.08.

* Sat Oct 21 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.07-1
- Update to 1.07.

* Fri Jul 21 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.06-1
- Update to 1.06.

* Sun Jun 18 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.05-1
- Update to 1.05.

* Tue Apr 25 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.04-2
- Log::Dispatch::FileRotate is no longer excluded due to licensing
  problems (the package now includes copyright information).

* Mon Mar  6 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.04-1
- Update to 1.04.

* Mon Feb 27 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.03-3
- Rebuild for FC5 (perl 5.8.8).

* Thu Feb  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.03-2
- Added a couple of comments as suggested by Paul Howarth (#176137).

* Tue Feb  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.03-1
- Update to 1.03.
- Disabled the Log::Dispatch::FileRotate requirement (see #171640).

* Mon Dec 19 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.02-1
- Update to 1.02.

* Sat Oct 22 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.01-1
- Update to 1.01.

* Sun Sep 11 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.00-1
- First build.

Name:           perl-SQL-Statement
Version:        1.27
Release:        1%{?dist}
Summary:        SQL parsing and processing engine

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/SQL-Statement/
Source0:        http://www.cpan.org/authors/id/R/RE/REHSACK/SQL-Statement-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::Simple) >= 0.86
BuildRequires:  perl(Clone) >= 0.30
BuildRequires:  perl(Params::Util) >= 1.00
# for tests only:
BuildRequires:  perl(DBD::CSV)
BuildRequires:  perl(DBD::File) >= 0.37
BuildRequires:  perl(DBD::XBase)

%description
The SQL::Statement module implements a pure Perl SQL parsing and execution
engine.  While it by no means implements full ANSI standard, it does support
many features including column and table aliases, built-in and user-defined
functions, implicit and explicit joins, complexly nested search conditions, and
other features.


%prep
%setup -q -n SQL-Statement-%{version}
find  -type f -perm /111 | xargs chmod -c a-x
%{__perl} -pi -e 's/\r\n/\n/' README


%build
export SQL_STATEMENT_WARN_UPDATE=sure
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/SQL/
%{_mandir}/man3/*.3pm*


%changelog
* Tue Jun  8 2010 Petr Pisar <ppisar@redhat.com> - 1.27-1
- 1.27 bump (do not backport, 1.22 lower-cases unqouted identifiers)
- Make tests fatal again

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.20-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.20-2
- rebuild against perl 5.10.1

* Wed Sep 23 2009 Stepan Kasal <skasal@redhat.com> - 1.20-1
- new upstream version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.15-4
- Rebuild for perl 5.10 (again)

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.15-3
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.15-2.2
- add BR: perl(Test::More)

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.15-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Sep  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.15-2
- Rebuild for FC6.

* Fri Feb 24 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.15-1
- Update to 1.15.

* Mon Feb 20 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.14-2
- Rebuild for FC5 (perl 5.8.8).

* Sun Sep 11 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.14-1
- First build.

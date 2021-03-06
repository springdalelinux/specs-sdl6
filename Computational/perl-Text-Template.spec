Name:           perl-Text-Template
Version:        1.45
Release:        3%{?dist}
Summary:        Expand template text with embedded Perl

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Text-Template/
Source0:        http://www.cpan.org/authors/id/M/MJ/MJD/Text-Template-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This is a library for generating form letters, building HTML pages, or
filling in templates generally.  A 'template' is a piece of text that
has little Perl programs embedded in it here and there.  When you
'fill in' a template, you evaluate the little programs and replace
them with their values.


%prep
%setup -q -n Text-Template-%{version}


%build
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
%doc Artistic COPYING README
%{perl_vendorlib}/Text/
%{_mandir}/man3/*.3pm*


%changelog
* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.45-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.45-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Apr 23 2008 Ralf Corsépius <rc040203@freenet.de> - 1.45-1
- Upstream update.
- Abandon perl-Text-Template-perl510-fixtest09.patch.

* Thu Feb  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.44-6
- fix test 09 for perl5.10

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.44-5
- rebuild for new perl

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.44-4.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Sep  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.44-4
- Rebuild for FC6.

* Thu Feb 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.44-3
- Rebuild for FC5 (perl 5.8.8).

* Thu Aug 25 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.44-2
- Removed the explicit perl build requirement.

* Wed Aug 10 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.44-1
- Update to Fedora Extras template.

* Sat Dec 18 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.44-0.fdr.1
- First build.

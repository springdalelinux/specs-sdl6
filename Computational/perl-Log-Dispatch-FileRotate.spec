Name:           perl-Log-Dispatch-FileRotate
Version:        1.19
Release:        4%{?dist}
Summary:        Log to files that archive/rotate themselves

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Log-Dispatch-FileRotate/
Source0:        http://www.cpan.org/authors/id/M/MA/MARKPF/Log-Dispatch-FileRotate-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Date::Manip)
BuildRequires:  perl(Log::Dispatch)
BuildRequires:  perl(ExtUtils::MakeMaker)
# See comment in the %%check section
%{?_with_tests:BuildRequires:  perl(Log::Log4perl) >= 1.0}
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module provides a simple object for logging to files under the
Log::Dispatch::* system, and automatically rotating them according to
different constraints. This is basically a Log::Dispatch::File wrapper
with additions.


%prep
%setup -q -n Log-Dispatch-FileRotate-%{version}


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
# Test suite disabled: circular dependencies with Log::Log4perl
%{?_with_tests:make test}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/Log/Dispatch/
%{_mandir}/man3/*.3pm*


%changelog
* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Oct 26 2008 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.19-1
- Upstream update.

* Fri Jun 27 2008 Ralf Corsépius <rc040203@freenet.de> - 1.18-1
- Upstream update.
- Add --with-tests.

* Tue Jun 03 2008 Ralf Corsépius <rc040203@freenet.de> - 1.16-3
- Use %%%%check in comments to work-around rpm bogusly parsing 
  %%check in comments (BZ 449419).

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.16-2
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.16-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Sat Nov 25 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.16-1
- Update to 1.16.

* Wed Apr 26 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.15-1
- Update to 1.15.
- The author corrected the licensing terms (License: GPL+ or Artistic).

* Mon Apr 24 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.14-1
- Update to 1.14.
- License: Artistic.

* Mon Apr 24 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.13-2
- The license is: GPL+ or Artistic.
  License information: http://rt.cpan.org/Public/Bug/Display.html?id=14563.

* Sun Sep 11 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.13-1
- First build.

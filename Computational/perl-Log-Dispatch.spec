# Build switch:
#   --with mailtests         Enable mail tests

%define mailtests      0

%{?_with_mailtests:%define mailtests 1}

Name:           perl-Log-Dispatch
Version:        2.27
Release:        1%{?dist}
Summary:        Dispatches messages to one or more outputs
Group:          Development/Libraries
License:        Artistic 2.0
URL:            http://search.cpan.org/dist/Log-Dispatch/
Source0:        http://www.cpan.org/authors/id/D/DR/DROLSKY/Log-Dispatch-%{version}.tar.gz
Patch0:         Log-Dispatch-2.11-enable-mail-tests.patch
BuildArch:      noarch
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Params::Validate)
%if %{mailtests}
BuildRequires:  perl(Mail::Send), perl(Mail::Sender)
BuildRequires:  perl(Mail::Sendmail), perl(MIME::Lite)
%endif
BuildRequires:  perl(File::Find::Rule)
BuildRequires:  perl(Apache2::Log)
BuildRequires:  perl(Sys::Syslog) >= 0.16

# for improved tests
BuildRequires:  perl(Test::Kwalitee)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Log::Dispatch is a suite of OO modules for logging messages to
multiple outputs, each of which can have a minimum and maximum log
level.  It is designed to be easily subclassed, both for creating a
new dispatcher object and particularly for creating new outputs.

%prep
%setup -q -n Log-Dispatch-%{version}
%if %{mailtests}
%patch0 -p1
%endif

# Requirements list: exclude mod_perl
cat <<__EOF__ > %{name}-perlreq
#!/bin/sh
/usr/lib/rpm/perl.req \$* | grep -v 'perl(Apache'
__EOF__
%define __perl_requires %{_builddir}/Log-Dispatch-%{version}/%{name}-perlreq
chmod +x %{__perl_requires}

%build
%{__perl} Makefile.PL installdirs=vendor
make

%install
make install DESTDIR=$RPM_BUILD_ROOT create_packlist=0
chmod -R u+w $RPM_BUILD_ROOT/*

# Delete unnecessary files.
rm -rf $RPM_BUILD_ROOT%{perl_vendorarch}/auto/
rm -rf $RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod

%check
IS_MAINTAINER=1 make test

%files
%defattr(-,root,root,-)
%doc Changes LICENSE README
%{perl_vendorlib}/Log/
%{_mandir}/man3/*.3pm*

%changelog
* Wed Nov 03 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.27-1
- update to 2.27

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.22-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.22-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.22-2
- BR: perl(Test::Kwalitee).

* Wed Nov 26 2008 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.22-1
- Upstream update.

* Fri Mar 14 2008 Ralf Corsépius <rc040203@freenet.de> - 2.21-1
- Upstream update.
- BR: perl(Apache2::Log) instead of mod_perl.
- Add BR: Test::Pod::Coverage, activate IS_MAINTAINER checks.

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.20-2
- rebuild for new perl

* Wed Dec 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.20-1
- bump to 2.20

* Sat Jun  9 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.18-1
- Update to 2.18.

* Wed Dec 20 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.16-1
- Update to 2.16.
- Removed perl(IO::String) from the BR list (no longer needed).

* Sat Dec 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.15-2
- New build requirement: perl(IO::String).

* Sat Dec 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.15-1
- Update to 2.15.

* Sat Nov 25 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.14-2
- Log-Dispatch-2.11-mod_perl2.patch no longer needed.

* Sat Nov 25 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.14-1
- Update to 2.14.

* Tue Sep 26 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.13-1
- Update to 2.13.

* Wed Aug  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.12-1
- Update to 2.12.

* Wed Feb 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.11-4
- Rebuild for FC5 (perl 5.8.8).

* Thu Sep 22 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.11-3
- Exclude mod_perl from the requirements list
  (overkill for most applications using Log::Dispatch).

* Mon Sep 12 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.11-2
- Better mod_perl handling.

* Fri Sep 09 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.11-1
- First build.

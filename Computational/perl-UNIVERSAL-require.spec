Name:           perl-UNIVERSAL-require
Version:        0.13
Release:        1%{?dist}
Summary:        Require() modules from a variable
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/UNIVERSAL-require/
Source0:        http://search.cpan.org/CPAN/authors/id/M/MS/MSCHWERN/UNIVERSAL-require-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Test::More)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
%{summary}.

%prep
%setup -q -n UNIVERSAL-require-%{version}

cat << \EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} $* |\
    sed -e '/^perl(UNIVERSAL)$/d'
EOF
%define __perl_provides %{_builddir}/UNIVERSAL-require-%{version}/%{name}-prov
chmod +x %{__perl_provides}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make

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
%doc Changes
%{perl_vendorlib}/UNIVERSAL
%{_mandir}/man3/*.3*


%changelog
* Wed Oct  7 2009 Marcela Mašláňová <mmaslano@redhat.com> - 0.13-1
- update to new upstream release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.11-4
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.11-3
- rebuild for new perl

* Sun Aug 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.11-2
- license tag fix

* Wed Jan 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.11-1
- bump to 0.11

* Mon Sep 11 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.10-2
- get rid of false provide

* Mon Sep  4 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.10-1
- initial package for Fedora

Name:           perl-HTML-Lint
Version:        2.06
Release:        4%{?dist}
Summary:        HTML::Lint Perl module
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/HTML-Lint/
Source0:        http://www.cpan.org/authors/id/P/PE/PETDANCE/HTML-Lint-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(HTML::Parser) >= 3.20
BuildRequires:  perl(HTML::Tagset) >= 3.03
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::More)

# For improved testing
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
BuildRequires:  perl(Test::Pod) >= 1.14

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# Convenience to users looking for weblint
Provides:       weblint = %{version}-%{release}

%description
HTML::Lint Perl module, a pure-Perl HTML parser and checker for syntactic
legitmacy.

%prep
%setup -q -n HTML-Lint-%{version}

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
%doc Changes README
%{_bindir}/weblint
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Ralf Corsépius <corsepiu@fedoraproject.org> 2.06-1
- Initial Fedora submission.

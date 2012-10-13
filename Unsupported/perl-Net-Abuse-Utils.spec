Name:           perl-Net-Abuse-Utils
Version:        0.11
Release:        1%{?dist}
Summary:        Routines useful for processing network abuse
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Net-Abuse-Utils/
Source0:        http://www.cpan.org/authors/id/M/MI/MIKEGRB/Net-Abuse-Utils-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl >= 0:5.006
BuildRequires:  perl(Email::Address)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Net::DNS)
BuildRequires:  perl(Net::Whois::IP)
Requires:       perl(Email::Address)
Requires:       perl(Net::DNS)
Requires:       perl(Net::Whois::IP)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Net::Abuse::Utils provides several functions useful for determining
information about an IP address including contact/reporting addresses,
ASN/network info, reverse dns, and DNSBL listing status.

%prep
%setup -q -n Net-Abuse-Utils-%{version}

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
#make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue Apr 03 2012 Brian Epstein 0.11-1
- Specfile autogenerated by cpanspec 1.78.

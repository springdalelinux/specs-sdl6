Name:           perl-Net-SNMP
Version:        5.2.0
Release:        4%{?dist}
Summary:        Object oriented interface to SNMP

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Net-SNMP/
Source0:        http://www.cpan.org/authors/id/D/DT/DTOWN/Net-SNMP-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Crypt::DES)
BuildRequires:  perl(Digest::HMAC)
BuildRequires:  perl(Digest::SHA1)
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
#Requires:       perl(Crypt::Rijndael)
#Requires:       perl(Socket6)

%description
The Net::SNMP module implements an object oriented interface to the
Simple Network Management Protocol.  Perl applications can use the
module to retrieve or update information on a remote host using the
SNMP protocol.  The module supports SNMP version-1, SNMP version-2c
(Community-Based SNMPv2), and SNMP version-3.  The Net::SNMP module
assumes that the user has a basic understanding of the Simple Network
Management Protocol and related network management concepts.


%prep
%setup -q -n Net-SNMP-%{version}
%{__perl} -pi -e 's|^#!\s+/usr/local/bin/perl|#!%{__perl}|' examples/*.pl
chmod -c a-x examples/*.pl

# Requirements: exclude perl(Socket6)
cat <<__EOF__ > %{name}-perlreq
#!/bin/sh
/usr/lib/rpm/perl.req \$* | grep -v '^perl(Socket6)'
__EOF__
%define __perl_requires %{_builddir}/Net-SNMP-%{version}/%{name}-perlreq
chmod +x %{__perl_requires}


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
%doc Changes README examples/
%{_bindir}/*
%{perl_vendorlib}/Net/
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3pm*


%changelog
* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.2.0-2
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 5.2.0-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Sat May 13 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 5.2.0-1
- First build.

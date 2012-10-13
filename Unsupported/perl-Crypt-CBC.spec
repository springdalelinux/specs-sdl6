Summary: Encrypt Data with Cipher Block Chaining Mode
Name: perl-Crypt-CBC
Version: 2.29
Release: 3%{?dist}
# Upstream confirms that they're under the same license as perl.
# Wording in CBC.pm is less than clear, but still.
License: GPL+ or Artistic
Group: Development/Libraries
URL: http://search.cpan.org/dist/Crypt-CBC/
Source0: http://search.cpan.org/CPAN/authors/id/L/LD/LDS/Crypt-CBC-%{version}.tar.gz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires: perl(ExtUtils::MakeMaker)

%description
This is Crypt::CBC, a Perl-only implementation of the cryptographic
cipher block chaining mode (CBC).  In combination with a block cipher
such as Crypt::DES or Crypt::IDEA, you can encrypt and decrypt
messages of arbitrarily long length.  The encrypted messages are
compatible with the encryption format used by SSLeay.

%prep
%setup -q -n Crypt-CBC-%{version}
chmod 644 eg/*.pl

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
%doc Changes README eg/
%{perl_vendorlib}/Crypt/
%{_mandir}/man3/*.3*

%changelog
* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jul 11 2008 Tom "spot" Callawau <tcallawa@redhat.com> - 2.29-1
- update to 2.29

* Mon Mar  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.22-3
- work around buildsystem burp

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.22-2
- rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.22-1.1
- add BR: perl(ExtUtils::MakeMaker)

* Wed Feb 07 2007 Andreas Thienemann <andreas@bawue.net> - 2.22-1
- Upgrade to 2.22

* Fri Sep 08 2006 Andreas Thienemann <andreas@bawue.net> - 2.19-1
- Upgrade to 2.19

* Fri Feb 24 2006 Andreas Thienemann <andreas@bawue.net> - 2.17-1
- Upgrade to 2.17

* Thu Jul 14 2005 Andreas Thienemann <andreas@bawue.net> - 2.14-2
- Remove execute permissions from example files

* Thu Jul 14 2005 Andreas Thienemann <andreas@bawue.net> - 2.14-1
- Initial package


Name:           perl-Archive-Any
Version:        0.0932
Release:        2%{?dist}
Summary:        Single interface to deal with file archives
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Archive-Any/
Source0:        http://search.cpan.org/CPAN/authors/id/C/CM/CMOORE/Archive-Any-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# core
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(Test::More) >= 0.4
# cpan
BuildRequires:  perl(Archive::Tar) >= 0.22
BuildRequires:  perl(Archive::Zip) >= 1.07
BuildRequires:  perl(File::MMagic) >= 1.27
BuildRequires:  perl(MIME::Types) >= 1.16
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Module::Find) >= 0.05
# testing
BuildRequires:  perl(Test::Pod), perl(Test::Pod::Coverage)
BuildRequires:  perl(Test::Perl::Critic)
BuildRequires:  perl(Test::Warn)

#Requires:       perl(Archive::Tar) >= 0.22
#Requires:       perl(Archive::Zip) >= 1.07
#Requires:       perl(File::MMagic) >= 1.27
#Requires:       perl(MIME::Types) >= 1.16
#Requires:       perl(Module::Find) >= 0.05

%description
This module is a single interface for manipulating different archive
formats. Tarballs, zip files, etc.

%prep
%setup -q -n Archive-Any-%{version}

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
rm -rf %{buildroot}

./Build install destdir=%{buildroot} create_packlist=0
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check
./Build test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README t/
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0932-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 07 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.0932-1
- auto-update to 0.0932 (by cpan-spec-update 0.01)
- altered br on perl(Test::More) (0 => 0.4)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.093-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 08 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.093-3
- rebuild for new perl

* Wed May 09 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.093-2
- bump

* Sat May 05 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.093-1
- Specfile autogenerated by cpanspec 1.71.

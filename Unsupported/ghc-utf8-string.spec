%global pkg_name utf8-string

%global common_summary Haskell UTF8 layer for IO and Strings

%global common_description The utf8-string package provides operations\
for encoding UTF8 strings to Word8 lists and back, and for reading and writing\
UTF8 without truncation. 

%bcond_without shared

# debuginfo is not useful for ghc
%global debug_package %{nil}

Name:           ghc-%{pkg_name}
Version:        0.3.6
Release:        5%{?dist}
Summary:        %{common_summary}

Group:          System Environment/Libraries
License:        BSD
URL:            http://hackage.haskell.org/cgi-bin/hackage-scripts/package/%{pkg_name}
Source0:        http://hackage.haskell.org/packages/archive/%{pkg_name}/%{version}/%{pkg_name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# fedora ghc archs:
ExclusiveArch:  %{ix86} x86_64 ppc alpha
BuildRequires:  ghc, ghc-doc, ghc-prof
BuildRequires:  ghc-rpm-macros >= 0.8.1
BuildRequires:  hscolour
BuildRequires:  ghc-hscolour

%description
%{common_description}
%if %{with shared}
This package provides the shared library.
%endif


%prep
%setup -q -n %{pkg_name}-%{version}


%build
%ghc_lib_build


%install
rm -rf $RPM_BUILD_ROOT
%ghc_lib_install


%clean
rm -rf $RPM_BUILD_ROOT


%ghc_lib_package -o 0.3.6-5


%changelog
* Sat Sep  4 2010 Jens Petersen <petersen@redhat.com> - 0.3.6-5
- update to latest macros, hscolour and drop doc pkg (cabal2spec-0.22.2)

* Wed Jun 23 2010 Jens Petersen <petersen@redhat.com> - 0.3.6-4
- use ghc_strip_dynlinked (ghc-rpm-macros-0.6.0)

* Tue Apr 27 2010 Jens Petersen <petersen@redhat.com> - 0.3.6-3
- ghc-6.12.2 doesn't provide utf8-string again
- condition ghc_lib_package

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 0.3.6-2
- update to ghc-rpm-macros-0.5.1 and cabal2spec-0.21.1:
- drop doc and prof bcond
- use common summary and common_description
- use ghc_lib_package

* Wed Dec 23 2009 Jens Petersen <petersen@redhat.com> - 0.3.6-1
- update to 0.3.6
- update packaging for ghc-6.12.1
- added shared library support: needs ghc-rpm-macros 0.3.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 12 2009 Zachary Oglesby <zoglesby@fedoraproject.org> - 0.3.5-2
- Added patch from Jens Petersen for better descriptions

* Fri Jun 12 2009 Zachary Oglesby <zoglesby@fedoraproject.org> - 0.3.5-1
- Updated to version 0.3.5

* Fri Jun  5 2009 Zachary Oglesby <zoglesby@fedoraproject.org> - 0.3.4-2
- Updated to new cabal2spec

* Fri May 29 2009 Zachary Oglesby <zoglesby@fedoraproject.org> - 0.3.4-1
- initial packaging for Fedora created by cabal2spec


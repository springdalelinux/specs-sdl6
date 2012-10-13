%global pkg_name parsec

%global common_summary Haskell parser library

%global common_description Parsec is an industrial-strength parser library.\
It is simple, safe, well documented, has extensive libraries and\
good error messages, and is also fast. It is defined as a monad transformer\
that can be stacked on arbitrary monads, and it is also parametric\
in the input stream type.

%bcond_without shared
%bcond_without hscolour

# debuginfo is not useful for ghc
%global debug_package %{nil}

Name:           ghc-%{pkg_name}
# part of haskell-platform-2010.2.0.0
Version:        2.1.0.1
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
%if %{with hscolour}
BuildRequires:  hscolour
%endif

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


%ghc_lib_package -o 2.1.0.1-5


%changelog
* Sat Sep  4 2010 Jens Petersen <petersen@redhat.com> - 2.1.0.1-5
- update to ghc-rpm-macros-0.8.1, hscolour and drop doc pkg (cabal2spec-0.22.2)
- part of haskell-platform-2010.2.0.0

* Wed Jun 23 2010 Jens Petersen <petersen@redhat.com> - 2.1.0.1-4
- use ghc_strip_dynlinked (ghc-rpm-macros-0.6.0)

* Sat Apr 24 2010 Jens Petersen <petersen@redhat.com> - 2.1.0.1-3
- part of haskell-platform-2010.1.0.0
- rebuild against ghc-6.12.2
- condition ghc_lib_package

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 2.1.0.1-2
- update to ghc-rpm-macros-0.5.1: use ghc_lib_package
- drop bcond for doc and prof
- add comment about haskell-platform

* Thu Dec 24 2009 Jens Petersen <petersen@redhat.com> - 2.1.0.1-1
- update packaging for ghc-6.12.1
- added shared library support
- use new ghc*_requires macros: needs ghc-rpm-macros 0.4.0

* Wed Dec 23 2009 Fedora Haskell SIG <fedora-haskell-list@redhat.com> - 2.1.0.1-0
- initial packaging for Fedora automatically generated by cabal2spec-0.19

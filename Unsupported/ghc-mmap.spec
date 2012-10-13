%global pkg_name mmap

%global common_summary Haskell Memory mapped files library

%global common_description A Haskell wrapper to mmap(2) or MapViewOfFile, allowing files or devices\
to be lazily loaded into memory as strict or lazy ByteStrings, ForeignPtrs or\
plain Ptrs, using the virtual memory subsystem to do on-demand loading.\
Modifications are also supported.

%bcond_without shared
%bcond_without hscolour

# debuginfo is not useful for ghc
%global debug_package %{nil}

Name:           ghc-%{pkg_name}
Version:        0.4.1
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


%ghc_lib_package -o 0.4.1-5


%changelog
* Sat Sep  4 2010 Jens Petersen <petersen@redhat.com> - 0.4.1-5
- add hscolour and doc obsolete (cabal2spec-0.22.2)

* Sat Jun 26 2010 Jens Petersen <petersen@redhat.com> - 0.4.1-4
- sync cabal2spec-0.22

* Sat Apr 24 2010 Jens Petersen <petersen@redhat.com> - 0.4.1-3
- rebuild against ghc-6.12.2
- condition ghc_lib_package

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 0.4.1-2
- update to ghc-rpm-macros-0.5.1 and cabal2spec-0.21.1:
- drop doc and prof bcond
- use common summary and common_description
- use ghc_lib_package
- drop redundant buildroot and its install cleaning

* Tue Nov 17 2009 Jens Petersen <petersen@redhat.com> - 0.4.1-1
- initial packaging for Fedora created by cabal2spec

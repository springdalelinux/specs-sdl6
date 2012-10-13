%global pkg_name hashed-storage

%global common_summary Haskell hashed file storage

%global common_description Support code for reading and manipulating hashed file storage (where each file\
and directory is associated with a cryptographic hash, for corruption-resistant\
storage and fast comparisons).\
\
The supported storage formats include darcs hashed pristine, a plain filesystem\
tree and an indexed plain tree (where the index maintains hashes of the plain\
files and directories).

%global ghc_pkg_deps ghc-binary-devel, ghc-dataenc-devel, ghc-mmap-devel, ghc-mtl-devel, ghc-zlib-devel

%bcond_without shared

# debuginfo is not useful for ghc
%global debug_package %{nil}

Name:           ghc-%{pkg_name}
Version:        0.4.13
Release:        2%{?dist}
Summary:        %{common_summary}

Group:          System Environment/Libraries
License:        BSD
URL:            http://hackage.haskell.org/cgi-bin/hackage-scripts/package/%{pkg_name}
Source0:        http://hackage.haskell.org/packages/archive/%{pkg_name}/%{version}/%{pkg_name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# fedora ghc archs:
ExclusiveArch:  %{ix86} x86_64 ppc alpha
BuildRequires:  ghc, ghc-doc, ghc-prof
BuildRequires:  ghc-rpm-macros >= 0.7.0
BuildRequires:  ghc-hscolour
BuildRequires:  hscolour
%{?ghc_pkg_deps:BuildRequires:  %{ghc_pkg_deps}, %(echo %{ghc_pkg_deps} | sed -e "s/\(ghc-[^, ]\+\)-devel/\1-doc,\1-prof/g")}

%description
%{common_description}
%if %{with shared}
This package provides the shared library.
%endif


%{?ghc_lib_package}


%prep
%setup -q -n %{pkg_name}-%{version}


%build
%ghc_lib_build


%check
# requires QuickCheck2

%install
rm -rf $RPM_BUILD_ROOT
%ghc_lib_install


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Sun Jun 27 2010 Jens Petersen <petersen@redhat.com> - 0.4.13-2
- sync cabal2spec-0.22.1

* Mon May 17 2010 Jens Petersen <petersen@redhat.com> - 0.4.13-1
- update to 0.4.13 for darcs-2.4.3

* Mon Apr 26 2010 Jens Petersen <petersen@redhat.com> - 0.4.11-2
- rebuild against ghc-6.12.2
- condition ghc_lib_package

* Thu Apr 15 2010 Jens Petersen <petersen@redhat.com> - 0.4.11-1
- update to 0.4.11 for darcs-2.4.1

* Mon Mar  1 2010 Jens Petersen <petersen@redhat.com> - 0.4.7-1
- update to 0.4.7

* Sat Jan 23 2010 Jens Petersen <petersen@redhat.com> - 0.4.5-1
- update to 0.4.5 for darcs-beta
- code is now pure BSD: upstream rewrote SHA256.hs
- now depends also on ghc-binary and ghc-dataenc

* Tue Jan 12 2010 Jens Petersen <petersen@redhat.com> - 0.3.9-2
- update to ghc-rpm-macros-0.5.1 and cabal2spec-0.21.1:
- drop doc and prof bcond
- use common summary and common_description
- use ghc_lib_package
- drop redundant buildroot and its install cleaning

* Tue Nov 17 2009 Jens Petersen <petersen@redhat.com> - 0.3.9-1
- initial packaging for Fedora created by cabal2spec

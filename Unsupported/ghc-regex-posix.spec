%global pkg_name regex-posix

%global common_summary Haskell posix regex backend library

%global common_description The posix regex backend for regex-base.

%global ghc_pkg_deps ghc-regex-base-devel

%bcond_without shared

# debuginfo is not useful for ghc
%global debug_package %{nil}

Name:           ghc-%{pkg_name}
# part of haskell-platform-2010.2.0.0
Version:        0.94.2
Release:        1%{?dist}
Summary:        %{common_summary}

Group:          System Environment/Libraries
License:        BSD
URL:            http://hackage.haskell.org/cgi-bin/hackage-scripts/package/%{pkg_name}
Source0:        http://hackage.haskell.org/packages/archive/%{pkg_name}/%{version}/%{pkg_name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# fedora ghc archs:
ExclusiveArch:  %{ix86} x86_64 ppc alpha
BuildRequires:  ghc, ghc-doc, ghc-prof
BuildRequires:  ghc-rpm-macros >= 0.8.0
BuildRequires:  ghc-hscolour
BuildRequires:  hscolour
%{?ghc_pkg_deps:BuildRequires:  %{ghc_pkg_deps}, %(echo %{ghc_pkg_deps} | sed -e "s/\(ghc-[^, ]\+\)-devel/\1-doc,\1-prof/g")}

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


%ghc_lib_package -o 0.94.2-1


%changelog
* Fri Jul 16 2010 Jens Petersen <petersen@redhat.com> - 0.94.2-1
- update to 0.94.2 for haskell-platform-2010.2.0.0
- obsolete doc subpackage (ghc-rpm-macros-0.8.0)

* Sat Jun 26 2010 Jens Petersen <petersen@redhat.com> - 0.94.1-4
- sync cabal2spec-0.22

* Tue Apr 27 2010 Jens Petersen <petersen@redhat.com> - 0.94.1-3
- rebuild against ghc-6.12.2
- condition ghc_lib_package

* Fri Jan 15 2010 Jens Petersen <petersen@redhat.com> - 0.94.1-2
- BSD license
- depends on regexp-base

* Fri Jan 15 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.94.1-1
- initial packaging for Fedora automatically generated by cabal2spec-0.21.1
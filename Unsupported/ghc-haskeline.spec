%global pkg_name haskeline

%global common_summary Haskell command-line interface for user input

%global common_description Haskeline provides a user interface for line input in command-line programs.\
This library is similar in purpose to readline, but since it is written in\
Haskell it is (hopefully) more easily used in other Haskell programs.\
\
Haskeline runs both on POSIX-compatible systems and on Windows.

%global ghc_pkg_deps ghc-mtl-devel ghc-utf8-string-devel

%bcond_without shared
%bcond_without hscolour
 
# debuginfo is not useful for ghc
%global debug_package %{nil}

Name:           ghc-%{pkg_name}
Version:        0.6.3.1
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
BuildRequires:  ghc-rpm-macros >= 0.8.1
%if %{with hscolour}
BuildRequires:  hscolour
%endif
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


%install
rm -rf $RPM_BUILD_ROOT
%ghc_lib_install


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Tue Oct  5 2010 Jens Petersen <petersen@redhat.com> - 0.6.3.1-2.el6
- build without terminfo

* Thu Sep 23 2010 Jens Petersen <petersen@redhat.com> - 0.6.3.1-1
- update to 0.6.3.1
- depend on optional ghc-terminfo-devel

* Fri Sep 17 2010 Jens Petersen <petersen@redhat.com> - 0.6.3-1
- update to 0.6.3

* Thu Aug 19 2010 Jens Petersen <petersen@redhat.com> - 0.6.2.3-1
- update to 0.6.2.3
- update to cabal2spec-0.22.2

* Fri Jun 25 2010 Jens Petersen <petersen@redhat.com> - 0.6.2.2-2
- strip shared library (cabal2spec-0.21.4)

* Thu Apr 29 2010 Jens Petersen <petersen@redhat.com> - 0.6.2.2-1
- 0.6.2.2
- condition ghc_lib_package
- for ghc-6.12.2 depends on utf8-string now

* Tue Feb 16 2010 Jens Petersen <petersen@redhat.com> - 0.6.2.1-2.1
- fix source tarball permissions (#555653)

* Fri Jan 15 2010 Jens Petersen <petersen@redhat.com> - 0.6.2.1-2
- BSD license
- depends on mtl

* Fri Jan 15 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.6.2.1-1
- initial packaging for Fedora automatically generated by cabal2spec-0.21.1
%global pkg_name zlib

%global common_summary Haskell compression and decompression library

%global common_description This package provides a pure Haskell interface for compressing and\
decompressing streams of data represented as lazy ByteStrings. It uses\
the zlib C library so it has high performance. It supports the "zlib",\
"gzip" and "raw" compression formats.\
\
It provides a convenient high level API suitable for most tasks.  For\
the few cases where more control is needed, it provides access to the\
full zlib feature set.

%global ghc_pkg_c_deps zlib-devel

%bcond_without shared
%bcond_without hscolour

# debuginfo is not useful for ghc
%global debug_package %{nil}

Name:           ghc-%{pkg_name}
# part of haskell-platform-2010.2.0.0
Version:        0.5.2.0
Release:        4%{?dist}
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
%{?ghc_pkg_c_deps:BuildRequires:  %{ghc_pkg_c_deps}}

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


%ghc_lib_package -o 0.5.2.0-4


%changelog
* Sat Sep  4 2010 Jens Petersen <petersen@redhat.com> - 0.5.2.0-4
- add hscolour and doc obsolete (cabal2spec-0.22.2)
- part of haskell-platform-2010.2.0.0

* Sat Jun 26 2010 Jens Petersen <petersen@redhat.com> - 0.5.2.0-3
- sync cabal2spec-0.22

* Sat Apr 24 2010 Jens Petersen <petersen@redhat.com> - 0.5.2.0-2
- part of haskell-platform-2010.1.0.0
- rebuild against ghc-6.12.2

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 0.5.2.0-1
- update to 0.5.2.0 (haskell-platform-2009.3.1)
- update to ghc-rpm-macros-0.5.1 and cabal2spec-0.21.1:
- drop doc and prof bcond
- use common summary and common_description
- use ghc_lib_package and ghc_pkg_c_deps

* Sat Dec 26 2009 Jens Petersen <petersen@redhat.com> - 0.5.0.0-12
- update to cabal2spec-0.20 and ghc-rpm-macros-0.4.0:
- use common_summary and common_description
- reenable debuginfo for stripping
- use ghc_requires, ghc_doc_requires, and ghc_prof_requires

* Tue Dec 22 2009 Jens Petersen <petersen@redhat.com>
- fix base Group and devel Summary
- only include docdir in devel if not shared build

* Wed Dec 16 2009 Jens Petersen <petersen@redhat.com> - 0.5.0.0-11
- build for ghc-6.12.1
- added shared library support: needs ghc-rpm-macros 0.3.1
- use cabal_pkg_conf to generate package.conf.d file and use ghc-pkg recache

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 16 2009 Jens Petersen <petersen@redhat.com> - 0.5.0.0-9
- buildrequires ghc-rpm-macros (cabal2spec-0.16)

* Fri Apr 24 2009 Jens Petersen <petersen@redhat.com> - 0.5.0.0-8
- sync with cabal2spec-0.14

* Fri Feb 27 2009 Jens Petersen <petersen@redhat.com> - 0.5.0.0-7
- update to cabal2spec-0.11:
- add devel subpackage
- use ix86 macro for archs and add alpha
- use global rather than define
- make devel subpackage own docdir for now

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb  9 2009 Jens Petersen <petersen@redhat.com> - 0.5.0.0-5
- rebuild to fix unexpanded post preun macros
- add doc subpackage and BR ghc-doc
- add doc requires(post) ghc-doc

* Mon Dec 22 2008 Jens Petersen <petersen@redhat.com> - 0.5.0.0-4
- use bcond for doc and prof build flags (Till Maas, #426751)

* Mon Dec  1 2008 Jens Petersen <petersen@redhat.com> - 0.5.0.0-3
- sync with lib template:
  - add build_prof and build_doc
  - prof requires main package
  - update scriptlet macro names

* Tue Nov 25 2008 Jens Petersen <petersen@redhat.com> - 0.5.0.0-2
- build with ghc-6.10.1
- no longer buildrequire haddock09
- provide devel
- add exclusivearch for current ghc archs
- reindex haddock docs only when uninstalling in postun

* Tue Nov 11 2008 Bryan O'Sullivan <bos@serpentine.com> - 0.5.0.0-1
- Update to 0.5.0.0

* Thu Oct 23 2008 Jens Petersen <petersen@redhat.com> - 0.4.0.4-2
- update for current rawhide
- add pkg_docdir and remove hsc_name
- use haddock09

* Tue Oct 14 2008 Bryan O'Sullivan <bos@serpentine.com> - 0.4.0.4-1
- Revised to follow Haskell packaging guidelines

* Sun Feb 17 2008 Yaakov Nemoy <haskell.rpms@hexago.nl> - 0.4.0.2-1
- added in url

* Sun Feb 17 2008 cabal-rpm <cabal-devel@haskell.org> - 0.4.0.2-1
- spec file autogenerated by cabal-rpm

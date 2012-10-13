%global pkg_name hscolour

%global common_summary Haskell %{pkg_name} library

%global common_description hscolour is a small Haskell package to colourize Haskell code.\
It currently has five output formats: ANSI terminal codes,\
HTML 3.2 with font tags, HTML 4.01 with CSS, LaTeX, and mIRC chat codes.

%bcond_without shared

# debuginfo is not useful for ghc
%global debug_package %{nil}

Name:           %{pkg_name}
Version:        1.16
Release:        1%{?dist}
Summary:        Colourizes Haskell code

Group:          Development/Tools
License:        GPLv2+
URL:            http://www.cs.york.ac.uk/fp/darcs/hscolour/
Source0:        http://hackage.haskell.org/packages/archive/%{name}/%{version}/%{name}-%{version}.tar.gz
# fedora ghc archs:
ExclusiveArch:  %{ix86} x86_64 ppc alpha
BuildRequires:  ghc, ghc-rpm-macros >= 0.5.1
BuildRequires:  ghc-doc
BuildRequires:  ghc-prof
%{?ghc_pkg_deps:BuildRequires:  %{ghc_pkg_deps}, %(echo %{ghc_pkg_deps} | sed -e "s/\(ghc-[^, ]\+\)-devel/\1-doc,\1-prof/g")}

%description
%{common_description}

%files
%defattr(-,root,root,-)
%doc README index.html LICENCE-GPL
%attr(755,root,root) %{_bindir}/HsColour
%{_datadir}/%{name}-%{version}


%ghc_binlib_package


%prep
%setup -q


%build
# dynamic + prof breaks cabal looking for p_dyn
%cabal_configure --ghc -p
%cabal build
%cabal haddock


%install
%cabal_install
%cabal_pkg_conf

%ghc_gen_filelists


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Mon Feb 15 2010 Conrad Meyer <konrad@tylerc.org> - 1.16-1
- Bump to 1.16

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 1.15-4
- update to ghc-rpm-macros-0.5.1 and cabal2spec-0.21.1:
- drop doc and prof bcond
- use common summary and common_description
- define pkg_name and use ghc_binlib_package

* Wed Dec 23 2009 Jens Petersen <petersen@redhat.com> - 1.15-3
- devel package requires shared library not base

* Wed Dec 23 2009 Jens Petersen <petersen@redhat.com> - 1.15-2
- update spec for ghc-6.12.1
- added shared library support: needs ghc-rpm-macros 0.3.1

* Fri Sep 18 2009 Jens Petersen <petersen@redhat.com> - 1.15-1
- update to 1.15

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 24 2009 Jens Petersen <petersen@redhat.com> - 1.13-1
- update to 1.13
- buildrequires ghc-rpm-macros (cabal2spec-0.16)

* Sat Apr 25 2009 Jens Petersen <petersen@redhat.com> - 1.12-3
- sync with cabal2spec-0.15

* Tue Mar 10 2009 Jens Petersen <petersen@redhat.com> - 1.12-2
- fix url (#488665)
- fix HsColour permissions (#488665)

* Thu Mar  5 2009 Jens Petersen <petersen@redhat.com> - 1.12-1
- initial packaging for Fedora created by cabal2spec

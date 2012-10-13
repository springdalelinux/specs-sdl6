%global pkg_name binary

%global common_summary Haskell binary serialisation library

%global common_description Binary serialisation for Haskell values using lazy ByteStrings\
\
Efficient, pure binary serialisation using lazy ByteStrings.\
Haskell values may be encoded to and from binary formats, written to disk as\
binary, or sent over the network. Serialisation speeds of over 1 G/sec have\
been observed, so this library should be suitable for high performance scenarios.

%bcond_without shared
%bcond_without hscolour

# debuginfo is not useful for ghc
%global debug_package %{nil}

Name:           ghc-%{pkg_name}
Version:        0.5.0.2
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


%ghc_lib_package -o 0.5.0.2-4


%changelog
* Sat Sep  4 2010 Jens Petersen <petersen@redhat.com> - 0.5.0.2-4
- add hscolour and doc obsolete (cabal2spec-0.22.2)

* Sat Jun 26 2010 Jens Petersen <petersen@redhat.com> - 0.5.0.2-3
- sync cabal2spec-0.22

* Sat Apr 24 2010 Jens Petersen <petersen@redhat.com> - 0.5.0.2-2
- rebuild against ghc-6.12.2
- condition ghc_lib_package

* Sat Jan 23 2010 Jens Petersen <petersen@redhat.com> - 0.5.0.2-1
- BSD license
- summary and description

* Sat Jan 23 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.5.0.2-0
- initial packaging for Fedora automatically generated by cabal2spec-0.21.1

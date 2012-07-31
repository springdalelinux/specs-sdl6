Summary: Snap for hyperbolic 3-manifolds
Name: snap
Version: 1.11.3
Release: 1%{?dist}
License: GPL
Group: Scientific/Applications
Source: snap-%{version}.tgz
BuildRequires: pari-devel readline-devel
Requires: pari
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Snap (snap-pari) is a computer program for studying arithmetic invariants of
hyperbolic 3-manifolds. See: Computing arithmetic invariants of 3-manifolds
by Coulson, Goodman, Hodgson and Neumann, Experimental Mathematics 
Vol.9 (2000) 1. 

%prep
%setup -q -n snap-pari

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/snap_data

%changelog
* Thu Jan 27 2011 Josko Plazonic <plazonic@math.princeton.edu>
- initial build

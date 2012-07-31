Summary: The GP to C compiler translates GP scripts to PARI programs.
Name: gp2c
Version: 0.0.5pl10
Release: 1%{?dist}
License: GPL
Group: Scientific/Applications
Packager: Josko Plazonic <plazonic@math.princeton.edu>
URL: http://pari.math.u-bordeaux.fr/
Source: http://pari.math.u-bordeaux.fr/pub/pari/GP2C/gp2c-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gmp-devel readline-devel qt-devel tetex tetex-latex ncurses-devel pari-devel
BuildRequires: perl flex bison byacc
Requires: gcc gmp-devel pari-devel

%description
The gp2c compiler is a package for translating GP routines into the C 
programming language, so that they can be compiled and used with the 
PARI system or the GP calculator.

The main advantage of doing this is to speed up computations and to 
include your own routines within the preexisting GP ones. It may also 
find bugs in GP scripts.

%prep
%setup

%build
PARICFG=`ls %{_defaultdocdir}/pari*/pari.cfg`
%configure --with-paricfg=$PARICFG
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{%{_prefix},%{_datadir},%{_includedir},%{_libdir}}
%makeinstall
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/gp2c

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS Change* COPYING INSTALL NEWS README*
%doc doc/*dvi doc/*png doc/*html
%doc %{_mandir}/man1/*
%{_bindir}/*
%{_datadir}/gp2c

%changelog
* Tue Nov 30 2010 Josko Plazonic <plazonic@math.princeton.edu>
- rebuild for rhel6 and tune for pari from epel

* Sun Dec 02 2007 Josko Plazonic <plazonic@math.princeton.edu>
- initial packaging

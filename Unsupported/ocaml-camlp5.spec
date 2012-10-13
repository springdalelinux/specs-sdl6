Name:		ocaml-camlp5
Version:	6.02.3
Release:	1%{?dist}
Summary:	Camlp5 is a preprocessor-prtty-printer of OCaml

Group:		Development/Languages
License:	INRIA
URL:		http://pauillac.inria.fr/~ddr/camlp5/
Source0:	http://pauillac.inria.fr/~ddr/camlp5/distrib/src/camlp5-%{version}.tgz
Patch0:		patch-6.02.3-1

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	ocaml
Requires:	ocaml

%description
Camlp5 is a preprocessor-pretty-printer of OCaml.
It is compatible with OCaml versions from 1.07 to 3.13.0 and branch 3.13.0-gadt.

%prep
%setup -q -n camlp5-%{version}
%patch0 -p0


%build
# their configure script doesn't even accept the options given in their usage
#./configure -bindir=%{_bindir} -libdir=%{_libdir}/ocaml -mandir=%{_mandir}
./configure 
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_mandir}
mv $RPM_BUILD_ROOT/usr/man/man1 $RPM_BUILD_ROOT%{_mandir}
\rmdir $RPM_BUILD_ROOT/usr/man


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc
%{_bindir}/camlp5*
%{_bindir}/mkcamlp5
%{_bindir}/ocpp5
%{_libdir}/ocaml/camlp5
%{_mandir}/man1/camlp5*
%{_mandir}/man1/mkcamlp5*
%{_mandir}/man1/ocpp5*

%changelog
* Tue Sep 20 2011 Thomas Uphill <uphill@ias.edu> - 6.02.3-1
- initial build

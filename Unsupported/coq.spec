Name:		coq
Version:	8.3pl2
Release:	1%{?dist}
Summary:	coq is a formal proof assistant

Group:		Applications/Engineering
License:	LGPL
URL:		coq.inria.fr
Source0:	http://coq.inria.fr/distrib/V8.3pl2/files/%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	mpfr ocaml ocaml-camlp5 ocaml-lablgtk-devel gtk2-devel
Requires:	mpfr ocaml ocaml-camlp5 ocaml-lablgtk gtk2

%description
Coq is a formal proof management system. It provides a formal language to write mathematical definitions, executable algorithms and theorems together with an environment for semi-interactive development of machine-checked proofs. Typical applications include the formalization of programming languages semantics (e.g. the CompCert compiler certification project or Java Card EAL7 certification in industrial context), the formalization of mathematics (e.g. the full formalization of the 4 color theorem or constructive mathematics at Nijmegen) and teaching.

%package ide
Summary:	coq interated development interface
Group:		Applications/Engineering
Requires: 	%{name} = %{version}

%description ide
The Coq Integrated Development Interface is a graphical interface for the
Coq proof assistant

%prep
%setup -q


%build
./configure --mandir %{_mandir} \
	--bindir %{_bindir} \
	--libdir %{_libdir}/coq \
	--docdir %{_docdir}/coq-%{version} \
	--emacslib %{_datadir}/emacs/site-lisp \
	--coqdocdir %{_datadir}/texmf/tex/latex/misc \
	--coqide byte

export LD_LIBRARY_PATH=$(pwd)/kernel/byterun:$LD_LIBRARY_PATH
make world


%install
rm -rf $RPM_BUILD_ROOT
make COQINSTALLPREFIX=%{buildroot} install-coq
make COQINSTALLPREFIX=%{buildroot} install-coqide
export EXCLUDE_FROM_STRIP=%{_bindir}

# Install desktop icon and menu entry

%global coqdatadir %{_libdir}/coq
%if %(test -d %{buildroot}%{coqdatadir} && echo 1 || echo 0) != 1
mkdir -p %{buildroot}%{coqdatadir}
%endif

# Temporary workaround for coq 8.3 install bugs.
# These files have to be installed for coq's provides to match its requires.
cp -p plugins/dp/fol.cmi %{buildroot}%{coqdatadir}/plugins/dp
cp -p plugins/extraction/miniml.cmi %{buildroot}%{coqdatadir}/plugins/extraction
cp -p plugins/micromega/sos_lib.cmi %{buildroot}%{coqdatadir}/plugins/micromega
cp -p proofs/decl_expr.cmi %{buildroot}%{coqdatadir}/proofs

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc CHANGES COPYRIGHT README CREDITS INSTALL LICENSE
%{_bindir}/*
%{_libdir}/coq
%{_mandir}/man1/*
%{_datadir}/emacs/site-lisp/*
%{_datadir}/texmf/tex/latex/misc/*
%exclude %{_bindir}/coqide*
%exclude %{_libdir}/coq/ide

%files ide 
%doc INSTALL.ide
%defattr(-,root,root)
%{_bindir}/coqide*
%{_libdir}/coq/ide

%changelog
* Tue Sep 20 2011 Thomas Uphill <uphill@ias.edu> - 8.3pl2-1
- initial build

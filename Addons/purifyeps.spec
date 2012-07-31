%{!?_texmf: %define _texmf %(eval "echo `kpsewhich -expand-var '$TEXMFMAIN'`")}

%define texpkg      purifyeps
%define texpkgdir   %{_texmf}/tex/latex/%{texpkg}
%define texpkgdoc   %{_texmf}/doc/latex/%{texpkg}
%define bibpkgdir   %{_texmf}/bibtex/bib/%{texpkg}
%define bstpkgdir   %{_texmf}/bibtex/bst/%{texpkg}
%define bibpkgdoc   %{_texmf}/doc/bibtex/%{texpkg}


Summary:	"Purifies" eps files for use by both dvips and pdflatex 
Name:		purifyeps
Version:	1.0a
Release:	2%{?dist}
License:	distributable
Source: 	ftp://ftp.ctan.org/tex-archive/support/purifyeps.zip
URL:            http://www.ctan.org/tex-archive/support/purifyeps
Group:		Applications/Graphics
Requires:	pstoedit
Requires:	tex(tex) tex(latex)
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildArch:      noarch

%description
While pdfLaTeX has a number of nice features, its primary shortcoming
relative to standard LaTeX+dvips is that it is unable to read ordinary
Encapsulated PostScript (EPS) files, the most common graphics format
in the LaTeX world.  purifyeps converts EPS files into a "purified"
form that can be read by *both* LaTeX+dvips and pdfLaTeX.  The trick
is that the standard LaTeX2e graphics packages can parse
MetaPost-produced EPS directly.  Hence, purifyeps need only convert an
arbitrary EPS file into the same stylized format that MetaPost
outputs.

Documentation is provided in Unix man-page format and in PDF
(U.S. letter-sized).  In addition, executing "purifyeps --help" gives
basic command-line usage.

%prep
%setup -n purifyeps

%build

%install
rm -rf  $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m 755 purifyeps $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -m 644 purifyeps.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README purifyeps.pdf
%{_bindir}/purifyeps
%{_mandir}/man1/*.1*

%changelog
* Tue Nov 30 2010 Josko Plazonic <plazonic@math.princeton.edu>
- rebuilt for 6

* Thu Apr 05 2007 Josko Plazonic <plazonic@math.princeton.edu>
- rebuilt for 5

* Thu May 01 2003 Josko Plazonic <plazonic@math.princeton.edu>
- rebuilt for 9

* Thu Mar 20 2003 Josko Plazonic <plazonic@math.princeton.edu>
- rebuilt for PU_IAS

* Fri Feb 14 2003 Duncan Haldane <haldane@princeton.edu>
- initial rpm package


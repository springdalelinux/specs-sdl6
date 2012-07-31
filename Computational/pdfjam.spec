%global majver  2
%global minver  08

Name:           pdfjam
Version:        %{majver}.%{minver}
Release:        1%{?dist}
Summary:        Utilities for joining, rotating and aligning PDFs

Group:          Applications/Publishing
# No version specified.
License:        GPL+
URL:            http://go.warwick.ac.uk/pdfjam
Source0:        http://go.warwick.ac.uk/pdfjam/pdfjam_%{majver}%{minver}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

# for testing
BuildRequires:	tetex-latex

Requires:       tetex-latex
# for mktemp
Requires:       coreutils

%description
PDFjam is a small collection of shell scripts which provide a simple
interface to some of the functionality of the excellent pdfpages
package (by Andreas Matthias) for pdfLaTeX.  At present the utilities
available are:

  * pdfnup, which allows PDF files to be "n-upped" in roughly the way
    that psnup does for PostScript files;
  * pdfjoin, which concatenates the pages of multiple PDF files
    together into a single file;
  * pdf90, which rotates the pages of one or more PDF files through 90
    degrees (anti-clockwise).

In every case, source files are left unchanged.

A potential drawback of these utilities is that any hyperlinks in the
source PDF are lost. On the positive side, there is no appreciable
degradation of image quality in processing PDF files with these
programs, unlike some other indirect methods such as "pdf2ps | psnup |
ps2pdf" (in the author's experience).


%prep
%setup -q -n pdfjam
unzip tests.zip

%build

%install
rm -rf $RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}
install -p -m 755 bin/* $RPM_BUILD_ROOT%{_bindir}/
install -p -m 644 man1/* $RPM_BUILD_ROOT%{_mandir}/man1/

%check
cd tests
./run.sh | tee testlog.txt
[ `grep ^OK testlog.txt | wc -l` == 5 ]

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING PDFjam-README.html pdfdroplets.png pdfjam.conf
%{_bindir}/*
%{_mandir}/man1/*


%changelog
* Mon Nov 15 2010 Michel Salim <salimma@fedoraproject.org> - 2.%{minver}-1
- Update to 2.08 (test5 fixed upstream)

* Sun Nov 14 2010 Michel Salim <salimma@fedoraproject.org> - 2.07-1
- Update to 2.07

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Mar 12 2009 Michel Salim <salimma@fedoraproject.org> - 1.21-1
- Update to 1.21, fixing security issues CVE-2008-5743, CVE-2008-5843
  (bz #480174)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Aug 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.20-7
- fix license tag

* Fri Jan 18 2008 Michel Salim <michel.sylvan@gmail.com> - 1.20-6
- Rebuild for Fedora 9 (development tree)

* Sat Sep  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.20-5
- Rebuild for FC6.

* Thu Mar  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.20-4
- Rebuild for FC5.

* Sat May 14 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.20-3
- Add dist tag.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.20-2
- rebuilt

* Thu Feb 24 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.20-1
- First build.

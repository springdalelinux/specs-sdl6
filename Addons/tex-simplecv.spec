%define real_name simplecv
%{!?_texmf: %define _texmf %(eval "echo `kpsewhich -expand-var '$TEXMFMAIN'`")}

Name:           tex-%{real_name}
Version:        1.6
Release:        8%{?dist}
Summary:        A simple latex class for writing curricula vitae

Group:          Applications/Publishing
License:        LPPL
URL:            http://tug.ctan.org/tex-archive/macros/latex/contrib/%{real_name}/
Source0:        http://tug.ctan.org/get/macros/latex/contrib/%{real_name}.zip

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  tex(latex)
BuildRequires:  /usr/bin/kpsewhich

Requires:       tex(latex)

# no debuginfo
%define debug_package %{nil}

%description
The simplecv document class is intended to provide a simple yet
elegant way to write your curriculum vitae (resume). This is a
repackaging of the |cv| class that has been available with LyX for a
long time. The change of name has been made necessary by the existence
of another |cv| class on CTAN.

%package doc
Summary:        Documentation for %{name}
Group:          Applications/Publishing
Requires:       texlive-texmf-doc

%description doc
Documentation for latex package %{real_name}.

%prep
%setup -q -n %{real_name}

%build
latex %{real_name}.ins

pdflatex %{real_name}.dtx
pdflatex %{real_name}.dtx

%install
rm -rf $RPM_BUILD_ROOT

install -d -m755 $RPM_BUILD_ROOT%{_texmf}/tex/latex/%{real_name}
install -d -m755 $RPM_BUILD_ROOT%{_texmf}/doc/tex/latex/%{real_name}

cp -p %{real_name}.cls $RPM_BUILD_ROOT%{_texmf}/tex/latex/%{real_name}

cp -p %{real_name}.pdf $RPM_BUILD_ROOT%{_texmf}/doc/tex/latex/%{real_name}
cp -p test* $RPM_BUILD_ROOT%{_texmf}/doc/tex/latex/%{real_name}

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /usr/bin/texhash

%postun -p /usr/bin/texhash

%post doc -p /usr/bin/texhash

%postun doc -p /usr/bin/texhash


%files
%defattr(-,root,root,-)
%{_texmf}/tex/latex/%{real_name}

%doc README

%files doc
%defattr(-,root,root,-)
%{_texmf}/doc/tex/latex/%{real_name}

%changelog
* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul  8 2008 José Matos <jamatos[AT]fc.up.pt> - 1.6-6

- Add distag, and replace the dependency of -doc subpackage just to
  require the directory ownership tetex-doc -> texlive-texmf-doc.
- replace tetex-latex by tex(latex) in [Build]Requires.

* Thu Jun 26 2008 José Matos <jamatos[AT]fc.up.pt> - 1.6-5
- doc subpackage requires tetex-doc and no longer requires the main package.

* Tue Apr 15 2008 José Matos <jamatos[AT]fc.up.pt> - 1.6-4
- Run texhash for doc subpackage.

* Tue Jan 15 2008 José Matos <jamatos[AT]fc.up.pt> - 1.6-3
- Create new subpackage with the documentation.
- Only copy cls file to texmf tree.

* Mon Jan 14 2008 José Matos <jamatos[AT]fc.up.pt> - 1.6-2
- Add README to %%doc.
- Create .cls file.

* Mon Jan 14 2008 José Matos <jamatos[AT]fc.up.pt> - 1.6-1
- First build.


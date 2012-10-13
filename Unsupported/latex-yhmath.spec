%define shortname yhmath
%define name latex-%{shortname}
%define version 20020913
%define release 3%{?dist}

%define texmfdir /usr/share/texmf
%define texdir %{texmfdir}/tex
%define latexdir %{texmfdir}/tex/latex
%define packagedir %{latexdir}/%{shortname}
%define lyxdir %{_datadir}/lyx
%define xemacsdir %{_datadir}/xemacs/xemacs-packages
%define emacsdir %{_datadir}/emacs/site-lisp
%define fonts %{texmfdir}/fonts
%define fontsmap %{texmfdir}/fonts/map
%define fontssource %{texmfdir}/fonts/source/%{shortname}
%define fontstfm %{fonts}/tfm/%{shortname}
%define fontsvf %{fonts}/vf/%{shortname}
%define fontstype1 %{fonts}/type1/%{shortname}

Summary: A LaTeX class for delimiters
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{shortname}.zip
Source1: %{shortname}.pdf
Source2: yhcmex.pfb
Source3: %{shortname}2.zip
License: GPL
Group: Publishing
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildArch: noarch
BuildRequires: texlive, texlive-latex
Requires: texlive, texlive-latex

%description
This package provides a set of big delimiters, intermediate to those of the original TeX, and also much bigger.
It also provides very wide accents (including two new ones: parenthesis and triangle).  These symbols are included
in a font which has Don's cmex10 as lower ASCII part.

%prep
%setup -n %{shortname} -c -T -a 3

%build
cp %{SOURCE1} %{SOURCE2} %{shortname}/
cd %{shortname}/
latex yhmath.ins
cd ..
unzip -o %{SOURCE0}

%install
cd %{shortname}
rm -rf "$RPM_BUILD_ROOT"
install --mode=0755 -d $RPM_BUILD_ROOT%{packagedir}
install --mode=0755 -d $RPM_BUILD_ROOT%{fontstfm}
install --mode=0755 -d $RPM_BUILD_ROOT%{fontsvf}
install --mode=0755 -d $RPM_BUILD_ROOT%{fontstype1}
install --mode=0755 -d $RPM_BUILD_ROOT%{fontssource}

# style file
mv OMXyhex.fd %{shortname}.sty $RPM_BUILD_ROOT%{packagedir}/

# fonts
mv yhcmex.pf* $RPM_BUILD_ROOT%{fontstype1}
mv *.tfm $RPM_BUILD_ROOT%{fontstfm}
mv yhcmex10.vf $RPM_BUILD_ROOT%{fontsvf}
mv *.mf $RPM_BUILD_ROOT%{fontssource}

rm -f yhmath.log yhmath.ins yhmath.drv yhmath.dtx
for i in dvips dvipdfm pdftex; do
	mkdir -p $RPM_BUILD_ROOT%{fontsmap}/$i/%{shortname}
	echo 'yrcmex10 Yhcmex <yhcmex.pfb' >> $RPM_BUILD_ROOT%{fontsmap}/$i/%{shortname}/%{shortname}.map
done

chmod -R a+rX,og-w "$RPM_BUILD_ROOT%{texdir}"

%post
/usr/bin/texhash
conffile="$(texconfig-sys conf | grep updmap.cfg)"
if [ "$1" -eq "1" ]; then
    updmap-sys --quiet --nohash --cnffile ${conffile} --enable Map %{shortname}.map
fi

%postun
conffile="$(texconfig-sys conf | grep updmap.cfg)"
if [ "$1" -eq "0" ]; then
  updmap-sys --quiet --nohash --cnffile ${conffile} --disable %{shortname}.map
fi
/usr/bin/texhash 

%clean
rm -rf "$RPM_BUILD_ROOT"

%files
%defattr(-,root,root)
%doc %{shortname}/%{shortname}.p*
%{packagedir}
%{fontssource}
%{fontstfm}
%{fontsvf}
%{fontstype1}
%{fontsmap}/*/%{shortname}

%changelog
* Fri Sep 16 2011 Thomas Uphill <uphill@ias.edu> 1.10
- first RPM version

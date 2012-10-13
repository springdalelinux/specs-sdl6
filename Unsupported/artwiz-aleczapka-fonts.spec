%global fontname artwiz-aleczapka
%global fontconf 60-%{fontname}

%define common_desc \
Artwiz is a family of very small futuristic fonts, with varying styles of \
typefaces designed at a single pixel size. The minimal nature of the \
fonts makes them popular with users of lightweight window managers. These \
fonts have been updated by Alec Zapka to be compatible with modern \
software and support an extended character set. \

Name:		%{fontname}-fonts
Version:	1.3
Release:	10%{?dist}
Summary:	Very small futuristic font family
Group:		User Interface/X
License:	GPLv2
URL:		http://artwizaleczapka.sourceforge.net/
Source0:	http://dl.sf.net/artwizaleczapka/artwiz-aleczapka-en-sources-1.3.tar.bz2
Source1:	http://dl.sf.net/artwizaleczapka/artwiz-aleczapka-de-sources-1.3.tar.bz2
Source2:	http://dl.sf.net/artwizaleczapka/artwiz-aleczapka-se-sources-1.3.tar.bz2
Source3:	artwiz-aleczapka-fonts-anorexia-fontconfig.conf
Source4:	artwiz-aleczapka-fonts-aqui-fontconfig.conf
Source5:	artwiz-aleczapka-fonts-cure-fontconfig.conf
Source6:	artwiz-aleczapka-fonts-drift-fontconfig.conf
Source7:	artwiz-aleczapka-fonts-edges-fontconfig.conf
Source8:	artwiz-aleczapka-fonts-fkp-fontconfig.conf
Source9:	artwiz-aleczapka-fonts-gelly-fontconfig.conf
Source10:	artwiz-aleczapka-fonts-glisp-fontconfig.conf
Source11:	artwiz-aleczapka-fonts-kates-fontconfig.conf
Source12:	artwiz-aleczapka-fonts-lime-fontconfig.conf
Source13:	artwiz-aleczapka-fonts-mints-mild-fontconfig.conf
Source14:	artwiz-aleczapka-fonts-mints-strong-fontconfig.conf
Source15:	artwiz-aleczapka-fonts-nu-fontconfig.conf
Source16:	artwiz-aleczapka-fonts-smoothansi-fontconfig.conf
Source17:	artwiz-aleczapka-fonts-snap-fontconfig.conf
Patch0:		artwiz-aleczapka-fkp-cleanups.patch
Patch1:		artwiz-aleczapka-fonts-1.3-fix-makepcf.patch
BuildArch:	noarch
BuildRequires:	xorg-x11-font-utils, fontpackages-devel
Requires:	%{fontname}-anorexia-fonts = %{version}-%{release}
Requires:	%{fontname}-aqui-fonts = %{version}-%{release}
Requires:	%{fontname}-cure-fonts = %{version}-%{release}
Requires:	%{fontname}-drift-fonts = %{version}-%{release}
Requires:	%{fontname}-edges-fonts = %{version}-%{release}
Requires:	%{fontname}-fkp-fonts = %{version}-%{release}
Requires:	%{fontname}-gelly-fonts = %{version}-%{release}
Requires:	%{fontname}-glisp-fonts	= %{version}-%{release}
Requires:	%{fontname}-kates-fonts = %{version}-%{release}
Requires:	%{fontname}-lime-fonts = %{version}-%{release}
Requires:	%{fontname}-mints-mild-fonts = %{version}-%{release}
Requires:	%{fontname}-mints-strong-fonts = %{version}-%{release}
Requires:	%{fontname}-nu-fonts = %{version}-%{release}
Requires:	%{fontname}-smoothansi-fonts = %{version}-%{release}
Requires:	%{fontname}-snap-fonts = %{version}-%{release}

%description
%common_desc
This is a metapackage, which pulls in all the separated fonts in this family.

%package common
Summary:	Common files for Artwiz Aleczapka fonts (documentation...)
Group:		User Interface/X
Requires:	fontpackages-filesystem

%description common
%common_desc

%package -n %{fontname}-anorexia-fonts
Summary:	Anorexia font in Artwiz family
Group:		User Interface/X
Requires:	%{name}-common = %{version}-%{release}

%description -n %{fontname}-anorexia-fonts
%common_desc
This package contains the Anorexia font in three encodings, English, German, 
and Swedish.

%_font_pkg -n anorexia -f %{fontconf}-anorexia.conf anorexia*.pcf

%package -n %{fontname}-aqui-fonts
Summary:	Aqui font in Artwiz family
Group:		User Interface/X
Requires:	%{name}-common = %{version}-%{release}

%description -n %{fontname}-aqui-fonts
%common_desc
This package contains the Aqui font in three encodings, English, German, and
Swedish.

%_font_pkg -n aqui -f %{fontconf}-aqui.conf aqui*.pcf

%package -n %{fontname}-cure-fonts
Summary:	Cure font in Artwiz family
Group:		User Interface/X
Requires:	%{name}-common = %{version}-%{release}

%description -n	%{fontname}-cure-fonts
%common_desc
This package contains the Cure font in three encodings, English, German, and 
Swedish.

%_font_pkg -n cure -f %{fontconf}-cure.conf cure*.pcf

%package -n %{fontname}-drift-fonts
Summary:	Drift font in Artwiz family
Group:		User Interface/X
Requires:	%{name}-common = %{version}-%{release}

%description -n %{fontname}-drift-fonts
%common_desc
This package contains the Drift font in three encodings, English, German,
and Swedish.

%_font_pkg -n drift -f %{fontconf}-drift.conf drift*.pcf

%package -n %{fontname}-edges-fonts
Summary:	Edges font in Artwiz family
Group:		User Interface/X
Requires:	%{name}-common = %{version}-%{release}

%description -n %{fontname}-edges-fonts
%common_desc
This package contains the Edges font in three encodings, English, German,
and Swedish.

%_font_pkg -n edges -f %{fontconf}-edges.conf edges*.pcf

%package -n %{fontname}-fkp-fonts
Summary:	Fkp font in Artwiz family
Group:		User Interface/X
Requires:	%{name}-common = %{version}-%{release}

%description -n %{fontname}-fkp-fonts
%common_desc
This package contains the fkp font in three encodings, English, German,
and Swedish.

%_font_pkg -n fkp -f %{fontconf}-fkp.conf fkp*.pcf

%package -n %{fontname}-gelly-fonts
Summary:	Gelly font in Artwiz family
Group:		User Interface/X
Requires:	%{name}-common = %{version}-%{release}

%description -n %{fontname}-gelly-fonts
%common_desc
This package contains the Gelly font in three encodings, English, German,
and Swedish.

%_font_pkg -n gelly -f %{fontconf}-gelly.conf gelly*.pcf

%package -n %{fontname}-glisp-fonts
Summary:	Glisp fonts in Artwiz family
Group:		User Interface/X
Requires:	%{name}-common = %{version}-%{release}

%description -n %{fontname}-glisp-fonts
%common_desc
This package contains the Glisp font in three encodings, English, German,
and Swedish. It also includes a Regular and Bold version of the font for 
each encoding.

%_font_pkg -n glisp -f %{fontconf}-glisp.conf glisp*.pcf

%package -n %{fontname}-kates-fonts
Summary:	Kates font in Artwiz family
Group:		User Interface/X
Requires:	%{name}-common = %{version}-%{release}

%description -n %{fontname}-kates-fonts
%common_desc
This package contains the Kates font in three encodings, English, German,
and Swedish. 

%_font_pkg -n kates -f %{fontconf}-kates.conf kates*.pcf

%package -n %{fontname}-lime-fonts
Summary:	Lime font in Artwiz family
Group:		User Interface/X
Requires:	%{name}-common = %{version}-%{release}

%description -n %{fontname}-lime-fonts
%common_desc
This package contains the Lime font in three encodings, English, German,
and Swedish.

%_font_pkg -n lime -f %{fontconf}-lime.conf lime*.pcf

%package -n %{fontname}-mints-mild-fonts
Summary:	Mints Mild font in Artwiz family
Group:		User Interface/X
Requires:	%{name}-common = %{version}-%{release}

%description -n %{fontname}-mints-mild-fonts
%common_desc
This package contains the Mints Mild font in three encodings, English, German,
and Swedish.

%_font_pkg -n mints-mild -f %{fontconf}-mints-mild.conf mints-mild*.pcf

%package -n %{fontname}-mints-strong-fonts
Summary:	Mints Strong font in Artwiz family
Group:		User Interface/X
Requires:	%{name}-common = %{version}-%{release}

%description -n %{fontname}-mints-strong-fonts
%common_desc
This package contains the Mints Strong font in three encodings, English, 
German, and Swedish.

%_font_pkg -n mints-strong -f %{fontconf}-mints-strong.conf mints-strong*.pcf

%package -n %{fontname}-nu-fonts
Summary:	Nu font in Artwiz family
Group:		User Interface/X
Requires:	%{name}-common = %{version}-%{release}

%description -n %{fontname}-nu-fonts
%common_desc
This package contains the Nu font in three encodings, English, German,
and Swedish.

%_font_pkg -n nu -f %{fontconf}-nu.conf nu*.pcf

%package -n %{fontname}-smoothansi-fonts
Summary:	Smoothansi font in Artwiz family
Group:		User Interface/X
Requires:	%{name}-common = %{version}-%{release}

%description -n %{fontname}-smoothansi-fonts
%common_desc
This package contains the Smoothansi font in three encodings, English, 
German, and Swedish.

%_font_pkg -n smoothansi -f %{fontconf}-smoothansi.conf smoothansi*.pcf

%package -n %{fontname}-snap-fonts
Summary:	Snap font in Artwiz family
Group:		User Interface/X
Requires:	%{name}-common = %{version}-%{release}

%description -n %{fontname}-snap-fonts
%common_desc
This package contains the Snap font in three encodings, English, German,
and Swedish.

%_font_pkg -n snap -f %{fontconf}-snap.conf snap*.pcf

%prep
%setup -q -c %{name}-%{version} -a1 -a2
%patch0 -p0
%patch1 -p1 -b .fix-makepcf

%build
for lang in de en se; do
    pushd %{_builddir}/%{name}-%{version}/artwiz-aleczapka-$lang-sources-%{version}
    sh makepcf.sh
    popd
done


%install
rm -rf %{buildroot}
install -m 0755 -d %{buildroot}%{_fontdir}
for lang in de en se; do
    install -p -m 0644 artwiz-aleczapka-$lang-sources-%{version}/*.pcf %{buildroot}%{_fontdir}
done
install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} %{buildroot}%{_fontconfig_confdir}
install -m 0644 -p %{SOURCE3} %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-anorexia.conf
install -m 0644 -p %{SOURCE4} %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-aqui.conf
install -m 0644 -p %{SOURCE5} %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-cure.conf
install -m 0644 -p %{SOURCE6} %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-drift.conf
install -m 0644 -p %{SOURCE7} %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-edges.conf
install -m 0644 -p %{SOURCE8} %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-fkp.conf
install -m 0644 -p %{SOURCE9} %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-gelly.conf
install -m 0644 -p %{SOURCE10} %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-glisp.conf
install -m 0644 -p %{SOURCE11} %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-kates.conf
install -m 0644 -p %{SOURCE12} %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-lime.conf
install -m 0644 -p %{SOURCE13} %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-mints-mild.conf
install -m 0644 -p %{SOURCE14} %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-mints-strong.conf
install -m 0644 -p %{SOURCE15} %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-nu.conf
install -m 0644 -p %{SOURCE16} %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-smoothansi.conf
install -m 0644 -p %{SOURCE17} %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-snap.conf

for fontconf in %{fontconf}-anorexia.conf %{fontconf}-aqui.conf %{fontconf}-cure.conf %{fontconf}-drift.conf %{fontconf}-edges.conf %{fontconf}-fkp.conf %{fontconf}-gelly.conf\
		%{fontconf}-glisp.conf %{fontconf}-kates.conf %{fontconf}-lime.conf %{fontconf}-mints-mild.conf %{fontconf}-mints-strong.conf %{fontconf}-nu.conf \
		%{fontconf}-smoothansi.conf %{fontconf}-snap.conf
do
	ln -s %{_fontconfig_templatedir}/$fontconf %{buildroot}%{_fontconfig_confdir}/$fontconf
done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
# This is a dummy metapackage.

%files common
%defattr(-,root,root,-)
# generic docs are the same for every lang (AUTHORS has all info in german dir
# so use it from german font dir)
%doc artwiz-aleczapka-de-sources-1.3/{AUTHORS,COPYING,README,VERSION}
%doc artwiz-aleczapka-de-sources-1.3/README.DE
%doc artwiz-aleczapka-se-sources-1.3/README.SE
%dir %{_fontdir}

%changelog
* Thu Jan 21 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.3-10
- rework package to meet font packaging guidelines

* Thu Jan 14 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.3-9
- rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.3-6
- font cleanup on fkp font (bz 472220)

* Sat Sep 23 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.3-5
- Rebuilt for FC6

* Tue Feb 14 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.3-4
Rebuild for Fedora Extras 5

* Sat Dec 31 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.3-3
- apply fixes from Dawid Gajownik
- add documentation

* Tue Nov 29 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.3-2
- package name with -fonts
- use fc-cache in post/postun

* Sat Nov 26 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.3-1
- split from fluxbox package

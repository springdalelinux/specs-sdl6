%global fontname stix
%global fontconf 61-%{fontname}

%global archivename STIXv%{version}

%global common_desc \
The mission of the Scientific and Technical Information Exchange (STIX) font \
creation project is the preparation of a comprehensive set of fonts that serve \
the scientific and engineering community in the process from manuscript \
creation through final publication, both in electronic and print formats.

Name:    %{fontname}-fonts
Version: 1.0.0
Release: 3%{?dist}
Summary: Scientific and engineering fonts

Group:   User Interface/X
License: OFL
URL:     http://www.stixfonts.org/
# Download hidden behind a form
Source0: %{archivename}.zip
Source10: stix-fonts-fontconfig.conf
Source11: stix-fonts-pua-fontconfig.conf
Source12: stix-fonts-integrals-fontconfig.conf
Source13: stix-fonts-sizes-fontconfig.conf
Source14: stix-fonts-variants-fontconfig.conf

BuildArch:     noarch
BuildRequires: fontpackages-devel
Requires:      fontpackages-filesystem

%description
%common_desc

This package includes base Unicode fonts containing most glyphs for standard
use.

%_font_pkg -f %{fontconf}.conf STIXGeneral*otf
%doc License/*.pdf


%package -n %{fontname}-pua-fonts
Summary:  Scientific and engineering fonts, PUA glyphs
Requires: %{name} = %{version}-%{release}

%description -n %{fontname}-pua-fonts
%common_desc

This package includes fonts containing glyphs called out from the Unicode
Private Use Area (PUA) range. Glyphs in this range do not have an official
Unicode codepoint. They're generally accessible only through specialised
software. Text using them will break if they're ever accepted by the Unicode
Consortium and moved to an official codepoint.

%_font_pkg -n pua -f %{fontconf}-pua.conf STIXNonUni*otf


%package -n %{fontname}-integrals-fonts
Summary:  Scientific and engineering fonts, additional integral glyphs
Requires: %{name} = %{version}-%{release}

%description -n %{fontname}-integrals-fonts
%common_desc

This package includes fonts containing additional integrals of various size
and slant.

%_font_pkg -n integrals -f %{fontconf}-integrals.conf STIXInt*.otf


%package -n %{fontname}-sizes-fonts
Summary:  Scientific and engineering fonts, additional glyph sizes
Requires: %{name} = %{version}-%{release}

%description -n %{fontname}-sizes-fonts
%common_desc

This package includes fonts containing glyphs in additional sizes (Mostly
"fence" and "piece" glyphs).

%_font_pkg -n sizes -f %{fontconf}-sizes.conf STIXSiz*.otf


%package -n %{fontname}-variants-fonts
Summary:  Scientific and engineering fonts, additional glyph variants
Requires: %{name} = %{version}-%{release}

%description -n %{fontname}-variants-fonts
%common_desc

This package includes fonts containing alternative variants of some glyphs.

%_font_pkg -n variants -f %{fontconf}-variants.conf STIXVar*otf


%package doc
Summary:  Scientific and engineering fonts, documentation

%description doc
%common_desc

This package includes the documentation released by the STIX project.

%prep
%setup -q -n %{archivename}
for txt in */*.TXT ; do
   fold -s $txt > $txt.new
   sed -i 's/\r//' $txt.new
   touch -r $txt $txt.new
   mv $txt.new $txt
done


%build


%install
rm -fr %{buildroot}

install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p Fonts/*.otf %{buildroot}%{_fontdir}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}

install -m 0644 -p %{SOURCE10} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}.conf
install -m 0644 -p %{SOURCE11} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-pua.conf
install -m 0644 -p %{SOURCE12} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-integrals.conf
install -m 0644 -p %{SOURCE13} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-sizes.conf
install -m 0644 -p %{SOURCE14} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-variants.conf

for fconf in %{fontconf}.conf \
             %{fontconf}-pua.conf \
             %{fontconf}-integrals.conf \
             %{fontconf}-sizes.conf \
             %{fontconf}-variants.conf ; do
  ln -s %{_fontconfig_templatedir}/$fconf \
        %{buildroot}%{_fontconfig_confdir}/$fconf
done


%clean
rm -fr %{buildroot}


%files doc
%defattr(0644,root,root,0755)
%doc *.pdf Blocks/ Glyphs/ HTML/ License/


%changelog
* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 25 2010 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 1.0.0-1
— Update to non-beta release
— Switch licensing to OFL
— Add -doc subpackage

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- 0.9-13
— Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- 0.9-12
— Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.9-11
— prepare for F11 mass rebuild, new rpm and new fontpackages

* Fri Jan 16 2009 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.9-10
‣ Convert to new naming guidelines

* Sun Nov 23 2008 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.9-9
ᛤ ‘rpm-fonts’ renamed to “fontpackages”

* Fri Nov 14 2008 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.9-8
▤ Rebuild using new « rpm-fonts »

* Fri Jul 11 2008 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.9-7
⌖ Fedora 10 alpha general package cleanup

* Thu Nov 1 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
☺ 0.9-6
 ✓ Add some fontconfig aliasing rules
☢ 0.9-4
⚠ Initial experimental packaging

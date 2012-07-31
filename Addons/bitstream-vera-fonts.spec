%global fontname    bitstream-vera
%global archivename ttf-bitstream-vera

%global common_desc \
The Vera fonts are high-quality Latin fonts donated by Bitstream. \
These fonts have been released under a liberal license, see the  \
licensing FAQ in COPYRIGHT.TXT or the online up-to-date version \
at %{url} for details.

Name:    %{fontname}-fonts
Version: 1.10
Release: 18%{?dist}
Summary: Bitstream Vera fonts

Group:     User Interface/X
License:   Bitstream Vera
URL:       http://www.gnome.org/fonts/
Source:    ftp://ftp.gnome.org/pub/GNOME/sources/%{archivename}/%{version}/%{archivename}-%{version}.tar.bz2
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:     noarch
BuildRequires: fontpackages-devel

%description
%common_desc


%package common
Summary:   Common files of the Bitstream Vera font set
Requires:  fontpackages-filesystem
Obsoletes: %{name}-compat < 1.10-17

%description common
%common_desc

This package consists of files used by other %{name} packages.


%package -n %{fontname}-sans-fonts
Summary:  Variable-width sans-serif Bitstream Vera fonts
Requires: %{name}-common = %{version}-%{release}

Obsoletes: %{name}-sans < 1.10-13

%description -n %{fontname}-sans-fonts
%common_desc

This package consists of the Bitstream Vera sans-serif variable-width font
faces.

%_font_pkg -n sans Vera.ttf VeraBd.ttf VeraIt.ttf VeraBI.ttf


%package -n %{fontname}-serif-fonts
Summary:  Variable-width serif Bitstream Vera fonts
Requires: %{name}-common = %{version}-%{release}

Obsoletes: %{name}-serif < 1.10-13

%description -n %{fontname}-serif-fonts
%common_desc

This package consists of the Bitstream Vera serif variable-width font faces.

%_font_pkg -n serif VeraSe*ttf


%package -n %{fontname}-sans-mono-fonts
Summary:  Monospace sans-serif Bitstream Vera fonts
Requires: %{name}-common = %{version}-%{release}

Obsoletes: %{name}-sans-mono < 1.10-13

%description -n %{fontname}-sans-mono-fonts
%common_desc

This package consists of the Bitstream Vera sans-serif monospace font faces.

%_font_pkg -n sans-mono VeraMo*ttf


%prep
%setup -q -n %{archivename}-%{version}

%build

%install
rm -fr %{buildroot}

install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p *.ttf %{buildroot}%{_fontdir}


%clean
rm -fr %{buildroot}


%files common
%defattr(0644,root,root,0755)
%doc *.TXT


%changelog
* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 1.10-17
— remove pre-F11 compatibility metapackage


* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- 1.10-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 1.10-15
— prepare for F11 mass rebuild, new rpm and new fontpackages

* Thu Jan 15 2009 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 1.10-14
– update for new naming guidelines
– build with new fontpackages (1.15)

* Sun Nov 23 2008 <nicolas.mailhot at laposte.net>
- 1.10-12
ᛤ ‘rpm-fonts’ renamed to “fontpackages”

* Fri Nov 14 2008 <nicolas.mailhot at laposte.net>
- 1.10-11
▤ Rebuild using new « rpm-fonts »

* Fri Aug 10 2007 Matthias Clasen <mclasen@redhat.com> - 1.10-8
- Update license field
- Shorten description line

* Fri Sep 08 2006 Behdad Esfahbod <besfahbo@redhat.com> - 1.10-7
- s/latin/Latin/ in package description (#205693)

* Fri Jul 14 2006 Behdad Esfahbod <besfahbo@redhat.com> - 1.10-6
- remove ghost file fonts.cache-1 as fontconfig uses out of tree
  cache files now.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.10-5.1.1
- rebuild

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Jan 08 2005 Florian La Roche <laroche@redhat.com>
- rebuilt to get rid of legacy selinux filecontexts

* Sun May 30 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- change post/postun scripts

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun 10 2003 Owen Taylor <otaylor@redhat.com> 1.10-1
- Base package on spec file from Nicolas Mailhot <Nicolas.Mailhot at laPoste.net>
- Cleanups from Warren Togami and Nicolas Mailhot

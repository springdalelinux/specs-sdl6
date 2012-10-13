#TODO: 
# - gnome/tango integration
# - verify spell checker integration works as expected
# - verify l10n packs works when rpm-ized

%global cairo_version 0.5

%global minimum_build_nspr_version 4.7.2
%global minimum_build_nss_version 3.12

Name:           kompozer
%global upstream_version 0.8b3
Version:        0.8
Release:        0.5.b3%{?dist}
Summary:        Web Authoring System

Group:          Applications/Publishing
License:        GPLv2+ or LGPLv2+ or MPLv1.1
URL:            http://www.kompozer.net/
#Source0:       https://sourceforge.net/projects/kompozer/files/current/0.8b3/%{name}-%{upstream_version}-src.tar.bz2/download
Source0:        %{name}-%{upstream_version}-src.tar.bz2
# upstream URI: http://git.debian.org/?p=users/derevko-guest/kompozer.git;a=blob_plain;f=debian/kompozer.1;hb=HEAD
Source1:        kompozer-debian-manpage

# language support
Source2:       http://kompozer.sourceforge.net/l10n/kpz08/kpz-langpack-da.xpi
Source3:       http://kompozer.sourceforge.net/l10n/kpz08/kpz-langpack-de.xpi
Source4:       http://kompozer.sourceforge.net/l10n/kpz08/kpz-langpack-enUS.xpi
Source5:       http://kompozer.sourceforge.net/l10n/kpz08/kpz-langpack-esES.xpi
Source6:       http://kompozer.sourceforge.net/l10n/kpz08/kpz-langpack-fr.xpi
Source7:       http://kompozer.sourceforge.net/l10n/kpz08/kpz-langpack-it.xpi
Source8:       http://kompozer.sourceforge.net/l10n/kpz08/kpz-langpack-nl.xpi
Source9:       http://kompozer.sourceforge.net/l10n/kpz08/kpz-langpack-ru.xpi
Source10:      http://kompozer.sourceforge.net/l10n/kpz08/kpz-langpack-zhCN.xpi
Source11:      http://kompozer.sourceforge.net/l10n/kpz08/kpz-langpack-zhTW.xpi

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc-c++ zip
# got from http://cvs.fedoraproject.org/viewvc/devel/seamonkey/seamonkey.spec?revision=1.51&view=markup : 
BuildRequires:  nspr-devel >= %{minimum_build_nspr_version}
BuildRequires:  nss-devel >= %{minimum_build_nss_version}
BuildRequires:  cairo-devel >= %{cairo_version}
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  zlib-devel
BuildRequires:  libIDL-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gtk2-devel
BuildRequires:  gnome-vfs2-devel
BuildRequires:  libgnome-devel
BuildRequires:  libgnomeui-devel
BuildRequires:  krb5-devel
BuildRequires:  pango-devel
BuildRequires:  freetype-devel >= 2.1.9
BuildRequires:  glib2-devel
BuildRequires:  libXt-devel
BuildRequires:  libXrender-devel
BuildRequires:  fileutils
BuildRequires:  perl
Requires:       mozilla-filesystem hunspell
Requires: nspr >= %{minimum_build_nspr_version}
Requires: nss >= %{minimum_build_nss_version}
Requires(post):         desktop-file-utils 
Requires(postun):       desktop-file-utils 
Provides:       nvu = 1
Obsoletes:      nvu < 1

%description
A complete web authoring system for linux desktop users that  makes managing
a web site a snap.  Now anyone can create web pages and manage a Web site
with no technical expertise or HTML knowledge.

Features:

* WYSIWYG editing of pages, making Web creation as easy as typing a
   letter with your word processor.
* Integrated file management via FTP.  Simply log in to your Web
   site and navigate through your files, editing Web pages on the
   fly, directly from your site.
* Reliable HTML code creation that works with today's most popular
   browsers.
* Jump between WYSIWYG editing mode and HTML using tabs.
* Tabbed editing to make working on multiple pages a snap.
* Powerful support for frames, forms, tables, and templates.

KompoZer is an unofficial branch of Nvu, previously developed by
Linspire Inc.


%prep
%setup -q -c %{name}-%{version}

%build
cd mozilla/
cp composer/config/mozconfig.fedora .mozconfig
## (I think this is ) for x64 and x32 compatibility 
 echo "ac_add_options --libdir %{_libdir}" >> .mozconfig
 echo "ac_add_options --with-default-mozilla-five-home=%{_libdir}/kompozer" >> .mozconfig

make -f client.mk build_all


%install
rm -rf %{buildroot}

pushd obj-kompozer/xpfe/components && %__make ; popd
pushd obj-kompozer && %__make install DESTDIR=%{buildroot} ;popd

# Remove internal myspell directory and myspell dicts.
# dh_install symlinks it to /usr/share/myspell where all myspell-* dicts place their stuff
rm -rf %{buildroot}/%{_libdir}/kompozer/components/myspell
# Remove exec bit from .js files to prevent lintian warnings.
chmod -x %{buildroot}/%{_libdir}/kompozer/components/*.js

rm -rf %{buildroot}/usr/include/
rm -rf %{buildroot}/%{_datadir}/idl/

#Menu entry
install -d -m755 %{buildroot}%{_datadir}/applications

cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Name=KompoZer
GenericName=Web Authoring System
Comment=Create Web Pages
Comment[es]=Crea páginas web
Comment[it]=Creare pagine Web
Categories=Development;WebDevelopment;Network;
TryExec=%{name}
Exec=%{name} %u
Icon=%{_libdir}/kompozer/icons/mozicon50.xpm
Terminal=false
MimeType=text/html;text/xml;text/css;text/x-javascript;text/javascript;application/x-php;text/x-php;application/xhtml+xml;
Type=Application
EOF
## installing kompozer.desktop
desktop-file-install --dir=%{buildroot}%{_datadir}/applications/ %{buildroot}%{_datadir}/applications/%{name}.desktop 

# manpage:m
install -d -m755 %{buildroot}%{_mandir}/man1/
install -m 644 %{SOURCE1} %{buildroot}%{_mandir}/man1/%{name}.1

# spellchecker support:
rm -rf %{buildroot}%{_libdir}/kompozer/dictionaries/
cd %{buildroot}%{_libdir}/kompozer
ln -s %{_datadir}/myspell %{buildroot}%{_libdir}/kompozer/dictionaries
# kompozer doesn't own it:
#rmdir %{buildroot}%{_datadir}/myspell/

# cleaning non used devel and debug files
rm %{buildroot}%{_bindir}/kompozer-config
rm -rf %{buildroot}%{_libdir}/pkgconfig/
rm -rf %{buildroot}%{_libdir}/debug/

# localization support
# TBD

%clean
rm -rf %{buildroot}

%post
update-desktop-database %{_datadir}/applications
/sbin/ldconfig

%postun
update-desktop-database %{_datadir}/applications
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc mozilla/LEGAL mozilla/LICENSE mozilla/README.txt
%dir %{_libdir}/kompozer
%{_bindir}/*
%{_libdir}/kompozer/*
%{_mandir}/man1/kompozer.1.gz
%{_datadir}/applications/kompozer.desktop

%changelog

* Mon Aug 9 2010 Ismael Olea <ismael@olea.org> 0.8-0.5.b3
- attending https://bugzilla.redhat.com/show_bug.cgi?id=519521#c8 suggestions
- minor stetic changes

* Tue Feb 23 2010 Ismael Olea <ismael@olea.org> 0.8-0.4.b3
- update to 0.8b3

* Tue Feb 23 2010 Ismael Olea <ismael@olea.org> 0.8-0.3.b2
- update to 0.8b2

* Mon Oct 12 2009 Ismael Olea <ismael@olea.org> 0.8-0.2.b1
- update to 0.8b1

* Mon Sep 21 2009 Ismael Olea <ismael@olea.org> 0.8-0.1.a4
- new version/release schema following guidelines

* Wed Sep 3 2009 Ismael Olea <ismael@olea.org> 0.8a4-4
- QA and cosmetic changes

* Wed Aug 26 2009 Ismael Olea <ismael@olea.org> 0.8a4-3
- QA and cosmetic changes

* Sun Jun 28 2009 Ismael Olea <ismael@olea.org> 0.8a4-2
- Cosmetic changes

* Wed May 13 2009 Ismael Olea <ismael@olea.org> 0.8a4-1
- update to 0.8a4

* Tue May 12 2009 Ismael Olea <ismael@olea.org> 0.8a3-3
- fixing paths to build in x64

* Thu May 7 2009 Ismael Olea <ismael@olea.org> 0.8a3-2
- man page from debian, icon on desktop file, using hunspell dicts

* Thu May 7 2009 Ismael Olea <ismael@olea.org> 0.8a3-1
- first version

Name:		xournal
Version:	0.4.5
Release:	9%{?dist}
Summary:	Notetaking, sketching, PDF annotation and general journal

Group:		Applications/Editors
License:	GPLv2
URL:		http://xournal.sourceforge.net/
Source0:	http://downloads.sourceforge.net/xournal/%{name}-%{version}.tar.gz
Patch0:		xournal-configure.in.patch
Patch1:		xournal-0.4.5-xoprint-len.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	gtk2-devel >= 2.10.0 
BuildRequires:	libgnomecanvas-devel >= 2.4.0 
BuildRequires:	libgnomeprintui22-devel >= 2.0.0 
%if 0%{?fedora} > 9 || 0%{?rhel} > 5
BuildRequires:	poppler-glib-devel >= 0.5.4
%else
BuildRequires:	poppler-devel >= 0.5.4
%endif
%if 0%{?rhel} > 4
BuildRequires:	autoconf, automake
%endif
BuildRequires:	freetype-devel >= 2.0.0
BuildRequires:	desktop-file-utils
BuildRequires:	ImageMagick
BuildRequires:	gettext

Requires:	poppler-utils
Requires:	ghostscript

%description
Xournal is an application for notetaking, sketching, keeping a journal and 
annotating PDFs. Xournal aims to provide superior graphical quality (subpixel 
resolution) and overall functionality.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
NOCONFIGURE=1 ./autogen.sh
CFLAGS="%optflags -DPACKAGE_LOCALE_DIR=\\\"\"%{_datadir}/locale\"\\\" -DPACKAGE_DATA_DIR=\\\"\"%{_datadir}\"\\\"" %configure
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p"

# xournal icons and mime icons
# create 16x16, 32x32, 64x64, 128x128 icons and copy the 48x48 icon
for s in 16 32 48 64 128 ; do
	%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps/
	convert -scale ${s}x${s} \
		pixmaps/%{name}.png \
		$RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps/%{name}.png
	%{__mkdir_p} ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/${s}x${s}/mimetypes
	pushd ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/${s}x${s}/mimetypes
	%{__ln_s} ../apps/xournal.png application-x-xoj.png
	%{__ln_s} application-x-xoj.png gnome-mime-application-x-xoj.png
	popd
done

# Desktop entry
%{__install} -p -m 0644 -D pixmaps/xournal.png ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/xournal.png
desktop-file-install --vendor fedora \
	--dir ${RPM_BUILD_ROOT}%{_datadir}/applications \
	xournal.desktop

# GNOME (shared-mime-info) MIME type registration
%{__install} -p -m 0644 -D xournal.xml ${RPM_BUILD_ROOT}%{_datadir}/mime/packages/xournal.xml

# KDE (legacy) MIME type registration
%{__install} -p -m 0644 -D x-xoj.desktop ${RPM_BUILD_ROOT}%{_datadir}/mimelnk/application/x-xoj.desktop

%find_lang %{name}

%post
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
update-mime-database %{_datadir}/mime > /dev/null 2>&1 || :
update-desktop-database %{_datadir}/applications > /dev/null 2>&1 || :

%postun
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
update-mime-database %{_datadir}/mime > /dev/null 2>&1 || :
update-desktop-database %{_datadir}/applications > /dev/null 2>&1 || :

%clean
%{__rm} -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/xournal
%{_datadir}/icons/hicolor/*x*/apps/%{name}.png
%{_datadir}/icons/hicolor/*x*/mimetypes/application-x-xoj.png
%{_datadir}/icons/hicolor/*x*/mimetypes/gnome-mime-application-x-xoj.png
%{_datadir}/pixmaps/xournal.png
%{_datadir}/applications/fedora-xournal.desktop
%{_datadir}/mime/packages/xournal.xml
%{_datadir}/mimelnk/application/x-xoj.desktop
%{_datadir}/xournal/
%doc AUTHORS ChangeLog COPYING



%changelog
* Wed Dec 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.4.5-9
- rebuild (poppler)

* Sat Nov 06 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.4.5-8
- rebuilt (poppler)

* Tue Oct  5 2010 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> 0.4.5-7
- rebuild (poppler)

* Thu Aug 19 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.4.5-6
- rebuild (poppler)

* Tue Jun 22 2010 Matthias Clasen <mclasen@redhat.com> - 0.4.5-5
- Rebuild against new poppler

* Tue Jun 01 2010 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> 0.4.5-4
- Add EPEL defines

* Tue Feb 16 2010 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> 0.4.5-3
- Remove freetype patch and add general configure.in patch to
  fix implicit DSO linking

* Wed Jan 06 2010 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> 0.4.5-2
- Added xournal-0.4.5-xoprint-len.patch to fix 64 bit systems

* Mon Oct 05 2009 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> 0.4.5-1
- New upstream release
- Removed xournal.xml, xournal.desktop and x-xoj.desktop sources as they are now in upstream source
- Updated gtk2 devel requirements to 2.10
- Added poppler-glib-devel to BR
- Added gettext BR
- Updated summary

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Sep 21 2008 Ville Skyttä <ville.skytta at iki.fi> - 0.4.2.1-2
- Fix Patch0:/%%patch mismatch (#463069)

* Mon Apr  7 2008 Jeremy Katz <katzj@redhat.com> - 0.4.2.1-1
- Update to 0.4.2.1 to fix problems with newer xorg

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.4.1-4
- Autorebuild for GCC 4.3

* Wed Oct 10 2007 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> 0.4.1-3
- Changed permission on xournal.png from 0755 to 0644

* Fri Sep 21 2007 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> 0.4.1-2
- Added freetype to build requires
- Created patch to add freetype to configure.in pkgconfig

* Thu Sep 20 2007 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> 0.4.1-1
- New upstream release
- Changed source to use name and version variables
- Updated xournal.desktop to reflect upstream changes
- Updated x-xoj.desktop to reflect upstream changes
- Updated license to reflect specific GPL version

* Mon Jun 11 2007 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> 0.3.3-5
- Added Requires for poppler-utils (#243750)
- Added Requires for ghostscript

* Wed May 30 2007 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> 0.3.3-4
- Added optflags and PACKAGE_DATA_DIR to CFLAGS

* Tue May 29 2007 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> 0.3.3-3
- Changed all commands to macros
- Removed icon sources and create icons in spec from xournal icon
- Added 64x64 and 128x128 icons
- Consolidated icon directories with wildcards
- Added timestamp preservation to install
- Removed desktop categories Application and X-Fedora
- Added NOCONFIGURE to autogen.sh to stop auto-conf from running twice
- Removed desktop-file-utils post and postun requires
- Removed manual from doc section; it is already installed by the package
- Changed xournal.desktop, xournal.xml and x-xoj.desktop from here documents to files
- Add ImageMagick buildrequires for convert command
- Separated BuildRequires into one per line for easier reading
- Added PACKAGE_LOCALE_DIR CFLAG to configure

* Fri May 18 2007 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> 0.3.3-2
- Added mimetype support for gnome and kde
- Made xournal.desktop a here document

* Sat May 12 2007 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> 0.3.3-1
- Initial version


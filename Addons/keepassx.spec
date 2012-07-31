Name:           keepassx
Version:        0.4.3
Release:        1%{?dist}
Summary:        Cross-platform password manager

Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://keepassx.sourceforge.net
Source0:        http://download.sf.net/keepassx/keepassx-%{version}.tar.gz
Patch1:         keepassx-0.3.3-gcc43.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  qt4-devel > 4.1, libXtst-devel, ImageMagick, desktop-file-utils

Requires:       hicolor-icon-theme

%description
KeePassX is an application for people with extremly high demands on secure
personal data management.
KeePassX saves many different information e.g. user names, passwords, urls,
attachemts and comments in one single database. For a better management
user-defined titles and icons can be specified for each single entry.
Furthermore the entries are sorted in groups, which are customizable as well.
The integrated search function allows to search in a single group or the
complete database.
KeePassX offers a little utility for secure password generation. The password
generator is very customizable, fast and easy to use. Especially someone who
generates passwords frequently will appreciate this feature.
The complete database is always encrypted either with AES (alias Rijndael) or
Twofish encryption algorithm using a 256 bit key. Therefore the saved
information can be considered as quite safe. KeePassX uses a database format
that is compatible with KeePass Password Safe for MS Windows.


%prep
%setup -q
%patch1 -p0 -b .gcc43


%build
export CFLAGS=$RPM_OPT_FLAGS
export CXXFLAGS=$RPM_OPT_FLAGS
qmake-qt4 PREFIX=%{_prefix}
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install INSTALL_ROOT=$RPM_BUILD_ROOT

# Use png in _datadir/icons/hicolor instead of xpm in pixmaps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/
convert $RPM_BUILD_ROOT%{_datadir}/pixmaps/keepassx.xpm \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/keepassx.png
rm -f $RPM_BUILD_ROOT%{_datadir}/pixmaps/keepassx.xpm

# Menu
sed -i -e 's/^Exec=keepassx$/Exec=keepassx %f/g' \
        $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop
desktop-file-install  --vendor fedora \
        --dir $RPM_BUILD_ROOT%{_datadir}/applications \
        --delete-original \
        --add-mime-type application/x-keepass \
        $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

# Associate KDB files
cat > x-keepass.desktop << EOF
[Desktop Entry]
Comment=
Hidden=false
Icon=keepassx.png
MimeType=application/x-keepass
Patterns=*.kdb;*.KDB
Type=MimeType
EOF
install -D -m 644 -p x-keepass.desktop \
  $RPM_BUILD_ROOT%{_datadir}/mimelnk/application/x-keepass.desktop


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null ||:
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null ||:
update-mime-database %{_datadir}/mime &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc share/keepassx/license.html
%{_bindir}/keepassx
%{_datadir}/keepassx
%{_datadir}/applications/*.desktop
%{_datadir}/mimelnk/application/*.desktop
%{_datadir}/mime/packages/*.xml
%{_datadir}/icons/hicolor/*/apps/keepassx.png


%changelog
* Sun Mar 14 2010 Aurelien Bompard <abompard@fedoraproject.org> -  0.4.3-1
- version 0.4.3

* Sun Jan 03 2010 Aurelien Bompard <abompard@fedoraproject.org> -  0.4.1-1
- version 0.4.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Apr 18 2009 Aurelien Bompard <abompard@fedoraproject.org> 0.4.0-2
- add patch0 to fix bug 496035

* Thu Mar 26 2009 Aurelien Bompard <abompard@fedoraproject.org> 0.4.0-1
- version 0.4.0
- drop patch0 (upstream)

* Thu Mar 12 2009 Aurelien Bompard <abompard@fedoraproject.org> 0.3.4-3
- backport fix from upstream for bug #489820

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Nov 11 2008 Aurelien Bompard <abompard@fedoraproject.org> 0.3.4-1
- version 0.3.4

* Sat Aug 23 2008 Aurelien Bompard <abompard@fedoraproject.org> 0.3.3-2
- rebase patch for version 0.3.3

* Tue Aug 12 2008 Aurelien Bompard <abompard@fedoraproject.org> 0.3.3-1
- version 0.3.3

* Mon Jul 21 2008 Aurelien Bompard <abompard@fedoraproject.org> 0.3.2-1
- version 0.3.2

* Sun Mar 16 2008 Aurelien Bompard <abompard@fedoraproject.org> 0.3.1-1
- version 0.3.1
- drop xdg patch, keepassx now uses QDesktopServices

* Wed Mar 05 2008 Aurelien Bompard <abompard@fedoraproject.org> 0.3.0-3.a
- version 0.3.0a

* Wed Mar 05 2008 Aurelien Bompard <abompard@fedoraproject.org> 0.3.0-2
- patch for gcc 4.3

* Sun Mar 02 2008 Aurelien Bompard <abompard@fedoraproject.org> 0.3.0-1
- version 0.3.0
- drop helpwindow patch (feature dropped upstream)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.2.2-5
- Autorebuild for GCC 4.3

* Sun Oct 07 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.2.2-4
- use xdg-open instead of htmlview

* Sat Aug 25 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.2.2-3
- fix license tag
- rebuild for BuildID

* Wed Jun 27 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.2.2-2
- fix help button
- use htmlview instead of the hardcoded konqueror

* Sun Mar 04 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.2.2-1
- initial package

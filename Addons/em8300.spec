%global rpmver  %(v=$(rpmbuild --version | sed -e 's/.* //') ; echo ${v:-0})
#global prever  rc1

Name:           em8300
Version:        0.18.0
Release:        2%{?prever:.%{prever}}%{?dist}
Summary:        DXR3/Hollywood Plus MPEG decoder card support tools

Group:          Applications/System
License:        GPLv2+
URL:            http://dxr3.sourceforge.net/
#Source0: http://dxr3.sourceforge.net/download/em8300-%{version}%{?prever:-%{prever}}.tar.gz with modules/em8300.uc removed
#Source0:        %{name}-nofirmware-%{version}%{?prever:-%{prever}}.tar.lzma
Source0:        http://downloads.sourceforge.net/dxr3/%{name}-nofirmware-%{version}%{?prever:-%{prever}}.tar.gz
Source1:        %{name}.console.perms
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel
BuildRequires:  desktop-file-utils
BuildRequires:  alsa-lib
#Requires:       em8300-kmod >= %{version}
# udev >= 136-1 for the video group
Requires:       udev >= 136-1
Requires:       alsa-lib
Requires:       %{_sysconfdir}/security/console.perms.d
Provides:       em8300-kmod-common = %{version}-%{release}

%description
%{summary}.

%package        utils
Summary:        GUI utilities for DXR3/Hollywood plus MPEG decoder cards
Group:          User Interface/X Hardware Support
Requires:       %{name} = %{version}-%{release}

%description    utils
%{summary}.

%package        devel
Summary:        Development files for DXR3/Hollywood Plus MPEG decoder cards
Group:          Development/Libraries
%if "%{rpmver}" >= "4.6.0"
BuildArch:      noarch
%endif
# Does not require main package on purpose: #189400
Requires:       kernel-headers

%description    devel
%{summary}.


%prep
%setup -q -n %{name}-%{version}%{?prever:-%{prever}}
echo "Icon=redhat-sound_video" >> overlay/dxr3view.desktop
sed -i -e 's/microcode_extract.pl/em8300-mc_ex/' scripts/microcode_extract.pl


%build
%configure --disable-dependency-tracking
make %{?_smp_mflags} LDFLAGS="-lX11 -lm"


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

for f in */*.desktop ; do
  desktop-file-install --vendor=fedora --mode=644 \
    --dir=$RPM_BUILD_ROOT%{_datadir}/applications $f
done
install -Dpm 644 dhc/dhc.xpm \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/dhc.xpm

install -Dpm 644 modules/em8300-udev.rules \
  $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/60-%{name}.rules

install -Dpm 644 %{SOURCE1} \
  $RPM_BUILD_ROOT%{_sysconfdir}/security/console.perms.d/60-%{name}.perms

mv $RPM_BUILD_ROOT%{_datadir}/em8300/microcode_extract.pl \
  $RPM_BUILD_ROOT%{_bindir}/em8300-mc_ex

cat /dev/null > %{name}.files
for alsadir in %{_datadir}/alsa %{_sysconfdir}/alsa ; do
    if [ -f "$RPM_BUILD_ROOT$alsadir/cards/EM8300.conf" ] ; then
        echo "$alsadir/cards/EM8300.conf" > %{name}.files
        break
    fi
done


%check
if [ ! -s %{name}.files ] ; then
    echo "ERROR: EM8300.conf not installed in expected location"
    exit 1
fi


%clean
rm -rf $RPM_BUILD_ROOT


%post utils
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun utils
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans utils
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README modules/README-modoptions
%config(noreplace) %{_sysconfdir}/security/console.perms.d/*-%{name}.perms
%config(noreplace) %{_sysconfdir}/udev/rules.d/*-%{name}.rules
%{_bindir}/em8300setup
%{_mandir}/man1/em8300setup.1*

%files utils
%defattr(-,root,root,-)
%doc overlay/configs/
%{_bindir}/autocal
%{_bindir}/dhc
%{_bindir}/dxr3view
%{_bindir}/em8300-mc_ex
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/48x48/apps/dhc.xpm

%files devel
%defattr(-,root,root,-)
%{_includedir}/linux/em8300.h
%{_datadir}/em8300/


%changelog
* Sun Feb 14 2010 Felix Kaechele <heffer@fedoraproject.org> - 0.18.0-2
- fixed implicit DSO-linking

* Tue Dec 29 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.18.0-1
- Update to 0.18.0.
- Don't create the video group, require udev >= 136-1 for it.
- Drop mostly obsolete README-modprobe.conf.

* Fri Dec 25 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.17.4-1
- Update to 0.17.4.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Felix Kaechele <heffer@fedoraproject.org> - 0.17.3-1
- new upstream version

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.17.2-2
- Improve icon cache refresh scriptlets, move them to -utils where they belong.
- Make -devel subpackage noarch when built with rpmbuild >= 4.6.0.

* Sun Nov 09 2008 Felix Kaechele <felix at fetzig dot org> - 0.17.2-1
- 0.17.2

* Tue Oct 14 2008 Ville Skyttä <ville.skytta@iki.fi> - 0.17.2-0.1.rc1
- 0.17.2-rc1.

* Sun Sep 14 2008 Ville Skyttä <ville.skytta@iki.fi> - 0.17.1-2
- Adapt to a couple of different alsa/cards dir locations.

* Thu Aug 14 2008 Ville Skyttä <ville.skytta@iki.fi> - 0.17.1-1
- 0.17.1.

* Mon Jun  9 2008 Ville Skyttä <ville.skytta@iki.fi> - 0.17.0-1
- 0.17.0.

* Sat Apr 12 2008 Ville Skyttä <ville.skytta@iki.fi> - 0.17.0-0.1.rc1
- 0.17.0-rc1.

* Tue Feb  5 2008 Ville Skyttä <ville.skytta@iki.fi> - 0.16.4-1
- 0.16.4.
- Drop WSS patch, it no longer applies.
- Prune pre-0.16.0 changelog entries.

* Wed Nov 21 2007 Ville Skyttä <ville.skytta@iki.fi> - 0.16.3-2
- Drop dependency on em8300-kmod.

* Sat Aug 18 2007 Ville Skyttä <ville.skytta@iki.fi> - 0.16.3-1
- 0.16.3.

* Fri Aug 10 2007 Ville Skyttä <ville.skytta@iki.fi> - 0.16.3-0.1.rc3
- 0.16.3-rc3.
- License: GPLv2+

* Fri Jul 20 2007 Ville Skyttä <ville.skytta@iki.fi> - 0.16.3-0.1.rc2
- 0.16.3-rc2.

* Wed Jul 11 2007 Ville Skyttä <ville.skytta@iki.fi> - 0.16.3-0.1.rc1
- 0.16.3-rc1, fixes #241041.
- Update icon cache and group handling to current guidelines/drafts.

* Mon May  7 2007 Ville Skyttä <ville.skytta@iki.fi> - 0.16.2-1
- 0.16.2.

* Wed Apr  4 2007 Ville Skyttä <ville.skytta@iki.fi> - 0.16.2-0.1.rc1
- 0.16.2-rc1.
- Update examples in README-modprobe.conf.

* Thu Mar  1 2007 Ville Skyttä <ville.skytta@iki.fi> - 0.16.1-1
- 0.16.1.

* Sat Feb 24 2007 Ville Skyttä <ville.skytta@iki.fi> - 0.16.1-0.1.rc2
- 0.16.1-rc2.

* Tue Dec 26 2006 Ville Skyttä <ville.skytta@iki.fi> - 0.16.0-3
- Ship console.perms.d snippet uncommented (#206700 fixed).

* Fri Dec 22 2006 Ville Skyttä <ville.skytta@iki.fi> - 0.16.0-2
- Eliminate some file based dependencies.

* Sun Nov 26 2006 Ville Skyttä <ville.skytta@iki.fi> - 0.16.0-1
- 0.16.0.
- Drop X-Fedora category from desktop entries.

%define name    stardict
%define version 3.0.1

Name:		%{name}
Summary:        A powerful dictionary platform written in GTK+2
Version:        %{version}
Release:        22%{?dist}
Group:          Applications/System
License:        GPLv3
URL:            http://stardict.sourceforge.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1:        defaultdict.cfg
Patch0:         stardict-3.0.1.gcc43.patch
Patch1:         transparent_trayicon.patch
Patch2:         stardict-3.0.1-10.gucharmap.patch
Patch3:         stardict-3.0.1-13.bz441209.patch
Patch4:         stardict-3.0.1.gcc44.patch
Patch5:         stardict-3.0.1-20.security.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: enchant, espeak, gucharmap >= 2.22.1, libbonobo >= 2.2.0, libgnome >= 2.2.0, libgnomeui >= 2.2.0, libsigc++20 >= 2.0.17
#Requires: festival, speech-tools
Requires(preun): GConf2
Requires(post): GConf2, scrollkeeper
Requires(postun): scrollkeeper

BuildRequires: autoconf, automake, libtool
BuildRequires: desktop-file-utils, enchant-devel, gettext,  intltool, libgnomeui-devel >= 2.2.0, libsigc++20-devel, libtool, perl-XML-Parser, scrollkeeper

#Bz #641955: remove gucharmap dependency as gucharmap use gtk3, but stardict still use gtk2.
%if 0%{?fedora} <=13
BuildRequires: gucharmap-devel >= 2.22.1
%endif
#BuildRequires: festival-devel, speech-tools-devel, espeak-devel

%description
StarDict is a Cross-Platform and international dictionary written in Gtk2.
It has powerful features such as "Glob-style pattern matching,"
"Scan selection word," "Fuzzy query," etc.

%prep
%setup -q
%patch0 -p1 -b .1-gcc43
%patch1 -p1 -b .2-trayicon
%patch2 -p1 -b .3-gucharmap
%patch3 -p1 -b .4-bz441209
%patch4 -b .5-gcc44
%patch5 -p1 -b .6-netdict

# Remove unneeded sigc++ header files to make it sure
# that we are using system-wide libsigc++
# (and these does not work on gcc43)
# 
find src/sigc++* -name \*.h -or -name \*.cc | xargs rm -f


%build
%{__aclocal}
%{__autoconf}
%{__libtoolize}
%configure --disable-schemas-install --disable-festival --disable-espeak --disable-gucharmap
make -k %{_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p" install

desktop-file-install --vendor fedora --delete-original	\
  --dir $RPM_BUILD_ROOT%{_datadir}/applications		\
  $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

# copy config file of locale specific default dictionaries
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

rm -f `find $RPM_BUILD_ROOT%{_libdir}/stardict/plugins -name "*.la"`
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-, root, root)
%{_bindir}/stardict
%{_datadir}/applications/*.desktop
%{_datadir}/stardict
%{_libdir}/stardict
%{_datadir}/idl/*
%{_libdir}/bonobo/servers/*.server
%{_datadir}/pixmaps/stardict.png
%config(noreplace) %{_sysconfdir}/gconf/schemas/*.schemas
%config(noreplace) %dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/defaultdict.cfg
%{_datadir}/omf/*
%{_mandir}/man1/*
%doc %{_datadir}/gnome/help/stardict
%doc README COPYING ChangeLog AUTHORS doc/FAQ doc/HACKING doc/HowToCreateDictionary doc/StarDictFileFormat doc/Translation


%preun
if [ "$1" -gt 1 ] ; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/stardict.schemas >/dev/null || :
fi

%post
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/stardict.schemas >/dev/null || :
if which scrollkeeper-update>/dev/null 2>&1; then scrollkeeper-update; fi

%postun
if which scrollkeeper-update>/dev/null 2>&1; then scrollkeeper-update; fi

%changelog
* Thu Oct 14 2010 Ding-Yi Chen <dchen at redhat.com> - 3.0.1-22
- Fixed Bz #641955: remove gucharmap dependency as gucharmap use gtk3, but stardict still use gtk2.

* Sun Dec 27 2009 Caius 'kaio' Chance <k at kaio.me> - 3.0.1-21
- rebuilt

* Sun Dec 27 2009 Caius 'kaio' Chance <k at kaio.me> - 3.0.1-20
- Disable netdict by default and set warning for security.

* Thu Dec 17 2009 Caius 'kaio' Chance <k at kaio.me> - 3.0.1-19
- Resolves: rhbz#475904: Disabled espeak for instance as espeak has problems when it is built with pulseaudio.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Apr 25 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 3.0.1-17
- Fix FTBFS: added stardict-3.0.1.gcc44.patch

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec  2 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 3.0.1-15
- BR libtool and run libtoolize to fix build with libtool2.
- Add preun scriptlet for GConf2 uninstall rule.
- Build with SMP make flags.
- Install with -p.

* Fri Aug 29 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 3.0.1-14.fc10
- Include /etc/stardict directory

* Mon Aug 04 2008 Caius Chance <cchance@redhat.com> - 3.0.1-13.fc10
- Resolves: rhbz#441209
  - Enable appropriate locale based dictionaries in user's first time usage.

* Thu Jul 17 2008 Caius Chance <cchance@redhat.com> - 3.0.1-12.fc10
- Resolves: rhbz#455685 (Broken dependency of bonobo-activitation.)

* Mon Jul 14 2008 Caius Chance <cchance@redhat.com> - 3.0.1-11.1.fc10
- Enable gucharmap-2.

* Mon Jul 14 2008 Caius Chance <cchance@redhat.com> - 3.0.1-11.fc10
- Disable gucharmap for incompatibility with gucharmap-2.
- Refactorized Requires and BuildRequires tags.

* Thu Jul 10 2008 Caius Chance <cchance@redhat.com> - 3.0.1-10.fc10
- Rebuilt for gucharmap updation 2.22.1 and pkgconfig .ac name change.

* Mon Jun 30 2008 Caius Chance <cchance@redhat.com> - 3.0.1-9.fc10
- Fixed broken dependencies with gucharmap.

* Fri Feb 29 2008 Hu Zheng <zhu@redhat.com> - 3.0.1-8
- Forget commit first.

* Fri Feb 29 2008 Hu Zheng <zhu@redhat.com> - 3.0.1-7
- Add trayicon transparent patch.

* Thu Feb 28 2008 Hu Zheng <zhu@redhat.com> - 3.0.1-6
- OK

* Wed Feb 27 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 3.0.1-5
- More gcc43 fix

* Wed Feb 27 2008 Hu Zheng <zhu@redhat.com> - 3.0.1-4
- small fix.

* Tue Feb 26 2008 Hu Zheng <zhu@redhat.com> - 3.0.1-3
- Gcc-4.3 compile fix.

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.0.1-2
- Autorebuild for GCC 4.3

* Thu Nov 08 2007 Hu Zheng <zhu@redhat.com> - 3.0.1-1
- Update to upstream.

* Mon Sep 03 2007 Hu Zheng <zhu@redhat.com> - 3.0.0-4
- Small fix on spec file. Use desktop-file-install.

* Thu Aug 23 2007 Hu Zheng <zhu@redhat.com> - 3.0.0-3
- Add floatwin and espeak patch.

* Mon Aug 13 2007 Hu Zheng <zhu@redhat.com> - 3.0.0-1
- Update to upstream.

* Fri Jun 22 2007 Hu Zheng <zhu@redhat.com> - 2.4.8-3
- Add dic and treedict directory.

* Thu Jan 16 2007 Mayank Jain <majain@redhat.com>
- Removed gnome support from the spec file (--disable-gnome-support) for bug 213850
- Commented the gnome related directives.

* Thu Jan 12 2007 Mayank Jain <majain@redhat.com>
- Added perl-XML-Parser as BuildRequires

* Thu Jan 11 2007 Mayank Jain <majain@redhat.com>
* Thu Jan 11 2007 Mayank Jain <majain@redhat.com>
- Updated to version 2.4.8
- Removed invalid patch - stardict-2.4.5-invalid-cplusplus.patch
- Reset release number to 2.4.8-1
- Added dist-tag to the release version directive

* Tue Jul 18 2006 Jesse Keating <jkeating@redhat.com> - 2.4.5-5
- rebuild
- add gettext as br

* Mon Jun 12 2006 Mayank Jain <majain@redhat.com>
- Updated package description

* Mon Jun 05 2006 Jesse Keating <jkeating@redhat.com>
- Added missing BuildRequires scrollkeeper
- Added Requires(post) and (postun) accordingly

* Tue Apr 18 2006 Mayank Jain <majain@redhat.com>
- Corrected spelling mistakes in the description section, RH bug #161777

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.4.5-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.4.5-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 13 2006 Leon Ho <llch@redhat.com> 2.4.5-2
- added in patch to fix #176890

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Sep 19 2005 Leon Ho <llch@redhat.com> 2.4.5-1
- Upgraded to 2.4.5

* Thu Mar 17 2005 Leon Ho <llch@redhat.com> 2.4.4-3
- rebuilt

* Thu Feb 03 2005 Leon Ho <llch@redhat.com> 2.4.4-2
- Reupdate the spec file
- Upgrade to 2.4.4

* Sun Nov 28 2004 Hu Zheng  <huzheng_001@163.com> 2.4.4
- Public release of StarDict 2.4.4.

* Thu Feb 19 2004 Hu Zheng <huzheng_001@163.com> 2.4.3
- Public release of StarDict 2.4.3.

* Sat Nov 15 2003 Hu Zheng <huzheng_001@163.com> 2.4.2
- Public release of StarDict 2.4.2.

* Sun Sep 28 2003 Hu Zheng <huzheng_001@163.com> 2.4.1
- Public release of StarDict 2.4.1.

* Thu Aug 28 2003 Hu Zheng <huzheng_001@163.com> 2.4.0
- Public release of StarDict 2.4.0.

* Sat Jun 28 2003 Hu Zheng <huzheng_001@163.com> 2.2.1
- Public release of StarDict 2.2.1.

* Sun Jun 01 2003 Hu Zheng <huzheng_001@163.com> 2.2.0
- Public release of StarDict 2.2.0.

* Sun May 18 2003 Hu Zheng <huzheng_001@163.com> 2.1.0
- Public release of StarDict 2.1.0.

* Fri May 02 2003 Hu Zheng <huzheng_001@163.com> 2.0.0
- Public release of StarDict 2.0.0.

* Wed Apr  9 2003 Hu Zheng <huzheng_001@163.com> 2.0.0-pre2
- Second public preview release of StarDict 2.

* Sun Mar 30 2003 Hu Zheng <huzheng_001@163.com> 2.0.0-pre1
- First public preview release of StarDict 2.

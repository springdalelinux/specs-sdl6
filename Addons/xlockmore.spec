Summary: Screen lock and screen saver
Name: xlockmore
Version: 5.31
Release: 2%{?dist}
License: BSD
Group: Amusements/Graphics
URL: http://www.tux.org/~bagleyd/xlockmore.html
Source0: http://www.tux.org/~bagleyd/xlock/xlockmore-5.31/xlockmore-5.31.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: pam-devel esound-devel
BuildRequires: mesa-libGL-devel mesa-libGLU-devel
BuildRequires: desktop-file-utils libXdmcp-devel
BuildRequires: lesstif-devel gtk2-devel
BuildRequires: libXau-devel

%description
Locks the local X display until a password is entered.

%package motif
Group: Amusements/Graphics
Summary: Motif based frontend for xlockmore
Requires: %{name} = %{version}-%{release}

%description motif
Motif based frontend for xlockmore.

%package gtk
Group: Amusements/Graphics
Summary: GTK based frontend for xlockmore
Requires: %{name} = %{version}-%{release}

%description gtk
GTK based frontend for xlockmore.

%prep
%setup -q

%{__sed} -i -e "s,/lib,/%{_lib},g" configure
%{__sed} -i -e "s,@XLOCKLIBS@$,@XLOCKLIBS@ -laudiofile," modes/Makefile.in

%build
%configure \
	--with-crypt --enable-pam --enable-syslog --disable-setuid
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__install} -D -m0755 xlock/xlock %{buildroot}%{_bindir}/xlock
%{__install} -D -m0755 xmlock/xmlock %{buildroot}%{_bindir}/xmlock
%{__install} -D -m0755 xglock/xglock %{buildroot}%{_bindir}/xglock
%{__install} -p -D -m0644 xlock/xlock.man %{buildroot}%{_mandir}/man1/xlock.1
%{__install} -p -D -m0644 xlock/XLock.ad %{buildroot}%{_libdir}/X11/app-defaults/XLock
%{__install} -p -D -m0644 xmlock/XmLock.ad %{buildroot}%{_libdir}/X11/app-defaults/XmLock
%{__chmod} 644 README
%{__chmod} 644 docs/Revisions


%{__mkdir_p} %{buildroot}%{_sysconfdir}/pam.d
cat > %{buildroot}%{_sysconfdir}/pam.d/xlock << EOF
#%PAM-1.0
auth       include      system-auth
account    include      system-auth
password   include      system-auth
session    include      system-auth
EOF

%{__mkdir_p} %{buildroot}%{_datadir}/applications

cat >> %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Xlock
Comment=Screen Saver
Encoding=UTF-8
Icon=gnome-lockscreen.png
Exec=xlock
Terminal=false
Type=Application
EOF

desktop-file-install \
	--vendor=fedora \
	--dir %{buildroot}%{_datadir}/applications \
	--delete-original \
	--add-category X-Fedora \
	--add-category Application \
	--add-category Graphics \
        %{buildroot}%{_datadir}/applications/%{name}.desktop

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc README docs/*
%doc %{_mandir}/man1/xlock.1*
%{_bindir}/xlock
%{_libdir}/X11/app-defaults/XLock
%config(noreplace) %{_sysconfdir}/pam.d/xlock
%{_datadir}/applications/*

%files motif
%defattr(-, root, root, 0755)
%{_bindir}/xmlock
%{_libdir}/X11/app-defaults/XmLock

%files gtk
%defattr(-, root, root, 0755)
%{_bindir}/xglock

%changelog
* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 08 2010 Adrian Reber <adrian@lisas.de> - 5.31-1
- updated to 5.31
- removed xlockmore-fix_petri.patch

* Sat May 08 2010 Adrian Reber <adrian@lisas.de> - 5.28-2
- fixed "FTBFS xlockmore-5.28-1.fc12: ImplicitDSOLinking" (#564929)

* Sun Aug 30 2009 Adrian Reber <adrian@lisas.de> - 5.28-1
- updated to 5.28
- applied patch to fix "xlock -mode petri segfaults with 32 bit displays" (#518379)

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.26.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.26.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Aug 09 2008 Adrian Reber <adrian@lisas.de> - 5.26.1-1
- updated to 5.26.1

* Mon Feb 18 2008 Adrian Reber <adrian@lisas.de> - 5.25-1
- updated to 5.25

* Sat Oct 13 2007 Adrian Reber <adrian@lisas.de> - 5.24-1
- updated to 5.24

* Tue Feb 08 2007 Adrian Reber <adrian@lisas.de> - 5.23-1
- updated to 5.23

* Tue Sep 12 2006 Adrian Reber <adrian@lisas.de> - 5.22-3
- rebuilt
- swtiched to lesstif

* Sun Jul 09 2006 Adrian Reber <adrian@lisas.de> - 5.22-2
- rebuild for new freetype

* Mon May 01 2006 Adrian Reber <adrian@lisas.de> - 5.22-1
- updated to 5.22
- changed pam file to use include instead of pam_stack.so

* Tue Feb 21 2006 Adrian Reber <adrian@lisas.de> - 5.21-1
- updated to 5.21

* Fri Dec 16 2005 Adrian Reber <adrian@lisas.de> - 5.20.1-1
- updated to 5.20.1
- changes for modular X
- removed "GENTOO" hack

* Sun Aug 21 2005 Adrian Reber <adrian@lisas.de> - 5.19-1
- updated to 5.19
- upstream included a fix for (BZ #161740), but "GENTOO" needs
  to be defined during compilation

* Mon Jun 27 2005 Adrian Reber <adrian@lisas.de> - 5.18-3
- included patch to make it work again with PAM (BZ #161740)

* Fri Jun 17 2005 Adrian Reber <adrian@lisas.de> - 5.18-2
- update to 5.18

* Wed Apr 13 2005 Adrian Reber <adrian@lisas.de> - 5.16-1
- update to 5.16

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Thu Feb 24 2005 Adrian Reber <adrian@lisas.de> - 5.15-1
- update to 5.15
- moved motif and gtk2 frontend to subpackages
- build with pam support
- added .desktop file

* Sun Dec 12 2004 Dries Verachtert <dries@ulyssis.org> 5.14.1-1
- Update to release 5.14.1.

* Thu Oct 28 2004 Dries Verachtert <dries@ulyssis.org> 5.13-1
- update to release 5.13

* Thu May 27 2004 Dries Verachtert <dries@ulyssis.org> 5.12-1
- update to 5.12

* Sun Jan 11 2004 Dries Verachtert <dries@ulyssis.org> 5.10-2
- cleanup of spec file

* Thu Dec 25 2003 Dries Verachtert <dries@ulyssis.org> 5.10-1
- first packaging for Fedora Core 1

Name: bitmap
Version: 1.0.3
Release: 7%{?dist}
Summary: Bitmap editor and converter utilities for the X Window System
Group: User Interface/X
Url: http://www.x.org
Source0: http://xorg.freedesktop.org/releases/individual/app/%{name}-%{version}.tar.bz2
Source1: bitmap.desktop
Source2: bitmap.png
License: MIT
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# the bitmap-devel corresponds only with bitmap files. They are needed
# by the base package, so this Provides is added
Provides: %{name}-devel = %{version}-%{release}
# other xorg apps are called like that
Provides: xorg-x11-%{name} = %{version}-%{release}
Provides: xorg-x11-%{name}-devel = %{version}-%{release}

# libXaw-devel requires libXmu-devel 
# libXmu-devel requires libX11-devel, libXt-devel, xorg-x11-util-macros
BuildRequires: xbitmaps-devel libXaw-devel libXext-devel
BuildRequires: desktop-file-utils pkgconfig
# also needed at runtime
Requires: xbitmaps

%description
Bitmap provides a bitmap editor and misc converter utilities for the X
Window System.

The package also includes files defining bitmaps associated with the 
Bitmap x11 editor.

%prep
%setup -q


%build
%configure --disable-dependency-tracking
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL='install -p'

desktop-file-install --vendor fedora                            \
        --dir %{buildroot}%{_datadir}/applications         \
        %{SOURCE1}

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
install -p -m644 %{SOURCE2} %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/


%clean
rm -rf %{buildroot}


%post
# update the icon cache, if it exists
if [ -d %{_datadir}/icons/hicolor -a -x %{_bindir}/gtk-update-icon-cache ]
then
  touch %{_datadir}/icons/hicolor
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi

%postun
# update the icon cache, if it exists
if [ -d %{_datadir}/icons/hicolor -a -x %{_bindir}/gtk-update-icon-cache ]
then
  touch %{_datadir}/icons/hicolor
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi


%files
%defattr(-,root,root,-)
# COPYING is a stub!
%doc ChangeLog
%{_bindir}/atobm
%{_bindir}/bmtoa
%{_bindir}/bitmap
%{_includedir}/X11/bitmaps/*
%{_datadir}/X11/app-defaults/Bitmap*
%{_datadir}/applications/*bitmap*
%{_datadir}/icons/hicolor/32x32/apps/bitmap.png
%{_mandir}/man1/*.1*

%changelog
* Tue Dec 15 2009 Stepan Kasal <skasal@redhat.com> - 1.0.3-7
- silence scriptlets

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.3-4
- Autorebuild for GCC 4.3

* Mon Dec 17 2007 Patrice Dumas <pertusus@free.fr> 1.0.3-3
- keep timestamps

* Mon Jan 29 2007 Patrice Dumas <pertusus@free.fr> 1.0.3-2
- update to 1.0.3

* Tue Oct 10 2006 Patrice Dumas <pertusus@free.fr> 1.0.2-3
- use consistently %%{buildroot}
- provides xorg-x11-%%{name}-devel

* Mon Oct  9 2006 Patrice Dumas <pertusus@free.fr> 1.0.2-2
- buildrequires pkgconfig, libXext-devel

* Sun Sep  3 2006 Patrice Dumas <pertusus@free.fr> 1.0.2-1
- Packaged for fedora extras

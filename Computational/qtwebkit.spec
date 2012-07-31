Name: qtwebkit
Version: 2.1.1
Release: 1%{?dist}
Summary: Qt WebKit bindings
Group: System Environment/Libraries
License: LGPLv2 with exceptions or GPLv3 with exceptions
URL: http://trac.webkit.org/wiki/QtWebKit
## start with, http://gitorious.org/webkit/qtwebkit/archive-tarball/qtwebkit-2.1.1
## then rm -rf *Tests/ , and, ... 
## zcat qtwebkit-developers-qtwebkit-qtwebkit-2.1.1.tar.gz | xz > qtwebkit-developers-qtwebkit-qtwebkit-2.1.1.tar.xz
Source0: qtwebkit-developers-qtwebkit-qtwebkit-2.1.1.tar.xz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

# use phonon instead of QtMultimediaKit (from qt-mobility)
Patch1: webkit-qtwebkit-2.1-use_phonon.patch

# search /usr/lib{,64}/mozilla/plugins-wrapped for browser plugins too
Patch2: webkit-qtwebkit-2.1-pluginpath.patch

# include JavaScriptCore -debuginfo too
Patch3: webkit-qtwebkit-2.1-javascriptcore-debuginfo.patch

BuildRequires: bison
BuildRequires: chrpath
BuildRequires: flex
BuildRequires: gperf
BuildRequires: libicu-devel
BuildRequires: pcre-devel
BuildRequires: perl
BuildRequires: qt4-devel
# for qtlocation and qtmultimedia
BuildRequires: qt-mobility-devel
BuildRequires: sqlite-devel

## only if applying patch1 above, else use qt-mobility's qtmultimedia
%if 0
BuildRequires: phonon-devel
Requires: qt4%{?_isa} >= %{_qt4_version}
%global phonon_ver %(pkg-config --modversion phonon 2>/dev/null || echo 4.5.0)
Requires: phonon%{?_isa} >= %{phonon_ver}
%endif

Obsoletes: qt-webkit < 1:4.7.3
Provides: qt-webkit = 2:%{version}-%{release}
Provides: qt4-webkit = 2:%{version}-%{release}
Provides: qt4-webkit%{?_isa} = 2:%{version}-%{release}

%description
%{summary}

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
# when qt_webkit_version.pri was moved from qt-devel => qt-webkit-devel
%if 0%{?fedora}
Conflicts: qt-devel < 1:4.7.2-9
%endif
Requires: qt4-devel
Obsoletes: qt-webkit-devel < 1:4.7.3
Provides:  qt-webkit-devel = 2:%{version}-%{release}
Provides:  qt4-webkit-devel = 2:%{version}-%{release}
Provides:  qt4-webkit-devel%{?_isa} = 2:%{version}-%{release}

%description devel
%{summary}.


%prep
%setup -q -n webkit-qtwebkit 

#patch1 -p1 -b .use_phonon
%patch2 -p1 -b .pluginpath
# workaround memory exhaustion during linking of libQtWebKit
%ifnarch s390
%patch3 -p1 -b .javascriptcore_debuginfo
%endif

# build script assumes this is present
mkdir WebKitLibraries ||:


%build 

PATH=%{_qt4_bindir}:$PATH; export PATH
QTDIR=%{_qt4_prefix}; export QTDIR

WebKitTools/Scripts/build-webkit \
  --makeargs="%{?_smp_mflags}" \
  --qmake=%{_qt4_qmake} \
  --qt \
  --release


%install
rm -rf %{buildroot} 

make install INSTALL_ROOT=%{buildroot} -C WebKitBuild/Release

## HACK, there has to be a better way
chrpath --list   %{buildroot}%{_qt4_libdir}/libQtWebKit.so.4.8.1 ||:
chrpath --delete %{buildroot}%{_qt4_libdir}/libQtWebKit.so.4.8.1 ||:
%if 0%{?_qt4_importdir:1}
chrpath --list   %{buildroot}%{_qt4_importdir}/QtWebKit/libqmlwebkitplugin.so ||:
chrpath --delete %{buildroot}%{_qt4_importdir}/QtWebKit/libqmlwebkitplugin.so ||:
%endif


%clean
rm -rf %{buildroot} 


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_qt4_libdir}/libQtWebKit.so.4*
%if 0%{?_qt4_importdir:1}
%{_qt4_importdir}/QtWebKit/
%endif

%files devel
%defattr(-,root,root,-)
%{_qt4_datadir}/mkspecs/modules/qt_webkit_version.pri
%{_qt4_headerdir}/QtWebKit/
%{_qt4_libdir}/libQtWebKit.prl
%{_qt4_libdir}/libQtWebKit.so
%{_libdir}/pkgconfig/QtWebKit.pc


%changelog
* Tue May 24 2011 Than Ngo <than@redhat.com> - 2.1.1-1
- 2.1.1
- fixups for qt-4.6.x (el6)

* Mon May 23 2011 Rex Dieter <rdieter@fedoraproject.org> 2.1-4
- use qt-mobility after all
- backport javascriptcore_debuginfo patch
- fixups for qt-4.6.x (el6)

* Fri Apr 22 2011 Rex Dieter <rdieter@fedoraproject.org> 2.1-3
- Provides: qt(4)-webkit(-devel) = 2:%%version...

* Thu Apr 21 2011 Rex Dieter <rdieter@fedoraproject.org> 2.1-2
- -devel: Conflicts: qt-devel < 1:4.7.2-9 (qt_webkit_version.pri)
- drop old/deprecated Obsoletes/Provides: WebKit-qt
- use modified, less gigantic tarball
- patch to use phonon instead of QtMultimediaKit
- patch pluginpath for /usr/lib{,64}/mozilla/plugins-wrapped

* Tue Apr 19 2011 Rex Dieter <rdieter@fedoraproject.org> 2.1-1
- 2.1

* Mon Nov 08 2010 Than Ngo <than@redhat.com> - 2.0-2
- fix webkit to export symbol correctly

* Tue Nov 02 2010 Rex Dieter <rdieter@fedoraproject.org> 2.0-1
- 2.0 (as released with qt-4.7.0)

* Thu Sep 09 2010 Rex Dieter <rdieter@fedoraproject.org> 2.0-0.1.week32
- first try, borrowing a lot from debian/kubuntu packaging

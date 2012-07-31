
# options
#define examples 1 

Name:    qt-mobility
Version: 1.1.3
Release: 2%{?dist}
Summary: Qt Mobility Framework
Group:   System Environment/Libraries
License: LGPLv2 with exceptions
URL:     http://qt.nokia.com/products/qt-addons/mobility 
Source0: http://get.qt.nokia.com/qt/add-ons/qt-mobility-opensource-src-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: qt4-mobility = %{version}-%{release}
Provides: qt4-mobility%{?_isa} = %{version}-%{release}

## upstreamable patches
Patch50: qt-mobility-opensource-src-1.1.0-translationsdir.patch

## upstream patches
# double-check if this is still required -- Rex
Patch101: qt-mobility-opensource-src-1.1.0-pulseaudio-lib.patch

BuildRequires: alsa-lib-devel
BuildRequires: bluez-libs-devel
BuildRequires: chrpath
BuildRequires: gstreamer-plugins-bad-free-devel
BuildRequires: gstreamer-plugins-base-devel
BuildRequires: libXv-devel
BuildRequires: NetworkManager-devel
BuildRequires: pulseaudio-libs-devel
## under review, http://bugzilla.redhat.com/626122
# BuildRequires: libqmf-devel >= 1.0
BuildRequires: qt4-devel

%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}

%description
Qt Mobility Project delivers a set of new APIs to Qt with features that are well
known from the mobile device world, in particular phones. However, these APIs
allow the developer to use these features with ease from one framework and apply
them to phones, netbooks and non-mobile personal computers. The framework not
only improves many aspects of a mobile experience, because it improves the use
of these technologies, but has applicability beyond the mobile device arena.

%package devel
Summary: Qt Mobility Framework development files
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt4-devel
Provides: qt4-mobility-devel = %{version}-%{release}
Provides: qt4-mobility-devel%{?_isa} = %{version}-%{release}
Provides: %{name}-messaging-devel = %{version}-%{release}
Provides: %{name}-bearer-devel = %{version}-%{release}
Provides: %{name}-versit-devel = %{version}-%{release}
Provides: %{name}-contacts-devel = %{version}-%{release}
Provides: %{name}-location-devel = %{version}-%{release}
Provides: %{name}-multimedia-devel = %{version}-%{release}
Provides: %{name}-publishsubscribe-devel = %{version}-%{release}
Provides: %{name}-sensors-devel = %{version}-%{release}
Provides: %{name}-serviceframework-devel = %{version}-%{release}
Provides: %{name}-systeminfo-devel = %{version}-%{release}
%description devel
%{summary}.

%package doc
Summary: API documentation for %{name}
Group: Documentation
Requires: qt4
BuildArch: noarch
%description doc
%{summary}.

%package examples
Summary: Qt Mobility Framework examples
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.


%prep
%setup -q -n %{name}-opensource-src-%{version}

%patch50 -p1 -b .translationsdir
%patch101 -p1 -b .pulseaudio_lib


%build
PATH=%{_qt4_bindir}:$PATH; export PATH

./configure \
  -prefix %{_qt4_prefix} \
  -bindir %{_bindir} \
  -headerdir %{_qt4_headerdir} \
  -libdir %{_qt4_libdir} \
  -plugindir %{_qt4_plugindir} \
  -qmake-exec %{_qt4_qmake} \
  %{?examples:-examples} 

make %{?_smp_mflags} 


%install
rm -rf %{buildroot}

make install INSTALL_ROOT=%{buildroot} 

# manually install docs
install -p -m644 -D doc/qch/qtmobility.qch %{buildroot}%{_qt4_docdir}/qch/qtmobility.qch
mkdir -p %{buildroot}%{_qt4_docdir}/html/qtmobility
cp -a doc/html/* %{buildroot}%{_qt4_docdir}/html/qtmobility/

## WTF, translations went awol in 1.1.0 ?  -- Rex
#find_lang %{name} --all-name --with-qt --without-mo

# die rpath, die
chrpath --delete %{buildroot}%{_bindir}/* ||:
chrpath --delete %{buildroot}%{_qt4_libdir}/libQt*.so ||:
chrpath --delete %{buildroot}%{_qt4_plugindir}/*/*.so ||:
%if 0%{?_qt4_importdir:1}
chrpath --delete %{buildroot}%{_qt4_importdir}/*/*.so ||:
chrpath --delete %{buildroot}%{_qt4_importdir}/*/*/*.so ||:
%endif


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files 
%defattr(-,root,root,-)
%doc LICENSE.LGPL LGPL_EXCEPTION.txt
%doc changes*
%{_qt4_libdir}/libQtBearer.so.1*
%{_qt4_libdir}/libQtContacts.so.1*
%{_qt4_libdir}/libQtFeedback.so.1*
%{_qt4_libdir}/libQtGallery.so.1*
%{_qt4_libdir}/libQtLocation.so.1*
%{_qt4_libdir}/libQtMultimediaKit.so.1*
%{_qt4_libdir}/libQtOrganizer.so.1*
%{_qt4_libdir}/libQtPublishSubscribe.so.1*
%{_qt4_libdir}/libQtSensors.so.1*
%{_qt4_libdir}/libQtServiceFramework.so.1*
%{_qt4_libdir}/libQtSystemInfo.so.1*
%{_qt4_libdir}/libQtVersit.so.1*
%{_qt4_libdir}/libQtVersitOrganizer.so.1*
%if 0%{?_qt4_importdir:1}
%{_qt4_importdir}/QtMobility/
%{_qt4_importdir}/QtMultimediaKit/
%endif
%{_qt4_plugindir}/*

%files devel
%defattr(-,root,root,-)
%{_bindir}/icheck
%{_bindir}/qcrmlgen
%{_bindir}/servicedbgen
%{_bindir}/servicefw
%{_bindir}/servicexmlgen
%{_bindir}/vsexplorer
%{_qt4_prefix}/mkspecs/features/mobility.prf
%{_qt4_prefix}/mkspecs/features/mobilityconfig.prf 
%{_qt4_headerdir}/Qt*/
%{_qt4_libdir}/libQt*.prl
%{_qt4_libdir}/libQt*.so

%files doc
%defattr(-,root,root,-)
%{_qt4_docdir}/qch/qtmobility.qch
%{_qt4_docdir}/html/qtmobility/

%if 0%{?examples}
%files examples
%defattr(-,root,root,-)
%{_qt4_bindir}/arrowkeys
%{_qt4_bindir}/audiodevices
%{_qt4_bindir}/audioinput
%{_qt4_bindir}/audiooutput
%{_qt4_bindir}/audiorecorder
%{_qt4_bindir}/battery-publisher
%{_qt4_bindir}/battery-subscriber
%{_qt4_bindir}/bearercloud
%{_qt4_bindir}/bearermonitor
%{_qt4_bindir}/cubehouse
%{_qt4_bindir}/flickrdemo
%{_qt4_bindir}/grueapp
%{_qt4_bindir}/logfilepositionsource
%{_qt4_bindir}/metadata
%{_qt4_bindir}/nmealog.txt
%{_qt4_bindir}/orientation
%{_qt4_bindir}/publish-subscribe
%{_qt4_bindir}/radio
%{_qt4_bindir}/samplephonebook
%{_qt4_bindir}/satellitedialog
%{_qt4_bindir}/sensor_explorer
%{_qt4_bindir}/servicebrowser
%{_qt4_bindir}/sfw-notes
%{_qt4_bindir}/show_acceleration
%{_qt4_bindir}/show_als
%{_qt4_bindir}/show_compass
%{_qt4_bindir}/show_magneticflux
%{_qt4_bindir}/show_orientation
%{_qt4_bindir}/show_proximity
%{_qt4_bindir}/show_rotation
%{_qt4_bindir}/show_tap
%{_qt4_bindir}/simplelog.txt
%{_qt4_bindir}/slideshow
%{_qt4_bindir}/videographicsitem
%{_qt4_bindir}/videowidget
%{_qt4_bindir}/xmldata
%{_qt4_plugindir}/serviceframework/libserviceframework_voipdialerservice.so
%{_qt4_plugindir}/serviceframework/libserviceframework_landlinedialerservice.so
%{_qt4_plugindir}/serviceframework/libserviceframework_filemanagerplugin.so
%{_qt4_plugindir}/serviceframework/libserviceframework_bluetoothtransferplugin.so
%{_qt4_plugindir}/serviceframework/libserviceframework_notesmanagerplugin.so
%{_qt4_plugindir}/sensors/libqtsensors_grueplugin.so
%endif


%changelog
* Mon May 23 2011 Rex Dieter <rdieter@fedoraproject.org> 1.1.3-2
- drop BR: qt4-webkit-devel
- BR: gstreamer-plugins-bad-free-devel gstreamer-plugins-base-devel libXv-devel
- tweaks for qt-4.6 (el6)

* Mon May 09 2011 Jaroslav Reznik <jreznik@redhat.com> 1.1.3-1
- 1.1.3

* Tue Apr 19 2011 Rex Dieter <rdieter@fedoraproject.org> 1.1.1-1
- 1.1.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 09 2010 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-1
- 1.1.0

* Wed Jul 14 2010 Rex Dieter <rdieter@fedoraproject.org> 1.0.1-3
- License: LGPLv2 ...
- -doc subpkg

* Wed Jul 14 2010 Rex Dieter <rdieter@fedoraproject.org> 1.0.1-2
- 1.0.1 (first try, based on work by heliocastro)


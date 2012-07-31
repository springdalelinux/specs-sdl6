%define real_version v19_20071207

Summary: Free, cross platform, open-source, audio I/O library
Name: portaudio
Version: 19
Release: 9%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.portaudio.com/
Source: http://www.portaudio.com/archives/pa_stable_%{real_version}.tar.gz
Patch0: portaudio-non-mmap-alsa.patch
Patch1: portaudio-doxynodate.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: doxygen
BuildRequires: alsa-lib-devel
BuildRequires: jack-audio-connection-kit-devel

%description
PortAudio is a portable audio I/O library designed for cross-platform
support of audio. It uses a callback mechanism to request audio processing.
Audio can be generated in various formats, including 32 bit floating point,
and will be converted to the native format internally.


%package devel
Summary: Development files for the portaudio audio I/O library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}, pkgconfig

%description devel
PortAudio is a portable audio I/O library designed for cross-platform
support of audio. It uses a callback mechanism to request audio processing.
Audio can be generated in various formats, including 32 bit floating point,
and will be converted to the native format internally.

This package contains files required to build applications that will use the
portaudio library.


%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1


%build
%configure --disable-static --enable-cxx
%{__make} %{?_smp_mflags}
# Build html devel documentation
doxygen


%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}


%clean
%{__rm} -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc LICENSE.txt README.txt
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/html/*
%{_includedir}/portaudiocpp/
%{_includedir}/portaudio.h
%exclude %{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 19-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 19-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 22 2008 Matthias Saou <http://freshrpms.net/> 19-7
- Add Doxyfile patch to remove date in footer and fix multilib (#342931).

* Sun Dec  7 2008 Hans de Goede <hdegoede@redhat.com> 19-6
- Add a patch by Kevin Kofler to make non mmap alsa (and thus pulseaudio) work
  (bz 445644)

* Sun Feb  3 2008 Matthias Saou <http://freshrpms.net/> 19-5
- Update to "stable" v19_20071207.
- Rebuild against latest jack in rawhide (#430672).
- Backport update to F8 too (#431266).

* Mon Dec 10 2007 Matthias Saou <http://freshrpms.net/> 19-4
- Include portaudiocpp library and headers (#413681).

* Wed Aug 22 2007 Matthias Saou <http://freshrpms.net/> 19-3
- Rebuild for new BuildID feature.

* Sun Aug  5 2007 Matthias Saou <http://freshrpms.net/> 19-2
- Update License field.

* Tue Jun 19 2007 Matthias Saou <http://freshrpms.net/> 19-1
- Update to "stable" v19_061121.
- Switch virtual devel provide to a real sub-package.
- Update spec to match build changes from custom Makefile to autotools.
- Include new pkgconfig file and require pkgconfig from the devel package.
- Add ldconfig calls now that we have a versionned shared library.
- Rebuild against alsa-lib and jack-audio-connection-kit.
- Build doxygen documentation and include it in the devel package.

* Mon Aug 28 2006 Matthias Saou <http://freshrpms.net/> 18.1-8
- FC6 rebuild.

* Mon Mar  6 2006 Matthias Saou <http://freshrpms.net/> 18.1-7
- FC5 rebuild.

* Thu Feb  9 2006 Matthias Saou <http://freshrpms.net/> 18.1-6
- Rebuild for new gcc/glibc.

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 18.1-5
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 18.1-4
- rebuilt

* Tue Nov 16 2004 Matthias Saou <http://freshrpms.net/> 18.1-3
- Bump release to provide Extras upgrade path.

* Fri Nov  5 2004 Matthias Saou <http://freshrpms.net/> 18.1-2
- Add -devel provides.
- Fix .so 644 mode (overidden in defattr).

* Thu Jun 10 2004 Dag Wieers <dag@wieers.com> - 18.1-1
- Added -fPIC for x86_64.

* Sat Sep 13 2003 Dag Wieers <dag@wieers.com> - 18.1-0
- Initial package. (using DAR)


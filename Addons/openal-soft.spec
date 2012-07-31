Name:		openal-soft
Version:	1.12.854
Release:	1%{?dist}
Summary:	Open Audio Library

Group:		System Environment/Libraries
License:	LGPLv2+
URL:		http://kcat.strangesoft.net/openal.html
Source0:	http://kcat.strangesoft.net/openal-releases/openal-soft-%{version}.tar.bz2
#http://repo.or.cz/w/openal-soft.git?a=snapshot;h=%{revision};sf=tgz
#Source0:	openal-soft-%{version}.tar.gz 
Patch1:		openal-soft.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	alsa-lib-devel
BuildRequires:	pulseaudio-libs-devel
BuildRequires:	portaudio-devel
BuildRequires:	cmake
Obsoletes:	openal <= 0.0.10
Provides:	openal = %{version}

%description
OpenAL Soft is a cross-platform software implementation of the OpenAL 3D
audio API. It's built off of the open-sourced Windows version available
originally from the SVN repository at openal.org. OpenAL provides
capabilities for playing audio in a virtual 3d environment. Distance
attenuation, doppler shift, and directional sound emitters are among
the features handled by the API. More advanced effects, including air
absorption, low-pass filters, and reverb, are available through the
EFX extension. It also facilitates streaming audio, multi-channel buffers,
and audio capture.

%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	openal-devel <= 0.0.10
Provides:	openal-devel = %{version}

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch1 -p0 -b .orig

%build
%cmake .
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

install -Dpm644 alsoftrc.sample %{buildroot}%{_sysconfdir}/openal/alsoft.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/openal-info
%{_libdir}/libopenal.so.*
%dir %{_sysconfdir}/openal
%config(noreplace) %{_sysconfdir}/openal/alsoft.conf

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/libopenal.so
%{_libdir}/pkgconfig/openal.pc

%changelog
* Thu Apr 01 2010 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.12.854-1
- New upstream release

* Mon Mar 01 2010 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.11.753-3.20100225
- Fixed Version Number

* Sun Feb 28 2010 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.11.753-2.a9e0e57797c6f4321d5776e1f29bf1e75b11e6a1
- Fixed Bug 567870

* Mon Jan 18 2010 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.11.753-1
- New Upstream Release

* Wed Jan 13 2010 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.10.622-7.931f5875cdc4ce0ac61a5110f11e962426e53d99
- Newer git version that fix more problems with pulseaudio.

* Mon Jan 04 2010 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.10.622-6.0ceaa01c3de75c946ff2e7591e7f69b28ec00409
- Newer git version with more Pulseaudio fixes. Have fun.

* Mon Dec 28 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.10.622-5.3793919892e6d61e5fec3abeaaeebc3f2332be13
- Fixed small spec verion info.

* Mon Dec 28 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.10.622-4.3793919892e6d61e5fec3abeaaeebc3f2332be13
- Fixed broken upgrade paths.

* Sat Dec 26 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.10.622-3.3793919892e6d61e5fec3abeaaeebc3f2332be13
- Updatet to an newer git version because of some pulseaudio fixes.

* Tue Nov 10 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> - 1.10.622-2
- add default config

* Mon Nov 09 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.10.622-1
- New upstream release

* Sat Nov 07 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.9.563-2.c1b161b44bbf60420de2e1ba886e957d9fcd495e
- Updatet to an newer git version because of some pulseaudio fixes.
- I hope it fix bug 533501

* Fri Oct  09 2009 Hans de Goede <hdegoede@redhat.com> - 1.9.563-1.d6e439244ae00a1750f0dc8b249f47efb4967a23git
- Update to 1.9.563 + some fixes from git
- This fixes:
  - Not having any sound in chromium-bsu 
  - Various openal using programs hanging on exit

* Fri Aug 21 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.8.466-9.487f0dde7593144ceabd817306500465caf7602agit
- Fixed version info

* Fri Aug 21 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.8.466-8.487f0dde7593144ceabd817306500465caf7602agit
- Fixed bug 517973

* Sun Aug 16 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.8.466-7
- Fixed bug 517721. Added upstream.patch

* Sat Aug 08 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.8.466-6
- Fixed license and pkgconfig problem thx goes to Christoph Wickert

* Wed Aug 05 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.8.466-5
- Fixed Obsoletes: and Provides: sections

* Tue Aug 04 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.8.466-4
- Added Obsoletes: openal <= 0.0.9 and remove Conflicts: openal-devel

* Fri Jun 26 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.8.466-3
- Fixed all warnings of rpmlint

* Fri Jun 20 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.8.466-2
- Updatet the SPEC and SRPM file because openal-soft-devel conflicts with
openal-devel

* Fri Jun 20 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.8.466-1
- Initial release for Fedora

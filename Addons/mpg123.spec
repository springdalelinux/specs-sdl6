%global man_ext .gz
# alternatives priority (we are the real thing)
%global apriority 99

Name:           mpg123
Version:        1.12.3
Release:        1%{?dist}
Summary:        MPEG audio player
Group:          Applications/Multimedia
License:        GPLv2+ and LGPLv2
URL:            http://mpg123.org/
Source:         http://downloads.sourceforge.net/mpg123/mpg123-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libtool-ltdl-devel SDL-devel portaudio-devel esound-devel
BuildRequires:  jack-audio-connection-kit-devel nas-devel arts-devel
BuildRequires:  alsa-lib-devel pulseaudio-libs-devel openal-soft-devel
Requires(post): %{_sbindir}/alternatives
Requires(postun): %{_sbindir}/alternatives
Provides:       mp3-cmdline = %{version}-%{release}

%description
Real time command line MPEG audio player for Layer 1, 2 and Layer3.


%package plugins-pulseaudio
Summary:        Pulseaudio output plug-in for mpg123
Group:          Applications/Multimedia
Requires:       %{name} = %{version}-%{release}

%description plugins-pulseaudio
Pulseaudio output plug-in for mpg123.


%package plugins-jack
Summary:        JACK output plug-in for mpg123
Group:          Applications/Multimedia
Requires:       %{name} = %{version}-%{release}

%description plugins-jack
JACK output plug-in for mpg123.


%package plugins-extras
Summary:        Extra output plugins for mpg123
Group:          Applications/Multimedia
Requires:       %{name} = %{version}-%{release}

%description plugins-extras
Extra (non often used) output plugins for mpg123 which require additional
dependencies to be installed.


%package -n libmpg123
Summary:        MPEG audio Layer 1, 2 and Layer3 library
Group:          System Environment/Libraries

%description -n libmpg123
MPEG audio Layer 1, 2 and Layer3 library.


%package -n libmpg123-devel
Summary:        Development files for mpg123
Group:          Development/Libraries
Requires:       libmpg123 = %{version}-%{release}, pkgconfig

%description -n libmpg123-devel
The libmpg123-devel package contains libraries and header files for
developing applications that use libmpg123.


%prep
%setup -q
iconv -f iso8859-1 -t utf8 AUTHORS -o AUTHORS.utf8
touch -r AUTHORS AUTHORS.utf8
mv AUTHORS.utf8 AUTHORS


%build
%configure
# Get rid of /usr/lib64 rpath on 64bit
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la
# mpg321 also "provides" a mpg123 manpage an binary so mv ours to mpg123.bin
# and use alternatives
mv $RPM_BUILD_ROOT%{_bindir}/mpg123 $RPM_BUILD_ROOT%{_bindir}/mpg123.bin
mv $RPM_BUILD_ROOT%{_mandir}/man1/mpg123.1 \
   $RPM_BUILD_ROOT%{_mandir}/man1/mpg123.bin.1
# prepare ghost alternatives
# touch does not set the correct file mode bits 
ln -s mpg123.bin $RPM_BUILD_ROOT%{_bindir}/mpg123
ln -s mpg123.bin $RPM_BUILD_ROOT%{_bindir}/mp3-cmdline
ln -s mpg123.bin.1 $RPM_BUILD_ROOT%{_mandir}/man1/mpg123.1


%clean
rm -rf $RPM_BUILD_ROOT


%post
%{_sbindir}/alternatives \
  --install %{_bindir}/mpg123 mpg321_binlink %{_bindir}/mpg123.bin %{apriority} \
  --slave %{_mandir}/man1/mpg123.1%{man_ext} mpg321_manlink %{_mandir}/man1/mpg123.bin.1%{man_ext} \
  --slave %{_bindir}/mp3-cmdline mpg321_mp3cmdline %{_bindir}/mpg123.bin \
  >/dev/null 2>&1 || :

%postun
if [ "$1" -eq 0 ]; then
  %{_sbindir}/alternatives \
    --remove mpg321_binlink %{_bindir}/mpg123.bin \
    >/dev/null 2>&1 || :
fi

%post -n libmpg123 -p /sbin/ldconfig

%postun -n libmpg123 -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_bindir}/mpg123.bin
%ghost %{_bindir}/mpg123
%ghost %{_bindir}/mp3-cmdline
%dir %{_libdir}/mpg123
%{_libdir}/mpg123/output_alsa.*
%{_libdir}/mpg123/output_dummy.*
%{_libdir}/mpg123/output_oss.*
%{_mandir}/man1/mpg123.bin.1%{man_ext}
%ghost %{_mandir}/man1/mpg123.1%{man_ext}

%files plugins-pulseaudio
%defattr(-,root,root,-)
%{_libdir}/mpg123/output_pulse.*

%files plugins-jack
%defattr(-,root,root,-)
%{_libdir}/mpg123/output_jack.*

%files plugins-extras
%defattr(-,root,root,-)
%{_libdir}/mpg123/output_arts.*
%{_libdir}/mpg123/output_esd.*
%{_libdir}/mpg123/output_nas.*
%{_libdir}/mpg123/output_openal.*
%{_libdir}/mpg123/output_portaudio.*
%{_libdir}/mpg123/output_sdl.*

%files -n libmpg123
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/libmpg123.so.*

%files -n libmpg123-devel
%defattr(-,root,root,-)
%doc doc/*
%{_includedir}/mpg123.h
%{_libdir}/libmpg123.so
%{_libdir}/pkgconfig/libmpg123.pc


%changelog
* Tue Aug 24 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 1.12.3-1
- New upstream release 1.12.3

* Fri Jul 16 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 1.12.1-4
- Put the pulseaudio and jack output plugins in their own subpackages (rf#1278)

* Mon Jun 21 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 1.12.1-3
- Move mpg123 (and its manpage) to mpg123.bin and use alternatives, so as to
  peacefully co-exist with mpg321 (rf#1278)

* Fri Jun 18 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 1.12.1-2
- Add arts-devel BuildRequire and add the arts output plug-in to the
  mpg123-plugins-extras package

* Mon Jun 14 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 1.12.1-1
- Update to 1.12.1
- Put libmpg123 into its own package
- Put some less often used output plugins into their own mpg123-plugins-extras
  package

* Thu May 29 2008 Matthias Saou <http://freshrpms.net/> 1.4.2-2
- Don't remove plugins *.la files, as they're required to run.

* Mon May 12 2008 Matthias Saou <http://freshrpms.net/> 1.4.2-1
- Update to 1.4.2.
- Obolete mpg321 up to last known version, as it's pretty much dead.
- Add libtool-ltdl-devel build req, without a copy is installed.
- Add scriplets for new library.

* Mon Jun 04 2007 Dag Wieers <dag@wieers.com> - 0.66-1
- Updated to release 0.66.

* Wed Feb 07 2007 Dag Wieers <dag@wieers.com> - 0.65-1
- Updated to release 0.65.

* Tue Jan 16 2007 Dag Wieers <dag@wieers.com> - 0.64-1
- Updated to release 0.64.

* Mon Jan 15 2007 Dag Wieers <dag@wieers.com> - 0.63-1
- Updated to release 0.63.

* Sun Oct 22 2006 Dag Wieers <dag@wieers.com> - 0.61-1
- Updated to release 0.61.

* Mon Sep  4 2006 Matthias Saou <http://freshrpms.net/> 0.60-1
- Update to 0.60 final.
- Add support for all available compatible outputs, unfortunately it's a build
  time choice, so default to alsa.
- Obsolete mpg321 up to the last know package version.

* Tue Jul 25 2006 Matthias Saou <http://freshrpms.net/> 0.60-0.1.beta2
- Initial RPM release, now that mpg123 is maintained again and went GPL/LGPL.
- Audio output type is not (yet?) plugin-based, so use libao (for ALSA).

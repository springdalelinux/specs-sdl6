
%define kdelibs3 kdelibs3
#define ffmpeg ffmpeg
#define _with_ffmpeg --with-ffmpeg

Name:           k3b-extras-freeworld
Epoch:          1
Version:        1.0.5
Release:        7.1%{?dist}
Summary:        Additional codec plugins for the k3b CD/DVD burning application

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://www.k3b.org
Source0:        http://downloads.sourceforge.net/sourceforge/k3b/k3b-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)

## upstreamable
Patch50: k3b-1.0.5-ffmpeg.patch

## upstream
Patch100: k3b-lavc52.patch

ExcludeArch:    s390 s390x

BuildRequires:  %{kdelibs3}-devel
BuildRequires:  lame-devel
BuildRequires:  libdvdread-devel
BuildRequires:  libmad-devel
%{?ffmpeg:BuildRequires:  %{ffmpeg}-devel automake libtool}
BuildRequires:  libmusicbrainz-devel
BuildRequires:  gettext
BuildRequires:  taglib-devel

Obsoletes:      k3b-mp3 < 0.12.10 
Provides:       k3b-mp3 = %{version}-%{release}

# livna upgrade
Obsoletes: k3b-extras-nonfree < 1.0.4-3
Provides:  k3b-extras-nonfree = %{version}-%{release}

Requires:       k3b >= %{version}


%description
Additional decoder/encoder plugins for k3b, a feature-rich and easy to
handle CD/DVD burning application.


%prep
%setup -q -n k3b-%{version}

%if 0%{?ffmpeg:1}
%patch50 -p1 -b .ffmpeg
%patch100 -p1 -b .lavc52

# hack/fix for newer automake
sed -iautomake -e 's|automake\*1.10\*|automake\*1.1[0-5]\*|' admin/cvs.sh

make -f admin/Makefile.common
%endif


%build
unset QTDIR
[ -z "$QTDIR" ] && . /etc/profile.d/qt.sh

%configure \
  --disable-rpath \
  --enable-new-ldflags \
  --disable-debug --disable-warnings \
  --disable-dependency-tracking --enable-final \
  --with-libdvdread \
  --with-external-libsamplerate=no \
  --without-oggvorbis \
  --without-flac \
  --without-sndfile \
  --without-hal \
  --without-musepack \
  --with-k3bsetup=no \
  %{?_with_ffmpeg} %{!?_with_ffmpeg:--without-ffmpeg} \
  --with-lame \
  --with-libmad

%global makeflags %{?_smp_mflags}%{nil}

# We need just a few k3b core libs.
# As FC k3b package no longer includes the libtool archives,
# we cannot simply link them anymore.
pushd libk3bdevice
#ln -s %{_libdir}/libk3bdevice.la libk3bdevice.la
make %makeflags
popd

pushd libk3b
#ln -s %{_libdir}/libk3b.la libk3b.la
make %makeflags
popd

# Now build individual plugins.
make %makeflags -C plugins/decoder/mp3
%{?ffmpeg:make %makeflags -C plugins/decoder/ffmpeg}
make %makeflags -C plugins/encoder/lame


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT -C plugins/decoder/mp3
%{?ffmpeg:make install DESTDIR=$RPM_BUILD_ROOT -C plugins/decoder/ffmpeg}
make install DESTDIR=$RPM_BUILD_ROOT -C plugins/encoder/lame


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{?ffmpeg:%{_libdir}/kde3/libk3bffmpegdecoder.*}
%{?ffmpeg:%{_datadir}/apps/k3b/plugins/k3bffmpegdecoder.plugin}
%{_libdir}/kde3/libk3blameencoder.*
%{_datadir}/apps/k3b/plugins/k3blameencoder.plugin
%{_libdir}/kde3/libk3bmaddecoder.*
%{_datadir}/apps/k3b/plugins/k3bmaddecoder.plugin


%changelog
* Thu Oct 01 2009 Rex Dieter <rdieter@fedoraproject.org> - 1:1.0.5-7
- Epoch: 1 (F-12 revert to k3b-1.0.5)

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.0.5-6
- rebuild for new F11 features

* Mon Dec 15 2008 Dominik Mierzejewski <rpm@greysector.net> - 1.0.5-5
- fix build with current ffmpeg

* Wed Sep 17 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.0.5-4
- better pkgconfig-based ffmpeg patch
- optimize configure
- License: GPLv2+

* Tue Sep 16 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.0.5-3
- re-enable ffmpeg support

* Mon Sep 15 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.0.5-2
- omit ffmpeg support (for now)

* Mon Sep 15 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.0.5-1
- k3b-extras-freeworld for rpmfusion

* Thu Jan 31 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.0.4-2
- BR: kdelibs3-devel

* Mon Nov 26 2007 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.0.4-1
- Update to 1.0.4 (no relevant changes, however).

* Sat Nov 24 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.0.3-2
- rebuilt

* Tue Jul 24 2007 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.0.3-1
- Update to 1.0.3 (fix for mp3 without tags).

* Mon Jun 25 2007 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.0.2-1
- Update to 1.0.2.

* Wed May 30 2007 Rex Dieter <rexdieter[AT]users.sf.net>
- drop extraneous BR's

* Fri Apr 27 2007 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.0.1-1
- Update to 1.0.1 (LAME encoder plugin fix).

* Sat Mar 17 2007 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.0-1
- Upgrade to 1.0 final.

* Sun Feb 18 2007 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.0-0.2.rc6
- Upgrade to 1.0rc6 (which has appeared in Rawhide).

* Tue Feb  6 2007 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.12.17-3
- Rebuild for new ffmpeg.

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.12.17-2
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Sun Sep 24 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.12.17-1
- Update to 0.12.17.

* Fri Mar 31 2006 Michael Schwendt <mschwendt[AT]users.sf.net> 0.12.14-2
- Don't build libsndfile plugin anymore, since it moves to k3b-extras.

* Wed Mar 15 2006 Michael Schwendt <mschwendt[AT]users.sf.net> 0.12.14-1
- Update to 0.12.14.
- The oh-so-clever build speed-up trick cannot be used anymore,
  since libtool archives have been dropped from FC k3b package.

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Sat Dec 31 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 0.12.10-0.lvn.1
- Update to 0.12.10.
- Rename package to k3b-extras-nonfree.

* Sun Jul 17 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 0.12.2-0.lvn.1
- Update to 0.12.2 (for FC Development).
- Rename package to k3b-extras.
- Add plugins: ffmpeg decoder, libsndfile decoder, lame encoder.
- Use BR k3b to speed up build.
- Drop explicit Epoch 0.

* Fri May 20 2005 Thorsten Leemhuis <fedora[AT]leemhuis.info> 0:0.11.24-0.lvn.2
- Use configure-parm "--with-qt-libraries=$QTDIR/lib" to fix FC4-x86_64 build

* Wed May 11 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 0:0.11.24-0.lvn.1
- Update to 0.11.24 (advertised as handling mp3 errors better).
- Remove GCC version check which blacklists FC4's GCC (d'oh!).
- Explicity disable external libsamplerate, which is in FE and
  hence FC's k3b doesn't use it either.
- Merge statfs patch from FC's k3b package.

* Thu Mar 24 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 0:0.11.22-0.lvn.1
- Update to 0.11.22 (MAD decoder update).
- Use new switches to disable OggVorbis and FLAC explicitly.

* Wed Jan 26 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 0:0.11.19-0.lvn.1
- Update to 0.11.19 (for another mp3 detection fix).

* Tue Aug 10 2004 Michael Schwendt <mschwendt[AT]users.sf.net> 0:0.11.14-0.lvn.1
- Update to 0.11.14 (which obsoletes patches again).

* Tue Aug 10 2004 Michael Schwendt <mschwendt[AT]users.sf.net> 0:0.11.13-0.lvn.1
- Add patch from CVS to fix mp3 decoder.

* Sat Aug  7 2004 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.11.13-0.lvn.1
- Updated to 0.11.13 (includes new mp3 backport).
- Patch for k3bdiskinfo.cpp is obsolete.
- Now k3bdevice.cpp needs patch for Qt 3.1.
- Remove a few more unneeded BR.

* Thu May 27 2004 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.11.10-0.lvn.1
- Update to 0.11.10 (includes mp3 fixes).
- Fix k3bdiskinfo.cpp for Qt 3.1.
- Remove redundant BR qt-devel.
- Disable RPATH (seems to work now).
- Rename package to k3b-mp3, build just the plugin and all depending targets.
- Delete old changelog entries which are no longer relevant to this package.

* Mon Mar 29 2004 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.11.9-0.fdr.1
- Update to 0.11.9.

* Mon Mar 29 2004 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.11.8-0.fdr.1
- Update to 0.11.8.

* Sun Mar 28 2004 Michael Schwendt <mschwendt[AT]users.sf.net>
- Rewrite the conditional code sections, although they work fine in
  normal build environments and the fedora.us build system. But 'mach'
  makes some weird assumptions about build requirements in spec files
  and causes unexpected results.


%define _pkglibdir %{_libdir}/nx
%define _pkgdatadir %{_datadir}/nx
%define _pkglibexecdir %{_libexecdir}/nx

Summary: Proxy system for X11
Name: nx
Version: 3.5.0
Release: 3%{?dist}
# MIT on the X11 bits
License: GPLv2 and MIT
Group: Applications/Internet
URL: http://www.nomachine.com
# Compression Libraries and Proxy Sources
Source0: http://64.34.161.181/download/%{version}/sources/nxproxy-%{version}-1.tar.gz
Source1: http://64.34.161.181/download/%{version}/sources/nxcomp-%{version}-2.tar.gz
Source2: http://64.34.161.181/download/%{version}/sources/nxcompext-%{version}-1.tar.gz
Source3: http://64.34.161.181/download/%{version}/sources/nxssh-%{version}-2.tar.gz
# Shadowing Libraries
Source4: http://64.34.161.181/download/%{version}/sources/nxcompshad-%{version}-2.tar.gz
# X11 Support Programs and Libraries
Source5: http://64.34.161.181/download/%{version}/sources/nx-X11-%{version}-1.tar.gz
Source6: http://64.34.161.181/download/%{version}/sources/nxauth-%{version}-1.tar.gz
# X11 Agent Sources
Source7: http://64.34.161.181/download/%{version}/sources/nxagent-%{version}-2.tar.gz
# NX Example Scripts
Source8: http://64.34.161.181/download/%{version}/sources/nxscripts-%{version}-1.tar.gz

Source9: nxwrapper.in
Source10: docs.tar.bz2
Patch0: nx-3.5.0-optflags.patch
Patch1: nx-3.5.0-syslibs.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gcc-c++, libstdc++-devel, redhat-release, hardlink
BuildRequires: expat-devel, audiofile-devel, openssl-devel, libjpeg-devel, libpng-devel
BuildRequires: libXt-devel, xorg-x11-proto-devel, libXp-devel, imake
BuildRequires: libXdamage-devel, libXrandr-devel, libXtst-devel
BuildRequires: fontconfig-devel
# Better mention what we really require on a file basis.
# Requires: xorg-x11-utils

%filter_from_provides /libX\(11\|ext\|render\)\.so/d
%filter_setup

%description
NX provides a proxy system for the X Window System.

%prep
%setup -q -c %{name}-%{version} -T -a0 -a1 -a2 -a3 -a4 -a5 -a6 -a7 -a8
%patch0 -p1
%patch1 -p1
find nx-X11 -name "*.[ch]" -print0 | xargs -0 chmod -c -x

%build
export CFLAGS="%{optflags} -Wl,-rpath,%{_pkglibdir}"
%ifarch x86_64 ppc64
export CFLAGS="$CFLAGS -fPIC -DPIC"
%endif
export CXXFLAGS="$CFLAGS"
export RPM_OPT_FLAGS="$CFLAGS"

# The commented parts show how the build would proceed step by step.
# This information is important in case someone wants to split this package
# (which would be the proper thing to do).
# Within the commented area the make World invocation does all for
# you. It isn't placed by accident in the middle of the commented
# build instructions, as this is where the X11 libs would be built

# build Compression Library and Proxy
for i in nxcomp nxcompshad nxproxy; do
  pushd $i; ./configure; make %{?_smp_mflags} CCFLAGS="$CFLAGS"; popd
done
# build X11 Support Libraries and Agents
make %{?_smp_mflags} -C nx-X11 World
%if 0
# build Extended Compression Library
pushd nxcompext
  ./configure; make %{?_smp_mflags}
popd
%endif
pushd nxssh
LDFLAGS="-Wl,-rpath,%{_pkglibdir}" ./configure --without-zlib-version-check
make %{?_smp_mflags} nxssh
popd

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_pkglibdir}
mkdir -p %{buildroot}%{_pkglibexecdir}
mkdir -p %{buildroot}%{_mandir}/man1

# install X11 Support Libraries and Agents
install -p -m 0755 nx-X11/lib/X11/libX11.so.*.* \
   nx-X11/lib/Xext/libXext.so.*.* \
   nx-X11/lib/Xrender/libXrender.so.*.* \
   %{buildroot}%{_pkglibdir}
install -p -m 0755 nx-X11/programs/Xserver/nxagent \
  %{buildroot}%{_pkglibexecdir}
# nxwrapper
sed -e's,@PKGLIBDIR@,%{_pkglibdir},g' \
    -e's,@PKGLIBEXECDIR@,%{_pkglibexecdir},g' \
  < %{SOURCE9} > %{buildroot}%{_pkglibexecdir}/nxwrapper
chmod 0755 %{buildroot}%{_pkglibexecdir}/nxwrapper
ln -s %{_pkglibexecdir}/nxwrapper %{buildroot}%{_bindir}/nxagent
# install Compression Libraries and Proxy
install -p -m 0755 nxcomp/libXcomp.so.*.* \
  nxcompext/libXcompext.so.*.* \
  nxcompshad/libXcompshad.so.*.* \
  %{buildroot}%{_pkglibdir}
install -p -m 0755 nxssh/nxssh %{buildroot}%{_pkglibexecdir}
ln -s %{_pkglibexecdir}/nxssh %{buildroot}%{_bindir}/nxssh
install -p -m 0755 nxproxy/nxproxy %{buildroot}%{_pkglibexecdir}
ln -s %{_pkglibexecdir}/nxproxy %{buildroot}%{_bindir}/nxproxy
# set up shared lib symlinks
/sbin/ldconfig -n %{buildroot}%{_pkglibdir}
# prelink blacklisting, to be removed once lib rpaths are worked out (#689508)
mkdir -p %{buildroot}%{_sysconfdir}/prelink.conf.d
cat <<EOF > %{buildroot}%{_sysconfdir}/prelink.conf.d/nx.conf
-b %{_pkglibexecdir}/nxagent
EOF
# install scripts
mkdir -p %{buildroot}%{_defaultdocdir}/%{name}-%{version}
cp -a nxscripts %{buildroot}%{_defaultdocdir}/%{name}-%{version}
# documentation and license
# TODO: docs tarball contains dupes wrt nxscripts
tar xjf %{SOURCE10} -C %{buildroot}%{_defaultdocdir}/%{name}-%{version}
for i in nxcomp nxcompext nxcompshad nxproxy nxssh nx-X11 \
  nx-X11/programs/nxauth nx-X11/programs/Xserver/hw/nxagent; do
  for j in CHANGELOG COPYING LICENSE; do
    [ -f $i/$j ] && install -Dpm 0644 $i/$j \
      %{buildroot}%{_defaultdocdir}/%{name}-%{version}/${i##*/}/$j
  done
done
# save a bit of space
%{_sbindir}/hardlink -cv %{buildroot}%{_defaultdocdir}/%{name}-%{version}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{_defaultdocdir}/%{name}-%{version}
%config(noreplace) %{_sysconfdir}/prelink.conf.d
%{_bindir}/*
%{_pkglibdir}
%{_pkglibexecdir}

%changelog
* Sun Jul  3 2011 Ville Skyttä <ville.skytta@iki.fi> - 3.5.0-3
- Use system fontconfig and expat during build.
- Build executables with rpath to fix prelinking, libs and nxagent still to do.
- Fix optflags by patching instead of embedding options in specfile.

* Sat Jun 25 2011 Ville Skyttä <ville.skytta@iki.fi> - 3.5.0-2
- Update nxcomp and nxssh to 3.5.0-2.
- Install symlinks instead of duplicate copies of shared libs (#689508).
- Blacklist executables from prelinking for now (#689508).
- Build nxssh with %%{optflags}, and everything with %%{_smp_mflags}.
- Don't try to build nxproxy more than once.
- Don't compile throwaway nxssh parts.

* Wed Jun  8 2011 Ville Skyttä <ville.skytta@iki.fi> - 3.5.0-1
- Update to 3.5.0.

* Sat Feb 19 2011 Ville Skyttä <ville.skytta@iki.fi> - 3.4.0-41
- Update nxagent to 3.4.0-16.
- Package more docs.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 10 2010 Ville Skyttä <ville.skytta@iki.fi> - 3.4.0-39
- Update to 3.4.0.
- Use Fedora %%filter* macros for Provides filtering.
- Build with %%{optflags} on x86_64.
- Fix debuginfo and source file permissions.

* Wed Sep  2 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 3.3.0-38
- Update to latest (third) maintenance release.

* Sat Jun  6 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 3.3.0-35
- Update to latest maintenance sources.

* Sun May 17 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 3.3.0-34
- Fix FTBFS: added nx-gcc44.patch.

* Sat Feb 14 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 3.3.0-33
- Update to 3.3.0.

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 3.2.0-32
- rebuild with new openssl

* Tue Aug 26 2008 TOm "spot" Callaway <tcallawa@redhat.com> - 3.2.0-31
- fix license tag

* Mon Aug 25 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 3.2.0-30
- Update nxagent to fix some keyboard mapping on 64 bits and broken
  repaint on ADSL type lines.

* Tue Aug 12 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 3.2.0-29
- Remove old patches.

* Sun Aug 10 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 3.2.0-28
- Upstream updates to nxcomp, nxcompshad, nx-X11, nxagent.

* Sat Apr 12 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 3.2.0-27
- Update to 3.2.0.

* Sat Apr  5 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 3.1.0-26
- Update to maintenance release #2.
- Add nxssh.
- mv nxwrapper to the libexec dir.

* Wed Jan  2 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 3.1.0-25
- Update to 3.1.0.
- add nxcompshad, nxauth; remove nxviewer, nxdesktop.
- add -fPIC for ppc64.
- Propagate %%{optflags} for x86_64, too.

* Fri Jun  1 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.1.0-22
- Sync with ATrpms' nxfindprovides helper.

* Wed May 23 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.1.0-21.1
- Fix typo in nxwrapper.in (PKGEXECDIR -> PKGLIBEXECDIR).

* Tue May 22 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.1.0-20
- readded Source11 to filter find-provides from showing libraries that
  should not be provided to the system. BZ#194652 & 240835.

* Mon Feb 19 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.1.0-18
- Update to 2.1.0 (4th? maintenance release).

* Tue Jan 17 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to maintenance release.

* Sat Jul 30 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to nx 1.5.0. final.

* Mon Feb 14 2005 Rick Stout <zipsonic[AT]gmail.com> - 4:1.4.0
- updated nx-X11, nxproxy, nxcomp, nxagent and nxdesktop
- released to address X11 security concerns.

* Tue Nov 09 2004 Rick Stout <zipsonci[AT]gmail.com> - 3:1.4.0
- updated to 1.4.0 final

* Mon Oct 11 2004 Rick Stout <zipsonic[AT]gmail.com> - 2:1.4.0
- Changed naming structure to be more friendly (lowercase)

* Fri Oct 07 2004 Rick Stout <zipsonic[AT]gmail.com> - 1:1.4.0
- Updated package dependencies

* Wed Sep 29 2004 Rick Stout <zipsonic[AT]gmail.com> - 0:1.4.0
- Initial Fedora RPM release.
- Updated SuSE package to work with Fedora

Summary: A set of basic GNU tools commonly used in shell scripts
Name:    coreutils
Version: 8.4
Release: 16.0.1%{?dist}
License: GPLv3+
Group:   System Environment/Base
Url:     http://www.gnu.org/software/coreutils/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
Source101:  coreutils-DIR_COLORS
Source102:  coreutils-DIR_COLORS.lightbgcolor
Source103:  coreutils-DIR_COLORS.256color
Source105:  coreutils-colorls.sh
Source106:  coreutils-colorls.csh
Source200:  coreutils-su.pamd
Source201:  coreutils-runuser.pamd
Source202:  coreutils-su-l.pamd
Source203:  coreutils-runuser-l.pamd

# From upstream
#"who" doesn't determine user's message status correctly - #454261
Patch1: coreutils-8.4-who-msgstatus.patch
#fix detection of xattr support in configure
Patch2: coreutils-8.4-xattrmodule.patch

# Our patches
#general patch to workaround koji build system issues
Patch100: coreutils-6.10-configuration.patch
#add note about no difference between binary/text mode on Linux - md5sum manpage
Patch101: coreutils-6.10-manpages.patch
#temporarily workaround probable kernel issue with TCSADRAIN(#504798)
Patch102: coreutils-7.4-sttytcsadrain.patch
#add support for dtr/dsr to stty
Patch103: coreutils-445213-stty-dtrdsr.patch
#do display processor type for uname -p/-i based on uname(2) syscall
Patch104: coreutils-8.2-uname-processortype.patch
#bz 479364 (df --direct)
Patch105: coreutils-df-direct.patch
#bz 600384 - some japanese translation missing (as marked fuzzy)
Patch106: coreutils-fuzzyjapanesetranslation.patch

# sh-utils
#add info about TZ envvar to date manpage
Patch703: sh-utils-2.0.11-dateman.patch
#set paths for su explicitly, don't get influenced by paths.h
Patch704: sh-utils-1.16-paths.patch
# RMS will never accept the PAM patch because it removes his historical
# rant about Twenex and the wheel group, so we'll continue to maintain
# it here indefinitely.
Patch706: coreutils-pam.patch
Patch713: coreutils-4.5.3-langinfo.patch

# (sb) lin18nux/lsb compliance - multibyte functionality patch
Patch800: coreutils-i18n.patch

#Call setsid() in su under some circumstances (bug #173008).
Patch900: coreutils-setsid.patch
#make runuser binary based on su.c
Patch907: coreutils-5.2.1-runuser.patch
#getgrouplist() patch from Ulrich Drepper.
Patch908: coreutils-getgrouplist.patch
#Prevent buffer overflow in who(1) (bug #158405).
Patch912: coreutils-overflow.patch
#split the PAM scripts for "su -l"/"runuser -l" from that of normal "su" and
#"runuser" (#198639)
Patch915: coreutils-split-pam.patch
#prevent koji build failure with wrong getfacl exit code
Patch916: coreutils-getfacl-exit-code.patch
#compile su with pie flag and RELRO protection
Patch917: coreutils-8.4-su-pie.patch
#document rare usefulness of --sleep-interval with inotify support
Patch918: coreutils-8.4-tail-sleepinterval.patch
#fix double free error in tac for input line longer than 16KiB(#628212)
Patch919: coreutils-8.4-tac-doublefree.patch
#fix segfault in sort if LC_TIME differs from the rest of locales(#649224)
Patch920: coreutils-8.4-sort-monthssigsegv.patch
#make note in infopage about mkdir --mode behaviour(#6092620
Patch921: coreutils-8.4-mkdir-modenote.patch
#make note about dropped ninth bit of 3-digit octal values in byte
#representations(#660033)
Patch922: coreutils-8.4-echooctalinfo.patch
#document that dd's iflag=fulblock prevents dd's oflag=direct
#automatic turn off when reading via pipe(#614605)
Patch923: coreutils-8.4-dddirectturnoff.patch
#su: fix shell suspend in tcsh (#703712)
Patch924: coreutils-8.4-tcshsuspend.patch
#ls: use acl_extended_file_nofollow() to prevent unnecessary autofs mounts(#720325)
Patch925: coreutils-8.4-ls-aclnofollow.patch

#SELINUX Patch - implements Redhat changes
#(upstream did some SELinux implementation unlike with RedHat patch)
Patch950: coreutils-selinux.patch
Patch951: coreutils-selinuxmanpages.patch
#prevent build failure on system with mock>=1.1.9
Patch952: coreutils-8.4-newmock.patch

#turn off inotify on gpfs
Patch1000: gpfsfix.patch

BuildRequires: libselinux-devel
BuildRequires: libacl-devel
BuildRequires: gettext bison
BuildRequires: texinfo
BuildRequires: autoconf
BuildRequires: automake
%{?!nopam:BuildRequires: pam-devel}
BuildRequires: libcap-devel
BuildRequires: libattr-devel >= 2.2.49-6
BuildRequires: gmp-devel
BuildRequires: attr
BuildRequires: strace

Requires(post): libselinux
Requires:       libattr
Requires(pre): /sbin/install-info
Requires(preun): /sbin/install-info
Requires(post): /sbin/install-info
Requires(post): grep
%{?!nopam:Requires: pam }
Requires(post): libcap
Requires:       ncurses
Requires:       gmp
Requires: %{name}-libs = %{version}-%{release}

Provides: fileutils = %{version}-%{release}
Provides: sh-utils = %{version}-%{release}
Provides: stat = %{version}-%{release}
Provides: textutils = %{version}-%{release}
#old mktemp package had epoch 3, so we have to use 4 for coreutils
Provides: mktemp = 4:%{version}-%{release}
Obsoletes: mktemp < 4:%{version}-%{release}
Obsoletes: fileutils <= 4.1.9
Obsoletes: sh-utils <= 2.0.12
Obsoletes: stat <= 3.3
Obsoletes: textutils <= 2.0.21

%description
These are the GNU core utilities.  This package is the combination of
the old GNU fileutils, sh-utils, and textutils packages.

%package libs
Summary: Libraries for %{name}
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description libs
Libraries for coreutils package.

%prep
%setup -q

# From upstream
%patch1 -p1 -b .whomsg
%patch2 -p1 -b .xattr

# Our patches
%patch100 -p1 -b .configure
%patch101 -p1 -b .manpages
%patch102 -p1 -b .tcsadrain
%patch103 -p1 -b .dtrdsr
%patch104 -p1 -b .sysinfo
%patch105 -p1 -b .dfdirect
%patch106 -p1 -b .japfuzzy

# sh-utils
%patch703 -p1 -b .dateman
%patch704 -p1 -b .paths
%patch706 -p1 -b .pam
%patch713 -p1 -b .langinfo
# li18nux/lsb
%patch800 -p1 -b .i18n

# Coreutils
%patch900 -p1 -b .setsid
%patch907 -p1 -b .runuser
%patch908 -p1 -b .getgrouplist
%patch912 -p1 -b .overflow
%patch915 -p1 -b .splitl
%patch916 -p1 -b .getfacl-exit-code
%patch917 -p1 -b .pie
%patch918 -p1 -b .sleepinotify
%patch919 -p1 -b .doublefree
%patch920 -p1 -b .monthnames
%patch921 -p1 -b .mkdirmode
%patch922 -p1 -b .octal
%patch923 -p1 -b .directturnoff
%patch924 -p1 -b .tcshsuspend
%patch925 -p1 -b .nofollow

#SELinux
%patch950 -p1 -b .selinux
%patch951 -p1 -b .selinuxman
%patch952 -p1 -b .newmock

# PUIAS patches
%patch1000 -p1 -b .gpfsfix

chmod a+x tests/misc/sort-mb-tests tests/df/direct tests/ls/slink-acl

#fix typos/mistakes in localized documentation(#439410, #440056)
find ./po/ -name "*.p*" | xargs \
 sed -i \
 -e 's/-dpR/-cdpR/'

%build
%ifarch s390 s390x
# Build at -O1 for the moment (bug #196369).
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -fPIC -O1"
%else
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -fpic"
%endif
%{expand:%%global optflags %{optflags} -D_GNU_SOURCE=1}
#autoreconf -i -v
touch aclocal.m4 configure config.hin Makefile.in */Makefile.in
aclocal -I m4
autoconf --force
automake --copy --add-missing
%configure --enable-largefile %{?!nopam:--enable-pam} \
           --enable-selinux \
           --enable-install-program=su,hostname,arch \
           --with-tty-group \
           DEFAULT_POSIX2_VERSION=200112 alternative=199209 || :

# Regenerate manpages
touch man/*.x

make all %{?_smp_mflags} \
         %{?!nopam:CPPFLAGS="-DUSE_PAM"}

# XXX docs should say /var/run/[uw]tmp not /etc/[uw]tmp
sed -i -e 's,/etc/utmp,/var/run/utmp,g;s,/etc/wtmp,/var/run/wtmp,g' doc/coreutils.texi

%check
make check

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# man pages are not installed with make install
make mandir=$RPM_BUILD_ROOT%{_mandir} install-man

# fix japanese catalog file
if [ -d $RPM_BUILD_ROOT%{_datadir}/locale/ja_JP.EUC/LC_MESSAGES ]; then
   mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale/ja/LC_MESSAGES
   mv $RPM_BUILD_ROOT%{_datadir}/locale/ja_JP.EUC/LC_MESSAGES/*mo \
      $RPM_BUILD_ROOT%{_datadir}/locale/ja/LC_MESSAGES
   rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/ja_JP.EUC
fi

bzip2 -9f ChangeLog

# let be compatible with old fileutils, sh-utils and textutils packages :
mkdir -p $RPM_BUILD_ROOT{/bin,%_bindir,%_sbindir,/sbin}
%{?!nopam:mkdir -p $RPM_BUILD_ROOT%_sysconfdir/pam.d}
for f in arch basename cat chgrp chmod chown cp cut date dd df echo env false link ln ls mkdir mknod mktemp mv nice pwd readlink rm rmdir sleep sort stty sync touch true uname unlink
do
    mv $RPM_BUILD_ROOT{%_bindir,/bin}/$f
done

# chroot was in /usr/sbin :
mv $RPM_BUILD_ROOT{%_bindir,%_sbindir}/chroot
# {env,cut,readlink} were previously moved from /usr/bin to /bin and linked into
for i in env cut readlink; do ln -sf ../../bin/$i $RPM_BUILD_ROOT/usr/bin; done

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -p -c -m644 %SOURCE101 $RPM_BUILD_ROOT%{_sysconfdir}/DIR_COLORS
install -p -c -m644 %SOURCE102 $RPM_BUILD_ROOT%{_sysconfdir}/DIR_COLORS.lightbgcolor
install -p -c -m644 %SOURCE103 $RPM_BUILD_ROOT%{_sysconfdir}/DIR_COLORS.256color
install -p -c -m644 %SOURCE105 $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/colorls.sh
install -p -c -m644 %SOURCE106 $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/colorls.csh

# su
install -m 4755 src/su $RPM_BUILD_ROOT/bin
install -m 755 src/runuser $RPM_BUILD_ROOT/sbin
# do not ship runuser in /usr/bin/runuser
rm -rf $RPM_BUILD_ROOT/usr/bin/runuser

# These come from util-linux and/or procps.
for i in hostname uptime kill ; do
    rm $RPM_BUILD_ROOT{%_bindir/$i,%_mandir/man1/$i.1}
done

%{?!nopam:install -p -m 644 %SOURCE200 $RPM_BUILD_ROOT%_sysconfdir/pam.d/su}
%{?!nopam:install -p -m 644 %SOURCE202 $RPM_BUILD_ROOT%_sysconfdir/pam.d/su-l}
%{?!nopam:install -p -m 644 %SOURCE201 $RPM_BUILD_ROOT%_sysconfdir/pam.d/runuser}
%{?!nopam:install -p -m 644 %SOURCE203 $RPM_BUILD_ROOT%_sysconfdir/pam.d/runuser-l}

# Compress ChangeLogs from before the fileutils/textutils/etc merge
bzip2 -f9 old/*/C*

# Use hard links instead of symbolic links for LC_TIME files (bug #246729).
find %{buildroot}%{_datadir}/locale -type l | \
(while read link
 do
   target=$(readlink "$link")
   rm -f "$link"
   ln "$(dirname "$link")/$target" "$link"
 done)

%find_lang %name

# (sb) Deal with Installed (but unpackaged) file(s) found
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# We must deinstall these info files since they're merged in
# coreutils.info. else their postun'll be run too late
# and install-info will fail badly because of duplicates
for file in sh-utils textutils fileutils; do
  if [ -f %{_infodir}/$file.info.gz ]; then
    /sbin/install-info --delete %{_infodir}/$file.info.gz --dir=%{_infodir}/dir &> /dev/null || :
  fi
done

%preun
if [ $1 = 0 ]; then
  if [ -f %{_infodir}/%{name}.info.gz ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
  fi
fi

%post
/bin/grep -v '(sh-utils)\|(fileutils)\|(textutils)' %{_infodir}/dir > \
  %{_infodir}/dir.rpmmodify || exit 0
    /bin/mv -f %{_infodir}/dir.rpmmodify %{_infodir}/dir
if [ -f %{_infodir}/%{name}.info.gz ]; then
  /sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%dir %{_datadir}/locale/*/LC_TIME
%config(noreplace) %{_sysconfdir}/DIR_COLORS*
%config(noreplace) %{_sysconfdir}/profile.d/*
%{?!nopam:%config(noreplace) %{_sysconfdir}/pam.d/su}
%{?!nopam:%config(noreplace) %{_sysconfdir}/pam.d/su-l}
%{?!nopam:%config(noreplace) %{_sysconfdir}/pam.d/runuser}
%{?!nopam:%config(noreplace) %{_sysconfdir}/pam.d/runuser-l}
%doc COPYING ABOUT-NLS ChangeLog.bz2 NEWS README THANKS TODO old/*
/bin/arch
/bin/basename
/bin/cat
/bin/chgrp
/bin/chmod
/bin/chown
/bin/cp
/bin/cut
/bin/date
/bin/dd
/bin/df
/bin/echo
/bin/env
/bin/false
/bin/link
/bin/ln
/bin/ls
/bin/mkdir
/bin/mknod
/bin/mv
/bin/nice
/bin/pwd
/bin/readlink
/bin/rm
/bin/rmdir
/bin/sleep
/bin/sort
/bin/stty
%attr(4755,root,root) /bin/su
/bin/sync
/bin/mktemp
/bin/touch
/bin/true
/bin/uname
/bin/unlink
%_bindir/*
%_infodir/coreutils*
%_mandir/man*/*
%_sbindir/chroot
/sbin/runuser

%files libs
%defattr(-, root, root, -)
%{_libdir}/coreutils

%changelog
* Wed Oct 05 2011 Ondrej Vasik <ovasik@redhat.com> - 8.4-16
- improve the acl_extended_file_nofollow() fix to prevent
 ls -L regression(#720325)

* Wed Aug 17 2011 Ondrej Vasik <ovasik@redhat.com> - 8.4-15
- ensure that we have libacl-devel with support for
  acl_extened_file_nofollow()

* Thu Aug 11 2011 Ondrej Vasik <ovasik@redhat.com> - 8.4-14
- tweak documentation of tail --sleep-interval (#725618)
- prevent build failure on system with mock>=1.1.9 (#691292)
- su: fix shell suspend in tcsh (#703712)
- ls: use acl_extended_file_nofollow() to prevent unnecessary
  autofs mounts(#720325)
- fix cp -Z functionality if the destination exists(#715557)

* Thu Mar 10 2011 Ondrej Vasik <ovasik@redhat.com> - 8.4-13
- fix possible uninitalized variables usage caused by i18n
  patch(#683799)

* Wed Feb 02 2011 Ondrej Vasik <ovasik@redhat.com> - 8.4-12
- document that dd's iflag=fulblock prevents dd's oflag=direct
 automatic turn off when reading via pipe(#614605)

* Mon Jan 17 2011 Ondrej Vasik <ovasik@redhat.com> - 8.4-11
- adjust the wording in the octal value byte representation
  documentation to match with upstream(#660033)

* Fri Jan 14 2011 Ondrej Vasik <ovasik@redhat.com> - 8.4-10
- compile coreutils su with RELRO and PIE again(#630017)
- document rare usefulness of tail options --sleep-interval
  and --max-unchanged-stats with inotify support(#662900)
- fix double free error in tac for input line longer
  than 16KiB(#628212)
- fix segfault in sort if LC_TIME differs from the rest
  of locales(#649224)
- fix support for DTR/DSR control flow in stty(#598631)
- clarify mkdir --mode behaviour in info documentation
  (#609262)
- inform about dropped ninth bit of 3-digit octal values in byte
  representations in info documentation(#660033)

* Mon Jun 14 2010 Ondrej Vasik <ovasik@redhat.com> - 8.4-9
- compile coreutils with xattr support again(#603617)

* Mon Jun 07 2010 Ondrej Vasik <ovasik@redhat.com> - 8.4-8
- remove word "fuzzy" from japanese translation of ls -l
  timestamp format(#600384)

* Wed Apr 28 2010 Ondrej Vasik <ovasik@redhat.com> - 8.4-7
- doublequote LS_COLORS in colorls.*sh scripts to speedup
  shell start(#586949)
- update /etc/DIR_COLORS* files
- move readlink from /usr/bin to bin, keep symlink in
  /usr/bin(#586948)

* Mon Mar 29 2010 Kamil Dudka <kdudka@redhat.com> - 8.4-6
- a new option df --direct (#479364)

* Sat Mar 20 2010 Ondrej Vasik <ovasik@redhat.com> - 8.4-5
- run tput colors in colorls profile.d scripts only
  in the interactive mode(#586947)

* Fri Feb 12 2010 Ondrej Vasik <ovasik@redhat.com> - 8.4-4
- fix exit status of terminated child processes in su with
  pam(#563852)
- do not depend on selinux patch application in
  _require_selinux tests

* Fri Jan 29 2010 Ondrej Vasik <ovasik@redhat.com> - 8.4-3
- do not fail tests if there are no loopdevices left
  (#558898)

* Mon Jan 25 2010 Ondrej Vasik <ovasik@redhat.com> - 8.4-2
- who doesn't determine user's message status correctly
  (#553625)

* Thu Jan 14 2010 Ondrej Vasik <ovasik@redhat.com> - 8.4-1
- new upstream release 8.4

* Fri Jan 08 2010 Ondrej Vasik <ovasik@redhat.com> - 8.3-1
- new upstream release 8.3, fixes several regressions

* Wed Jan 06 2010 Ondrej Vasik <ovasik@redhat.com> - 8.2-3
- require gmp-devel/gmp for large numbers support
- fix misc/selinux root-only test
- bring back uname -p/-i functionality except of the
  athlon hack
- comment patches

* Wed Dec 16 2009 Ondrej Vasik <ovasik@redhat.com> - 8.2-2
- Sanity changes(#548421):
  - use grep instead of deprecated egrep in colorls.sh script
  - remove unnecessary versioned requires
  - remove non-upstream hack for uname -p
  - add dtrdsr patch from RHEL-5 to prevent regression

* Fri Dec 11 2009 Ondrej Vasik <ovasik@redhat.com> - 8.2-1
- new upstream release 8.2
- removed applied patches, temporarily do not run dup_cloexec()
  dependent gnulib tests failing in koji
- do not use bold attribute in 256-colors dircolor
- CVE-2009-4135 coreutils: Unsafe temporary directory use
  in "distcheck" rule(#546705)

* Fri Nov 27 2009 Ondrej Vasik <ovasik@redhat.com> - 8.1-1
- new upstream release 8.1
- fix build under koji (no test failures with underlying
  RHEL-5 XEN kernel due to unsearchable path and lack of
  futimens functionality)

* Wed Oct 07 2009 Ondrej Vasik <ovasik@redhat.com> - 8.0-2
- update /etc/DIR_COLORS* files

* Wed Oct 07 2009 Ondrej Vasik <ovasik@redhat.com> - 8.0-1
- New upstream release 8.0 (beta), defuzz patches,
  remove applied patches

* Mon Oct 05 2009 Ondrej Vasik <ovasik@redhat.com> - 7.6-7
- chcon no longer aborts on a selinux disabled system
  (#527142)

* Fri Oct 02 2009 Ondrej Vasik <ovasik@redhat.com> - 7.6-6
- ls -LR exits with status 2, not 0, when it encounters
  a cycle(#525402)
- ls: print "?", not "0" as inode of dereferenced dangling
  symlink(#525400)
- call the install-info on .gz info files

* Tue Sep 22 2009 Ondrej Vasik <ovasik@redhat.com> - 7.6-5
- improve and correct runuser documentation (#524805)

* Mon Sep 21 2009 Ondrej Vasik <ovasik@redhat.com> - 7.6-4
- add dircolors color for GNU lzip (#516897)

* Fri Sep 18 2009 Ondrej Vasik <ovasik@redhat.com> - 7.6-3
- fixed typo in DIR_COLORS.256color causing no color for
  multihardlink

* Wed Sep 16 2009 Ondrej Vasik <ovasik@redhat.com> - 7.6-2
- fix copying of extended attributes for read only source
  files

* Sat Sep 12 2009 Ondrej Vasik <ovasik@redhat.com> - 7.6-1
- new upstream bugfix release 7.6, removed applied patches,
  defuzzed the rest

* Thu Sep 10 2009 Ondrej Vasik <ovasik@redhat.com> - 7.5-6
- fix double free error in fold for singlebyte locales
  (caused by multibyte patch)

* Tue Sep 08 2009 Ondrej Vasik <ovasik@redhat.com> - 7.5-5
- fix sort -h for multibyte locales (reported via
  http://bugs.archlinux.org/task/16022)

* Thu Sep 03 2009 Ondrej Vasik <ovasik@redhat.com> - 7.5-4
- fixed regression where df -l <device> as regular user
  cause "Permission denied" (#520630, introduced by fix for
  rhbz #497830)

* Fri Aug 28 2009 Ondrej Vasik <ovasik@redhat.com> - 7.5-3
- ls -i: print consistent inode numbers also for mount points
  (#453709)

* Mon Aug 24 2009 Ondrej Vasik <ovasik@redhat.com> - 7.5-2
- Better fix than workaround the koji insufficient utimensat
  support issue to prevent failures in other packages

* Fri Aug 21 2009 Ondrej Vasik <ovasik@redhat.com> - 7.5-1
- New upstream release 7.5, remove already applied patches,
  defuzz few others, xz in default set(by dependencies),
  so no explicit br required
- skip two new tests on system with insufficient utimensat
  support(e.g. koji)
- libstdbuf.so in separate coreutils-libs subpackage
- update /etc/DIRCOLORS*

* Thu Aug 06 2009 Ondrej Vasik <ovasik@redhat.com> - 7.4-6
- do process install-info only with info files present(#515970)
- BuildRequires for xz, use xz tarball

* Wed Aug 05 2009 Kamil Dudka <kdudka@redhat.com> - 7.4-5
- ls -1U with two or more arguments (or with -R or -s) works properly again
- install runs faster again with SELinux enabled (#479502)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 06 2009 Ondrej Vasik <ovasik@redhat.com> 7.4-3
- do not ignore sort's version sort for multibyte locales
  (#509688)

* Thu Jun 16 2009 Ondrej Vasik <ovasik@redhat.com> 7.4-2
- temporarily workaround probable kernel issue with
  TCSADRAIN(#504798)

* Mon May 25 2009 Ondrej Vasik <ovasik@redhat.com> 7.4-1
- new upstream release 7.4, removed applied patches

* Thu Apr 23 2009 Ondrej Vasik <ovasik@redhat.com> 7.2-3
- fix segfaults in join (i18n patch) when using multibyte
  locales(#497368)

* Fri Apr 17 2009 Ondrej Vasik <ovasik@redhat.com> 7.2-2
- make mv xattr support failures silent (as is done for
  cp -a) - #496142

* Tue Mar 31 2009 Ondrej Vasik <ovasik@redhat.com> 7.2-1
- New upstream bugfix release 7.2
- removed applied patches
- temporarily disable strverscmp failing gnulib test

* Thu Mar 19 2009 Ondrej Vasik <ovasik@redhat.com> 7.1-7
- do not ship /etc/DIR_COLORS.xterm - as many terminals
  use TERM xterm and black background as default - making
  ls color output unreadable
- shipping /etc/DIR_COLORS.lightbgcolor instead of it for
  light(white/gray) backgrounds
- try to preserve xattrs in cp -a when possible

* Mon Mar 02 2009 Ondrej Vasik <ovasik@redhat.com> 7.1-6
- fix sort bugs (including #485715) for multibyte locales
  as well

* Fri Feb 27 2009 Ondrej Vasik <ovasik@redhat.com> 7.1-5
- fix infinite loop in recursive cp (upstream, introduced
  by 7.1)

* Thu Feb 26 2009 Ondrej Vasik <ovasik@redhat.com> 7.1-4
- fix showing ACL's for ls -Z (#487374), fix automatic
  column width for it as well

* Wed Feb 25 2009 Ondrej Vasik <ovasik@redhat.com> 7.1-3
- fix couple of bugs (including #485715) in sort with
  determining end of fields(upstream)

* Wed Feb 25 2009 Ondrej Vasik <ovasik@redhat.com> 7.1-2
- workaround libcap issue with broken headers (#483548)
- fix gnulib testsuite failure (4x77 (skip) is not
  77(skip) ;) )

* Tue Feb 24 2009 Ondrej Vasik <ovasik@redhat.com> - 7.1-1
- New upstream release 7.1 (temporarily using tar.gz tarball
  as there are no xz utils in Fedora), removed applied
  patches, amended patches and LS_COLORS files

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 28 2009 Kamil Dudka <kdudka@redhat.com> - 7.0-7
- added BuildRequires for libattr-devel and attr

* Wed Jan 28 2009 Kamil Dudka <kdudka@redhat.com> - 7.0-6
- cp/mv: add --no-clobber (-n) option to not overwrite target
- cp/mv: add xattr support (#202823)

* Thu Dec 04 2008 Ondrej Vasik <ovasik@redhat.com> - 7.0-5
- fix info documentation for expr command as well(#474434)

* Thu Dec 04 2008 Ondrej Vasik <ovasik@redhat.com> - 7.0-4
- fixed syntax error w/ "expr" command using negative
  string/integer as first (i.e expr -125) - due to
  complexity of changes used diff against upstream git-head
  (#474434)
- enable total-awk test again (and skip it when df not working)

* Tue Nov 25 2008 Ondrej Vasik <ovasik@redhat.com> - 7.0-3
- package summary tuning

* Fri Nov 21 2008 Ondrej Vasik <ovasik@redhat.com> - 7.0-2
- added requirements for util-linux-ng >= 2.14
  because of file conflict in update from F-8/F-9(#472445)
- some sed cleanup, df totaltests patch changes (not working
  correctly yet :( )

* Wed Nov 12 2008 Ondrej Vasik <ovasik@redhat.com> - 7.0-1
- new upstream release
- modification/removal of related patches
- use automake 1.10.1 instead of 1.10a
- temporarily skip df --total tests (failures),
  timeout-paramaters (failure on ppc64)

* Mon Nov 03 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-17
- Requires: ncurses (#469277)

* Wed Oct 21 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-16
- make possible to disable capability in ls due to
  performance impact when not cached(#467508)
- do not patch generated manpages - generate them at build
  time
- do not mistakenly display -g and -G runuser option in su
  --help output

* Mon Oct 13 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-15
- fix several date issues(e.g. countable dayshifts, ignoring
  some cases of relative offset, locales conversions...)
- clarify ls exit statuses documentation (#446294)

* Sun Oct 12 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-14
- cp -Z now correctly separated in man page (#466646)
- cp -Z works again (#466653)
- make preservation of SELinux CTX non-mandatory for
  preserve=all cp option

* Wed Oct 08 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-13
- remove unimplemented (never accepted by upstream) option
  for chcon changes only. Removed from help and man.
- remove ugly lzma hack as lzma is now supported by setup
  macro

* Mon Oct 06 2008 Jarod Wilson <jarod@redhat.com> - 6.12-12
- fix up potential test failures when building in certain
  slightly quirky environments (part of bz#442352)

* Mon Oct 06 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-11
- added requires for libattr (#465569)

* Mon Sep 29 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-10
- seq should no longer fail to display final number of some
  float usages of seq with utf8 locales(#463556)

* Wed Aug 13 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-9
- mention that DISPLAY and XAUTHORITY envvars are preserved
  for pam_xauth in su -l (#450505)

* Mon Aug 04 2008 Kamil Dudka <kdudka@redhat.com> - 6.12-8
- ls -U1 now uses constant memory

* Wed Jul 24 2008 Kamil Dudka <kdudka@redhat.com> - 6.12-7
- dd: iflag=fullblock now read full blocks if possible
  (#431997, #449263)
- ls: --color now highlights files with capabilities (#449985)

* Wed Jul 16 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-6
- Get rid off fuzz in patches

* Fri Jul 04 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-5
- fix authors for basename and echo
- fix who info pages, print last runlevel only for printable
  chars

* Mon Jun 16 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-4
- print verbose output of chcon with newline after each 
  message (#451478)

* Fri Jun 06 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-3
- workaround for koji failures(#449910, #442352) now 
  preserves timestamps correctly - fallback to supported
  functions, added test case
- runuser binary is no longer doubled in /usr/bin/runuser

* Wed Jun 04 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-2
- workaround for strange koji failures(#449910,#442352)
- fixed ls -ZC segfault(#449866, introduced by 6.10-1 
  SELinux patch reworking) 

* Mon Jun 02 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-1
- New upstream release 6.12, adapted patches

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 6.11-5
- fix SHA256/SHA512 to work on sparc

* Tue May 20 2008 Ondrej Vasik <ovasik@redhat.com> - 6.11-4
- fixed a HUGE memory leak in install binary(#447410)

* Mon May 19 2008 Ondrej Vasik <ovasik@redhat.com> - 6.11-3
- added arch utility (from util-linux-ng)
- do not show executable file types without executable bit
  in colored ls as executable

* Wed Apr 23 2008 Ondrej Vasik <ovasik@redhat.com> - 6.11-2
- Do not show misleading scontext in id command when user
  is specified (#443485)
- Avoid possible test failures on non-english locales

* Mon Apr 21 2008 Ondrej Vasik <ovasik@redhat.com> - 6.11-1
- New upstream release 6.11 
- removed accepted patches + few minor patch changes

* Fri Apr 18 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-21
- fix wrong checksum line handling in sha1sum -c 
  command(#439531)

* Tue Apr 15 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-20
- fix possible segfault in sha1sum/md5sum command

* Mon Apr 14 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-19
- fix possible build-failure typo in i18n patch(#442205)

* Mon Apr  7 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-18
- fix colorls.sh syntax with Zsh (#440652)
- mention that cp -a includes -c option + mention cp -c 
  option in manpages (#440056)
- fix typo in runuser manpages (#439410)

* Sat Mar 29 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-17
- better workaround of glibc getoptc change(factor test)
- don't segfault mknod, mkfifo with invalid-selinux-context

* Thu Mar 27 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-16
- keep LS_COLORS when USER_LS_COLORS defined
- someupstream fixes:
- mkdir -Z invalid-selinux-context dir no longer segfaults
- ptx with odd number of backslashes no longer leads to buffer
  overflow
- paste -d'\' file" no longer ovveruns memory

* Wed Mar 26 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-15
- covered correct handling for some test conditions failures
  e.g. root build+selinux active and not running mcstrans(d)
  or selinux enforcing (#436717)

* Wed Mar 19 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-14
- mv: never unlink a destination file before calling rename
  (upstream, #438076)

* Mon Mar 17 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-13
- disable echo option separator behavior(added by #431005,
  request for removal #437653 + upstream)
- temporarily disabled longoptions change until full 
  clarification upstreamery (#431005)

* Tue Mar 11 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-12
- fixed harmless double close of stdout in dd(#436368)

* Thu Mar  6 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-11
- fixed broken order of params in stat(#435669)

* Tue Mar  4 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-10
- colorls.csh missing doublequotes (#435789)
- fixed possibility to localize verbose outputs

* Mon Mar  3 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-9
- consolidation of verbose output to stdout (upstream)

* Mon Feb 18 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-8
- use default security context in install - broken by 
  coreutils-6.10 update(#319231)
- some sh/csh scripts optimalizations(by ville.skytta@iki.fi,
  - #433189, #433190)

* Mon Feb 11 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-7
- keep old csh/sh usermodified colorls shell scripts
  but use the new ones(#432154)

* Thu Feb  7 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-6
- better 256-color support in colorls shell scripts
- color tuning(based on feedback in #429121)

* Mon Feb  4 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-5
- enabled 256-color support in colorls shell scripts(#429121)
- fixed syntax error in csh script(#431315)

* Thu Jan 31 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-4
- forgotten return in colorls.sh change

* Thu Jan 31 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-3
- fix unability of echo to display certain strings(added --
  separator, #431005)
- do not require only one long_opt for certain commands 
  e.g. sleep, yes - but use first usable (#431005)
- do not override userspecified LS_COLORS variable, but
  use it for colored ls(#430827)
- discard errors from dircolors to /dev/null + some tuning 
  of lscolor sh/csh scripts(#430823)
- do not consider files with SELinux security context as
  files having ACL in ls long format(#430779)

* Mon Jan 28 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-2
- some manpages improvements(#406981,#284881)
- fix non-versioned obsoletes of mktemp(#430407)

* Fri Jan 25 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-1
- New upstream release(changed %%prep because of lack of lzma
  support in %%setup macro)
- License GPLv3+
- removed patches cp-i-u,du-ls-upstream,statsecuritycontext,
  futimens,getdateYYYYMMDD,ls-x
- modified patches to be compilable after upstream changes
- selinux patch reworked to have backward compatibility with
  F8(cp,ls and stat behaviour differ from upstream in SELinux
  options)
- su-l/runuser-l pam file usage a bit documented(#368721)
- more TERMs for DIR_COLORS, added colors for audio files,
  more image/compress file types(taken from upstream 
  dircolors.hin)
- new file DIR_COLORS.256color which takes advantage from 
  256color term types-not really used yet(#429121)

* Wed Jan 16 2008 Ondrej Vasik <ovasik@redhat.com> - 6.9-17
- added several missing colored TERMs(including rxvt-unicode,
  screen-256color and xterm-256color) to DIR_COLORS and
  DIR_COLORS.xterm(#239266) 

* Wed Dec 05 2007 Ondrej Vasik <ovasik@redhat.com> - 6.9-16
- fix displaying of security context in stat(#411181)

* Thu Nov 29 2007 Ondrej Vasik <ovasik@redhat.com> - 6.9-15
- completed fix of wrong colored broken symlinks in ls(#404511)

* Fri Nov 23 2007 Ondrej Vasik <ovasik@redhat.com> - 6.9-14
- fixed bug in handling YYYYMMDD date format with relative
  signed offset(#377821)

* Tue Nov 13 2007 Ondrej Vasik <ovasik@redhat.com> - 6.9-13
- fixed bug in selinux patch which caused bad preserving
  of security context in install(#319231)

* Fri Nov 02 2007 Ondrej Vasik <ovasik@redhat.com> - 6.9-12
- added some upstream supported dircolors TERMs(#239266)
- fixed du output for unaccesible dirs(#250089)
- a bit of upstream tunning for symlinks

* Tue Oct 30 2007 Ondrej Vasik <ovasik@redhat.com> - 6.9-11
- allow cp -a to rewrite file on different filesystem(#219900)
  (based on upstream patch)

* Mon Oct 29 2007 Ondrej Vasik <ovasik@redhat.com> - 6.9-10
- modified coreutils-i18n.patch because of sort -R in
  a non C locales(fix by Andreas Schwab) (#249315)

* Mon Oct 29 2007 Ondrej Vasik <ovasik@redhat.com> - 6.9-9
- applied upstream patch for runuser to coreutils-selinux.patch(#232652)
- License tag to GPLv2+

* Thu Oct 25 2007 Ondrej Vasik <ovasik@redhat.com> - 6.9-8
- applied upstream patch for cp and mv(#248591)

* Thu Aug 23 2007 Pete Graner <pgraner@redhat.com> - 6.9-7
- Fix typo in spec file. (CVS merge conflict leftovers)

* Thu Aug 23 2007 Pete Graner <pgraner@redhat.com> - 6.9-6
- Remove --all-name from spec file its now provided in the upstream rpm's find-lang.sh
- Rebuild

* Tue Aug 14 2007 Tim Waugh <twaugh@redhat.com> 6.9-5
- Don't generate runuser.1 since we ship a complete manpage for it
  (bug #241662).

* Wed Jul  4 2007 Tim Waugh <twaugh@redhat.com> 6.9-4
- Use hard links instead of symbolic links for LC_TIME files (bug #246729).

* Wed Jun 13 2007 Tim Waugh <twaugh@redhat.com> 6.9-3
- Fixed 'ls -x' output (bug #240298).
- Disambiguate futimens() from the glibc implementation (bug #242321).

* Mon Apr 02 2007 Karsten Hopp <karsten@redhat.com> 6.9-2
- /bin/mv in %%post requires libselinux

* Mon Mar 26 2007 Tim Waugh <twaugh@redhat.com> 6.9-1
- 6.9.

* Fri Mar  9 2007 Tim Waugh <twaugh@redhat.com>
- Better install-info scriptlets (bug #225655).

* Thu Mar  1 2007 Tim Waugh <twaugh@redhat.com> 6.8-1
- 6.8+, in preparation for 6.9.

* Thu Feb 22 2007 Tim Waugh <twaugh@redhat.com> 6.7-9
- Use sed instead of perl for text replacement (bug #225655).
- Use install-info scriptlets from the guidelines (bug #225655).

* Tue Feb 20 2007 Tim Waugh <twaugh@redhat.com> 6.7-8
- Don't mark profile scripts as config files (bug #225655).
- Avoid extra directory separators (bug #225655).

* Mon Feb 19 2007 Tim Waugh <twaugh@redhat.com> 6.7-7
- Better Obsoletes/Provides versioning (bug #225655).
- Use better defattr (bug #225655).
- Be info file compression tolerant (bug #225655).
- Moved changelog compression to %%install (bug #225655).
- Prevent upstream changes being masked (bug #225655).
- Added a comment (bug #225655).
- Use install -p for non-compiled files (bug #225655).
- Use sysconfdir macro for /etc (bug #225655).
- Use Requires(pre) etc for install-info (bug #225655).

* Fri Feb 16 2007 Tim Waugh <twaugh@redhat.com> 6.7-6
- Provide version for stat (bug #225655).
- Fixed permissions on profile scripts (bug #225655).

* Wed Feb 14 2007 Tim Waugh <twaugh@redhat.com> 6.7-5
- Removed unnecessary stuff in pre scriptlet (bug #225655).
- Prefix sources with 'coreutils-' (bug #225655).
- Avoid %%makeinstall (bug #225655).

* Tue Feb 13 2007 Tim Waugh <twaugh@redhat.com> 6.7-4
- Ship COPYING file (bug #225655).
- Use datadir and infodir macros in %%pre scriptlet (bug #225655).
- Use spaces not tabs (bug #225655).
- Fixed build root.
- Change prereq to requires (bug #225655).
- Explicitly version some obsoletes tags (bug #225655).
- Removed obsolete pl translation fix.

* Mon Jan 22 2007 Tim Waugh <twaugh@redhat.com> 6.7-3
- Make scriptlet unconditionally succeed (bug #223681).

* Fri Jan 19 2007 Tim Waugh <twaugh@redhat.com> 6.7-2
- Build does not require libtermcap-devel.

* Tue Jan  9 2007 Tim Waugh <twaugh@redhat.com> 6.7-1
- 6.7.  No longer need sort-compatibility, rename, newhashes, timestyle,
  acl, df-cifs, afs or autoconf patches.

* Tue Jan  2 2007 Tim Waugh <twaugh@redhat.com>
- Prevent 'su --help' showing runuser-only options such as --group.

* Fri Nov 24 2006 Tim Waugh <twaugh@redhat.com> 5.97-16
- Unbreak id (bug #217177).

* Thu Nov 23 2006 Tim Waugh <twaugh@redhat.com> 5.97-15
- Fixed stat's 'C' format specifier (bug #216676).
- Misleading 'id -Z root' error message (bug #211089).

* Fri Nov 10 2006 Tim Waugh <twaugh@redhat.com> 5.97-14
- Clarified runcon man page (bug #213846).

* Tue Oct 17 2006 Tim Waugh <twaugh@redhat.com> 5.97-13
- Own LC_TIME locale directories (bug #210751).

* Wed Oct  4 2006 Tim Waugh <twaugh@redhat.com> 5.97-12
- Fixed 'cp -Z' when destination exists, again (bug #189967).

* Thu Sep 28 2006 Tim Waugh <twaugh@redhat.com> 5.97-11
- Back-ported rename patch (bug #205744).

* Tue Sep 12 2006 Tim Waugh <twaugh@redhat.com> 5.97-10
- Ignore 'cifs' filesystems for 'df -l' (bug #183703).
- Include -g/-G in runuser man page (part of bug #199344).
- Corrected runuser man page (bug #200620).

* Thu Aug 24 2006 Tim Waugh <twaugh@redhat.com> 5.97-9
- Fixed warnings in pam, i18n, sysinfo, selinux and acl patches (bug #203166).

* Wed Aug 23 2006 Tim Waugh <twaugh@redhat.com> 5.97-8
- Don't chdir until after PAM bits in su (bug #197659).

* Tue Aug 15 2006 Tim Waugh <twaugh@redhat.com> 5.97-7
- Fixed 'sort -b' multibyte problem (bug #199986).

* Fri Jul 21 2006 Tim Waugh <twaugh@redhat.com> 5.97-6
- Added runuser '-g' and '-G' options (bug #199344).
- Added su '--session-command' option (bug #199066).

* Tue Jul 18 2006 Tomas Mraz <tmraz@redhat.com> 5.97-5
- 'include' su and runuser scripts in su-l and runuser-l scripts

* Thu Jul 13 2006 David Howells <dhowells@redhat.com> 5.97-4
- split the PAM scripts for "su -l"/"runuser -l" from that of normal "su" and
  "runuser" (#198639)
- add keyinit instructions to PAM scripts

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 5.97-3.1
- rebuild

* Tue Jul 11 2006 Tomas Mraz <tmraz@redhat.com> 5.97-3
- allow root to su to expired user (#152420)

* Thu Jun 29 2006 Tim Waugh <twaugh@redhat.com> 5.97-2
- Allow 'sort +1 -2' (patch from upstream).

* Sun Jun 25 2006 Tim Waugh <twaugh@redhat.com> 5.97-1
- 5.97.  No longer need tempname or tee patches, or pl translation.

* Sun Jun 25 2006 Tim Waugh <twaugh@redhat.com> 5.96-4
- Include new hashes (bug #196369).  Patch from upstream.
- Build at -O1 on s390 for the moment (bug #196369).

* Fri Jun  9 2006 Tim Waugh <twaugh@redhat.com>
- Fix large file support for temporary files.

* Mon Jun  5 2006 Tim Waugh <twaugh@redhat.com> 5.96-3
- Fixed Polish translation.

* Mon May 22 2006 Tim Waugh <twaugh@redhat.com> 5.96-2
- 5.96.  No longer need proc patch.

* Fri May 19 2006 Tim Waugh <twaugh@redhat.com>
- Fixed pr properly in multibyte locales (bug #192381).

* Tue May 16 2006 Tim Waugh <twaugh@redhat.com> 5.95-3
- Upstream patch to fix cp -p when proc is not mounted (bug #190601).
- BuildRequires libacl-devel.

* Mon May 15 2006 Tim Waugh <twaugh@redhat.com>
- Fixed pr in multibyte locales (bug #189663).

* Mon May 15 2006 Tim Waugh <twaugh@redhat.com> 5.95-2
- 5.95.

* Wed Apr 26 2006 Tim Waugh <twaugh@redhat.com> 5.94-4
- Avoid redeclared 'tee' function.
- Fix 'cp -Z' when the destination exists (bug #189967).

* Thu Apr 20 2006 Tim Waugh <twaugh@redhat.com> 5.94-3
- Make 'ls -Z' output more consistent with other output formats.

* Fri Mar 24 2006 Tim Waugh <twaugh@redhat.com> 5.94-2
- 5.94.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 5.93-7.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 5.93-7.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 23 2006 Tim Waugh <twaugh@redhat.com>
- Fixed chcon(1) bug reporting address (bug #178523).

* Thu Jan  5 2006 Tim Waugh <twaugh@redhat.com> 5.93-7
- Don't suppress chown/chgrp errors in install(1) (bug #176708).

* Mon Jan  2 2006 Dan Walsh <dwalsh@redhat.com> 5.93-6
- Remove pam_selinux.so from su.pamd, not needed for targeted and Strict/MLS 
  will have to newrole before using.

* Fri Dec 23 2005 Tim Waugh <twaugh@redhat.com> 5.93-5
- Fix "sort -n" (bug #176468).

* Fri Dec 16 2005 Tim Waugh <twaugh@redhat.com>
- Explicitly set default POSIX2 version during configure stage.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec  2 2005 Tim Waugh <twaugh@redhat.com>
- Parametrize SELinux (bug #174067).
- Fix runuser.pamd (bug #173807).

* Thu Nov 25 2005 Tim Waugh <twaugh@redhat.com> 5.93-4
- Rebuild to pick up new glibc *at functions.
- Apply runuser PAM patch from bug #173807.  Ship runuser PAM file.

* Tue Nov 14 2005 Dan Walsh <dwalsh@redhat.com> 5.93-3
- Remove multiple from su.pamd

* Mon Nov 14 2005 Tim Waugh <twaugh@redhat.com> 5.93-2
- Call setsid() in su under some circumstances (bug #173008).
- Prevent runuser operating when setuid (bug #173113).

* Tue Nov  8 2005 Tim Waugh <twaugh@redhat.com> 5.93-1
- 5.93.
- No longer need alt-md5sum-binary, dircolors, mkdir, mkdir2 or tac patches.

* Fri Oct 28 2005 Tim Waugh <twaugh@redhat.com> 5.92-1
- Finished porting i18n patch to sort.c.
- Fixed for sort-mb-tests (avoid +n syntax).

* Fri Oct 28 2005 Tim Waugh <twaugh@redhat.com> 5.92-0.2
- Fix chgrp basic test.
- Include md5sum patch from ALT.

* Mon Oct 24 2005 Tim Waugh <twaugh@redhat.com> 5.92-0.1
- 5.92.
- No longer need afs, dircolors, utmp, gcc4, brokentest, dateseconds,
  chown, rmaccess, copy, stale-utmp, no-sign-extend, fchown patches.
- Updated acl, dateman, pam, langinfo, i18n, getgrouplist, selinux patches.
- Dropped printf-ll, allow_old_options, jday, zh_CN patches.
- NOTE: i18n patch not ported for sort(1) yet.

* Fri Sep 30 2005 Tomas Mraz <tmraz@redhat.com> - 5.2.1-56
- use include instead of pam_stack in pam config

* Fri Sep 9 2005 Dan Walsh <dwalsh@redhat.com> 5.2.1-55
- Reverse change to use raw functions

* Thu Sep  8 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-54
- Explicit setuid bit for /bin/su in file manifest (bug #167745).

* Tue Sep 6 2005 Dan Walsh <dwalsh@redhat.com> 5.2.1-53
- Allow id to run even when SELinux security context can not be run
- Change chcon to use raw functions.

* Thu Jun 28 2005 Tim Waugh <twaugh@redhat.com>
- Corrected comments in DIR_COLORS.xterm (bug #161711).

* Wed Jun 22 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-52
- Fixed stale-utmp patch so that 'who -r' and 'who -b' work
  again (bug #161264).

* Fri Jun 17 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-51
- Use upstream hostid fix.

* Thu Jun 16 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-50
- Don't display the sign-extended part of the host id (bug #160078).

* Tue May 31 2005 Dan Walsh <dwalsh@redhat.com> 5.2.1-49
- Eliminate bogus "can not preserve context" message when moving files.

* Wed May 25 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-48
- Prevent buffer overflow in who(1) (bug #158405).

* Fri May 20 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-47
- Better error checking in the pam patch (bug #158189).

* Mon May 16 2005 Dan Walsh <dwalsh@redhat.com> 5.2.1-46
- Fix SELinux patch to better handle MLS integration

* Mon May 16 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-45
- Applied Russell Coker's selinux changes (bug #157856).

* Fri Apr  8 2005 Tim Waugh <twaugh@redhat.com>
- Fixed pam patch from Steve Grubb (bug #154946).
- Use better upstream patch for "stale utmp".

* Tue Mar 29 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-44
- Added "stale utmp" patch from upstream.

* Thu Mar 24 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-43
- Removed patch that adds -C option to install(1).

* Wed Mar 14 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-42
- Fixed pam patch.
- Fixed broken configure test.
- Fixed build with GCC 4 (bug #151045).

* Wed Feb  9 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-41
- Jakub Jelinek's sort -t multibyte fixes (bug #147567).

* Sat Feb  5 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-40
- Undo last change (bug #145266).

* Fri Feb  4 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-38
- Special case for ia32e in uname (bug #145266).

* Thu Jan 13 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-37
- Fixed zh_CN translation (bug #144845).  Patch from Mitrophan Chin.

* Mon Dec 28 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-36
- Fix to only setdefaultfilecon if not overridden by command line

* Mon Dec 27 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-35
- Change install to restorecon if it can

* Wed Dec 15 2004 Tim Waugh <twaugh@redhat.com>
- Fixed small bug in i18n patch.

* Mon Dec  6 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-34
- Don't set fs uid until after pam_open_session (bug #77791).

* Thu Nov 25 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-33
- Fixed colorls.csh (bug #139988).  Patch from Miloslav Trmac.

* Mon Nov  8 2004 Tim Waugh <twaugh@redhat.com>
- Updated URL (bug #138279).

* Mon Oct 25 2004 Steve Grubb <sgrubb@redhat.com> 5.2.1-32
- Handle the return code of function calls in runcon.

* Mon Oct 18 2004 Tim Waugh <twaugh@redhat.com>
- Prevent compiler warning in coreutils-i18n.patch (bug #136090).

* Tue Oct  5 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-31
- getgrouplist() patch from Ulrich Drepper.
- The selinux patch should be applied last.

* Mon Oct  4 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-30
- Mv runuser to /sbin

* Mon Oct  4 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-28
- Fix runuser man page.

* Mon Oct  4 2004 Tim Waugh <twaugh@redhat.com>
- Fixed build.

* Fri Sep 24 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-26
- Add runuser as similar to su, but only runable by root

* Fri Sep 24 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-25
- chown(1) patch from Ulrich Drepper.

* Tue Sep 14 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-24
- SELinux patch fix: don't display '(null)' if getfilecon() fails
  (bug #131196).

* Fri Aug 20 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-23
- Fixed colorls.csh quoting (bug #102412).
- Fixed another join LSB test failure (bug #121153).

* Mon Aug 16 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-22
- Fixed sort -t LSB test failure (bug #121154).
- Fixed join LSB test failure (bug #121153).

* Wed Aug 11 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-21
- Apply upstream patch to fix 'cp -a' onto multiply-linked files (bug #128874).
- SELinux patch fix: don't error out if lgetfilecon() returns ENODATA.

* Tue Aug 10 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-20
- Added 'konsole' TERM to DIR_COLORS (bug #129544).

* Wed Aug  4 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-19
- Added 'gnome' TERM to DIR_COLORS (bug #129112).
- Worked around a bash bug #129128.
- Fixed an i18n patch bug in cut (bug #129114).

* Tue Aug  3 2004 Tim Waugh <twaugh@redhat.com>
- Fixed colorls.{sh,csh} so that the l. and ll aliases are always defined
  (bug #128948).

* Tue Jul 13 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-18
- Fixed field extraction in sort (bug #127694).

* Fri Jun 25 2004 Tim Waugh <twaugh@redhat.com>
- Added 'TERM screen.linux' to DIR_COLORS (bug #78816).

* Wed Jun 23 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-17
- Move pam-xauth to after pam-selinux

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun  7 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-15
- Fix ls -Z (bug #125447).

* Fri Jun  4 2004 Tim Waugh <twaugh@redhat.com>
- Build requires bison (bug #125290).

* Fri Jun  4 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-14
- Fix selinux patch causing problems with ls --format=... (bug #125238).

* Thu Jun 3 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-13
- Change su to use pam_selinux open and pam_selinux close

* Wed Jun  2 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-12
- Don't call access() on symlinks about to be removed (bug #124699).

* Wed Jun  2 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-11
- Fix ja translation (bug #124862).

* Tue May 18 2004 Jeremy Katz <katzj@redhat.com> 5.2.1-10
- rebuild

* Mon May 17 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-9
- Mention pam in the info for su (bug #122592).
- Remove wheel group rant again (bug #122886).
- Change default behaviour for chgrp/chown (bug #123263).  Patch from
  upstream.

* Mon May 17 2004 Thomas Woerner <twoerner@redhat.com> 5.2.1-8
- compiling su PIE

* Wed May 12 2004 Tim Waugh <twaugh@redhat.com>
- Build requires new versions of autoconf and automake (bug #123098).

* Tue May  4 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-7
- Fix join -t (bug #122435).

* Tue Apr 20 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-6
- Fix 'ls -Z' displaying users/groups if stat() failed (bug #121292).

* Fri Apr 9 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-5
- Add ls -LZ fix
- Fix chcon to handle "."

* Wed Mar 17 2004 Tim Waugh <twaugh@redhat.com>
- Apply upstream fix for non-zero seconds for --date="10:00 +0100".

* Tue Mar 16 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-3
- If preserve fails, report as warning unless user requires preserve

* Tue Mar 16 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-2
- Make mv default to preserve on context

* Sat Mar 13 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-1
- 5.2.1.

* Fri Mar 12 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-9
- Add '-Z' to 'ls --help' output (bug #118108).

* Fri Mar  5 2004 Tim Waugh <twaugh@redhat.com>
- Fix deref-args test case for rebuilding under SELinux (bug #117556).

* Wed Feb 25 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-8
- kill(1) offloaded to util-linux altogether.

* Tue Feb 24 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-7
- Ship the real '[', not a symlink.

* Mon Feb 23 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-6
- Apply Paul Eggert's chown patch (bug #116536).
- Merged chdir patch into pam patch where it belongs.

* Mon Feb 23 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-5
- Fixed i18n patch bug causing sort -M not to work (bug #116575).

* Sat Feb 21 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-4
- Reinstate kill binary, just not its man page (bug #116463).

* Sat Feb 21 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-3
- Updated ls-stat patch.

* Fri Feb 20 2004 Dan Walsh <dwalsh@redhat.com> 5.2.0-2
- fix chcon to ignore . and .. directories for recursing

* Fri Feb 20 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-1
- Patch ls so that failed stat() is handled gracefully (Ulrich Drepper).
- 5.2.0.

* Thu Feb 19 2004 Tim Waugh <twaugh@redhat.com>
- More AFS patch tidying.

* Wed Feb 18 2004 Dan Walsh <dwalsh@redhat.com> 5.1.3-0.2
- fix chcon to handle -h qualifier properly, eliminate potential crash 

* Wed Feb 18 2004 Tim Waugh <twaugh@redhat.com>
- Stop 'sort -g' leaking memory (i18n patch bug #115620).
- Don't ship kill, since util-linux already does.
- Tidy AFS patch.

* Mon Feb 16 2004 Tim Waugh <twaugh@redhat.com> 5.1.3-0.1
- 5.1.3.
- Patches ported forward or removed.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 5.0-40
- rebuilt

* Tue Jan  20 2004 Dan Walsh <dwalsh@redhat.com> 5.0-39
- Change /etc/pam.d/su to remove preservuser and add multiple

* Tue Jan  20 2004 Dan Walsh <dwalsh@redhat.com> 5.0-38
- Change is_selinux_enabled to is_selinux_enabled > 0

* Tue Jan  20 2004 Dan Walsh <dwalsh@redhat.com> 5.0-37
- Add pam_selinux to pam file to allow switching of roles within selinux

* Fri Jan 16 2004 Tim Waugh <twaugh@redhat.com>
- The textutils-2.0.17-mem.patch is no longer needed.

* Thu Jan 15 2004 Tim Waugh <twaugh@redhat.com> 5.0-36
- Fixed autoconf test causing builds to fail.

* Tue Dec  9 2003 Dan Walsh <dwalsh@redhat.com> 5.0-35
- Fix copying to non xattr files

* Thu Dec  4 2003 Tim Waugh <twaugh@redhat.com> 5.0-34.sel
- Fix column widths problems in ls.

* Tue Dec  2 2003 Tim Waugh <twaugh@redhat.com> 5.0-33.sel
- Speed up md5sum by disabling speed-up asm.

* Wed Nov 19 2003 Dan Walsh <dwalsh@redhat.com> 5.0-32.sel
- Try again

* Wed Nov 19 2003 Dan Walsh <dwalsh@redhat.com> 5.0-31.sel
- Fix move on non SELinux kernels

* Fri Nov 14 2003 Tim Waugh <twaugh@redhat.com> 5.0-30.sel
- Fixed useless acl dependencies (bug #106141).

* Fri Oct 24 2003 Dan Walsh <dwalsh@redhat.com> 5.0-29.sel
- Fix id -Z

* Tue Oct 21 2003 Dan Walsh <dwalsh@redhat.com> 5.0-28.sel
- Turn on SELinux
- Fix chcon error handling

* Wed Oct 15 2003 Dan Walsh <dwalsh@redhat.com> 5.0-28
- Turn off SELinux

* Mon Oct 13 2003 Dan Walsh <dwalsh@redhat.com> 5.0-27.sel
- Turn on SELinux

* Mon Oct 13 2003 Dan Walsh <dwalsh@redhat.com> 5.0-27
- Turn off SELinux

* Mon Oct 13 2003 Dan Walsh <dwalsh@redhat.com> 5.0-26.sel
- Turn on SELinux

* Sun Oct 12 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- allow compiling without pam support

* Fri Oct 10 2003 Tim Waugh <twaugh@redhat.com> 5.0-23
- Make split(1) handle large files (bug #106700).

* Thu Oct  9 2003 Dan Walsh <dwalsh@redhat.com> 5.0-22
- Turn off SELinux

* Wed Oct  8 2003 Dan Walsh <dwalsh@redhat.com> 5.0-21.sel
- Cleanup SELinux patch

* Fri Oct  3 2003 Tim Waugh <twaugh@redhat.com> 5.0-20
- Restrict ACL support to only those programs needing it (bug #106141).
- Fix default PATH for LSB (bug #102567).

* Thu Sep 11 2003 Dan Walsh <dwalsh@redhat.com> 5.0-19
- Turn off SELinux

* Wed Sep 10 2003 Dan Walsh <dwalsh@redhat.com> 5.0-18.sel
- Turn on SELinux

* Fri Sep 5 2003 Dan Walsh <dwalsh@redhat.com> 5.0-17
- Turn off SELinux

* Tue Sep 2 2003 Dan Walsh <dwalsh@redhat.com> 5.0-16.sel
- Only call getfilecon if the user requested it.
- build with selinux

* Wed Aug 20 2003 Tim Waugh <twaugh@redhat.com> 5.0-14
- Documentation fix (bug #102697).

* Tue Aug 12 2003 Tim Waugh <twaugh@redhat.com> 5.0-13
- Made su use pam again (oops).
- Fixed another i18n bug causing sort --month-sort to fail.
- Don't run dubious stty test, since it fails when backgrounded
  (bug #102033).
- Re-enable make check.

* Fri Aug  8 2003 Tim Waugh <twaugh@redhat.com> 5.0-12
- Don't run 'make check' for this build (build environment problem).
- Another uninitialized variable in i18n (from bug #98683).

* Wed Aug 6 2003 Dan Walsh <dwalsh@redhat.com> 5.0-11
- Internationalize runcon
- Update latest chcon from NSA

* Wed Jul 30 2003 Tim Waugh <twaugh@redhat.com>
- Re-enable make check.

* Wed Jul 30 2003 Tim Waugh <twaugh@redhat.com> 5.0-9
- Don't run 'make check' for this build (build environment problem).

* Mon Jul 28 2003 Tim Waugh <twaugh@redhat.com> 5.0-8
- Actually use the ACL patch (bug #100519).

* Wed Jul 18 2003 Dan Walsh <dwalsh@redhat.com> 5.0-7
- Convert to SELinux

* Mon Jun  9 2003 Tim Waugh <twaugh@redhat.com>
- Removed samefile patch.  Now the test suite passes.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 28 2003 Tim Waugh <twaugh@redhat.com> 5.0-5
- Both kon and kterm support colours (bug #83701).
- Fix 'ls -l' alignment in zh_CN locale (bug #88346).

* Mon May 12 2003 Tim Waugh <twaugh@redhat.com> 5.0-4
- Prevent file descriptor leakage in du (bug #90563).
- Build requires recent texinfo (bug #90439).

* Wed Apr 30 2003 Tim Waugh <twaugh@redhat.com> 5.0-3
- Allow obsolete options unless POSIXLY_CORRECT is set.

* Sat Apr 12 2003 Tim Waugh <twaugh@redhat.com>
- Fold bug was introduced by i18n patch; fixed there instead.

* Fri Apr 11 2003 Matt Wilson <msw@redhat.com> 5.0-2
- fix segfault in fold (#88683)

* Sat Apr  5 2003 Tim Waugh <twaugh@redhat.com> 5.0-1
- 5.0.

* Mon Mar 24 2003 Tim Waugh <twaugh@redhat.com>
- Use _smp_mflags.

* Mon Mar 24 2003 Tim Waugh <twaugh@redhat.com> 4.5.11-2
- Remove overwrite patch.
- No longer seem to need nolibrt, errno patches.

* Thu Mar 20 2003 Tim Waugh <twaugh@redhat.com>
- No longer seem to need danglinglink, prompt, lug, touch_errno patches.

* Thu Mar 20 2003 Tim Waugh <twaugh@redhat.com> 4.5.11-1
- 4.5.11.
- Use packaged readlink.

* Wed Mar 19 2003 Tim Waugh <twaugh@redhat.com> 4.5.10-1
- 4.5.10.
- Update lug, touch_errno, acl, utmp, printf-ll, i18n, test-bugs patches.
- Drop fr_fix, LC_TIME, preserve, regex patches.

* Wed Mar 12 2003 Tim Waugh <twaugh@redhat.com> 4.5.3-21
- Fixed another i18n patch bug (bug #82032).

* Tue Mar 11 2003 Tim Waugh <twaugh@redhat.com> 4.5.3-20
- Fix sort(1) efficiency in multibyte encoding (bug #82032).

* Tue Feb 18 2003 Tim Waugh <twaugh@redhat.com> 4.5.3-19
- Ship readlink(1) (bug #84200).

* Thu Feb 13 2003 Tim Waugh <twaugh@redhat.com> 4.5.3-18
- Deal with glibc < 2.2 in %%pre scriplet (bug #84090).

* Wed Feb 12 2003 Tim Waugh <twaugh@redhat.com> 4.5.3-16
- Require glibc >= 2.2 (bug #84090).

* Tue Feb 11 2003 Bill Nottingham <notting@redhat.com> 4.5.3-15
- fix group (#84095)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 4.5.3-14
- rebuilt

* Thu Jan 16 2003 Tim Waugh <twaugh@redhat.com>
- Fix rm(1) man page.

* Thu Jan 16 2003 Tim Waugh <twaugh@redhat.com> 4.5.3-13
- Fix re_compile_pattern check.
- Fix su hang (bug #81653).

* Tue Jan 14 2003 Tim Waugh <twaugh@redhat.com> 4.5.3-11
- Fix memory size calculation.

* Tue Dec 17 2002 Tim Waugh <twaugh@redhat.com> 4.5.3-10
- Fix mv error message (bug #79809).

* Mon Dec 16 2002 Tim Powers <timp@redhat.com> 4.5.3-9
- added PreReq on grep

* Fri Dec 13 2002 Tim Waugh <twaugh@redhat.com>
- Fix cp --preserve with multiple arguments.

* Thu Dec 12 2002 Tim Waugh <twaugh@redhat.com> 4.5.3-8
- Turn on colorls for screen (bug #78816).

* Mon Dec  9 2002 Tim Waugh <twaugh@redhat.com> 4.5.3-7
- Fix mv (bug #79283).
- Add patch27 (nogetline).

* Sun Dec  1 2002 Tim Powers <timp@redhat.com> 4.5.3-6
- use the su.pamd from sh-utils since it works properly with multilib systems

* Fri Nov 29 2002 Tim Waugh <twaugh@redhat.com> 4.5.3-5
- Fix test suite quoting problems.

* Fri Nov 29 2002 Tim Waugh <twaugh@redhat.com> 4.5.3-4
- Fix scriplets.
- Fix i18n patch so it doesn't break uniq.
- Fix several other patches to either make the test suite pass or
  not run the relevant tests.
- Run 'make check'.
- Fix file list.

* Thu Nov 28 2002 Tim Waugh <twaugh@redhat.com> 4.5.3-3
- Adapted for Red Hat Linux.
- Self-host for help2man.
- Don't ship readlink just yet (maybe later).
- Merge patches from fileutils and sh-utils (textutils ones are already
  merged it seems).
- Keep the binaries where the used to be (in particular, id and stat).

* Sun Nov 17 2002 Stew Benedict <sbenedict@mandrakesoft.com> 4.5.3-2mdk
- LI18NUX/LSB compliance (patch800)
- Installed (but unpackaged) file(s) - /usr/share/info/dir

* Thu Oct 31 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.3-1mdk
- new release
- rediff patch 180
- merge patch 150 into 180

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-6mdk
- move su back to /bin

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-5mdk
- patch 0 : lg locale is illegal and must be renamed lug (pablo)

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-4mdk
- fix conflict with procps

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-3mdk
- patch 105 : fix install -s

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-2mdk
- fix build
- don't chmode two times su
- build with large file support
- fix description
- various spec cleanups
- fix chroot installation
- fix missing /bin/env
- add old fileutils, sh-utils & textutils ChangeLogs

* Fri Oct 11 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-1mdk
- initial release (merge fileutils, sh-utils & textutils)
- obsoletes/provides: sh-utils/fileutils/textutils
- fileutils stuff go in 1xx range
- sh-utils stuff go in 7xx range
- textutils stuff go in 5xx range
- drop obsoletes patches 1, 2, 10 (somes files're gone but we didn't ship
  most of them)
- rediff patches 103, 105, 111, 113, 180, 706
- temporary disable patch 3 & 4
- fix fileutils url

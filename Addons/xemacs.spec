# TODO: review desktop entry associations (does text/* work?)
# TODO: zero-length /usr/share/xemacs-21.5-b26/lisp/dump-paths.el
# TODO: non-ASCII in buffer tabs

%bcond_with     gtk
%bcond_with     wnn
%bcond_with     xaw3d
%bcond_with     xfs
%bcond_without  mule
%bcond_without  nox
%bcond_without  xim
%ifarch ia64
# no-expdyn-ia64 patch, https://bugzilla.redhat.com/show_bug.cgi?id=106744#c39
%bcond_with     modules
%else
%bcond_without  modules
%endif

#global snap    20090311hg4626
%global majver  21.5

Name:           xemacs
Version:        21.5.29
Release:        15%{?snap:.%{snap}}%{?dist}.2
Summary:        Different version of Emacs

Group:          Applications/Editors
License:        GPLv2+
URL:            http://www.xemacs.org/
%if 0%{?snap:1}
Source0:        %{name}-%{snap}.tar.xz
%else
Source0:        http://ftp.xemacs.org/xemacs-%{majver}/xemacs-%{version}.tar.gz
%endif
Source1:        %{name}.png
Source2:        xemacs.desktop
Source3:        dotxemacs-init.el
Source4:        default.el
Source5:        xemacs-sitestart.el

Patch0:         %{name}-21.5.26-utf8-fonts.patch
Patch1:         %{name}-21.5.25-x-paths.patch
# Applied upstream 2009-07-01
Patch2:         %{name}-21.5.29-image-overflow.patch
Patch3:         %{name}-21.5.25-mk-nochk-features.patch
Patch4:         %{name}-21.5.27-no-expdyn-ia64-106744.patch
Patch5:         %{name}-21.5.25-wnnfix-128362.patch
# Proposed by upstream 2009-08-25
Patch6:         %{name}-21.5.29-no-xft.patch
# Applied upstream 2009-09-23
Patch7:         %{name}-21.5.29-png.patch
Patch8:         %{name}-21.5.28-courier-default.patch
Patch9:         %{name}-21.5.29-destdir.patch
# Sent upstream 2009-10-28
Patch10:        %{name}-21.5.29-tty-font-512623.patch
# Sent upstream 2009-12-08
Patch11:        %{name}-21.5.29-etags-memmove-545399.patch
# Applied upstream 2009-12-21
Patch12:        %{name}-21.5.29-arabic-547840.patch
# Applied upstream 2009-01-07
Patch13:        %{name}-21.5.29-dired-550145.patch
# Sent upstream 2009-03-12
Patch14:        %{name}-beta-infodir.patch
Patch15:        %{name}-21.5.29-x-server.patch

BuildRequires:  autoconf
BuildRequires:  sed >= 3.95
BuildRequires:  texinfo
BuildRequires:  ncurses-devel
BuildRequires:  gpm-devel
BuildRequires:  pam-devel
BuildRequires:  zlib-devel
BuildRequires:  libjpeg-devel
BuildRequires:  compface-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  desktop-file-utils
%if %{with mule}
BuildRequires:  Canna-devel
%if %{with wnn}
BuildRequires:  FreeWnn-devel
%endif # wnn
%endif # mule
BuildRequires:  xmkmf
BuildRequires:  libXau-devel
BuildRequires:  libXpm-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  db4-devel
BuildRequires:  gmp-devel
%if %{with gtk}
BuildRequires:  gtk+-devel
BuildRequires:  libglade-devel
%else  # gtk
BuildRequires:  xorg-x11-xbitmaps
%if %{with xaw3d}
BuildRequires:  Xaw3d-devel
%else  # xaw3d
BuildRequires:  neXtaw-devel
%endif # xaw3d
%endif # gtk
BuildRequires:  libXft-devel
# Note: no xemacs-packages-extra dependency here, need main pkg to build it.
Requires:       xemacs-packages-base >= 20060510
Requires:       %{name}-common = %{version}-%{release}
Requires:       xorg-x11-fonts-ISO8859-1-75dpi
Requires:       xorg-x11-fonts-ISO8859-1-100dpi
Requires:       xorg-x11-fonts-misc
Requires(post): coreutils
Provides:       xemacs(bin) = %{version}-%{release}

%global xver    %(echo %{version} | sed -e 's/\\.\\([0-9]\\+\\)$/-b\\1/')
%global xbuild  %(echo %{_build} | sed -e 's/^\\([^-]*-[^-]*-[^-]*\\).*/\\1/')

%description
XEmacs is a highly customizable open source text editor and
application development system.  It is protected under the GNU General
Public License and related to other versions of Emacs, in particular
GNU Emacs.  Its emphasis is on modern graphical user interface support
and an open software development model, similar to Linux.

This package contains XEmacs built for X Windows%{?with_mule: with MULE support}.

%package        common
Summary:        Byte-compiled lisp files and other common files for XEmacs
Group:          Applications/Editors
Requires:       xemacs(bin) = %{version}-%{release}
Requires(post): %{_sbindir}/alternatives
Requires(preun): %{_sbindir}/alternatives

%description    common
XEmacs is a highly customizable open source text editor and
application development system.  It is protected under the GNU General
Public License and related to other versions of Emacs, in particular
GNU Emacs.  Its emphasis is on modern graphical user interface support
and an open software development model, similar to Linux.

This package contains byte-compiled lisp and other common files for XEmacs.

%package        nox
Summary:        Different version of Emacs built without X Windows support
Group:          Applications/Editors
# Note: no xemacs-packages* dependencies here, we need -nox to build the
# base package set.
Requires:       %{name}-common = %{version}-%{release}
Requires(post): coreutils
Provides:       xemacs(bin) = %{version}-%{release}

%description    nox
XEmacs is a highly customizable open source text editor and
application development system.  It is protected under the GNU General
Public License and related to other versions of Emacs, in particular
GNU Emacs.  Its emphasis is on modern graphical user interface support
and an open software development model, similar to Linux.

This package contains XEmacs built without X Windows support.

%package        xft
Summary:        Different version of Emacs built with Xft/fontconfig support
Group:          Applications/Editors
Requires:       %{name}-common = %{version}-%{release}
Requires:       xemacs-packages-base >= 20060510
Requires(post): coreutils
Provides:       xemacs(bin) = %{version}-%{release}

%description    xft
XEmacs is a highly customizable open source text editor and
application development system.  It is protected under the GNU General
Public License and related to other versions of Emacs, in particular
GNU Emacs.  Its emphasis is on modern graphical user interface support
and an open software development model, similar to Linux.

This package contains XEmacs built with Xft and fontconfig support.

%package        el
Summary:        Emacs lisp source files for XEmacs
Group:          Development/Libraries
Requires:       %{name}-common = %{version}-%{release}

%description    el
XEmacs is a highly customizable open source text editor and
application development system.  It is protected under the GNU General
Public License and related to other versions of Emacs, in particular
GNU Emacs.  Its emphasis is on modern graphical user interface support
and an open software development model, similar to Linux.

This package contains the lisp source files for XEmacs, mainly of
interest when developing or debugging XEmacs itself.

%package        info
Summary:        XEmacs documentation in GNU texinfo format
Group:          Documentation
%if 0%{?fedora} >= 10
BuildArch:      noarch
%endif
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description    info
XEmacs is a highly customizable open source text editor and
application development system.  It is protected under the GNU General
Public License and related to other versions of Emacs, in particular
GNU Emacs.  Its emphasis is on modern graphical user interface support
and an open software development model, similar to Linux.

This package contains XEmacs documentation in GNU texinfo format.

%package        devel
Summary:        Development files for XEmacs
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
XEmacs is a highly customizable open source text editor and
application development system.  It is protected under the GNU General
Public License and related to other versions of Emacs, in particular
GNU Emacs.  Its emphasis is on modern graphical user interface support
and an open software development model, similar to Linux.

This package contains XEmacs development support files.


%prep
%setup -q -n %{name}-%{?snap:beta}%{!?snap:%{version}}
find . -type f -name "*.elc" -o -name "*.info*" | xargs rm -f
rm -f configure.in
sed -i -e /tetris/d lisp/menubar-items.el
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%ifarch ia64
touch -r aclocal.m4 aclocal.m4-stamp
%patch4 -p1
touch -r aclocal.m4-stamp aclocal.m4
%endif
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1

sed -i -e 's/"lib"/"%{_lib}"/' lisp/setup-paths.el

autoconf --force # for DESTDIR patch

for f in man/lispref/mule.texi man/xemacs-faq.texi CHANGES-beta ; do
    iconv -f iso-8859-1 -t utf-8 -o $f.utf8 $f ; mv $f.utf8 $f
done


%build
CFLAGS="${CFLAGS:-$RPM_OPT_FLAGS -fno-strict-aliasing}"
%if %{with gtk}
CFLAGS="$CFLAGS $(pkg-config libglade --cflags)"
%endif
export CFLAGS
export EMACSLOADPATH=$PWD/lisp:$PWD/lisp/mule

# The --with-*dir args can probably go away in the future if/when upstream
# configure learns to honor standard autofoo dirs better.
common_options="
    --mandir=%{_mandir}/man1
    --with-archlibdir=%{_libdir}/xemacs-%{xver}/%{xbuild}
%if %{with modules}
    --with-moduledir=%{_libdir}/xemacs-%{xver}/%{xbuild}/modules
%endif
    --with-lispdir=%{_datadir}/xemacs-%{xver}/lisp
    --with-etcdir=%{_datadir}/xemacs-%{xver}/etc
    --with-system-packages=%{_datadir}/xemacs
    --without-msw
%if %{with mule}
    --with-mule
%endif
    --with-clash-detection
    --with-database=berkdb
    --without-ldap
    --without-postgresql
    --with-mail-locking=lockf
    --with-pop
    --without-hesiod
%ifarch alpha ia64 ppc64
    --with-system-malloc
%endif
    --with-pdump
%if ! %{with modules}
    --without-modules
%endif
    --with-debug
    --with-error-checking=none
    --enable-bignum=gmp
"

%if %{with nox}
# build without X
%configure $common_options \
    --with-docdir=%{_libdir}/xemacs-%{xver}/doc-nox \
    --with-sound=none \
    --with-xim=no \
    --without-canna \
    --without-wnn \
    --without-x
make EMACSDEBUGPATHS=yes # toplevel parallel make fails
mv lib-src/DOC{,-nox}
mv src/xemacs{,-nox-%{xver}}
mv lib-src/config.values{,-nox}
mv Installation{,-nox}
# grab these from -nox, the X ones may have deps on ALSA, X, etc
for file in {e,oo}tags gnuserv {fake,move}mail yow ; do
    mv lib-src/$file{,-mindep}
done
%endif # nox

# build with Xft
%configure $common_options \
    --with-docdir=%{_libdir}/xemacs-%{xver}/doc-xft \
    --with-sound=nonative,alsa \
    --with-xft=all \
%if %{with gtk}
    --with-gtk \
    --with-gnome \
%else
    --with-athena=%{?with_xaw3d:3d}%{!?with_xaw3d:next} \
    --with-menubars=lucid \
    --with-widgets=athena \
    --with-dialogs=athena \
    --with-scrollbars=lucid \
    --with-xim=%{?with_xim:xlib}%{!?with_xim:no} \
%endif
%if ! %{with wnn}
    --without-wnn
%endif
make EMACSDEBUGPATHS=yes # toplevel parallel make fails
mv lib-src/DOC{,-xft}
mv src/xemacs{,-xft-%{xver}}
mv lib-src/config.values{,-xft}
mv Installation{,-xft}

# build with X
%configure $common_options \
    --with-docdir=%{_libdir}/xemacs-%{xver}/doc \
    --with-sound=nonative,alsa \
%if %{with xft}
    --with-xft=all \
%else
%if %{with xfs}
    --with-xfs \
%endif
%endif
%if %{with gtk}
    --with-gtk \
    --with-gnome \
%else
    --with-athena=%{?with_xaw3d:3d}%{!?with_xaw3d:next} \
    --with-menubars=lucid \
    --with-widgets=athena \
    --with-dialogs=athena \
    --with-scrollbars=lucid \
    --with-xim=%{?with_xim:xlib}%{!?with_xim:no} \
%endif
%if ! %{with wnn}
    --without-wnn
%endif

make EMACSDEBUGPATHS=yes # toplevel parallel make fails

cat << \EOF > xemacs.pc
prefix=%{_prefix}
%if %{with modules}
includedir=%{_libdir}/xemacs-%{xver}/%{xbuild}/include
sitemoduledir=%{_libdir}/xemacs/site-modules
%endif
sitestartdir=%{_datadir}/xemacs/site-packages/lisp/site-start.d
sitepkglispdir=%{_datadir}/xemacs/site-packages/lisp

Name: xemacs
Description: Different version of Emacs
Version: %{version}
%if %{with modules}
Cflags: -I${includedir}
%endif
EOF

cat > macros.xemacs << EOF
%%_xemacs_version %{majver}
%%_xemacs_ev %{?epoch:%{epoch}:}%{version}
%%_xemacs_evr %{?epoch:%{epoch}:}%{version}-%{release}
%%_xemacs_sitepkgdir %{_datadir}/xemacs/site-packages
%%_xemacs_sitelispdir %{_datadir}/xemacs/site-packages/lisp
%%_xemacs_sitestartdir %{_datadir}/xemacs/site-packages/lisp/site-start.d
%%_xemacs_bytecompile /usr/bin/xemacs -q -no-site-file -batch -f batch-byte-compile
%if %{with modules}
%%_xemacs_includedir %{_libdir}/xemacs-%{xver}/%{xbuild}/include
%%_xemacs_sitemoduledir %{_libdir}/xemacs/site-modules
%endif
EOF

%install
rm -rf $RPM_BUILD_ROOT

%if %{with nox}
# restore binaries with less dependencies; note: no -p nor move
for file in lib-src/*-mindep ; do cp $file ${file%%-mindep} ; done
%endif

make install DESTDIR=$RPM_BUILD_ROOT

%if %{with nox}
# install nox files
echo ".so man1/xemacs.1" > $RPM_BUILD_ROOT%{_mandir}/man1/xemacs-nox.1
install -pm 755 src/xemacs-nox-%{xver} $RPM_BUILD_ROOT%{_bindir}
ln -s xemacs-nox-%{xver} $RPM_BUILD_ROOT%{_bindir}/xemacs-nox
install -dm 755 $RPM_BUILD_ROOT%{_libdir}/xemacs-%{xver}/doc-nox
install -pm 644 lib-src/DOC-nox \
    $RPM_BUILD_ROOT%{_libdir}/xemacs-%{xver}/doc-nox/DOC
install -pm 644 lib-src/config.values-nox \
    $RPM_BUILD_ROOT%{_libdir}/xemacs-%{xver}/doc-nox/config.values
%endif # nox

# install xft files
echo ".so man1/xemacs.1" > $RPM_BUILD_ROOT%{_mandir}/man1/xemacs-xft.1
install -pm 755 src/xemacs-xft-%{xver} $RPM_BUILD_ROOT%{_bindir}
ln -s xemacs-xft-%{xver} $RPM_BUILD_ROOT%{_bindir}/xemacs-xft
install -dm 755 $RPM_BUILD_ROOT%{_libdir}/xemacs-%{xver}/doc-xft
install -pm 644 lib-src/DOC-xft \
    $RPM_BUILD_ROOT%{_libdir}/xemacs-%{xver}/doc-xft/DOC
install -pm 644 lib-src/config.values-xft \
    $RPM_BUILD_ROOT%{_libdir}/xemacs-%{xver}/doc-xft/config.values

# these clash with GNU Emacs
mv $RPM_BUILD_ROOT%{_bindir}/etags{,.xemacs}
rm -f $RPM_BUILD_ROOT%{_bindir}/{ctags,rcs-checkin,b2m}
mv $RPM_BUILD_ROOT%{_mandir}/man1/etags{,.xemacs}.1
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/ctags.1

# these clash with other packages
rm -f $RPM_BUILD_ROOT%{_infodir}/info*
rm -f $RPM_BUILD_ROOT%{_infodir}/standards*
rm -f $RPM_BUILD_ROOT%{_infodir}/termcap*
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

desktop-file-install --vendor=fedora --mode=644 \
    --dir=$RPM_BUILD_ROOT%{_datadir}/applications \
    %{SOURCE2}

# site-start.el
install -dm 755 \
    $RPM_BUILD_ROOT%{_datadir}/xemacs/site-packages/lisp/site-start.d
install -pm 644 %{SOURCE5} \
    $RPM_BUILD_ROOT%{_datadir}/xemacs/site-packages/lisp/site-start.el

# default.el
install -pm 644 %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}/xemacs/site-packages/lisp

# default user init file
install -Dpm 644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/skel/.xemacs/init.el

# icon
install -Dpm 644 %{SOURCE1} \
    $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/xemacs.png

# macro file
install -Dpm 644 macros.xemacs $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.xemacs

# Empty directories for external packages to use
mkdir -m 0755 $RPM_BUILD_ROOT%{_datadir}/xemacs/site-packages/etc
mkdir -m 0755 $RPM_BUILD_ROOT%{_datadir}/xemacs/site-packages/info
mkdir -m 0755 $RPM_BUILD_ROOT%{_datadir}/xemacs/site-packages/lib-src
mkdir -m 0755 $RPM_BUILD_ROOT%{_datadir}/xemacs/site-packages/man
mkdir -m 0755 $RPM_BUILD_ROOT%{_datadir}/xemacs/site-packages/pkginfo

# make sure nothing is 0400
chmod -R a+rX $RPM_BUILD_ROOT%{_prefix}
chmod a+x $RPM_BUILD_ROOT%{_datadir}/xemacs-%{xver}%{_sysconfdir}/xemacs-fe.sh

# clean up unneeded stuff (TODO: there's probably much more)
find $RPM_BUILD_ROOT%{_prefix} -name "*~" | xargs -r rm
rm $RPM_BUILD_ROOT%{_libdir}/xemacs-%{xver}/%{xbuild}/gzip-el.sh
rm $RPM_BUILD_ROOT{%{_bindir}/gnuattach,%{_mandir}/man1/gnuattach.1}
cd $RPM_BUILD_ROOT%{_datadir}/xemacs-%{xver}/etc
rm -r editclient.sh InstallGuide sparcworks tests XKeysymDB *.sco *.1
cd -

# separate files
rm -f *.files base-files el-files info-files
echo "%%defattr(-,root,root,-)" > base-files
echo "%%defattr(-,root,root,-)" > el-files
echo "%%defattr(-,root,root,-)" > info-files

find $RPM_BUILD_ROOT{%{_datadir}/xemacs-%{xver},%{_datadir}/xemacs} \
  \( -type f -not -name '*.el' -fprint base-non-el.files \) -o \
  \( -type d -name info -fprint info.files -prune \) -o \
  \( -type d -fprintf dir.files "%%%%dir %%p\n" \) -o \
  \( -name '*.el' \( -exec test -e '{}'c \; -fprint el-bytecomped.files -o \
     -fprint base-el-not-bytecomped.files \) \)
sed -i -e "s|$RPM_BUILD_ROOT||" *.files

# make site-packages lisp files config files
sed -i -e 's|^\(.*/site-packages/lisp/.*\)$|%%config(noreplace) \1|' \
  base-el-not-bytecomped.files

# combine the file lists
cat base-*.files dir.files >> base-files
cat el-*.files >> el-files
cat info.files >> info-files

install -Dpm 644 xemacs.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig/xemacs.pc


%clean
rm -rf $RPM_BUILD_ROOT


%post
# rm because alternatives won't overwrite pre-alternatives symlink, bug?
rm -f %{_bindir}/xemacs && \
%{_sbindir}/alternatives --install %{_bindir}/xemacs xemacs \
    %{_bindir}/xemacs-%{xver} 80
touch --no-create %{_datadir}/icons/hicolor &>/dev/null
:

%postun
[ -e %{_bindir}/xemacs-%{xver} ] || \
%{_sbindir}/alternatives --remove xemacs %{_bindir}/xemacs-%{xver}
if [ $1 -eq 0 ] ; then
    update-desktop-database %{_datadir}/applications &>/dev/null
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null
fi
:

%posttrans
update-desktop-database %{_datadir}/applications &>/dev/null
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%post nox
# rm because alternatives won't overwrite pre-alternatives symlink, bug?
rm -f %{_bindir}/xemacs && \
%{_sbindir}/alternatives --install %{_bindir}/xemacs xemacs \
    %{_bindir}/xemacs-nox-%{xver} 40 || :

%postun nox
[ -e %{_bindir}/xemacs-nox-%{xver} ] || \
%{_sbindir}/alternatives --remove xemacs %{_bindir}/xemacs-nox-%{xver} || :

%post xft
# rm because alternatives won't overwrite pre-alternatives symlink, bug?
rm -f %{_bindir}/xemacs && \
%{_sbindir}/alternatives --install %{_bindir}/xemacs xemacs \
    %{_bindir}/xemacs-xft-%{xver} 40 || :

%postun xft
[ -e %{_bindir}/xemacs-xft-%{xver} ] || \
%{_sbindir}/alternatives --remove xemacs %{_bindir}/xemacs-xft-%{xver} || :

%post common
%{_sbindir}/alternatives --install %{_bindir}/etags etags \
    %{_bindir}/etags.xemacs 40 || :

%preun common
[ $1 -ne 0 ] || \
%{_sbindir}/alternatives --remove etags %{_bindir}/etags.xemacs || :

%post info
for file in xemacs cl internals lispref new-users-guide ; do
    /sbin/install-info %{_infodir}/$file.info %{_infodir}/dir
done
:

%preun info
if [ $1 -eq 0 ] ; then
    for file in xemacs cl internals lispref new-users-guide ; do
        /sbin/install-info --delete %{_infodir}/$file.info %{_infodir}/dir
    done
fi
:


%files
%defattr(-,root,root,-)
%doc Installation
# gnuclient needs X libs, so not in -common
%{_bindir}/gnuclient
%{_bindir}/gnudoit
%ghost %{_bindir}/xemacs
%{_bindir}/xemacs-%{xver}
%{_libdir}/xemacs-%{xver}/doc/
%if %{with modules}
%if %{with mule}
%{_libdir}/xemacs-%{xver}/%{xbuild}/modules/canna_api.ell
%endif
%endif
%{_datadir}/applications/*-%{name}.desktop
%{_datadir}/icons/hicolor/48x48/apps/xemacs.png
%{_mandir}/man1/gnuclient.1*
%{_mandir}/man1/gnudoit.1*

%if %{with nox}
%files nox
%defattr(-,root,root,-)
%doc Installation-nox
%ghost %{_bindir}/xemacs
%{_bindir}/xemacs-nox
%{_bindir}/xemacs-nox-%{xver}
%{_libdir}/xemacs-%{xver}/doc-nox/
%{_mandir}/man1/xemacs-nox.1*
%endif

%files xft
%defattr(-,root,root,-)
%doc Installation-xft
%ghost %{_bindir}/xemacs
%{_bindir}/xemacs-xft
%{_bindir}/xemacs-xft-%{xver}
%{_libdir}/xemacs-%{xver}/doc-xft/
%{_mandir}/man1/xemacs-xft.1*

%files common -f base-files
%defattr(-,root,root,-)
%doc INSTALL README COPYING PROBLEMS CHANGES-beta etc/NEWS etc/TUTORIAL
%doc etc/editclient.sh
%{_bindir}/etags.xemacs
%{_bindir}/ootags
%{_bindir}/xemacs-script
%dir %{_libdir}/xemacs-%{xver}/
%dir %{_libdir}/xemacs-%{xver}/%{xbuild}/
%{_libdir}/xemacs-%{xver}/%{xbuild}/[acdfghprsvwy]*
%{_libdir}/xemacs-%{xver}/%{xbuild}/m[am]*
%{_libdir}/xemacs-%{xver}/%{xbuild}/movemail
%if %{with modules}
%{_libdir}/xemacs/
%dir %{_libdir}/xemacs-%{xver}/%{xbuild}/modules/
%{_libdir}/xemacs-%{xver}/%{xbuild}/modules/auto-autoloads.elc
%endif
%config(noreplace) %{_sysconfdir}/rpm/macros.xemacs
%config(noreplace) %{_sysconfdir}/skel/.xemacs/
%{_mandir}/man1/etags.xemacs.1*
%{_mandir}/man1/gnuserv.1*
%{_mandir}/man1/xemacs.1*

%files el -f el-files
%defattr(-,root,root,-)
%if %{with modules}
%{_libdir}/xemacs-%{xver}/%{xbuild}/modules/auto-autoloads.el
%endif

%files info -f info-files
%defattr(-,root,root,-)
%doc COPYING
%{_infodir}/*.info*

%files devel
%defattr(-,root,root,-)
%if %{with modules}
%{_bindir}/ellcc
%{_libdir}/xemacs-%{xver}/%{xbuild}/include/
%endif
%{_libdir}/pkgconfig/xemacs.pc


%changelog
* Fri Dec  3 2010 Steve Traylen <steve.traylen@cern.ch> - 21.5.29-15 2
- Correct previous wrong date on last change log entry.

* Wed Dec  3 2010 Steve Traylen <steve.traylen@cern.ch> - 21.5.29-15 1
- Merge Fedora 15 .spec file to EPEL6.

* Wed Dec  1 2010 Jerry James <loganjerry@gmail.com> - 21.5.29-15
- Don't create /var/lock/xemacs; it is not used (bz 656723).
- Drop the BuildRoot tag.
- Ship COPYING with the -info subpackage.

* Wed Nov 10 2010 Jerry James <loganjerry@gmail.com> - 21.5.29-14
- Create and own subdirectories of site-packages

* Tue Jul  6 2010 Jerry James <loganjerry@gmail.com> - 21.5.29-13
- Add db4 support (bz 581614).
- Add -xft subpackage (bz 356961).
- Recognize Fedora's X server.

* Tue Mar  2 2010 Jerry James <loganjerry@gmail.com> - 21.5.29-12
- Remove the bitmap-fonts dependency.

* Thu Jan  7 2010 Jerry James <loganjerry@gmail.com> - 21.5.29-11
- New upstream patch for bz 547840.
- Add dired patch for large files (bz 550145).
- Replace "lzma" with "xz" for snapshots.

* Mon Dec 21 2009 Jerry James <loganjerry@gmail.com> - 21.5.29-10
- Don't crash with a Persian keyboard layout (bz 547840)

* Tue Dec  8 2009 Jerry James <loganjerry@gmail.com> - 21.5.29-9
- Add patch to use memmove in etags (bz 545399).

* Mon Nov  9 2009 Jerry James <loganjerry@gmail.com> - 21.5.29-8
- Move macros.xemacs to the -common subpackage (bz 533611).
- Updated TTY font patch from upstream.

* Tue Nov  3 2009 Jerry James <loganjerry@gmail.com> - 21.5.29-7
- Make the desktop file consistent with Emacs (bz 532296).

* Wed Oct 28 2009 Jerry James <loganjerry@gmail.com> - 21.5.29-6
- Bring back the courier font patch; that was a red herring.
- Really, seriously fix bz 512623 with a TTY font patch.
- Fix the version number in macros.xemacs.
- Build with bignum support.
- Turn off OSS support.

* Wed Sep 23 2009 Jerry James <loganjerry@gmail.com> - 21.5.29-5
- Final fix for bz 512623, which is actually two bugs, because ...
- ... the courier font patch breaks TTY font detection.  Removed that patch
  and Require bitmap-fonts to supply the original font name.
- Add macros.xemacs (bz 480546)
- Add png patch to fix a problem with reading PNG files

* Wed Aug 26 2009 Jerry James <loganjerry@gmail.com> - 21.5.29-4
- Use upstream's attempt at fixing #512623 instead of mine, which didn't work.

* Mon Aug 24 2009 Jerry James <loganjerry@gmail.com> - 21.5.29-3
- Fix image overflow bug (CVE-2009-2688).
- Fix calling xft-font-create-object in non-Xft builds (#512623).
- Rebase patches to eliminate fuzz/offsets.

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 21.5.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 20 2009 Ville Skyttä <ville.skytta at iki.fi> - 21.5.29-1
- Update to 21.5.29; gtk-gcc4, finder-lisp-dir, 3d-athena, autoconf262,
  doc-encodings, revert-modified, and xemacs-base-autoloads patches applied
  upstream.

* Thu Mar 12 2009 Ville Skyttä <ville.skytta at iki.fi> - 21.5.28-13
- Add possibility to build upstream hg snapshots.
- Add dependency on xorg-x11-fonts-misc (#478370, Carl Brune).
- Include Installation{,-nox} in docs.

* Sun Mar  8 2009 Ville Skyttä <ville.skytta at iki.fi> - 21.5.28-12
- Make XFontSet support optional at build time and disable it by default
  to work around #478370.

* Thu Feb 26 2009 Ville Skyttä <ville.skytta at iki.fi> - 21.5.28-11
- Apply upstream autoload changes to be able to build recent XEmacs packages.
- Make support for XIM optional at build time, still enabled by default.
- Drop support for building without stack protector compiler flags.
- Make -info subpackage noarch when built for Fedora >= 10.
- Improve icon cache and desktop database refresh scriptlets.
- Use %%global instead of %%define.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 21.5.28-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jul 20 2008 Ville Skyttä <ville.skytta at iki.fi> - 21.5.28-9
- Rebuild.

* Sun Jul  6 2008 Ville Skyttä <ville.skytta at iki.fi> - 21.5.28-8
- Apply upstream fix for detection of 3D Athena widget sets.

* Sun Jul  6 2008 Ville Skyttä <ville.skytta at iki.fi> - 21.5.28-7
- Fix build with autoconf >= 2.62 (#449626).

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 21.5.28-6
- Autorebuild for GCC 4.3

* Fri Aug 17 2007 Ville Skyttä <ville.skytta at iki.fi> - 21.5.28-5
- Turn on syntax highlighting by default only if lazy-lock is available.
- Requires(post): coreutils in main package and -nox.
- Scriptlet cleanups.
- License: GPLv2+

* Sat Jun 30 2007 Ville Skyttä <ville.skytta at iki.fi> - 21.5.28-4
- Turn on syntax highlighting with lazy-lock by default.
- Drop Application and X-Fedora categories and Encoding from desktop entry.
- Move diff-switches default from skeleton init.el to site-start.el.

* Sun Jun 24 2007 Ville Skyttä <ville.skytta at iki.fi> - 21.5.28-3
- Apply upstream fix for #245017.

* Wed Jun  6 2007 Ville Skyttä <ville.skytta at iki.fi> - 21.5.28-2
- Set more dirs explicitly until upstream configure honors them better.
- Borrow DESTDIR install patch from openSUSE.
- Add pkgconfig file to -devel.

* Mon May 21 2007 Ville Skyttä <ville.skytta at iki.fi> - 21.5.28-1
- 21.5.28, module path fix applied upstream.
- Patch to retain courier as the default font.
- Fix some corrupt characters in docs.

* Fri May 18 2007 Ville Skyttä <ville.skytta at iki.fi> - 21.5.27-9
- Require one of the actual editor variants in -common.
- Require -common in -el, drop duplicate dir ownerships.

* Wed Jan 24 2007 Ville Skyttä <ville.skytta at iki.fi> - 21.5.27-8
- Fix canna_api.ell install/load paths (#222559).
- Fix site-start.el locale setup when the LANG env var is unset.

* Thu Jan  4 2007 Ville Skyttä <ville.skytta at iki.fi> - 21.5.27-7
- Don't run autoconf during build.

* Wed Jan  3 2007 Ville Skyttä <ville.skytta at iki.fi> - 21.5.27-6
- Fix site-start.el coding system setup in non-UTF8 locales (#213582).
- Fix "--without modules" build.

* Mon Oct  2 2006 Ville Skyttä <ville.skytta at iki.fi> - 21.5.27-5
- Rebuild.

* Wed Sep 20 2006 Ville Skyttä <ville.skytta at iki.fi> - 21.5.27-4
- Disable graphical progress bar by default (#188973).
- Make Wnn support optional at build time, disabled by default.

* Sun Sep 10 2006 Ville Skyttä <ville.skytta at iki.fi> - 21.5.27-3
- Adjust to split xemacs-packages-{base,extra}.
- Provide xemacs(bin) in main package and -nox.

* Sat Sep  2 2006 Ville Skyttä <ville.skytta at iki.fi> - 21.5.27-2
- Fix build when previous revision of the same XEmacs version is installed.
- BuildRequire compface-devel instead of compface.
- Turn error checking off.
- Specfile cleanups.

* Tue May 16 2006 Ville Skyttä <ville.skytta at iki.fi> - 21.5.27-1
- 21.5.27, maximize patch included upstream.
- Drop no longer needed find-paths patch.
- Fix alternatives setup.

* Sun May  7 2006 Ville Skyttä <ville.skytta at iki.fi> - 21.5.26-5
- Apply upstream fix for window maximization problems (#111225).

* Sun Apr 23 2006 Ville Skyttä <ville.skytta at iki.fi> - 21.5.26-4
- Bring StartupWMClass in desktop entry up to date.
- Fix non-MULE build.

* Sat Apr 15 2006 Ville Skyttä <ville.skytta at iki.fi> - 21.5.26-3
- Don't expect to find ellcc if building without modules (#188929).
- New --with/--without rpmbuild flags:
  - xft: enable/disable Xft support, default disabled.
  - nox: enable/disable building the non-X version, default enabled
  - modules: enable/disable module support, default arch-dependent.
- Re-enable XFontSet support for menubars for non-Xft builds (from openSUSE).
- Move gnuserv to -common, gnudoit to base package, drop gnuattach.
- Split ellcc and headers to -devel subpackage.
- Drop unneeded libXaw-devel build dependency.
- Move -nox "man page" to -nox subpackage.
- Fix GTK build and glade detection for it.
- Avoid -common dependency on ALSA.

* Thu Apr  6 2006 Ville Skyttä <ville.skytta at iki.fi> - 21.5.26-2
- Borrow Mike Fabian's site-start.el work from the SuSE package.

* Tue Apr  4 2006 Ville Skyttä <ville.skytta at iki.fi> - 21.5.26-1
- 21.5.26 (WIP).
- Make %%{_bindir}/xemacs an alternative (main/nox).
- Convert some info docs to UTF-8.

* Fri Mar 31 2006 Ville Skyttä <ville.skytta at iki.fi> - 21.5.25-1
- 21.5.25 (WIP).
- Trim pre-21.5 %%changelog entries.

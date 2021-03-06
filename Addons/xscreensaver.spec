%define name          xscreensaver

%define mainversion   5.12
%define beta_ver      %{nil}

%define fedora 12

%define modular_conf  1
%define fedora_rel    7

%undefine extrarel

%if 0%{?fedora} >= 12
%define default_text  %{_datadir}/doc/HTML/readme/en_US/README-en_US.txt
%else
%define default_text  %{_datadir}/doc/HTML/README-Accessibility
%endif
%define default_URL   http://planet.fedoraproject.org/rss20.xml

%define pam_ver       0.80-7
%define autoconf_ver  2.53

%define update_po     1
%define build_tests   0

Buildroot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Summary:         X screen saver and locker
Name:            %{name}
Version:         %{mainversion}
Release:         %{fedora_rel}%{?dist}%{?extrarel}
Epoch:           1
License:         MIT
Group:           Amusements/Graphics
URL:             http://www.jwz.org/xscreensaver/
Source0:         http://www.jwz.org/xscreensaver/xscreensaver-%{mainversion}%{?beta_ver}.tar.gz
%if %{modular_conf}
Source10:        update-xscreensaver-hacks
%endif
%if 0%{?fedora} >= 12
Source11:        xscreensaver-autostart
Source12:        xscreensaver-autostart.desktop
%endif
##
## Patches
##
# bug 129335
# sanitize the names of modes in barcode
Patch1:          xscreensaver-5.00b5-sanitize-hacks.patch
# Change webcollage not to access to net
# Also see bug 472061
Patch21:         xscreensaver-5.11-webcollage-default-nonet.patch
#
## Patches already sent to the upsteam
# Remove "AC_PROG_CC' was expanded before it was required" warning
Patch30:         xscreensaver-5.11-conf264.patch
#
## Patches which must be discussed with upstream
# For now set LANG to C for daemon because some garbage character appears
# on passwd prompt
Patch31:         xscreensaver-5.12-for-now-set-lang-on-daemon-to-C.patch
#
# Patch32, 33, 34, 35, 36: already sent to the upstream
#
# Kill memleak on gltext (bug 638600)
Patch32:         xscreensaver-5.12-gltext-memleak.patch
# Remove duplicate xml files entry
Patch33:         xscreensaver-5.12-xml-duplicate-list.patch
# Fix the issue that flame is completely blank (bug 642651)
Patch34:         xscreensaver-5.12-flame-completely-blank.patch
# Remove Gtk-warning
# "GtkSpinButton: setting an adjustment with non-zero page size is deprecated"
Patch35:         xscreensaver-5.12-gtkspinbox-page-size-to-zero.patch
# Warn (not say "Error") about missing image directory, and warn
# only once (bug 648304)
Patch36:         xscreensaver-5.12-warn-only-once-with-missing-image-dir.patch
# Patches end
Requires:        xscreensaver-base = %{epoch}:%{version}-%{release}
Requires:        xscreensaver-extras = %{epoch}:%{version}-%{release}
Requires:        xscreensaver-gl-extras = %{epoch}:%{version}-%{release}

%package base
Summary:         A minimal installation of xscreensaver
Group:           Amusements/Graphics
BuildRequires:   autoconf
BuildRequires:   bc
BuildRequires:   desktop-file-utils
BuildRequires:   gawk
BuildRequires:   gettext
BuildRequires:   libtool
BuildRequires:   pam-devel > %{pam_ver}
BuildRequires:   sed
# Use pseudo symlink
# BuildRequires:   xdg-utils
BuildRequires:   xorg-x11-proto-devel
# extrusioni
%if 0%{?fedora} >= 13
BuildRequires:   libgle-devel
%endif
BuildRequires:   libX11-devel
BuildRequires:   libXScrnSaver-devel
BuildRequires:   libXext-devel
# From xscreensaver 5.12, write explicitly
BuildRequires:   libXi-devel
BuildRequires:   libXinerama-devel
BuildRequires:   libXmu-devel
BuildRequires:   libXpm-devel
# Write explicitly
BuildRequires:   libXrandr-devel
BuildRequires:   libXt-devel
BuildRequires:   libXxf86misc-devel
BuildRequires:   libXxf86vm-devel
BuildRequires:   gtk2-devel	
BuildRequires:   libjpeg-devel
BuildRequires:   libglade2-devel
# For --with-login-manager option
%if 0%{?fedora} >= 14
# Use pseudo symlink, not writing BR: gdm
#BuildRequires:   gdm
%endif
Requires:        %{_sysconfdir}/pam.d/system-auth
Requires:        pam > %{pam_ver}
Requires:        xdg-utils
Requires:        xorg-x11-resutils
Requires:        xorg-x11-fonts-ISO8859-1-100dpi
%if 0%{?build_tests} < 1
# Obsoletes but not Provides
Obsoletes:       xscreeensaver-tests < %{epoch}:%{version}-%{release}
%endif

%package extras
Summary:         An enhanced set of screensavers
Group:           Amusements/Graphics
BuildRequires:   desktop-backgrounds-basic
Requires:        %{name}-base = %{epoch}:%{version}-%{release}

%package gl-base
Summary:         A base package for screensavers that require OpenGL
Group:           Amusements/Graphics
Requires:        %{name}-base = %{epoch}:%{version}-%{release}

%package gl-extras
Summary:         An enhanced set of screensavers that require OpenGL
Group:           Amusements/Graphics
Provides:        xscreensaver-gl = %{epoch}:%{version}-%{release}
Obsoletes:       xscreensaver-gl <= 1:5.00
BuildRequires:   libGL-devel
BuildRequires:   libGLU-devel
%if %{modular_conf}
Requires:        %{name}-gl-base = %{epoch}:%{version}-%{release}
%else
Requires:        %{name}-base = %{epoch}:%{version}-%{release}
%endif

%package extras-gss
Summary:         Desktop files of extras for gnome-screensaver
Group:           Amusements/Graphics
Requires:        %{name}-extras = %{epoch}:%{version}-%{release}
Requires:        gnome-screensaver

%package gl-extras-gss
Summary:         Desktop files of gl-extras for gnome-screensaver
Group:           Amusements/Graphics
Requires:        %{name}-gl-extras = %{epoch}:%{version}-%{release}
Requires:        gnome-screensaver

%package tests
Summary:         Test programs related to XScreenSaver
Group:           Development/Debuggers
Requires:        %{name}-base = %{epoch}:%{version}-%{release}


%description
A modular screen saver and locker for the X Window System.
More than 200 display modes are included in this package.

This is a metapackage for installing all default packages
related to XScreenSaver.

%description -l fr
Un économiseur d'écran modulaire pour le système X Window.
Plus de 200 modes d'affichages sont inclus dans ce paquet.

This is a metapackage for installing all default packages
related to XScreenSaver.

%description base
A modular screen saver and locker for the X Window System.
This package contains the bare minimum needed to blank and
lock your screen.  The graphical display modes are the
"xscreensaver-extras" and "xscreensaver-gl-extras" packages.

%description -l fr base 
Un économiseur d'écran modulaire pour le système X Window.
Ce paquet contient le minimum vital pour éteindre et verouiller
votre écran. Les modes d'affichages graphiques sont inclus
dans les paquets "xscreensaver-extras" et "xscreensaver-gl-extras".

%description extras
A modular screen saver and locker for the X Window System.
This package contains a variety of graphical screen savers for
your mind-numbing, ambition-eroding, time-wasting, hypnotized
viewing pleasure.

%description -l fr extras
Un économiseur d'écran modulaire pour le système X Window.
Ce paquet contient une pléthore d'économiseurs d'écran graphiques
pour votre plaisir des yeux.

%description gl-base
A modular screen saver and locker for the X Window System.
This package contains minimal files to make screensaver hacks
that require OpenGL work for XScreenSaver.

%description gl-extras
A modular screen saver and locker for the X Window System.
This package contains a variety of OpenGL-based (3D) screen
savers for your mind-numbing, ambition-eroding, time-wasting,
hypnotized viewing pleasure.

%description -l fr gl-extras
Un économiseur d'écran modulaire pour le système X Window.
Ce paquet contient une pléthore d'économiseurs d'écran basés sur OpenGL (3D)
pour votre plaisir des yeux.

%description extras-gss
This package contains desktop files of extras screensavers
for gnome-screensaver compatibility.

%description gl-extras-gss
This package contains desktop files of gl-extras screensavers
for gnome-screensaver compatibility.

%description tests
This package contains some test programs to debug XScreenSaver.


%prep
%setup -q -n %{name}-%{mainversion}%{?beta_ver}

%patch1 -p1 -b .sanitize-hacks
%patch21 -p1 -b .nonet
%patch30 -p1 -b .conf264
%patch31 -p1 -b .langc
%patch32 -p1 -b .gltext_mem
%patch33 -p1 -b .xmllist
%patch34 -p1 -b .flame_blank
%patch35 -p1 -b .spin_warn
%patch36 -p1 -b .warn_once

change_option(){
   set +x
   ADFILE=$1
   if [ ! -f ${ADFILE}.opts ] ; then
      cp -p $ADFILE ${ADFILE}.opts
   fi
   shift

   for ARG in "$@" ; do
      TYPE=`echo $ARG | sed -e 's|=.*$||'`
      VALUE=`echo $ARG | sed -e 's|^.*=||'`

      eval sed -i \
         -e \'s\|\^\\\(\\\*$TYPE\:\[ \\t\]\[ \\t\]\*\\\)\[\^ \\t\]\.\*\$\|\\1$VALUE\|\' \
         $ADFILE
   done
   set -x
}

silence_hack(){
   set +x
   ADFILE=$1
   if [ ! -f ${ADFILE}.hack ] ; then
      cp -p $ADFILE ${ADFILE}.hack
   fi
   shift

   for hack in "$@" ; do
      eval sed -i \
         -e \'\/\^\[ \\t\]\[ \\t\]\*$hack\/s\|\^\|-\|g\' \
         -e \'s\|\^@GL_\.\*@.*\\\(GL\:\[ \\t\]\[ \\t\]\*$hack\\\)\|-\\t\\1\|g\' \
         $ADFILE
   done
   set -x
}

# change some files to UTF-8
for f in \
   driver/XScreenSaver.ad.in \
   hacks/glx/sproingies.man \
   ; do
   iconv -f ISO-8859-1 -t UTF-8 $f > $f.tmp || cp -p $f $f.tmp
   touch -r $f $f.tmp
   mv $f.tmp $f
done

# Change some options
# For grabDesktopImages, lock, see bug 126809
change_option driver/XScreenSaver.ad.in \
   captureStderr=False \
   passwdTimeout=0:00:15 \
   grabDesktopImages=False \
   lock=True \
   splash=False \
   ignoreUninstalledPrograms=True \
   textProgram=fortune\ -s \
%if 0%{?fedora} >= 12
   textURL=%{default_URL}
%endif

# Disable the following hacks by default
# (disable, not remove)
silence_hack driver/XScreenSaver.ad.in \
   bsod flag

# Record time, EVR
eval sed -i.ver \
   -e \'s\|version \[45\]\.\[0-9a-z\]\[0-9a-z\]\*\|version %{version}-`echo \
      %{release} | sed -e '/IGNORE THIS/s|\.[a-z][a-z0-9].*$||'`\|\' \
      driver/XScreenSaver.ad.in

eval sed -i.date \
   -e \'s\|\[0-9\].\*-.\*-20\[0-9\]\[0-9\]\|`LANG=C date -u +'%%d-%%b-%%Y'`\|g\' \
   driver/XScreenSaver.ad.in

eval sed -i.ver \
   -e \'s\|\(\[0-9\].\*-.\*-20\[0-9\]\[0-9\]\)\|\(`LANG=C \
      date -u +'%%d-%%b-%%Y'`\)\|g\' \
   -e \'s\|\\\(5.\[0-9\]\[0-9\]\\\)[a-z]\[0-9\]\[0-9\]\*\|\\\1\|\' \
   -e \'s\|5.\[0-9\]\[0-9\]\|%{version}-`echo %{release} | \
      sed -e '/IGNORE THIS/s|\.[a-zA-Z][a-zA-Z0-9].*$||'`\|\' \
   utils/version.h

# Move man entry to 6x (bug 197741)
for f in `find hacks -name Makefile.in` ; do
   sed -i.mansuf \
      -e '/^mansuffix/s|6|6x|'\
      $f
done

# Search first 6x entry, next 1 entry for man pages
sed -i.manentry -e 's@man %%s@man 6x %%s 2>/dev/null || man 1 %%s @' \
   driver/XScreenSaver.ad.in

# Suppress rpmlint warnings.
# suppress about pam config (although this is 
# not the fault of xscreensaver.pam ......).
sed -i.rpmlint -n -e '1,5p' driver/xscreensaver.pam 

if [ -x %{_datadir}/libtool/config.guess ]; then
  # use system-wide copy
   cp -p %{_datadir}/libtool/config.{sub,guess} .
fi

# Fix for desktop-file-utils 0.14+
%if 0%{?fedora} >= 9
sed -i.icon -e 's|xscreensaver\.xpm|xscreensaver|' \
   driver/screensaver-properties.desktop.in
%endif

# Disable (don't build) some tests
# apm: doesn't compile
# passwd: causes segv
# mlstring: causes OOM
sed -i.test \
   -e 's|test-apm[ \t][ \t]*t|t|' \
   -e 's|test-passwd[ \t][ \t]*t|t|' \
   -e 's|test-mlstring[ \t][ \t]*t|t|' \
   driver/Makefile.in
sed -i.dir -e '/TEST_FADE_OBJS =/s|UTILS_SRC|UTILS_BIN|' driver/Makefile.in

# test-fade: give more time between fading
sed -i.delay -e 's| delay = 1| delay = 3|' driver/test-fade.c
# test-grab: testing time too long, setting time 15 min -> 20 sec
sed -i.delay -e 's|60 \* 15|20|' driver/test-grab.c

autoconf
autoheader

%build

archdir=`./config.guess`
[ -d $archdir ] || mkdir $archdir
cd $archdir

# Create temporary path and symlink
rm -rf ./TMPBINDIR

mkdir TMPBINDIR
pushd TMPBINDIR/
export PATH=$(pwd):$PATH

# xdg-open
ln -sf /bin/true xdg-open
popd

export CFLAGS="${CFLAGS:-${RPM_OPT_FLAGS}}"

CONFIG_OPTS="--prefix=%{_prefix} --with-pam --without-shadow --without-kerberos"
CONFIG_OPTS="$CONFIG_OPTS --without-setuid-hacks"
CONFIG_OPTS="$CONFIG_OPTS --with-text-file=%{default_text}"
CONFIG_OPTS="$CONFIG_OPTS --with-x-app-defaults=%{_datadir}/X11/app-defaults"
CONFIG_OPTS="$CONFIG_OPTS --disable-root-passwd"
CONFIG_OPTS="$CONFIG_OPTS --with-browser=xdg-open"
# From xscreensaver 5.12, login-manager option is on by default
# For now, let's enable it on F-14 and above
%if 0%{?fedora} >= 14
pushd TMPBINDIR
ln -sf /bin/true gdmflexiserver
export PATH=$(pwd):$PATH
popd
%else
CONFIG_OPTS="$CONFIG_OPTS --without-login-manager"
%endif
# Enable extrusion on F-13 and above
%if 0%{?fedora} <= 12
CONFIG_OPTS="$CONFIG_OPTS --without-gle"
%endif

# This is flaky:
# CONFIG_OPTS="$CONFIG_OPTS --with-login-manager"

unlink configure || :
ln -s ../configure .
%configure $CONFIG_OPTS
rm -f configure

%if %{update_po}
( cd po ; make generate_potfiles_in update-po )
%endif

make %{?_smp_mflags} -k \
	GMSGFMT="msgfmt --statistics"

%if %{modular_conf}
# Make XScreenSavar.ad modular (bug 200881)
CONFD=xscreensaver
rm -rf $CONFD
mkdir $CONFD

# Preserve the original adfile
cp -p driver/XScreenSaver.ad $CONFD

# First split XScreenSaver.ad into 3 parts
cat driver/XScreenSaver.ad | \
   sed -n -e '1,/\*programs/p' > $CONFD/XScreenSaver.ad.header
cat driver/XScreenSaver.ad | sed -e '1,/\*programs/d' | \
   sed -n -e '1,/\\n$/p' > $CONFD/XScreenSaver.ad.hacks
cat driver/XScreenSaver.ad | sed -e '1,/\\n$/d' > $CONFD/XScreenSaver.ad.tail

# Seperate XScreenSaver.ad.hacks into each hacks
cd $CONFD
mkdir hacks.conf.d ; cp -p XScreenSaver.ad.hacks hacks.conf.d/xscreensaver.conf
cd ..

%endif

# test
%if %{build_tests}
make tests -C driver
%endif

%install
archdir=`./config.guess`
cd $archdir

rm -rf ${RPM_BUILD_ROOT}

# We have to make sure these directories exist,
# or nothing will be installed into them.
#
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pam.d

make install_prefix=$RPM_BUILD_ROOT INSTALL="install -c -p" install

# Kill OnlyShowIn=GNOME; on F-11+ (bug 483495)
desktop-file-install --vendor "" --delete-original    \
   --dir $RPM_BUILD_ROOT%{_datadir}/applications         \
%if 0%{?fedora} < 11
   --add-only-show-in GNOME                              \
%endif
   --add-category    DesktopSettings                     \
%if 0
   --add-category X-Red-Hat-Base                         \
%else
   --remove-category Appearance                          \
   --remove-category AdvancedSettings                    \
   --remove-category Application                         \
%endif
   $RPM_BUILD_ROOT%{_datadir}/applications/*.desktop

# This function prints a list of things that get installed.
# It does this by parsing the output of a dummy run of "make install".
list_files() {
   echo "%%defattr(-,root,root,-)"
   make -s install_prefix=${RPM_BUILD_ROOT} INSTALL=true "$@"  \
      | sed -n -e 's@.* \(/[^ ]*\)$@\1@p'                      \
      | sed    -e "s@^${RPM_BUILD_ROOT}@@"                     \
               -e "s@/[a-z][a-z]*/\.\./@/@"                    \
      | sed    -e 's@\(.*/man/.*\)@%%doc \1\*@'                      \
               -e 's@\(.*/pam\.d/\)@%%config(noreplace) \1@'    \
      | sort  \
      | uniq
}

# Generate three lists of files for the three packages.
#
dd=%{_builddir}/%{name}-%{mainversion}%{?beta_ver}

# In case rpm -bi --short-circuit is tried multiple times:
rm -f $dd/*.files

(  cd hacks     ; list_files install ) >  $dd/extras.files
(  cd hacks/glx ; list_files install ) >  $dd/gl-extras.files
(  cd driver    ; list_files install ) >  $dd/base.files

# Move %%{_bindir}/xscreensaver-gl-helper to gl-base
# (bug 336331).
%if %{modular_conf}
echo "%%defattr(-,root,root,-)" >> $dd/gl-base.files

sed -i -e '/xscreensaver-gl-helper/d' $dd/gl-extras.files
pushd $RPM_BUILD_ROOT
for dir in `find . -name \*xscreensaver-gl-helper\*` ; do
   echo "${dir#.}" >> $dd/gl-base.files
done
popd
sed -i -e 's|^\(%{_mandir}.*\)$|\1*|' $dd/gl-base.files
%endif

%if %{modular_conf}
# Install update script
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
install -cpm 755 %{SOURCE10} $RPM_BUILD_ROOT%{_sbindir}
echo "%{_sbindir}/update-xscreensaver-hacks" >> $dd/base.files

# Make hack conf modular
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xscreensaver
mkdir -p $RPM_BUILD_ROOT%{_datadir}/xscreensaver/hacks.conf.d
cp -p xscreensaver/XScreenSaver.ad* \
   $RPM_BUILD_ROOT%{_sysconfdir}/xscreensaver
cp -p xscreensaver/hacks.conf.d/xscreensaver.conf \
   $RPM_BUILD_ROOT%{_datadir}/xscreensaver/hacks.conf.d/

for adfile in xscreensaver/XScreenSaver.ad.* ; do
   filen=`basename $adfile`
   echo "%%config(noreplace) %{_sysconfdir}/xscreensaver/$filen" >> $dd/base.files
done
echo -n "%%verify(not size md5 mtime) " >> $dd/base.files
echo "%{_sysconfdir}/xscreensaver/XScreenSaver.ad" >> \
   $dd/base.files
echo "%{_datadir}/xscreensaver/hacks.conf.d/xscreensaver.conf" \
   >> $dd/base.files

# Check symlink
rm -f $RPM_BUILD_ROOT%{_datadir}/X11/app-defaults/XScreenSaver

pushd $RPM_BUILD_ROOT%{_datadir}/X11/app-defaults
pushd ../../../..
if [ ! $(pwd) == $RPM_BUILD_ROOT ] ; then
   echo "Possibly symlink broken"
   exit 1
fi
popd
popd

ln -sf ../../../..%{_sysconfdir}/xscreensaver/XScreenSaver.ad \
   $RPM_BUILD_ROOT%{_datadir}/X11/app-defaults/XScreenSaver

%endif

# Add documents
pushd $dd &> /dev/null
for f in README* ; do
   echo "%%doc $f" >> $dd/base.files
done
popd

# Add directory
pushd $RPM_BUILD_ROOT
for dir in `find . -type d | grep xscreensaver` ; do
   echo "%%dir ${dir#.}" >> $dd/base.files
done
popd

%find_lang %{name}
cat %{name}.lang | uniq >> $dd/base.files

# Suppress rpmlint warnings
# sanitize path in script file
for f in ${RPM_BUILD_ROOT}%{_bindir}/xscreensaver-getimage-* \
   ${RPM_BUILD_ROOT}%{_libexecdir}/xscreensaver/vidwhacker \
   ${RPM_BUILD_ROOT}%{_bindir}/xscreensaver-text ; do
   if [ -f $f ] ; then
      sed -i -e 's|%{_prefix}//bin|%{_bindir}|g' $f
   fi
done

# tests
%if %{build_tests}
echo "%%defattr(-,root,root,-)" > $dd/tests.files
cd driver
for tests in `find . -name test-\* -perm -0700` ; do
   install -cpm 0755 $tests ${RPM_BUILD_ROOT}%{_libexecdir}/xscreensaver
   echo "%{_libexecdir}/xscreensaver/$tests" >> $dd/tests.files
done
cd ..
%endif

# Install desktop application autostart stuff
# Add OnlyShowIn=GNOME (bug 517391)
%if 0%{?fedora} >= 12
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/xdg/autostart
install -cpm 0755 %{SOURCE11} ${RPM_BUILD_ROOT}%{_libexecdir}/
desktop-file-install \
   --vendor "" \
   --dir ${RPM_BUILD_ROOT}%{_sysconfdir}/xdg/autostart \
   --add-only-show-in=GNOME \
   %{SOURCE12}
chmod 0644 ${RPM_BUILD_ROOT}%{_sysconfdir}/xdg/autostart/xscreensaver*.desktop

echo "%{_libexecdir}/xscreensaver-autostart" >> $dd/base.files
echo '%{_sysconfdir}/xdg/autostart/xscreensaver*.desktop' >> $dd/base.files
%endif

# Create desktop entry for gnome-screensaver
# bug 204944, 208560
create_desktop(){
   COMMAND=`cat $1 | sed -n -e 's|^<screen.*name=\"\([^ ][^ ]*\)\".*$|\1|p'`
# COMMAND must be full path (see bug 531151)
# Check if the command actually exists
   COMMAND=%{_libexecdir}/xscreensaver/$COMMAND
   if [ ! -x $RPM_BUILD_ROOT/$COMMAND ] ; then
      echo
      echo "WARNING:"
      echo "$COMMAND could not be found under $RPM_BUILD_ROOT"
      #exit 1
   fi
   NAME=`cat $1 | sed -n -e 's|^<screen.*_label=\"\(.*\)\">.*$|\1|p'`
   ARG=`cat $1 | sed -n -e 's|^.*<command arg=\"\([^ ][^ ]*\)\".*$|\1|p'`
   ARG=$(echo "$ARG" | while read line ; do echo -n "$line " ; done)
   COMMENT="`cat $1 | sed -e '1,/_description/d' | \
     sed -e '/_description/q' | sed -e '/_description/d'`"
   COMMENT=$(echo "$COMMENT" | while read line ; do echo -n "$line " ; done)

# webcollage treatment
## changed to create wrapper script
%if 0
   if [ "x$COMMAND" = "xwebcollage" ] ; then
      ARG="$ARG -directory %{_datadir}/backgrounds/images"
   fi
%endif

   if [ "x$NAME" = "x" ] ; then NAME=$COMMAND ; fi

   rm -f $2
   echo "[Desktop Entry]" >> $2
#   echo "Encoding=UTF-8" >> $2
   echo "Name=$NAME" >> $2
   echo "Comment=$COMMENT" >> $2
   echo "TryExec=$COMMAND" >> $2
   echo "Exec=$COMMAND $ARG" >> $2
   echo "StartupNotify=false" >> $2
   echo "Type=Application" >> $2
   echo "Categories=GNOME;Screensaver;" >> $2
}

cd $dd

SAVERDIR=%{_datadir}/applications/screensavers
mkdir -p ${RPM_BUILD_ROOT}${SAVERDIR}
echo "%%dir $SAVERDIR" >> base.files

for list in *extras.files ; do

   glist=gnome-$list
   rm -f $glist

   echo "%%defattr(-,root,root,-)" > $glist
##  move the owner of $SAVERDIR to -base
##   echo "%%dir $SAVERDIR" >> $glist

   set +x
   for xml in `cat $list | grep xml$` ; do
      file=${RPM_BUILD_ROOT}${xml}
      desktop=xscreensaver-`basename $file`
      desktop=${desktop%.xml}.desktop

      echo + create_desktop $file  ${RPM_BUILD_ROOT}${SAVERDIR}/$desktop
      create_desktop $file  ${RPM_BUILD_ROOT}${SAVERDIR}/$desktop
      echo ${SAVERDIR}/$desktop >> $glist
   done
   set -x
done

# Create wrapper script for webcollage to use nonet option
# by default, and rename the original webcollage
# (see bug 472061)
pushd ${RPM_BUILD_ROOT}%{_libexecdir}/%{name}
mv -f webcollage webcollage.original

cat > webcollage <<EOF
#!/bin/sh
PATH=%{_libexecdir}/%{name}:\$PATH
exec webcollage.original \\
	-directory %{_datadir}/backgrounds/images \\
	"\$@"
EOF
chmod 0755 webcollage
echo "%%{_libexecdir}/%%{name}/webcollage.original" >> \
	$dd/extras.files

# Make sure all files are readable by all, and writable only by owner.
#
chmod -R a+r,u+w,og-w ${RPM_BUILD_ROOT}

%clean
rm -rf ${RPM_BUILD_ROOT}

%if %{modular_conf}
%post base
%{_sbindir}/update-xscreensaver-hacks
exit 0
%endif

%files
%defattr(-,root,root,-)

%files -f base.files base
%defattr(-,root,root,-)

%if %{build_tests}
%files -f tests.files tests
%defattr(-,root,root,-)
%endif

%files -f extras.files extras
%defattr(-,root,root,-)

%if %{modular_conf}
%files -f gl-base.files gl-base
%defattr(-,root,root,-)
%endif

%files -f gl-extras.files gl-extras
%defattr(-,root,root,-)

%files -f gnome-extras.files extras-gss
%defattr(-,root,root,-)

%files -f gnome-gl-extras.files gl-extras-gss
%defattr(-,root,root,-)

%changelog
* Thu Nov 11 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.12-7
- Warn (not say "Error") about missing image directory, and warn
  only once (bug 648304)

* Thu Oct 28 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.12-6
- Remove GTK warning about non-zero page-size on GtkSpinButton

* Wed Oct 13 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.12-5
- Fix the issue that flame is completely blank (bug 642651)

* Wed Oct 13 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.12-4
- Enable libgle dependent hacks on F-13+

* Wed Oct 13 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.12-3
- Kill memleak on gltext (bug 638600)

* Sun Oct 10 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- F-14+: rebuild against fixed gcc

* Mon Sep 20 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.12-2
- Update Patch 31 (xscreensaver-5.12-for-now-set-lang-on-daemon-to-C.patch)
- Reduce BR using pseudo symlink

* Fri Sep 17 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.12-1
- Update to 5.12

* Mon Aug  9 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.11-9.respin1
- Fix sinc() (in ripple.c) argument when window is small
  (may fix bug 622188)

* Sun Jul 25 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.11-8.1.respin1
- And more fix for the below patch

* Sun Jul 25 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.11-8.respin1
- Fix xscreensaver-5.11-xjack-with-small-window.patch (bug 617905)

* Thu Jul  8 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.11-7.respin1
- Fix codes which contain undefined behavior, detected by gcc45

* Mon Jun 28 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.11-6.respin1
- Replace Patch32 (xscreensaver-5.11-xjack-with-small-window.patch) with the one
  revised by the upstream

* Thu Jun 24 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.11-5.respin1
- Make hacks' names in gss compat desktop files written in full path
  (ref: bug 531151)
- Update gss compat desktop creation

* Mon Jun 14 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.11-4.1.respin1
- Fix crash of xjack when window is too small (bug 603587)

* Sat Jun  5 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.11-3.respin1
- Upstream seems to have released new 5.11 tarball
  containing po/ directory, use that tarball
  (detected by Kevin's source audit)

* Sat May  1 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.11-2
- Fix crash when not using "pair" mode and when MappingNotify
  or so is received (bug 587537)

* Mon Apr 12 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.11-1
- Update to 5.11
- All patches sent to the upstream now applied in the tarball
- 2 new patches, one for autoconf, one for po
- Preserve 5.10 tarball for now for translation

* Sat Feb 27 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- F-12: rebuild with newer gcc

* Fri Feb  5 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.10-6.1
- A bit more memleak fix

* Fri Feb  5 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.10-6
- Fix memleak on analogtv based hacks, especially on apple2

* Wed Feb  3 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.10-5
- Fix crash on noseguy when X resource is no longer available (bug 560614)

* Fri Dec 11 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.10-4
- Fix occasional crash on substrate (bug 545847)
- Fix initialization process on apple2, hopefully fix bug 540790??

* Thu Oct  8 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.10-2
- F-12+: Restrict Autostart effect to GNOME session only (bug 517391)
- F-12+: Use planet.fedoraproject.org for textURL (still the default textMode
  is "file", i.e. no net connection)

* Tue Sep  8 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.10-1
- Update to 5.10
- All non Fedora-specific patches applied upstream

* Thu Sep  3 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.09-1
- Update to 5.09
- Drop patches applied by upstream (1 patch still pending on upstream
  + 2 Fedora specific patches left)
- Add one patch to generate missing header files
- Suppress compilation warnings with -std=c89

* Fri Aug 28 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.08-13
- Another case of hack's crash when window size is too small
  (Ubuntu bug 418419)

* Thu Jul 30 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.08-12
- Install desktop application autostart stuff on F-12+

* Sat Jul 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.08-11
- Build fix for new xextproto (libXext 1.0.99.3)
- Fix for breaking strict aliasing rule
- Again change %%default_text

* Thu Jun 11 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.08-10
- Fix crash on startup when randr reports no rroi->ncrtc
  (bug 504912), patch from gentoo

* Tue Feb 24 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.08-9
- F-11: Mass rebuild

* Sun Feb 15 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.08-8
- Fix the difference of creation of desktop files for gss between
  different archs (detected by Florian Festi)

* Mon Feb  2 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.08-7
- Remove OnlyShowIn=GNOME on F-11+ (to make happy with XFCE):
  bug 483495
- Add more comments about bug reference

* Thu Jan 22 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.08-5
- Fix phosphor segv when changing window size (bug 481146)

* Tue Dec 30 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.08-4
- Fix the process of "make update-po -C po", reported by jwz

* Sun Dec 28 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.08-1
- Update to 5.08
- All non Fedora-specific patches went upstream
- Preserve all %%release string for XScreenSaver.ad, util.h

* Sat Dec 27 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.07-5
- Apply gdk trial patch from jwz (slightly modified)
- Fix warning on m6502.c

* Fri Nov 28 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.07-4
- Fix fireworkx segfault (bug 473355)

* Wed Nov 19 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.07-3
- Create wrapper script for webcollage to use nonet option
  by default, and rename the original webcollage (bug 472061)

* Fri Sep 12 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.07-2
- Update ja.po
- Fix the explanation in XScreenSaver.ad (bug 461415)

* Thu Aug 21 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.07-1
- Update to 5.07
- Fix the license tag: BSD -> MIT

* Sat Aug  9 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.06-3
- Fallback to Xinerama extension when Xrandr reports less screens
  than Xinerama
  (bug 457685: patch by jwz and Aaron Plattner <aplattner@nvidia.com>)

* Fri Jul 25 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.06-2
- Fix crash on start up in some case with dual screen
  (bug 456399: patch from jwz)

* Thu Jul 24 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- Build some test binaries for debugging

* Thu Jul 17 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.06-1
- Update to 5.06

* Wed Jul  9 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.05.90.3-3
- Apply a experimental randr 1.2 patch by jwz

* Mon Jun  1 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.05-4
- Fix compilation error with GLib 2.17+

* Sun Apr  6 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.05-3
- penetrate - fallback to smaller font

* Wed Mar  5 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.05-2
- Replace addopts.patch with the patch from jwz

* Sun Mar  2 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.05-1
- Update to 5.05

* Sun Feb 10 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.04-5
- Add -Wno-overlength-strings to shut up string length warning

* Sat Feb  9 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.04-4
- Add patch to xscreensaver be happy with gcc43
- Rebuild against gcc43

* Fri Dec  7 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.04-3
- Fix desktop icon name for desktop-file-utils 0.14+ on F-9+

* Fri Nov 16 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.04-2
- Rebuild against fixed mesa for F-9 (bug 380141)

* Tue Nov 13 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.04-1
- Update to 5.04

* Thu Nov  1 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.03-14
- Patch from upstream to fix screen depth problem (also "really"
  fix bug 336331).

* Thu Oct 18 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.03-12
- Create -gl-base subpackage and split xscreensaver-gl-helper 
  into -gl-base subpackage so that external GL screensavers can
  use it (bug 336331)

* Mon Oct 15 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.03-11
- Suppress compiler warning

* Sat Oct  6 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.03-10
- Fix the maximum value on demo configuration dialog
- Change the encoding of XScreenSaver.ad and man files (bug 319101)

* Tue Oct  2 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.03-9
- Change the default browser to xdg-open
- Don't mark XScreenSaver.ad as %%config. This file is overwritten
  automatically.

* Mon Sep 24 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.03-8
- Some cleanup.

* Wed Sep 19 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.03-7
- Remove noreplace flag from XScreenSaver.ad as this is updated
  automatically.

* Sat Sep 15 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.03-6
- Fix update script to treat the ending character of conf file
  correctly.

* Sat Sep 15 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.03-5
- Add some comments on update script.

* Mon Sep  3 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.03-3
- Don't split hack part of XScreenSaver.ad into each hack piece
  and make update script allow multiple hacks in one config file
  (along with rss-glx, bug 200881)
- move hack update scripts to %%_sbindir

* Sun Sep  2 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.03-2
- Try to make XScreenSaver.ad modular (bug 200881)

* Wed Aug 29 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.03-1
- Update to 5.03

* Tue Aug 28 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.02-4
- Spec file cleanup
  - Don't use include-directory patch anymore
  - Make all xscreensaver related directories owned by -base subpackage
    because now -extras and -gl-extras subpackage require it.
  - Mark man files as %%doc explicitly, because %%_mandir is expanded
    in files list
- Fix write_long() (actually no_malloc_number_to_string())

* Wed Aug 22 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.02-3.dist.1
- Mass rebuild (buildID or binutils issue)

* Tue Aug 14 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.02-3
- Remove man6x from file entry, now included in filesystem

* Sun Aug 12 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.02-2
- Fix up desktop categories

* Sat Apr 21 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.02-1
- Update to 5.02

* Sat Feb  3 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.01-6
- Make hack packages require base package (#227017)
- Create xscreensaver metapackage

* Mon Nov 20 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.01-5
- Require xorg-x11-resutils (#216245)

* Sun Nov  5 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.01-4
- No net connection by default for webcollage (possibly fix #214095 ?)

* Fri Sep 29 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.01-3
- Fix the arguments of desktop files (#208560)

* Tue Sep 26 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.01-2
- Finally move man pages to 6x (#205796)
- Fix the ownership of directories (#187892)

* Tue Sep 19 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.01-1
- 5.01
- Revert non-passwd auth patch and disable it for now (see bug #205669)

* Sun Sep 17 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.01-0.a1.2
- 5.01a1
- Revert lang related patch (still needing some works)
- Disable small scale window (patch from upstream)
- Disable non-password authentication.

* Sun Sep 10 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-22
- Fix Patch114.

* Sun Sep 10 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-21
- Try to support non-password PAM authentication (bug #205669)

* Sat Sep  9 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-20
- Change default document.
- Again man entry fix.

* Tue Sep  5 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-19
- Create desktop files for gnome-screensaver (bug #204944)

* Mon Aug 28 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-18
- Unify locale releated patches.

* Mon Aug 28 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-17.1
- Rebuild.

* Fri Aug 18 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-17
- Very nasty segv problem was brought by me. Fixing......
 
* Thu Aug 10 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-16
- Move man entry to 6x (bug #197741)

* Fri Jul 28 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-15
- Rebuild again as fedora-release-5.91.1 is released.

* Mon Jul 17 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-14
- Correct paths to update po files properly and try re-creating po files.
- Rebuild for FC6T2 devel freeze.

* Mon Jul  3 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-13
- Fix for causing SEGV on exit about petri, squiral (total: 22 hacks)
  I hope this will finally fix all hacks' problems.

* Sun Jul  2 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-12
- Fix other (extras, gl-extras) hacks (total: 21 hacks).
- Make sure the subprocess xscreensaver-getimage is properly
  killed by parent hack process.

* Fri Jun 30 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-11
- Fix interaggregate segv.

* Thu Jun 29 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-10
- Fix xscreensaver-extras hacks which cause SEGV or SIGFPE.

* Tue Jun 27 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-9
- Don't make xscreensaver-base require htmlview.
- Update ja.po again.
- Fix noseguy not to eat cpu when geometry is too small.

* Fri Jun 23 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-8
- Spec file script change.
- Add libtool to BuildRequires.

* Thu Jun 15 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-7
- Change timestamps.
- Forcely replace the default text till the release version of fedora-release
  formally changes.

* Sat Jun 10 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-6.1
- Fix the requirement for rebuilding to meet the demand
  from current mock.

* Wed Jun  7 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-6
- Another fixes of config files for ifsmap as reported to jwz 
  livejournal page.
- Update Japanese translation.
- Locale fix for xscreensaver-text.

* Thu Jun  1 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-5
- Disable (not remove) some hacks by default according to 4.24 behavior.
- XML file fix for slidescreen.

* Thu Jun  1 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-4
- Rewrite the patch for decimal separator as discussed with jwz.
- Change defaults not by patch but by function.

* Wed May 31 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-3
- Fix browser option patch.

* Wed May 31 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-2
- Change the default text.
- Rewrite root passwd patch.
- Add browser option to configure.
- Fix requirement about desktop-backgrounds-basic.
- Fix decimal separator problem reported by upstream.

* Fri May 26 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-1
- Update to 5.00 .
- Switch to extras, don't remove anything.

* Fri Mar 24 2006 Ray Strode <rstrode@redhat.com> - 1:4.24-2
- add patch from jwz to reap zombie processes (bug 185833)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:4.24-1.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:4.23-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 13 2006 Ray Strode <rstrode@redhat.com> 1:4.23-1
- update to 4.23
- add a BuildRequires on imake (spotted by Mamoru Tasaka)
- add a lot of patches and fixes from Mamoru Tasaka

* Sat Dec 17 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Dec  5 2005 Ray Strode <rstrode@redhat.com> 1:4.22-21
- Update list_files function to fix ownership issues.
  Patch from Mamoru Tasaka (mtasaka@ioa.s.u-tokyo.ac.jp) (bug 161728).

* Tue Nov  1 2005 Ray Strode <rstrode@redhat.com> 1:4.22-20
- Switch requires to modular X

* Thu Oct 13 2005 Tomas Mraz <tmraz@redhat.com> 1:4.22-19
- use include instead of pam_stack in pam config

* Wed Sep 28 2005 Ray Strode <rstrode@redhat.com> 1:4.22-18
- accept zero timeout values for suspend and off.
  Patch from Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
  (bug 157501). 

* Fri Sep 23 2005 Ray Strode <rstrode@redhat.com> 1:4.22-17
- remove explicit dependency on xscreensaver-base for 
  extras and gl-extras packages

* Fri Sep 16 2005 Ray Strode <rstrode@redhat.com> 1:4.22-16
- don't allow root to authenticate lock dialog when selinux
  is enabled (bug 157014).

* Fri Sep  9 2005 Ray Strode <rstrode@redhat.com> 1:4.22-15
- take BSOD out of the default random list (bug 105388).

* Thu Sep 08 2005 Florian La Roche <laroche@redhat.com>
- add version-release to the Provides:

* Wed Sep  7 2005 Ray Strode <rstrode@redhat.com> 1:4.22-13
- Patch from Mamoru Tasaka to improve man page handling
  (bug 167708).

* Tue Sep  6 2005 Ray Strode <rstrode@redhat.com> 1:4.22-12
- remove density option from squiral screensaver,
  Patch from Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
  (bug 167374).

* Wed Aug 31 2005 Ray Strode <rstrode@redhat.com> 1:4.22-11
- ignore unprintable characters in password dialog (bug 135966).

* Thu Aug 25 2005 Ray Strode <rstrode@redhat.com> 1:4.22-10
- Move man pages to section 6 (bug 166441). 

* Wed Aug 24 2005 Ray Strode <rstrode@redhat.com> 1:4.22-9
- The only legitimate way to call realpath is with NULL 
  buffer (bug 165270).

* Fri Aug 19 2005 Ray Strode <rstrode@redhat.com> 1:4.22-8
- Don't try to use an invalid tree iterator (bug 166299)

* Tue Aug 16 2005 Warren Togami <wtogami@redhat.com> - 1:4.22-7
- rebuild for new cairo

* Wed Aug 10 2005 Ray Strode <rstrode@redhat.com> 1:4.22-6
- Don't call printf in signal handler (might fix 126428)

* Wed Aug  3 2005 Ray Strode <rstrode@redhat.com> 1:4.22-5
- Update to xscreensaver 4.22.

* Sun Jun 19 2005 Ray Strode <rstrode@redhat.com> 1:4.21-5
- Add build requires for desktop-file-utils (bug 160980). 

* Wed May 11 2005 Ray Strode <rstrode@redhat.com> 1:4.21-4
- Allow configuration gui to support hacks with absolute paths
  (bug 157417). 

* Mon May 09 2005 Ray Strode <rstrode@redhat.com> 1:4.21-3
- Use @libexecdir@/xscreensaver instead of @HACKDIR@ in
  default configuration file so that the path gets expanded
  fully (bug 156906).

* Tue May 03 2005 Ray Strode <rstrode@redhat.com> 1:4.21-2
- Use absolute filenames for screenhacks so we don't pull
  in screenhacks from PATH (bug 151677).
- Don't try to ping in sonar screensaver (bug 139692).

* Sun Mar 20 2005 Ray Strode <rstrode@redhat.com> 1:4.21-1
- Update to xscreensaver-4.21.
- Update spec file to better match new upstream spec file.

* Fri Feb 25 2005 Nalin Dahyabhai <nalin@redhat.com> 1:4.18-19
- We don't patch configure.in, so we don't need to run 'autoconf'.
- Add --without-kerberos to skip built-in Kerberos password verification, so
  that we'll always go through PAM (fixes 149731).

* Mon Feb 21 2005 Ray Strode <rstrode@redhat.com> 1:4.18-18
- Install desktop files to /usr/share/applications instead of
  /usr/share/control-center-2.0 (should fix bug 149229).

* Thu Jan  6 2005 Ray Strode <rstrode@redhat.com> 1:4.18-17
- Change lock dialog instructions to only ask for password
  and not username.

* Tue Jan  4 2005 Ray Strode <rstrode@redhat.com> 1:4.18-16
- Add patch to spec file to change defaults

* Tue Jan  4 2005 Ray Strode <rstrode@redhat.com> 1:4.18-15
- Remove xscreensaver-config-tool after some discussions with
  jwz.
- Take out some additional screensavers

* Wed Dec  1 2004 Ray Strode <rstrode@redhat.com> 1:4.18-14
- Add utility xscreensaver-config-tool to make changing settings
  easier (replaces the short lived xscreensaver-register-hack
  program).  Use xscreensaver-config-tool to set default settings
  instead of using patches. 
- Split up xscreensaver (fixes 121693).
- Make preferences dialog slightly more pretty
- Make lock dialog slightly more pretty

* Fri Nov 26 2004 Than Ngo <than@redhat.com> 1:4.18-13
- add patch to fix vroot bug and make xscreensaver working in KDE again.
- get rid of webcollage, which often download porn images
 
* Wed Nov 10 2004 Ray Strode <rstrode@redhat.com> 1:4.18-11
- Add xscreensaver-register-hack program to make
  installing and uninstalling screensavers easier
  (working toward fixing bug 121693 [split up screensaver])

* Wed Nov 10 2004 Ray Strode <rstrode@redhat.com> 1:4.18-10
- Get rid of unnecessary xloadimage requirement
  (bug 100641)

* Wed Nov 10 2004 Ray Strode <rstrode@redhat.com> 1:4.18-9
- Call pam_acct_mgmt() (might fix bug 137195) 

* Tue Nov 9 2004 Ray Strode <rstrode@redhat.com> 1:4.18-8
- Give vidwhacker screensaver working defaults
  (bug 64518)

* Tue Nov 9 2004 Ray Strode <rstrode@redhat.com> 1:4.18-7
- Get rid of old crufty %%{_datadir}/control-center/ tree
  (bug 114692)

* Wed Nov 3 2004 Ray Strode <rstrode@redhat.com> 1:4.18-6
- rebuild for rawhide

* Wed Nov 3 2004 Ray Strode <rstrode@redhat.com> 1:4.18-5
- Don't allow screensavers access to desktop images by default (bug #126809)
- Lock screen by default (bug #126809)

* Tue Oct 19 2004  <krh@redhat.com> 4.18-4
- Add xscreensaver-4.18-stuff-piecewise-leak.patch to stop piecewise
  from leaking (#135164).

* Wed Sep 1 2004 Ray Strode <rstrode@redhat.com> 4.18-3
- remove superfluous line in the spec file

* Wed Sep 1 2004 Ray Strode <rstrode@redhat.com> 4.18-2
- blank the screen by default

* Tue Aug 24 2004 Ray Strode <rstrode@redhat.com> 4.18-1
- update to 4.18 (fixes bug 87745).

* Sat Aug 14 2004 Ray Strode <rstrode@redhat.com> 4.16-4
- change titles of questionably named bar codes
  (fixes bug 129929).

* Fri Aug 6 2004 Ray Strode <rstrode@redhat.com> 4.16-3
- change titles of questionably named shape formations
  (fixes bug 129335).

* Wed Jun 23 2004 Ray Strode <rstrode@redhat.com> 4.16-2
- use htmlview for browsing help.

* Mon Jun 21 2004 Ray Strode <rstrode@redhat.com> 4.16-1
- update to 4.16.  Use desktop-file-install for desktop file.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May  5 2004 Bill Nottingham <notting@redhat.com> 4.14-5
- config tweaks

* Wed Mar 31 2004 Karsten Hopp <karsten@redhat.de> 4.14-4 
- fix fortune stand-in (#115369)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Oct 27 2003 Bill Nottingham <notting@redhat,com> 1:4.14-1
- update to 4.14

* Tue Oct  7 2003 Bill Nottingham <notting@redhat.com> 1:4.13-1
- take out flag-with-logo, don't require redhat-logos (#106046)
- update to 4.13

* Wed Aug 27 2003 Bill Nottingham <notting@redhat.com> 1:4.12-1
- update to 4.12 (fixes #101920)
- re-add BSOD to the random list

* Tue Jun 24 2003 Bill Nottingham <notting@redhat.com> 1:4.11-1
- update to 4.11

* Fri Jun 13 2003 Bill Nottingham <notting@redhat.com> 1:4.10-3
- fix some 64-bit arches (#97359)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 28 2003 Bill Nottingham <notting@redhat.com> 1:4.10-1
- update to 4.10

* Thu Mar 20 2003 Bill Nottingham <notting@redhat.com> 1:4.09-1
- update to 4.09, now with bouncing cows

* Mon Feb 10 2003 Bill Nottingham <notting@redhat.com> 1:4.07-2
- oops, xloadimage *is* needed (#83676)

* Thu Feb  6 2003 Bill Nottingham <notting@redhat.com> 1:4.07-1
- update to 4.07, fixes #76276, #75574

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Nov 29 2002 Tim Powers <timp@redhat.com> 1:4.06-4
- call autoconf instead of autoconf-2.53

* Mon Nov 11 2002 Bill Nottingham <notting@redhat.com> 4.06-3
- put glade tweaks back in
- switch pam package to not specify directories, to work on multilib
  arches

* Fri Nov  8 2002 Nalin Dahyabhai <nalin@redhat.com> 4.06-1
- add a BuildPrereq on bc, which configure requires
- replace use of fortune with an innocuous-and-editable stand-in script in
  %%{stand_in_path}
- define FORTUNE_PROGRAM at compile-time to force apps to use what's specified
  even if it doesn't happen to be installed at compile-time

* Sun Sep  2 2002 Bill Nottingham <notting@redhat.com> 4.05-6
- fix typo (#73246)

* Wed Aug 28 2002 Bill Nottingham <notting@redhat.com> 4.05-5
- revert to non-gtk unlock dialog
- fix translations

* Mon Aug 12 2002 Bill Nottingham <notting@redhat.com> 4.05-4
- twiddle titlebar (#67844)
- fix extraneous text (#70975)
- tweak desktop entry (#69502)

* Fri Aug 9 2002 Yu Shao <yshao@redhat.com> 4.05-3
- use GTK_IM_MODULE=gtk-im-context-simple in lock widget
- to avoid CJK IM weirdness (#70655, #68216)
- xscreensaver-rh-imcjk.patch

* Wed Jul 17 2002 Elliot Lee <sopwith@redhat.com> 4.05-2
- Add fortune-mod to buildprereq to make beehive happy
- Fix find_lang usage - install translations properly by specifying datadir

* Tue Jun 11 2002 Bill Nottingham <notting@redhat.com> 4.05-1
- update to 4.05
- use gtk2 lock widget (<jacob@ximian.com>)
- some Red Hat-ifications
- fix critical (#63916)

* Mon Jun 10 2002 Bill Nottingham <notting@redhat.com> 4.04-2
- remove no longer needed xloadimage dependency

* Mon Jun  3 2002 Bill Nottingham <notting@redhat.com> 4.04-1
- update to 4.04, gtk2 property dialog is now mainline

* Thu May 16 2002 Bill Nottingham <notting@redhat.com> 4.03-1
- update to 4.03
- use gtk2 properties dialog

* Thu Mar 14 2002 Bill Nottingham <notting@redhat.com> 4.01-2
- don't show screensavers that aren't available

* Sun Feb 24 2002 Bill Nottingham <notting@redhat.com>
- update to 4.01

* Mon Feb 11 2002 Bill Nottingham <notting@redhat.com>
- update to 4.00

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Aug 23 2001 Bill Nottingham <notting@redhat.com>
- fix segfault on ia64 (#52336)

* Thu Aug  9 2001 Bill Nottingham <notting@redhat.com>
- never mind, back to 3.33 (wheeee)
- hack window-id back in for the time being
- disable memlimit so GL works

* Mon Jul 23 2001 Bill Nottingham <notting@redhat.com>
- oops, back to 3.32 for now
- remove optflags override (oops)
- add pam-devel buildprereq

* Mon Jul 16 2001 Bill Nottingham <notting@redhat.com>
- update to 3.33, fix broken last build
- fix build weirdness on some package sets (#48905)
- don't document non-existent options for forest (#49139)

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Tue May 22 2001 Havoc Pennington <hp@redhat.com>
- putting in tree for David 

* Tue May 22 2001 David Sainty <dsainty@redhat.com>
- added DPMS options to command line help

* Sun Apr 22 2001 Bill Nottingham <notting@redhat.com>
- update to 3.32
- add patch to specify DPMS settings on the command line

* Wed Apr 11 2001 Bill Nottingham <notting@redhat.com>
- update to 3.31

* Wed Apr  4 2001 Bill Nottingham <notting@redhat.com>
- fix extrusion exclusion (#34742)

* Tue Apr  3 2001 Bill Nottingham <notting@redhat.com>
- disable GL screensavers by default (bleah)

* Mon Feb 19 2001 Bill Nottingham <notting@redhat.com>
- update to 3.29 (#27437)

* Tue Jan 23 2001 Bill Nottingham <notting@redhat.com>
- update to 3.27

* Fri Dec 01 2000 Bill Nottingham <notting@redhat.com>
- rebuild because of broken fileutils

* Fri Nov 10 2000 Bill Nottingham <notting@redhat.com>
- 3.26

* Fri Aug 11 2000 Jonathan Blandford <jrb@redhat.com>
- Up Epoch and release

* Wed Jul 26 2000 Bill Nottingham <notting@redhat.com>
- hey, vidmode works again

* Fri Jul 21 2000 Bill Nottingham <notting@redhat.com>
- update to 3.25

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jun 17 2000 Bill Nottingham <notting@redhat.com>
- xscreensaver.kss is not a %%config file.

* Sun Jun 11 2000 Bill Nottingham <notting@redhat.com>
- tweak kss module (#11872)

* Thu Jun  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- modify PAM configuration to use system-auth

* Thu May 18 2000 Preston Brown <pbrown@redhat.com>
- added Red Hat screensaver (waving flag has logo now).

* Fri May  5 2000 Bill Nottingham <notting@redhat.com>
- tweaks for ia64

* Mon Apr 10 2000 Bill Nottingham <notting@redhat.com>
- turn off xf86vidmode ext, so that binaries built against XFree86 4.0
  work on 3.x servers

* Wed Apr  5 2000 Bill Nottingham <notting@redhat.com>
- turn off gnome support for now

* Mon Apr  3 2000 Bill Nottingham <notting@redhat.com>
- update to 3.24

* Wed Feb 09 2000 Preston Brown <pbrown@redhat.com>
- wmconfig entry gone.

* Mon Jan 31 2000 Bill Nottingham <notting@redhat.com>
- update to 3.23

* Fri Jan 14 2000 Bill Nottingham <notting@redhat.com>
- rebuild to fix GL depdencies

* Tue Dec 14 1999 Bill Nottingham <notting@redhat.com>
- everyone in GL
- single package again

* Fri Dec 10 1999 Bill Nottingham <notting@redhat.com>
- update to 3.22
- turn off xf86vmode on alpha

* Tue Dec  7 1999 Bill Nottingham <notting@redhat.com>
- mmm... hardware accelerated GL on i386. :) :)

* Mon Nov 22 1999 Bill Nottingham <notting@redhat.com>
- 3.21
- use shm on alpha, let's see what breaks

* Tue Nov 16 1999 Bill Nottingham <notting@redhat.com>
- update to 3.20

* Wed Nov  3 1999 Bill Nottingham <notting@redhat.com>
- update to 3.19

* Thu Oct 14 1999 Bill Nottingham <notting@redhat.com>
- update to 3.18

* Sat Sep 25 1999 Bill Nottingham <notting@redhat.com>
- add a '-oneshot' single time lock option.

* Mon Sep 20 1999 Bill Nottingham <notting@redhat.com>
- take webcollage out of random list (for people who pay for bandwidth)

* Fri Sep 10 1999 Bill Nottingham <notting@redhat.com>
- patch webcollage to use xloadimage
- in the random list, run petri with -size 2 to save memory
- extend RPM silliness to man pages, too.

* Mon Jul 19 1999 Bill Nottingham <notting@redhat.com>
- update to 3.17
- add a little RPM silliness to package GL stuff if it's built

* Thu Jun 24 1999 Bill Nottingham <notting@redhat.com>
- update to 3.16

* Mon May 10 1999 Bill Nottingham <notting@redhat.com>
- update to 3.12

* Tue May  4 1999 Bill Nottingham <notting@redhat.com>
- remove security problem introduced earlier

* Wed Apr 28 1999 Bill Nottingham <notting@redhat.com>
- update to 3.10

* Thu Apr 15 1999 Bill Nottingham <notting@redhat.com>
- kill setuid the Right Way(tm)

* Mon Apr 12 1999 Bill Nottingham <notting@redhat.com>
- fix xflame on alpha

* Mon Apr 12 1999 Preston Brown <pbrown@redhat.com>
- upgrade to 3.09, fixes vmware interaction problems.

* Mon Apr  5 1999 Bill Nottingham <notting@redhat.com>
- remove setuid bit. Really. I mean it.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 3)

* Fri Mar 19 1999 Bill Nottingham <notting@redhat.com>
- kill setuid, since pam works OK

* Tue Mar 16 1999 Bill Nottingham <notting@redhat.com>
- update to 3.08

* Wed Feb 24 1999 Bill Nottingham <notting@redhat.com>
- wmconfig returns, and no one is safe...

* Tue Feb 23 1999 Bill Nottingham <notting@redhat.com>
- remove bsod from random list because it's confusing people???? *sigh*

* Tue Jan 12 1999 Cristian Gafton <gafton@redhat.com>
- call libtoolize to get it to compile cleanely on the arm

* Tue Jan  5 1999 Bill Nottingham <notting@redhat.com>
- update to 3.07

* Mon Nov 23 1998 Bill Nottingham <notting@redhat.com>
- update to 3.06

* Tue Nov 17 1998 Bill Nottingham <notting@redhat.com>
- update to 3.04

* Thu Nov 12 1998 Bill Nottingham <notting@redhat.com>
- update to 3.02
- PAMify

* Tue Oct 13 1998 Cristian Gafton <gafton@redhat.com>
- take out Noseguy module b/c of possible TMv
- install modules in /usr/X11R6/lib/xscreensaver
- don't compile support for xshm on the alpha
- properly buildrooted
- updated to version 2.34

* Fri Aug  7 1998 Bill Nottingham <notting@redhat.com>
- update to 2.27

* Wed Jun 10 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Mon Jun 08 1998 Erik Troan <ewt@redhat.com>
- added fix for argv0 buffer overflow

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sat Apr 11 1998 Donnie Barnes <djb@redhat.com>
- updated from 2.10 to 2.16
- added buildroot

* Wed Oct 25 1997 Marc Ewing <marc@redhat.com>
- wmconfig

* Thu Oct 23 1997 Marc Ewing <marc@redhat.com>
- new version, configure

* Fri Aug 22 1997 Erik Troan <ewt@redhat.com>
- built against glibc


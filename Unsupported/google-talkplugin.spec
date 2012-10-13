%define __os_install_post %{nil}
%define _enable_debug_packages %{nil}
Summary: Google Talk Plugin
Name: google-talkplugin
Version: 2.5.6.0
Release: 1
License: Proprietary (see http://www.google.com/talk/terms.html)
Group: Applications/Internet
Packager: Voice and Video Chat Linux Team <voice-and-video-linux-packager@google.com>
Vendor: Google, Inc.
URL: http://www.google.com/chat/video
BuildArch: x86_64
Prefix: /opt
Source: google-talkplugin-2.5.6.0-1.x86_64.rpm
BuildRoot: %{_tmppath}/%{name}-%{version}-root
AutoReqProv: 0
Requires: /bin/sh, at, ld-linux-x86-64.so.2()(64bit), libCg.so()(64bit), libCgGL.so()(64bit), libGL.so.1()(64bit), libX11.so.6, libX11.so.6()(64bit), libXcomposite.so.1, libXfixes.so.3, libXrandr.so.2, libXrender.so.1, libXt.so.6()(64bit), libasound.so.2, libc.so.6, libc.so.6()(64bit), libc.so.6(GLIBC_2.0), libc.so.6(GLIBC_2.1), libc.so.6(GLIBC_2.1.2), libc.so.6(GLIBC_2.1.3), libc.so.6(GLIBC_2.11), libc.so.6(GLIBC_2.11)(64bit), libc.so.6(GLIBC_2.2), libc.so.6(GLIBC_2.2.5)(64bit), libc.so.6(GLIBC_2.3), libc.so.6(GLIBC_2.3)(64bit), libc.so.6(GLIBC_2.3.2), libc.so.6(GLIBC_2.3.4), libc.so.6(GLIBC_2.3.4)(64bit), libc.so.6(GLIBC_2.4), libc.so.6(GLIBC_2.4)(64bit), libc.so.6(GLIBC_2.7), libc.so.6(GLIBC_2.7)(64bit), libcairo.so.2()(64bit), libdl.so.2, libdl.so.2()(64bit), libdl.so.2(GLIBC_2.0), libdl.so.2(GLIBC_2.1), libdl.so.2(GLIBC_2.2.5)(64bit), libfontconfig.so.1()(64bit), libfreetype.so.6()(64bit), libgcc_s.so.1, libgcc_s.so.1(GCC_3.0), libgcc_s.so.1(GLIBC_2.0), libgdk-x11-2.0.so.0, libgdk-x11-2.0.so.0()(64bit), libgdk_pixbuf-2.0.so.0, libglib-2.0.so.0, libglib-2.0.so.0()(64bit), libgobject-2.0.so.0, libgobject-2.0.so.0()(64bit), libgtk-x11-2.0.so.0, libgtk-x11-2.0.so.0()(64bit), libm.so.6, libm.so.6()(64bit), libm.so.6(GLIBC_2.0), libm.so.6(GLIBC_2.1), libm.so.6(GLIBC_2.2.5)(64bit), libpng12.so.0()(64bit), libpng12.so.0(PNG12_0)(64bit), libpthread.so.0, libpthread.so.0()(64bit), libpthread.so.0(GLIBC_2.0), libpthread.so.0(GLIBC_2.1), libpthread.so.0(GLIBC_2.2), libpthread.so.0(GLIBC_2.2.5)(64bit), libpthread.so.0(GLIBC_2.3.2), libpthread.so.0(GLIBC_2.3.2)(64bit), libpthread.so.0(GLIBC_2.3.3), libpulse.so.0, librt.so.1, librt.so.1()(64bit), librt.so.1(GLIBC_2.2), librt.so.1(GLIBC_2.2.5)(64bit), libstdc++.so.6, libstdc++.so.6()(64bit), libstdc++.so.6(CXXABI_1.3), libstdc++.so.6(CXXABI_1.3)(64bit), libstdc++.so.6(CXXABI_1.3.1), libstdc++.so.6(GLIBCXX_3.4), libstdc++.so.6(GLIBCXX_3.4)(64bit), libstdc++.so.6(GLIBCXX_3.4.11)(64bit), libstdc++.so.6(GLIBCXX_3.4.9), libstdc++.so.6(GLIBCXX_3.4.9)(64bit), libv4l2.so.0, rtld(GNU_HASH)
Provides: libCg.so()(64bit), libCgGL.so()(64bit), libnpgoogletalk64.so()(64bit), libnpgtpo3dautoplugin.so()(64bit), google-talkplugin = 2.5.6.0-1, google-talkplugin(x86-64) = 2.5.6.0-1

%description
The Google Talk Plugin is a browser plugin that enables you to use Google voice
and video chat to chat face to face with family and friends.

This product includes software developed by the OpenSSL Project for use in the
OpenSSL Toolkit (http://www.openssl.org/). This product includes cryptographic
software written by Eric Young (eay@cryptsoft.com).

Originally done with rpm version 4.8.1,
built on ri-ou2.kir.corp.google.com at Wed Nov 16 19:12:16 2011
from google-talkplugin-2.5.6.0-1.src.rpm with opt flags -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m64 -mtune=generic

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
pushd $RPM_BUILD_ROOT
rpm2cpio %{SOURCE0}|cpio -i -d
popd

%clean
rm -rf $RPM_BUILD_ROOT


%pre

exit 0




#------------------------------------------------------------------------------
#   Post install script
#------------------------------------------------------------------------------


%post

# System-wide package configuration.
DEFAULTS_FILE="/etc/default/google-talkplugin"

# sources.list setting for google-talkplugin updates.
REPOCONFIG="http://dl.google.com/linux/talkplugin/rpm/stable"

# Install the repository signing key (see also:
# http://www.google.com/linuxrepositories/aboutkey.html)
install_rpm_key() {
  # Check to see if key already exists.
  rpm -q gpg-pubkey-7fac5991-4615767f > /dev/null 2>&1
  if [ "$?" -eq "0" ]; then
    # Key already exists
    return 0
  fi
  # This is to work around a bug in RPM 4.7.0. (see http://crbug.com/22312)
  rpm -q gpg-pubkey-7fac5991-45f06f46 > /dev/null 2>&1
  if [ "$?" -eq "0" ]; then
    # Key already exists
    return 0
  fi

  # RPM on Mandriva 2009 is dumb and does not understand "rpm --import -"
  TMPKEY=$(mktemp /tmp/google.sig.XXXXXX)
  if [ -n "$TMPKEY" ]; then
    cat > "$TMPKEY" <<KEYDATA
-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG v1.4.2.2 (GNU/Linux)

mQGiBEXwb0YRBADQva2NLpYXxgjNkbuP0LnPoEXruGmvi3XMIxjEUFuGNCP4Rj/a
kv2E5VixBP1vcQFDRJ+p1puh8NU0XERlhpyZrVMzzS/RdWdyXf7E5S8oqNXsoD1z
fvmI+i9b2EhHAA19Kgw7ifV8vMa4tkwslEmcTiwiw8lyUl28Wh4Et8SxzwCggDcA
feGqtn3PP5YAdD0km4S4XeMEAJjlrqPoPv2Gf//tfznY2UyS9PUqFCPLHgFLe80u
QhI2U5jt6jUKN4fHauvR6z3seSAsh1YyzyZCKxJFEKXCCqnrFSoh4WSJsbFNc4PN
b0V0SqiTCkWADZyLT5wll8sWuQ5ylTf3z1ENoHf+G3um3/wk/+xmEHvj9HCTBEXP
78X0A/0Tqlhc2RBnEf+AqxWvM8sk8LzJI/XGjwBvKfXe+l3rnSR2kEAvGzj5Sg0X
4XmfTg4Jl8BNjWyvm2Wmjfet41LPmYJKsux3g0b8yzQxeOA4pQKKAU3Z4+rgzGmf
HdwCG5MNT2A5XxD/eDd+L4fRx0HbFkIQoAi1J3YWQSiTk15fw7RMR29vZ2xlLCBJ
bmMuIExpbnV4IFBhY2thZ2UgU2lnbmluZyBLZXkgPGxpbnV4LXBhY2thZ2VzLWtl
eW1hc3RlckBnb29nbGUuY29tPohjBBMRAgAjAhsDBgsJCAcDAgQVAggDBBYCAwEC
HgECF4AFAkYVdn8CGQEACgkQoECDD3+sWZHKSgCfdq3HtNYJLv+XZleb6HN4zOcF
AJEAniSFbuv8V5FSHxeRimHx25671az+uQINBEXwb0sQCACuA8HT2nr+FM5y/kzI
A51ZcC46KFtIDgjQJ31Q3OrkYP8LbxOpKMRIzvOZrsjOlFmDVqitiVc7qj3lYp6U
rgNVaFv6Qu4bo2/ctjNHDDBdv6nufmusJUWq/9TwieepM/cwnXd+HMxu1XBKRVk9
XyAZ9SvfcW4EtxVgysI+XlptKFa5JCqFM3qJllVohMmr7lMwO8+sxTWTXqxsptJo
pZeKz+UBEEqPyw7CUIVYGC9ENEtIMFvAvPqnhj1GS96REMpry+5s9WKuLEaclWpd
K3krttbDlY1NaeQUCRvBYZ8iAG9YSLHUHMTuI2oea07Rh4dtIAqPwAX8xn36JAYG
2vgLAAMFB/wKqaycjWAZwIe98Yt0qHsdkpmIbarD9fGiA6kfkK/UxjL/k7tmS4Vm
CljrrDZkPSQ/19mpdRcGXtb0NI9+nyM5trweTvtPw+HPkDiJlTaiCcx+izg79Fj9
KcofuNb3lPdXZb9tzf5oDnmm/B+4vkeTuEZJ//IFty8cmvCpzvY+DAz1Vo9rA+Zn
cpWY1n6z6oSS9AsyT/IFlWWBZZ17SpMHu+h4Bxy62+AbPHKGSujEGQhWq8ZRoJAT
G0KSObnmZ7FwFWu1e9XFoUCt0bSjiJWTIyaObMrWu/LvJ3e9I87HseSJStfw6fki
5og9qFEkMrIrBCp3QGuQWBq/rTdMuwNFiEkEGBECAAkFAkXwb0sCGwwACgkQoECD
D3+sWZF/WACfeNAu1/1hwZtUo1bR+MWiCjpvHtwAnA1R3IHqFLQ2X3xJ40XPuAyY
/FJG
=Quqp
-----END PGP PUBLIC KEY BLOCK-----
KEYDATA
    rpm --import "$TMPKEY"
    rc=$?
    rm -f "$TMPKEY"
    if [ "$rc" -eq "0" ]; then
      return 0
    fi
  fi
  return 1
}

determine_rpm_package_manager() {
  local RELEASE
  LSB_RELEASE="$(which lsb_release 2> /dev/null)"
  if [ -x "$LSB_RELEASE" ]; then
    RELEASE=$(lsb_release -i 2> /dev/null)
    case $DISTRIB_ID in
    "Fedora")
      PACKAGEMANAGER=yum
      ;;
    "MandrivaLinux")
      PACKAGEMANAGER=urpmi
      ;;
    "SUSE LINUX")
      PACKAGEMANAGER=yast
      ;;
    esac
  fi

  if [ "$PACKAGEMANAGER" ]; then
    return
  fi

  # Fallback methods that are probably unnecessary on modern systems.
  if [ -f "/etc/lsb-release" ]; then
    # file missing on Fedora, does not contain DISTRIB_ID on OpenSUSE.
    eval $(sed -e '/DISTRIB_ID/!d' /etc/lsb-release)
    case $DISTRIB_ID in
    MandrivaLinux)
      PACKAGEMANAGER=urpmi
      ;;
    esac
  fi

  if [ "$PACKAGEMANAGER" ]; then
    return
  fi

  if [ -f "/etc/fedora-release" ] || [ -f "/etc/redhat-release" ]; then
    PACKAGEMANAGER=yum
  elif [ -f "/etc/SuSE-release" ]; then
    PACKAGEMANAGER=yast
  elif [ -f "/etc/mandriva-release" ]; then
    PACKAGEMANAGER=urpmi
  fi
}

DEFAULT_ARCH="x86_64"
YUM_REPO_FILE="/etc/yum.repos.d/google-talkplugin.repo"
ZYPPER_REPO_FILE="/etc/zypp/repos.d/google-talkplugin.repo"
URPMI_REPO_FILE="/etc/urpmi/urpmi.cfg"

install_yum() {
  install_rpm_key

  if [ ! "$REPOCONFIG" ]; then
    return 0
  fi

  if [ -d "/etc/yum.repos.d" ]; then
cat > "$YUM_REPO_FILE" << REPOCONTENT
[google-talkplugin]
name=google-talkplugin
baseurl=$REPOCONFIG/$DEFAULT_ARCH
enabled=1
gpgcheck=1
REPOCONTENT
  fi
}

# This is called by the cron job, rather than in the RPM postinstall.
# We cannot do this during the install when urpmi is running due to
# database locking. We also need to enable the repository, and we can
# only do that while we are online.
# see: https://qa.mandriva.com/show_bug.cgi?id=31893
configure_urpmi() {
  if [ ! "$REPOCONFIG" ]; then
    return 0
  fi

  urpmq --list-media | grep -q -s "^google-talkplugin$"
  if [ "$?" -eq "0" ]; then
    # Repository already configured
    return 0
  fi
  urpmi.addmedia --update \
    "google-talkplugin" "$REPOCONFIG/$DEFAULT_ARCH"
}

install_urpmi() {
  # urpmi not smart enough to pull media_info/pubkey from the repository?
  install_rpm_key

  # Defer urpmi.addmedia to configure_urpmi() in the cron job.
  # See comment there.
  #
  # urpmi.addmedia --update \
  #   "google-talkplugin" "$REPOCONFIG/$DEFAULT_ARCH"
}

install_yast() {
  if [ ! "$REPOCONFIG" ]; then
    return 0
  fi

  # We defer adding the key to later. See comment in the cron job.

  # Ideally, we would run: zypper addrepo -t YUM -f \
  # "$REPOCONFIG/$DEFAULT_ARCH" "google-talkplugin"
  # but that does not work when zypper is running.
  if [ -d "/etc/zypp/repos.d" ]; then
cat > "$ZYPPER_REPO_FILE" << REPOCONTENT
[google-talkplugin]
name=google-talkplugin
enabled=1
autorefresh=1
baseurl=$REPOCONFIG/$DEFAULT_ARCH
type=rpm-md
keeppackages=0
REPOCONTENT
  fi
}

# Check if the automatic repository configuration is done, so we know when to
# stop trying.
verify_install() {
  # It's probably enough to see that the repo configs have been created. If they
  # aren't configured properly, update_bad_repo should catch that when it's run.
  case $1 in
  "yum")
    [ -f "$YUM_REPO_FILE" ]
    ;;
  "yast")
    [ -f "$ZYPPER_REPO_FILE" ]
    ;;
  "urpmi")
    urpmq --list-url | grep -q -s "\bgoogle-talkplugin\b"
    ;;
  esac
}

# Update the Google repository if it's not set correctly.
update_bad_repo() {
  if [ ! "$REPOCONFIG" ]; then
    return 0
  fi

  determine_rpm_package_manager

  case $PACKAGEMANAGER in
  "yum")
    update_repo_file "$YUM_REPO_FILE"
    ;;
  "yast")
    update_repo_file "$ZYPPER_REPO_FILE"
    ;;
  "urpmi")
    update_urpmi_cfg
    ;;
  esac
}

update_repo_file() {
  REPO_FILE="$1"

  # Don't do anything if the file isn't there, since that probably means the
  # user disabled it.
  if [ ! -r "$REPO_FILE" ]; then
    return 0
  fi

  # Check if the correct repository configuration is in there.
  REPOMATCH=$(grep "^baseurl=$REPOCONFIG/$DEFAULT_ARCH" "$REPO_FILE" \
    2>/dev/null)
  # If it's there, nothing to do
  if [ "$REPOMATCH" ]; then
    return 0
  fi

  # Check if it's there but disabled by commenting out (as opposed to using the
  # 'enabled' setting).
  MATCH_DISABLED=$(grep "^[[:space:]]*#.*baseurl=$REPOCONFIG/$DEFAULT_ARCH" \
    "$REPO_FILE" 2>/dev/null)
  if [ "$MATCH_DISABLED" ]; then
    # It's OK for it to be disabled, as long as nothing bogus is enabled in its
    # place.
    ACTIVECONFIGS=$(grep "^baseurl=.*" "$REPO_FILE" 2>/dev/null)
    if [ ! "$ACTIVECONFIGS" ]; then
      return 0
    fi
  fi

  # If we get here, the correct repository wasn't found, or something else is
  # active, so fix it. This assumes there is a 'baseurl' setting, but if not,
  # then that's just another way of disabling, so we won't try to add it.
  sed -i -e "s,^baseurl=.*,baseurl=$REPOCONFIG/$DEFAULT_ARCH," "$REPO_FILE"
}

update_urpmi_cfg() {
  REPOCFG=$(urpmq --list-url | grep "\bgoogle-talkplugin\b")
  if [ ! "$REPOCFG" ]; then
    # Don't do anything if the repo isn't there, since that probably means the
    # user deleted it.
    return 0
  fi

  # See if it's the right repo URL
  URLMATCH=$(echo "$REPOCFG" | grep "\b$REPOCONFIG/$DEFAULT_ARCH\b")
  # If so, nothing to do
  if [ "$REPOMATCH" ]; then
    return 0
  fi

  # Looks like it's the wrong URL, so recreate it.
  urpmi.removemedia "google-talkplugin" && \
    urpmi.addmedia --update "google-talkplugin" "$REPOCONFIG/$DEFAULT_ARCH"
}

# We only remove the repository configuration during a purge. Since RPM has
# no equivalent to dpkg --purge, the code below is actually never used. We
# keep it only for reference purposes, should we ever need it.
#
#remove_yum() {
#  rm -f "$YUM_REPO_FILE"
#}
#
#remove_urpmi() {
#  # Ideally, we would run: urpmi.removemedia "google-talkplugin"
#  # but that does not work when urpmi is running.
#  # Sentinel comment text does not work either because urpmi.update removes
#  # all comments. So we just delete the entry that matches what we originally
#  # inserted. If such an entry was added manually, that's tough luck.
#  if [ -f "$URPMI_REPO_FILE" ]; then
#    sed -i '\_^google-talkplugin $REPOCONFIG/$DEFAULT_ARCH {$_,/^}$/d' "$URPMI_REPO_FILE"
#  fi
#}
#
#remove_yast() {
#  # Ideally, we would run: zypper removerepo "google-talkplugin"
#  # but that does not work when zypper is running.
#  rm -f /etc/zypp/repos.d/google-talkplugin.repo
#}

get_lib_dir() {
  if [ "$DEFAULT_ARCH" = "i386" ]; then
    LIBDIR=lib
  elif [ "$DEFAULT_ARCH" = "x86_64" ]; then
    LIBDIR=lib64
  else
    echo Unknown CPU Architecture: "$DEFAULT_ARCH"
    exit 1
  fi
}

NSS_FILES="libnspr4.so.0d libplds4.so.0d libplc4.so.0d libssl3.so.1d \
    libnss3.so.1d libsmime3.so.1d libnssutil3.so.1d"

add_nss_symlinks() {
  get_lib_dir
  for f in $NSS_FILES
  do
    target=$(echo $f | sed 's/\.[01]d$//')
    if [ -f "/$LIBDIR/$target" ]; then
      ln -snf "/$LIBDIR/$target" "/$f"
    elif [ -f "/usr/$LIBDIR/$target" ]; then
      ln -snf "/usr/$LIBDIR/$target" "/$f"
    else
      echo $f not found in "/$LIBDIR/$target" or "/usr/$LIBDIR/$target".
      exit 1
    fi
  done
}

remove_nss_symlinks() {
  for f in $NSS_FILES
  do
    rm -rf "/$f"
  done
}

LIBBZ2_1=libbz2.so.1
LIBBZ2_1_0=libbz2.so.1.0

add_bzip2_symlinks() {
  get_lib_dir
  if [ -f "/$LIBDIR/$LIBBZ2_1_0" -o -f "/usr/$LIBDIR/$LIBBZ2_1_0" ]; then
    return 0
  fi

  # Most RPM distros do not provide libbz2.so.1.0, i.e.
  # https://bugzilla.redhat.com/show_bug.cgi?id=461863
  # so we create a symlink and point it to libbz2.so.1.
  # This is technically wrong, but it'll work since we do
  # not anticipate a new version of bzip2 with a different
  # minor version number anytime soon.
  if [ -f "/$LIBDIR/$LIBBZ2_1" -a ! -f "/$LIBDIR/$LIBBZ2_1_0" ]; then
    ln -snf "/$LIBDIR/$LIBBZ2_1" "/$LIBBZ2_1_0"
  elif [ -f "/usr/$LIBDIR/$LIBBZ2_1" -a ! -f "/usr/$LIBDIR/$LIBBZ2_1_0" ];
  then
    ln -snf "/usr/$LIBDIR/$LIBBZ2_1" "/$LIBBZ2_1_0"
  else
    echo "$LIBBZ2_1" not found in "$LIBDIR" or "/usr/$LIBDIR".
    exit 1
  fi
}

remove_bzip2_symlinks() {
  rm -rf "/$LIBBZ2_1_0"
}


DEFAULTS_FILE="/etc/default/google-talkplugin"
if [ ! -e "$DEFAULTS_FILE" ]; then
  echo 'repo_add_once="true"' > "$DEFAULTS_FILE"
fi

. "$DEFAULTS_FILE"

if [ "$repo_add_once" = "true" ]; then
  determine_rpm_package_manager

  case $PACKAGEMANAGER in
  "yum")
    install_yum
    ;;
  "urpmi")
    install_urpmi
    ;;
  "yast")
    install_yast
    ;;
  esac
fi

# Some package managers have locks that prevent everything from being
# configured at install time, so wait a bit then kick the cron job to do
# whatever is left. Probably the db will be unlocked by then, but if not, the
# cron job will keep retrying.
# Do this with 'at' instead of a backgrounded shell because zypper waits on all
# sub-shells to finish before it finishes, which is exactly the opposite of
# what we want here. Also preemptively start atd because for some reason it's
# not always running, which kind of defeats the purpose of having 'at' as a
# required LSB command.
service atd start
echo "sh /etc/cron.daily/google-talkplugin" | at now + 2 minute
exit 0


#------------------------------------------------------------------------------
#   Pre uninstallation script
#------------------------------------------------------------------------------


%preun

exit 0

#------------------------------------------------------------------------------
#   Post uninstallation script
#------------------------------------------------------------------------------


%postun

exit 0


%files
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /etc/cron.daily
%verify(md5 size link user group mtime mode rdev) %attr(-,root,root) /etc/cron.daily/google-talkplugin
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin
%verify(md5 size link user group mtime mode rdev) %attr(0755L,root,root) /opt/google/talkplugin/GoogleTalkPlugin
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/cron
%verify(md5 size link user group mtime mode rdev) %attr(0755L,root,root) /opt/google/talkplugin/cron/google-talkplugin
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/data
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/data/LMprec_508.emd
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/data/MFTprec_120.emd
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/data/SFTprec_120.emd
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/lib
%verify(md5 size link user group mtime mode rdev) %attr(0755L,root,root) /opt/google/talkplugin/lib/libCg.so
%verify(md5 size link user group mtime mode rdev) %attr(0755L,root,root) /opt/google/talkplugin/lib/libCgGL.so
%verify(md5 size link user group mtime mode rdev) %attr(0755L,root,root) /opt/google/talkplugin/libnpgoogletalk64.so
%verify(md5 size link user group mtime mode rdev) %attr(0755L,root,root) /opt/google/talkplugin/libnpgtpo3dautoplugin.so
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/ar
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/ar/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/ar/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/bg
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/bg/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/bg/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/bn
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/bn/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/bn/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/ca
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/ca/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/ca/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/cs
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/cs/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/cs/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/da
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/da/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/da/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/de
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/de/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/de/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/el
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/el/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/el/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/en
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/en-GB
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/en-GB/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/en-GB/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/en/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/en/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/es
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/es-419
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/es-419/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/es-419/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/es/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/es/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/et
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/et/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/et/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/fa
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/fa/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/fa/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/fi
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/fi/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/fi/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/fil
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/fil/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/fil/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/fr
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/fr/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/fr/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/gu
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/gu/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/gu/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/hi
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/hi/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/hi/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/hr
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/hr/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/hr/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/hu
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/hu/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/hu/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/id
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/id/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/id/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/is
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/is/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/is/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/it
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/it/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/it/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/iw
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/iw/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/iw/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/ja
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/ja/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/ja/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/kn
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/kn/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/kn/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/ko
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/ko/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/ko/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/lt
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/lt/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/lt/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/lv
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/lv/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/lv/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/ml
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/ml/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/ml/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/mr
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/mr/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/mr/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/ms
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/ms/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/ms/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/nl
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/nl/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/nl/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/no
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/no/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/no/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/or
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/or/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/or/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/pl
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/pl/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/pl/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/pt-BR
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/pt-BR/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/pt-BR/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/pt-PT
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/pt-PT/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/pt-PT/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/ro
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/ro/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/ro/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/ru
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/ru/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/ru/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/sk
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/sk/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/sk/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/sl
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/sl/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/sl/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/sr
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/sr/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/sr/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/sv
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/sv/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/sv/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/ta
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/ta/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/ta/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/te
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/te/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/te/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/th
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/th/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/th/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/tl
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/tl/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/tl/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/tr
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/tr/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/tr/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/uk
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/uk/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/uk/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/ur
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/ur/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/ur/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/vi
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/vi/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/vi/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/zh-CN
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/zh-CN/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/zh-CN/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/zh-TW
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /opt/google/talkplugin/locale/zh-TW/LC_MESSAGES
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/locale/zh-TW/LC_MESSAGES/windowpicker.mo
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/openssl.txt
%verify(md5 size link user group mtime mode rdev) %attr(0644L,root,root) /opt/google/talkplugin/windowpicker.glade
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /usr/lib64/firefox
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /usr/lib64/firefox/plugins
%verify(md5 size link user group mtime mode rdev) %attr(-,root,root) /usr/lib64/firefox/plugins/libnpgoogletalk64.so
%verify(md5 size link user group mtime mode rdev) %attr(-,root,root) /usr/lib64/firefox/plugins/libnpgtpo3dautoplugin.so
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /usr/lib64/iceape
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /usr/lib64/iceape/plugins
%verify(md5 size link user group mtime mode rdev) %attr(-,root,root) /usr/lib64/iceape/plugins/libnpgoogletalk64.so
%verify(md5 size link user group mtime mode rdev) %attr(-,root,root) /usr/lib64/iceape/plugins/libnpgtpo3dautoplugin.so
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /usr/lib64/iceweasel
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /usr/lib64/iceweasel/plugins
%verify(md5 size link user group mtime mode rdev) %attr(-,root,root) /usr/lib64/iceweasel/plugins/libnpgoogletalk64.so
%verify(md5 size link user group mtime mode rdev) %attr(-,root,root) /usr/lib64/iceweasel/plugins/libnpgtpo3dautoplugin.so
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /usr/lib64/midbrowser
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /usr/lib64/midbrowser/plugins
%verify(md5 size link user group mtime mode rdev) %attr(-,root,root) /usr/lib64/midbrowser/plugins/libnpgoogletalk64.so
%verify(md5 size link user group mtime mode rdev) %attr(-,root,root) /usr/lib64/midbrowser/plugins/libnpgtpo3dautoplugin.so
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /usr/lib64/mozilla
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /usr/lib64/mozilla/plugins
%verify(md5 size link user group mtime mode rdev) %attr(-,root,root) /usr/lib64/mozilla/plugins/libnpgoogletalk64.so
%verify(md5 size link user group mtime mode rdev) %attr(-,root,root) /usr/lib64/mozilla/plugins/libnpgtpo3dautoplugin.so
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /usr/lib64/xulrunner
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /usr/lib64/xulrunner-addons
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /usr/lib64/xulrunner-addons/plugins
%verify(md5 size link user group mtime mode rdev) %attr(-,root,root) /usr/lib64/xulrunner-addons/plugins/libnpgoogletalk64.so
%verify(md5 size link user group mtime mode rdev) %attr(-,root,root) /usr/lib64/xulrunner-addons/plugins/libnpgtpo3dautoplugin.so
%verify(md5 size link user group mtime mode rdev) %dir %attr(0755L,root,root) /usr/lib64/xulrunner/plugins
%verify(md5 size link user group mtime mode rdev) %attr(-,root,root) /usr/lib64/xulrunner/plugins/libnpgoogletalk64.so
%verify(md5 size link user group mtime mode rdev) %attr(-,root,root) /usr/lib64/xulrunner/plugins/libnpgtpo3dautoplugin.so

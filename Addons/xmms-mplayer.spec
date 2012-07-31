Name:          xmms-mplayer
Summary:       MPlayer plugin for XMMS
Version:       0.5
Release:       2%{?dist}
License:       GPL+
Group:         Applications/Multimedia
URL:           http://xmmsmplayer.sourceforge.net
Source:        http://downloads.sourceforge.net/xmmsmplayer/xmmsmplayer-%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libtool 
BuildRequires: xmms-devel
Requires:      mplayer
Requires:      xmms

%description
Xmms-MPlayer is an input plugin for XMMS that allows you to play all audio and
video files in XMMS. Thus, allowing you to use XMMS as a playlist frontend for
MPlayer. This project aims at merely being a connecting link between XMMS and 
MPlayer. It does not intend to get involved into any processing of video files,
all that is left to MPlayer.

%prep
%setup -q -n xmmsmplayer-%{version}

# To compile the shared version of the library:
sed -i 's|XMMS_LIBS=\(.*\)|XMMS_LIBS="-L%{_libdir} \1"|' aclocal.m4
cat /dev/null > acinclude.m4
aclocal
autoconf
libtoolize --force

# Check if there's anything new:
[ -s NEWS ] && exit 1

%build
%configure 
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"

# Kill .la files
rm -f %{buildroot}%{_libdir}/xmms/Input/*.la

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%{_libdir}/xmms/Input/libxmmsmplayer.*

%changelog
* Thu May 21 2009 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.5-2
- Use "install -p".
- Add [ -s NEWS ] && exit 1

* Thu Apr 02 2009 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.5-1
- Initial build.

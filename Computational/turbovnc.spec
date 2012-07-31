Summary:   A highly-optimized version of VNC that can be used with real-time video applications
Name:      turbovnc
Version:   1.0.2
Release:   20110808.1%{?dist}
URL:       http://www.virtualgl.org
Source0: http://prdownloads.sourceforge.net/virtualgl/%{name}-%{version}.tar.gz
License:   GPL
Group:     User Interface/Desktops
Requires:  bash >= 2.0
Requires:  /sbin/chkconfig /etc/init.d
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: /usr/bin/perl libjpeg-turbo-static
BuildRequires: zlib-devel libXext-devel libX11-devel
BuildRequires: libX11-devel automake autoconf libtool
BuildRequires: libXi-devel xorg-x11-xtrans-devel xorg-x11-util-macros
BuildRequires: libXtst-devel libdrm-devel libXt-devel libXfont-devel libxkbfile-devel
BuildRequires: openssl-devel libXinerama-devel libXdmcp-devel libXaw-devel
Buildrequires: imake rsync pam-devel freetype-devel desktop-file-utils
#libpciaccess-devel  
#mesa-libGL-devel  
#ImageMagick  
#java-1.5.0-gcj-devel  
#gnutls-devel  
#nasm  
#xorg-x11-server-source >= 1.10.4 pixman-devel


%description
Virtual Network Computing (VNC) is a remote display system which
allows you to view a computing 'desktop' environment not only on the
machine where it is running, but from anywhere on the Internet and
from a wide variety of machine architectures.  TurboVNC is a sleek and
fast VNC distribution, containing a high-performance implementation of
Tight encoding designed to work in conjunction with VirtualGL.

%prep
%setup -q -n vnc/vnc_unixsrc

%build
./configure --prefix=/opt/TurboVNC --sysconfdir=/etc --mandir=/opt/TurboVNC/man
make DESTDIR=%{buildroot}
make xserver DESTDIR=%{buildroot}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} sysconfdir=/etc
make xserver-install DESTDIR=%{buildroot} sysconfdir=/etc

mkdir -p %{buildroot}/etc/init.d

cat vncserver.init   | \
sed -e 's@vncserver :${display\%\%:@/opt/TurboVNC/bin/vncserver :${display\%\%:@g' | \
sed -e 's@vncserver -kill :${display\%\%:@/opt/TurboVNC/bin/vncserver -kill :${display\%\%:@g' \
 > %{buildroot}/etc/init.d/tvncserver
chmod 755 %{buildroot}/etc/init.d/tvncserver

mkdir -p %{buildroot}/etc/sysconfig
install -m 644 tvncservers %{buildroot}/etc/sysconfig/tvncservers

mkdir -p %{buildroot}/usr/share/applications
cat > %{buildroot}/usr/share/applications/tvncviewer.desktop << EOF
[Desktop Entry]
Name=TurboVNC Viewer
Comment=TurboVNC client application
Exec=/opt/TurboVNC/bin/vncviewer
Terminal=0
Type=Application
Categories=Application;Utility;X-Red-Hat-Extra;
EOF

chmod 644 LICENCE.TXT ../TurboVNC-ChangeLog.txt ../vnc_docs/LICEN*.txt ../vnc_docs/*.html ../vnc_docs/*.png ../vnc_docs/*.css

%clean
rm -rf %{buildroot}

%post
if [ "$1" = 1 ]; then
  if [ -f /etc/redhat-release ]; then /sbin/chkconfig --add tvncserver; fi
fi

%preun
if [ "$1" = 0 ]; then
  /etc/init.d/tvncserver stop >/dev/null 2>&1
  if [ -f /etc/redhat-release ]; then /sbin/chkconfig --del tvncserver; fi
fi

%postun
if [ "$1" -ge "1" ]; then
  /etc/init.d/tvncserver condrestart >/dev/null 2>&1
fi

%files
%defattr(-,root,root)
%attr(0755,root,root) %config /etc/init.d/tvncserver
%config(noreplace) /etc/sysconfig/tvncservers
%config(noreplace) /etc/turbovncserver.conf
%config(noreplace) /etc/turbovncserver-auth.conf
%doc LICENCE.TXT  ../TurboVNC-ChangeLog.txt ../vnc_docs/LICEN*.txt ../vnc_docs/*.html ../vnc_docs/*.png ../vnc_docs/*.css

%dir /opt/TurboVNC
%dir /opt/TurboVNC/bin
%dir /opt/TurboVNC/man
%dir /opt/TurboVNC/man/man1
%dir /opt/TurboVNC/vnc
%dir /opt/TurboVNC/vnc/classes

/opt/TurboVNC/bin/vncviewer
%config(noreplace) /usr/share/applications/tvncviewer.desktop
/opt/TurboVNC/man/man1/vncviewer.1*
/opt/TurboVNC/bin/Xvnc
/opt/TurboVNC/bin/vncserver
/opt/TurboVNC/bin/vncpasswd
/opt/TurboVNC/bin/vncconnect
/opt/TurboVNC/bin/autocutsel
/opt/TurboVNC/vnc/classes/index.vnc
/opt/TurboVNC/vnc/classes/VncViewer.jar
/opt/TurboVNC/vnc/classes/README
/opt/TurboVNC/man/man1/Xvnc.1*
/opt/TurboVNC/man/man1/Xserver.1*
/opt/TurboVNC/man/man1/vncserver.1*
/opt/TurboVNC/man/man1/vncconnect.1*
/opt/TurboVNC/man/man1/vncpasswd.1*

%changelog

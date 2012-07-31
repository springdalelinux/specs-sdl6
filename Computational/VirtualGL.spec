# This is a hack to prevent the RPM from depending on libGLcore.so.1 and
# libnvidia-tls.so.1 if it was built on a system that has the NVidia
# drivers installed.  The custom find-requires script is created during
# install and removed during clean

#define __find_requires %{_tmppath}/%{name}-%{version}-%{release}-find-requires

# Prefix in which essential server/client binaries should be stored
%define sysprefix /usr

# Prefix in which everything else (except docs) should be stored
%define prefix /opt/VirtualGL

%define usesysdir %(test ! "%{prefix}" = "%{sysprefix}" && echo 1 || echo 0)

%define docsymlink %(test ! "%{prefix}" = "`dirname %{_defaultdocdir}`" -a 1 = 1 && echo 1 || echo 0)

Summary: A toolkit for displaying OpenGL applications to thin clients
Name: VirtualGL
Version: 2.3
Vendor: The VirtualGL Project
URL: http://www.virtualgl.org
Group: Applications/Graphics
Source0: http://prdownloads.sourceforge.net/virtualgl/VirtualGL-%{version}.tar.gz
Release: 20111213.1%{?dist}
License: wxWindows Library License v3.1
BuildRoot: %{_tmppath}/%{name}-buildroot-%{version}-%{release}
BuildRequires: cmake28 libX11-devel libjpeg-turbo-static
BuildRequires: mesa-libGL-devel mesa-libGLU-devel libXext-devel libXv-devel
Requires: /sbin/ldconfig
Requires: %{name}-libs = %{version}-%{release}
Provides: %{name} = %{version}-%{release}

%description
VirtualGL is a toolkit that allows most Unix/Linux OpenGL applications to be
remotely displayed with hardware 3D acceleration to thin clients, regardless
of whether the clients have 3D capabilities, and regardless of the size of the
3D data being rendered or the speed of the network.

Using the vglrun script, the VirtualGL "faker" is loaded into an OpenGL
application at run time.  The faker then intercepts a handful of GLX calls,
which it reroutes to the server's X display (the "3D X Server", which
presumably has a 3D accelerator attached.)  The GLX commands are also
dynamically modified such that all rendering is redirected into a Pbuffer
instead of a window.  As each frame is rendered by the application, the faker
reads back the pixels from the 3D accelerator and sends them to the
"2D X Server" for compositing into the appropriate X Window.

VirtualGL can be used to give hardware-accelerated 3D capabilities to VNC or
other X proxies that either lack OpenGL support or provide it through software
rendering.  In a LAN environment, VGL can also be used with its built-in
high-performance image transport, which sends the rendered 3D images to a
remote client (vglclient) for compositing on a remote X server.  VirtualGL
also supports image transport plugins, allowing the rendered 3D images to be
sent or captured using other mechanisms.

VirtualGL is based upon ideas presented in various academic papers on
this topic, including "A Generic Solution for Hardware-Accelerated Remote
Visualization" (Stegmaier, Magallon, Ertl 2002) and "A Framework for
Interactive Hardware Accelerated Remote 3D-Visualization" (Engel, Sommer,
Ertl 2000.)

%package libs
Summary:        VirtualGL libraries
Group:          Applications/Graphics

%description libs
Libraries for VirtualGL - separated so that we can install the 32bit ones on x86_64 machines.

%prep
%setup -q

%build
cmake -G"Unix Makefiles" -DCMAKE_INSTALL_PREFIX=%{prefix} -DVGL_USEXV=ON -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_VERBOSE_MAKEFILE=1 \
	-DTJPEG_LIBRARY=%{_libdir}/libturbojpeg.a .
make

%install

rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%ifarch x86_64
mv $RPM_BUILD_ROOT/%{prefix}/bin/glxspheres $RPM_BUILD_ROOT/%{prefix}/bin/glxspheres64
%endif

%if %{usesysdir}

mkdir -p $RPM_BUILD_ROOT/%{sysprefix}/bin
%ifarch x86_64
mv $RPM_BUILD_ROOT/%{prefix}/lib $RPM_BUILD_ROOT/%{sysprefix}/lib64
%else
mv $RPM_BUILD_ROOT/%{prefix}/lib $RPM_BUILD_ROOT/%{sysprefix}/lib
%endif

for i in vglclient vglconfig vglconnect vglgenkey vgllogin vglrun vglserver_config; do
	mv $RPM_BUILD_ROOT/%{prefix}/bin/$i $RPM_BUILD_ROOT/%{sysprefix}/bin/
done

mkdir -p $RPM_BUILD_ROOT/%{sysprefix}/include
for i in rr.h rrtransport.h; do
	mv $RPM_BUILD_ROOT/%{prefix}/include/$i $RPM_BUILD_ROOT/%{sysprefix}/include/
	ln -fs %{sysprefix}/include/$i $RPM_BUILD_ROOT/%{prefix}/include/$i
done

pushd $RPM_BUILD_ROOT/%{sysprefix}/bin
for i in *; do
	ln -fs %{sysprefix}/bin/$i $RPM_BUILD_ROOT/%{prefix}/bin/; done
popd

%else

%ifarch x86_64
mv $RPM_BUILD_ROOT/%{prefix}/lib $RPM_BUILD_ROOT/%{prefix}/lib64
%endif

%endif

%ifarch x86_64
rm $RPM_BUILD_ROOT/%{prefix}/fakelib/64/libGL.so
ln -fs %{sysprefix}/lib64/librrfaker.so $RPM_BUILD_ROOT/%{prefix}/fakelib/64/libGL.so
%else
rm $RPM_BUILD_ROOT/%{prefix}/fakelib/libGL.so
ln -fs %{sysprefix}/lib/librrfaker.so $RPM_BUILD_ROOT/%{prefix}/fakelib/libGL.so
%endif

mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}
mv $RPM_BUILD_ROOT/%{prefix}/doc $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}
%if %{docsymlink}
ln -fs %{_defaultdocdir}/%{name}-%{version} $RPM_BUILD_ROOT/%{prefix}/doc
%endif

echo '/usr/lib/rpm/find-requires|grep -v libGLcore|grep -v libnvidia-tls' >%{_tmppath}/%{name}-%{version}-%{release}-find-requires
chmod 755 %{_tmppath}/%{name}-%{version}-%{release}-find-requires

%clean
rm -rf $RPM_BUILD_ROOT
rm %{_tmppath}/%{name}-%{version}-%{release}-find-requires

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files -n %{name}
%defattr(-,root,root)
%dir %{_defaultdocdir}/%{name}-%{version}
%doc %{_defaultdocdir}/%{name}-%{version}/*

%dir %{prefix}

%dir %{prefix}/bin
%{prefix}/bin/tcbench
%{prefix}/bin/nettest
%{prefix}/bin/cpustat
%{prefix}/bin/glxinfo
%{prefix}/bin/vglclient
%{prefix}/bin/vglconfig
%{prefix}/bin/vglconnect
%{prefix}/bin/vglgenkey
%{prefix}/bin/vgllogin
%{prefix}/bin/vglserver_config
%{prefix}/bin/vglrun
%ifarch x86_64
 %{prefix}/bin/glxspheres64
%else
 %{prefix}/bin/glxspheres
%endif
%if %{usesysdir}
 %{sysprefix}/bin/vglclient
 %{sysprefix}/bin/vglconfig
 %{sysprefix}/bin/vglconnect
 %{sysprefix}/bin/vgllogin
 %{sysprefix}/bin/vglrun
 %{sysprefix}/bin/vglgenkey
 %{sysprefix}/bin/vglserver_config
%endif

%if %{docsymlink}
 %{prefix}/doc
%endif

%dir %{prefix}/fakelib
%ifarch x86_64
 %dir %{prefix}/fakelib/64
 %{prefix}/fakelib/64/libGL.so
%else
 %{prefix}/fakelib/libGL.so
%endif

%dir %{prefix}/include
%{prefix}/include/rrtransport.h
%{prefix}/include/rr.h
%if %{usesysdir}
 %{sysprefix}/include/rrtransport.h
 %{sysprefix}/include/rr.h
%endif

%files libs
%defattr(-,root,root)
%ifarch x86_64
 %{sysprefix}/lib64/librrfaker.so
 %{sysprefix}/lib64/libdlfaker.so
 %{sysprefix}/lib64/libgefaker.so
 %if %{usesysdir}
 %else
  %dir %{prefix}/lib64
 %endif
%else
 %{sysprefix}/lib/librrfaker.so
 %{sysprefix}/lib/libdlfaker.so
 %{sysprefix}/lib/libgefaker.so
 %if %{usesysdir}
 %else
  %dir %{prefix}/lib
 %endif
%endif

%changelog

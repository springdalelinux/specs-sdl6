# Disable OSMesa builds for now - see Bug 744434
%bcond_with OSMesa
%bcond_without java

%{!?python_sitearch:%global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: The Visualization Toolkit - A high level 3D visualization library
Name: vtk
Version: 5.8.0
Release: 1%{?dist}
# This is a variant BSD license, a cross between BSD and ZLIB.
# For all intents, it has the same rights and restrictions as BSD.
# http://fedoraproject.org/wiki/Licensing/BSD#VTKBSDVariant
License: BSD
Group: System Environment/Libraries
Source: http://www.vtk.org/files/release/5.8/%{name}-%{version}.tar.gz
Patch1: vtk-5.2.0-gcc43.patch
# Use system libraries
# http://public.kitware.com/Bug/view.php?id=11823
Patch5: vtk-5.6.1-system.patch

URL: http://vtk.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: cmake28
BuildRequires: gcc-c++
#%{?with_java:BuildRequires: gcc-java, libgcj-devel, java-devel}
%{?with_java:BuildRequires: java-devel}
BuildRequires: libX11-devel, libXt-devel, libXext-devel
BuildRequires: libICE-devel, libGL-devel
%{?with_OSMesa:BuildRequires: mesa-libOSMesa-devel}
BuildRequires: tk-devel, tcl-devel
BuildRequires: python-devel
BuildRequires: expat-devel, freetype-devel, libjpeg-devel, libpng-devel
BuildRequires: gl2ps-devel
BuildRequires: libtiff-devel, zlib-devel
BuildRequires: libxml2-devel
BuildRequires: qt4-devel
BuildRequires: qtwebkit-devel
BuildRequires: chrpath
BuildRequires: doxygen, graphviz
BuildRequires: gnuplot
BuildRequires: boost-devel
BuildRequires: hdf5-devel
BuildRequires: libtheora-devel
BuildRequires: mysql-devel
BuildRequires: postgresql-devel
BuildRequires: wget
BuildRequires: %{_includedir}/Xm
%{!?with_java:Conflicts: vtk-java}

%description
VTK is an open-source software system for image processing, 3D
graphics, volume rendering and visualization. VTK includes many
advanced algorithms (e.g., surface reconstruction, implicit modelling,
decimation) and rendering techniques (e.g., hardware-accelerated
volume rendering, LOD control).

%package devel
Summary: VTK header files for building C++ code
Requires: vtk = %{version}-%{release}
%{?with_OSMesa:Requires: mesa-libOSMesa-devel}
Requires: gl2ps-devel
Requires: expat-devel, libjpeg-devel, libpng-devel
Requires: libogg-devel
Requires: libtheora-devel
Requires: libtiff-devel
Requires: postgresql-devel
Requires: mysql-devel
Requires: qt4-devel
Group: Development/Libraries

%description devel 
This provides the VTK header files required to compile C++ programs that
use VTK to do 3D visualisation.

%package tcl
Summary: Tcl bindings for VTK
Requires: vtk = %{version}-%{release}
Group: System Environment/Libraries

%description tcl
tcl bindings for VTK

%package python
Summary: Python bindings for VTK
Requires: vtk = %{version}-%{release}
Group: System Environment/Libraries

%description python
python bindings for VTK

%if %{with java}
%package java
Summary: Java bindings for VTK
Requires: vtk = %{version}-%{release}
Group: System Environment/Libraries

%description java
Java bindings for VTK
%endif

%package qt
Summary: Qt bindings for VTK
Requires: vtk = %{version}-%{release}
Group: System Environment/Libraries

%description qt
Qt bindings for VTK

%package testing
Summary: Testing programs for VTK
Requires: vtk = %{version}-%{release}, vtkdata = %{version}
Group: Applications/Engineering

%description testing
Testing programs for VTK

%package examples
Summary: Examples for VTK
Requires: vtk = %{version}-%{release}, vtkdata = %{version}
Group: Applications/Engineering

%description examples
This package contains many well-commented examples showing how to use
VTK. Examples are available in the C++, Tcl, Python and Java
programming languages.


%prep
%setup -q -n VTK
%patch1 -p1 -b .gcc43
%patch5 -p1 -b .system

# Replace relative path ../../../VTKData with %{_datadir}/vtkdata-%{version}
# otherwise it will break on symlinks.
grep -rl '\.\./\.\./\.\./\.\./VTKData' . | xargs \
  perl -pi -e's,\.\./\.\./\.\./\.\./VTKData,%{_datadir}/vtkdata-%{version},g'

# Save an unbuilt copy of the Example's sources for %doc
mkdir vtk-examples
cp -a Examples vtk-examples
# Don't ship Win32 examples
rm -rf vtk-examples/Examples/GUI/Win32
find vtk-examples -type f | xargs chmod -R a-x

%build
export CFLAGS="%{optflags} -D_UNICODE"
export CXXFLAGS="%{optflags} -D_UNICODE"
%if %{with java}
export JAVA_HOME=/usr/lib/jvm/java
%endif

mkdir build
pushd build
%{cmake} .. \
 -DBUILD_DOCUMENTATION:BOOL=ON \
 -DBUILD_EXAMPLES:BOOL=ON \
 -DBUILD_TESTING:BOOL=ON \
 -DVTK_INSTALL_INCLUDE_DIR:PATH=/include/vtk \
 -DVTK_INSTALL_LIB_DIR:PATH=/%{_lib}/vtk \
 -DVTK_INSTALL_QT_DIR=/%{_lib}/qt4/plugins/designer \
 -DTK_INTERNAL_PATH:PATH=/usr/include/tk-private/generic \
%if %{with OSMesa}
 -DVTK_OPENGL_HAS_OSMESA:BOOL=ON \
%endif
 -DVTK_PYTHON_SETUP_ARGS="--prefix=/usr --root=%{buildroot}" \
 -DVTK_WRAP_PYTHON:BOOL=ON \
%if %{with java}
 -DVTK_WRAP_JAVA:BOOL=ON \
 -DJAVA_INCLUDE_PATH:PATH=$JAVA_HOME/include \
 -DJAVA_INCLUDE_PATH2:PATH=$JAVA_HOME/include/linux \
 -DJAVA_AWT_INCLUDE_PATH:PATH=$JAVA_HOME/include \
%else
 -DVTK_WRAP_JAVA:BOOL=OFF \
%endif
 -DVTK_WRAP_TCL:BOOL=ON \
 -DVTK_USE_BOOST:BOOL=ON \
 -DVTK_USE_GL2PS:BOOL=ON \
 -DVTK_USE_GUISUPPORT:BOOL=ON \
 -DVTK_USE_MYSQL=ON \
 -DVTK_USE_OGGTHEORA_ENCODER=ON \
 -DVTK_USE_PARALLEL:BOOL=ON \
 -DVTK_USE_POSTGRES=ON \
 -DVTK_USE_SYSTEM_LIBRARIES=ON \
 -DVTK_USE_SYSTEM_LIBPROJ4=OFF \
 -DVTK_USE_QVTK=ON \
 -DVTK_USE_QT=ON \
 -DVTK_USE_TEXT_ANALYSIS=ON

# Not working, see http://public.kitware.com/Bug/view.php?id=11978
# -DVTK_USE_ODBC=ON \
# Not working, see http://public.kitware.com/Bug/view.php?id=10779
# -DVTK_USE_GNU_R:BOOL=ON \
# Commented old flags in case we'd like to reactive some of them
# -DVTK_USE_DISPLAY:BOOL=OFF \ # This prevents building of graphics tests
# -DVTK_USE_MPI:BOOL=ON \

# Got intermittent build error with -j
make #%{?_smp_mflags}

# Remove executable bits from sources (some of which are generated)
find . -name \*.c -or -name \*.cxx -or -name \*.h -or -name \*.hxx -or \
       -name \*.gif | xargs chmod -x

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
pushd build
make install DESTDIR=%{buildroot}

if [ "%{_lib}" != lib -a "`ls %{buildroot}%{_prefix}/lib/*`" != "" ]; then
  mkdir -p %{buildroot}%{_libdir}
  mv %{buildroot}%{_prefix}/lib/* %{buildroot}%{_libdir}/
fi
mv %{buildroot}%{_libdir}/vtk/lib*.so* %{buildroot}%{_libdir}/

# Gather list of non-python/tcl libraries
ls %{buildroot}%{_libdir}/*.so.* \
  | grep -Ev '(Java|QVTK|PythonD|TCL)' | sed -e's,^%{buildroot},,' > libs.list

# List of executable utilities
cat > utils.list << EOF
vtkEncodeString
lproj
EOF

# List of executable examples
cat > examples.list << EOF
HierarchicalBoxPipeline
MultiBlock
Arrays
Cube
RGrid
SGrid
Medical1
Medical2
Medical3
finance
AmbientSpheres
Cylinder
DiffuseSpheres
SpecularSpheres
Cone
Cone2
Cone3
Cone4
Cone5
Cone6
EOF

# List of executable test binaries
cat > testing.list << EOF
CommonCxxTests
TestCxxFeatures
TestInstantiator
FilteringCxxTests
GraphicsCxxTests
GenericFilteringCxxTests
ImagingCxxTests
IOCxxTests
RenderingCxxTests
VTKBenchMark
VolumeRenderingCxxTests
WidgetsCxxTests
SocketClient
SocketServer
EOF

# Install utils/examples/testing, too
for filelist in utils.list examples.list testing.list; do
  for file in `cat $filelist`; do
    install -p bin/$file %{buildroot}%{_bindir}
  done
  perl -pi -e's,^,%{_bindir}/,' $filelist
done

# Remove any remnants of rpaths
for file in `cat utils.list examples.list testing.list`; do
  chrpath -d %{buildroot}$file
done

# Main package contains utils and core libs
cat libs.list utils.list > main.list
popd

# Make shared libs and scripts executable
chmod a+x %{buildroot}%{_libdir}/lib*.so.*
chmod a+x %{buildroot}%{_libdir}/vtk/doxygen/*.pl
chmod a+x %{buildroot}%{_libdir}/vtk/testing/*.{py,tcl}

# Remove exec bit from non-scripts and %%doc
for file in `find %{buildroot} -type f -perm 0755 \
  | xargs -r file | grep ASCII | awk -F: '{print $1}'`; do
  head -1 $file | grep '^#!' > /dev/null && continue
  chmod 0644 $file
done
find Utilities/Upgrading -type f | xargs chmod -x

# Add exec bits to shared libs ...
chmod 0755 %{buildroot}%{_libdir}/python*/site-packages/vtk/*.so

# Verdict places the docs in the false folder
rm -fr %{buildroot}%{_libdir}/vtk/doc

%check
#LD_LIBARARY_PATH=`pwd`/bin ctest -V

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post tcl -p /sbin/ldconfig

%postun tcl -p /sbin/ldconfig

%post python -p /sbin/ldconfig

%postun python -p /sbin/ldconfig

%if %{with java}
%post java -p /sbin/ldconfig

%postun java -p /sbin/ldconfig
%endif

%post qt -p /sbin/ldconfig

%postun qt -p /sbin/ldconfig

%files -f build/main.list
%defattr(-,root,root,-)
%doc --parents Copyright.txt README.html vtkLogo.jpg vtkBanner.gif Wrapping/*/README*

%files devel
%defattr(-,root,root,-)
%doc Utilities/Upgrading
%{_bindir}/vtkWrapHierarchy
%{_libdir}/vtk/doxygen
%{_includedir}/vtk
%{_libdir}/*.so
%{_libdir}/vtk/CMake
%{_libdir}/vtk/*.cmake
%{_libdir}/vtk/hints

%files tcl
%defattr(-,root,root,-)
%{_libdir}/*TCL.so.*
%{_bindir}/vtk
%{_bindir}/vtkWrapTcl
%{_bindir}/vtkWrapTclInit
%{_libdir}/vtk/pkgIndex.tcl
%{_libdir}/vtk/tcl

%files python
%defattr(-,root,root,-)
#%{python_sitearch}/vtk
%{python_sitearch}/*
%{_libdir}/*PythonD.so.*
%{_bindir}/vtkpython
%{_bindir}/vtkWrapPython
%{_bindir}/vtkWrapPythonInit

%if %{with java}
%files java
%defattr(-,root,root,-)
%{_libdir}/*Java.so.*
%{_libdir}/vtk/java
%{_bindir}/vtkParseJava
%{_bindir}/vtkWrapJava
%endif

%files qt
%defattr(-,root,root,-)
%{_libdir}/libQVTK.so.*
%{_libdir}/qt4/plugins/designer

%files testing -f build/testing.list
%defattr(-,root,root,-)
%{_libdir}/vtk/testing

%files examples -f build/examples.list
%defattr(-,root,root,-)
%doc vtk-examples/Examples

%changelog
* Fri Oct 7 2011 Orion Poplawski <orion@cora.nwra.com> - 5.8.0-1
- Update to 5.8.0
- Drop version from directory names
- Use VTK_PYTHON_SETUP_ARGS instead of patch to set python install dir
- Drop several patches fixed upstream
- Remove rpaths from all hand installed binaries (Bug 744437)
- Don't link against OSMesa (Bug 744434)

* Thu Jun 23 2011 Orion Poplawski <orion@cora.nwra.com> - 5.6.1-10
- Add BR qtwebkit-devel, fixes FTBS bug 715770

* Thu May 19 2011 Orion Poplawski <orion@cora.nwra.com> - 5.6.1-9
- Update soversion patch to add soversion to libvtkNetCDF.so

* Mon Mar 28 2011 Orion Poplawski <orion@cora.nwra.com> - 5.6.1-8
- Rebuild for new mysql

* Thu Mar 17 2011 Orion Poplawski <orion@cora.nwra.com> - 5.6.1-7
- Add needed requires to vtk-devel

* Wed Mar 16 2011 Orion Poplawski <orion@cora.nwra.com> - 5.6.1-6
- Turn on boost, mysql, postgres, ogg theora, and text analysis support,
  bug 688275.

* Wed Mar 16 2011 Marek Kasik <mkasik@redhat.com> - 5.6.1-5
- Add backslashes to VTK_INSTALL_LIB_DIR and
- VTK_INSTALL_INCLUDE_DIR (#687895)

* Tue Mar 15 2011 Orion Poplawski <orion@cora.nwra.com> - 5.6.1-4
- Set VTK_INSTALL_LIB_DIR, fix bug 687895

* Fri Feb 18 2011 Orion Poplawski <orion@cora.nwra.com> - 5.6.1-3
- Add patch to support gcc 4.6
- Add patch to make using system libraries easier
- Update pythondestdir patch to use --prefix and --root
- Use system gl2ps and libxml2
- Use standard cmake build macro, out of tree builds
- Add patch from upstream to add sonames to libCosmo and libVPIC (bug #622840)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 7 2010 Orion Poplawski <orion@cora.nwra.com> - 5.6.1-1
- Update to 5.6.1
- Enable qt4 support, drop qt3 support

* Wed Oct 20 2010 Adam Jackson <ajax@redhat.com> 5.6.0-37
- Rebuild for new libOSMesa soname

* Sat Jul 31 2010 David Malcolm <dmalcolm@redhat.com> - 5.6.0-36
- add python 2.7 compat patch

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 5.6.0-35
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jul  5 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.6.0-34
- Update to 5.6.0.

* Sat Jun  6 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.4.2-30
- Update to 5.4.2.

* Thu Mar 12 2009 Orion Poplawski <orion@cora.nwra.com> - 5.2.1-29
- Update to 5.2.1

* Fri Mar 06 2009 Jesse Keating <jkeating@redhat.com> - 5.2.0-28
- Remove chmod on examples .so files, none are built.  This needs
  more attention.

* Sun Oct  5 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.2.0-26
- Update to 5.2.0.

* Wed Oct 1 2008 Orion Poplawski <orion@cora.nwra.com> - 5.0.2-25
- Fix patch fuzz

* Mon Aug 25 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.4-24
- Change java build dependencies from java-devel to gcj.

* Sun Aug 24 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.4-23
- %%check || : does not work anymore.
- enable java by default.

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.0.4-22
- fix license tag

* Sat Apr 12 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.4-21
- Fixes for gcc 4.3 by Orion Poplawski.

* Sat Apr  5 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.4-20
- Change BR to qt-devel to qt3-devel.

* Sat Feb 23 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.4-19
- Update to 5.0.4.

* Mon May 28 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.3-18
- Move headers to %%{_includedir}/vtk.
- Remove executable bit from sources.

* Mon Apr 16 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.3-17
- Make java build conditional.
- Add ldconfig %%post/%%postun for java/qt subpackages.

* Sun Apr 15 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.3-16
- Remove %%ghosting pyc/pyo.

* Wed Apr 04 2007 Paulo Roma <roma@lcg.ufrj.br> - 5.0.3-15
- Update to 5.0.4.
- Added support for qt4 plugin.

* Wed Feb  7 2007 Orion Poplawski <orion@cora.nwra.com> - 5.0.2-14
- Enable Java, Qt, GL2PS, OSMESA

* Mon Sep 11 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.2-13
- Update to 5.0.2.

* Sun Aug  6 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.1-12
- cmake needs to be >= 2.0.4.

* Fri Aug  4 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.1-11
- Fix some python issues including pyo management.

* Sun Jul 23 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.1-10
- Embed feedback from bug 199405 comment 5.
- Fix some Group entries.
- Remove redundant dependencies.
- Use system libs.
- Comment specfile more.
- Change buildroot handling with CMAKE_INSTALL_PREFIX.
- Enable qt designer plugin.

* Wed Jul 19 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.1-7
- Fix some permissions for rpmlint and debuginfo.

* Sun Jul 16 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.1-7
- Remove rpath and some further rpmlint warnings.

* Thu Jul 13 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.1-6
- Update to 5.0.1.

* Wed May 31 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 5.0.

* Mon Apr 04 2004 Intrinsic Spin <spin@freakbait.com> 2.mr
- built on a machine with a stock libGL.so

* Sun Apr 04 2004 Intrinsic Spin <spin@freakbait.com>
- little cleanups
- Built for FC1

* Sun Jan 11 2004 Intrinsic Spin <spin@freakbait.com>
- Built against a reasonably good (according to dashboard) CVS version so-as
 to get GL2PS support.
- Rearranged. Cleaned up. Added some comments. 

* Sat Jan 10 2004 Intrinsic Spin <spin@freakbait.com>
- Blatently stole this spec file for my own nefarious purposes.
- Removed Java (for now). Merged the Python and Tcl stuff into 
 the main rpm.

* Fri Dec 05 2003 Fabrice Bellet <Fabrice.Bellet@creatis.insa-lyon.fr>
- (See Fabrice's RPMs for any more comments --Spin)

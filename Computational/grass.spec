Name:      grass
Version:   6.4.1
Release:   3%{?dist}
Summary:   GRASS - Geographic Resources Analysis Support System
Group:     Applications/Engineering
License:   GPLv2
URL:       http://grass.itc.it/index.php
Source0:   http://grass.itc.it/grass64/source/grass-%{version}.tar.gz  
Source1:   grass.desktop
Source2:   http://grass.itc.it/images/grasslogo_vector_small.png
Patch0:    grass-pkgconf.patch
Patch1:    grass-shlib-soname.patch
Patch2:    grass-gcc44.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:  proj-nad proj-epsg wxPython
Requires:  wxGTK wxGTK-gl

BuildRequires:  gettext
BuildRequires:  python-devel
BuildRequires:  bison flex pkgconfig swig
BuildRequires:  proj-devel proj-nad proj-epsg
BuildRequires:  desktop-file-utils libjpeg-devel
BuildRequires:  libtiff-devel libpng-devel freetype-devel
BuildRequires:  zlib-devel readline-devel ncurses-devel tk-devel 
BuildRequires:  unixODBC-devel mysql-devel postgresql-devel sqlite-devel
BuildRequires:  geos-devel blas-devel lapack-devel fftw2-devel gdal-devel
BuildRequires:  mesa-libGLU-devel mesa-libGLw-devel libXmu-devel lesstif-devel wxPython-devel
BuildRequires:  cairo-devel wxGTK-devel

# we have multilib triage
%if "%{_lib}" == "lib"
%define cpuarch 32
%else
%define cpuarch 64
%endif

%description
GRASS (Geographic Resources Analysis Support System) is a Geographic
Information System (GIS) used for geospatial data management and
analysis, image processing, graphics/maps production, spatial
modeling, and visualization. GRASS is currently used in academic and
commercial settings around the world, as well as by many governmental
agencies and environmental consulting companies.

%package libs
Summary: GRASS (Geographic Resources Analysis Support System) runtime libraries
Group: Applications/Engineering

%description libs
GRASS (Geographic Resources Analysis Support System) runtime libraries.

%package devel
Summary: GRASS (Geographic Resources Analysis Support System) development headers
Group: Applications/Engineering
Requires: %{name}-libs = %{version}-%{release}
Requires: pkgconfig
Requires: grass-devel lesstif-devel wxPython-devel
Requires: mesa-libGL-devel libX11-devel libXt-devel
Requires: gdal-devel proj-devel xorg-x11-proto-devel

%description devel
GRASS (Geographic Resources Analysis Support System) development headers.

%prep
%setup  -n %{name}-%{version} -q
%patch0 -p0 -b .pkgconf~
%patch1 -p0 -b .shlibver~
%patch2 -p1 -b .gcc44~

# remove the swap file
rm -rf doc/.howto_release.txt.swp

# readline requires ncurses, so workaround
# correct mysql_config query
sed -i 's|-lreadline|-lreadline -lcurses|g' configure
sed -i 's|--libmysqld-libs|--libs|g' configure

# preserve timestamp during install process
sed -i 's|^cp |cp -p |' tools/build_html_index.sh
sed -i 's|-cp |-cp -p |' Makefile

# convert some offendig file UTF-8
for file in {translators.csv,doc/infrastructure.txt} ; do
   if file $file | grep -q ISO-8859 ; then
      iconv -f ISO-8859-1 -t UTF-8 $file > ${file}.tmp && \
      mv -f ${file}.tmp $file
   fi
done

%build

# code may contain sensible buffer overflows triggered by gcc ssp flag (mustfixupstream).
CFLAGS=`echo %{optflags}|sed -e 's/-Wp,-D_FORTIFY_SOURCE=2 //g'`
# keep timestamp over install section
export INSTALL="%{__install} -c -p"
# correct linkage against libm.so
export LDFLAGS="-lm"
export CFLAGS

%configure \
   --enable-shared \
   --with-nls \
   --with-blas \
   --with-lapack \
   --with-fftw \
   --with-gdal \
   --with-proj \
   --with-proj-includes=%{_includedir} \
   --with-proj-libs=%{_libdir} \
   --with-proj-share=%{_datadir}/proj \
   --with-readline \
   --with-readline-includes=%{_includedir}/readline \
   --with-readline-libs=%{_libdir} \
   --with-sqlite \
   --with-odbc \
   --with-odbc-libs=%{_libdir} \
   --with-odbc-includes=%{_includedir} \
   --with-mysql \
   --with-mysql-includes=%{_includedir}/mysql \
   --with-mysql-libs=%{_libdir}/mysql \
   --with-postgres  \
   --with-postgres-includes=%{_includedir}/pgsql \
   --with-postgres-libs=%{_libdir} \
   --with-freetype=yes \
   --with-freetype-includes=%{_includedir}/freetype2 \
   --with-motif \
   --with-opengl \
   --with-x \
   --with-cairo \
%ifarch x86_64 ia64 ppc64 s390x sparc64 alpha 
   --enable-64bit \
%endif
%ifarch sparcv9 sparc64
   --enable-64bit-vis \
%endif       
   --enable-largefile \
   --with-cxx \
   --with-wxwidgets=wx-config \
   --with-python \
   --with-glw \
   --with-glw-libs=%{_libdir}

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

# make install
make prefix=%{buildroot}%{_prefix} BINDIR=%{buildroot}%{_bindir} \
     PREFIX=%{buildroot}%{_prefix} install

# changing GISBASE in startup script to point to systems %{_libdir}%{name}-%{version}
mv  %{buildroot}%{_bindir}/grass64 %{buildroot}%{_bindir}/grass64.tmp
cat %{buildroot}%{_bindir}/grass64.tmp | \
    sed -e "1,\$s&^GISBASE.*&GISBASE=%{_libdir}/%{name}-%{version}&" | \
    cat - > %{buildroot}%{_bindir}/grass64
rm  %{buildroot}%{_bindir}/grass64.tmp
chmod +x %{buildroot}%{_bindir}/grass64

# change to wxWidgets by default
cat %{buildroot}%{_prefix}/grass-%{version}%{_sysconfdir}/Init.sh | \
sed -e '/default if needed \- currently tcltk/,/fi/ {:ack N; /fi/! b ack  s/\"tcltk/\"wxpython/}' \
    > %{buildroot}%{_prefix}/grass-%{version}%{_sysconfdir}/Init.sh.tmp
mv -f %{buildroot}%{_prefix}/grass-%{version}%{_sysconfdir}/Init.sh.tmp \
      %{buildroot}%{_prefix}/grass-%{version}%{_sysconfdir}/Init.sh
chmod 755 %{buildroot}%{_prefix}/grass-%{version}%{_sysconfdir}/Init.sh

# fix docs lookup path
sed -i -e 's/$env(GISBASE)\/docs\//\/usr\/share\/doc\/%{name}-%{version}\/docs\//' \
    %{buildroot}%{_prefix}/%{name}-%{version}/etc/gis_set.tcl
sed -i -e 's/$env(GISBASE)\/docs\//\/usr\/share\/doc\/%{name}-%{version}\/docs\//' \
    %{buildroot}%{_prefix}/%{name}-%{version}/etc/gui.tcl
sed -i -e 's/$env(GISBASE)\/docs\//\/usr\/share\/doc\/%{name}-%{version}\/docs\//' \
    %{buildroot}%{_prefix}/%{name}-%{version}/etc/nviz2.2/scripts/nviz2.2_script
sed -i -e 's|C_BASE="$GISBASE"|C_BASE=\"\/usr\/share\/doc\/%{name}-%{version}\/docs"|g' \
    %{buildroot}%{_prefix}/%{name}-%{version}/scripts/g.manual
sed -i -e 's|%{name}-%{version}\/docs|%{name}-%{version}|g' \
    %{buildroot}%{_prefix}/%{name}-%{version}/scripts/g.manual
sed -i -e 's|(\"GISBASE\"), \"docs\", \"html\", \"icons\", \"silk\")|(\"GISBASE\"), \"icons\", \"silk\")|g' \
    %{buildroot}%{_prefix}/%{name}-%{version}/etc/wxpython/icons/icon.py

# make grass libraries available on the system
mv %{buildroot}%{_prefix}/grass-%{version}/lib/ %{buildroot}%{_libdir}

# make grass headers available on the system
mv %{buildroot}%{_prefix}/grass-%{version}/include %{buildroot}%{_prefix}/
rm -rf %{buildroot}%{_includedir}/Make

# create universal multilib header bz#341391
install -p -m 644 %{buildroot}%{_includedir}/%{name}/config.h \
           %{buildroot}%{_includedir}/%{name}/config-%{cpuarch}.h

cat > %{buildroot}%{_includedir}/%{name}/config.h <<EOF
#include <bits/wordsize.h>

#if __WORDSIZE == 32
#include "grass/config-32.h"
#else
#if __WORDSIZE == 64
#include "grass/config-64.h"
#else
#error "Unknown word size"
#endif
#endif
EOF
touch -r ChangeLog_%{version}.gz %{buildroot}%{_includedir}/%{name}/config.h
touch -r ChangeLog_%{version}.gz %{buildroot}%{_includedir}/%{name}/config-%{cpuarch}.h

# fix prelink issue bz#458427
mkdir -p %{buildroot}%{_sysconfdir}/prelink.conf.d
cat > %{buildroot}%{_sysconfdir}/prelink.conf.d/%{name}-%{cpuarch}.conf <<EOF
-b %{_libdir}/libgrass_gproj.so.6.4.0
-b %{_libdir}/libgrass_sim.so.6.4
EOF

# make man pages aviable in system, convert in utf8.
pushd %{buildroot}%{_prefix}/grass-%{version}/man/
for manpage in `find  man1 -type f` ; do
   iconv -f iso88592 -t utf8 \
        $manpage > $manpage.tmp
        mv -f $manpage.tmp $manpage
done
popd
mkdir -p %{buildroot}%{_datadir}/man/
mv  %{buildroot}%{_prefix}/grass-%{version}/man/* %{buildroot}%{_mandir}
rm -rf %{buildroot}%{_prefix}/grass-%{version}/man
gzip -d ChangeLog_%{version}.gz
iconv -f iso88592 -t utf8 ChangeLog_%{version} | \
gzip -9 > ChangeLog_%{version}.gz

# make locales aviable in system, fix issue for pt_BR.
mkdir -p %{buildroot}%{_datadir}/locale/
mv %{buildroot}%{_prefix}/grass-%{version}/locale %{buildroot}%{_datadir}/
mv %{buildroot}%{_datadir}/locale/pt_br %{buildroot}%{_datadir}/locale/pt_BR

# pack lang sets
%find_lang grassmods
%find_lang grasslibs
%find_lang grasswxpy
cat grassmods.lang > %{name}.lang
cat grasslibs.lang >> %{name}.lang
cat grasswxpy.lang >> %{name}.lang

# install pkg-config file
mkdir -p %{buildroot}%{_libdir}/pkgconfig
install -p -m 644 grass.pc %{buildroot}%{_libdir}/pkgconfig/

# install desktop icon
mkdir  %{buildroot}%{_datadir}/pixmaps/
install -p -m 644 %{SOURCE2} %{buildroot}%{_datadir}/pixmaps/grass.png
desktop-file-install --vendor="fedora" \
        --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}

# fixup spurious exec flags here
find %{buildroot} -name "*.tcl" -exec chmod +r-x '{}' \;
chmod +x %{buildroot}%{_prefix}/grass-%{version}%{_sysconfdir}/wxpython/gui_modules/menuform.py
chmod -x %{buildroot}%{_prefix}/grass-%{version}%{_sysconfdir}/nviz2.2/scripts/configIndex
chmod -x %{buildroot}%{_prefix}/grass-%{version}%{_sysconfdir}/nviz2.2/scripts/nviz_params
chmod -x %{buildroot}%{_prefix}/grass-%{version}%{_sysconfdir}/nviz2.2/scripts/tclIndex
chmod -x %{buildroot}%{_prefix}/grass-%{version}%{_sysconfdir}/nviz2.2/scripts/panelIndex
chmod +x %{buildroot}%{_prefix}/grass-%{version}%{_sysconfdir}/gem/skeleton/post
chmod +x %{buildroot}%{_prefix}/grass-%{version}%{_sysconfdir}/gem/skeleton/uninstall
chmod +x %{buildroot}%{_prefix}/grass-%{version}%{_sysconfdir}/g.mapsets.tcl
chmod +x %{buildroot}%{_prefix}/grass-%{version}%{_sysconfdir}/dm/tksys.tcl
chmod +x %{buildroot}%{_prefix}/grass-%{version}%{_sysconfdir}/gm/tksys.tcl
chmod +x %{buildroot}%{_prefix}/grass-%{version}%{_sysconfdir}/gm/animate.tcl

# fixup few nviz script header, it will anyway allways executed by nviz
for nviz in {script_play,nviz2.2_script,script_tools,script_file_tools,script_get_line}; do
 cat %{buildroot}%{_prefix}/grass-%{version}%{_sysconfdir}/nviz2.2/scripts/$nviz \
  | grep -v '#!nviz' > %{buildroot}%{_prefix}/grass-%{version}%{_sysconfdir}/nviz2.2/scripts/$nviz.tmp 
 mv  %{buildroot}%{_prefix}/grass-%{version}%{_sysconfdir}/nviz2.2/scripts/$nviz.tmp \
     %{buildroot}%{_prefix}/grass-%{version}%{_sysconfdir}/nviz2.2/scripts/$nviz
done

# move icon folder in GISBASE and set its path to be FHS compliant
mv %{buildroot}%{_prefix}/%{name}-%{version}/docs/html/icons %{buildroot}%{_prefix}/grass-%{version}/

# switch to the system wide docs to be FHS compliant
rm -rf %{buildroot}%{_prefix}/%{name}-%{version}/docs

# hide GISBASE into systems %{_libdir} insted, to be FHS compliant
mv %{buildroot}%{_prefix}/%{name}-%{version} %{buildroot}%{_libdir}/

# fix fontpath
sed -i -e 's|%{buildroot}%{_prefix}/%{name}-%{version}|%{_libdir}/%{name}-%{version}|' \
%{buildroot}%{_libdir}/%{name}-%{version}/etc/fontcap

%clean
rm -rf %{buildroot}

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING GPL.TXT README 
#%%doc README-fedora
%doc REQUIREMENTS.html CHANGES
%doc doc dist.*/docs
%{_sysconfdir}/prelink.conf.d/%{name}-%{cpuarch}.conf
%{_bindir}/grass64
%{_bindir}/gem64
%dir %{_libdir}/%{name}-%{version}
%exclude %{_libdir}/%{name}-%{version}/etc/*.table
%exclude %{_libdir}/%{name}-%{version}/driver/db/*
%{_libdir}/%{name}-%{version}/*
%{_datadir}/applications/fedora-grass.desktop
%{_datadir}/pixmaps/grass.png
%{_datadir}/locale/*/LC_MESSAGES/grasswxpy.mo
%{_mandir}/man1/*

%files libs
%defattr(-,root,root,-)
%doc AUTHORS COPYING GPL.TXT README
%{_libdir}/libgrass_*.so.*
%{_libdir}/%{name}-%{version}/etc/*.table
%{_libdir}/%{name}-%{version}/driver/db/*

%files devel
%defattr(-,root,root,-)
%doc AUTHORS COPYING GPL.TXT README TODO
%doc ChangeLog_%{version}.gz doc/raster doc/vector 
%exclude %{_libdir}/libgrass_*.a
%{_libdir}/pkgconfig/%{name}.pc
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%dir %{_includedir}/%{name}/dgl
%dir %{_includedir}/%{name}/rtree
%dir %{_includedir}/%{name}/vect
%{_includedir}/%{name}/dgl/*.h
%{_includedir}/%{name}/rtree/*.h
%{_includedir}/%{name}/vect/*.h
%{_includedir}/%{name}/iostream/*.h
%{_libdir}/libgrass_*.so

%changelog
* Wed Mar 23 2011 Dan Horák <dan@danny.cz> - 6.4.0-3
- rebuilt for mysql 5.5.10 (soname bump in libmysqlclient)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 22 2010 Viji Nair <viji [AT] fedoraproject DOT org> - 6.4.0-1
- Rebuilt with new gdal 1.7.3.
- Updated to upstream version 6.4.0.
- Removed grass-gdilib.patch
- Spec review

* Fri Dec 4 2009 Devrim GÜNDÜZ <devrim@gunduz.org> - 6.3.0-15
- Rebuilt with new geos

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 6.3.0-14
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.3.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 23 2009 Lubomir Rintel <lkundrak@v3.sk> - 6.3.0-12
- Fix build with GCC 4.4

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 29 2009 Balint Cristian <cristian.balint@gmail.com> - 6.3.0-10
- email change
- rebuild for new mysql

* Sun Dec 07 2008 Balint Cristian <rezso@rdsor.ro> 6.3.0-9
- rebuild against newer gdal

* Sun Dec 07 2008 Balint Cristian <rezso@rdsor.ro> 6.3.0-8
- rebuild against newer gdal

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> 6.3.0-7
- Rebuild for Python 2.6

* Sat Aug 24 2008 Balint Cristian <rezso@rdsor.ro> 6.3.0-6
- bz#458427 (prelink fail)
- bz#458563 (grass not able to display documentation)

* Sat Jul 05 2008 Balint Cristian <rezso@rdsor.ro> 6.3.0-5
- address bz#454146 (wxPython miss)

* Thu Jun 12 2008 Balint Cristian <rezso@rdsor.ro> 6.3.0-4
- address bz#341391 (multilib issue)

* Mon May 23 2008 Balint Cristian <rezso@rdsor.ro> 6.3.0-3
- bugfix initscripts permission

* Thu May 15 2008 Balint Cristian <rezso@rdsor.ro> 6.3.0-2
- require swig to build

* Thu May 15 2008 Balint Cristian <rezso@rdsor.ro> 6.3.0-1
- final stable release upstream

* Thu Mar 27 2008 Balint Cristian <rezso@rdsor.ro> 6.3.0-0.4.RC6
- really rebuild against latest gdal

* Thu Mar 27 2008 Balint Cristian <rezso@rdsor.ro> 6.3.0-0.2.RC6
- rebuild against latest gdal

* Thu Mar 27 2008 Balint Cristian <rezso@rdsor.ro> 6.3.0-0.2.RC6
- BuildRequire: python-devel

* Thu Mar 27 2008 Balint Cristian <rezso@rdsor.ro> 6.3.0-0.1.RC6
- new branch release
- enable new wxWidgets support
- set wxpython as default instead of tcltk
- fix missing GDI unaviable on unices
- smp build is safe now
- r.terraflow license problem fixed
- no fedora custom packs anymore, all license clear

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 6.2.3-2
- Autorebuild for GCC 4.3

* Sat Jan 5 2008 Devrim GUNDUZ <devrim@commandprompt.com> 6.2.3-1
- Update to 6.2.3

* Thu Dec 06 2007 Release Engineering <rel-eng at fedoraproject dot org> - 6.2.2-3
- Rebuild for deps

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 6.2.2-2
- Rebuild for selinux ppc32 issue.

* Wed Jul 25 2007 Balint Cristian <cbalint@redhat.com> 6.2.2-1
- new upstream stable version

* Thu Jun 07 2007 Balint Cristian <cbalint@redhat.com> 6.2.2-0.2.RC1
- fix version string in desktop file
- add RO lang to desktop file
- dropped one patch, seems fixed upstream.

* Fri Jun 01 2007 Balint Cristian <cbalint@redhat.com> 6.2.2-0.1.RC1
- 6.2.2 rc1 bugfix release
- fix docbase lookup path for g.manual

* Sat May 12 2007 Balint Cristian <cbalint@redhat.com> 6.2.1-16
- fix koji build for ppc ppc64, dont use _host macro anymore.

* Sat May 12 2007 Balint Cristian <cbalint@redhat.com> 6.2.1-15
- rebuild against new gdal

* Mon Apr 02 2007 Balint Cristian <cbalint@redhat.com> 6.2.1-14
- remove bogus requirement in grass-libs
- rename gem loader to gem62

* Tue Mar 20 2007 Balint Cristian <cbalint@redhat.com> 6.2.1-13
- see README-fedora for license fix in redistributed tarball
- r.terraflow plugin removal from -fedora tarball

* Fri Mar 13 2007 Balint Cristian <cbalint@redhat.com> 6.2.1-12
- more spec review

* Fri Mar 13 2007 Balint Cristian <cbalint@redhat.com> 6.2.1-11
- more spec review

* Fri Mar 13 2007 Balint Cristian <cbalint@redhat.com> 6.2.1-10
- more spec review

* Fri Mar 2 2007 Balint Cristian <cbalint@redhat.com> 6.2.1-9
- require missing libjpeg-devel

* Tue Feb 27 2007 Balint Cristian <cbalint@redhat.com> 6.2.1-8
- more buildfixes, should build now in mock for any arches
- estetic changes in spec file

* Sat Feb 25 2007 Balint Cristian <cbalint@redhat.com> 6.2.1-7
- fix mock build on any arch.

* Sat Feb 23 2007 Balint Cristian <cbalint@redhat.com> 6.2.1-6
- fix mock build, more spec cleanup.
- fix docs lookup from g.manual
- disable fedora c flags, ssp break functionality for now.

* Sat Feb 23 2007 Balint Cristian <cbalint@redhat.com> 6.2.1-5
- use macros if posible.

* Sat Feb 10 2007 Balint Cristian <cbalint@redhat.com> 6.2.1-4
- fix more nits in specs
- fix require list.

* Fri Feb 09 2007 Balint Cristian <cbalint@redhat.com> 6.2.1-3
- fix more nits in specs

* Wed Feb 07 2007 Balint Cristian <cbalint@redhat.com> 6.2.1-2
- fix nits in specs
- disable static libs pack
- use macros in file lists if possible.

* Wed Feb 07 2007 Balint Cristian <cbalint@redhat.com> 6.2.1-1
- first build for fedora-extras
- enable all options for packages aviable in fedora
- fix buffer overflow problem during compile with ssp
- fix paths in pkconfig file
- add desktop icon
- relocate lang and man page folders in the right places
- sanitize shared library names, fix -soname versioning in libs.
- fix some non utf8 manpage
- fix pt_BR locale path
- fix some nviz script headers
- fix exec rights across some scripts, remove exec from tcl scripts
- move out GISBASE in lib and fixup script enviroment for this
- switch help-doc to datadir/doc/grass and fixit up in grass paths

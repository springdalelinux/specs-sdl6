%global gmthome %{_datadir}/GMT
%global gmtconf %{_sysconfdir}/GMT
%global gmtdoc %{_docdir}/gmt

#We can't link with octave until we are GPLv3+ compatible
%bcond_with octave
%if %with octave
%{!?octave_api: %define octave_api %(octave-config -p API_VERSION 2>/dev/null || echo 0)}
%define octave_mdir %(octave-config -p LOCALAPIFCNFILEDIR || echo)
%define octave_octdir %(octave-config -p LOCALAPIOCTFILEDIR || echo)
%endif

Name:           GMT
Version:        4.5.5
Release:        2%{?dist}.1
Summary:        Generic Mapping Tools

Group:          Applications/Engineering
License:        GPLv2
URL:            http://gmt.soest.hawaii.edu/
Source0:        ftp://ftp.soest.hawaii.edu/gmt/GMT%{version}_src.tar.bz2
Source1:        ftp://ftp.soest.hawaii.edu/gmt/GMT%{version}_share.tar.bz2
Source2:        ftp://ftp.soest.hawaii.edu/gmt/GMT%{version}_suppl.tar.bz2
Source3:        ftp://ftp.soest.hawaii.edu/gmt/GMT%{version}_doc.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gdal-devel
BuildRequires:  libXt-devel libXaw-devel libXmu-devel libXext-devel
BuildRequires:  netcdf-devel
BuildRequires:  GMT-coastlines >= 2.1.0
%if %with octave
BuildRequires:  octave-devel
%endif
# less is detected by configure, and substituted in GMT.in
BuildRequires:  less
Requires:       less
Requires:       %{name}-common = %{version}-%{release}
Requires:       GMT-coastlines >= 2.1.0
Provides:       gmt = %{version}-%{release}
%if %without octave
Obsoletes:      GMT-octave <= %{version}-%{release}
%endif

#No xerces-c-devel -> gdal on ppc64
ExcludeArch:    ppc64

%description
GMT is an open source collection of ~60 tools for manipulating geographic and
Cartesian data sets (including filtering, trend fitting, gridding, projecting,
etc.) and producing Encapsulated PostScript File (EPS) illustrations ranging
from simple x-y plots via contour maps to artificially illuminated surfaces
and 3-D perspective views.  GMT supports ~30 map projections and transforma-
tions and comes with support data such as coastlines, rivers, and political
boundaries.

GMT is developed and maintained by Paul Wessel and Walter H. F.  Smith with
help from a global set of volunteers, and is supported by the National
Science Foundation.


%package        common
Summary:        Common files for %{name}
Group:          Applications/Engineering
Provides:       gmt-common = %{version}-%{release}
BuildArch:      noarch

%description    common
The %{name}-common package contains common files for GMT (Generic
Mapping Tools) package.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Provides:       gmt-devel = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}
Provides:       gmt-doc = %{version}-%{release}
Provides:       %{name}-examples = %{version}-%{release}
Obsoletes:      %{name}-examples < %{version}-%{release}
BuildArch:      noarch

%description    doc
The %{name}-doc package provides the documentation for the GMT (Generic
Mapping Tools) package.


%package        static
Summary:        Static libraries for %{name}
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}
Provides:       gmt-static = %{version}-%{release}

%description    static
The %{name}-static package contains static libraries for developing
applications that use %{name}.


%if %with octave
%package        octave
Summary:        Octave libraries for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       octave(api) = %{octave_api}
Provides:       gmt-octave = %{version}-%{release}

%description    octave
The %{name}-octave package contains and Octave interface for developing
applications that use %{name}.
%endif


# X11 application in a subpackage. No .desktop file since it
# requires a file name as argument
%package -n      xgridedit
Summary:         GMT grid code graphical editor
Group:           Applications/Engineering

%description -n xgridedit
XGridEdit is an application for viewing and editing the numerical values in
GMT 2 dimensional grids.


%prep
%setup -q -b1 -b2 -b3 -n GMT%{version}
#We don't care about .bat files
find -name \*.bat | xargs rm
#Fix permissions
find -name \*.c | xargs chmod a-x


%build
#So we execute do_examples.sh instead of do_examples.csh
export CSH=sh
export CFLAGS="$RPM_OPT_FLAGS -fPIC -I%{_includedir}/netcdf"
%configure --datadir=%{gmthome} \
           --enable-debug \
           --enable-gdal GDAL_INC=%{_includedir}/gdal \
           --enable-shared \
%if %with octave
           --enable-octave --enable-mex-mdir=%{octave_mdir} \
           --enable-mex-xdir=%{octave_octdir} \
%endif
           --disable-rpath
make
make suppl


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT INSTALL='install -c -p'  install-all
#Setup configuration files 
mkdir -p $RPM_BUILD_ROOT%{gmtconf}/{mgg,dbase,mgd77,conf}
pushd $RPM_BUILD_ROOT%{gmthome}/
# put conf files in %{gmtconf} and do links in %{gmthome}
for file in conf/*.conf conf/gmtdefaults_* mgg/gmtfile_paths dbase/grdraster.info \
    mgd77/mgd77_paths.txt; do
  mv $file $RPM_BUILD_ROOT%{gmtconf}/$file
  ln -s ../../../../../%{gmtconf}/$file $RPM_BUILD_ROOT%{gmthome}/$file
done
popd

#Don't bring in csh for the csh examples
find $RPM_BUILD_ROOT/%{gmtdoc}/examples -name \*.csh | 
  xargs chmod a-x

# separate the README files that are associated with gmt main package
rm -rf __package_docs
mkdir __package_docs
cp -p src/*/README.* __package_docs
rm __package_docs/README.xgrid __package_docs/README.mex


%check
#Cleanup from previous runs
rm -f $RPM_BUILD_DIR/GMT%{version}/share/coast

#Setup environment for the tests
export GMT_SHAREDIR=$RPM_BUILD_DIR/GMT%{version}/share
export LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%{_libdir}

#Link in the coastline data
ln -s %{gmthome}/coast $RPM_BUILD_DIR/GMT%{version}/share

#Run the examples - note that this doesn't return errors if any fail, check logs!
make run-examples


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc README LICENSE.TXT ChangeLog
%{_bindir}/*
%exclude %{_bindir}/xgridedit
%{_libdir}/*.so.*

%files common
%defattr(-,root,root,-)
%doc README __package_docs/* LICENSE.TXT ChangeLog gmt_bench-marks
%dir %{gmtconf}
%dir %{gmtconf}/mgg
%dir %{gmtconf}/dbase
%dir %{gmtconf}/mgd77
%dir %{gmtconf}/conf
%config(noreplace) %{gmtconf}/conf/*
%config(noreplace) %{gmtconf}/mgg/gmtfile_paths
%config(noreplace) %{gmtconf}/dbase/grdraster.info 
%config(noreplace) %{gmtconf}/mgd77/mgd77_paths.txt
%{gmthome}/
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_mandir}/man3/*.3*

%files doc
%defattr(-,root,root,-)
%{gmtdoc}/

%files static
%defattr(-,root,root,-)
%{_libdir}/*.a

%if %with octave
%files octave
%defattr(-,root,root,-)
%{octave_mdir}/*.m
%{octave_octdir}/*.mex
%endif

%files -n xgridedit
%defattr(-,root,root,-)
%doc src/xgrid/README.xgrid
%{_bindir}/xgridedit


%changelog
* Fri Dec 3 2010 Orion Poplawski <orion@cora.nwra.com> 4.5.5-2.1
- Exclude ppc64 for now due to missing dependencies

* Sat Nov 6 2010 Orion Poplawski <orion@cora.nwra.com> 4.5.5-2
- Drop octave package due to licensing issues (bug 511844)

* Wed Nov 3 2010 Orion Poplawski <orion@cora.nwra.com> 4.5.5-1
- Update to 4.5.5
- Drop bufoverflow patch fixed upstream

* Thu Jul 22 2010 Orion Poplawski <orion@cora.nwra.com> 4.5.3-3
- Fix buffer overflow in psimage (bug #617332)

* Tue Jul 20 2010 Orion Poplawski <orion@cora.nwra.com> 4.5.3-2
- Bump coastlines requirement to 2.1.0

* Mon Jul 19 2010 Orion Poplawski <orion@cora.nwra.com> 4.5.3-1
- Update to 4.5.3

* Wed Jan 27 2010 Orion Poplawski <orion@cora.nwra.com> 4.5.2-1
- Update to 4.5.2

* Thu Nov 19 2009 Orion Poplawski <orion@cora.nwra.com> 4.5.1-3
- Re-enable check

* Thu Nov 19 2009 Orion Poplawski <orion@cora.nwra.com> 4.5.1-2
- Rebuild for netcdf 4.1.0
- Don't make GMT-common depend on GMT
- Remove BR GMT-coastlines, disable check for bootstrap

* Mon Oct 19 2009 Orion Poplawski <orion@cora.nwra.com> 4.5.1-1
- Update to 4.5.1
- Enable gdal support

* Fri Jul 31 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 4.5.0-4
- Rebuild against Octave 3.2.2

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Orion Poplawski <orion@cora.nwra.com> 4.5.0-1
- Update to 4.5.0

* Fri Apr 10 2009 Orion Poplawski <orion@cora.nwra.com> 4.4.0-2
- Add --enable-debug to avoid stripping of -g from CFLAGS

* Tue Feb 24 2009 Orion Poplawski <orion@cora.nwra.com> 4.4.0-1
- Update to 4.4.0
- Merge doc package into main package as noarch sub-packages
- Merge examples sub-package into doc

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue May 27 2008 Orion Poplawski <orion@cora.nwra.com> 4.3.1-2
- Fix lowercase provides (bug #448263)

* Wed May 21 2008 Orion Poplawski <orion@cora.nwra.com> 4.3.1-1
- Update to 4.3.1, drop upstreamed patches
- Remove other install fixes upstreamed

* Mon May 12 2008 Orion Poplawski <orion@cora.nwra.com> 4.3.0-2
- Add patch to link libraries properly
- Run ldconfig in %%post, dummy
- Don't ship .bat file
- Don't ship .in files
- Don't make .csh examples executable
- Drop execute bit on .m files

* Tue May 6 2008 Orion Poplawski <orion@cora.nwra.com> 4.3.0-1
- Update to 4.3.0, drop many upsreamed patches
- Add patch to install octave files in DESTDIR
- Add patch to fix segfaults due to uninitialized memory
- Add patch to fix a possible buffer overflow warning
- Remove duplicate html directory from examples package
- Create __package_docs directory for main package docs

* Tue Apr 28 2008 Orion Poplawski <orion@cora.nwra.com> 4.2.1-3
- Remove unfree source
- Split out xgridedit into sub-package
- Add BR and R on less
- Redirect octave-config stderr to /dev/null
- Move config files to /etc/GMT
- Use install -c -p to preserve timestamps
- Use cp -pr to copy share data
- Add sonames to shared libraries

* Mon Mar 24 2008 Orion Poplawski <orion@cora.nwra.com> 4.2.1-2
- Drop -doc sub-package, will have separate -docs package
- Add lower case name provides
- Build Octave files

* Mon Mar 17 2008 Orion Poplawski <orion@cora.nwra.com> 4.2.1-1
- Initial version

Name:       kst
Version:    2.0.3
Release:    2%{?dist}
Summary:    A data viewing program

Group:      Applications/Engineering
License:    GPLv3
URL:        http://kst.kde.org/
Source0:    ftp://ftp.kde.org/pub/kde/stable/apps/KDE3.x/scientific/kst-%{version}.tar.gz
#Source0:    Kst-2.0.3-rc1-sources.tar.bz2
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires: gsl-devel cmake28
BuildRequires: cfitsio-devel netcdf-devel
BuildRequires: getdata-devel muParser-devel
BuildRequires: desktop-file-utils
BuildRequires: autoconf automake qt4-devel

%description
Kst is a real-time data viewing and plotting tool with basic data analysis 
functionality. Kst contains many powerful built-in features and is 
expandable with plugins and extensions. 

Main features of kst include:
  * Robust plotting of live "streaming" data.
  * Powerful keyboard and mouse plot manipulation.
  * Powerful plugins and extensions support.
  * Large selection of built-in plotting and data manipulation functions, 
    such as histograms, equations, and power spectra.
  * Color mapping and contour mapping capabilities for three-dimensional data.
  * Monitoring of events and notifications support.
  * Filtering and curve fitting capabilities.
  * Convenient command-line interface.
  * Powerful graphical user interface.
  * Support for several popular data formats.
  * Multiple tabs or windows. 

%package docs
Summary:    Documentation for kst
Group:      Applications/Engineering
Requires:   %{name} = %{version}-%{release}
BuildArch:  noarch

%description docs
Documentation, tutorial, and sample data for kst.

%package devel
Summary:    Development libraries and headers for kst
Group:      Applications/Engineering
Requires:   %{name} = %{version}-%{release}

%description devel
Headers and libraries required when building against kst.

%package netcdf
Summary:    netcdf datasource plugin for kst
Group:      Applications/Engineering
Requires:   %{name} = %{version}-%{release}

%description netcdf
A plugin allowing kst to open and read data in netcdf format.

%package fits
Summary:    fits datasource plugin for kst
Group:      Applications/Engineering
Requires:   %{name} = %{version}-%{release}
# Hack because cfitsio won't run if it's internal library version
# doesn't perfectly match between installed library and compiled
# against library.  Meh.
Requires:   cfitsio = %(pkg-config --modversion cfitsio 2>/dev/null || echo 0)

%description fits
A plugin allowing kst to open and read data and images contained within 
fits files. 

%package getdata
Summary:    getdata datasource plugin for kst
Group:      Applications/Engineering
Requires:   %{name} = %{version}-%{release}

%description getdata
A plugin allowing kst to open and read data in getdata (dirfile) format.

%prep
%setup -q

%build
%cmake -Dkst_merge_files=1 -Dkst_rpath=0 \
  -Dkst_install_prefix=%{_prefix} -Dkst_install_libdir=%{_lib} \
  -Dkst_test=1 cmake
make %{?_smp_mflags} kst2

%check
#make test

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
make DESTDIR=%{buildroot} SUID_ROOT="" install
rm -f %{buildroot}%{_bindir}/test_*

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc INSTALL AUTHORS README COPYING COPYING-DOCS COPYING.LGPL 

#binaries
%{_bindir}/kst*
%{_libdir}/libkst*so.*
%{_libdir}/kst2/plugins/libkst2_dataobject*so
%{_libdir}/kst2/plugins/libkst2_fi*so

%{_datadir}/applications/kst.desktop
%{_datadir}/applnk/Graphics/kst.desktop
%{_datadir}/mimelink/application/x-kst.desktop
%{_datadir}/services/kst/kstplugin_*desktop
%{_datadir}/servicetypes/kst/kst*desktop
%{_datadir}/apps/kst/kstui.rc
%{_datadir}/man/man1/kst*

%{_libdir}/kst2/plugins/libkst2_datasource_ascii.so
%{_datadir}/services/kst/kstdata_ascii.desktop

%{_libdir}/kst2/plugins/libkst2_datasource_qimagesource.so
%{_datadir}/services/kst/kstdata_qimagesource.desktop

%{_libdir}/kst2/plugins/libkst2_datasource_sampledatasource.so
%{_datadir}/services/kst/kstdata_sampledatasource.desktop

%{_datadir}/config/colors/IDL*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libkst*a
%{_libdir}/libkst*so

%files docs
%defattr(-,root,root,-)
%{_datadir}/apps/kst/tutorial/gyrodata.dat

%files fits
%defattr(-,root,root,-)
%{_libdir}/kst2/plugins/libkst2_datasource_fitsimage.so
%{_datadir}/services/kst/kstdata_fitsimage.desktop

%files netcdf
%defattr(-,root,root,-)
%{_libdir}/kst2/plugins/libkst2_datasource_netcdf.so
%{_datadir}/services/kst/kstdata_netcdf.desktop

%files getdata
%defattr(-,root,root,-)
%{_libdir}/kst2/plugins/libkst2_datasource_dirfilesource.so
%{_datadir}/services/kst/kstdata_dirfilesource.desktop

%changelog
* Fri Jun 10 2011 Jon Ciesla <limb@jcomserv.net> - 2.0.3-2
- Rebuild for new cfitsio.

* Wed Jun 01 2011 Jon Ciesla <limb@jcomserv.net> - 2.0.3-1
- Update to 2.0.3 final.

* Fri Feb 18 2011 Matthew Truch <matt at truch.net> - 2.0.3-0.rc1
- Major overhaul to kst2.  

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 5 2010 Matthew Truch <matt at truch.net> - 1.8.0-8
- Bump to pickup new cfitsio.

* Wed Feb 24 2010 Matthew Truch <matt at truch.net> - 1.8.0-7
- Bump to pickup fixed cfitsio.
- Remove packaged fonts (which are unused and packaged incorrectly).

* Fri Feb 12 2010 Matthew Truch <matt at truch.net> - 1.8.0-6
- Hack to work around autotools build issue.
-  Use the libtool in the tarball; do not generate a new one.
- Modify kst-except.diff patch to *not* turn off exceptions in CXXFLAGS

* Wed Nov 25 2009 Orion Poplawski <orion at cora.nwra.com> - 1.8.0-5
- Rebuild for netcdf 4.1.0 and new cfitsio

* Tue Nov 17 2009 Matthew Truch <matt at truch.net> - 1.8.0-4
- Bump to pickup new cfitsio.

* Fri Jul 24 2009 Matthew Truch <matt at truch.net> - 1.8.0-3
- Really fix the patch.  Don't know how it wasn't fixed the first time.

* Fri Jul 24 2009 Matthew Truch <matt at truch.net> - 1.8.0-2
- Fix patch so it doesn't require fuzz.

* Sat Jul 18 2009 Matthew Truch <matt at truch.net> - 1.8.0-1
- Upstream kst 1.8.0
- Drop patch for saveperiod as it's included in upstream 1.8.0
- Separate out getdata support to subpackage (requires getdata)
- Include muParser support for general non-linear fit plugin.
- Bump for mass rebuild.

* Tue Mar 10 2009 Matthew Truch <matt at truch.net> - 1.7.0-6
- Make cfitsio explicit version check work.

* Thu Feb 26 2009 Matthew Truch <matt at truch.net> - 1.7.0-5
- Make documentation noarch.

* Mon Feb 23 2009 Matthew Truch <matt at truch.net> - 1.7.0-4
- Bump for mass rebuild.

* Fri Oct 17 2008 Matthew Truch <matt at truch.net> - 1.7.0-3
- Include patch from upstream to fix savePeriod.

* Fri Sep 19 2008 Matthew Truch <matt at truch.net> - 1.7.0-2
- Allow build from netcdf version 4.  

* Fri Sep 19 2008 Matthew Truch <matt at truch.net> - 1.7.0-1
- Update to upstream 1.7.0.  
- Re-enable ppc64 build of netcdf subpackage.

* Sat May 10 2008 Matthew Truch <matt at truch.net> - 1.6.0-4
- ExcludeArch ppc64 for netcdf subpackage as netcdf is disabled on ppc64.

* Sat May 10 2008 Matthew Truch <matt at truch.net> - 1.6.0-3
- Pick up patch from upstream fixing -F command line option
  Upstream KDE svn revision 805176
  Fixes upstream reported KDE BUG:161766

* Thu Apr 24 2008 Matthew Truch <matt at truch.net> - 1.6.0-2
- Also remove PlanckIDEF datasoure.

* Thu Apr 24 2008 Matthew Truch <matt at truch.net> - 1.6.0-1
- New version of kst.
- Re-add gsl-devel as qt is now compatable with GPLv3.

* Mon Feb 11 2008 Matthew Truch <matt at truch.net> - 1.5.0-3
- Bump release for rebuild.

* Wed Dec 12 2007 Matthew Truch <matt at truch.net> - 1.5.0-2
- Remove BR kdebindings-devel; it is no longer provided for KDE3 in Fedora.
  kst will use its internal kdebindings branch which is older, but should suffice.

* Sun Nov 18 2007 Matthew Truch <matt at truch.net> - 1.5.0-1
- Update to kst 1.5.0 [primarily] bugfix release
- Remove patch to fix open() call; fix was pushed upstream.
- Add autoreconf (and associated BR) as 1.5.0 tarball requires such.

* Tue Nov 13 2007 Matthew Truch <matt at truch.net> - 1.4.0-10
- Remove gsl-devel BuildRequires as gsl is GPLv3+ which is incompatable with qt.

* Sat Nov 10 2007 Matthew Truch <matt at truch.net> - 1.4.0-9
- Bump build to pick up new cfitsio

* Tue Aug 21 2007 Matthew Truch <matt at truch.net> - 1.4.0-8
- Add patch to fix open() call that was not compliant.  

* Thu Aug 2 2007 Matthew Truch <matt at truch.net> - 1.4.0-7
- Update License tag

* Mon Jul 23 2007 Matthew Truch <matt at truch.net> - 1.4.0-6
- Readd kdebindings-devel: KDE4 slipped; will readjust when appropriate.

* Mon Jul 23 2007 Matthew Truch <matt at truch.net> - 1.4.0-5
- kst never needed BR kdebase-devel
- Change BR to kdelibs3-devel for upcoming switch to KDE4 as primary.
- Remove BR kdebindings-devel; kst will use it's internal bindings which
  should suffice until kst 2.0 is released (and switch to KDE4).  
- Fix typo in version of Jesse's changelog entry below from 1.3.0-4 to 1.4.0-4

* Thu Jul 19 2007 Jesse Keating <jkeating@redhat.com> - 1.4.0-4
- Rebuild for new cfitsio

* Tue May 29 2007 Matthew Truch <matt at truch.net> - 1.4.0-3
- Recall that things get installed into %%{buildroot}

* Tue May 29 2007 Matthew Truch <matt at truch.net> - 1.4.0-2
- Remove wmap and scuba2 datasources.  They shouldn't have been included
  in the upstream release.  

* Thu May 17 2007 Matthew Truch <matt at truch.net> - 1.4.0-1
- Update to kst 1.4.0 release.  

* Mon Jan 8 2007 Matthew Truch <matt at truch.net> - 1.3.1-3
- Bump release to pick up newest cfitsio (3.030).

* Fri Jan 5 2007 Matthew Truch <matt at truch.net> - 1.3.1-2
- Include explicit Requires: for cfitsio exact version compiled against.  

* Fri Oct 20 2006 Matthew Truch <matt at truch.net> - 1.3.1-1
- Update to kst 1.3.1 bugfix release.

* Fri Sep 29 2006 Matthew Truch <matt at truch.net> - 1.3.0-2
- Bump release to maintain upgrade path.

* Wed Sep 27 2006 Matthew Truch <matt at truch.net> - 1.3.0-1
- Update to kst 1.3.0 release.

* Mon Aug 28 2006 Matthew Truch <matt at truch.net> - 1.2.1-2
- Bump release to force build in prep. for FC6.

* Thu Mar 23 2006 Matthew Truch <matt at truch.net> - 1.2.1-1
- Update to kst 1.2.1 bugfix release from upstream.

* Sun Mar 12 2006 Matthew Truch <matt at truch.net> - 1.2.0-10
- Yet another tweak to configure options.
- Bump build so new cfitsio version is picked up.

* Sun Feb 26 2006 Matthew Truch <matt at truch.net> - 1.2.0-9
- Improve qt lib and include configure options.

* Sun Feb 26 2006 Matthew Truch <matt at truch.net> - 1.2.0-8
- Bump release due to build issue.

* Sun Feb 26 2006 Matthew Truch <matt at truch.net> - 1.2.0-7
- Teach configure to properly find qt libs and includes.

* Fri Feb 17 2006 Matthew Truch <matt at truch.net> - 1.2.0-6
- Make desktop file appear in proper menu.

* Fri Feb 17 2006 Matthew Truch <matt at truch.net> - 1.2.0-5
- Use a better script for fixing non-relative doc symlinks.
- Install desktop file in proper Fedora location.

* Thu Feb 16 2006 Matthew Truch <matt at truch.net> - 1.2.0-4
- Fix compile flags.
- Take two at fixing non-relative symlinks.  
- Own doc kst directories.

* Wed Feb 15 2006 Matthew Truch <matt at truch.net> - 1.2.0-3
- Fix non-relative symlinks.

* Wed Feb 15 2006 Matthew Truch <matt at truch.net> - 1.2.0-2
- Own all directories.
- Remove redundant build requires.

* Tue Feb 14 2006 Matthew Truch <matt at truch.net> - 1.2.0-1
- Initial fedora specfile for kst based partially on spec file 
  included with kst source.

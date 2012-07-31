%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           python-basemap
Version:        0.99.4
Release:        10%{?dist}
Summary:        Plots data on map projections (with continental and political boundaries) 
Group:          Development/Libraries
License:        LGPLv2+
URL:            http://matplotlib.sourceforge.net/users/toolkits.html 
Source0:        http://downloads.sourceforge.net/matplotlib/basemap-%{version}.tar.gz
Source1:        http://dl.sf.net/matplotlib/basemap-%{version}-examples.tar.gz
#Patch0:         python-basemap-0.99-setup.cfg.patch
#Patch1:         python-basemap-0.99-setup.patch
Patch2:         python-basemap-0.99-datadir.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel, proj-devel, shapelib-devel, numpy-f2py, geos-devel 
BuildRequires:  python-httplib2
Requires:       python-matplotlib >= 0.98, python-basemap-data

%description
Basemap is a matplotlib toolkit that allows you to plot data on map
projections (with continental and political boundaries).

%package -n     python-basemap-examples
Summary:        Example programs and data for python-basemap
Group:          Development/Libraries
License:        Copyright only
Requires:       python-basemap

%description -n python-basemap-examples
%{summary}.

%prep
%setup -q -n basemap-%{version}
#%patch0 -p0
#%patch1 -p0
%patch2 -p1
#Remove the bundled libraries
#mv src/_pyproj.c src/basemap_pycompat.h .
#rm -rf src pyshapelib/shapelib
#rm -rf src goes-2.2.3/
#Remove the data files
rm -rf lib/mpl_toolkits/basemap/data/

%build
export GEOS_LIB="/usr/"
%{__python} setup.py config
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root=$RPM_BUILD_ROOT

# We ship the data in another package
rm -rf $RPM_BUILD_ROOT%{_datadir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changelog README LICENSE_pyshapelib
%exclude %{python_sitearch}/mpl_toolkits/__init__.*
%{python_sitearch}/mpl_toolkits/basemap
%{python_sitearch}/dbflib/
%{python_sitearch}/dap/
%{python_sitearch}/dbflibc.so
%{python_sitearch}/shapelib/
%{python_sitearch}/shapelibc.so
%{python_sitearch}/shptree.so
%{python_sitearch}/*.egg-info
%{python_sitearch}/_geoslib.so

%files -n python-basemap-examples
%defattr(-,root,root,-)
%doc examples/*

%changelog
* Mon Apr 02 2012 Devrim Gunduz <devrim@gunduz.org> - 0.99.4-10
- Rebuild to for geos soname bump.

* Tue Oct 18 2011 Devrim Gunduz <devrim@gunduz.org> - 0.99.4-9
- Rebuild to for geos soname bump.

* Thu Jun 03 2010 Jef Spaleta <jspaleta@fedoraproject.org> - 0.99.4-8
- update the homepage url 

* Fri May 28 2010 Jef Spaleta <jspaleta@fedoraproject.org> - 0.99.4-7
- Examples is now a subpackage of python-basemap instead of python-basemap-data 

* Mon Apr 12 2010 Jef Spaleta <jspaleta@fedoraproject.org> - 0.99.4-6
- Fix the data directory patch. 

* Mon Apr 12 2010 Jef Spaleta <jspaleta@fedoraproject.org> - 0.99.4-5
- Rebuild to for geos soname bump and numpy 1.3 reversion. 

* Thu Apr 01 2010 Jef Spaleta <jspaleta@fedoraproject.org> - 0.99.4-4
- Added back the data directory patch. It is needed to correctly set the 
  default location of system data files provided by the python-basemap-data 
  package.  Setting the environment variable at build time is not sufficient 
  to set the correct system-wide location for distribution packaging.  

* Thu Apr 01 2010 Jef Spaleta <jspaleta@fedoraproject.org> - 0.99.4-3
- Rebuild to fix numpy ABI change.

* Fri Jan 08 2010 Jon Ciesla <limb@jcomserv.net> - 0.99.4-2
- Rebuild for broken dep.

* Fri Dec 11 2009 Jon Ciesla <limb@jcomserv.net> - 0.99.4-1
- Update to latest upstream.
- Dropped datadir patch, now handled with environment variable.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Caolán McNamara <caolanm@redhat.com> - 0.99.2-4
- Resolves: rhbz#511576 FTBFS showimg numpy -> numpy-f2py

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 11 2008 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.99.2-2
- Update data directory patch

* Thu Dec 11 2008 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.99.2-1
- Update to latest release

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.99-6
- Rebuild for Python 2.6

* Thu Oct 23 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.99-5
- Also patch runtime GEOS version check (as discussed on the fedora-devel-list)

* Sun Oct 19 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.99-4
- Update -setup.py patch for geos 3.0.1

* Sun Oct 19 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.99-3
- Rebuild for new geos, fixes broken deps

* Fri Jul 11 2008 Jef Spaleta <jspaleta AT fedoraproject DOT org> 0.99-2
- File conflict fix for Bug 455005

* Wed Jul 02 2008 Jef Spaleta <jspaleta AT fedoraproject DOT org> 0.99-1
- Update to match latest matplotlib 

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.5-5
- Autorebuild for GCC 4.3

* Fri Jan 04 2008 Jef Spaleta <jspaleta@fedoraproject.org> 0.9.5-4
- Fix for egg-info file creation

* Thu Aug 23 2007 Orion Poplawski <orion@cora.nwra.com> 0.9.5-3
- Explicitly remove included libraries in prep
- Update license tag to LGPLv2+
- Rebuild for BuildID

* Wed Jun 06 2007 Orion Poplawski <orion@cora.nwra.com> 0.9.5-2
- Rebuild

* Fri Mar 23 2007 Orion Poplawski <orion@cora.nwra.com> 0.9.5-1
- Update to 0.9.5
- Ship the examples in a separate rpm

* Mon Dec 11 2006 Orion Poplawski <orion@cora.nwra.com> 0.9.4-2
- Remove unnecessary (and damaging) line ending change

* Mon Nov 20 2006 Orion Poplawski <orion@cora.nwra.com> 0.9.4-1
- Update to upstream 0.9.4

* Wed Oct 18 2006 Orion Poplawski <orion@cora.nwra.com> 0.9.3-1
- Update to upstream 0.9.3

* Thu Sep  7 2006 Orion Poplawski <orion@cora.nwra.com> 0.9.2-1
- Update to upstream 0.9.2

* Fri Jul 28 2006 Orion Poplawski <orion@cora.nwra.com> 0.9.1-1
- Update to upstream 0.9.1

* Mon Jul  3 2006 Orion Poplawski <orion@cora.nwra.com> 0.9-1
- Update to upstream 0.9

* Mon Mar  6 2006 Orion Poplawski <orion@cora.nwra.com> 0.8.2-3
- Rebuild for updated shapelib

* Tue Feb 28 2006 Orion Poplawski <orion@cora.nwra.com> 0.8.2-2
- python-matplotlib now owns toolkits directoery

* Mon Feb 27 2006 Orion Poplawski <orion@cora.nwra.com> 0.8.2-1
- Update to upstream 0.8.2

* Fri Feb 24 2006 Orion Poplawski <orion@cora.nwra.com> 0.8.1-1
- Update to upstream 0.8.1

* Sun Nov 20 2005 Orion Poplawski <orion@cora.nwra.com> 0.7.2.1-1
- Update to upstream 0.7.2.1
- Split into python-basemap and python-basemap-data
- No longer requires python-numarray
- Use system shapelib for pyshapelib components

* Tue Sep 13 2005 Orion Poplawski <orion@cora.nwra.com> 0.6.2-1
- Update to upstream 0.6.2

* Tue Aug 02 2005 Orion Poplawski <orion@cora.nwra.com> 0.5.2-1
- Initial package for Fedora Extras

%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           python-basemap-data
Version:        0.99.4
Release:        2%{?dist}
Summary:        Data for python-basemap
Group:          Development/Libraries
License:        GPLv2 and Public Domain
URL:            http://matplotlib.sourceforge.net/matplotlib.toolkits.basemap.basemap.html
Source0:        http://dl.sf.net/matplotlib/basemap-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel

%description
Data for python-basemap


%package        hires
Summary:        High resolution map data for python-basemap
Group:          Development/Libraries
License:        GPLv2
Requires:       python-basemap-data

%description    hires
%{summary}.




%prep
%setup -q -n basemap-%{version}



%build


%install
rm -rf $RPM_BUILD_ROOT
# Install the data
install -d $RPM_BUILD_ROOT%{_datadir}
cp -a lib/mpl_toolkits/basemap/data/ $RPM_BUILD_ROOT%{_datadir}/basemap


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README LICENSE_data
%{_datadir}/basemap/
%exclude %{_datadir}/basemap/*_h.dat


%files hires
%defattr(-,root,root,-)
%doc LICENSE_data
%{_datadir}/basemap/*_h.dat




%changelog
* Fri May 28 2010 Jef Spaleta <jspaleta AT fedoraproject DOT org> 0.99.4-2
- Move python-basemap-examples subpackage to python-basemap srpm 
- Make it possible to install python-basemap-data without python-basemap

* Fri Dec 11 2009 Jon Ciesla <limb@jcomserv.net> - 0.99.4-1
- Update to latest upstream.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 11 2008 Jef Spaleta <jspaleta AT fedoraproject DOT org> 0.99.2-1
- Update to latest release

* Thu Dec 11 2008 Jef Spaleta <jspaleta AT fedoraproject DOT org> 0.99.1-1
- Update to match matplotlib release

* Thu Aug 23 2007 Orion Poplawski <orion@cora.nwra.com> 0.9.5-3
- Update license tags

* Thu Mar 29 2007 Orion Poplawski <orion@cora.nwra.com> 0.9.5-2
- Change Requires from /usr/share/basemap to python-basemap

* Wed Mar 28 2007 Orion Poplawski <orion@cora.nwra.com> 0.9.5-1
- Split into regular and -hires packages
- Ship the basemap examples in python-basemap-examples

* Mon Feb 19 2007 Orion Poplawski <orion@cora.nwra.com> 0.9-2
- Add BR: python-devel

* Mon Jul  3 2006 Orion Poplawski <orion@cora.nwra.com> 0.9-1
- Update to 0.9

* Fri Feb 24 2006 Orion Poplawski <orion@cora.nwra.com> 0.8-1
- Update to 0.8

* Sun Nov 20 2005 Orion Poplawski <orion@cora.nwra.com> 0.7-1
- Initial package for Fedora Extras

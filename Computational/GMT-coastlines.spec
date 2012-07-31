Name:           GMT-coastlines
Version:        2.1.0
Release:        1%{?dist}.1
Summary:        Coastline data for GMT

Group:          Applications/Engineering
License:        GPLv2
URL:            http://gmt.soest.hawaii.edu/
# seems to be derived at least from 2 Public Domain datasets, 
# CIA World DataBank II and World Vector Shoreline (already in fedora),
# then modified.
Source0:        ftp://ftp.soest.hawaii.edu/gmt/GSHHS%{version}_coast.tar.bz2
Source1:        ftp://ftp.soest.hawaii.edu/gmt/GSHHS%{version}_full.tar.bz2
Source2:        ftp://ftp.soest.hawaii.edu/gmt/GSHHS%{version}_high.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Provides:       gmt-coastlines = %{version}-%{release}
#Requires:       GMT-common


%description
Crude, low, and intermediate resolutions coastline data for GMT.


%package        full
Summary:        Full resolution coastline data for GMT
Group:          Applications/Engineering
Requires:       GMT-coastlines
Provides:       gmt-coastlines = %{version}-%{release}

%description    full
%{summary}.


%package        high
Summary:        High resolution coastline data for GMT
Group:          Applications/Engineering
Requires:       GMT-coastlines
Provides:       gmt-coastlines = %{version}-%{release}

%description    high
%{summary}.


%package        all
Summary:        All coastline data for GMT
Group:          Applications/Engineering
Requires:       GMT-coastlines
Requires:       GMT-coastlines-full
Requires:       GMT-coastlines-high
Provides:       gmt-coastlines-all = %{version}-%{release}

%description    all
%{summary}.


%prep
%setup -q -c -b1 -b2


%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}/%{_datadir}/GMT
cp -a share/coast  ${RPM_BUILD_ROOT}/%{_datadir}/GMT/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE.TXT README.TXT
%dir %{_datadir}/GMT/coast
%{_datadir}/GMT/coast/*_[cil].cdf

%files full
%defattr(-,root,root,-)
%{_datadir}/GMT/coast/*_f.cdf

%files high
%defattr(-,root,root,-)
%{_datadir}/GMT/coast/*_h.cdf

%files all
%defattr(-,root,root,-)


%changelog
* Fri Dec 3 2010 Orion Poplawski <orion@cora.nwra.com> 2.1.0-1.1
- Drop Requires: GMT-common for bootstrap

* Tue Jul 20 2010 Orion Poplawski <orion@cora.nwra.com> 2.1.0-1
- Update to 2.1.0

* Tue Jan 26 2010 Orion Poplawski <orion@cora.nwra.com> 2.0.2-1
- Update to 2.0.2

* Thu Nov 19 2009 Orion Poplawski <orion@cora.nwra.com> 2.0.1-2
- Require GMT-common instead for directory ownership

* Fri Oct 16 2009 Orion Poplawski <orion@cora.nwra.com> 2.0.1-1
- Update to 2.0.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Orion Poplawski <orion@cora.nwra.com> 2.0-1
- Update to 2.0

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Orion Poplawski <orion@cora.nwra.com> 1.10-2
- Add Requires: GMT to get needed directories (bug #473592)

* Mon May 5 2008 Orion Poplawski <orion@cora.nwra.com> 1.10-1
- Update to 1.10

* Fri Apr 25 2008 Orion Poplawski <orion@cora.nwra.com> 1.9-3
- Add lowercase provides
- Fix URLs and timestamps
- Add comment about source

* Mon Mar 24 2008 Orion Poplawski <orion@cora.nwra.com> 1.9-2
- Merged version

* Mon Mar 17 2008 Orion Poplawski <orion@cora.nwra.com> 1.9-1
- Initial version

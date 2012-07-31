Name:           ncview
Version:        1.93c
Release:        6%{?dist}
Summary:        A visual browser for netCDF format files
Group:          Applications/Engineering
License:        GPLv1
URL:            http://meteora.ucsd.edu/~pierce/ncview_home_page.html
Source0:        ftp://cirrus.ucsd.edu/pub/ncview/ncview-1.93c.tar.gz
Patch0:         ncview-1.92e-Makefile.in.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  xorg-x11-proto-devel libXaw-devel libXt-devel libXext-devel
BuildRequires:  libXmu-devel libICE-devel libSM-devel libX11-devel
BuildRequires:  netcdf-devel udunits-devel netpbm-devel
Requires:       udunits

%description
Ncview is a visual browser for netCDF format files.  Typically you
would use ncview to get a quick and easy, push-button look at your
netCDF files.  You can view simple movies of the data, view along
various dimensions, take a look at the actual data values, change
color maps, invert the data, etc.

%prep
%setup -q
%patch0 -p1
#%patch1 -p1

%build
%configure --with-netcdf_incdir=%{_includedir} \
 --x-libraries=%{_libdir}  --datadir=%{_datadir}/ncview
#  WARNING!
#  The parallel build was tested and it does NOT work.
#  make %{?_smp_mflags}
make
sed s=NCVIEW_LIB_DIR=%{_datadir}/ncview= < ncview.1.sed > ncview.1

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/X11/app-defaults
cp -p Ncview-appdefaults ${RPM_BUILD_ROOT}%{_datadir}/X11/app-defaults/Ncview
#cat > install-appdef <<EOF
##!/bin/bash
#echo "no longer needed"
#EOF
%makeinstall NCVIEW_LIB_DIR=${RPM_BUILD_ROOT}%{_datadir}/ncview BINDIR=${RPM_BUILD_ROOT}%{_bindir} MANDIR=${RPM_BUILD_ROOT}%{_mandir}/man1
mkdir ${RPM_BUILD_ROOT}%{_datadir}/ncview/
install -m0644 -p *.ncmap nc_overlay* ${RPM_BUILD_ROOT}%{_datadir}/ncview/
chmod 644 ${RPM_BUILD_ROOT}%{_datadir}/X11/app-defaults/Ncview
chmod 644 ${RPM_BUILD_ROOT}%{_mandir}/man1/*


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README COPYING
%{_bindir}/*
%{_datadir}/ncview/
%{_datadir}/X11/app-defaults/Ncview
%{_mandir}/man1/*


%changelog
* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.93c-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.93c-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Aug 26 2008 Adam Jackson <ajax@redhat.com> 1.93c-4
- Drop Requires: xorg-x11-server-Xorg.

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.93c-3
- fix patch to apply with fuzz=0

* Thu Apr 10 2008 Patrice Dumas <pertusus@free.fr> - 1.93c-2
- update to 1.93c

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.92e-13
- Autorebuild for GCC 4.3

* Sat Aug 25 2007 Ed Hill <ed@eh3.com> - 1.92e-12
- add BR: netcdf-static

* Sat Aug 25 2007 Ed Hill <ed@eh3.com> - 1.92e-11
- rebuild for BuildID

* Tue Nov 14 2006 Ed Hill <ed@eh3.com> - 1.92e-10
- more cleanups for check-buildroot

* Tue Nov 14 2006 Ed Hill <ed@eh3.com> - 1.92e-9
- bz 215632

* Sat Sep  2 2006 Ed Hill <ed@eh3.com> - 1.92e-8
- rebuild for imminent FC-6 release

* Thu Feb 16 2006 Ed Hill <ed@eh3.com> - 1.92e-7
- rebuild for new gcc

* Sun Nov 20 2005 Ed Hill <ed@eh3.com> - 1.92e-6
- update for the new modular xorg-x11

* Wed Aug  3 2005 Ed Hill <ed@eh3.com> - 1.92e-5
- fix dist tag

* Wed Jul  6 2005 Ed Hill <ed@eh3.com> - 1.92e-4
- mkstemp() security fix and more cleanups

* Wed Jul  6 2005 Ed Hill <ed@eh3.com> - 1.92e-3
- move the data files to %%{_datadir} and add COPYING
- added xorg-x11 Requires and BuildRequires

* Tue Jul  5 2005 Ed Hill <ed@eh3.com> - 1.92e-2
- fix permissions, remove fortran dependency, and small cleanups

* Tue Jul  5 2005 Tom "spot" Callaway <tcallawa@redhat.com> - 1.92e-1
- Fedora Extras cleanups

* Sun Dec  5 2004 Ed Hill <eh3@mit.edu> - 0:1.92e-0.fdr.0
- Initial version


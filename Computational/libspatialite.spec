Name:      libspatialite
Version:   2.4.0
Release:   0.6.RC4%{?dist}
Summary:   Enables SQLite to support spatial data
Group:     System Environment/Libraries
License:   MPLv1.1
URL:       http://www.gaia-gis.it/spatialite
Source0:   http://www.gaia-gis.it/spatialite-2.4.0-4/%{name}-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: proj-devel geos-devel sqlite-devel

# https://bugzilla.redhat.com/show_bug.cgi?id=663938
ExcludeArch: ppc64

%description
SpatiaLite extension enables SQLite to support spatial data, in
a way conformant to OpenGIS specifications. It implements
spatial indices, spatial functions and supports metadata.

%package devel
Summary: Development Libraries for the SpatiaLite extension
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
# Geocallbacks work with SQLite 3.7.3, available in F15, but not in RHEL yet.
%if (0%{?fedora} < 15 || 0%{?rhel})
%configure \
    --disable-static \
    --disable-geocallbacks
%else
%configure --disable-static
%endif

make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

# Delete undesired libtool archives
rm -f %{buildroot}/%{_libdir}/%{name}.la


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files 
%defattr(-,root,root,-)
%doc COPYING AUTHORS
%{_libdir}/%{name}.so.*


%files devel
%defattr(-,root,root,-)
%{_includedir}/spatialite.h
%{_includedir}/spatialite/*
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/spatialite.pc


%changelog
* Wed Dec 8 2010 Volker Fröhlich <volker27@gmx.at> 2.4.0-0.6.RC4
- Exclude ppc64

* Tue Dec 7 2010 Volker Fröhlich <volker27@gmx.at> 2.4.0-0.5.RC4
- Corrected wrong Fedora version number in if-statement

* Sun Dec 5 2010 Volker Fröhlich <volker27@gmx.at> 2.4.0-0.4.RC4
- Refined configure condition to support RHEL

* Fri Dec 3 2010 Volker Fröhlich <volker27@gmx.at> 2.4.0-0.3.RC4
- Added buildroot
- Added doc files

* Wed Dec 1 2010 Volker Fröhlich <volker27@gmx.at> 2.4.0-0.2.RC4
- Added description of devel package
- Switched to disable-static flag

* Sun Nov 28 2010 Volker Fröhlich <volker27@gmx.at> 2.4.0-0.1.RC4
- Initial packaging for Fedora

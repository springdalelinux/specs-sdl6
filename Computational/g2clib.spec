Name:           g2clib
Version:        1.2.0
Release:        1%{?dist}
Summary:        GRIB2 encoder/decoder and search/indexing routines in C

Group:          System Environment/Libraries
License:        Public Domain
URL:            http://www.nco.ncep.noaa.gov/pmb/codes/GRIB2/
Source0:        http://www.nco.ncep.noaa.gov/pmb/codes/GRIB2/g2clib-%{version}.tar
Source1:        g2clib-msg.txt
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libpng-devel jasper-devel
#Requires:       

%description
This library contains "C" decoder/encoder
routines for GRIB edition 2.  The user API for the GRIB2 routines
is described in file "grib2c.doc".


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
#Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-static = %{version}-%{release}
Requires:       libpng-devel jasper-devel

%description    devel
This library contains "C" decoder/encoder
routines for GRIB edition 2.  The user API for the GRIB2 routines
is described in file "grib2c.doc".

The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
chmod a-x *.h *.c README CHANGES grib2c.doc makefile
cp -p %{SOURCE1} .


%build
make CFLAGS="$RPM_OPT_FLAGS -DUSE_PNG -DUSE_JPEG2000" \
  CC="%{__cc}" ARFLAGS=


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_includedir}
install -p -m0644 libgrib2c.a $RPM_BUILD_ROOT%{_libdir}
install -p -m0644 grib2.h $RPM_BUILD_ROOT%{_includedir}


%clean
rm -rf $RPM_BUILD_ROOT


%files devel
%defattr(-,root,root,-)
%doc README CHANGES grib2c.doc g2clib-msg.txt
%{_libdir}/libgrib2c.a
%{_includedir}/grib2.h


%changelog
* Fri Apr 16 2010 Orion Poplawski <orion@cora.nwra.com> - 1.2.0-1
- Update to 1.2.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Orion Poplawski <orion@cora.nwra.com> - 1.1.9-1
- Update to 1.1.9

* Fri Apr 17 2009 Orion Poplawski <orion@cora.nwra.com> - 1.1.8-1
- Update to 1.1.8

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Aug 28 2008 Orion Poplawski <orion@cora.nwra.com> - 1.1.7-1
- Update to 1.1.7
- Add quotes around %%{__cc} as it can be multi-word

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.5-4
- Autorebuild for GCC 4.3

* Tue Jan 22 2008 Orion Poplawski <orion@cora.nwra.com> 1.0.5-3
- Remove %%{?_smp_mflags}, makefile is not parallel make safe

* Fri Dec 14 2007 Patrice Dumas <pertusus@free.fr> 1.0.5-2
- Add the mail message precising the license

* Thu Dec 13 2007 Orion Poplawski <orion@cora.nwra.com> 1.0.5-1
- Update to 1.0.5

* Fri Aug 24 2007 Patrice Dumas <pertusus@free.fr> 1.0.4-1
- initial packaging

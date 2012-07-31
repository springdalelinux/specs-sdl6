Name:      qwtpolar
Version:   0.1.0
Release:   5%{?dist}
Summary:   Qwt/Qt Polar Plot Library
Group:     System Environment/Libraries
License:   LGPLv2 with exceptions
URL:       http://qwtpolar.sourceforge.net/
Source0:   http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2

# Introduces placeholders in Qmake's .pri file to be substituted later
Patch0:    %{name}-%{version}-path.patch
Patch1:    %{name}-%{version}-api.patch
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: qwt-devel
BuildRequires: doxygen

%description
The QwtPolar library contains classes for displaying values on a polar
coordinate system. It is an add-on package for the Qwt Library.

%package devel
Summary:        Development Libraries for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains the files necessary
to develop applications using QwtPolar.

%prep
%setup -q
%patch0 -p1 -b .path
%patch1 -p1 -b .api

# Make the Makefile verbose, set include- and lib paths, as well as the path for documentation
sed -i "/silent/d" qwtpolar.pri
sed -i "s\LIBPATH\ %{_libdir}\1" qwtpolar.pri
sed -i "s\HEADERPATH\ %{_includedir}/%{name}\1" qwtpolar.pri
sed -i "s\DOCPATH\ %{_docdir}/%{name}-%{version}\1" qwtpolar.pri
sed -i "s|/path/to/qwt-5.2/include|%{_includedir}/qwt|" qwtpolar.pri
sed -i "s|/path/to/qwt-5.2/lib|%{_libdir}|" qwtpolar.pri

# Don't link pthread and rather use -O2 as linker optimization level
# These two settings come from:
# /usr/lib64/qt4/mkspecs/common/linux.conf
# /usr/lib64/qt4/mkspecs/common/g++-multilib.conf
sed -i "/qt/iQMAKE_LIBS_THREAD -= -lpthread" qwtpolar.pri
sed -i "/qt/iQMAKE_LFLAGS_RELEASE ~= s\/-O1\/-O2" qwtpolar.pri

chmod 644 COPYING

%build
qmake-qt4
#Not parallel build proof
make

pushd doc
doxygen Doxyfile
popd

%install
make install INSTALL_ROOT=%{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files 
%doc COPYING CHANGES
%{_libdir}/lib%{name}.so.*

%files devel
%doc doc/html examples
%{_includedir}/%{name}
%{_libdir}/qt4/plugins/designer/libqwt_polar_designer_plugin.so
%{_libdir}/lib%{name}.so

%changelog
* Mon Jul 11 2011 Volker Fröhlich <volker27@gmx.at> 0.1.0-5
- Don't build with multiple workers

* Thu Jul 07 2011 Volker Fröhlich <volker27@gmx.at> 0.1.0-4
- Replace optimization on linker call and remove pthread link
- Explicit make call
- Produce proper developer documentation
- Drop defattr lines

* Sat Jun 06 2011 Volker Fröhlich <volker27@gmx.at> 0.1.0-3
- Removed waste word from description

* Sat May 21 2011 Volker Fröhlich <volker27@gmx.at> 0.1.0-2
- Use upstream's summary

* Sat May 21 2011 Volker Fröhlich <volker27@gmx.at> 0.1.0-1
- Initial packaging for Fedora

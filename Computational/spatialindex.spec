Name:      spatialindex
Version:   1.6.1
Release:   3%{?dist}
Summary:   Spatial index library 
Group:     System Environment/Libraries
License:   LGPLv2+
URL:       http://trac.gispython.org/spatialindex
Source0:   http://download.osgeo.org/lib%{name}/%{name}-src-%{version}.tar.bz2

%description
Spatialindex provides a general framework for developing spatial indices.
Currently it defines generic interfaces, provides simple main memory and
disk based storage managers and a robust implementation of an R*-tree,
an MVR-tree and a TPR-tree.

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for %{name}.

# Correct FSF postal address
# Request sent to spatialindex@lists.gispython.org
sed -i 's/59 Temple Place, Suite 330/51 Franklin Street, Fifth Floor/' COPYING
sed -i 's/02111-1307/02110-1301/' COPYING

#TODO: Undefined symbols
# ldd -d -r /usr/lib64/libspatialindex.so.1.0.0

%prep
%setup -qn %{name}-src-%{version}
chmod -x include/tools/*.h

%build
%configure

# Remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
make install INSTALL='install -p' DESTDIR=%{buildroot}

# Delete libtool archives, because we don't ship them.
pushd %{buildroot}%{_libdir} 
  rm -f *.a *.la
popd

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files 
%doc AUTHORS ChangeLog COPYING README
%{_libdir}/lib%{name}*.so.*

%files devel
%{_includedir}/%{name}
%{_libdir}/lib%{name}*.so

%changelog
* Thu Aug 04 2011 Volker Fröhlich <volker27@gmx.at> - 1.6.1-3
- Preserve timestamps by using install -p

* Thu Aug 04 2011 Volker Fröhlich <volker27@gmx.at> - 1.6.1-2
- Generalized file list to avoid specifying so-version
- Adapt Require in sub-package to guidelines
- Removed BR chrpath; using approach from
  http://fedoraproject.org/wiki/Packaging:Guidelines#Removing_Rpath
- Correct FSF postal address

* Thu Jun 02 2011 Volker Fröhlich <volker27@gmx.at> - 1.6.1-1
- Initial packaging

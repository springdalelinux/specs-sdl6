Name:           libmspack
Version:        0.2
Release:        0.1.20100723alpha%{?dist}
Summary:        Library for CAB and related files compression and decompression

Group:          System Environment/Libraries
License:        LGPLv2
URL:            http://www.cabextract.org.uk/libmspack/
Source0:        http://www.cabextract.org.uk/libmspack/%{name}-%{version}alpha.tar.gz
Patch0:         %{name}-0.2alpha-doc.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  doxygen


%description
The purpose of libmspack is to provide both compression and decompression of 
some loosely related file formats used by Microsoft.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Obsoletes:      %{name}-doc < 0.2

%description    devel
The %{name}-devel package contains libraries, header files and documentation
for developing applications that use %{name}.


%prep
%setup -q -n %{name}-%{version}alpha
%patch0 -p1

chmod a-x mspack/mspack.h


%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
rm $RPM_BUILD_ROOT%{_libdir}/libmspack.la

iconv -f ISO_8859-1 -t utf8 ChangeLog --output Changelog.utf8
touch -r ChangeLog Changelog.utf8
mv Changelog.utf8 ChangeLog

pushd doc
doxygen
find html -type f | xargs touch -r %{SOURCE0}
rm -f html/installdox
popd


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc README TODO COPYING.LIB ChangeLog AUTHORS
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/html
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Mon Aug 30 2010 Dan Horák <dan[at]danny.cz> - 0.2-0.1.20100723alpha
- updated to 0.2alpha released 2010/07/23
- merged the doc subpackage with devel

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0-0.7.20060920alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0-0.6.20060920alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 13 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.0-0.5-20060920alpha
- Rebuild for gcc4.3

* Sun Jan 20 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.0-0.4.20060920alpha
- installed documentation into html subdir
- manually installed doc's for main package

* Sun Jan 20 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.0-0.3.20060920alpha
- Got source using wget -N
- Removed some doc's
- Shifted doc line for doc package
- Added install -p

* Sun Jan 20 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.0-0.2.20060920alpha
- Changed install script for doc package
- Fixed rpmlint issue with debug package

* Fri Jan 18 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 20060920cvs.a-1
- Initial release

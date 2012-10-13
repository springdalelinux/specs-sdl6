Name:           qrencode
Version:        3.1.1
Release:        5%{?dist}
Summary:        Generate QR 2D barcodes

Group:          Applications/Engineering
License:        LGPLv2+
URL:            http://megaui.net/fukuchi/works/qrencode/index.en.html
Source0:        http://megaui.net/fukuchi/works/qrencode/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libpng-devel chrpath


%description
Qrencode is a utility software using libqrencode to encode string data in
a QR Code and save as a PNG image.

%package        devel
Summary:        QR Code encoding library - Development files
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The qrencode-devel package contains libraries and header files for developing
applications that use qrencode.

%prep
%setup -q


%build
%configure --with-tests
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -rf $RPM_BUILD_ROOT%{_libdir}/libqrencode.la
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/qrencode

%check
cd ./tests
sh test_all.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING NEWS README TODO
%{_bindir}/qrencode
%{_mandir}/man1/qrencode.1.*
%{_libdir}/libqrencode.so.3
%{_libdir}/libqrencode.so.3.1.1

%files devel
%defattr(-,root,root,-)
%{_includedir}/qrencode.h
%{_libdir}/libqrencode.so
%{_libdir}/pkgconfig/libqrencode.pc


%changelog
* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 13 2010 Tareq Al Jurf <taljurf@fedoraproject.org> - 3.1.1-4
- Fixed the rpath problem.

* Mon Jul 12 2010 Tareq Al Jurf <taljurf@fedoraproject.org> - 3.1.1-3
- Fixed some small spec mistakes.

* Mon Jul 12 2010 Tareq Al Jurf <taljurf@fedoraproject.org> - 3.1.1-2
- Fixed some small errors.

* Thu Jul 08 2010 Tareq Al Jurf <taljurf@fedoraproject.org> - 3.1.1-1
- Initial build.

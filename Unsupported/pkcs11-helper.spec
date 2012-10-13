Name:           pkcs11-helper
Version:        1.07
Release:        5%{?dist}
Summary:        A library for using PKCS#11 providers

Group:          System Environment/Libraries
License:        GPLv2 or BSD
URL:            http://www.opensc-project.org/pkcs11-helper/
Source0:        http://www.opensc-project.org/files/%{name}/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  doxygen graphviz
BuildRequires:  openssl-devel

%description
pkcs11-helper is a library that simplifies the interaction with PKCS#11
providers for end-user applications using a simple API and optional OpenSSL
engine. The library allows using multiple PKCS#11 providers at the same time,
enumerating available token certificates, or selecting a certificate directly
by serialized id, handling card removal and card insert events, handling card
re-insert to a different slot, supporting session expiration and much more all
using a simple API. 

%package        devel
Summary:        Development files for pkcs11-helper
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       openssl-devel
# for /usr/share/aclocal
Requires:       automake

%description    devel
This package contains header files and documentation necessary for developing
programs using the pkcs11-helper library.


%prep
%setup -q


%build
%configure --disable-static --enable-doc
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# Use %%doc to install documentation in a standard location
mkdir apidocdir
mv $RPM_BUILD_ROOT%{_datadir}/doc/%{name}/api/ apidocdir/
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/%{name}/

# Remove libtool .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING* README THANKS
%{_libdir}/libpkcs11-helper.so.*


%files devel
%defattr(-,root,root,-)
%doc apidocdir/*
%{_includedir}/pkcs11-helper-1.0/
%{_libdir}/libpkcs11-helper.so
%{_libdir}/pkgconfig/libpkcs11-helper-1.pc
%{_datadir}/aclocal/pkcs11-helper-1.m4
%{_mandir}/man8/pkcs11-helper-1.8*


%changelog
* Thu Jul 01 2010 Kalev Lember <kalev@smartlink.ee> - 1.07-5
- use System Environment/Libraries group for main package
- removed R: pkgconfig from devel subpackage

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.07-4
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 11 2009 Kalev Lember <kalev@smartlink.ee> - 1.07-2
- Make devel package depend on automake for /usr/share/aclocal

* Tue Jun 23 2009 Kalev Lember <kalev@smartlink.ee> - 1.07-1
- Initial RPM release.

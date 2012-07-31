Name:		ftplib
Version:	3.1
Release:	6%{?dist}
Summary:	Library of FTP routines
Group:		System Environment/Libraries
License:	LGPLv2+
URL:		http://nbpfaus.net/~pfau/ftplib/
Source0:	http://nbpfaus.net/~pfau/ftplib/%{name}-%{version}-1.tar.gz
Patch0:		ftplib-3.1-1-modernize.patch
BuildRoot:  	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
ftplib is a set of routines that implement the FTP protocol. They allow 
applications to create and access remote files through function calls 
instead of needing to fork and exec an interactive ftp client program.

%package devel
Summary:	Development files for ftplib
Group:		Development/Libraries
Requires:	ftplib = %{version}-%{release}

%description devel
Development libraries and headers for ftplib.

%package -n qftp
Summary:	Simple ftp client application
Group:		Applications/Internet
License:	GPLv2+

%description -n qftp
Command line driven ftp file transfer program using ftplib.

%prep
%setup -q -n %{name}-%{version}-1
%patch0 -p1

%build
cd src/
make %{?_smp_mflags} DEBUG="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT 
mkdir $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}
cd src/
make DESTDIR=$RPM_BUILD_ROOT LIBDIR="%{_libdir}" install

cd ${RPM_BUILD_ROOT}%{_libdir}
chmod +x libftp.so.3.1
ln -sf libftp.so.3.1 libftp.so.3
ln -sf libftp.so.3 libftp.so

cd ${RPM_BUILD_ROOT}%{_bindir}
for f in ftpdir ftpget ftplist ftprm ftpsend; do
	ln -s qftp $f
done

%clean
rm -rf $RPM_BUILD_ROOT 

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc CHANGES TODO NOTES
%{_libdir}/libftp*.so.*

%files devel
%defattr(-,root,root)
%doc additional_rfcs README.ftplib* RFC959.txt html/
%{_includedir}/ftplib.h
%{_libdir}/libftp*.so

%files -n qftp
%defattr(-,root,root)
%doc README.qftp
%{_bindir}/ftpdir
%{_bindir}/ftpget
%{_bindir}/ftplist
%{_bindir}/ftprm
%{_bindir}/ftpsend
%{_bindir}/qftp

%changelog
* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.1-4
- Autorebuild for GCC 4.3

* Thu Aug 23 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 3.1-3
- fix licensing (v2+)
- rebuild for BuildID (F-8)

* Mon Jun  4 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 3.1-2
- fix licensing (libs LGPL, qftp GPL)

* Mon Jun  4 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 3.1-1
- initial build for Fedora

Name:		libprojectM-qt
Version:	2.0.1
Release:	2%{?dist}
Summary:	The Qt frontend to the projectM visualization plugin
Group:		Applications/Multimedia
License:	GPLv2+
URL:		http://projectm.sourceforge.net/
Source0:	http://downloads.sourceforge.net/projectm/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	cmake, qt4-devel, libprojectM-devel = %{version}

%description
projectM-qt is a GUI designed to enhance the projectM user and preset writer
experience.  It provides a way to browse, search, rate presets and setup
preset playlists for projectM-jack and projectM-pulseaudio.

%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}, pkgconfig, libprojectM-devel, qt-devel

%description	devel
projectM-qt is a GUI designed to enhance the projectM user and preset writer
experience.  It provides a way to browse, search, rate presets and setup
preset playlists for projectM-jack and projectM-pulseaudio.
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} -DLIB_INSTALL_DIR=%{_libdir} .
make %{?_smp_mflags} VERBOSE=1


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%{_datadir}/pixmaps/prjm16-transparent.svg

%files devel
%defattr(-,root,root,-)
%doc ReadMe
%{_includedir}/%{name}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Sat Jan 16 2010 Jameson Pugh (imntreal@gmail.com) - 2.0.1-2
- Rebuilding due to libprojectM SONAME bump

* Sun Dec 13 2009 Jameson Pugh (imntreal@gmail.com) - 2.0.1-1
- New release

* Mon Oct 12 2009 Jameson Pugh (imntreal@gmail.com) - 1.2.0r1300-1
- New SVN version to prepare for v2

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 9 2008 Jameson Pugh (imntreal@gmail.com) - 1.2.0-4
- Changed qt-devel to qt4-devel for F8

* Thu Nov 6 2008 Jameson Pugh (imntreal@gmail.com) - 1.2.0-3
- Removed superfluous line to get rid of .la files
- Cleaned up Requires
- Added to devel Requires

* Thu Nov 6 2008 Jameson Pugh (imntreal@gmail.com) - 1.2.0-2
- Fixed mixed use of tabs/spaces
- Corrected SOURCE0
- Removed doc until there is a license in the tarball
- Added cmake to BR
- Added a patch to fix the libsuffix issue in the pc file

* Wed Sep 3 2008 Jameson Pugh <imntreal@gmail.com> - 1.2.0-1
- Initial public release of the package

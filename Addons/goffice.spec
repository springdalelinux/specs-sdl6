Name:           goffice         
Version:        0.8.12
Release:        1%{?dist}
Summary:        Goffice support libraries
Group:          System Environment/Libraries
# bug filed upstream about this being GPL v2 only:
# http://bugzilla.gnome.org/show_bug.cgi?id=463248
License:        GPLv2
URL:            http://freshmeat.net/projects/goffice/
Source0:        http://ftp.acc.umu.se/pub/GNOME/sources/%{name}/%{version}/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libgsf-gnome-devel     >= 1.13.3
BuildRequires:  libgnomeui-devel       >= 2.0.0
BuildRequires:  intltool gettext

%description
Support libraries for gnome office


%package devel
Summary:        Libraries and include files for goffice
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libgsf-gnome-devel     >= 1.13.3
Requires:       libgnomeui-devel       >= 2.0.0
Requires:       pkgconfig

%description devel
Development libraries for goffice


%prep
%setup -q


%build
%configure --disable-dependency-tracking
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
%find_lang goffice-%{version}
rm $RPM_BUILD_ROOT/%{_libdir}/*.la
rm $RPM_BUILD_ROOT/%{_libdir}/%{name}/%{version}/plugins/*/*.la


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%clean
rm -rf $RPM_BUILD_ROOT


%files -f goffice-%{version}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/*.so.*
%{_libdir}/goffice/
%{_datadir}/goffice/
%{_datadir}/pixmaps/goffice/

%files devel
%{_includedir}/libgoffice-0.8/
%{_libdir}/pkgconfig/libgoffice-0.8.pc
%{_libdir}/*.so
%{_datadir}/gtk-doc/html/goffice-0.8/


%changelog
* Thu Dec 02 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.8.12-1
- Updated to 0.8.12

* Sat Oct 02 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.8.11-1
- Updated to 0.8.11

* Mon Sep 06 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.8.10-1
- Updated to 0.8.10

* Tue Aug 17 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.8.9-1
- Updated to 0.8.9

* Sun Jul 31 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.8.8-1
- Updated to 0.8.8

* Sun Jul 25 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.8.7-1
- Updated to 0.8.7

* Sat Apr 10 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.8.1-1
- Updated to 0.8.1

* Mon Feb 22 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> 0.8.0-1
- New upstream

* Wed Dec 31 2009 Huzaifa Sidhpurwala <huzaifas@redhat.com> 0.7.17-1
- New upstream version

* Tue Dec 01 2009 Huzaifa Sidhpurwala <huzaifas@redhat.com> 0.7.16-2
- New build
- Version bump

* Wed Oct 21 2009 Robert Scheck <robert@fedoraproject.org> - 0.6.6-4
- Applied 3 patches from the 0.6 branch (#503068, #505001)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 31 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.6.6-1
- Updated to 0.6.6

* Mon Jan 12 2009 Caolán McNamara <caolanm@redhat.com> - 0.6.5-2
- rebuild to get provides pkgconfig(libgoffice-0.4) >= 0:0.4.0

* Sun Sep  7 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.6.5-1
- Updated to 0.6.5
- Development docs are now in goffice-0.6

* Wed Aug 27 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.6.4-1
- Updated to 0.6.4
- BuildRequires: pcre-devel only on Fedora < 9

* Sat Mar  8 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.6.2-1
- New upstream version 0.6.2

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.6.1-2
- Autorebuild for GCC 4.3

* Fri Jan 25 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.6.1-1
- Jump to upstream version 0.6.1 for new gnumeric
- Notice ABI and API changes!

* Fri Aug  3 2007 Bill Nottingham <notting@redhat.com>
- tweak license tag

* Thu Mar  1 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.2-1
- New upstream release 0.2.2
- Fix rpath usage on x86_64

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.1-2
- FE6 Rebuild

* Tue May  2 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.1-1
- new upstream version: 0.2.1

* Tue Mar 21 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.0-2
- rebuild for new libgsf

* Thu Feb 16 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.0-1
- New upstream version
- Remove .la files from plugin dirs
- Add BuildRequires: intltool gettext

* Mon Feb 13 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1.2-4
- Bump release and rebuild for new gcc4.1 and glibc.
- add %%{?dist} for consistency with my other packages

* Thu Dec  8 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1.2-3
-Switch to core version of libgsf now Core has 1.13 instead of using special
 Extras libgsf113 version.

* Mon Nov 28 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1.2-2
-Make Source0 a full URL
-Better URL tag
-Fix not owning /usr/lib(64)/goffice and /usr/share/goffice

* Fri Nov 25 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1.2-1
-change name to goffice as that is the upstream tarbal name.
-bump to 0.1.2 this is the minimal version supported by gnumeric-1.6
-use extras libgsf113 package since core libgsf is to old
-use locale macros
-don't ship .la files
-remove some redundant (already included in other) (Build)Requires

* Sat Nov 05 2005 Michael Wise <micwise at gmail.com> - 0.0.4-1
- Initial spec file

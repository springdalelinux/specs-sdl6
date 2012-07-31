Name:		ots
Summary:	A text summarizer
Version:	0.5.0
Release:	3%{?dist}

License:	GPLv2+
URL:		http://libots.sourceforge.net/
Group:		System Environment/Libraries

Source0:	http://prdownloads.sourceforge.net/libots/ots-%{version}.tar.gz

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	glib2-devel >= 2.0
BuildRequires:	libxml2-devel >= 2.4.23
BuildRequires:	popt-devel >= 1.5
BuildRequires:	libtool

Requires:	%{name}-libs = %{version}-%{release}

%description
The open text summarizer is an open source tool for summarizing texts.
The program reads a text and decides which sentences are important and
which are not.

 
%package	devel
Summary: 	Libraries and include files for developing with libots
Group: 		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires: 	glib2-devel >= 2.0
Requires:	libxml2-devel >= 2.4.23
Requires:	popt-devel >= 1.5
Requires:	pkgconfig

%description	devel
This package provides the necessary development libraries and include
files to allow you to develop with libots.


%package	libs
Summary:	Shared libraries for %{name}
Group:		Development/Libraries

%description	libs
The %{name}-libs package contains shared libraries used by %{name}.


%prep
%setup -q 


%build
%configure --with-html-dir=%{_datadir}/gtk-doc/html/ots
# XXX: Disgusting kludge to fix upstream's broken package.
touch ./gtk-doc.make
%{__make} LIBTOOL=%{_bindir}/libtool


%install
rm -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}


%clean
rm -rf %{buildroot}


%post	libs -p /sbin/ldconfig


%postun	libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_bindir}/ots

%files	libs
%defattr(-,root,root,-)
%doc COPYING
%exclude %{_libdir}/*.a
%exclude %{_libdir}/*.la
%{_libdir}/libots-1.so.*
%{_datadir}/ots/

%files	devel
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libots-1.so
%{_includedir}/libots-1/
%{_libdir}/pkgconfig/libots-1.pc


%changelog
* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 08 2008 Peter Gordon <peter@thecodergeek.com> - 0.5.0-1
- Update to new upstream release (0.5.0).
- Drop GCC4 patch (fixed upstream):
  - 0.4.2-gcc4.patch

* Mon Apr 23 2007 Peter Gordon <peter@thecodergeek.com> - 0.4.2-11
- Remove static libraries (%%_libdir/*.a).
- Fix %%defattr lines in the %%files listings.
- Lots of formatting/aesthetic fixes.
- Remove pkgconfig from build-time dependencies (required by glib2-devel and
  libxml2-devel).
- Add LDFLAGS to fix shared library linking: libots-1.so.0 needs to link to
  glib2 and libxml2 libraries to fix unresolved symbol errors. (Resolves bug
  #237501; thanks to Matthias Clasen for the report).
- Split off libs subpackage to avoid potential multilib conflicts.    

* Mon Aug 27 2006 Michael J. Knox <michael[AT]knox.net.nz> - 0.4.2-10
- Rebuild for FC6

* Sun May 21 2006 Michael J. Knox <michael[AT]knox.net.nz> - 0.4.2-9
- rebuild and spec tidy

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 0.4.2-7
- rebuild on all arches

* Wed Mar 16 2005 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.4.2-5
- Reenable man page.
- Disable rebuilding documentation via configure switch instead of an automake
  requiring patch.
- Remove the API documentation for now as it is just a placeholder.

* Wed Mar  2 2005 Caolan McNamara <caolanm@redhat.com> - 0.4.2-4
- rebuild with gcc4
- small lvalue assign patch

* Wed Feb 09 2005 Caolan McNamara <caolanm@redhat.com> - 0.4.2-3
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 19 2004 Jeremy Katz <katzj@redhat.com> - 0.4.2-1
- 0.4.2

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Nov 28 2003 Jeremy Katz <katzj@redhat.com> 
- add some buildrequires (#111158)

* Mon Sep 15 2003 Jeremy Katz <katzj@redhat.com> 0.4.1-1
- 0.4.1

* Mon Aug  4 2003 Jeremy Katz <katzj@redhat.com> 0.4.0-1
- 0.4.0

* Tue Jul 22 2003 Jeremy Katz <katzj@redhat.com> 0.3.0-1
- update to 0.3.0

* Sat Jul 12 2003 Jeremy Katz <katzj@redhat.com> 0.2.0-2
- forcibly disable gtk-doc (openjade is busted on s390)

* Mon Jul  7 2003 Jeremy Katz <katzj@redhat.com> 0.2.0-1
- update to 0.2.0
- ldconfig in %%post/%%postun
- libtoolize
- clean up spec file a little, build gtk-doc
- fix libtool versioning 

* Thu Jun 05 2003 Rui Miguel Silva Seabra <rms@1407.org>
- fix spec
- disable gtk-doc (it's not building in RH 9,
  maybe it's broken for some reason)

* Fri May 02 2003 Rui Miguel Silva Seabra <rms@1407.org>
- define a longer description from the README file
- explicitly set file permissions

* Wed Apr 30 2003 Dom Lachowicz <cinamod@hotmail.com>
- created this thing

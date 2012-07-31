%define with_ssl   1
%define gnutls_ver 1.4.0

Name:           loudmouth
Version:        1.4.3
Release:        6%{?dist}
Summary:        XMPP/Jabber C programming library

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.loudmouth-project.org/
Source0:        http://ftp.imendio.com/pub/imendio/%{name}/src/%{name}-%{version}.tar.bz2
Patch0:		%{name}-1.4.3-certs_location.patch
Patch1:		%{name}-1.4.3-async_assertion.patch
Patch2:		%{name}-1.4.3-fix-sasl-md5-digest-uri.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  glib2-devel >= 2.4.0
BuildRequires:	check-devel
BuildRequires:	libidn-devel
BuildRequires:	libasyncns-devel
%if %{with_ssl}
BuildRequires:	gnutls-devel >= %{gnutls_ver}
%endif


%description
Loudmouth is a lightweight and easy-to-use C library for programming
with the XMPP/Jabber protocol. It's designed to be easy to get started
with and yet extensible to let you do anything the XMPP protocol allows.


%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel
Requires:	libidn-devel
Requires:	pkgconfig
%if %{with_ssl}
Requires:	gnutls-devel >= %{gnutls_ver}
%endif


%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1 -b .certs
%patch1 -p1 -b .async
%patch2 -p1 -b .uri


%build
%configure --enable-static=no	\
	   --with-asyncns=yes	\
%if %{with_ssl}
	   --with-ssl=gnutls
%else
	   --with-ssl=no
%endif

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Copy the files from the tarball to avoid the IDs generated by gtk-doc being
# different on different builds
mkdir -p $RPM_BUILD_ROOT%{_datadir}/gtk-doc/html/%{name}/
cp -a docs/reference/html/* $RPM_BUILD_ROOT%{_datadir}/gtk-doc/html/%{name}/


%check
make check


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc ChangeLog NEWS README COPYING
%{_libdir}/libloudmouth*.so.*


%files devel
%defattr(-,root,root,-)
%{_libdir}/libloudmouth*.so
%{_libdir}/pkgconfig/%{name}-1.0.pc
%{_includedir}/%{name}-1.0
%{_datadir}/gtk-doc/html/%{name}


%changelog
* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 12 2009 Brian Pepple <bpepple@fedoraproject.org> - 1.4.3-5
- Add patch to fix digest uri bug. (#503901)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Nov 28 2008 Brian Pepple <bpepple@fedoraproject.org> - 1.4.3-3
- Add patch to search correct location for ssl certs. (#473458)
- Add patch to fix async assertion. (#473436)

* Sat Nov 22 2008 Brian Pepple <bpepple@fedoraproject.org> - 1.4.3-2
- Simplify sumary & description.

* Sun Nov  9 2008 Brian Pepple <bpepple@fedoraproject.org> - 1.4.3-1
- Update to 1.4.3.

* Thu Aug 28 2008 Brian Pepple <bpepple@fedoraproject.org> - 1.4.2-1
- Update to 1.4.2.
- Enable libasyncns support.

* Sat Aug  2 2008 Brian Pepple <bpepple@fedoraproject.org> - 1.4.1-1
- Update to 1.4.1.

* Wed Jun 25 2008 Tomas Mraz <tmraz@redhat.com> - 1.4.0-2
- rebuild with new gnutls

* Tue Jun 10 2008 Brian Pepple <bpepple@fedoraproject.org> - 1.4.0-1
- Update to 1.4.0.

* Wed Apr  2 2008 Brian Pepple <bpepple@fedoraproject.org> - 1.3.4-1
- Update to 1.3.4.
- Run check test.
- Bump min version needed for gnutls-devel.
- Drop stream-error.patch. Fixed upstream.
- Drop eai-nodata.patch. Fixed upstream.
- Drop connect-fail-sync.patch. Fixed upstream.
- Drop connect-fail-async patch. Fixed upstream.
- Update URL & Source URL.
- Don't generate the gtk-doc docs, and use the ones in the tarball
  to avoid having different files in different builds, fixes
  multilib problems (#342551)

* Thu Feb 21 2008 Owen Taylor <otaylor@redhat.com> - 1.3.3-4
- Fix build with recent GNU libc

* Thu Feb  7 2008 Owen Taylor <otaylor@redhat.com> - 1.3.3-3
- Add patches fixing reentrancy problems on connection failure

* Wed Jan 30 2008 Owen Taylor <otaylor@redhat.com> - 1.3.3-2
- Add back stream-error patch, it wasn't fixed in the 1.3 branch

* Fri Jan 18 2008 Brian Pepple <bpepple@fedoraproject.org> - 1.3.3-1
- Update to 1.3.3.
- Drop reconnect-failure patch.
- Drop gnutls compression patch. fixed upstream.

* Thu Nov 15 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.3-6
- Ugh.  Let's acutally use a valid e-mail addy.

* Thu Nov 15 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.3-5
- Add patch to use gnutls compression.

* Mon Nov 12 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.3-4
- Add reconnect-failure patch. Thanks to Robert McQueen.

* Tue Aug 21 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.3-3
- Rebuild.

* Sun Aug  5 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.3-2
- Update license tag.

* Sun Jun 10 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3.
- Drop stream-error patch. fixed upstream.

* Wed May 16 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.2-3
- Add patch to fix stream error.

* Tue May 15 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.2-2
- Drop BR on libtasn1-devel.

* Mon May 14 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.2-1
- Update to 1.2.2.

* Sat Feb 24 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.1-2
- Fix typo.

* Sat Feb 24 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1.

* Tue Feb 20 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.0-3
- Add necessary requires to devel package. D'Oh!

* Tue Feb 20 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.0-2
- Add BR on libidn-devel.
- Specify which ssl implementation to use.

* Mon Feb  5 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0.
- Drop mono config option since it's been dropped from the tarball.

* Mon Sep 11 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.0.5-2
- Change source to .gz.

* Mon Sep 11 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5.

* Tue Aug 29 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.0.4-3
- Rebuild for FC6.
- Simplify devel description.

* Thu Jun 29 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.0.4-2
- Update to 1.0.4.
- Add devel requires on pkgconfig.
- Drop reentrancy patch, fixed upstream.

* Thu Jun 15 2006 Jeremy Katz <katzj@redhat.com> - 1.0.3-5
- rebuild for new gnutls

* Fri May 26 2006 Brian Pepple <bdpepple@ameritech.net> - 1.0.3-4
- Add patch to fix some reentrancy crashes.  (Thanks, Havoc)

* Wed Apr  5 2006 Brian Pepple <bdpepple@ameritech.net> - 1.0.3-3
- Update to 1.0.3.
- Add BR for gnutls-devel to devel package.
- Disable static libs.
- Add BR for check-devel.

* Thu Feb 16 2006 Brian Pepple <bdpepple@ameritech.net> - 1.0.1-6
- Remove unnecessary BR (libgcrypt-devel).

* Mon Feb 13 2006 Brian Pepple <bdpepple@ameritech.net> - 1.0.1-5
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Dec 26 2005 Brian Pepple <bdpepple@ameritech.net> - 1.0.1-4
- Rebuild.

* Wed Aug 31 2005 Brian Pepple <bdpepple@ameritech.net> - 1.0.1-3
- Update to 1.0.1.

* Sun Aug 14 2005 Brian Pepple <bdpepple@ameritech.net> - 1.0-2
- Update to 1.0.

* Mon Aug  8 2005 Brian Pepple <bdpepple@ameritech.net> - 0.90-5
- Rebuild due to new gnutls.

* Sat Jul 30 2005 Brian Pepple <bdpepple@ameritech.net> - 0.90-4
- Fix description.

* Fri May 13 2005 Brian Pepple <bdpepple@ameritech.net> - 0.90-2
- Add dist tag.

* Fri May 13 2005 Brian Pepple <bdpepple@ameritech.net> - 0.90-1
- Update to 0.9.

* Thu May  5 2005 Brian Pepple <bdpepple@ameritech.net> - 0.17.2-3
- Adde glib2-devel requires.

* Thu May  5 2005 Brian Pepple <bdpepple@ameritech.net> - 0.17.2-2
- added %%{_includedir}.
- Add libgcrypt-devel BR.

* Sun May  1 2005 Brian Pepple <bdpepple@ameritech.net> - 0.17.2-1
- Initial Fedora build.


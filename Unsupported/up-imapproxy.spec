Name:           up-imapproxy
Summary:        University of Pittsburgh IMAP Proxy
Version:        1.2.8
Release:        0.svn20110801.1%{?dist}
License:        GPLv2+
Group:          System Environment/Daemons
URL:            http://www.imapproxy.org
Source0:        http://www.imapproxy.org/downloads/squirrelmail-20110801_0201-SVN.imap_proxy.tar.bz2
Source1:        imapproxy.init
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  openssl-devel tcp_wrappers ncurses-devel tcp_wrappers-devel 
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service

%description
imapproxy was written to compensate for webmail clients that are
unable to maintain persistent connections to an IMAP server. Most
webmail clients need to log in to an IMAP server for nearly every
single transaction. This behaviour can cause tragic performance
problems on the IMAP server. imapproxy tries to deal with this problem
by leaving server connections open for a short time after a webmail
client logs out. When the webmail client connects again, imapproxy
will determine if there's a cached connection available and reuse it
if possible.

%prep
%setup -q -n squirrelmail.imap_proxy

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
# The install-* Makefile targets don't support DESTDIR syntax, so work around.
install -D -m 0644 -p scripts/imapproxy.conf \
    $RPM_BUILD_ROOT%{_sysconfdir}/imapproxy.conf
install -D -m 0755 -p %{SOURCE1} \
    $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/imapproxy
install -d -m 0755 $RPM_BUILD_ROOT%{_sbindir}
install -m 0755 bin/* $RPM_BUILD_ROOT%{_sbindir}
install -d -m 0755 $RPM_BUILD_ROOT%{_localstatedir}/run
touch $RPM_BUILD_ROOT%{_localstatedir}/run/pimpstats

# Fix doc permissions
chmod 644 README* COPYING copyright ChangeLog

# Fix debuginfo package file permission
chmod 644 include/imapproxy.h src/main.c

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ $1 == 1 ] ; then
    /sbin/chkconfig --add imapproxy &> /dev/null || :
fi

%preun
if [ $1 == 0 ] ; then
    /sbin/service imapproxy stop &> /dev/null || :
    /sbin/chkconfig --del imapproxy || :
fi

%postun
/sbin/service imapproxy condrestart &> /dev/null || :

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog README README.ssl
%doc copyright
%config(noreplace) %{_sysconfdir}/imapproxy.conf
%ghost %{_localstatedir}/run/pimpstats
%{_sysconfdir}/rc.d/init.d/*
%{_sbindir}/*

%changelog
* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Rakesh Pandit <rakesh@fedoraproject.org> 1.2.7-1
- Updated to 1.2.7

* Fri Dec 04 2009 Rakesh Pandit <rakesh@fedoraproject.org> 1.2.7-0.7.rc3
- Updated to 1.2.7-0.7.rc3

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.2.7-0.6.rc1
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-0.5.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-0.4.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 04 2009 Rakesh Pandit <rakesh@fedoraproject.org> 1.2.7-0.3.rc1
- Patched buggy init script (David Rees, Bug 477096)

* Sun Jan 18 2009 Tomas Mraz <tmraz@redhat.com> 1.2.7-0.2.rc1
- rebuild with new openssl

* Thu Oct 23 2008 Rakesh Pandit <rakesh@fedoraproject.org> 1.2.7-0.1.rc1
- fixed version and release fields (acc. to guidelines)

* Thu Oct 23 2008 Rakesh Pandit <rakesh@fedoraproject.org> 1.2.7.rc1-1
- updated to 1.2.7.rc1 - security updates, buffer overflow etc.

* Thu Aug 28 2008 Rakesh Pandit <rakesh@fedoraproject.org> 1.2.6-2
- fixed initscript to follow guidelines

* Thu Aug 28 2008 Rakesh Pandit <rakesh@fedoraproect.org> 1.2.6-1
- Update to 1.2.6
- Remove old patches (already upstream), Remove README.known_issues
- Tidy init script (Tim Jackson)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.4-9
- Autorebuild for GCC 4.3

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.2.4-8
 - Rebuild for deps

* Thu Sep 14 2006 Jeff Carlson <jeff@ultimateevil.org> - 1.2.4-7
- Force rebuild for FC-6.

* Thu Apr 27 2006 Jeff Carlson <jeff@ultimateevil.org> - 1.2.4-6
- Patch to fix changes in OpenSSL.
- Thanks to Paul W. Frields for providing the patch.

* Mon Dec 26 2005 Jeff Carlson <jeff@ultimateevil.org> - 1.2.4-5
- Rebuild against new OpenSSL in devel (fc5 only).

* Tue Oct 11 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.2.4-4
- Fix for CAN-2005-2661 (#170220, from Debian).

* Fri Sep  9 2005 Jeff Carlson <jeff@ultimateevil.org> - 1.2.4-3
- Same as -2.

* Fri Sep  9 2005 Jeff Carlson <jeff@ultimateevil.org> - 1.2.4-2
- No-op release bump to get a new buildsys tag.

* Fri Sep  9 2005 Jeff Carlson <jeff@ultimateevil.org> - 1.2.4-1
- Bump to current upstream release.
- Upstream includes a new doc (copyright), included.

* Fri Sep  9 2005 Jeff Carlson <jeff@ultimateevil.org> - 1.2.3-6
- Another change to the init script.

* Sat Sep  3 2005 Jeff Carlson <jeff@ultimateevil.org> - 1.2.3-5
- Preserve certain timestamps.

* Thu Sep  1 2005 Jeff Carlson <jeff@ultimateevil.org> - 1.2.3-4
- Fix rpmlint complaints.
- Paul also provided a replacement init script.
- Fixed some redundant BuildReqs.
- Tuned Requires, install, and files.
- Many thanks to Paul Howarth.

* Wed Aug 31 2005 Jeff Carlson <jeff@ultimateevil.org> - 1.2.3-3
- Added BuildRequires.

* Fri Aug 12 2005 Jeff Carlson <jeff@ultimateevil.org> - 1.2.3-2
- Multiple fixups recommended by spot.

* Mon Jul 18 2005 Jeff Carlson <jeff@ultimateevil.org> - 1.2.3-1
- Initial build.

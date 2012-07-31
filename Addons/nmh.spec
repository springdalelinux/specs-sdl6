Name:           nmh
Version:        1.3
Release:        3%{?dist}
Summary:        A capable mail handling system with a command line interface.

Group:          Applications/Internet
License:        BSD
URL:            http://savannah.nongnu.org/projects/nmh
Source0:        nmh-1.3.tar.gz
Patch0:         nmh-1.1-inc_install.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  ncurses-devel
BuildRequires:  db4-devel
BuildRequires:  /usr/sbin/sendmail
BuildRequires:  /bin/vi

%description
Nmh is an email system based on the MH email system and is intended to
be a (mostly) compatible drop-in replacement for MH.  Nmh isn't a
single comprehensive program.  Instead, it consists of a number of
fairly simple single-purpose programs for sending, receiving, saving,
retrieving and otherwise manipulating email messages.  You can freely
intersperse nmh commands with other shell commands or write custom
scripts which utilize nmh commands.  If you want to use nmh as a true
email user agent, you'll want to also install exmh to provide a user
interface for it--nmh only has a command line interface.

%prep
%setup -q -n nmh-1.3
%patch0 -p0

%build
CFLAGS="$RPM_OPT_FLAGS -fno-builtin-strcasecmp"
%configure \
            --sysconfdir=%{_sysconfdir}/nmh \
            --libdir=%{_libexecdir}/nmh \
            --with-locking=fcntl \
            --enable-pop
make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

chmod g-s $RPM_BUILD_ROOT/%{_bindir}/inc


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/*
%dir %{_sysconfdir}/nmh
%config(noreplace) %{_sysconfdir}/nmh/*
%dir %{_libexecdir}/nmh
%{_libexecdir}/nmh/*
%{_mandir}/man[851]/*
%doc docs/COMPLETION-* docs/DIFFERENCES docs/FAQ docs/MAIL.FILTERING VERSION
%doc docs/TODO docs/README* COPYRIGHT

%changelog
* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jun 19 2008 Josh Bressers <bressers@redhat.com> 0:1.3-1
- Update nmh to 1.3

* Wed Apr 30 2008 Josh Bressers <bressers@redhat.com> 0:1.3-RC1.1
- Update nmh to 1.3-RC1

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2-20070116cvs.4
- Autorebuild for GCC 4.3

* Tue Aug 21 2007 Josh Bressers <bressers@redhat.com> 0:1.2_20070115cvs.4
- Fix inc when the -silent flag is used

* Sun Feb 04 2007 Josh Bressers <bressers@redhat.com> 0:1.2_20070115cvs.3
- Use double quotes not single quotes for CFLAGS

* Sun Feb 04 2007 Josh Bressers <bressers@redhat.com> 0:1.2_20070115cvs.2
- Use $RPM_OPT_FLAGS when building the source bz#227243

* Mon Jan 15 2007 Josh Bressers <bressers@redhat.com> 0:1.2_CVS_20070115
- Update to nmh 1.2 post CVS (thanks to Horst H. von Brand for assistance
  in this task)

* Wed Jan 10 2007 Josh Bressers <bressers@redhat.com> 0:1.1-20
- Replace the libtermcap-devel buildrequires with ncurses-devel

* Mon Sep 11 2006 Josh Bressers <bressers@redhat.com> 0:1.1-19.fc6
- Use %dist tag
- Place helper programs in /usr/libexec
- Rebuild for FC6

* Sun Feb 19 2006 Josh Bressers <bressers@redhat.com> 0:1.1-18.fc5
- Fix a broken spec file.

* Sun Feb 19 2006 Josh Bressers <bressers@redhat.com> 0:1.1-17.fc5
- Stop trying to install inc sgid.

* Mon Feb 13 2006 Josh Bressers <bressers@redhat.com> 0:1.1-16.fc5
- Rebuild for Fedora Extras 5.

* Fri Dec 16 2005 Josh Bressers <bressers@redhat.com> 0:1.1-15.fc5
- Add the -fno-builtin-strcasecmp cflag.

* Tue Dec 13 2005 Josh Bressers <bressers@redhat.com> 0:1.1-14.fc5
- Add a patch to prevent multiple calls to context_read from squashing
  settings.

* Mon Dec 12 2005 Josh Bressers <bressers@redhat.com> 0:1.1-13.fc5
- Add a patch to allow repl to properly annotate messages.

* Mon Dec 05 2005 Josh Bressers <bressers@redhat.com> 0:1.1-12.fc5
- Add a buildrequires on /bin/vi
- Modify the sendmail buildrequires to use /usr/sbin/sendmail

* Thu Nov 10 2005 Josh Bressers <bressers@redhat.com> 0:1.1-11.fc5
- Add a sendmail buildrequires to make spost work properly

* Thu Nov 03 2005 Josh Bressers <bressers@redhat.com> 0:1.1-10.fc5
- Prevent mhshow from trying to close a file stream twice

* Thu Aug 25 2005 Josh Bressers <bressers@redhat.com> 0:1.1-9.fc5
- Fix the specfile to honor the $RPM_OPT_FLAGS

* Tue May 10 2005 Josh Bressers <bressers@redhat.com> 0:1.1-8.fc4
- Use fcntl for filelocking instead of the default dotlocks.

* Sun Apr 24 2005 Josh Bressers <bressers@redhat.com> 0:1.1-7.fc4
- Add patch from Jason Venner to avoid trying to lock files in /dev

* Sun Apr 17 2005 Josh Bressers <bressers@redhat.com> 0:1.1-6.fc4
- Remove what should have been commented out redinitions of the _sysconfdir
  and _libdir macros.

* Thu Apr 14 2005 Josh Bressers <bressers@redhat.com> 0:1.1-5
- Make the spec file much more sane.

* Wed Apr 13 2005 Josh Bressers <bressers@redhat.com> 0:1.1-3
- Initial build

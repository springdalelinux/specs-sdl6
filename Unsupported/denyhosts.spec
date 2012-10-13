Name:       denyhosts
Version:    2.6
Release:    19%{?dist}
Summary:    A script to help thwart ssh server attacks

Group:      Applications/System
License:    GPLv2
URL:        http://denyhosts.sourceforge.net/
Source0:    http://dl.sourceforge.net/denyhosts/DenyHosts-%{version}.tar.gz
Source1:    denyhosts.cron
Source2:    denyhosts.init
Source3:    denyhosts-allowed-hosts
Source4:    denyhosts.sysconfig
Source5:    denyhosts.logrotate
Source6:    README.fedora
Source10:   denyhosts-restorecon.plugin
Patch0:     denyhosts-2.6-config.patch
Patch1:     denyhosts-2.4-setup.patch
Patch2:     denyhosts-2.6-daemon-control.patch
Patch3:     denyhosts-2.6-defconffile.patch
Patch4:     denyhosts-2.6-commandlinesync.patch
Patch5:     denyhosts-2.6-selinux.patch
# Patch10 is a security fix
Patch10:    denyhosts-2.6-regex.patch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  python-devel
# libselinux-python is necessary due to Patch5.
Requires:       openssh-server libselinux-python

%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}


%description
DenyHosts is a Python script that analyzes the sshd server log
messages to determine which hosts are attempting to hack into your
system. It also determines what user accounts are being targeted. It
keeps track of the frequency of attempts from each host and, upon
discovering a repeated attack host, updates the /etc/hosts.deny file
to prevent future break-in attempts from that host.  Email reports can
be sent to a system admin.


%prep
%setup -q -n DenyHosts-%{version}
%patch0 -p0 -b .config
%patch1 -p0 -b .setup
%patch2 -p0 -b .daemon-control
%patch3 -p0 -b .defconffile
%patch4 -p1 -b .commandlinesync
%patch10 -p1 -b .regex

cp %{SOURCE6} .

# Fix up non-utf8-ness
for i in CHANGELOG.txt; do
  iconv -f iso-8859-1 -t utf-8 < $i > $i. && touch -r $i $i. && mv -f $i. $i
done

# This must be moved before the Python build process runs so that we
# can include it as documentation.
mv plugins/README.contrib .

# And the permissions are off as well
chmod +x plugins/*


%build
%{__python} setup.py build


%install
rm -rf %{buildroot}

%{__python} setup.py install -O1 --skip-build --root=%{buildroot}

install -d %{buildroot}/%{_bindir}
install -d %{buildroot}/%{_initrddir}
install -d %{buildroot}/%{_sysconfdir}/cron.d
install -d %{buildroot}/%{_sysconfdir}/logrotate.d
install -d %{buildroot}/%{_sysconfdir}/sysconfig

install -d -m 700 %{buildroot}/%{_localstatedir}/lib/denyhosts
install -d %{buildroot}/%{_localstatedir}/log

install -p -m 600 denyhosts.cfg-dist %{buildroot}/%{_sysconfdir}/denyhosts.conf
install -p -m 755 daemon-control-dist %{buildroot}/%{_bindir}/denyhosts-control
install -p -m 644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/cron.d/denyhosts
install -p -m 755 %{SOURCE2} %{buildroot}/%{_initrddir}/denyhosts
install -p -m 644 %{SOURCE3} %{buildroot}/%{_localstatedir}/lib/denyhosts/allowed-hosts
install -p -m 644 %{SOURCE4} %{buildroot}/%{_sysconfdir}/sysconfig/denyhosts
install -p -m 644 %{SOURCE5} %{buildroot}/%{_sysconfdir}/logrotate.d/denyhosts

install -p -m 755 %{SOURCE10} %{buildroot}/%{_datadir}/denyhosts/plugins/restorecon.sh

touch %{buildroot}/%{_localstatedir}/log/denyhosts

for i in allowed-warned-hosts hosts hosts-restricted hosts-root \
         hosts-valid offset suspicious-logins sync-hosts \
         users-hosts users-invalid users-valid; do
  touch %{buildroot}/%{_localstatedir}/lib/denyhosts/$i
done

# FC-4 and earlier won't create these automatically; create them here
# so that the %exclude below doesn't fail
touch %{buildroot}/%{_bindir}/denyhosts.pyc
touch %{buildroot}/%{_bindir}/denyhosts.pyo


%clean
rm -rf %{buildroot}


# Note that we do not automaticaly run --migrate, because we can't be
# sure that all of the hosts.deny entries were created by denyhosts
%post
/sbin/chkconfig --add denyhosts
/sbin/service denyhosts condrestart
exit 0


%preun
if [ $1 = 0 ]; then
  /sbin/service denyhosts stop > /dev/null 2>&1
  /sbin/chkconfig --del denyhosts
fi
exit 0


%files
%defattr(-,root,root,-)
%doc CHANGELOG.txt denyhosts.cfg-dist LICENSE.txt
%doc README.fedora README.txt setup.py README.contrib

%{_bindir}/denyhosts.py
%exclude %{_bindir}/denyhosts.py[co]

%{_bindir}/denyhosts-control
%{_datadir}/denyhosts
%{python_sitelib}/*

%config(noreplace) %{_sysconfdir}/denyhosts.conf
%config(noreplace) %{_sysconfdir}/cron.d/denyhosts
%config(noreplace) %{_sysconfdir}/logrotate.d/denyhosts
%config(noreplace) %{_sysconfdir}/sysconfig/denyhosts
%config(noreplace) %{_localstatedir}/lib/denyhosts/allowed-hosts

%ghost %{_localstatedir}/log/denyhosts
%ghost %{_localstatedir}/lib/denyhosts/allowed-warned-hosts
%ghost %{_localstatedir}/lib/denyhosts/hosts
%ghost %{_localstatedir}/lib/denyhosts/hosts-restricted
%ghost %{_localstatedir}/lib/denyhosts/hosts-root
%ghost %{_localstatedir}/lib/denyhosts/hosts-valid
%ghost %{_localstatedir}/lib/denyhosts/offset
%ghost %{_localstatedir}/lib/denyhosts/suspicious-logins
%ghost %{_localstatedir}/lib/denyhosts/sync-hosts
%ghost %{_localstatedir}/lib/denyhosts/users-hosts
%ghost %{_localstatedir}/lib/denyhosts/users-invalid
%ghost %{_localstatedir}/lib/denyhosts/users-valid

%dir %{_localstatedir}/lib/denyhosts

%{_initrddir}/denyhosts


%changelog
* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar 04 2009 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.6-18
- Add patch to keep proper file context on the hosts.deny file.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.6-16
- Rebuild for Python 2.6

* Thu Nov 13 2008 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.6-15
- Tweak default config file and add info to README.Fedora asking folks not to
  use sync and to report bugs upstream if they do.

* Fri Nov 07 2008 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.6-14
- Add patch from upstream to fix command line --sync.

* Mon Sep 22 2008 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.6-13
- Add plugin to restore file contexts after purging.

* Thu Aug 28 2008 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.6-12
- Fix up patches to apply with --fuzz=0.

* Fri Jul 11 2008 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.6-11
- Tweak initscript priorities to ensure that the MTA is started first.

* Tue Jul 01 2008 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.6-10
- Fix initscript lockfile handling:
   Stop creating the lockfile in the initscript.
   Clean up stray lockfiles automatically.
   Don't attempt to start the daemon if its already running.
- Various initscript cleanups.
- Set default configuration file location to match what we use.
- Make it easier to add extra options like --debug from the sysconfig file.

* Fri Jan 04 2008 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.6-9
- Properly escape percent symbols in the changelog entries.

* Thu Jan 03 2008 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.6-8
- Include everything under %%python_sitelib to pick up any egg-info files that
  might be generated.
- Silence file-not-utf8 rpmlint complaint.
- Silence missing-mandatory-lsb-keyword rpmlint complaint.

* Thu Aug 23 2007 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.6-7
- Init file tweaks including patch from Jonathan Underwood
  (bug 188536).
- Attempt to add LSB-compliant comment block.

* Mon Aug 20 2007 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.6-6
- Update license tag.

* Tue Jun 19 2007 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.6-5
- Apply yet another regex.py fix from Jonathan Underwood to fix bug 244943.

* Mon Apr 23 2007 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.6-4
- Apply fix to regex.py from Jonathan Underwood to fix bug 237449.

* Fri Dec 08 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.6-3
- Rebuild for new python.

* Thu Dec 07 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.6-2
- Update config patch.

* Thu Dec 07 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.6-1
- Update to 2.6; fixes bug 218824, CVE-2006-6301.

* Tue Aug 29 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.5-2
- No need to ghost .pyo files.
- Fix %%{python_sitelib}/Denyhosts ownership.

* Thu Jun 22 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.5-1
- Update to 2.5.

* Mon Apr 10 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.4b-1
- Update to 2.4b.

* Thu Apr  6 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.3-2
- Fix uncommented MacOS X SECURE_LOG config setting.

* Tue Apr  4 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.3-1
- Update to version 2.3.

* Fri Mar 31 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.2-6
- More reversion of the name change.

* Fri Mar 31 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.2-5
- Revert renaming of the denyhosts.py script

* Fri Mar 31 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.2-4
- Fix permissions on plugins.

* Thu Mar 30 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.2-3
- Switch from $RPM_BUILD_ROOT to %%{buildroot} (looks cleaner).
- Rename the main executable from denyhosts.py to denyhosts.

* Wed Mar 29 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.2-2
- Specfile cleanups.
- Add hostname to default report subject.

* Tue Mar 14 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.2-1
- Update to 2.2.

* Tue Feb 28 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.1-2
- Add some additional ghosted files.

* Fri Feb 10 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.1-1
- Update to 2.1
- Package plugins and scripts.

* Sat Feb  4 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.0-1
- Update to 2.0.

* Mon Jan 30 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.1.4-5
- Redo installation to match current Python packaging guidelines.

* Mon Jan 30 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.1.4-4
- Simplify "[ -f ... ] && rm" to "rm -f".

* Mon Jan 30 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.1.4-3
- Delete stray .pyo and .pyc files that appear for no reason.

* Fri Jan 13 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.1.4-2
- Clean up %%post script; just call condrestart and don't bother with
  the call to --upgrade099.

* Fri Jan 13 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.1.4-1
- Update to 1.1.4.

* Fri Nov 18 2005 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.1.3-1
- Update to 1.1.3
- Update README.fedora to document what the package currently does.
- Drop default PURGE_DENY from one year to four weeks.

* Tue Oct 11 2005 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.1.2-1
- Update to 1.1.2

* Mon Oct  3 2005 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.1.1-2
- Bump version to fix build.

* Mon Oct  3 2005 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.1.1-1
- Update to 1.1.1

* Mon Sep 19 2005 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.0.3-1
- Update to 1.0.3

* Tue Aug 23 2005 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.0.2-1
- Update to 1.0.2

* Thu Aug 18 2005 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.0.1-2
- Bump release for build

* Thu Aug 18 2005 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.0.1-1
- Update to 1.0.1

* Wed Aug 17 2005 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.0.0-2
- Restart the daemon in the logrotate script
- Stop the running daemon before calling --upgrade099

* Tue Aug 16 2005 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.0.0-1
- Fix condrestart
- Actually install logrotate entry

* Mon Aug 15 2005 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.0.0-0
- Update to 1.0.0
- Add logrotate entry
- Clean up initscript
- Add notes on upgrading.

* Mon Aug 15 2005 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.9.9-2
- Automatically upgrade the format of hosts.deny entries.

* Sun Aug 14 2005 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.9.9-1
- Framework for enabling daemon mode.

* Sat Aug 13 2005 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.9.9-0
- Update to 0.9.9

* Fri Aug  5 2005 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.9.8-1
- Update to 0.9.8

* Fri Jul 22 2005 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.8.0-3
- Rename the lockfile used by the initscript/cron setup because
  DenyHosts now has its own internal locking and they chose the exact
  same lockfile we were using.
- Turn on PURGE_DENY in the installed config file.
- Delete data_files from setup.py.
- Enable purging in denyhosts.cron.
- Add README.fedora file.

* Thu Jul 21 2005 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.8.0-2
- Package CHANGELOG.txt and denyhosts.cfg-dist as well (as
  documentation).

* Thu Jul 21 2005 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.8.0-1
- Update to 0.8.0
- Use proper Python installation mechanism.
- Drop denyhosts-0.6.0-version.patch as it's no longer necessary.

* Sat Jul  2 2005 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.6.0-1
- Update to 0.6.0
- Add fix for "from version import VERSION" issue.

* Thu May 19 2005 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.5.5-2
- Use dist tag
- Don't automatically enable at install time
- Include %%ghost'ed allowed-warned-hosts file
- Use %%ghost instead of including zero length files.
- Source is at dl.sourceforge.net

* Thu May 12 2005 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.5.5-1
- Initial build


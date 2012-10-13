# Augeas and SELinux requirements may be disabled at build time by passing
# --without augeas and/or --without selinux to rpmbuild or mock

%{!?ruby_sitelibdir: %global ruby_sitelibdir %(ruby -rrbconfig -e 'puts Config::CONFIG["sitelibdir"]')}
%global confdir conf/redhat

%global vimdir %{_datadir}/vim/vimfiles

Name:           puppet
Version:        2.7.19
Release:        9%{?dist}
Summary:        A network tool for managing many disparate systems
License:        GPLv2
URL:            http://puppetlabs.com
Source0:        http://puppetlabs.com/downloads/%{name}/%{name}-%{version}.tar.gz
Source100:	%{name}-selinux.tar.gz

Group:          System Environment/Base

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  facter >= 1.5
BuildRequires:  ruby >= 1.8.1
Requires:	augeas

# selinux
# http://fedoraproject.org/wiki/PackagingDrafts/SELinux
# http://selinuxproject.org/page/RPM
BuildRequires: selinux-policy

%if 0%{?fedora} || 0%{?rhel} >= 5
BuildArch:      noarch
Requires:       ruby(abi) = 1.8
Requires:       ruby-shadow
%endif

# Pull in ruby selinux bindings where available
%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6
%{!?_without_selinux:Requires: ruby(selinux)}
%else
%if 0%{?fedora} || 0%{?rhel} >= 5
%{!?_without_selinux:Requires: libselinux-ruby}
%endif
%endif

Requires:       facter >= 1.5
Requires:       ruby >= 1.8.1
%{!?_without_augeas:Requires: ruby-augeas}

Requires(pre):  shadow-utils
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
Requires(postun): initscripts

%description
Puppet lets you centrally manage every important aspect of your system using a
cross-platform specification language that manages all the separate elements
normally aggregated in different files, like users, cron jobs, and hosts,
along with obviously discrete elements like packages, services, and files.

%package server
Group:          System Environment/Base
Summary:        Server for the puppet system management tool
Requires:       puppet = %{version}-%{release}
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
Requires(postun): initscripts

%description server
Provides the central puppet server daemon which provides manifests to clients.
The server can also function as a certificate authority and file server.

%policy server
%module %{name}-selinux/%{name}-passenger.pp
  Name: %{name}-passenger

%package server-selinux
Group:          System Environment/Base
Summary:        selinux Modules for the puppet system management tool
Requires:       puppet = %{version}-%{release}
Requires:	policycoreutils

%description server-selinux
Selinux modules for the puppet system management tool

%package vim
Group:		Applications/Editors
Summary:	vim syntax modules for puppet
Requires:	vim-enhanced

%description vim
puppet syntax files for vim.

To install these files, copy them into ~/.vim, or the relevant
system-wide location.  To use the ftplugin and indenting, you may need
to enable them with "filetype plugin indent on" in your vimrc.

%package emacs
Group:		Applications/Editors
Summary: 	emacs syntax modules for puppet
Requires:	emacs

%description emacs
puppet syntax files for emacs

%prep
%setup -q
patch -s -p1 < conf/redhat/rundir-perms.patch

# selinux
%setup -a 100


%build
# Fix some rpmlint complaints
for f in mac_dscl.pp mac_dscl_revert.pp \
         mac_pkgdmg.pp ; do
  sed -i -e'1d' examples/$f
  chmod a-x examples/$f
done
# mongrel was replaced by passenger
#for f in external/nagios.rb network/http_server/mongrel.rb relationship.rb; do
# this removes the /usr/bin/env line
for f in external/nagios.rb relationship.rb; do
  sed -i -e '1d' lib/puppet/$f
done
#chmod +x ext/puppetstoredconfigclean.rb

find examples/ -type f -empty | xargs rm
find examples/ -type f | xargs chmod a-x

# puppet-queue.conf is more of an example, used for stompserver
mv conf/puppet-queue.conf examples/etc/puppet/

# selinux policy
make -f /usr/share/selinux/devel/Makefile -C %{name}-selinux

%install
rm -rf %{buildroot}
ruby install.rb --destdir=%{buildroot} --quick --no-rdoc

install -d -m0755 %{buildroot}%{_sysconfdir}/puppet/manifests
install -d -m0755 %{buildroot}%{_datadir}/%{name}/modules
install -d -m0755 %{buildroot}%{_localstatedir}/lib/puppet
install -d -m0755 %{buildroot}%{_localstatedir}/run/puppet
install -d -m0750 %{buildroot}%{_localstatedir}/log/puppet
install -Dp -m0644 %{confdir}/client.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/puppet
install -Dp -m0755 %{confdir}/client.init %{buildroot}%{_initrddir}/puppet
install -Dp -m0644 %{confdir}/server.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/puppetmaster
install -Dp -m0755 %{confdir}/server.init %{buildroot}%{_initrddir}/puppetmaster
install -Dp -m0644 %{confdir}/fileserver.conf %{buildroot}%{_sysconfdir}/puppet/fileserver.conf
install -Dp -m0644 %{confdir}/puppet.conf %{buildroot}%{_sysconfdir}/puppet/puppet.conf
install -Dp -m0644 %{confdir}/logrotate %{buildroot}%{_sysconfdir}/logrotate.d/puppet

# We need something for these ghosted files, otherwise rpmbuild
# will complain loudly. They won't be included in the binary packages
touch %{buildroot}%{_sysconfdir}/puppet/puppetmasterd.conf
touch %{buildroot}%{_sysconfdir}/puppet/puppetca.conf
touch %{buildroot}%{_sysconfdir}/puppet/puppetd.conf

# Install the ext/ directory to %{_datadir}/%{name}
install -d %{buildroot}%{_datadir}/%{name}
cp -a ext/ %{buildroot}%{_datadir}/%{name}
# emacs and vim bits are installed elsewhere
rm -rf %{buildroot}%{_datadir}/%{name}/ext/{emacs,vim}

# Install emacs mode files
emacsdir=%{buildroot}%{_datadir}/emacs/site-lisp
install -Dp -m0644 ext/emacs/puppet-mode.el $emacsdir/puppet-mode.el
install -Dp -m0644 ext/emacs/puppet-mode-init.el \
    $emacsdir/site-start.d/puppet-mode-init.el

# Install vim syntax files
install -Dp -m0644 ext/vim/ftdetect/puppet.vim $RPM_BUILD_ROOT/%{vimdir}/ftdetect/puppet.vim
install -Dp -m0644 ext/vim/ftplugin/puppet.vim $RPM_BUILD_ROOT/%{vimdir}/ftplugin/puppet.vim
install -Dp -m0644 ext/vim/indent/puppet.vim $RPM_BUILD_ROOT/%{vimdir}/indent/puppet.vim
install -Dp -m0644 ext/vim/syntax/puppet.vim $RPM_BUILD_ROOT/%{vimdir}/syntax/puppet.vim

# selinux
install -p -m 644 -D %{name}-selinux/%{name}-passenger.pp $RPM_BUILD_ROOT/%{_datadir}/selinux/packages/%{name}/%{name}-passenger.pp

%files
%defattr(-, root, root)
%doc CHANGELOG CONTRIBUTING.md LICENSE README.md examples
%{_bindir}/pi
%{_bindir}/puppet
%{_bindir}/ralsh
%{_bindir}/filebucket
%{_bindir}/puppetdoc
%{_sbindir}/puppetca
%{_sbindir}/puppetd
%{ruby_sitelibdir}/*
%{_initrddir}/puppet
%dir %{_sysconfdir}/puppet
%config(noreplace) %{_sysconfdir}/sysconfig/puppet
%config(noreplace) %{_sysconfdir}/puppet/puppet.conf
%config(noreplace) %{_sysconfdir}/puppet/auth.conf
%ghost %config(noreplace,missingok) %{_sysconfdir}/puppet/puppetca.conf
%ghost %config(noreplace,missingok) %{_sysconfdir}/puppet/puppetd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/puppet
%{_datadir}/%{name}
# These need to be owned by puppet so the server can
# write to them
%attr(1777, puppet, puppet) %{_localstatedir}/run/puppet
%attr(0750, puppet, puppet) %{_localstatedir}/log/puppet
%attr(-, puppet, puppet) %{_localstatedir}/lib/puppet
%{_mandir}/man5/puppet.conf.5.gz
%{_mandir}/man8/pi.8.gz
%{_mandir}/man8/puppet.8.gz
%{_mandir}/man8/puppetca.8.gz
%{_mandir}/man8/puppetd.8.gz
%{_mandir}/man8/ralsh.8.gz
%{_mandir}/man8/puppetdoc.8.gz
# uphill
%{_mandir}/man8/puppet-agent.8.gz
%{_mandir}/man8/puppet-apply.8.gz
%{_mandir}/man8/puppet-ca.8.gz
%{_mandir}/man8/puppet-certificate_request.8.gz
%{_mandir}/man8/puppet-config.8.gz
%{_mandir}/man8/puppet-describe.8.gz
%{_mandir}/man8/puppet-doc.8.gz
%{_mandir}/man8/puppet-file.8.gz
%{_mandir}/man8/puppet-filebucket.8.gz
%{_mandir}/man8/puppet-help.8.gz
%{_mandir}/man8/puppet-inspect.8.gz
%{_mandir}/man8/puppet-instrumentation_data.8.gz
%{_mandir}/man8/puppet-instrumentation_listener.8.gz
%{_mandir}/man8/puppet-instrumentation_probe.8.gz
%{_mandir}/man8/puppet-key.8.gz
%{_mandir}/man8/puppet-kick.8.gz
%{_mandir}/man8/puppet-man.8.gz
%{_mandir}/man8/puppet-module.8.gz
%{_mandir}/man8/puppet-node.8.gz
%{_mandir}/man8/puppet-parser.8.gz
%{_mandir}/man8/puppet-queue.8.gz
%{_mandir}/man8/puppet-resource.8.gz
%{_mandir}/man8/puppet-resource_type.8.gz
%{_mandir}/man8/puppet-secret_agent.8.gz
%{_mandir}/man8/puppet-status.8.gz

%files vim
# we do want to require vim for the vim package...
%defattr(-, root, root, 0755)
%{_datadir}/vim

%files emacs
# we do want to require emacs for the emacs package...
%defattr(-, root, root, 0755)
%{_datadir}/emacs

%files server
%defattr(-, root, root, 0755)
%{_sbindir}/puppetmasterd
%{_sbindir}/puppetrun
%{_sbindir}/puppetqd
%{_initrddir}/puppetmaster
%config(noreplace) %{_sysconfdir}/puppet/fileserver.conf
%dir %{_sysconfdir}/puppet/manifests
%config(noreplace) %{_sysconfdir}/sysconfig/puppetmaster
%ghost %config(noreplace,missingok) %{_sysconfdir}/puppet/puppetmasterd.conf
%{_mandir}/man8/filebucket.8.gz
%{_mandir}/man8/puppetmasterd.8.gz
%{_mandir}/man8/puppetrun.8.gz
%{_mandir}/man8/puppetqd.8.gz
# uphill
%{_mandir}/man8/puppet-catalog.8.gz
%{_mandir}/man8/puppet-cert.8.gz
%{_mandir}/man8/puppet-certificate.8.gz
%{_mandir}/man8/puppet-certificate_revocation_list.8.gz
%{_mandir}/man8/puppet-device.8.gz
%{_mandir}/man8/puppet-facts.8.gz
%{_mandir}/man8/puppet-master.8.gz
%{_mandir}/man8/puppet-plugin.8.gz
%{_mandir}/man8/puppet-report.8.gz

%files server-selinux
%defattr(-, root, root, 0755)
%{_datadir}/selinux/packages/%{name}/%{name}-passenger.pp


# Fixed uid/gid were assigned in bz 472073 (Fedora), 471918 (RHEL-5),
# and 471919 (RHEL-4)
%pre
getent group puppet &>/dev/null || groupadd -r puppet -g 52 &>/dev/null
getent passwd puppet &>/dev/null || \
useradd -r -u 52 -g puppet -d %{_localstatedir}/lib/puppet -s /sbin/nologin \
    -c "Puppet" puppet &>/dev/null
# ensure that old setups have the right puppet home dir
if [ $1 -gt 1 ] ; then
  usermod -d %{_localstatedir}/lib/puppet puppet &>/dev/null
fi
exit 0

%post
/sbin/chkconfig --add puppet || :
if [ "$1" -ge 1 ]; then
  # The pidfile changed from 0.25.x to 2.6.x, handle upgrades without leaving
  # the old process running.
  oldpid="%{_localstatedir}/run/puppet/puppetd.pid"
  newpid="%{_localstatedir}/run/puppet/agent.pid"
  if [ -s "$oldpid" -a ! -s "$newpid" ]; then
    (kill $(< "$oldpid") && rm -f "$oldpid" && \
      /sbin/service puppet start) >/dev/null 2>&1 || :
  fi
fi

%post server
/sbin/chkconfig --add puppetmaster || :
if [ "$1" -ge 1 ]; then
  # The pidfile changed from 0.25.x to 2.6.x, handle upgrades without leaving
  # the old process running.
  oldpid="%{_localstatedir}/run/puppet/puppetmasterd.pid"
  newpid="%{_localstatedir}/run/puppet/master.pid"
  if [ -s "$oldpid" -a ! -s "$newpid" ]; then
    (kill $(< "$oldpid") && rm -f "$oldpid" && \
      /sbin/service puppetmaster start) >/dev/null 2>&1 || :
  fi
fi

%preun
if [ "$1" = 0 ] ; then
  /sbin/service puppet stop >/dev/null 2>&1
  /sbin/chkconfig --del puppet || :
fi

%preun server
if [ "$1" = 0 ] ; then
  /sbin/service puppetmaster stop >/dev/null 2>&1
  /sbin/chkconfig --del puppetmaster || :
fi

%postun
if [ "$1" -ge 1 ]; then
  /sbin/service puppet condrestart >/dev/null 2>&1 || :
fi

%postun server
if [ "$1" -ge 1 ]; then
  /sbin/service puppetmaster condrestart >/dev/null 2>&1 || :
fi

%post server-selinux
if [ "$1" -le "1" ]; then # first install
semodule -i %{_datadir}/selinux/packages/%{name}/%{name}-passenger.pp 2>/dev/null || :
fi

%preun server-selinux
if [ "$1" -lt "1" ]; then # final removal
semodule -r %{name}-passenger 2>/dev/null || :
fi

%postun server-selinux
if [ "$1" -ge "1" ]; then # upgrade
semodule -u %{_datadir}/selinux/packages/%{name}/%{name}-passenger.pp 2>/dev/null || :
fi

%clean
rm -rf %{buildroot}

%changelog
* Thu Sep 20 2012 Josko Plazonic <plazonic@math.princeton.edu> - 2.7.19-9
- yet another selinux tweak

* Wed Sep 19 2012 Josko Plazonic <plazonic@math.princeton.edu> - 2.7.19-8
- upgrade to 2.7.19 and tweak selinux module

* Fri Jul 20 2012 Thomas Uphill <uphill@ias.edu> - 2.7.18-5
- inc'd the release on the selinux module

* Tue Jul 17 2012 Thomas Uphill <uphill@ias.edu> - 2.7.18-4
- added to selinux module:
    allow httpd_t passenger_tmp_t:file unlink;

* Thu Jul 12 2012 Thomas Uphill <uphill@ias.edu> - 2.7.18-3
- added to selinux module:
    allow httpd_t passenger_tmp_t:dir remove_name;
    allow httpd_t passenger_tmp_t:file getattr;

* Tue May 08 2012 Thomas Uphill <uphill@ias.edu> - 2.7.14-2
- added augeas as dependency

* Fri May 04 2012 Thomas Uphill <uphill@ias.edu> - 2.7.14-1
- update to 2.7.14

* Tue Apr 24 2012 Thomas Uphill <uphill@ias.edu> - 2.7.14-rc2
- update to 2.7.14-rc2 (for testing purposes)

* Wed Apr 04 2012 Thomas Uphill <uphill@ias.edu> - 2.7.12
- update to 2.7.12
- updated selinux policy, many of the things we were doing are now in the default policy
- changed semodule to use upgrade (-u) when upgrading.

* Wed Mar 09 2011 Todd Zullinger <tmz@pobox.com> - 2.6.6-0.2
- Update to 2.6.6

* Wed Mar 02 2011 Todd Zullinger <tmz@pobox.com> - 2.6.6-0.1.rc1
- Update to 2.6.6rc1

* Mon Feb 28 2011 Todd Zullinger <tmz@pobox.com> - 2.6.5-1
- Update to 2.6.5

* Mon Feb 21 2011 Todd Zullinger <tmz@pobox.com> - 2.6.5-0.5.rc5
- Update to 2.6.5-rc5

* Wed Feb 16 2011 Todd Zullinger <tmz@pobox.com> - 2.6.5-0.4.rc4
- Fix License tag, puppet is now GPLv2 only

* Mon Feb 14 2011 Todd Zullinger <tmz@pobox.com> - 2.6.5-0.3.rc4
- Update to 2.6.5-rc4

* Fri Feb 11 2011 Todd Zullinger <tmz@pobox.com> - 2.6.5-0.2.rc2
- Update to 2.6.5-rc2

* Sun Feb 06 2011 Todd Zullinger <tmz@pobox.com> - 2.6.5-0.1.rc1
- Update to 2.6.5-rc1

* Tue Jan 11 2011 Todd Zullinger <tmz@pobox.com> - 2.6.4-0.7
- Properly restart puppet agent/master daemons on upgrades from 0.25.x
  (pidfiles changed)

* Wed Dec 01 2010 Todd Zullinger <tmz@pobox.com> - 2.6.4-0.6
- Drop explicit auth.conf install, the stock install script handles this

* Wed Dec 01 2010 Todd Zullinger <tmz@pobox.com> - 2.6.4-0.5
- Update to 2.6.4

* Tue Nov 16 2010 Todd Zullinger <tmz@pobox.com> - 2.6.3-0.4
- Update to 2.6.3

* Fri Nov 12 2010 Todd Zullinger <tmz@pobox.com> - 2.6.3-0.3.rc3
- Update to 2.6.3rc3

* Thu Oct 28 2010 Todd Zullinger <tmz@pobox.com> - 2.6.3-0.3.rc2
- Update to 2.6.3rc2

* Fri Oct 15 2010 Todd Zullinger <tmz@pobox.com> - 2.6.3-0.2.rc1
- Ensure %%pre exits cleanly

* Thu Oct 14 2010 Todd Zullinger <tmz@pobox.com> - 2.6.3-0.1.rc1
- Update to 2.6.3rc1

* Thu Oct 07 2010 Todd Zullinger <tmz@pobox.com> - 2.6.2-0.3
- Update to 2.6.2

* Mon Oct 04 2010 Todd Zullinger <tmz@pobox.com> - 2.6.2-0.2.rc1
- Apply upstream patch for spurious warnings
  http://projects.puppetlabs.com/issues/4919

* Sat Oct 02 2010 Todd Zullinger <tmz@pobox.com> - 2.6.2-0.1.rc1
- Update to 2.6.2rc1
- Fix man page installation

* Thu Sep 16 2010 Todd Zullinger <tmz@pobox.com> - 2.6.1-0.6
- Apply upstream fix in testing to fix implicit tagging
  http://projects.puppetlabs.com/issues/4631

* Mon Sep 13 2010 Todd Zullinger <tmz@pobox.com> - 2.6.1-0.5
- Update to 2.6.1

* Tue Sep 07 2010 Todd Zullinger <tmz@pobox.com> - 2.6.1-0.4.rc4
- Update to 2.6.1rc4

* Wed Aug 25 2010 Todd Zullinger <tmz@pobox.com> - 2.6.1-0.3.rc3
- Update to 2.6.1rc3

* Mon Aug 16 2010 Todd Zullinger <tmz@pobox.com> - 2.6.1-0.2.rc2
- Update to 2.6.1rc2

* Mon Jul 26 2010 Todd Zullinger <tmz@pobox.com> - 2.6.1-0.1.rc1
- Update to 2.6.1rc1

* Tue Jul 20 2010 Todd Zullinger <tmz@pobox.com> - 2.6.0-0.7
- Update to 2.6.0

* Mon Jul 19 2010 Todd Zullinger <tmz@pobox.com> - 2.6.0-0.6.rc4
- Update to 2.6.0rc4

* Fri Jul 16 2010 Todd Zullinger <tmz@pobox.com> - 2.6.0-0.5.rc3
- Create and own /usr/share/puppet/modules (#615432)

* Wed Jul 14 2010 Todd Zullinger <tmz@pobox.com> - 2.6.0-0.4.rc3
- Update to 2.6.0rc3

* Tue Jul 13 2010 Todd Zullinger <tmz@pobox.com> - 2.6.0-0.3.rc2
- Add patches for misc issues in included conf/init files

* Mon Jul 12 2010 Todd Zullinger <tmz@pobox.com> - 2.6.0-0.2.rc2
- Update to 2.6.0rc2

* Sat Jul 10 2010 Todd Zullinger <tmz@pobox.com> - 2.6.0-0.1.rc1
- Update to 2.6.0rc1

* Mon May 17 2010 Todd Zullinger <tmz@pobox.com> - 0.25.5-1
- Update to 0.25.5
- Adjust selinux conditional for EL-6
- Apply rundir-perms patch from tarball rather than including it separately
- Update URL's to reflect the new puppetlabs.com domain

* Fri Jan 29 2010 Todd Zullinger <tmz@pobox.com> - 0.25.4-1
- Update to 0.25.4

* Tue Jan 19 2010 Todd Zullinger <tmz@pobox.com> - 0.25.3-2
- Apply upstream patch to fix cron resources (upstream #2845)

* Mon Jan 11 2010 Todd Zullinger <tmz@pobox.com> - 0.25.3-1
- Update to 0.25.3

* Tue Jan 05 2010 Todd Zullinger <tmz@pobox.com> - 0.25.2-1.1
- Replace %%define with %%global for macros

* Tue Jan 05 2010 Todd Zullinger <tmz@pobox.com> - 0.25.2-1
- Update to 0.25.2
- Fixes CVE-2010-0156, tmpfile security issue (#502881)
- Install auth.conf, puppetqd manpage, and queuing examples/docs

* Wed Nov 25 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.25.1-1
- New upstream version

* Tue Oct 27 2009 Todd Zullinger <tmz@pobox.com> - 0.25.1-0.3
- Update to 0.25.1
- Include the pi program and man page (R.I.Pienaar)

* Sat Oct 17 2009 Todd Zullinger <tmz@pobox.com> - 0.25.1-0.2.rc2
- Update to 0.25.1rc2

* Tue Sep 22 2009 Todd Zullinger <tmz@pobox.com> - 0.25.1-0.1.rc1
- Update to 0.25.1rc1
- Move puppetca to puppet package, it has uses on client systems
- Drop redundant %%doc from manpage %%file listings

* Fri Sep 04 2009 Todd Zullinger <tmz@pobox.com> - 0.25.0-1
- Update to 0.25.0
- Fix permissions on /var/log/puppet (#495096)
- Install emacs mode and vim syntax files (#491437)
- Install ext/ directory in %%{_datadir}/%{name} (/usr/share/puppet)

* Mon May 04 2009 Todd Zullinger <tmz@pobox.com> - 0.25.0-0.1.beta1
- Update to 0.25.0beta1
- Make Augeas and SELinux requirements build time options

* Mon Mar 23 2009 Todd Zullinger <tmz@pobox.com> - 0.24.8-1
- Update to 0.24.8
- Quiet output from %%pre
- Use upstream install script
- Increase required facter version to >= 1.5

* Tue Dec 16 2008 Todd Zullinger <tmz@pobox.com> - 0.24.7-4
- Remove redundant useradd from %%pre

* Tue Dec 16 2008 Jeroen van Meeuwen <kanarip@kanarip.com> - 0.24.7-3
- New upstream version
- Set a static uid and gid (#472073, #471918, #471919)
- Add a conditional requirement on libselinux-ruby for Fedora >= 9
- Add a dependency on ruby-augeas

* Wed Oct 22 2008 Todd Zullinger <tmz@pobox.com> - 0.24.6-1
- Update to 0.24.6
- Require ruby-shadow on Fedora and RHEL >= 5
- Simplify Fedora/RHEL version checks for ruby(abi) and BuildArch
- Require chkconfig and initstripts for preun, post, and postun scripts
- Conditionally restart puppet in %%postun
- Ensure %%preun, %%post, and %%postun scripts exit cleanly
- Create puppet user/group according to Fedora packaging guidelines
- Quiet a few rpmlint complaints
- Remove useless %%pbuild macro
- Make specfile more like the Fedora/EPEL template

* Mon Jul 28 2008 David Lutterkort <dlutter@redhat.com> - 0.24.5-1
- Add /usr/bin/puppetdoc

* Thu Jul 24 2008 Brenton Leanhardt <bleanhar@redhat.com>
- New version
- man pages now ship with tarball
- examples/code moved to root examples dir in upstream tarball

* Tue Mar 25 2008 David Lutterkort <dlutter@redhat.com> - 0.24.4-1
- Add man pages (from separate tarball, upstream will fix to
  include in main tarball)

* Mon Mar 24 2008 David Lutterkort <dlutter@redhat.com> - 0.24.3-1
- New version

* Wed Mar  5 2008 David Lutterkort <dlutter@redhat.com> - 0.24.2-1
- New version

* Sat Dec 22 2007 David Lutterkort <dlutter@redhat.com> - 0.24.1-1
- New version

* Mon Dec 17 2007 David Lutterkort <dlutter@redhat.com> - 0.24.0-2
- Use updated upstream tarball that contains yumhelper.py

* Fri Dec 14 2007 David Lutterkort <dlutter@redhat.com> - 0.24.0-1
- Fixed license
- Munge examples/ to make rpmlint happier

* Wed Aug 22 2007 David Lutterkort <dlutter@redhat.com> - 0.23.2-1
- New version

* Thu Jul 26 2007 David Lutterkort <dlutter@redhat.com> - 0.23.1-1
- Remove old config files

* Wed Jun 20 2007 David Lutterkort <dlutter@redhat.com> - 0.23.0-1
- Install one puppet.conf instead of old config files, keep old configs
  around to ease update
- Use plain shell commands in install instead of macros

* Wed May  2 2007 David Lutterkort <dlutter@redhat.com> - 0.22.4-1
- New version

* Thu Mar 29 2007 David Lutterkort <dlutter@redhat.com> - 0.22.3-1
- Claim ownership of _sysconfdir/puppet (bz 233908)

* Mon Mar 19 2007 David Lutterkort <dlutter@redhat.com> - 0.22.2-1
- Set puppet's homedir to /var/lib/puppet, not /var/puppet
- Remove no-lockdir patch, not needed anymore

* Mon Feb 12 2007 David Lutterkort <dlutter@redhat.com> - 0.22.1-2
- Fix bogus config parameter in puppetd.conf

* Sat Feb  3 2007 David Lutterkort <dlutter@redhat.com> - 0.22.1-1
- New version

* Fri Jan  5 2007 David Lutterkort <dlutter@redhat.com> - 0.22.0-1
- New version

* Mon Nov 20 2006 David Lutterkort <dlutter@redhat.com> - 0.20.1-2
- Make require ruby(abi) and buildarch: noarch conditional for fedora 5 or
  later to allow building on older fedora releases

* Mon Nov 13 2006 David Lutterkort <dlutter@redhat.com> - 0.20.1-1
- New version

* Mon Oct 23 2006 David Lutterkort <dlutter@redhat.com> - 0.20.0-1
- New version

* Tue Sep 26 2006 David Lutterkort <dlutter@redhat.com> - 0.19.3-1
- New version

* Mon Sep 18 2006 David Lutterkort <dlutter@redhat.com> - 0.19.1-1
- New version

* Thu Sep  7 2006 David Lutterkort <dlutter@redhat.com> - 0.19.0-1
- New version

* Tue Aug  1 2006 David Lutterkort <dlutter@redhat.com> - 0.18.4-2
- Use /usr/bin/ruby directly instead of /usr/bin/env ruby in
  executables. Otherwise, initscripts break since pidof can't find the
  right process

* Tue Aug  1 2006 David Lutterkort <dlutter@redhat.com> - 0.18.4-1
- New version

* Fri Jul 14 2006 David Lutterkort <dlutter@redhat.com> - 0.18.3-1
- New version

* Wed Jul  5 2006 David Lutterkort <dlutter@redhat.com> - 0.18.2-1
- New version

* Wed Jun 28 2006 David Lutterkort <dlutter@redhat.com> - 0.18.1-1
- Removed lsb-config.patch and yumrepo.patch since they are upstream now

* Mon Jun 19 2006 David Lutterkort <dlutter@redhat.com> - 0.18.0-1
- Patch config for LSB compliance (lsb-config.patch)
- Changed config moves /var/puppet to /var/lib/puppet, /etc/puppet/ssl
  to /var/lib/puppet, /etc/puppet/clases.txt to /var/lib/puppet/classes.txt,
  /etc/puppet/localconfig.yaml to /var/lib/puppet/localconfig.yaml

* Fri May 19 2006 David Lutterkort <dlutter@redhat.com> - 0.17.2-1
- Added /usr/bin/puppetrun to server subpackage
- Backported patch for yumrepo type (yumrepo.patch)

* Wed May  3 2006 David Lutterkort <dlutter@redhat.com> - 0.16.4-1
- Rebuilt

* Fri Apr 21 2006 David Lutterkort <dlutter@redhat.com> - 0.16.0-1
- Fix default file permissions in server subpackage
- Run puppetmaster as user puppet
- rebuilt for 0.16.0

* Mon Apr 17 2006 David Lutterkort <dlutter@redhat.com> - 0.15.3-2
- Don't create empty log files in post-install scriptlet

* Fri Apr  7 2006 David Lutterkort <dlutter@redhat.com> - 0.15.3-1
- Rebuilt for new version

* Wed Mar 22 2006 David Lutterkort <dlutter@redhat.com> - 0.15.1-1
- Patch0: Run puppetmaster as root; running as puppet is not ready
  for primetime

* Mon Mar 13 2006 David Lutterkort <dlutter@redhat.com> - 0.15.0-1
- Commented out noarch; requires fix for bz184199

* Mon Mar  6 2006 David Lutterkort <dlutter@redhat.com> - 0.14.0-1
- Added BuildRequires for ruby

* Wed Mar  1 2006 David Lutterkort <dlutter@redhat.com> - 0.13.5-1
- Removed use of fedora-usermgmt. It is not required for Fedora Extras and
  makes it unnecessarily hard to use this rpm outside of Fedora. Just
  allocate the puppet uid/gid dynamically

* Sun Feb 19 2006 David Lutterkort <dlutter@redhat.com> - 0.13.0-4
- Use fedora-usermgmt to create puppet user/group. Use uid/gid 24. Fixed
problem with listing fileserver.conf and puppetmaster.conf twice

* Wed Feb  8 2006 David Lutterkort <dlutter@redhat.com> - 0.13.0-3
- Fix puppetd.conf

* Wed Feb  8 2006 David Lutterkort <dlutter@redhat.com> - 0.13.0-2
- Changes to run puppetmaster as user puppet

* Mon Feb  6 2006 David Lutterkort <dlutter@redhat.com> - 0.13.0-1
- Don't mark initscripts as config files

* Mon Feb  6 2006 David Lutterkort <dlutter@redhat.com> - 0.12.0-2
- Fix BuildRoot. Add dist to release

* Tue Jan 17 2006 David Lutterkort <dlutter@redhat.com> - 0.11.0-1
- Rebuild

* Thu Jan 12 2006 David Lutterkort <dlutter@redhat.com> - 0.10.2-1
- Updated for 0.10.2 Fixed minor kink in how Source is given

* Wed Jan 11 2006 David Lutterkort <dlutter@redhat.com> - 0.10.1-3
- Added basic fileserver.conf

* Wed Jan 11 2006 David Lutterkort <dlutter@redhat.com> - 0.10.1-1
- Updated. Moved installation of library files to sitelibdir. Pulled
initscripts into separate files. Folded tools rpm into server

* Thu Nov 24 2005 Duane Griffin <d.griffin@psenterprise.com>
- Added init scripts for the client

* Wed Nov 23 2005 Duane Griffin <d.griffin@psenterprise.com>
- First packaging

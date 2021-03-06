Summary: The InterNetNews system, an Usenet news server
Name: inn
Version: 2.5.2
Release: 4%{?dist}
#see LICENSE file for details
License: GPLv2+ and BSD and MIT and Public Domain
Group: System Environment/Daemons
URL: https://www.isc.org/software/INN/
Source0: ftp://ftp.isc.org/isc/inn/inn-%{version}.tar.gz
Source2: inn-default-distributions
Source4: inn-cron-expire
Source5: inn-cron-rnews
Source7: inn-cron-nntpsend
Source8: innd.init
Source10: inn-faq.tar.gz
Patch1:  inn-2.4.3.rh.patch
Patch4: inn-2.5.1.pie.patch
Patch6: inn-2.5.2.posix.patch
Patch7: inn-2.4.3.warn.patch
Patch8: inn-2.4.2-makedbz.patch
Patch10: inn-2.5.1-nologinshell.patch
Patch13: inn-2.5.0-chown.patch
Patch14: inn-redhat_build.patch
Patch15: inn-shared.patch
Patch16: inn-2.5.2-hdr.patch
patch17: inn-2.5.2-pconf.patch
Patch18: inn-2.5.2-smp.patch
BuildRequires: python db4-devel byacc krb5-devel pam-devel e2fsprogs-devel perl
BuildRequires: perl(ExtUtils::Embed) flex
Requires(pre): shadow-utils
Requires: chkconfig, grep, coreutils, sed
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires: bash >= 2.0
Requires(post): inews

# XXX white out bogus perl requirement for now
Provides: perl(::usr/lib/innshellvars.pl) = %{version}-%{release}

Buildroot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
INN (InterNetNews) is a complete system for serving Usenet news and/or
private newsfeeds.  INN includes innd, an NNTP (NetNews Transport
Protocol) server, and nnrpd, a newsreader that is spawned for each
client.  Both innd and nnrpd vary slightly from the NNTP protocol, but
not in ways that are easily noticed.

Install the inn package if you need a complete system for serving and
reading Usenet news.  You may also need to install inn-devel, if you
are going to use a separate program which interfaces to INN, like
newsgate or tin.

%package devel
Summary: The INN (InterNetNews) library
Group: Development/Libraries
Requires: inn = %{version}
Requires: %{name}-libs = %{version}-%{release}

%description devel
The inn-devel package contains the INN (InterNetNews) library, which
several programs that interface with INN need in order to work (for
example, newsgate and tin).

If you are installing a program which must interface with the INN news
system, you should install inn-devel.

%package -n inews
Summary: Sends Usenet articles to a local news server for distribution
Group: System Environment/Daemons

%description -n inews
The inews program is used by some news programs (for example, inn and
trn) to post Usenet news articles to local news servers.  Inews reads
an article from a file or standard input, adds headers, performs some
consistency checks and then sends the article to the local news server
specified in the inn.conf file.

Install inews if you need a program for posting Usenet articles to
local news servers.

%package libs
Summary: Libraries provided by INN
Group: Applications/System

%description libs
This package contains dynamic libraries provided by INN project

%pre
getent group news >/dev/null || groupadd -g 13 -r news
getent passwd news >/dev/null || \
useradd -r -u 9 -g news -d /etc/news -s /sbin/nologin \
-c "News server user" news
exit 0

%prep
%setup -q
%patch1 -p1 -b .rh
%patch4 -p1 -b .pie
%patch6 -p1 -b .posix
%patch7 -p1 -b .warn
%patch8 -p1 -b .makedbz
%patch10 -p1 -b .nologin
%patch13 -p1 -b .chown
%patch14 -p1 -b .redhat_build
%patch15 -p1 -b .shared
%patch16 -p1 -b .hdr
%patch17 -p1 -b .pfix
%patch18 -p1 -b .smp

perl -pi -e 's/LOCK_READ/LLOCK_READ/' `find . -type f`
perl -pi -e 's/LOCK_WRITE/LLOCK_WRITE/' `find . -type f`

%build
export DEFINE_INN_FLAGS="-D_XOPEN_SOURCE=600 -D_BSD_SOURCE -DHAVE_ET_COM_ERR_H"
export CFLAGS="$RPM_OPT_FLAGS $DEFINE_INN_FLAGS -fno-strict-aliasing -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"

%ifarch s390 s390x sparc sparcv9 sparc64
export CFLAGS="$CFLAGS -fPIC"
%else
export CFLAGS="$CFLAGS -fpic"
%endif

%configure --bindir=%{_libexecdir}/news \
  --sysconfdir=%{_sysconfdir}/news --exec-prefix=%{_libexecdir}/news \
  --with-log-dir=/var/log/news --with-spool-dir=/var/spool/news\
  --with-db-dir=%{_sharedstatedir}/news --with-run-dir=/var/run/news \
  --with-etc-dir=%{_sysconfdir}/news --with-tmp-dir=%{_sharedstatedir}/news/tmp \
  --with-perl --enable-shared --enable-uucp-rnews \
  --with-libperl-dir=%{perl_vendorlib} \
  --enable-pgp-verify --with-sendmail=/usr/sbin/sendmail \
  --with-news-user=news --with-news-group=news --with-news-master=news \
  --enable-ipv6 --with-http-dir=%{_sharedstatedir}/news/http \
  --enable-libtool --disable-static --with-pic

# Don't hardcode rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/news/http
make install DESTDIR=$RPM_BUILD_ROOT

# -- Install man pages needed by suck et al.
mkdir -p $RPM_BUILD_ROOT%{_includedir}/inn

for f in clibrary.h config.h
do
    install -p -m 0644 ./include/$f $RPM_BUILD_ROOT%{_includedir}/inn
done
for f in defines.h system.h libinn.h storage.h options.h dbz.h
do
    install -p -m 0644 ./include/inn/$f $RPM_BUILD_ROOT%{_includedir}/inn
done

touch     $RPM_BUILD_ROOT%{_sharedstatedir}/news/subscriptions
chmod 644 $RPM_BUILD_ROOT%{_sharedstatedir}/news/subscriptions

install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sharedstatedir}/news/distributions

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cron.{hourly,daily}
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/inn-cron-expire
install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/cron.hourly/inn-cron-rnews
install %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/cron.hourly/inn-cron-nntpsend

mkdir -p $RPM_BUILD_ROOT%{_initrddir}
install %{SOURCE8} $RPM_BUILD_ROOT%{_initrddir}/innd

tar xf %{SOURCE10}
mv inn.html FAQ.html

touch $RPM_BUILD_ROOT%{_sharedstatedir}/news/history
#LD_LIBRARY_PATH=$RPM_BUILD_ROOT/usr/lib $RPM_BUILD_ROOT/usr/bin/makedbz -i \
# -f $RPM_BUILD_ROOT/var/lib/news/history
#chmod 644 $RPM_BUILD_ROOT/var/lib/news/*

cat > $RPM_BUILD_ROOT%{_sysconfdir}/news/.profile <<EOF
PATH=\$PATH:%{_libexecdir}/news
export PATH
EOF

#Fix perms in sample directory to avoid bogus dependencies
find samples -name "*.in" -exec chmod a-x {} \;

# we get this from cleanfeed
rm -f $RPM_BUILD_ROOT%{_libexecdir}/news/filter/filter_innd.pl

mkdir -p $RPM_BUILD_ROOT%{_bindir}
ln -sf %{_libexecdir}/news/inews $RPM_BUILD_ROOT%{_bindir}/inews
ln -sf %{_libexecdir}/news/rnews $RPM_BUILD_ROOT%{_bindir}/rnews

# Remove unwanted files
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.a

# Documentation is installed via rpm %%doc directive
rm -rf $RPM_BUILD_ROOT/usr/doc/

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add innd
#su -m news -c '/usr/lib/news/bin/makehistory'
su -m news -c '/usr/libexec/news/makedbz -i -o'

umask 002
touch /var/log/news/news.notice
touch /var/log/news/news.crit
touch /var/log/news/news.err
chown -R news:news /var/log/news*

%post libs -p /sbin/ldconfig

%triggerpostun -- inn < 2.3.0
service innd stop > /dev/null 2>&1

%triggerin -- rsyslog
if [ -f /etc/rsyslog.conf ]; then
  if ! grep -q INN /etc/rsyslog.conf; then
    sed 's/mail.none;/mail.none;news.none;/' < /etc/rsyslog.conf > /etc/rsyslog.conf.inn
    mv /etc/rsyslog.conf.inn /etc/rsyslog.conf

    echo '' \
       >> /etc/rsyslog.conf
    echo '#' \
       >> /etc/rsyslog.conf
    echo '# INN' \
       >> /etc/rsyslog.conf
    echo '#' \
       >> /etc/rsyslog.conf
    echo 'news.=crit                                        /var/log/news/news.crit'   >> /etc/rsyslog.conf
    echo 'news.=err                                         /var/log/news/news.err'    >> /etc/rsyslog.conf
    echo 'news.notice                                       /var/log/news/news.notice' >> /etc/rsyslog.conf
    echo 'news.=debug                                       /var/log/news/news.debug' >> /etc/rsyslog.conf

    fi
  if [ -f /var/run/rsyslogd.pid ]; then
    kill -HUP `cat /var/run/rsyslogd.pid` 2> /dev/null ||:
  fi
fi

%triggerin -- sysklogd
if [ -f /etc/syslog.conf ]; then
  if ! grep -q INN /etc/syslog.conf; then
    sed 's/mail.none;/mail.none;news.none;/' < /etc/syslog.conf > /etc/syslog.conf.inn
    mv /etc/syslog.conf.inn /etc/syslog.conf

    echo '' \
       >> /etc/syslog.conf
    echo '#' \
       >> /etc/syslog.conf
    echo '# INN' \
       >> /etc/syslog.conf
    echo '#' \
       >> /etc/syslog.conf
    echo 'news.=crit                                        /var/log/news/news.crit'   >> /etc/syslog.conf
    echo 'news.=err                                         /var/log/news/news.err'    >> /etc/syslog.conf
    echo 'news.notice                                       /var/log/news/news.notice' >> /etc/syslog.conf
    fi
  if [ -f /var/run/syslogd.pid ]; then
    kill -HUP `cat /var/run/syslogd.pid` 2> /dev/null ||:
  fi
fi

%preun
if [ $1 = 0 ]; then
    service innd stop > /dev/null 2>&1
    /sbin/chkconfig --del innd
    if [ -f /var/lib/news/history.dir ]; then
       rm -f /var/lib/news/history.*
    fi
fi

%postun
if [ "$1" -ge 1 ]; then
    service innd condrestart > /dev/null 2>&1
fi

%postun libs -p /sbin/ldconfig

%files
%defattr(0755,news,news,-)
%{_bindir}/rnews
%defattr(0755,root,root,-)
# /etc config files plus cron config
%{_initrddir}/innd
%{_sysconfdir}/cron.hourly/inn-cron-rnews
%{_sysconfdir}/cron.hourly/inn-cron-nntpsend
%{_sysconfdir}/cron.daily/inn-cron-expire

%defattr(-,news,news,-)
# /etc/news config files
%dir %{_sysconfdir}/news
%config(noreplace) %{_sysconfdir}/news/passwd.nntp
%config(noreplace) %{_sysconfdir}/news/send-uucp.cf
%config(noreplace) %{_sysconfdir}/news/actsync.cfg
%config(noreplace) %{_sysconfdir}/news/motd.news
%config(noreplace) %{_sysconfdir}/news/expire.ctl
%config(noreplace) %{_sysconfdir}/news/actsync.ign
%config(noreplace) %{_sysconfdir}/news/innreport.conf
%config(noreplace) %{_sysconfdir}/news/distrib.pats
%config(noreplace) %{_sysconfdir}/news/buffindexed.conf
%config(noreplace) %{_sysconfdir}/news/innwatch.ctl
%config(noreplace) %{_sysconfdir}/news/nntpsend.ctl
%config(noreplace) %{_sysconfdir}/news/innfeed.conf
%config(noreplace) %{_sysconfdir}/news/nnrpd.track
%config(noreplace) %{_sysconfdir}/news/control.ctl.local
%config(noreplace) %{_sysconfdir}/news/storage.conf
%config(noreplace) %{_sysconfdir}/news/moderators
%config(noreplace) %{_sysconfdir}/news/news2mail.cf
%config(noreplace) %{_sysconfdir}/news/cycbuff.conf
%config(noreplace) %{_sysconfdir}/news/subscriptions
%config(noreplace) %{_sysconfdir}/news/control.ctl
%config(noreplace) %{_sysconfdir}/news/localgroups
%config(noreplace) %{_sysconfdir}/news/.profile
%config(noreplace) %{_sysconfdir}/news/nocem.ctl
%config(noreplace) %{_sysconfdir}/news/incoming.conf
%config(noreplace) %{_sysconfdir}/news/radius.conf
%config(noreplace) %{_sysconfdir}/news/ovdb.conf
%config(noreplace) %{_sysconfdir}/news/newsfeeds
%config(noreplace) %{_sysconfdir}/news/readers.conf
%config(noreplace) %{_sysconfdir}/news/distributions

%dir %{_sharedstatedir}/news
%config(noreplace) %{_sharedstatedir}/news/active.times
%config(noreplace) %{_sharedstatedir}/news/distributions
%config(noreplace) %{_sharedstatedir}/news/newsgroups
%config(noreplace) %{_sharedstatedir}/news/active
%config(noreplace) %{_sharedstatedir}/news/subscriptions
%config(noreplace) %{_sharedstatedir}/news/history

%defattr(0755,root,news,-)
%dir %{_libexecdir}/news
%{_libexecdir}/news/controlbatch
%attr(4510,root,news) %{_libexecdir}/news/innbind
%{_libexecdir}/news/docheckgroups
%{_libexecdir}/news/imapfeed
%{_libexecdir}/news/send-nntp
%{_libexecdir}/news/actmerge
%{_libexecdir}/news/ovdb_server
%{_libexecdir}/news/filechan
%{_libexecdir}/news/ninpaths
%{_libexecdir}/news/mod-active
%{_libexecdir}/news/news2mail
%{_libexecdir}/news/innconfval
%{_libexecdir}/news/shlock
%{_libexecdir}/news/nnrpd
%{_libexecdir}/news/controlchan
%{_libexecdir}/news/procbatch
%{_libexecdir}/news/expire
%{_libexecdir}/news/convdate
%{_libexecdir}/news/pullnews
%{_libexecdir}/news/archive
%{_libexecdir}/news/cnfsstat
%{_libexecdir}/news/grephistory
%{_libexecdir}/news/send-ihave
%{_libexecdir}/news/tinyleaf
%{_libexecdir}/news/cvtbatch
%{_libexecdir}/news/expirerm
%{_libexecdir}/news/rc.news
%attr(4550,uucp,news) %{_libexecdir}/news/rnews
%{_libexecdir}/news/innxmit
%{_libexecdir}/news/actsyncd
%{_libexecdir}/news/shrinkfile
%{_libexecdir}/news/makedbz
%{_libexecdir}/news/actsync
%{_libexecdir}/news/pgpverify
%{_libexecdir}/news/inndf
%{_libexecdir}/news/scanlogs
%{_libexecdir}/news/simpleftp
%{_libexecdir}/news/ovdb_init
%{_libexecdir}/news/ctlinnd
%{_libexecdir}/news/innstat
%{_libexecdir}/news/send-uucp
%{_libexecdir}/news/buffchan
%{_libexecdir}/news/perl-nocem
%{_libexecdir}/news/scanspool
%{_libexecdir}/news/expireover
%{_libexecdir}/news/batcher
%{_libexecdir}/news/fastrm
%{_libexecdir}/news/innmail
%{_libexecdir}/news/innxbatch
%{_libexecdir}/news/buffindexed_d
%{_libexecdir}/news/nntpget
%{_libexecdir}/news/cnfsheadconf
%{_libexecdir}/news/ovdb_stat
%{_libexecdir}/news/prunehistory
%{_libexecdir}/news/innreport
%attr(0644,root,news) %{_libexecdir}/news/innreport_inn.pm
%{_libexecdir}/news/getlist
%{_libexecdir}/news/innd
%{_libexecdir}/news/innupgrade
%{_libexecdir}/news/news.daily
%{_libexecdir}/news/sm
%{_libexecdir}/news/innwatch
%{_libexecdir}/news/inncheck
%{_libexecdir}/news/writelog
%{_libexecdir}/news/signcontrol
%{_libexecdir}/news/tdx-util
%{_libexecdir}/news/tally.control
%{_libexecdir}/news/overchan
%{_libexecdir}/news/sendinpaths
%{_libexecdir}/news/makehistory
%{_libexecdir}/news/nntpsend
%{_libexecdir}/news/mailpost
%{_libexecdir}/news/innfeed
%{_libexecdir}/news/ovdb_monitor
%{_libexecdir}/news/sendxbatches

%define filterdir %{_libexecdir}/news/filter
%dir %{filterdir}
%{filterdir}/filter_nnrpd.pl
%{filterdir}/nnrpd_access.pl
%{filterdir}/startup_innd.pl
%{filterdir}/nnrpd_auth.py*
%{filterdir}/nnrpd_access.py*
%{filterdir}/nnrpd_auth.pl
%{filterdir}/INN.py*
%{filterdir}/nnrpd.py*
%{filterdir}/filter_innd.py*
%{filterdir}/nnrpd_dynamic.py*

%define authdir %{_libexecdir}/news/auth
%define passwddir %{authdir}/passwd
%dir %{authdir}
%dir %{passwddir}
%{passwddir}/radius
%{passwddir}/ckpasswd

%define resolvdir %{authdir}/resolv
%dir %{resolvdir}
%{resolvdir}/domain
%{resolvdir}/ident

%define controldir %{_libexecdir}/news/control
%dir %{controldir}
%{controldir}/version.pl
%{controldir}/ihave.pl
%{controldir}/sendsys.pl
%{controldir}/sendme.pl
%{controldir}/checkgroups.pl
%{controldir}/senduuname.pl
%{controldir}/newgroup.pl
%{controldir}/rmgroup.pl

%define rnewsdir %{_libexecdir}/news/rnews.libexec
%dir %{rnewsdir}
%{rnewsdir}/encode
%{rnewsdir}/gunbatch
%{rnewsdir}/decode
%{rnewsdir}/bunbatch
%{rnewsdir}/c7unbatch

%{_libexecdir}/news/innshellvars.pl
%{_libexecdir}/news/innshellvars
%{_libexecdir}/news/innshellvars.tcl

%attr(0775,root,news) %dir %{_sharedstatedir}/news/http
%{_sharedstatedir}/news/http/innreport.css

%dir %{perl_vendorlib}/INN
%{perl_vendorlib}/INN/Config.pm

%defattr(-,news,news,-)
%dir /var/spool/news
%dir /var/spool/news/archive
%dir /var/spool/news/articles
%attr(0775,news,news) %dir /var/spool/news/incoming
%attr(0775,news,news) %dir /var/spool/news/incoming/bad
%dir /var/spool/news/innfeed
%dir /var/spool/news/outgoing
%dir /var/spool/news/overview
%dir /var/log/news/OLD
%dir %{_sharedstatedir}/news/tmp
%ghost %dir /var/run/news
%defattr(-,root,root,-)
%{_mandir}/man1/c*.1.gz
%{_mandir}/man1/f*.1.gz
%{_mandir}/man1/g*.1.gz
%{_mandir}/man1/inn*.1.gz
%{_mandir}/man1/n*.1.gz
%{_mandir}/man1/p*.1.gz
%{_mandir}/man1/r*.1.gz
%{_mandir}/man1/s*.1.gz
%{_mandir}/man[58]/*
%defattr(-,root,root,0755)
%doc NEWS README* HACKING ChangeLog CONTRIBUTORS LICENSE INSTALL FAQ.html 
%doc doc/config-design doc/history-innfeed doc/GPL doc/sample-control
%doc doc/config-semantics doc/external-auth TODO doc/hook-python doc/config-syntax
%doc doc/hook-perl doc/history
%doc %dir samples

%files libs
%defattr(-,root,root,-)
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/inn/
%{_includedir}/inn/*
%{_libdir}/lib*.so
%{_mandir}/man3/*

%files -n inews
%defattr(-,root,root,-)
%config(noreplace) %attr(-,news,news) %{_sysconfdir}/news/inn.conf
%{_bindir}/inews
%attr(0755,root,root) %{_libexecdir}/news/inews
%{_mandir}/man1/inews*

%changelog
* Wed Aug 11 2010 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.2-4
- Rebuild for python-2.7 (#623322)
- Fix SMP issue in frontends

* Wed Jul 14 2010 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.2-3
- /var/run/news ghosted tmpfs

* Tue Jul  6 2010 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.2-2
- Try to fix a smp issue on innfeed/Makefile

* Mon Jun 28 2010 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.2-1
- New upstream release

* Wed Jun 2 2010 Nikola Pajkovsky <npajkovs@redhat.com> - 2.5.1-5
- Resolves: #597799 - Two typos in /etc/init.d/inn, three typos in /etc/cron.*/inn* in F13
- Resolves: #596580 - Migration from /usr/lib/news/bin to /usr/libexec/news is not complete
- Resolves: #604473 - wrong permissions on /usr/share/doc/inn-2.5.1(Jochen@herr-schmitt.de)
- add patch inn-2.5.1-config-path.patch
- add BuildRequires: flex (Jochen@herr-schmitt.de)

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.5.1-4
- Mass rebuild with perl-5.12.0

* Wed Dec 16 2009 Nikola Pajkovsky <npajkovs@redhta.com> - 2.5.1-3
- rebuild 
- chage licence and remove on rm -f
- drop patches inn-2.4.1.perl.patch and inn-2.4.5-dynlib.patch

* Fri Dec 11 2009 Nikola Pajkovsky <npajkovs@redhat.com> - 2.5.1-2
- #225901 - Merge Review: inn

* Tue Oct 13 2009 Jochen Schmitt <Jochen herr-schmitt de> - 2.5.1-1
- New upstream release

* Mon Sep 14 2009 Nikola Pajkovsky <npajkovs@redhat.com> - 2.5.0-5
- resolved: 511772 - inn/storage.h not self-contained, missing inn/options.h

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Nikola Pajkovsky <npajkovs@redhat.com> 2.5.0-3
- ugly sed script for file section was deleted and rewrite in classic style
- fix init script(does not start correctly and shutdown when pid does not exist when service run)

* Wed Jun 24 2009 Ondrej Vasik <ovasik@redhat.com> - 2.5.0-2
- add support for load average to makehistory(#276061)
- update faq, ship it in %%doc
- fix typo in filelist

* Tue Jun 09 2009 Ondrej Vasik <ovasik@redhat.com> - 2.5.0-1
- new upstream release 2.5.0
- remove applied and adjust modified patches

* Tue May 19 2009 Ondrej Vasik <ovasik@redhat.com> - 2.4.6-2
- reflect change in sasl_encode64 abi(null terminator) - #501452

* Wed Mar 11 2009 Ondrej Vasik <ovasik@redhat.com> - 2.4.6-1
- new bugfix upstream release 2.4.6
- no strict aliasing, remove pyo/.pyc filters files from list

* Wed Feb 25 2009 Ondrej Vasik <ovasik@redhat.com> - 2.4.5-10
- mark /usr/lib/news/lib/innshellvars* as noreplace,
  versioned provide for perl(::/usr/lib/innshellvars.pl)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Ondrej Vasik <ovasik@redhat.com> - 2.4.5-8
- create user/group news with reserved uidgid numbers

* Wed Jan 13 2009 Ondrej Vasik <ovasik@redhat.com> - 2.4.5-7
- fix upstream url

* Mon Dec  1 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.4.5-6
- Rebuild for Python 2.6

* Mon Dec 01 2008 Ondrej Vasik <ovasik@redhat.com> - 2.4.5-5
- do own /usr/include/inn in devel package (#473922)

* Tue Nov 25 2008 Ondrej Vasik <ovasik@redhat.com> - 2.4.5-4
- package summary tuning

* Fri Aug 29 2008 Ondrej Vasik <ovasik@redhat.com> - 2.4.5-3
- patch fuzz clean up

* Fri Jul  7 2008 Ondrej Vasik <ovasik@redhat.com> - 2.4.5-2
- do not use static libraries(changes by Jochen Schmitt,#453993)
- own all dirs spawned by inn package(#448088)

* Thu Jul  3 2008 Ondrej Vasik <ovasik@redhat.com> - 2.4.5-1
- new upstream release 2.4.5

* Tue Jun 17 2008 Ondrej Vasik <ovasik@redhat.com> - 2.4.4-3
- Add news user. fixes bug #437462
* Mon May 19 2008 Ondrej Vasik <ovasik@redhat.com> - 2.4.4-2
- add sparc arches to the list for -fPIC(Dennis Gilmore)

* Thu May 15 2008 Ondrej Vasik <ovasik@redhat.com> - 2.4.4-1
- new upstream release 2.4.4

* Thu Apr 24 2008 Ondrej Vasik <ovasik@redhat.com> - 2.4.3-14
- make /var/spool/news/incoming writable for news group
  (#426760)
- changes because of /sbin/nologin shell for news user

* Wed Apr  9 2008 Ondrej Vasik <ovasik@redhat.com> - 2.4.3-13
- few documentation changes because of /sbin/nologin shell 
  for news user (su - news -c <commmand> will not work in 
  that case ) #233738

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.4.3-12
- BuildRequires: perl(ExtUtils::Embed)

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.4.3-11
- add Requires for versioned perl (libperl.so)

* Mon Feb 11 2008 Ondrej Vasik <ovasik@redhat.com> 2.4.3-10
- again added trigger for sysklogd
- rebuild for gcc43

* Wed Jan 16 2008 Ondrej Vasik <ovasik@redhat.com> 2.4.3-9
- do not show annoying fatal log message when nonfatal error 
  eaddrinuse occured in rcreader
- use /etc/rsyslog.conf instead of /etc/syslog.conf

* Mon Jan 07 2008 Ondrej Vasik <ovasik@redhat.com> 2.4.3-8
- initscript changes - review changes caused errors while
  in stop() phase - not known variable NEWSBIN(#401241)
- added url, fixed License tag

* Tue Oct 02 2007 Ondrej Dvoracek <odvorace@redhat.com> 2.4.3-7
- initscript review (#246951)
- added buildrequires for perl-devel and python

* Tue Aug 29 2006 Martin Stransky <stransky@redhat.com> 2.4.3-6
- added dist tag
- added patch from #204371 - innd.init script should use 
  ctlinnd to stop the server

* Mon Jul 17 2006 Jesse Keating <jkeating@redhat.com> - 2.4.3-5
- rebuild

* Wed Jun 21 2006 Martin Stransky <stransky@redhat.com> 2.4.3-4
- enabled ipv6 support

* Wed Jun 07 2006 Karsten Hopp <karsten@redhat.de> 2.4.3-3
- add some buildrequirements (krb5-devel pam-devel e2fsprogs-devel)

* Sun May 28 2006 Martin Stransky <stransky@redhat.com> 2.4.3-2
- file conflicts for inn (#192689)
- added byacc to dependencies (#193402)

* Mon Mar 27 2006 Martin Stransky <stransky@redhat.com> 2.4.3-1
- new upstream

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.4.2-4.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.4.2-4.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Aug 02 2005 Karsten Hopp <karsten@redhat.de> 2.4.2-4
- rebuild with current rpm
- include .pyc and pyo files created by /usr/lib/rpm/brp-python-bytecompile

* Thu Apr  7 2005 Martin Stransky <stransky@redhat.com> 2.4.2-3
- add support for large files

* Mon Mar  7 2005 Martin Stransky <stransky@redhat.com>
- rebuilt

* Tue Jan 11 2005 Martin Stransky <stransky@redhat.com> 2.4.2-1
- fix file conflict between inews and inn packages (#51607)
- update to 2.4.2
- thanks to Jochen Schmitt <Jochen@herr-schmitt.de>

* Thu Dec 23 2004 Martin Stransky <stransky@redhat.com> 2.4.1-2
- fix array overflow / uninitialized pointer (#143592)

* Wed Dec 15 2004 Martin Stransky <stransky@redhat.com> 2.4.1-1
- diff patch (fix obsolete version of diff parameter) #137342
- posix/warnings patch #110825

* Mon Dec 13 2004 Martin Stransky <stransky@redhat.com> 2.4.1-1
- update to INN 2.4.1
- Thanks to Jochen Schmitt <Jochen@herr-schmitt.de>

* Tue Oct  5 2004 Thomas Woerner <twoerner@redhat.com> 2.3.5-11.1
- using runuser instead of su in cronjobs

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 17 2004 Thomas Woerner <twoerner@redhat.com> 2.3.5-10
- compiling server and suid programs PIE

* Tue Apr  6 2004 Thomas Woerner <twoerner@redhat.com> 2.3.5-9
- /etc/rc.d/init.d/innd is owned by root now (#119131)

* Mon Feb 23 2004 Tim Waugh <twaugh@redhat.com>
- Use ':' instead of '.' as separator for chown.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 29 2004 Thomas Woerner <twoerner@redhat.com> 2.3.5-7
- using db-4.2

* Mon Jul 14 2003 Chip Turner <cturner@redhat.com>
- rebuild for new perl 5.8.1

* Thu Jul 03 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- recompile for other thingy

* Wed Jun 11 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- link against db-4.1  #92420
- use correct optims settings from rpm  #92410
- install with other perms to allow debuginfo stripping #92412

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Apr 30 2003 Ellito Lee <sopwith@redhat.com> 2.3.5-2
- headusage patch for ppc64 etc.

* Sun Mar 30 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- 2.3.5 update

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Jan 17 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to current bug-fix release

* Fri Jan 03 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- do not require cleanfeed  #80124

* Tue Dec 17 2002 Phil Knirsch <pknirsch@redhat.com> 2.3.3-9
- Fixed changelog entries containing percent sections.

* Tue Dec 03 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- do not link against -lelf

* Thu Nov  7 2002 Tim Powers <timp@redhat.com>
- rebuilt to fix unsatisfied dependencies
- pass _target_platform when configuring

* Tue Jul 23 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- fix cron scripts to use correct paths #69189
- add compat symlinks for rnews/inews into /usr/bin

* Thu Jul 18 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- make check if networking is up more robust in initscript
- move most apps into /usr/lib/news/bin for less namespace pollution

* Tue Jun 18 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add some cvs patches
- crude hack to change LOCK_READ and LOCK_WRITE within INN source code

* Mon May 27 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to inn-2.3.3
- use db4

* Mon Apr 15 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- put /etc/news/inn.conf into the inews subpackage to make a smaller
  client side possible and require inews from the main inn rpm

* Mon Apr 08 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- startup and cron scripts unset LANG and LC_COLLATE to make
  inn more robust   (#60770)
- really link against db3
- inews requires inn #59852

* Thu Feb 28 2002 Elliot Lee <sopwith@redhat.com> 2.3.2-10
- Change db4-devel requirement to db3-devel.
- Use _smp_mflags

* Thu Jan 31 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- fix #59123

* Wed Jan 30 2002 Jeff Johnson <jbj@redhat.com>
- white out bogus perl requirement for now.
- don't include <db1/ndbm.h> to avoid linking with -ldb1.

* Sat Jan 26 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- change to db4

* Sun Jan 20 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- allow rebuilding by not using newer autoconf, adjust inn patches

* Tue Jul 24 2001 Tim Powers <timp@redhat.com>
- make inews owned by root, not the build system

* Tue Jul 24 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- fix badd attr() macro

* Sat Jul 21 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add build req

* Fri Jul 06 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- change perms on inews

* Tue Jun 19 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.3.2

* Wed Feb 14 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add startup script patch by kevin@labsysgrp.com #27421
- inews subpackage does not depend on inn anymore #24439
- fix reload and make some cleanups to the startup script #18076

* Wed Feb 07 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add a "exit 0" to the postun script

* Wed Jan 24 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.3.1
- do not use --enable-tagged-hash
- move tmp dir to /var/lib/news/tmp
- add more docu
- do not call "strip" directly
- remove some of the default files as the ones in INN are ok
- do not req /etc/init.d
- do not attempt an automatic update from previous versions as
  we have to deal with different storage methods
- prepare startup script for translations
- add minimal check into startup for a history file

* Mon Jan 22 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- innreport had wrong perms
- files for the cron-jobs must be owned by root:root

* Tue Aug 29 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- remove cleanfeed sources

* Mon Jul 24 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- fix some perms

* Mon Jul 24 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.2.3
- fixed many perms
- cleaned up complete build process

* Sat Jul 15 2000 Bill Nottingham <notting@redhat.com>
- move initscript back

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jul 10 2000 Bill Nottingham <notting@redhat.com>
- add fix for the verifycancels problem fron Russ Allbery
- turn them off anyways
- fix perms on inews

* Sat Jul  8 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- prereq init.d

* Tue Jun 27 2000 Than Ngo <than@redhat.de>
- /etc/rc.d/init.d -> /etc/init.d
- fix initscript

* Sun Jun 25 2000 Matt Wilson <msw@redhat.com>
- defattr root

* Wed Jun 21 2000 Preston Brown <pbrown@redhat.com>
- fix up some issues with our new gcc compiler (patch 6)
- don't do chown in the install script so we can build as nonroot

* Mon Jun 19 2000 Preston Brown <pbrown@redhat.com>
- FHS mandir

* Tue May 23 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- add inn-2.2.2-rnews.patch which is also accepted in current cvs

* Mon May 22 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- fix stupid bug in rnews cronjob
- enable controlchan in default newsfeeds config
- run "rnews -U" hourly instead of daily

* Fri May 19 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- add bug-fix to batcher from cvs version
- "su news" before starting rnews from cron

* Mon Apr  3 2000 Bill Notttingham <notting@redhat.com>
- arrgh, there is no /usr/lib/news anymore. (#10536)
- pppatch ppport for ppproper ppperl

* Thu Mar 02 2000 Cristian Gafton <gafton@redhat.com>
- remove useless filter_innd.pl so that we will get the cleanfeed one
  instead

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages
- other minor fixes

* Tue Dec 14 1999 Bill Nottingham <notting@redhat.com>
- update to 2.2.2

* Sun Aug 29 1999 Cristian Gafton <gafton@redhat.com>
- version 2.2.1 to fix security problems in previous inn versions
- add the faq back to the source rpm

* Mon Aug 16 1999 Bill Nottingham <notting@redhat.com>
- initscript munging

* Tue Jun 22 1999 Jeff Johnson <jbj@redhat.com>
- fix syntax error in reload (#3636).

* Fri Jun 18 1999 Bill Nottingham <notting@redhat.com>
- don't run by default

* Sun Jun 13 1999 Jeff Johnson <jbj@redhat.com>
- mark /var/lib/news/* as config(noreplace) (#3425)

* Thu Jun 10 1999 Dale Lovelace <dale@redhat.com>
- change su news to su - news (#3331)

* Wed Jun  2 1999 Jeff Johsnon <jbj@redhat.com>
- complete trn->inews->inn dependency (#2646)
- use f_bsize rather than f_frsize when computing blocks avail (#3154).
- increase client timeout to 30 mins (=1800) (#2833).
- add missing includes to inn-devel (#2904).

* Mon May 31 1999 Jeff Johnson <jbj@redhat.com>
- fix owner and permissions on /var/lib/news/.news.daily (#2354).

* Tue Mar 30 1999 Preston Brown <pbrown@redhat.com>
- fixed paths in cron jobs, check to see that innd is enabled

* Fri Mar 26 1999 Preston Brown <pbrown@redhat.com>
- path to makehistory corrected.

* Mon Mar 22 1999 Preston Brown <pbrown@redhat.com>
- fixed permissions on rnews for uucp

* Fri Mar 19 1999 Preston Brown <pbrown@redhat.com>
- make sure init scripts get packaged up, fix other minor bugs
- major fixups to innd.conf for denial of service attacks, sanity, etc.
- make sure history gets rebuilt in an upgrade (added to post section)
- many thanks go out to mmchen@minn.net for these suggestions.

* Fri Feb 19 1999 Cristian Gafton <gafton@redhat.com>
- prereq all the stuff we need in the postinstall scripts

* Sat Feb  6 1999 Bill Nottingham <notting@redhat.com>
- strip -x bits from docs/samples (bogus dependencies)

* Thu Sep 03 1998 Cristian Gafton <gafton@redhat.com>
- updated to version 2.1

* Fri Aug 21 1998 Jeff Johnson <jbj@redhat.com>
- innd.init chkconfig entry was incorrect (problem #855)

* Tue Jun 30 1998 Jeff Johnson <jbj@redhat.com>
- susbsys name must be identical to script name (problem #700)

* Mon Jun 29 1998 Bryan C. Andregg <bandregg@redhat.com>
- fixed startinnfeed paths

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sat May 02 1998 Cristian Gafton <gafton@redhat.com>
- enhanced initscript

* Fri May 01 1998 Cristian Gafton <gafton@redhat.com>
- fixed innfeed patched to be perl-version independent

* Wed Apr 15 1998 Bryan C. Andregg <bandregg@redhat.com>
- fixed sfnet.* entries in control.ctl

* Mon Apr 13 1998 Bryan C. Andregg <bandregg@redhat.com>
- moved cleanfeed to its own package

* Thu Apr 09 1998 Bryan C. Andregg <bandregg@redhat.com>
- added insync patches
- added cleanfeed
- added innfeed

* Thu Apr 09 1998 Cristian Gafton <gafton@redhat.com>
- abuse buildroot to simplify the file list
- built against Manhattan

* Tue Mar 24 1998 Bryan C. Andregg <bandregg@redhat.com>
- updated to inn 1.7.2
- Added REMEMBER_TRASH and Poison patch

* Sun Oct 19 1997 Erik Troan <ewt@redhat.com>
- updated to inn 1.7
- added chkconfig support to the initscripts
- orginally released as release 2, leving release 1 if a 4.2.x upgrade
  is ever necessary 
- don't start it in any runlevel (by default)
- added inndcomm.h

* Thu Oct 09 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Tue Aug 05 1997 Elliot Lee <sopwith@redhat.com>
- Applied the 1.5.1sec and 1.5.1sec2 patches
- Applied 3 more unoff patches.
- Removed insanity in /etc/cron.hourly/inn-cron-nntpsend, it now
  just runs nntpsend as news.

* Wed Apr 02 1997 Erik Troan <ewt@redhat.com>
- Patch from CERT for sh exploit.
- Changed /usr/ucb/compress reference to /usr/bin/compress

* Mon Mar 17 1997 Erik Troan <ewt@redhat.com>
- Removed inews.1 from main inn package (it's still in the inews packaeg)
- Fixed references to /usr/spoo in sendbatch
- added "-s -" to crosspost line in newsfeeds
- /var/lib/news/active.time is now created as news.news
- /etc/news/nnrp.access and /etc/news/nntpsend.ctl are mode 0440 
- included a better rc script which does a better job of shutting down news
- updated /etc/rc.d/rc.news output look like the rest of our initscripts
- hacked sendbatch df stuff to work on machines w/o a separate /var/spool/news

* Tue Mar 11 1997 Erik Troan <ewt@redhat.com>
- added chmod to make sure rnews is 755
- /etc/news/nnrp.access and /etc/news/nntpsend.ctl are news.news not root.news
  or root.root
- install an empty /var/lib/news/.news.daily as a config file
- added dbz/dbz.h as /usr/include/dbz.h
- added /usr/bin/inews link to /usr/lib/news/inews
- changed INEWS_PATH to DONT -- I'm not sure this is right though
- turned off MMAP_SYNC
- added a ton of man pages which were missing from the filelist
- increased CLIENT_TIMEOUT to (30 * 60)
- added a postinstall to create /var/lib/news/active.times if it doesn't
  already exist
- patched rc.news to start inn w/ -L flag
- pulled news.init into a separate source file rather then creating it through
  a patch
- added /etc/rc.d/rc5.d/S95news to the file list
- remove pid files from /var/lock/news/* on shutdown
- use /var/lock/subsys/news rather then /var/lock/subsys/inn or things
  don't shutdown properly

* Mon Mar 10 1997 Christian 'Dr. Disk' Hechelmann <drdisk@ds9.au.s.shuttle.de>
- changed devel package description to include tin.
- the devel package missed libinn.h
- moved libinn.3 man-page to the devel package
- moved changelog up
- in post some echo statements were messed up. if we put the redirection
  staements in a different line than the echo command we really should use
  a backslash to thell the shell :-)
- in install a chmod line referenced the same directory twice.
- changed inn-1.5.1-redhat.patch: The patch for news.daily had a side effect.
  as EXPIREOVERFLAGS was set to '-a', expireover would break if there were
  articles to be removed, as '-a' can't be used if '-z' is specified...
  Now there is a separate 'eval expireover -a' after the first eval. Dirty
  but works.

* Wed Feb 26 1997 Erik Troan <ewt@redhat.com>
- Added a /usr/bin/rnews symlink to /usr/lib/news/rnews as other programs like
  to use it.

* Tue Feb 25 1997 Elliot Lee <sopwith@cuc.edu>
- Fixed rnews path in /etc/cron.daily/inn-cron-rnews
- Added overview! and crosspost lines to /etc/news/newsfeeds
- Fixed nntpsend.ctl path in /usr/lib/news/bin/nntpsend, and set a saner
  nntpsend.ctl config file.
- Added automated inn.conf 'server: ' line creation in post
- Added misc. patches from ftp.isc.org/isc/inn/unoff-patches/1.5
- Removed -lelf from config.data LIBS
- Made RPM_OPT_FLAGS work.
- Bug in rpm meant that putting post after files made it not run. Moved
  post up.
- Added /etc/cron.hourly/inn-cron-nntpsend to send news every hour.
- Fixed most of the misc permissions/ownership stuff that inncheck
  complained about.

* Wed Feb 19 1997 Erik Troan <ewt@redhat.com>
- Incorporated changes from <drdisk@tilx01.ti.fht-esslingen.de> which fixed
  some paths and restored the cron jobs which disappeared in the 1.5.1
  switch. He also made the whole thing use a buildroot and added some files
  which were missing from the file list.

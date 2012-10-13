# SA-Exim has long since been obsoleted by the proper built-in ACL support
# from exiscan. Disable it for FC6 unless people scream.
%define fedora 13
%if 0%{?fedora} < 6
%define buildsa 1
%endif

# Build clamav subpackage for FC5 and above.
%if 0%{?fedora} >= 5
%define buildclam 1
%endif

Summary: The exim mail transfer agent
Name: exim
Version: 4.77
Release: 3%{?dist}
License: GPLv2+
Url: http://www.exim.org/
Group: System Environment/Daemons
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Provides: MTA smtpd smtpdaemon server(smtp)
Requires(post): /sbin/chkconfig /sbin/service %{_sbindir}/alternatives
Requires(preun): /sbin/chkconfig /sbin/service %{_sbindir}/alternatives
Requires(pre): %{_sbindir}/groupadd, %{_sbindir}/useradd
%if 0%{?buildclam}
BuildRequires: clamav-devel
%endif
Source: ftp://ftp.exim.org/pub/exim/exim4/exim-%{version}.tar.bz2
Source2: exim.init
Source3: exim.sysconfig
Source4: exim.logrotate
Source5: exim-tidydb.sh
Source11: exim.pam
%if 0%{?buildsa}
Source13: http://marc.merlins.org/linux/exim/files/sa-exim-4.2.tar.gz
%endif
Source20: exim-greylist.conf.inc
Source21: mk-greylist-db.sql
Source22: greylist-tidy.sh
Source23: trusted-configs

Patch4: exim-rhl.patch
Patch6: exim-4.73-config.patch
Patch8: exim-4.24-libdir.patch
Patch12: exim-4.33-cyrus.patch
Patch13: exim-4.43-pamconfig.patch
Patch14: exim-4.50-spamdconf.patch
Patch18: exim-4.71-dlopen-localscan.patch
Patch19: exim-4.63-procmail.patch
Patch20: exim-4.63-allow-filter.patch
Patch21: exim-4.63-localhost-is-local.patch
Patch22: exim-4.66-greylist-conf.patch
Patch23: exim-4.67-smarthost-config.patch
Patch25: exim-4.69-dynlookup-config.patch
Patch26: exim-4.69-strictaliasing.patch

Requires: /etc/pki/tls/certs /etc/pki/tls/private
Requires: /etc/aliases
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires: db4-devel openssl-devel openldap-devel pam-devel
%if 0%{?buildsa}
BuildRequires: lynx
%endif
BuildRequires: pcre-devel sqlite-devel tcp_wrappers-devel cyrus-sasl-devel
BuildRequires: openldap-devel openssl-devel mysql-devel postgresql-devel
BuildRequires: libXaw-devel libXmu-devel libXext-devel libX11-devel libSM-devel
BuildRequires: libICE-devel libXpm-devel libXt-devel perl(ExtUtils::Embed)
BuildRequires: libspf2-devel
Requires: libspf2

%description 
Exim is a message transfer agent (MTA) developed at the University of
Cambridge for use on Unix systems connected to the Internet. It is
freely available under the terms of the GNU General Public Licence. In
style it is similar to Smail 3, but its facilities are more
general. There is a great deal of flexibility in the way mail can be
routed, and there are extensive facilities for checking incoming
mail. Exim can be installed in place of sendmail, although the
configuration of exim is quite different to that of sendmail.

%package mysql
Summary: MySQL lookup support for Exim
Group: System Environment/Daemons
Requires: exim = %{version}-%{release}

%description mysql
This package contains the MySQL lookup module for Exim

%package pgsql
Summary: PostgreSQL lookup support for Exim
Group: System Environment/Daemons
Requires: exim = %{version}-%{release}

%description pgsql
This package contains the PostgreSQL lookup module for Exim

%package mon
Summary: X11 monitor application for Exim
Group: Applications/System

%description mon
The Exim Monitor is an optional supplement to the Exim package. It
displays information about Exim's processing in an X window, and an
administrator can perform a number of control actions from the window
interface.

%package sa
Summary: Exim SpamAssassin at SMTP time - d/l plugin
Group: System Environment/Daemons
Requires: exim = %{version}-%{release}

%description sa
The exim-sa package is an old method for allowing SpamAssassin to be run on
incoming mail at SMTP time. It is deprecated in favour of the built-in ACL
support for content scanning.

%package clamav
Summary: Clam Antivirus scanner dæmon configuration for use with Exim
Group: System Environment/Daemons
Requires: clamav-server exim
Obsoletes: clamav-exim <= 0.86.2
Requires(post): /sbin/chkconfig /sbin/service
Requires(preun): /sbin/chkconfig /sbin/service

%description clamav
This package contains configuration files which invoke a copy of the
clamav dæmon for use with Exim. It can be activated by adding (or
uncommenting)

   av_scanner = clamd:%{_var}/run/clamd.exim/clamd.sock

in your exim.conf, and using the 'malware' condition in the DATA ACL,
as follows:

   deny message = This message contains malware ($malware_name)
      malware = *

For further details of Exim content scanning, see chapter 41 of the Exim
specification:
http://www.exim.org/exim-html-%{version}/doc/html/spec_html/ch41.html

%package greylist
Summary: Example configuration for greylisting using Exim
Group: System Environment/Daemons
Requires: sqlite exim %{_sysconfdir}/cron.daily

%description greylist
This package contains a simple example of how to do greylisting in Exim's
ACL configuration. It contains a cron job to remove old entries from the
greylisting database, and an ACL subroutine which needs to be included
from the main exim.conf file.

To enable greylisting, install this package and then uncomment the lines
in Exim's configuration /etc/exim.conf which enable it. You need to
uncomment at least two lines -- the '.include' directive which includes
the new ACL subroutine, and the line which invokes the new subroutine.

By default, this implementation only greylists mails which appears
'suspicious' in some way. During normal processing of the ACLs we collect
a list of 'offended' which it's committed, which may include having
SpamAssassin points, lacking a Message-ID: header, coming from a blacklisted
host, etc. There are examples of these in the default configuration file,
mostly commented out. These should be sufficient for you to you trigger
greylisting for whatever 'offences' you can dream of, or even to make 
greylisting unconditional.

%prep
%setup -q
%if 0%{?buildsa}
%setup -q -T -D -a 13
%endif

%patch4 -p1 -b .rhl
%patch6 -p1 -b .config
%patch8 -p1 -b .libdir
%patch12 -p1 -b .cyrus
%patch13 -p1 -b .pam
%patch14 -p1 -b .spamd
%patch18 -p1 -b .dl
%patch19 -p1 -b .procmail
%patch20 -p1 -b .filter
%patch21 -p1 -b .localhost
%patch22 -p1 -b .grey
%patch23 -p1 -b .smarthost
%patch25 -p1 -b .dynconfig
#patch26 -p1 -b .strictaliasing

cp src/EDITME Local/Makefile
sed -i 's@^# LOOKUP_MODULE_DIR=.*@LOOKUP_MODULE_DIR=%{_libdir}/exim/%{version}-%{release}/lookups@' Local/Makefile
sed -i 's@^# AUTH_LIBS=-lsasl2@AUTH_LIBS=-lsasl2@' Local/Makefile
sed -i 's@^# EXPERIMENTAL_SPF=.*@EXPERIMENTAL_SPF=yes@' Local/Makefile
sed -i 's@^# LDFLAGS += -lspf2.*@LDFLAGS += -lspf2@' Local/Makefile
cp exim_monitor/EDITME Local/eximon.conf


%build
%ifnarch s390 s390x sparc sparcv9 sparcv9v sparc64 sparc64v
	export PIE=-fpie
%else
	export PIE=-fPIE
%endif
make LFLAGS=-pie _lib=%{_lib} FULLECHO=

%if 0%{?buildsa}
# build sa-exim
cd sa-exim*
perl -pi -e 's|\@lynx|HOME=/ /usr/bin/lynx|g;' Makefile
make SACONF=%{_sysconfdir}/exim/sa-exim.conf CFLAGS="$RPM_OPT_FLAGS -fPIC"
%endif

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pam.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/exim

cd build-`scripts/os-type`-`scripts/arch-type`
install -m 4775 exim $RPM_BUILD_ROOT%{_sbindir}

for i in eximon eximon.bin exim_dumpdb exim_fixdb exim_tidydb \
	exinext exiwhat exim_dbmbuild exicyclog exim_lock \
	exigrep eximstats exipick exiqgrep exiqsumm \
	exim_checkaccess convert4r4
do
	install -m 0755 $i $RPM_BUILD_ROOT%{_sbindir}
done

mkdir -p $RPM_BUILD_ROOT%{_libdir}/exim/%{version}-%{release}/lookups
for i in mysql.so pgsql.so
do 
	install -m755 lookups/$i \
	 $RPM_BUILD_ROOT%{_libdir}/exim/%{version}-%{release}/lookups
done

cd ..

install -m 0644 src/configure.default $RPM_BUILD_ROOT%{_sysconfdir}/exim/exim.conf
install -m 0644 %SOURCE11 $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/exim

mkdir -p $RPM_BUILD_ROOT/usr/lib
pushd $RPM_BUILD_ROOT/usr/lib
ln -sf ../sbin/exim sendmail.exim
popd

pushd $RPM_BUILD_ROOT%{_sbindir}/
ln -sf exim sendmail.exim
popd

pushd $RPM_BUILD_ROOT%{_bindir}/
ln -sf ../sbin/exim mailq.exim
ln -sf ../sbin/exim runq.exim
ln -sf ../sbin/exim rsmtp.exim
ln -sf ../sbin/exim rmail.exim
ln -sf ../sbin/exim newaliases.exim
popd

install -d -m 0750 $RPM_BUILD_ROOT%{_var}/spool/exim
install -d -m 0750 $RPM_BUILD_ROOT%{_var}/spool/exim/db
install -d -m 0750 $RPM_BUILD_ROOT%{_var}/spool/exim/input
install -d -m 0750 $RPM_BUILD_ROOT%{_var}/spool/exim/msglog
install -d -m 0750 $RPM_BUILD_ROOT%{_var}/log/exim

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8
install -m644 doc/exim.8 $RPM_BUILD_ROOT%{_mandir}/man8/exim.8
pod2man --center=EXIM --section=8 \
	$RPM_BUILD_ROOT/usr/sbin/eximstats \
	$RPM_BUILD_ROOT%{_mandir}/man8/eximstats.8

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 644 %SOURCE3 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/exim

mkdir -p $RPM_BUILD_ROOT%{_initrddir}
install %SOURCE2 $RPM_BUILD_ROOT%{_initrddir}/exim

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 0644 %SOURCE4 $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/exim

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily
install -m 0755 %SOURCE5 $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/exim-tidydb

%if 0%{?buildsa}
# install sa
cd sa-exim*
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/exim
install *.so  $RPM_BUILD_ROOT%{_libexecdir}/exim
install -m 644 *.conf $RPM_BUILD_ROOT%{_sysconfdir}/exim
ln -s sa-exim*.so $RPM_BUILD_ROOT%{_libexecdir}/exim/sa-exim.so
%endif

# generate ghost .pem file
mkdir -p $RPM_BUILD_ROOT/etc/pki/tls/{certs,private}
touch $RPM_BUILD_ROOT/etc/pki/tls/{certs,private}/exim.pem
chmod 600 $RPM_BUILD_ROOT/etc/pki/tls/{certs,private}/exim.pem

# generate alternatives ghosts
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
for i in %{_sbindir}/sendmail %{_bindir}/{mailq,runq,rsmtp,rmail,newaliases} \
	/usr/lib/sendmail %{_sysconfdir}/pam.d/smtp %{_mandir}/man1/mailq.1.gz
do
	touch $RPM_BUILD_ROOT$i
done

%if 0%{?buildclam}
# Munge the clamav init and config files from clamav-devel. This really ought
# to be a subpackage of clamav, but this hack will have to do for now.
function clamsubst() {
	 sed -e "s!<SERVICE>!$3!g;s!<USER>!$4!g;""$5" %{_datadir}/clamav/template/"$1" >"$RPM_BUILD_ROOT$2"
}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/clamd.d
clamsubst clamd.conf %{_sysconfdir}/clamd.d/exim.conf exim exim \
       's!^##*\(\(LogFile\|LocalSocket\|PidFile\|User\)\s\|\(StreamSaveToDisk\|ScanMail\|LogTime\|ScanArchive\)$\)!\1!;s!^Example!#Example!;'

clamsubst clamd.init %{_initrddir}/clamd.exim exim exim ''
clamsubst clamd.logrotate %{_sysconfdir}/logrotate.d/clamd.exim exim exim ''
cat <<EOF > $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/clamd.exim
CLAMD_CONFIG='%_sysconfdir/clamd.d/exim.conf'
CLAMD_SOCKET=%{_var}/run/clamd.exim/clamd.sock
EOF
ln -sf clamd $RPM_BUILD_ROOT/usr/sbin/clamd.exim

mkdir -p $RPM_BUILD_ROOT%{_var}/run/clamd.exim
mkdir -p $RPM_BUILD_ROOT%{_var}/log
touch $RPM_BUILD_ROOT%{_var}/log/clamd.exim

%endif

# Set up the greylist subpackage
install -m644 %{SOURCE20} $RPM_BUILD_ROOT/%_sysconfdir/exim/exim-greylist.conf.inc
install -m644 %{SOURCE21} $RPM_BUILD_ROOT/%_sysconfdir/exim/mk-greylist-db.sql
mkdir -p $RPM_BUILD_ROOT/%_sysconfdir/cron.daily
install -m755 %{SOURCE22} $RPM_BUILD_ROOT/%_sysconfdir/cron.daily/greylist-tidy.sh
install -m644 %{SOURCE23} $RPM_BUILD_ROOT/%_sysconfdir/exim/trusted-configs
touch $RPM_BUILD_ROOT/%_var/spool/exim/db/greylist.db

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%{_sbindir}/groupadd -g 93 exim 2>/dev/null
%{_sbindir}/useradd -d %{_var}/spool/exim -s /sbin/nologin -G mail -M -r -u 93 -g exim exim 2>/dev/null
# Copy TLS certs from old location to new -- don't move them, because the
# config file may be modified and may be pointing to the old location.
if [ ! -f /etc/pki/tls/certs/exim.pem -a -f %{_datadir}/ssl/certs/exim.pem ] ; then
   cp %{_datadir}/ssl/certs/exim.pem /etc/pki/tls/certs/exim.pem
   cp %{_datadir}/ssl/private/exim.pem /etc/pki/tls/private/exim.pem
fi

exit 0

%post
/sbin/chkconfig --add exim

%{_sbindir}/alternatives --install %{_sbindir}/sendmail mta %{_sbindir}/sendmail.exim 10 \
	--slave %{_bindir}/mailq mta-mailq %{_bindir}/mailq.exim \
	--slave %{_bindir}/runq mta-runq %{_bindir}/runq.exim \
	--slave %{_bindir}/rsmtp mta-rsmtp %{_bindir}/rsmtp.exim \
	--slave %{_bindir}/rmail mta-rmail %{_bindir}/rmail.exim \
	--slave /etc/pam.d/smtp mta-pam /etc/pam.d/exim \
	--slave %{_bindir}/newaliases mta-newaliases %{_bindir}/newaliases.exim \
	--slave /usr/lib/sendmail mta-sendmail /usr/lib/sendmail.exim \
	--slave %{_mandir}/man1/mailq.1.gz mta-mailqman %{_mandir}/man8/exim.8.gz \
	--initscript exim

%preun
if [ $1 = 0 ]; then
	/sbin/service exim stop > /dev/null 2>&1
	/sbin/chkconfig --del exim
	%{_sbindir}/alternatives --remove mta %{_sbindir}/sendmail.exim
fi

%postun
if [ "$1" -ge "1" ]; then
	/sbin/service exim  condrestart > /dev/null 2>&1
	mta=`readlink /etc/alternatives/mta`
	if [ "$mta" == "%{_sbindir}/sendmail.exim" ]; then
		/usr/sbin/alternatives --set mta %{_sbindir}/sendmail.exim
	fi
fi

%post greylist
if [ ! -r %{_var}/spool/exim/db/greylist.db ]; then
   sqlite3 %{_var}/spool/exim/db/greylist.db < %{_sysconfdir}/exim/mk-greylist-db.sql
   chown exim.exim %{_var}/spool/exim/db/greylist.db
   chmod 0660 %{_var}/spool/exim/db/greylist.db
fi

%files
%defattr(-,root,root)
%attr(4755,root,root) %{_sbindir}/exim
%{_sbindir}/exim_dumpdb
%{_sbindir}/exim_fixdb
%{_sbindir}/exim_tidydb
%{_sbindir}/exinext
%{_sbindir}/exiwhat
%{_sbindir}/exim_dbmbuild
%{_sbindir}/exicyclog
%{_sbindir}/exigrep
%{_sbindir}/eximstats
%{_sbindir}/exipick
%{_sbindir}/exiqgrep
%{_sbindir}/exiqsumm
%{_sbindir}/exim_lock
%{_sbindir}/exim_checkaccess
%{_sbindir}/convert4r4
%{_sbindir}/sendmail.exim
%{_bindir}/mailq.exim
%{_bindir}/runq.exim
%{_bindir}/rsmtp.exim
%{_bindir}/rmail.exim
%{_bindir}/newaliases.exim
/usr/lib/sendmail.exim
%{_mandir}/*/*
%dir %{_libdir}/exim
%dir %{_libdir}/exim/%{version}-%{release}
%dir %{_libdir}/exim/%{version}-%{release}/lookups

%defattr(-,exim,exim)
%dir %{_var}/spool/exim
%dir %{_var}/spool/exim/db
%dir %{_var}/spool/exim/input
%dir %{_var}/spool/exim/msglog
%dir %{_var}/log/exim

%defattr(-,root,root)
%dir %{_sysconfdir}/exim
%config(noreplace) %{_sysconfdir}/exim/exim.conf
%config(noreplace) %{_sysconfdir}/exim/trusted-configs
%config(noreplace) %{_sysconfdir}/sysconfig/exim
%{_sysconfdir}/rc.d/init.d/exim
%config(noreplace) %{_sysconfdir}/logrotate.d/exim
%config(noreplace) %{_sysconfdir}/pam.d/exim
%{_sysconfdir}/cron.daily/exim-tidydb

%doc ACKNOWLEDGMENTS LICENCE NOTICE README.UPDATING README 
%doc doc util/unknownuser.sh

%attr(0600,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) /etc/pki/tls/certs/exim.pem
%attr(0600,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) /etc/pki/tls/private/exim.pem

%attr(0755,root,root) %ghost %{_sbindir}/sendmail
%attr(0755,root,root) %ghost %{_bindir}/mailq
%attr(0755,root,root) %ghost %{_bindir}/runq
%attr(0755,root,root) %ghost %{_bindir}/rsmtp
%attr(0755,root,root) %ghost %{_bindir}/rmail
%attr(0755,root,root) %ghost %{_bindir}/newaliases
%attr(0755,root,root) %ghost /usr/lib/sendmail
%ghost %{_sysconfdir}/pam.d/smtp
%ghost %{_mandir}/man1/mailq.1.gz

%files mysql
%defattr(-,root,root,-)
%{_libdir}/exim/%{version}-%{release}/lookups/mysql.so

%files pgsql
%defattr(-,root,root,-)
%{_libdir}/exim/%{version}-%{release}/lookups/pgsql.so

%files mon
%defattr(-,root,root)
%{_sbindir}/eximon
%{_sbindir}/eximon.bin

%if 0%{?buildsa}
%files sa
%defattr(-,root,root)
%{_libexecdir}/exim
%config(noreplace) %{_sysconfdir}/exim/sa-*.conf
%doc sa-exim*/*.html
%doc sa-exim*/{ACKNOWLEDGEMENTS,INSTALL,LICENSE,TODO}
%endif

%if 0%{?buildclam}
%post clamav
/bin/touch %{_var}/log/clamd.exim
/bin/chown exim.exim %{_var}/log/clamd.exim
/sbin/chkconfig --add clamd.exim

%preun clamav
test "$1" != 0 || %{_initrddir}/clamd.exim stop &>/dev/null || :
test "$1" != 0 || /sbin/chkconfig --del clamd.exim

%postun clamav
test "$1"  = 0 || %{_initrddir}/clamd.exim condrestart >/dev/null || :

%files clamav
%defattr(-,root,root,-)
%{_sbindir}/clamd.exim
%attr(0755,root,root) %config %{_initrddir}/clamd.exim
%config(noreplace) %verify(not mtime) %{_sysconfdir}/clamd.d/exim.conf
%config(noreplace) %verify(not mtime) %{_sysconfdir}/sysconfig/clamd.exim
%config(noreplace) %verify(not mtime) %{_sysconfdir}/logrotate.d/clamd.exim
%attr(0750,exim,exim) %dir %{_var}/run/clamd.exim
%ghost %attr(0644,exim,exim) %{_var}/log/clamd.exim
%endif

%files greylist
%defattr(-,root,root,-)
%config %{_sysconfdir}/exim/exim-greylist.conf.inc
%ghost %{_var}/spool/exim/db/greylist.db
%{_sysconfdir}/exim/mk-greylist-db.sql
%{_sysconfdir}/cron.daily/greylist-tidy.sh

%changelog
* Mon Feb 06 2012 Josko Plazonic <plazonic@math.princeton.edu>
- add SPF2 support

* Mon May 09 2011 David Woodhouse <David.Woodhouse@intel.com> - 4.76-1
- Update to 4.76 (fixes CVS-2011-1764)

* Wed Mar 23 2011 Dan Horák <dan@danny.cz> - 4.73-3
- rebuilt for mysql 5.5.10 (soname bump in libmysqlclient)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.73-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 05 2011 David Woodhouse <David.Woodhouse@intel.com> - 4.73-1
- Update to 4.73

* Sat Aug 07 2010 David Woodhouse <David.Woodhouse@intel.com> - 4.72-2
- Fedora infrastructure ate my package; bump release and rebuild

* Thu Jun 03 2010 David Woodhouse <David.Woodhouse@intel.com> - 4.72-1
- Update to 4.72 (fixes CVE-2010-2023, CVS-2010-2024)

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 4.71-4
- Mass rebuild with perl-5.12.0

* Thu Mar 18 2010 Miroslav Lichvar <mlichvar@redhat.com> - 4.71-3
- follow guidelines for alternatives (#570800)
- fix init script LSB compliance (#523238)
- handle undefined NETWORKING in init script (#483528)

* Tue Feb 09 2010 Adam Jackson <ajax@redhat.com> 4.71-2
- Fix FTBFS with --no-add-needed

* Thu Dec 24 2009 David Woodhouse <David.Woodhouse@intel.com> - 4.69-20
- Update to 4.71

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 4.69-19
- rebuild against perl 5.10.1

* Mon Oct 05 2009 David Woodhouse <David.Woodhouse@intel.com> - 4.69-18
- Fix typo in clamd %%post (#527085)

* Wed Sep 16 2009 Tomas Mraz <tmraz@redhat.com> - 4.69-17
- Use password-auth common PAM configuration instead of system-auth

* Mon Aug 31 2009 David Woodhouse <David.Woodhouse@intel.com> - 4.69-16
- Create group for exim with correct gid (#518706)
- Allow expansion of spamd_address

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 4.69-15
- rebuilt with new openssl

* Tue Aug 18 2009 Miroslav Lichvar <mlichvar@redhat.com> - 4.69-14
- Move certificate generation to init script (#517013)
- Fix strict aliasing warning

* Wed Aug 12 2009 David Woodhouse <David.Woodhouse@intel.com> - 4.69-13
- Cope with lack of /etc/sysconfig/network (#506330)
- Require /etc/pki/tls/ directories
- Provide exim-tidydb cron job (#481426)
- Provide clamd.exim log file (#452358)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.69-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 4.69-11
- Add subpackage dependencies to fix unowned directories (#474869).
- Add missing defattr.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.69-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 24 2009 Caolán McNamara <caolanm@redhat.com> 4.69-9
- rebuild for dependencies

* Thu Aug 28 2008 Michael Schwendt <mschwendt@fedoraproject.org> 4.69-8
- Include unowned directories.

* Wed Aug 13 2008 David Woodhouse <David.Woodhouse@intel.com> 4.69-7
- Rediff all patches to cope with new zero-fuzz policy

* Wed Aug 13 2008 David Woodhouse <David.Woodhouse@intel.com> 4.69-6
- Add $RPM_OPT_FLAGS in config instead of overriding on make command line.
  (to fix the setting of largefile options which we were killing)

* Sat Apr 19 2008 David Woodhouse <dwmw2@infradead.org> 4.69-5
- Add dynamic lookup patch, split into subpackages (#199256)

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4.69-4
- add Requires for versioned perl (libperl.so)

* Mon Mar 17 2008 David Woodhouse <dwmw2@infradead.org> 4.69-3
- Rebuild for new perl

* Mon Feb 04 2008 Dennis Gilmore <dennis@ausil.us> 4.69-2
- sparc needs -fPIE not -fpie

* Thu Jan 03 2008 David Woodhouse <dwmw2@infradead.org> 4.69-1
- Update to 4.69
- Provide server(smtp) (#380611)

* Wed Dec 05 2007 David Woodhouse <dwmw2@infradead.org> 4.68-3
- Rebuild for OpenSSL/OpenLDAP

* Sun Nov 25 2007 David Woodhouse <dwmw2@infradead.org> 4.68-2
- Fix handling of IPv6 addresses as "known resenders" in example greylist
  configuration

* Fri Aug 31 2007 David Woodhouse <dwmw2@infradead.org> 4.68-1
- Update to 4.68

* Wed Aug 22 2007 David Woodhouse <dwmw2@infradead.org> 4.67-5
- Handle open() being a macro

* Wed Aug 22 2007 David Woodhouse <dwmw2@infradead.org> 4.67-4
- Update licence

* Wed Aug 22 2007 David Woodhouse <dwmw2@infradead.org> 4.67-3
- Rebuild

* Wed Jun 27 2007 David Woodhouse <dwmw2@infradead.org> 4.67-2
- Fix typo in config (#246799)

* Wed Jun 27 2007 David Woodhouse <dwmw2@infradead.org> 4.67-1
- Update to 4.67
- Add config example for using a smarthost, with SMTP AUTH.

* Thu Feb  8 2007 David Woodhouse <dwmw2@infradead.org> 4.66-3
- Improve documentation and error handling in greylist ACL.
- Require HELO before mail

* Wed Feb  7 2007 David Woodhouse <dwmw2@infradead.org> 4.66-2
- Add example of greylisting implementation in Exim ACLs

* Tue Feb  6 2007 David Woodhouse <dwmw2@infradead.org> 4.66-1
- Update to 4.66
- Add dovecot authenticator
- Add 'reload' in init script (#219174)

* Tue Oct 17 2006 Christian Iseli <Christian.Iseli@licr.org> 4.63-6
- Own /etc/exim directory

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 4.63-5
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 25 2006 David Woodhouse <dwmw2@infradead.org> - 4.63-4
- Set home_directory on lmtp_transport by default

* Sun Sep 3 2006 David Woodhouse <dwmw2@infradead.org> - 4.63-3
- chmod +x /etc/init.d/clamd.exim
- Make exim-clamav package require exim (since it uses the same uid)

* Sun Sep 3 2006 David Woodhouse <dwmw2@infradead.org> - 4.63-2
- Add procmail router and transport (#146848)
- Add localhost and localhost.localdomain as local domains (#198511)
- Fix mispatched authenticators (#204591)
- Other cleanups of config file and extra examples
- Add exim-clamav subpackage
- Use existing TLS cert on upgrade, even though it moved

* Sat Aug 26 2006 David Woodhouse <dwmw2@infradead.org> - 4.63-1
- Update to 4.63
- Disable sa-exim, but leave the dlopen patch in

* Wed Jul 19 2006 Thomas Woerner <twoerner@redhat.com> - 4.62-6
- final version
- changed permissions of /etc/pki/tls/*/exim.pem to 0600
- config(noreplace) for /etc/logrotate.d/exim, /etc/pam.d/exim and
  /etc/sysconfig/exim

* Mon Jul 17 2006 Thomas Woerner <twoerner@redhat.com> - 4.62-5
- fixed certs path
- fixed permissions for some binaries
- fixed pam file to use include instead of pam_stack

* Fri Jul  4 2006 David Woodhouse <dwmw2@redhat.com> 4.62-4
- Package review

* Wed Jun 28 2006 David Woodhouse <dwmw2@redhat.com> 4.62-3
- BR tcp_wrappers

* Tue May  2 2006 David Woodhouse <dwmw2@redhat.com> 4.62-2
- Bump release to work around 'make tag' error

* Tue May  2 2006 David Woodhouse <dwmw2@redhat.com> 4.62-1
- Update to 4.62

* Fri Apr  7 2006 David Woodhouse <dwmw2@redhat.com> 4.61-2
- Define LDAP_DEPRECATED to ensure ldap functions are all declared.

* Tue Apr  4 2006 David Woodhouse <dwmw2@redhat.com> 4.61-1
- Update to 4.61

* Thu Mar 23 2006 David Woodhouse <dwmw2@redhat.com> 4.60-5
- Fix eximon buffer overflow (#186303)

* Tue Mar 21 2006 David Woodhouse <dwmw2@redhat.com> 4.60-4
- Actually enable Postgres

* Tue Mar  7 2006 David Woodhouse <dwmw2@redhat.com> 4.60-3
- Rebuild

* Tue Nov 29 2005 David Woodhouse <dwmw2@redhat.com> 4.60-2
- Require libXt-devel

* Tue Nov 29 2005 David Woodhouse <dwmw2@redhat.com> 4.60-1
- Update to 4.60

* Sun Nov 13 2005 David Woodhouse <dwmw2@redhat.com> 4.54-4
- Fix 64-bit build

* Fri Nov 11 2005 David Woodhouse <dwmw2@redhat.com> 4.54-3
- Update X11 BuildRequires

* Wed Oct  5 2005 David Woodhouse <dwmw2@redhat.com> 4.54-2
- Rebuild for new OpenSSL
- Add MySQL and Postgres support to keep jgarzik happy

* Wed Oct  5 2005 David Woodhouse <dwmw2@redhat.com> 4.54-1
- Update to Exim 4.54
- Enable sqlite support

* Thu Aug 25 2005 David Woodhouse <dwmw2@redhat.com> 4.52-2
- Use system PCRE

* Fri Jul  1 2005 David Woodhouse <dwmw2@redhat.com> 4.52-1
- Update to Exim 4.52

* Thu Jun 16 2005 David Woodhouse <dwmw2@redhat.com> 4.51-3
- Rebuild for -devel

* Thu Jun 16 2005 David Woodhouse <dwmw2@redhat.com> 4.51-2
- Update CSA patch

* Wed May  4 2005 David Woodhouse <dwmw2@redhat.com> 4.51-1
- Update to Exim 4.51
- Include Tony's CSA support patch

* Tue Feb 22 2005 David Woodhouse <dwmw2@redhat.com> 4.50-2
- Move exim-doc into a separate package

* Tue Feb 22 2005 David Woodhouse <dwmw2@redhat.com> 4.50-1
- Update to Exim 4.50 and sa-exim 4.2
- Default headers_charset to utf-8
- Add sample spamd stuff to default configuration like exiscan-acl used to

* Sat Jan 15 2005 David Woodhouse <dwmw2@redhat.com> 4.44-1
- Update to Exim 4.44 and exiscan-acl-4.44-28

* Tue Jan  4 2005 David Woodhouse <dwmw2@redhat.com> 4.43-4
- Fix buffer overflows in host_aton() and SPA authentication

* Thu Dec 16 2004 David Woodhouse <dwmw2@redhat.com> 4.43-3
- Demonstrate SASL auth configuration in default config file
- Enable TLS and provide certificate if necessary
- Don't reject all GB2312 charset mail by default

* Mon Dec  6 2004 Thomas Woerner <twoerner@redhat.com> 4.43-2
- rebuild

* Thu Oct  7 2004 Thomas Woerner <twoerner@redhat.com> 4.43-1
- new version 4.43 with sasl support
- new exiscan-acl-4.43-28
- new config.samples and FAQ-html (added publication date)
- new BuildRequires for cyrus-sasl-devel openldap-devel openssl-devel
  and PreReq for cyrus-sasl openldap openssl

* Mon Sep 13 2004 Thomas Woerner <twoerner@redhat.com> 4.42-2
- update to sa-exim-4.1: fixes spamassassin's new score= string (#131796)

* Fri Aug 27 2004 Thomas Woerner <twoerner@redhat.com> 4.42-1
- new version 4.42

* Mon Aug  2 2004 Thomas Woerner <twoerner@redhat.com> 4.41-1
- new version 4.41

* Fri Jul  2 2004 Thomas Woerner <twoerner@redhat.com> 4.34-3
- added pre-definition of local_delivery using Cyrus-IMAP (#122912)
- added BuildRequires for pam-devel (#124555)
- fixed format string bugs (#125117)
- fixed sa-exim code placed wrong in spec file (#127102)
- extended postun with alternatives call

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 12 2004 David Woodhouse <dwmw2@redhat.com> 4.34-1
- Update to Exim 4.34, exiscan-acl 4.34-21

* Sat May 8 2004 David Woodhouse <dwmw2@redhat.com> 4.33-2
- fix buffer overflow in header_syntax check

* Wed May 5 2004 David Woodhouse <dwmw2@redhat.com> 4.33-1
- Update to Exim 4.33, exiscan-acl 4.33-20 to
  fix crashes both in exiscan-acl and Exim itself.

* Fri Apr 30 2004 David Woodhouse <dwmw2@redhat.com> 4.32-2
- Enable IPv6 support, Cyrus saslauthd support, iconv.

* Thu Apr 15 2004 David Woodhouse <dwmw2@redhat.com> 4.32-1
- update to Exim 4.32, exiscan-acl 4.32-17, sa-exim 4.0
- Fix Provides: and Source urls.
- include exiqgrep, exim_checkaccess, exipick
- require /etc/aliases instead of setup

* Tue Feb 24 2004 Thomas Woerner <twoerner@redhat.com> 4.30-6.1
- rebuilt

* Mon Feb 23 2004 Tim Waugh <twaugh@redhat.com>
- Use ':' instead of '.' as separator for chown.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 27 2004 Thomas Woerner <twoerner@redhat.com> 4.30-5
- /usr/lib/sendmail is in alternatives, now
- /etc/alises is now in setup: new Requires for setup >= 2.5.31-1

* Tue Jan 13 2004 Thomas Woerner <twoerner@redhat.com> 4.30-4
- fixed group test in init script
- fixed config patch: use /etc/exim/exim.conf instead of /usr/exim/exim4.conf

* Wed Dec 10 2003 Nigel Metheringham <Nigel.Metheringham@InTechnology.co.uk> - 4.30-3
- Use exim.8 manpage from upstream
- Add eximstats.8 man page (from pod)
- Fixed mailq(1) man page alternatives links

* Mon Dec 08 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- do not package /etc/aliases. We currently require sendmail rpm until
  /etc/aliases moves into a more suitable rpm like "setup" or something else.

* Thu Dec  4 2003 Thomas Woerner <twoerner@redhat.com> 4.30-1
- new version 4.30
- new exiscan-acl-4.30-14
- disabled pie for s390 and s390x

* Wed Dec  3 2003 Tim Waugh <twaugh@redhat.com>
- Fixed PIE support to make it actually work.

* Wed Dec  3 2003 Thomas Woerner <twoerner@redhat.com> 4.24-1.2
- added -fPIE to CFLAGS

* Sat Nov 15 2003 Thomas Woerner <twoerner@redhat.com> 4.24-1.1
- fixed useradd in pre
- fixed alternatives in post

* Thu Nov 13 2003 Thomas Woerner <twoerner@redhat.com> 4.24-1
- new version 4.24 with LDAP and perl support
- added SpamAssassin sa plugin

* Mon Sep 23 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.36-1
- 3.36, fixes security bugs

* Thu Jun 21 2001 Tim Waugh <twaugh@redhat.com> 3.22-14
- Bump release number.

* Tue Jun 12 2001 Tim Waugh <twaugh@redhat.com> 3.22-13
- Remove pam-devel build dependency in order to share package between
  Guinness and Seawolf.

* Fri Jun  8 2001 Tim Waugh <twaugh@redhat.com> 3.22-12
- Fix format string bug.

* Wed May  2 2001 Tim Waugh <twaugh@redhat.com> 3.22-11
- SIGALRM patch from maintainer (bug #20908).
- There's no README.IPV6 any more (bug #32378).
- Fix logrotate entry for exim's pidfile scheme (bug #35436).
- ignore_target_hosts crash fix from maintainer.
- Make the summary start with a capital letter.
- Add reload entry to initscript; use $0 in strings.

* Sun Mar  4 2001 Tim Waugh <twaugh@redhat.com> 3.22-10
- Make sure db ownership is correct on upgrade, since we don't run as
  root when running as a daemon any more.

* Fri Mar  2 2001 Tim Powers <timp@redhat.com>
- rebuilt against openssl-0.9.6-1

* Sat Feb 17 2001 Tim Waugh <twaugh@redhat.com>
- Run as user mail, group mail when we drop privileges (bug #28193).

* Tue Feb 13 2001 Tim Powers <timp@redhat.com>
- added conflict with postfix

* Thu Jan 25 2001 Tim Waugh <twaugh@redhat.com>
- Avoid using zero-length salt in crypteq expansion.

* Tue Jan 23 2001 Tim Waugh <twaugh@redhat.com>
- Redo initscript internationalisation.
- Initscript uses bash not sh.

* Mon Jan 22 2001 Tim Waugh <twaugh@redhat.com>
- Okay, the real bug was in libident.

* Mon Jan 22 2001 Tim Waugh <twaugh@redhat.com>
- Revert the RST patch for now; if it's needed, it's a pidentd bug
  and should be fixed there.

* Mon Jan 22 2001 Tim Waugh <twaugh@redhat.com>
- 3.22.
- Build requires XFree86-devel.

* Mon Jan 15 2001 Tim Waugh <twaugh@redhat.com>
- New-style prereqs.
- Initscript internationalisation.

* Thu Jan 11 2001 Tim Waugh <twaugh@redhat.com>
- Security patch no longer required; 3.20 and later have a hide feature
  to do the same thing.
- Mark exim.conf noreplace.
- Better libident (RST) patch.

* Wed Jan 10 2001 Tim Waugh <twaugh@redhat.com>
- Fix eximconfig so that it tells the user the correct place to look
  for documentation
- Fix configure.default to deliver mail as group mail so that local
  delivery works

* Tue Jan 09 2001 Tim Waugh <twaugh@redhat.com>
- 3.21

* Mon Jan 08 2001 Tim Waugh <twaugh@redhat.com>
- Enable TLS support (bug #23196)

* Mon Jan 08 2001 Tim Waugh <twaugh@redhat.com>
- 3.20 (bug #21895).  Absorbs configure.default patch
- Put URLs in source tags where applicable
- Add build requirement on pam-devel

* Wed Oct 18 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix up eximconfig's header generation (we're not Debian), Bug #18068
- BuildRequires db2-devel (Bug #18089)
- Fix typo in logrotate script (Bug #18308)
- Local delivery must be setuid to work (Bug #18314)
- Don't send TCP RST packages to ident (Bug #19048)

* Wed Oct 18 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 3.16
- fix security bug
- some specfile cleanups
- fix handling of RPM_OPT_FLAGS

* Fri Aug 18 2000 Tim Powers <timp@redhat.com>
- fixed bug #16535, logrotate script changes

* Thu Aug 17 2000 Tim Powers <timp@redhat.com>
- fixed bug #16460
- fixed bug #16458
- fixed bug #16476

* Wed Aug 2 2000 Tim Powers <timp@redhat.com>
- fixed bug #15142

* Fri Jul 28 2000 Than Ngo <than@redhat.de>
- add missing restart function in startup script
- add rm -rf $RPM_BUILD_ROOT in install section
- use %%{_tmppath}

* Fri Jul 28 2000 Tim Powers <timp@redhat.com>
- fixed initscript so that condrestart doesn't return 1 when the test fails

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Mon Jul 17 2000 Tim Powers <timp@redhat.com>
- inits bakc to rc.d/init.d, using service to start inits

* Thu Jul 13 2000 Tim Powers <timp@redhat.com>
- applied patch from bug #13890

* Mon Jul 10 2000 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jul 06 2000 Tim Powers <timp@redhat.com>
- added patch submitted by <Chris.Keane@comlab.ox.ac.uk>, fixes bug #13539

* Thu Jul 06 2000 Tim Powers <timp@redhat.com>
- fixed broken prereq to require /etc/init.d

* Tue Jun 27 2000 Tim Powers <timp@redhat.com>
- PreReq initscripts >= 5.20

* Mon Jun 26 2000 Tim Powers <timp@redhat.com>
- fix init.d script location
- add condrestart to init.d script

* Wed Jun 14 2000 Nalin Dahyabhai <nalin@redhat.com>
- migrate to system-auth setup

* Tue Jun 6 2000 Tim Powers <timp@redhat.com>
- fixed man page location

* Tue May 9 2000 Tim Powers <timp@redhat.com>
- rebuilt for 7.0

* Fri Feb 04 2000 Tim Powers <timp@redhat.com>
- fixed the groups to be in Red Hat groups.
- removed Vendor header since it is going to be marked Red Hat in our build
	system.
- quiet setups
- strip binaries
- fixed so that man pages can be auto gzipped by new RPM (in files list
	/usr/man/*/* )
- built for Powertools 6.2

* Tue Jan 18 2000 Mark Bergsma <mark@mbergsma.demon.nl>
- Upgraded to exim 3.13
- Removed i386 specialization
- Added syslog support

* Wed Dec 8 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Upgraded to exim 3.12
- Procmail no longer used as the delivery agent

* Wed Dec 1 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Upgraded to exim 3.11

* Sat Nov 27 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Added /etc/pam.d/exim

* Wed Nov 24 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Upgraded to exim 3.10

* Thu Nov 11 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Added eximconfig script, thanks to Mark Baker
- Exim now uses the Berkeley DB library.

* Fri Aug 4 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Upgraded to version 3.03
- Removed version number out of the spec file name.

* Fri Jul 23 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Added embedded Perl support.
- Added tcp_wrappers support.
- Added extra documentation in a new doc subpackage.

* Mon Jul 12 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Added /usr/sbin/sendmail as a link to exim.
- Fixed wrong filenames in logrotate entry. 

* Sun Jul 11 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Now using the '%%changelog' tag.
- Removed the SysV init links - let chkconfig handle them. 
- Replaced install -d with mkdir -p

* Sat Jul 10 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Fixed owner of the exim-mon files - the owner is now root

* Thu Jul 08 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Removed executable permission bits of /etc/exim.conf
- Removed setuid permission bits of all programs except exim
- Changed spool/log directory owner/groups to 'mail'
- Changed the default configuration file to make exim run
      as user and group 'mail'.

* Thu Jul 08 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Added the /usr/bin/rmail -> /usr/sbin/exim symlink.
- Added the convert4r3 script.
- Added the transport-filter.pl script to the documentation.

* Thu Jul 08 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Added procmail transport and director, and made that the
      default.
- Added the unknownuser.sh script to the documentation.

* Thu Jul 08 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Added manpage for exim.
- Fixed symlinks pointing to targets under Buildroot.
- The exim logfiles will now only be removed when uninstalling,
      not upgrading.

* Wed Jul 07 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Added 'Obsoletes' header.
- Added several symlinks to /usr/sbin/exim.

* Wed Jul 07 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- First RPM packet release.
- Not tested on other architectures/OS'es than i386/Linux..

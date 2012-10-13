Name:       awstats
Version:    7.0
Release:    2%{?dist}
Summary:    Advanced Web Statistics
License:    GPLv2
Group:      Applications/Internet
URL:        http://awstats.sourceforge.net
Source0:    http://downloads.sourceforge.net/project/awstats/AWStats/%{version}/awstats-%{version}.tar.gz
Patch0:     awstats-awredir.pl-sanitize-parameters.patch

BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  recode
Requires:   perl
Requires(post): perl
Requires(postun): /sbin/service

## SELinux policy is now included upstream
Obsoletes:  awstats-selinux < 6.8-1
Provides:   awstats-selinux = %{version}-%{release}


%description
Advanced Web Statistics is a powerful and featureful tool that generates
advanced web server graphic statistics. This server log analyzer works
from command line or as a CGI and shows you all information your log contains,
in graphical web pages. It can analyze a lot of web/wap/proxy servers like
Apache, IIS, Weblogic, Webstar, Squid, ... but also mail or ftp servers.

This program can measure visits, unique vistors, authenticated users, pages,
domains/countries, OS busiest times, robot visits, type of files, search
engines/keywords used, visits duration, HTTP errors and more...
Statistics can be updated from a browser or your scheduler.
The program also supports virtual servers, plugins and a lot of features.

With the default configuration, the statistics are available:
http://localhost/awstats/awstats.pl


%prep
%setup -q
%patch0 -p 1
# Fix style sheets.
perl -pi -e 's,/icon,/awstatsicons,g' wwwroot/css/*
# Fix some bad file permissions here for convenience.
chmod -x tools/httpd_conf
find tools/xslt -type f | xargs chmod -x
# Remove \r in conf file (file written on MS Windows)
perl -pi -e 's/\r//g' docs/COPYING.TXT docs/LICENSE.TXT docs/pad_awstats.xml docs/awstats_changelog.txt docs/styles.css tools/httpd_conf tools/logresolvemerge.pl tools/awstats_exportlib.pl tools/awstats_buildstaticpages.pl tools/maillogconvert.pl tools/urlaliasbuilder.pl wwwroot/cgi-bin/awredir.pl
# Encoding
recode ISO-8859-1..UTF-8 docs/awstats_changelog.txt


%install
rm -rf $RPM_BUILD_ROOT

### Create cron job
cat <<EOF >awstats.cron
#!/bin/bash
exec %{_datadir}/awstats/tools/awstats_updateall.pl now \
        -configdir="%{_sysconfdir}/awstats" \
        -awstatsprog="%{_datadir}/awstats/wwwroot/cgi-bin/awstats.pl" >/dev/null
exit 0
EOF

### Create folders
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/{httpd/conf.d,%{name},cron.hourly}
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}

### Install files
cp -pr tools $RPM_BUILD_ROOT%{_datadir}/%{name}
chmod 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/tools/*.pl
chmod 644 $RPM_BUILD_ROOT%{_datadir}/%{name}/tools/httpd_conf
cp -pr wwwroot $RPM_BUILD_ROOT%{_datadir}/%{name}
chmod 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/wwwroot/cgi-bin/*.pl
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/wwwroot/classes/src
### We want these outside CGI path.
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/wwwroot/cgi-bin/{lang,lib,plugins}
cp -pr wwwroot/cgi-bin/{lang,lib,plugins} $RPM_BUILD_ROOT%{_datadir}/%{name}

rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/wwwroot/cgi-bin/awstats.model.conf

### Commit permanent changes to default configuration
install -p -m 644 wwwroot/cgi-bin/awstats.model.conf \
    $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/%{name}.model.conf
perl -pi -e '
                s|^LogFile=.*$|LogFile="%{_localstatedir}/log/httpd/access_log"|;
                s|^DirData=.*$|DirData="%{_localstatedir}/lib/awstats"|;
                s|^DirCgi=.*$|DirCgi="/awstats"|;
                s|^DirIcons=.*$|DirIcons="/awstatsicons"|;
                s|^SiteDomain=.*$|SiteDomain="localhost.localdomain"|;
                s|^HostAliases=.*$|HostAliases="localhost 127.0.0.1"|;
                s|^EnableLockForUpdate=.*$|EnableLockForUpdate=1|;
                s|^SaveDatabaseFilesWithPermissionsForEveryone=.*$|SaveDatabaseFilesWithPermissionsForEveryone=0|;
                s|^SkipHosts=.*$|SkipHosts="127.0.0.1"|;
                s|^Expires=.*$|Expires=3600|;
            ' $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/%{name}.model.conf
install -p -m 644 $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/%{name}.{model,localhost.localdomain}.conf 

# Fix scripts
perl -pi -e 's|/usr/local/awstats|%{_datadir}/awstats|g' \
             $RPM_BUILD_ROOT%{_datadir}/%{name}/tools/{*.pl,httpd_conf}

# Apache configuration
install -p -m 644 tools/httpd_conf $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d/%{name}.conf
perl -pi -e 's|/usr/local|%{_datadir}|g;s|Allow from all|Allow from 127.0.0.1|g' \
             $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d/%{name}.conf
echo "# Additional Perl modules
<IfModule mod_env.c>
    SetEnv PERL5LIB %{_datadir}/awstats/lib:%{_datadir}/awstats/plugins
</IfModule>" >> $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d/%{name}.conf

# Cron job
install -m 0755 awstats.cron $RPM_BUILD_ROOT%{_sysconfdir}/cron.hourly/%{name}


%clean
rm -rf $RPM_BUILD_ROOT


%post
if [ $1 -eq 1 ]; then
  if [ ! -f %{_sysconfdir}/%{name}/%{name}.`hostname`.conf ]; then
    %{__cat} %{_sysconfdir}/%{name}/%{name}.model.conf | \
      %{__perl} -p -e 's|^SiteDomain=.*$|SiteDomain="'`hostname`'"|;
                       s|^HostAliases=.*$|HostAliases="REGEX[^.*'${HOSTNAME//./\\\\.}'\$]"|;
                      ' > %{_sysconfdir}/%{name}/%{name}.`hostname`.conf || :
  fi
fi

%postun
if [ $1 -ne 0 ]; then
  /sbin/service httpd condrestart >/dev/null 2>&1
fi


%files
%defattr(-,root,root,755)
# Apache configuration file
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/cron.hourly/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/
%{_localstatedir}/lib/%{name}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/wwwroot
%{_datadir}/%{name}/tools
%{_datadir}/%{name}/wwwroot/cgi-bin
# Different defattr to fix lots of files which should not be +x.
%defattr(644,root,root,755)
%doc README.TXT docs/*
%{_datadir}/%{name}/lang
%{_datadir}/%{name}/lib
%{_datadir}/%{name}/plugins
%{_datadir}/%{name}/wwwroot/classes
%{_datadir}/%{name}/wwwroot/css
%{_datadir}/%{name}/wwwroot/icon
%{_datadir}/%{name}/wwwroot/js


%changelog
* Fri Oct 07 2011 Petr Lautrbach <plautrba@redhat.com> 7.0-2
- fix multiple XSS and sql injection flaws (#740926)

* Tue Feb 15 2011 Petr Lautrbach <plautrba@redhat.com> 7.0-1
- update to upstream 7.0 version

* Thu Nov 26 2009 Aurelien Bompard <abompard@fedoraproject.org> -  6.95-1
- version 6.95 (security fix)
- drop patch0

* Fri Aug 21 2009 Aurelien Bompard <abompard@fedoraproject.org> -  6.9-4
- don't backup the cgi when patching (#518168)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 31 2008 Aurelien Bompard <abompard@fedoraproject.org> 6.9-1
- version 6.9
- use Debian's version of the CVE-2008-3714 fix

* Sat Dec 06 2008 Aurelien Bompard <abompard@fedoraproject.org> 6.8-3
- Use Debian's patch for CVE-2008-3714 (rh#474396)

* Sat Aug 23 2008 Aurelien Bompard <abompard@fedoraproject.org> 6.8-2
- Add upstream patch for CVE-2008-3714

* Mon Jul 21 2008 Aurelien Bompard <abompard@fedoraproject.org> 6.8-1
- version 6.8

* Fri Mar 14 2008 Aurelien Bompard <abompard@fedoraproject.org> 6.7-3
- SELinux policy is included upstream
- Fix cron job (bug 435101)

* Sun Dec 02 2007 Aurelien Bompard <abompard@fedoraproject.org> 6.7-2
- awstats does not actually require httpd (bug 406901)

* Mon Aug 13 2007 Aurelien Bompard <abompard@fedoraproject.org> 6.7-1
- split SElinux bits in the -selinux package (bug 250637)
- use an SElinux module instead of semanage
- update to version 6.7

* Sun Jan 07 2007 Aurelien Bompard <abompard@fedoraproject.org> 6.6-1
- version 6.6 final

* Fri Nov 03 2006 Aurelien Bompard <abompard@fedoraproject.org> 6.6-0.4.beta
- fix typo in the cron job (bug 213803)

* Mon Oct 30 2006 Aurelien Bompard <abompard@fedoraproject.org> 6.6-0.3.beta
- fix DOS encoding on logresolvemerge.pl

* Wed Aug 30 2006 Aurelien Bompard <abompard@fedoraproject.org> 6.6-0.2.beta
- rebuild

* Sun May 07 2006 Aurelien Bompard <gauret[AT]free.fr> 6.6-0.1.beta
- version 6.6 (beta), fixes CVE-2005-2732 (bug 190921, 190922, and 190923)

* Sun Apr 09 2006 Aurelien Bompard <gauret[AT]free.fr> 6.5-3
- SELinux support: use semanage to label the cgi and the database files
- Only allow access from localhost by default (this app has a security history)

* Thu Feb 23 2006 Aurelien Bompard <gauret[AT]free.fr> 6.5-2
- rebuild for FC5

* Wed Jan 11 2006 Aurelien Bompard <gauret[AT]free.fr> 6.5-1
- version 6.5 final

* Mon Aug 22 2005 Aurelien Bompard <gauret[AT]free.fr> 6.5-1
- version 6.5 (beta), fixes CAN-2005-1527

* Mon Mar 21 2005 Aurelien Bompard <gauret[AT]free.fr> 6.4-1
- version 6.4 final
- change release tag (following Owen's scheme)
- convert tabs into spaces

* Tue Feb 15 2005 Aurelien Bompard <gauret[AT]free.fr> 6.4-0.1.pre
- update to 6.4pre to fix a vulnerability

* Thu Feb 10 2005 Aurelien Bompard <gauret[AT]free.fr> 6.3-1
- version 6.3 final

* Thu Jan 27 2005 Aurelien Bompard <gauret[AT]free.fr> 6.3-0.1.20050122
- update to 6.3pre to fix vulnerability

* Sun Nov 28 2004 Aurelien Bompard <gauret[AT]free.fr> 6.2-0.fdr.1
- version 6.2

* Thu May 20 2004 Aurelien Bompard <gauret[AT]free.fr> 6.1-0.fdr.6
- remove redundant substitution

* Thu May 20 2004 Aurelien Bompard <gauret[AT]free.fr> 6.1-0.fdr.5
- be closer to upstream default configuration
- use the included apache conf file
- merge changes from Michael Schwendt (bug 1608)

* Wed May 19 2004 Aurelien Bompard <gauret[AT]free.fr> 6.1-0.fdr.4
- fix cron job for relocated tools

* Wed May 19 2004 Aurelien Bompard <gauret[AT]free.fr> 6.1-0.fdr.3
- keep the tools in the tools subdirectory

* Wed May 19 2004 Aurelien Bompard <gauret[AT]free.fr> 6.1-0.fdr.2
- fix scripts in /usr/bin
- rename configure.pl to awstats_configure.pl

* Sun May 16 2004 Aurelien Bompard <gauret[AT]free.fr> 6.1-0.fdr.1
- version 6.1

* Wed Mar 03 2004 Aurelien Bompard <gauret[AT]free.fr> 6.0.0.fdr.2
- requires perl without version to fix build on rh9

* Tue Feb 19 2004 Aurelien Bompard <gauret[AT]free.fr> 6.0-0.fdr.1
- version 6.0

* Mon Dec 22 2003 Aurelien Bompard <gauret[AT]free.fr> 5.9-0.fdr.5
- solve stupid bug in %%install
- only create the preconfigured config file on install, not on upgrade

* Mon Dec 22 2003 Aurelien Bompard <gauret[AT]free.fr> 5.9-0.fdr.4
- post scriptlet doesn't overwrite user configuration now
  be careful if you upgrade from 5.9-0.fdr.3
- replace _DATADIR in apache configuration in the install stage
  (was in the post scriptlet before)
- remove 'noreplace' tag from the apache config file
- various cleanups in the %%install stage
- Thanks to Mickael Schwendt.

* Sun Dec 07 2003 Aurelien Bompard <gauret[AT]free.fr> 5.9-0.fdr.3
- %%post et %%postun now use condrestart instead of restart
- only restart apache if we are upgrading
- install and cp use the "-p" switch
- use %%_datadir in /etc/httpd/conf.d/awstats.conf
- improve cron job 
- don't brutally recode HTML pages
- the scan is now done hourly instead of daily
- *.pm files are not executable any more
- tools are in %%bindir
- various other improvements
- many thanks to Michael Schwendt and Dag Wieers.

* Sat Nov 29 2003 Aurelien Bompard <gauret[AT]free.fr> 5.9-0.fdr.2
- Set the hostname in %%post (thanks to Michael Koziarski)
- Improved customization in %%post

* Sun Nov 16 2003 Aurelien Bompard <gauret[AT]free.fr> 5.9-0.fdr.1
- fix /etc/cron.daily/awstats permissions
- fix log name in conf file
- port to fedora (from Mandrake)

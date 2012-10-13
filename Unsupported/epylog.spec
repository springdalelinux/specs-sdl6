%{!?_python_sitelib: %define _python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           epylog
Version:        1.0.3
Release:        15%{?dist}
Summary:        New logs analyzer and parser

Group:          Applications/System
License:        GPLv2+
URL:            https://fedorahosted.org/epylog/
Source:         http://fedorapeople.org/~icon/epylog/epylog-%{version}.tar.gz
Patch0:         epylog-1.0.3-mimewriter.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:	libxml2-python
Requires:       libxml2-python


%description
Epylog is a new log notifier and parser which runs periodically out of
cron, looks at your logs, processes the entries in order to present
them in a more comprehensive format, and then provides you with the
output. It is written specifically with large network clusters in mind
where a lot of machines (around 50 and upwards) log to the same
loghost using syslog or syslog-ng.


%package perl
Summary:        Perl module for writing external Epylog modules
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description perl
This package provides a perl module for epylog. It is useful for
writing epylog modules that use external module API. No modules shipping
with epylog by default use that API, so install this only if you are using
external perl modules, or intend to write some of your own.


%prep
%setup -q
##
# Apply mimewriter patch
#
%patch0 -p1
##
# The --with-lynx is just a sane default. Epylog doesn't actually require 
# it to run in the out-of-the-box configuration.
#
%configure \
    --with-python=%{__python} \
    --with-python-dirs=%{_python_sitelib} \
    --with-lynx=%{_bindir}/links \
    --with-site-perl=%{perl_vendorlib}
##
# Fix version.
#
sed -i -e \
    "s/^VERSION\s*=\s*.*/VERSION = '%{name}-%{version}-%{release}'/g" \
    py/epylog/__init__.py


%build
make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
##
# Remove installed docs
#
rm -rf $RPM_BUILD_ROOT%{_docdir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog INSTALL LICENSE README doc/*
%config(noreplace) %{_sysconfdir}/epylog
%config(missingok) %{_sysconfdir}/cron.*/*
%dir %{_localstatedir}/lib/epylog
%dir %{_datadir}/epylog
%dir %{_datadir}/epylog/modules
%{_datadir}/epylog/modules/*
%{_python_sitelib}/epylog
%{_sbindir}/*
%{_mandir}/man8/*
%{_mandir}/man5/*


%files perl
%defattr(-,root,root,-)
%{perl_vendorlib}/epylog.pm
%{_mandir}/man3/*


%changelog
* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.0.3-14
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 16 2010 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.0.3-13
- Patch to fix MimeWriter warning
- Adjust URLs

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.0.3-12
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.0.3-11
- rebuild against perl 5.10.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0.3-8
- Rebuild for Python 2.6

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0.3-7
Rebuild for new perl

* Sun Feb 17 2008 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.0.3-6
- Remove manual python-abi provides
- Update license to GPLv2+

* Thu Dec 14 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.0.3-5
- Rebuild for new python.

* Tue Jun 20 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.0.3-4
- Disttagging
- BuildRequire libxml2-python

* Mon Apr 25 2005 Konstantin Ryabitsev <icon@linux.duke.edu> 1.0.3-3
- Do not redefine perl_vendorlib, since it's available in the default
  rpmmacros.
- Make epylog-perl depend on full EVR.
- Use _docdir instead of _defaultdocdir.
- Add modules dir to filelists.
- Don't move docs around.
- Remove 0-epoch.

* Tue Apr 05 2005 Konstantin Ryabitsev <icon@linux.duke.edu> 1.0.3-2
- Do not BuildRequire sed.

* Thu Mar 31 2005 Konstantin Ryabitsev <icon@linux.duke.edu> 1.0.3-1
- Rework the specfile to match Fedora Extras format.
- Use _perl_vendorlib
- Use _python_sitelib
- Make the cronfile config(missingok)

* Wed May 19 2004 Konstantin Ryabitsev <icon@linux.duke.edu> 1.0.1-1
- Use automatic _pyver determination to make rebuilds simpler.
- Don't gzip man, it will be done automatically.

* Fri Apr 09 2004 Konstantin Ryabitsev <icon@linux.duke.edu> 1.0-1
- Version 1.0
- Do not depend on elinks to make things simpler

* Mon Feb 09 2004 Konstantin Ryabitsev <icon@linux.duke.edu> 0.9.7-1
- Version 0.9.7
- Depend on python version.

* Mon Sep 22 2003 Konstantin Ryabitsev <icon@linux.duke.edu> 0.9.6-1
- Version 0.9.6

* Wed Jul 23 2003 Konstantin Ryabitsev <icon@linux.duke.edu> 0.9.5-1
- Version 0.9.5

* Tue May 20 2003 Konstantin Ryabitsev <icon@linux.duke.edu> 0.9.4-1
- Specfile cleanups to make it more easily adaptable for Linux@DUKE.
- Fix for bug 38 (incorrect offsets were causing backtrace)
- Normalized logger calls (bug 9)
- Enhancements to mail and packets modules

* Thu May  1 2003 Konstantin Ryabitsev <icon@linux.duke.edu> 0.9.3-1
- Now using autoconf to do the building.
- Added qmail support in mail module.
- Split perl module into a separate package.

* Tue Apr 29 2003 Konstantin Ryabitsev <icon@linux.duke.edu> 0.9.2-1
- Notices module reworked to support custom notifications.
- Weeder module now supports 'ALL' for enable
- Some changes to epylog core to return matched regex as part of linemap.

* Fri Apr 25 2003 Konstantin Ryabitsev <icon@linux.duke.edu> 0.9.1-1
- Some bugfixes after running pychecker
- Added doc/INSTALL for people not running RPM.

* Thu Apr 18 2003 Konstantin Ryabitsev <icon@linux.duke.edu> 0.9.0-1
- A significant rewrite of module handlers.

* Wed Mar 13 2003 Konstantin Ryabitsev <icon@linux.duke.edu> 0.8.14-1
- Fixes for html email sending
- Option to send via sendmail vs. smtplib
- Multiple mailto addresses now handled correctly
- Small bugfixes.

* Mon Mar 03 2003 Konstantin Ryabitsev <icon@linux.duke.edu> 0.8.13-1
- Two new features for module configs: you can now specify the priority
  and extra options for modules.

* Fri Feb 28 2003 Konstantin Ryabitsev <icon@linux.duke.edu> 0.8.12-1
- Two small bugfixes which prevented some modules from ever being 
  executed when the last log was 0 length.

* Thu Feb 27 2003 Konstantin Ryabitsev <icon@linux.duke.edu> 0.8.11-1
- Small changes to logrotation modules, allowing them to specify
  a full path to a rotated file.

* Wed Feb 26 2003 Konstantin Ryabitsev <icon@linux.duke.edu> 0.8.10-1
- Ported some modules from DULog.

* Mon Feb 10 2003 Konstantin Ryabitsev <icon@linux.duke.edu> 0.8.9-1
- Several fixes in fine_locate routines causing it not to break
  on logs with non-consecutive entries and live logs.

* Fri Feb 07 2003 Konstantin Ryabitsev <icon@linux.duke.edu> 0.8.7-1
- More fixes for the memory-friendly grep.

* Tue Jan 28 2003 Konstantin Ryabitsev <icon@linux.duke.edu> 0.8.6-1
- Lots and lots of memory optimizations (chunked reads throughout)
- Entities replaced in get_html_report
- memory-friendly fgrep calls

* Mon Jan 27 2003 Konstantin Ryabitsev <icon@linux.duke.edu> 0.8.5-1
- Big rewrite of logfile handling routines. This works much-much-much
  better!
- A useful usage().
- Lots of bugfixes.

* Sat Jan 18 2003 Konstantin Ryabitsev <icon@linux.duke.edu> 0.8-1
- First attempt at building a semi-usable epylog. It even works.
  Sometimes. :)
- Removed DULog-related changelogs.

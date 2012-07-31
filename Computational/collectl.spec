Summary: A utility to collect various Linux performance data
Name: collectl
Version: 3.6.0
Release: 1%{?dist}
License: GPLv2+ or Artistic
Group: Applications/System
Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.src.tar.gz
Source1: %{name}.initd
Source2: %{name}.sysconfig
URL: http://collectl.sourceforge.net
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: perl(Sys::Syslog), perl(Time::HiRes), perl(Compress::Zlib)
Requires(post): chkconfig
Requires(postun): initscripts
Requires(preun): chkconfig
Requires(preun): initscripts

%description
A utility to collect Linux performance data


%prep
%setup -q

# rename directory for easier inclusion
mv docs html

# fix EOLs + preserve timestamps
for f in col2tlviz.pl
do
    sed -i.orig 's/\r//g' $f
    touch -r $f.orig $f
done


%build
# nothing to do


%clean
rm -rf $RPM_BUILD_ROOT


%install
rm -rf $RPM_BUILD_ROOT

# create required directories
mkdir -p        $RPM_BUILD_ROOT%{_initrddir} \
                $RPM_BUILD_ROOT%{_sysconfdir} \
                $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig \
                $RPM_BUILD_ROOT%{_bindir} \
                $RPM_BUILD_ROOT%{_datadir}/%{name}/utils \
                $RPM_BUILD_ROOT%{_mandir}/man1/ \
                $RPM_BUILD_ROOT%{_localstatedir}/log/%{name}

# install the files, setting the mode
install -p -m 755  collectl.pl       $RPM_BUILD_ROOT%{_bindir}/collectl
install -p -m 644  *.ph              $RPM_BUILD_ROOT%{_datadir}/%{name}
install -p -m 644  envrules.std      $RPM_BUILD_ROOT%{_datadir}/%{name}
install -p -m 755  readS             $RPM_BUILD_ROOT%{_datadir}/%{name}/utils
install -p -m 755  col2tlviz.pl      $RPM_BUILD_ROOT%{_datadir}/%{name}/utils
install -p -m 755  client.pl         $RPM_BUILD_ROOT%{_datadir}/%{name}/utils
install -p -m 644  man1/collectl*.1  $RPM_BUILD_ROOT%{_mandir}/man1
install -p -m 644  collectl.conf     $RPM_BUILD_ROOT%{_sysconfdir}
install -p -m 755  %{SOURCE1}        $RPM_BUILD_ROOT%{_initrddir}/%{name}
install -p -m 644  %{SOURCE2}        $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}


%post
/sbin/chkconfig --add %{name}

%postun
if [ "$1" -ge "1" ] ; then
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi

%preun
if [ $1 = 0 ] ; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi


%files
%defattr(-,root,root,-)
%doc ARTISTIC COPYING GPL RELEASE-collectl html
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_bindir}/*
%{_datadir}/%{name}
%{_mandir}/man1/*
%{_localstatedir}/log/%{name}


%changelog
* Thu Oct 20 2011 Dan Horák <dan[at]danny.cz> 3.6.0-1
- upgrade to upstream version 3.6.0

* Thu Jun 02 2011 Dan Horák <dan[at]danny.cz> 3.5.1-1
- upgrade to upstream version 3.5.1

* Fri Mar 25 2011 Dan Horák <dan[at]danny.cz> 3.5.0-1
- upgrade to upstream version 3.5.0

* Mon Sep 13 2010 Dan Horák <dan[at]danny.cz> 3.4.3-1
- upgrade to upstream version 3.4.3

* Wed Jul 21 2010 Dan Horák <dan[at]danny.cz> 3.4.2-1
- upgrade to upstream version 3.4.2

* Thu Apr  1 2010 Dan Horák <dan[at]danny.cz> 3.4.1-1
- upgrade to upstream version 3.4.1

* Wed Feb 17 2010 Dan Horák <dan[at]danny.cz> 3.4.0-1
- upgrade to upstream version 3.4.0
- updated directory layout to match upstream

* Tue Jan  5 2010 Dan Horák <dan[at]danny.cz> 3.3.6-1
- upgrade to upstream version 3.3.6

* Fri Aug 21 2009 Dan Horák <dan[at]danny.cz> 3.3.5-1
- upgrade to upstream version 3.3.5

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 29 2009 Dan Horák <dan[at]danny.cz> 3.3.4-2
- install only a symlink into /usr/bin (#508724)

* Mon Jun 15 2009 Dan Horák <dan[at]danny.cz> 3.3.4-1
- upgrade to upstream version 3.3.4
- changelog: http://collectl.sourceforge.net/Releases.html

* Wed Apr 29 2009 Dan Horák <dan[at]danny.cz> 3.3.2-1
- upgrade to upstream version 3.3.2
- install missing file
- changelog: http://collectl.sourceforge.net/Releases.html

* Tue Apr 28 2009 Dan Horák <dan[at]danny.cz> 3.3.1-1
- upgrade to upstream version 3.3.1
- changelog: http://collectl.sourceforge.net/Releases.html

* Sat Mar 21 2009 Dan Horak <dan[at]danny.cz> 3.2.1-1
- upgrade to upstream version 3.2.1

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 24 2009 Dan Horak <dan[at]danny.cz> 3.1.3-1
- upgrade to upstream version 3.1.3

* Tue Jan 20 2009 Dan Horak <dan[at]danny.cz> 3.1.2-1
- upgrade to upstream version 3.1.2

* Sat Nov  8 2008 Dan Horak <dan[at]danny.cz> 3.1.1-1
- upgrade to upstream version 3.1.1

* Mon Sep 22 2008 Dan Horak <dan[at]danny.cz> 3.1.0-1
- upgrade to upstream version 3.1.0
- remove logrotate support because internal mechanism is used by default

* Tue Jul  8 2008 Karel Zak <kzak@redhat.com> 3.0.0-1
- upgrade to upstream version 3.0.0

* Thu Jun 19 2008 Karel Zak <kzak@redhat.com> 2.6.4-1
- initial packaging (thanks to Dan Horak), based upon upstream srpm

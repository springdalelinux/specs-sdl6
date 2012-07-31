Summary: collectl utilities
Name: collectl-utils
Version: 3.2.0
Release: 1%{?dist}
License: HP
Group: Application/Performance
Source: %{name}-%{version}.src.tar.gz
Url: http://collectl-utils.sourceforge.net
BuildRoot: %{_tmppath}/%{name}-root
BuildArch: noarch
AutoReqProv: no
Requires: /bin/sh
Requires: /usr/bin/perl
Requires: perl(Config)
Requires: perl(Cwd)
Requires: perl(File::Basename)
Requires: perl(Getopt::Long)
Requires: perl(IO::Select)
Requires: perl(IO::Socket)
Requires: perl(strict)

%description
collectl plotting and other miscellaneous utilities

%package        web
Summary:        Web collectl-utils files
Group:          Application/Performance
Requires:       %{name} = %{version}-%{release}
Requires:       httpd

%description    web

%prep
%setup -n %{name}-%{version}

%build

%clean 
rm -Rf $RPM_BUILD_ROOT

%install
cd $RPM_BUILD_DIR/%{name}-%{version}
rm -Rf %{buildroot}

# Create required directories
mkdir -p $RPM_BUILD_ROOT/etc
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/share/man/man1
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/collectl-utils-%{version}
mkdir -p $RPM_BUILD_ROOT/usr/share/collectl
mkdir -p $RPM_BUILD_ROOT/usr/share/collectl/plotfiles
mkdir -p $RPM_BUILD_ROOT/usr/share/collectl/util

# install the files, setting the mode
install -m 644 	colplot.conf          $RPM_BUILD_ROOT/etc
install -m 755 	colgui colmux colplot $RPM_BUILD_ROOT/usr/bin
install -m 644 	colplotlib.ph         $RPM_BUILD_ROOT/usr/share/collectl
install -m 644 	colplotlib.defs       $RPM_BUILD_ROOT/usr/share/collectl
install -m 644  plotfiles/*           $RPM_BUILD_ROOT/usr/share/collectl/plotfiles
install -m 755 	genplotfiles          $RPM_BUILD_ROOT/usr/share/collectl/util
install -m 644  man1/*.1*             $RPM_BUILD_ROOT/usr/share/man/man1

mkdir -p $RPM_BUILD_ROOT/etc/httpd/conf.d
install -m 644  colplot-apache.conf   $RPM_BUILD_ROOT/etc/httpd/conf.d/colplot.conf
perl -pi -e 's|/var/www/html/|/var/www/|g' $RPM_BUILD_ROOT/etc/httpd/conf.d/colplot.conf
mkdir -p $RPM_BUILD_ROOT/var/www/colplot
install -m 755 colplot $RPM_BUILD_ROOT/var/www/colplot/index.cgi
install -m 644 colplot-help.html FAQ-colgui.html FAQ-colplot.html $RPM_BUILD_ROOT/var/www/colplot/

%files
%defattr(-,root,root)
%doc FAQ*html README RELEASE-* INSTALL-colplot colplot-help.html
%dir /usr/share/collectl/
%dir /usr/share/collectl/plotfiles
%dir /usr/share/collectl/util
%config(noreplace) /etc/colplot.conf
/usr/bin/colgui
/usr/bin/colmux
/usr/bin/colplot
/usr/share/collectl/colplotlib.ph
/usr/share/collectl/colplotlib.defs
/usr/share/collectl/plotfiles/*
/usr/share/collectl/util/genplotfiles
/usr/share/man/man1/*

%files web
%defattr(-,root,root)
/etc/httpd/conf.d/colplot.conf
/var/www/colplot

%changelog
* Tue Jan 04 2011 Mark Seger
- change version/release format
* Fri Nov 19 2010 Mark Seger
- changed directory structure to match collectl
* Tue Dec 15 2009 Mark Seger
- changed directory structure to match collectl
* Fri Aug 21 2009 Mark Seger
- Open Source release
* Fri Jul 10 2009 Mark Seger
- Removed col2tlviz since now part of collectl
* Mon Nov 19 2007 Mark Seger
- Renamed colplot.conf to colplot-apache.conf to avoid confusion
* Tue Jul 17 2007 Mark Seger
- Added 'BuildArch: noarch'
- Put 'colplot' apache stanza into include directory rather than httpd.conf
* Thu Dec 7 2006 Mark Seger
- new directory structure
* Mon Nov 28 2005 Mark Seger
- cleanup
- support for colgui requires removing prerequisite for perk-tk
* Mon Oct 10 2005 Mark Seger
- created

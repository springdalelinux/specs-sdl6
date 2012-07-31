Name:       wv
Summary:    MSWord 6/7/8/9 binary file format to HTML converter
Version:    1.2.7
Release:    2%{?dist}
License:    GPLv2+
Group:      Applications/Text
URL:        http://wvware.sourceforge.net
Source:     http://dl.sourceforge.net/wvware/wv-%{version}.tar.gz

BuildRequires: glib2-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libxml2-devel
BuildRequires: ImageMagick-devel
BuildRequires: pkgconfig
BuildRequires: libgsf-devel >= 1.11.2
Provides:   wvware = %{version}-%{release}

%description
Wv is a program that understands the Microsoft Word 6/7/8/9
binary file format and is able to convert Word
documents into HTML, which can then be read with a browser.


%package        devel
Summary:        MSWord format converter - development files
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
Wv is a program that understands the Microsoft Word 6/7/8/9
binary file format and is able to convert Word
documents into HTML, which can then be read with a browser.
This package contains the development files


%prep
%setup -q
sed -i 's/^LT_CURRENT=`expr $WV_MICRO_VERSION - $WV_INTERFACE_AGE`/LT_CURRENT=3/' configure

%build
%configure --disable-static

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{_libdir} -name "*.la" -exec rm -f {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%doc COPYING README
%{_bindir}/wv*
%{_datadir}/wv
%{_mandir}/man1/*
%{_libdir}/libwv*.so.*

%files      devel
%defattr(-,root,root)
%{_includedir}/wv
%{_libdir}/libwv*.so
%{_libdir}/pkgconfig/*


%changelog
* Tue Dec 22 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 1.2.7-2
- Workaround a incorrect soname bump

* Fri Dec 11 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 1.2.7-1
- New upstream release that fixes a regression
- Resolves rhbz#546406,546406

* Sun Nov 29 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 1.2.6-1
- Changelog at rhbz#511221

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 12 2009 Caolán McNamara <caolanm@redhat.com> - 1.2.4-5
- rebuild to get provides pkgconfig(wv-1.0) >= 0:1.2.0

* Sun Mar 30 2008 Michel Salim <michel.sylvan@gmail.com> - 1.2.4-4
- fix libdir in wv's pkgconfig entry

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.4-3
- Autorebuild for GCC 4.3

* Sun Aug 26 2007 Aurelien Bompard <abompard@fedoraproject.org> 1.2.4-2
- fix license tag
- rebuild for BuildID

* Sat Oct 28 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.2.4-1
- update to 1.2.4, fixes #212696 (CVE-2006-4513)

* Fri Sep 08 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.2.1-7
- rebuild (releases 1 to 7, cvs problem)

* Fri Sep 08 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.2.1-1
- version 1.2.1

* Fri Apr 14 2006 Aurelien Bompard <gauret[AT]free.fr> 1.2.0-4
- rebuild

* Wed Feb 22 2006 Aurelien Bompard <gauret[AT]free.fr> 1.2.0-3
- don't build the static lib

* Tue Feb 21 2006 Aurelien Bompard <gauret[AT]free.fr> 1.2.0-2
- rebuild for FC5

* Fri Nov 11 2005 Aurelien Bompard <gauret[AT]free.fr> 1.2.0-1
- version 1.2.0

* Fri Oct 28 2005 Aurelien Bompard <gauret[AT]free.fr> 1.0.3-2
- split out a -devel package (#171962)

* Sun May 15 2005 Aurelien Bompard <gauret[AT]free.fr> 1.0.3-1%{?dist}
- new version
- fix build with gcc4
- use dist tag

* Tue May 10 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.0.0-5
- Include printf format fix for bug 150461.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Wed Jul 28 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.0-0.fdr.3
- fix security vulnerability (CAN-2004-0645)

* Fri May 14 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.0-0.fdr.2
- add several patches
- depend on glib2 (bug 1592)

* Wed May 12 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.0-0.fdr.1
- initial RPM (from Mandrake)

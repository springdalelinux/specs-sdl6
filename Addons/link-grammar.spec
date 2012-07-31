Summary: A Grammar Checking library
Name: link-grammar
Version: 4.6.7
Release: 3%{?dist}
Group: System Environment/Libraries
License: BSD
Source: http://www.abisource.com/downloads/link-grammar/%{version}/link-grammar-%{version}.tar.gz
URL: http://abisource.com/projects/link-grammar/
BuildRequires: aspell-devel, java-devel, jpackage-utils, libedit-devel, ant

%description
A library that can perform grammar checking.

%package devel
Summary: Support files necessary to compile applications with liblink-grammar
Group: Development/Libraries
Requires: link-grammar = %{version}-%{release}

%description devel
Libraries, headers, and support files needed for using liblink-grammar.

%package java
Summary: Java libraries for liblink-grammar
Group: Development/Libraries
Requires: java >= 1:1.6.0
Requires: jpackage-utils
Requires: link-grammar = %{version}-%{release}

%description java
Java libraries for liblink-grammar

%package java-devel
Summary: Support files necessary to compile Java applications with liblink-grammar
Group: Development/Libraries
Requires: link-grammar-java = %{version}-%{release}
Requires: link-grammar-devel = %{version}-%{release}

%description java-devel
Libraries for developing Java components using liblink-grammar.

%prep
%setup -q

%build
%configure --disable-static --enable-pthreads
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make
# currently the build system can not handle smp_flags properly
# make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README ChangeLog
%{_bindir}/*
%{_libdir}/liblink-grammar.so.*
%{_datadir}/link-grammar
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/liblink-grammar.so
%{_libdir}/pkgconfig/link-grammar.pc
%{_includedir}/link-grammar

%files java
%defattr(-,root,root,-)
%{_libdir}/liblink-grammar-java.so.*
%{_javadir}/linkgrammar*.jar

%files java-devel
%defattr(-,root,root,-)
%{_libdir}/liblink-grammar-java.so

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post java -p /sbin/ldconfig
%postun java -p /sbin/ldconfig

%changelog
* Fri May 28 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 4.6.7-3
- fix BuildRequires

* Fri May 28 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 4.6.7-2
- have the java-devel package Require the -devel package

* Fri May 28 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 4.6.7-1
- update to 4.6.7
- drop static libs
- get rid of rpath
- fix man page ownership
- add java subpackages
- fix defattr invocations

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4.3.5-3
- fix license tag

* Thu Jul 10 2008 Marc Maurer <uwog@abisource.com> 4.3.5-2
- Move the man-page from -devel to the main package

* Thu Jul 10 2008 Marc Maurer <uwog@abisource.com> 4.3.5-1
- New upstream version, fixes bug 434650
- Update URL
- Package man-page

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.2.5-2
- Autorebuild for GCC 4.3

* Mon Nov 12 2007 Marc Maurer <uwog@uwog.net> 4.2.5-1
- New upstream version, fixes bug 371221.

* Mon Sep 11 2006 Marc Maurer <uwog@abisource.com> 4.2.2-2.fc6
- Rebuild for FC6

* Wed Apr 12 2006 Marc Maurer <uwog@abisource.com> 4.2.2-1
- New upstream version

* Mon Apr 10 2006 Marc Maurer <uwog@abisource.com> 4.2.1-2
- Rebuild

* Mon Apr 10 2006 Marc Maurer <uwog@abisource.com> 4.2.1-1
- New upstream version

* Wed Feb 15 2006 Marc Maurer <uwog@abisource.com> 4.1.3-4
- Rebuild for Fedora Extras 5
- Use %%{?dist} in the release name

* Wed Aug 10 2005 Marc Maurer <uwog@abisource.com> - 4.1.3-3
- Set the buildroot to the standard Fedora buildroot
- Make the package own the %%{_datadir}/link-grammar
  directory (thanks go to Aurelien Bompard for both issues)

* Wed Aug 10 2005 Marc Maurer <uwog@abisource.com> - 4.1.3-2
- Remove epoch
- Make rpmlint happy

* Sun Aug 7 2005 Marc Maurer <uwog@abisource.com> - 1:4.1.3-1
- Initial version

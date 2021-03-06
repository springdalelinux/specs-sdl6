Name:		libjpeg-turbo
Version:	1.1.1
Release:	1.1%{?dist}
Summary:	A MMX/SSE2 accelerated library for manipulating JPEG image files

Group:		System Environment/Libraries
License:	wxWidgets
URL:		http://sourceforge.net/projects/libjpeg-turbo
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	autoconf, automake, libtool
%ifarch %{ix86} x86_64
BuildRequires:	nasm
%endif

# moved this from -utils, in an attempt to get it to better override
# libjpeg in rawhide -- Rex
#Obsoletes:	libjpeg < 6b-47
# add provides (even if it not needed) to workaround bad packages, like
# java-1.6.0-openjdk (#rh607554) -- atkac
#Provides:	libjpeg = 6b-47

Patch0:		libjpeg-turbo11-noinst_jpgtest.patch

%description
The libjpeg-turbo package contains a library of functions for manipulating
JPEG images

%package devel
Summary:	Headers for the libjpeg-turbo library
Group:		Development/Libraries
#Obsoletes:	libjpeg-devel < 6b-47
#Provides:	libjpeg-devel = 6b-47
%if "%{?_isa}" != ""
#Provides:	libjpeg-devel%{_isa} = 6b-47
%endif
Requires:	libjpeg-turbo%{?_isa} = %{version}-%{release}

%description devel
This package contains header files necessary for developing programs which
will manipulate JPEG files using the libjpeg-turbo library

%package utils
Summary:	Utilities for manipulating JPEG images
Group:		Applications/Multimedia
Requires:	libjpeg-turbo%{?_isa} = %{version}-%{release}

%description utils
The libjpeg-turbo-utils package contains simple client programs for
accessing the libjpeg functions. It contains cjpeg, djpeg, jpegtran,
rdjpgcom and wrjpgcom. Cjpeg compresses an image file into JPEG format.
Djpeg decompresses a JPEG file into a regular image file. Jpegtran
can perform various useful transformations on JPEG files. Rdjpgcom
displays any text comments included in a JPEG file. Wrjpgcom inserts
text comments into a JPEG file.

%package static
Summary:	Static version of the libjpeg-turbo library
Group:		Development/Libraries
#Obsoletes:	libjpeg-static < 6b-47
#Provides:	libjpeg-static = 6b-47
%if "%{?_isa}" != ""
#Provides:	libjpeg-static%{_isa} = 6b-47
%endif
Requires:	libjpeg-turbo-devel%{_isa} = %{version}-%{release}

%description static
The libjpeg-turbo-static package contains static library for manipulating
JPEG images

%prep
%setup -q

%patch0 -p1 -b .noinst_jpgtest

%build
autoreconf -fiv
%ifarch x86_64
export CFLAGS="-fPIC -DPIC %{optflags}"
%endif
%configure

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Fix perms
chmod -x README-turbo.txt

# Remove unwanted files
rm -f $RPM_BUILD_ROOT/%{_libdir}/lib{,turbo}jpeg.la

# Don't distribute libjpegturbo because it is unversioned
#rm -f $RPM_BUILD_ROOT/%{_includedir}/turbojpeg.h
#rm -f $RPM_BUILD_ROOT/%{_libdir}/libturbojpeg.{so,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README README-turbo.txt change.log ChangeLog.txt LGPL.txt LICENSE.txt
%{_libdir}/libjpeg.so.62.0.0
%{_libdir}/libjpeg.so.62
%{_libdir}/libturbojpeg.so

%files devel
%defattr(-,root,root,-)
%doc coderules.txt jconfig.txt libjpeg.txt structure.txt example.c
%{_includedir}/jconfig.h
%{_includedir}/jerror.h
%{_includedir}/jmorecfg.h
%{_includedir}/jpeglib.h
%{_includedir}/turbojpeg.h
%{_libdir}/libjpeg.so

%files utils
%defattr(-,root,root,-)
%doc usage.txt wizard.txt
%{_bindir}/cjpeg
%{_bindir}/djpeg
%{_bindir}/jpegtran
%{_bindir}/rdjpgcom
%{_bindir}/wrjpgcom
%{_mandir}/man1/cjpeg.1*
%{_mandir}/man1/djpeg.1*
%{_mandir}/man1/jpegtran.1*
%{_mandir}/man1/rdjpgcom.1*
%{_mandir}/man1/wrjpgcom.1*

%files static
%defattr(-,root,root,-)
%{_libdir}/libjpeg.a
%{_libdir}/libturbojpeg.a

%changelog
* Mon Jul 11 2011 Adam Tkac <atkac redhat com> 1.1.1-1
- update to 1.1.1
  - ljt11-rh688712.patch merged

* Tue Mar 22 2011 Adam Tkac <atkac redhat com> 1.1.0-2
- handle broken JPEGs better (#688712)

* Tue Mar 01 2011 Adam Tkac <atkac redhat com> 1.1.0-1
- update to 1.1.0

* Mon Jan 17 2011 Adam Tkac <atkac redhat com> 1.0.90-1
- update to 1.0.90
- libjpeg-turbo10-rh639672.patch merged

* Fri Oct 29 2010 Adam Tkac <atkac redhat com> 1.0.1-3
- add support for arithmetic coded files into decoder (#639672)

* Wed Sep 29 2010 jkeating - 1.0.1-1.1
- Rebuilt for gcc bug 634757

* Mon Sep 13 2010 Adam Tkac <atkac redhat com> 1.0.1-1
- update to 1.0.1
  - libjpeg-turbo10-rh617469.patch merged
- add -static subpkg (#632859)

* Wed Aug 04 2010 Adam Tkac <atkac redhat com> 1.0.0-3
- fix huffman decoder to handle broken JPEGs well (#617469)

* Fri Jul 02 2010 Adam Tkac <atkac redhat com> 1.0.0-2
- add libjpeg-devel%%{_isa} provides to -devel subpkg to satisfy imlib-devel
  deps

* Fri Jul 02 2010 Adam Tkac <atkac redhat com> 1.0.0-1
- update to 1.0.0
- patches merged
  - libjpeg-turbo-programs.patch
  - libjpeg-turbo-nosimd.patch
- add libjpeg provides to the main package to workaround problems with broken
  java-1.6.0-openjdk package

* Fri Jul 02 2010 Adam Tkac <atkac redhat com> 0.0.93-13
- remove libjpeg provides from -utils subpkg

* Wed Jun 30 2010 Rex Dieter <rdieter@fedoraproject.org> 0.0.93-12
- move Obsoletes: libjpeg to main pkg

* Wed Jun 30 2010 Rex Dieter <rdieter@fedoraproject.org> 0.0.93-11
- -utils: Requires: %%name ...

* Wed Jun 30 2010 Adam Tkac <atkac redhat com> 0.0.93-10
- add Provides = libjpeg to -utils subpackage

* Mon Jun 28 2010 Adam Tkac <atkac redhat com> 0.0.93-9
- merge review related fixes (#600243)

* Wed Jun 16 2010 Adam Tkac <atkac redhat com> 0.0.93-8
- merge review related fixes (#600243)

* Mon Jun 14 2010 Adam Tkac <atkac redhat com> 0.0.93-7
- obsolete -static libjpeg subpackage (#600243)

* Mon Jun 14 2010 Adam Tkac <atkac redhat com> 0.0.93-6
- improve package description a little (#600243)
- include example.c as %%doc in the -devel subpackage

* Fri Jun 11 2010 Adam Tkac <atkac redhat com> 0.0.93-5
- don't use "fc12" disttag in obsoletes/provides (#600243)

* Thu Jun 10 2010 Adam Tkac <atkac redhat com> 0.0.93-4
- fix compilation on platforms without MMX/SSE (#600243)

* Thu Jun 10 2010 Adam Tkac <atkac redhat com> 0.0.93-3
- package review related fixes (#600243)

* Wed Jun 09 2010 Adam Tkac <atkac redhat com> 0.0.93-2
- package review related fixes (#600243)

* Fri Jun 04 2010 Adam Tkac <atkac redhat com> 0.0.93-1
- initial package

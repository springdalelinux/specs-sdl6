Name: blitz
Version: 0.9
Release: 13%{?dist}
Summary: C++ class library for matrix scientific computing

Group: Development/Libraries
License: GPLv2
URL: http://www.oonumerics.org/blitz
Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0: blitz-gcc43.patch
Buildroot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description
Blitz++ is a C++ class library for scientific computing which provides 
performance on par with Fortran 77/90. It uses template techniques to achieve 
high performance. Blitz++ provides dense arrays and vectors, random number 
generators, and small vectors

%package devel
Summary: Libraries, includes, etc. used to develop an application with %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
%description devel
This are the header files and libraries needed to develop a %{name}
application

%package doc
Summary: The Blitz html docs
Group: Documentation
BuildArch: noarch

%description doc
HTML documentation files for the Blitz Library

%prep
%setup -q
%patch0 -p1

%build
%configure --enable-shared --disable-static --disable-fortran \
    --disable-dependency-tracking --disable-cxx-flags-preset
make %{?_smp_mflags}
# blitz.pc is created directly by configure
# I use sed to add %%libdir/blitz to the include directories of the library
# so that different bzconfig.h can be installed for different archs
%{__sed} -i -e "s/Cflags: -I\${includedir}/Cflags: -I\${includedir} -I\${libdir}\/blitz\/include/" blitz.pc

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{_libdir}/blitz/include/blitz
mv %{buildroot}%{_includedir}/blitz/gnu %{buildroot}%{_libdir}/blitz/include/blitz
rm -rf doc/doxygen/html/installdox
# There are some empty files in doc, remove before copying in doc
(find -empty | xargs rm)
# Put in doc only the source code
rm -rf examples/.deps
rm -rf examples/Makefile*

# Check fails with gcc 4.3 and ppc
# Removed for the moment
#%check
#make %{?_smp_mflags} check-testsuite

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%preun devel
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi


%files
%defattr(-,root,root,-)
%doc AUTHORS LEGAL COPYING README LICENSE
%{_libdir}/*so.*

%files devel
%defattr(-,root,root,-)
%doc examples
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_libdir}/blitz
%{_includedir}/*
%{_infodir}/*
%exclude %{_libdir}/*.la
%exclude %{_infodir}/dir
%exclude %{_libdir}/pkgconfig/blitz-uninstalled.pc

%files doc
%defattr(-,root,root,-)
%doc doc/{blitz.pdf,blitz.html,blitz_abt.html,blitz_fot.html,blitz_ovr.html,blitz_toc.html,blitz_1.html,blitz_2.html,blitz_3.html,blitz_4.html,blitz_5.html,blitz_6.html,blitz_7.html,blitz_8.html,blitz_9.html,blitz_10.html,blitz_11.html,blitz_12.html,blitz_13.html,blitz_14.html,blitz_15.html,blitz_16.html,indirect.gif,slice.gif,strideslice.gif,sinsoid.gif,tensor1.gif,blitz.gif,blitztiny.jpg}

%changelog
* Tue Dec 22 2009 Sergio Pascual <sergiopr at fedoraproject.org> - 0.9-13
- Using pregenerated documentation

* Sun Jul 26 2009 Sergio Pascual <sergiopr at fedoraproject.org> - 0.9-12
- Noarch doc subpackage

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May  7 2009 Ville Skyttä <ville.skytta at iki.fi> - 0.9-10
- Build with $RPM_OPT_FLAGS.
- Disable autotools dependency tracking during build for cleaner build logs
  and possible slight build speedup.

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 20 2009 Sergio Pascual <sergiopr at fedoraproject.org> - 0.9-8
- New patch (from upstream) to build with gcc4.3 

* Mon Mar 03 2008 Sergio Pascual <spr@astrax.fis.ucm.es> - 0.9-7
- Patch to build with gcc4.3

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9-6
- Autorebuild for GCC 4.3

* Mon Jan 07 2008 Sergio Pascual <spr@astrax.fis.ucm.es> 0.9-5
- Excluding /usr/share/info/dir

* Sat Dec 22 2007 Sergio Pascual <sergiopr at fedoraproject.com> 0.9-4
- Removed conflicting Makefiles from examples (bug #340751)
- Arch dependent gnu/bzconfig.h moved to %%libdir/blitz/include/blitz/gnu

* Wed Oct 17 2007 Sergio Pascual <spr@astrax.fis.ucm.es> 0.9-3
- Removed macro in changelog

* Tue Oct 16 2007 Sergio Pascual <spr@astrax.fis.ucm.es> 0.9-2
- Excluding /usr/share/info/dir

* Wed Oct 03 2007 Sergio Pascual <spr@astrax.fis.ucm.es> 0.9-1
- Changed wrong date in changelog
- Changed license to gplv2 (some .h files haven't got the license text)
- Changed _datadir/info/* to _infodir/%%{name}*

* Thu Oct 02 2007 Sergio Pascual <spr@astrax.fis.ucm.es> 0.9-0.2
- Adding requires pkgconfig
- Changed license tag
- Removing requires(pre,un)

* Thu May 03 2007 Sergio Pascual <spr@astrax.fis.ucm.es> 0.9-0.1
- Initial RPM file

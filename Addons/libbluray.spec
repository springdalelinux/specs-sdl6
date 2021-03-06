%global snapshot 0
%global tarball_date 20111023
%global git_hash e037110f11e707e223b715f70920913afecfe297
%global git_short %(echo '%{git_hash}' | cut -c -13)

Name:           libbluray
Version:        0.2.1
%if %{snapshot}
Release:        0.7.%{tarball_date}git%{git_short}%{?dist}
%else
Release:        1%{?dist}
%endif
Summary:        Library to access Blu-Ray disks for video playback 
Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.videolan.org/developers/libbluray.html
%if %{snapshot}
# Use the commands below to generate a tarball.
# git clone git://git.videolan.org/libbluray.git
# cd libbluray
# git archive --format=tar %{git_hash} --prefix=libbluray/ | bzip2 > ../libbluray-$( date +%Y%m%d )git%{git_short}.tar.bz2
Source0:        %{name}-%{tarball_date}git%{git_short}.tar.bz2
%else
Source0:        ftp://ftp.videolan.org/pub/videolan/%{name}/%{version}/%{name}-%{version}.tar.bz2
%endif
# Fixed upstream, will not be needed for next upstream release
Source1:        libbluray-0.2.1-bdj_build.xml
Source2:        libbluray-0.2.1-bdj_java_subdir.tar.bz2
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%if %{snapshot}
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
%endif
%ifnarch ppc64
BuildRequires:  java-1.6.0-devel
BuildRequires:  jpackage-utils
BuildRequires:  ant
%endif
BuildRequires:  libxml2-devel
BuildRequires:  doxygen
BuildRequires:  texlive-latex
BuildRequires:  graphviz


%description
This package is aiming to provide a full portable free open source bluray
library, which can be plugged into popular media players to allow full bluray
navigation and playback on Linux. It will eventually be compatible with all
current titles, and will be easily portable and embeddable in standard players
such as mplayer and vlc.


%ifnarch ppc64
%package        java
Summary:        BDJ support for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       java-1.6.0
Requires:       jpackage-utils

%description    java
The %{name}-java package contains the jar file needed to add BDJ support to
%{name}.
%endif


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%if %{snapshot}
%setup -q -n %{name}
%else
%setup -q
install -Dp -m 644 %{SOURCE1} src/libbluray/bdj/build.xml
tar xjf %{SOURCE2}
%endif


%build
%if %{snapshot}
autoreconf -vif
%endif
%configure --disable-static \
           --enable-examples \
%ifnarch ppc64
           --enable-bdjava --with-jdk=%{_jvmdir}/java-1.6.0
%endif

make %{?_smp_mflags}
make doxygen-pdf
# Remove uneeded script
rm doc/doxygen/html/installdox


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%ifnarch ppc64
# Install BD-J jar
install -Dp -m 644 src/.libs/libbluray.jar  $RPM_BUILD_ROOT%{_javadir}/libbluray.jar
%endif

# Install test utilities
for i in clpi_dump index_dump mobj_dump mpls_dump sound_dump
do install -Dp -m 0755 src/examples/$i $RPM_BUILD_ROOT%{_bindir}/$i; done;
for i in bd_info bdsplice hdmv_test libbluray_test list_titles 
do install -Dp -m755 src/examples/.libs/$i %{buildroot}%{_bindir}/$i; done
%ifnarch ppc64
install -Dp -m755 src/examples/.libs/bdj_test %{buildroot}%{_bindir}/bdj_test;
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING player_wrappers README.txt
%{_libdir}/*.so.*
%{_bindir}/*


%ifnarch ppc64
%files java
%defattr(-,root,root,-)
%{_javadir}/libbluray.jar
%endif


%files devel
%defattr(-,root,root,-)
%doc doc/doxygen/html doc/doxygen/libbluray.pdf
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libbluray.pc


%changelog
* Thu Dec 01 2011 Xavier Bachelot <xavier@bachelot.org> 
- First upstream official release.
- Fix BD-J build (missing files in upstream tarball).
- Have subpackages require an arch-specific base package.

* Sun Oct 23 2011 Xavier Bachelot <xavier@bachelot.org> 0.2-0.7.20111023gite037110f11e70
- Update to latest snapshot.

* Sat Jul 16 2011 Xavier Bachelot <xavier@bachelot.org> 0.2-0.6.20110710git51d7d60a96d06
- Don't build java subpackage on ppc64, no java-1.6.0-devel package.

* Sun Jul 10 2011 Xavier Bachelot <xavier@bachelot.org> 0.2-0.5.20110710git51d7d60a96d06
- Update to latest snapshot.

* Sat May 14 2011 Xavier Bachelot <xavier@bachelot.org> 0.2-0.4.20110514git46ee2766038e9
- Update to latest snapshot.
- Drop -static subpackage.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-0.3.20110126gitbbf11e43bd82e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Xavier Bachelot <xavier@bachelot.org> 0.2-0.2.20110126gitbbf11e43bd82e
- Update to latest snapshot.
- Split the BDJ support to a -java subpackage.

* Fri Jan 07 2011 Xavier Bachelot <xavier@bachelot.org> 0.2-0.1.20110107git0e5902ff9a6f1
- Update to latest snapshot.
- Add BR: libxml2-devel for metadata parser.
- Add BR: graphviz for doc generation.

* Thu Oct 28 2010 Xavier Bachelot <xavier@bachelot.org> 0.1-0.3.20101028gitc32862b77dea4
- Update to latest snapshot.
- Install BDJ jar.

* Thu Oct 21 2010 Xavier Bachelot <xavier@bachelot.org> 0.1-0.2.20101021git144a204c02687
- Fix release tag.
- Update to latest snapshot.

* Thu Aug 19 2010 Xavier Bachelot <xavier@bachelot.org> 0.1-0.1.20100819
- Initial Fedora release.

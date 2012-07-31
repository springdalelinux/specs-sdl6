
## build options
# experimental, off, for now -- Rex
%define _with_NTL --with-NTL

%define multilib_arches %{ix86} x86_64 ppc ppc64 s390 s390x sparcv9 sparc64

Summary: C++ class library for multivariate polynomial data
Name:    factory
Version: 3.1.3
Release: 1%{?dist}

License: GPLv2 or GPLv3
URL:	 http://www.mathematik.uni-kl.de/ftp/pub/Math/Singular/Factory/
Source0: http://www.mathematik.uni-kl.de/ftp/pub/Math/Singular/Factory/factory-3-1-3.tar.gz
Group:   System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source1: factoryconf.h

# -debuginfo useless for (only) static libs
%define debug_package   %{nil}

BuildRequires: bison
BuildRequires: gmp-devel
%{?_with_NTL:BuildRequires: ntl-devel}

%description
Factory is a C++ class library that implements a recursive representation
of multivariate polynomial data.

%package devel 
Summary: C++ class library for multivariate polynomial data 
Group:   Development/Libraries
Requires: gmp-devel
Obsoletes: %{name}-static < %{version}-%{release}
Provides:  %{name}-static = %{version}-%{release}
%description devel 
Factory is a C++ class library that implements a recursive representation
of multivariate polynomial data.


%prep
%setup -q -n factory-3-1-3
ln -s . factory

%build
%configure \
  --with-gmp \
  %{?_with_NTL}

# smp bustage?
make 


%install
rm -rf %{buildroot} 

# FAILS: make install DESTDIR=%{buildroot}
%makeinstall
mkdir %{buildroot}%{_includedir}/factory
pushd %{buildroot}%{_includedir}/factory
ln -s ../factoryconf* .
ln -s ../templates .
popd

%ifarch %{multilib_arches}
# hack to allow parallel installation of multilib factory-devel
mv  %{buildroot}%{_includedir}/factoryconf.h \
    %{buildroot}%{_includedir}/factoryconf-%{_arch}.h
install -p -m644 %{SOURCE1} %{buildroot}%{_includedir}/factoryconf.h
%endif


%clean
rm -rf %{buildroot} 


%files devel 
%defattr(-,root,root,-)
# FIXME: ping upstream 
#doc COPYING
%doc ChangeLog NEWS README
%{_libdir}/lib*.a
%{_includedir}/*


%changelog
* Tue Mar 16 2010 Rex Dieter <rdieter@fedoraproject.org> - 3.1.1-1
- factory-3-1-1
- enable NTL support

* Wed Jan 20 2010 Rex Dieter <rdieter@fedoraproject.org> - 3.1.0-5
- License: GPLv2 or GPLv3

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 01 2009 Rex Dieter <rdieter@fedoraproject.org> - 3.1.0-3
- s/i386/%%ix86/

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 13 2009 Rex Dieter <rdieter@fedoraproject.org> 3.1.0-1
- factory-3-1-0

* Fri Feb 13 2009 Rex Dieter <rdieter@fedoraproject.org> 3.0.4-2
- --enable-streamio

* Thu Oct 02 2008 Rex Dieter <rdieter@fedoraproject.org> 3.0.4-1
- factory-3.0.4

* Mon Sep 29 2008 Rex Dieter <rdieter@fedoraproject.org> 3.0.3-4
- multiarch fix (sparc)

* Thu Apr 03 2008 Rex Dieter <rdieter@fedoraproject.org> 3.0.3-3
- multiarch conflicts (#341091)

* Fri Feb 08 2008 Rex Dieter <rdieter@fedoraproject.org> 3.0.3-2 
- respin (gcc43)

* Tue Dec 18 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.0.3-1
- factory-3-0-3

* Tue Aug 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.0.2-1
- factory-3-0-2
- disable -debuginfo (static lib only)

* Sat Aug 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 2.0.5-12
- License: GPLv2
- -static -> -devel

* Mon Dec 18 2006 Rex Dieter <rdieter[AT]fedoraproject.org> 2.0.5-11
- -devel -> -static

* Mon Oct 02 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.0.5-10
- respin

* Mon Aug 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.0.5-9
- fc6 respin

* Tue Jul 25 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.0.5-8
- fc6 respin

* Tue Mar 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.0.5-7
- factory-2.0.5-gcc41.patch (#183258)

* Fri Feb 10 2006 Rex Dieter <rexdieter[AT]users.sf.net>
- fc5: gcc/glibc respin

* Thu May 26 2005 Jeremy Katz <katzj@redhat.com> - 2.0.5-6
- fix build on 64bit arches

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 2.0.5-5
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Wed Oct 06 2004 Rex Dieter <rexdieter at sf.net> 0:2.0.5-3
- (2nd try at) gcc34 patch

* Wed Oct 06 2004 Rex Dieter <rexdieter at sf.net> 0:2.0.5-0.fdr.2
- gcc34 patch

* Fri Oct 1 2004 Rex Dieter <rexdieter at sf.net> 0:2.0.5-0.fdr.1
- factory-2.0.5

* Mon Nov 17 2003 Rex Dieter <rexdieter at sf.net> 0:2.0.4-0.fdr.4.b
- update macros

* Fri Nov 14 2003 Rex Dieter <rexdieter at sf.net> 0:2.0.4-0.fdr.3.b
- document use of --disable-streamio

* Mon Oct 06 2003 Rex Dieter <rexdieter at sf.net> 0:2.0.4-0.fdr.2.b
- remove smp build.

* Mon Oct 06 2003 Rex Dieter <rexdieter at sf.net> 0:2.0.4-0.fdr.1.b
- -devel: Requires: gmp-devel
- remove extraneous cvs tags
- update macros for Fedora Core support

* Thu Sep 11 2003 Rex Dieter <rexdieter at sf.net> 0:2.0.4-0.fdr.0.b
- first try.
- no shared libs, but make (only) -devel package to signify it's purpose


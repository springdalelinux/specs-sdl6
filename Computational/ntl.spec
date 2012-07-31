
%define multilib_arches %{ix86} x86_64 ppc ppc64 s390 s390x sparcv9 sparc64

# define include static lib (else undef)
#define static 1

Summary: High-performance algorithms for vectors, matrices, and polynomials 
Name:    ntl 
Version: 5.5.2
Release: 1%{?dist}

License: GPLv2+
URL:     http://shoup.net/ntl/ 
Source0: http://shoup.net/ntl/ntl-%{version}.tar.gz
Group:   System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source1: multilib_template.h

BuildRequires: gmp-devel
BuildRequires: libtool

%description
NTL is a high-performance, portable C++ library providing data structures
and algorithms for arbitrary length integers; for vectors, matrices, and
polynomials over the integers and over finite fields; and for arbitrary
precision floating point arithmetic.

NTL provides high quality implementations of state-of-the-art algorithms for:
* arbitrary length integer arithmetic and arbitrary precision floating point
  arithmetic;
* polynomial arithmetic over the integers and finite fields including basic
  arithmetic, polynomial factorization, irreducibility testing, computation
  of minimal polynomials, traces, norms, and more;
* lattice basis reduction, including very robust and fast implementations of
  Schnorr-Euchner, block Korkin-Zolotarev reduction, and the new 
  Schnorr-Horner pruning heuristic for block Korkin-Zolotarev;
* basic linear algebra over the integers, finite fields, and arbitrary
  precision floating point numbers. 

%package devel 
Summary: Development files for %{name} 
Group:   Development/Libraries
Requires: %{name} = %{version}-%{release}
%description devel 
%{summary}.

%package static 
Summary: Static libraries for %{name}
Group:   Development/Libraries
Requires: %{name}-devel = %{version}-%{release}
#Requires: gmp-devel
%description static 
%{summary}.


%prep
%setup -q 


%build
pushd src
./configure \
  CC="%{__cc}" \
  CXX="%{__cxx}" \
  CFLAGS="%{optflags} -fPIC" \
  CXXFLAGS="%{optflags} -fPIC" \
  PREFIX=%{_prefix} \
  DOCDIR=%{_docdir} \
  INCLUDEDIR=%{_includedir} \
  LIBDIR=%{_libdir} \
  NTL_GMP_LIP=on \
  SHARED=on
popd

# not smp-safe
make -C src


%check
# skip by default, takes a *long, long, long* (days?) time -- Rex
%{?_with_check:make -C src check}


%install
rm -rf %{buildroot}

make -C src install \
  PREFIX=%{buildroot}%{_prefix} \
  DOCDIR=%{buildroot}%{_docdir} \
  INCLUDEDIR=%{buildroot}%{_includedir} \
  LIBDIR=%{buildroot}%{_libdir} 

# Unpackaged files
rm -rf %{buildroot}%{_docdir}/NTL
rm -f  %{buildroot}%{_libdir}/libntl.la
%if ! 0%{?static}
rm -f  %{buildroot}%{_libdir}/libntl.a
%endif

%ifarch %{multilib_arches}
# hack to allow parallel installation of multilib factory-devel
for header in NTL/config NTL/gmp_aux NTL/mach_desc  ; do
mv  %{buildroot}%{_includedir}/${header}.h \
    %{buildroot}%{_includedir}/${header}-%{_arch}.h
install -p -m644 %{SOURCE1} %{buildroot}%{_includedir}/${header}.h
sed -i \
  -e "s|@@INCLUDE@@|${header}|" \
  -e "s|@@PACKAGENAME@@|%{name}-devel|" \
  %{buildroot}%{_includedir}/${header}.h
done
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README doc/copying.txt 
%{_libdir}/libntl.so.0*

%files devel 
%defattr(-,root,root,-)
%doc doc/*
%{_includedir}/*
%{_libdir}/libntl.so

%if 0%{?static}
%files static
%defattr(-,root,root,-)
%{_libdir}/libntl.a
%endif


%changelog
* Fri Sep 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 5.5.2-1
- ntl-5.5.2

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 5.5-1
- ntl-5.5
- enable shared libs (and omit static lib)

* Fri Mar 20 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 5.4.2-7
- add -static virtual Provides to -devel package

* Mon Mar 02 2009 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-6
- s/i386/%%ix86/
- gcc44 patch

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 11 2008 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-4
- build -fPIC (#475254)

* Mon Sep 29 2008 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-3
- multilib fixes

* Thu Apr 03 2008 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-2
- multiarch conflicts (#342711)

* Tue Mar 11 2008 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-1
- ntl-5.4.2

* Fri Feb 08 2008 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-2 
- respin (gcc43)

* Tue Dec 08 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.4.1-1
- ntl-5.4.1

* Sat Aug 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.4-6
- License: GPLv2+
- -static -> -devel (revert previous change)

* Mon Dec 18 2006 Rex Dieter <rdieter[AT]fedoraproject.org> 5.4-5
- -devel -> -static

* Mon Aug 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.4-4
- fc6 respin

* Tue Jul 25 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.4-3
- fc6 respin

* Tue Apr 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.4-2
- Capitalize %%summary
- disable -debuginfo, includes no debuginfo'able bits 

* Fri Jan 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.4-1
- 5.4 (first try)



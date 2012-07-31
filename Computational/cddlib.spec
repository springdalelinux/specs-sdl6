%define debug_package %{nil}
# rpmbuild doesn't get useful debuginfo from .a libs, apparently

Name:           cddlib
Version:        094f
Release:        9%{?dist}
Summary:        A library for generating all vertices in convex polyhedrons
Group:          Applications/Engineering
License:        GPLv2+
URL:            http://www.ifor.math.ethz.ch/~fukuda/cdd_home/
#Source0:        ftp://ftp.ifor.math.ethz.ch/pub/fukuda/cdd/%{name}-094f.tar.gz
#tar -xzf cddlib-094f.tar.gz
#rm cddlib-094f/examples-ml/Combinatorica5.m
#tar -czf cddlib-094-free.tar.gz cddlib-094f/
Source0:        %{name}-094f-free.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  gmp-devel
BuildRequires:  texlive-latex


%description
The C-library cddlib is a C implementation of the Double Description 
Method of Motzkin et al. for generating all vertices (i.e. extreme points)
and extreme rays of a general convex polyhedron in R^d given by a system 
of linear inequalities:

   P = { x=(x1, ..., xd)^T :  b - A  x  >= 0 }

where A is a given m x d real matrix, b is a given m-vector 
and 0 is the m-vector of all zeros.

The program can be used for the reverse operation (i.e. convex hull
computation). This means that one can move back and forth between 
an inequality representation and a generator (i.e. vertex and ray) 
representation of a polyhedron with cdd. Also, cdd can solve a linear
programming problem, i.e. a problem of maximizing and minimizing 
a linear function over P.


%package devel
Summary: Header and static libraries for cddlib
Group: Development/Libraries
Requires: gmp-devel
Provides: %{name}-static = %{version}-%{release}

%description devel
Include files and static libraries for cddlib.


%prep
%setup -q
# Don't build/install the example programs
echo -e 'all:\ninstall:' > src/Makefile.in
echo -e 'all:\ninstall:' > src-gmp/Makefile.in
# Clean up the examples
rm -rf src/~
rm -rf src*/.DS_Store* src*/.gdb_history examples*/.DS_Store*
rm -rf src-gmp/~
chmod -x -R examples*/* src*/*
rm doc/cddlibman.pdf


%build
%configure
make %{?_smp_mflags}
cd doc
  pdflatex cddlibman.tex


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
mkdir $RPM_BUILD_ROOT%{_includedir}/cddlib
mv $RPM_BUILD_ROOT%{_includedir}/{cdd,cdd_f,cddmp,cddmp_f,cddtypes,cddtypes_f,setoper}.h \
  $RPM_BUILD_ROOT%{_includedir}/cddlib/


%clean
rm -rf $RPM_BUILD_ROOT


%files devel
%defattr(-,root,root,-)
%doc doc/cddlibman.pdf
%doc examples* src*
%{_includedir}/cddlib
%{_libdir}/libcdd.a
%{_libdir}/libcddgmp.a


%changelog
* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 094f-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 094f-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Nov 28 2008 Conrad Meyer <konrad@tylerc.org> - 094f-7
- Install headers with install -p to save timestamps.
- Install headers to namespaced directory.
- Generate pdf from latex source.

* Fri Oct 31 2008 Conrad Meyer <konrad@tylerc.org> - 094f-6
- Describe vividly the process whereby the non-free file is
  stripped from the source tarball.

* Thu Oct 30 2008 Conrad Meyer <konrad@tylerc.org> - 094f-5
- Tarball scrubbed of content we are unable to ship.

* Tue Oct 28 2008 Conrad Meyer <konrad@tylerc.org> - 094f-4
- Remove modules that do not meet licensing guidelines.
- Don't generate debuginfo.

* Tue Oct 28 2008 Conrad Meyer <konrad@tylerc.org> - 094f-3
- Fix permissions on documentation.

* Mon Oct 27 2008 Conrad Meyer <konrad@tylerc.org> - 094f-2
- Incorporate several suggestions from review.

* Thu Sep 25 2008 Conrad Meyer <konrad@tylerc.org> - 094f-1
- Initial package.

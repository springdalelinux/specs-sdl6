Name:		muParser
Summary:	A fast math parser library
Version:	1.32
Release:	1%{?dist}
BuildRequires:	dos2unix
URL:		http://muparser.sourceforge.net
License:	MIT
Group:          Development/Libraries
Source:		http://puzzle.dl.sourceforge.net/sourceforge/muparser/muparser_v132.tar.gz		
#Patch0:		muParser-244309.patch	
#Patch1:		muParser-1.28-gcc43.patch
Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%package devel
Summary:        Development and doc files for {%name}
Requires:       %{name} = %{version}-%{release} pkgconfig
Group:          Development/Libraries

%description
Many applications require the parsing of mathematical expressions.
The main objective of this project is to provide a fast and easy way
of doing this. muParser is an extensible high performance math parser
library. It is based on transforming an expression into a bytecode
and precalculating constant parts of it.

%description devel
Development files and the documentation

%prep
%setup -q -n muparser_v132
#%patch0 -p1
#%patch1 -p1

%build
%configure --enable-shared=yes --enable-debug=no --enable-samples=no
make CXXFLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags}
mv docs/html .
dos2unix *.txt
dos2unix html/sources/*
dos2unix html/script/*

%install
rm -rf $RPM_BUILD_ROOT
make libdir=$RPM_BUILD_ROOT%{_libdir} prefix=$RPM_BUILD_ROOT/usr install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc Changes.txt
%doc Credits.txt
%doc License.txt
%{_libdir}/libmuparser.so.0
%{_libdir}/libmuparser.so.0.0.0

%files devel
%{_includedir}/*
%doc html
%{_libdir}/libmuparser.so
%{_libdir}/pkgconfig/muparser.pc

%changelog
* Wed Feb 10 2010 Frank Büttner <frank-buettner@gmx.net> - 1.32-1
- update to 1.32

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Apr 08 2008 Jesse Keating <jkeating@redhat.com> - 1.28-4
- Fix the gcc4.3 errors.

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.28-3
- Autorebuild for GCC 4.3

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.28-2
- Rebuild for selinux ppc32 issue.

* Sat Jul 14 2007 Frank Büttner <frank-buettner@gmx.net> - 1.28-1
 - update to 1.28
* Fri Jun 15 2007 Frank Büttner <frank-buettner@gmx.net> - 1.27-5%{?dist}
 - fix bug #244309
* Fri Jun 08 2007 Frank Büttner <frank-buettner@gmx.net> - 1.27-4%{?dist}
 - fix depend on pkgconfig
* Wed Jun 06 2007 Frank Büttner <frank-buettner@gmx.net> - 1.27-3%{?dist}
 - clean build root before run install part
 - fix missing pkconfig file
* Thu May 17 2007 Frank Büttner <frank-buettner@gmx.net> - 1.27-2%{?dist}
  - fix missing post -p /sbin/ldconfig
  - fix the double doc files
  - fix missing compiler flags
  - fix wrong file encoding of the doc files
* Wed May 16 2007 Frank Büttner <frank-buettner@gmx.net> - 1.27-1%{?dist}
  - start

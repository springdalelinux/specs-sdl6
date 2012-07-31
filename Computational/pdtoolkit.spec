%ifarch %ix86
%define destdir linux
%endif
%ifarch x86_64
%define destdir x86_64
%endif

# this thing ships with some prebuilt binaries, therefore:
%undefine _missing_build_ids_terminate_build

# this is going to go under /usr/local
%define installdir /usr/local/pdtoolkit

%{!?modulefile_path: %define modulefile_path /usr/local/share/Modules/modulefiles/}
# type: string (subdir to install modulefile)
%{!?modulefile_subdir: %define modulefile_subdir pdtoolkit}

Name: pdtoolkit
Version: 3.17
Release: 1%{?dist}
Summary: The Program Database Toolkit
License: BSD-like
Group: Development/Tools
Url: http://www.cs.uoregon.edu/research/pdt/
Packager: Eugeny A. Rostovtsev (REAL) <real at altlinux.org>
Buildroot: %{_tmppath}/%{name}-%{version}-root

# originally extension of source archive was .tgz
Source: http://tau.uoregon.edu/pdt.tgz

Conflicts: tau < 2.18.1p1-alt4

BuildRequires: gcc-gfortran gcc-c++ redhat-lsb symlinks
BuildRequires: intel-compilerpro12-modules-devel >= 12.1.7.256

%description
The Program Database Toolkit (PDT) is a tool infrastructure that provides
access to the high-level interface of source code for analysis tools and
applications.  Currently, the toolkit consists of the C/C++ and Fortran 77/90/95
IL (Intermediate Language) Analyzers, and DUCTAPE (C++ program Database 
Utilities and Conversion Tools APplication Environment) library and applica-
tions.  The EDG C++ (or Mutek Fortran 90) Front End first parses a source 
file, and produces an intermediate language file.  The appropriate IL 
Analyzer processes this IL file, and creates a "program database" (PDB) file 
consisting of the high-level interface of the original source.  Use of the 
DUCTAPE library then makes the contents of the PDB file accessible to 
applications. This release also includes the Flint F95 parser from Cleanscape 
Inc.

This rpm contains shared files.

%package gcc
Summary: PDT gcc files
Group: Development/Tools

%description gcc
PDF gcc files

%package intel
Summary: PDT intel files
Group: Development/Tools

%description intel
PDF intel files

%package doc
Summary: Documentation for PDT
Group: Development/Documentation
BuildArch: noarch

%description doc
Documentation for PDT.

#%package libs
#Summary: Shared library of PDT
#Group: System/Libraries
#
#%description libs
#Shared library of PDT.

%package libs-devel
Summary: Development files of PDT
Group: Development/Other
Requires: %{name}-libs = %{version}-%{release}

%description libs-devel
Development files of PDT.

%package libs-static
Summary: Static library of PDT
Group: Development/Other
Requires: libs-devel = %{version}-%{release}

%description libs-static
Static library of PDT.

%package -n pdbsql
Summary: PDB files as a relational database
Group: Development/Databases
BuildArch: noarch
Requires: %{name} = %{version}-%{release}
Requires: sqlite

%description -n pdbsql
The pdbsql package includes two important pieces:

 - An SQLite schema that represents PDB files as a relational database.
 - A Perl script for converting PDB 3.0 files to the SQLite form.

The goal of this package is to allow users to write code that consumes
data contained within PDB files in a wider set of languages than
currently provided by the C++ Ductape API alone.  Any language that
has a binding to SQLite can use this method of accessing PDB data.
Furthermore, the use of SQL to construct queries on the data removes
the need for the user to explicitly code up the query by combining STL
data structures, iterators, and query-specific logic.  This also means
that general purpose user interface tools for accessing the data in
the database can traverse the PDB data using the standard SQL language.

%prep
%setup -c 
mkdir tempbin
cat > tempbin/lsb_release <<ENDLSB
if [ "x\$1" = "x-is" ]; then
	echo "RedHat Enterprise"
else
	/usr/bin/lsb_release \$1
fi
ENDLSB
chmod +x tempbin/lsb_release
for c in gcc intel; do
	cp -ar %{name}-%{version} $c
done

%build
export PATH="`pwd`/tempbin:$PATH"
pushd gcc
TARGET=`pwd`/built-gcc
./configure \
	-useropt='-O2' \
	-GNU \
	-prefix=$TARGET \
	-compdir=gcc
make
popd
pushd intel
TARGET=`pwd`/built-intel
. /etc/profile.d/modules.sh
module load intel
./configure \
	-useropt='-O2' \
	-ICPC \
	-prefix=$TARGET \
	-compdir=intel
make
popd

%install
for c in gcc intel; do
pushd $c
TARGET=`pwd`/built-$c
make install
if [ $c = "gcc" ]; then
	pushd ductape/inc
	PATH=$PATH:$TARGET/%destdir/$c/bin ./MakeHtmlDocu
	popd
fi


rm contrib/pdbsql/sqlite-3.5.6.tar.gz -f
pushd $TARGET
# fix up symlinks
symlinks -cr %destdir
rm -f craycnl xt3
ln -s %destdir craycnl
ln -s %destdir xt3
# fix up paths
perl -pi -e "s|$TARGET|%installdir|g" .last_config  .all_configs %destdir/$c/bin/*parse contrib/rose/roseparse/roseparse contrib/rose/roseparse/upcparse
sed -i '1s|/sh|/bash|' %destdir/$c/bin/gfparse
rm -f %destdir/$c/bin/gfortran
popd

if [ $c = "gcc" ]; then
	mkdir -p %buildroot/%{installdir}/docs
	cp -fR ductape/html doc/* README %buildroot/%{installdir}/docs/
	mv $TARGET/* %buildroot/%{installdir}/

	install -d %buildroot%_datadir/pdbsql
	install -d %buildroot%perl_vendorlib/pdbSql
	mv contrib/pdbsql/pdbSql.pm %buildroot%perl_vendorlib/pdbSql
	install -p -m644 contrib/pdbsql/* %buildroot%_datadir/pdbsql
else
	mv $TARGET/%destdir/$c %buildroot/%{installdir}/%destdir/
fi

mkdir -p $RPM_BUILD_ROOT/%{modulefile_path}/%{modulefile_subdir}/$c
cat > $RPM_BUILD_ROOT/%{modulefile_path}/%{modulefile_subdir}/$c/%{version} <<ENDVERSION
#%Module

# NOTE: This is an automatically-generated file!  (generated by the
# %{modulefile_subdir}).  Any changes made here will be lost a) if the RPM is
# uninstalled, or b) if the RPM is upgraded or uninstalled.

proc ModulesHelp { } {
   puts stderr "This module adds %{modulefile_subdir} $c %{version} to various paths"
}

module-whatis   "Sets up %{modulefile_subdir} $c %{version} in your environment"
 
prepend-path PATH "%{installdir}/%destdir/$c/bin"
append-path -d { } LOCAL_LDFLAGS "-L%{installdir}/%destdir/$c/lib"
append-path -d { } LOCAL_INCLUDE "-I%{installdir}/%destdir/$c/include"
append-path -d { } LOCAL_CFLAGS "-I%{installdir}/%destdir/$c/include"
append-path -d { } LOCAL_FFLAGS "-I%{installdir}/%destdir/$c/include"
append-path -d { } LOCAL_CXXFLAGS "-I%{installdir}/%destdir/$c/include"
ENDVERSION
popd
done

%files
%defattr(-, root, root, -)
%doc gcc/README gcc/CREDITS gcc/LICENSE
%{installdir}
%exclude %{installdir}/docs
%dir %{modulefile_path}/%{modulefile_subdir}

%files gcc
%defattr(-, root, root, -)
%{installdir}/%destdir/gcc
%dir %{modulefile_path}/%{modulefile_subdir}/gcc
%{modulefile_path}/%{modulefile_subdir}/gcc/%{version}

%files intel
%defattr(-, root, root, -)
%{installdir}/%destdir/intel
%dir %{modulefile_path}/%{modulefile_subdir}/intel
%{modulefile_path}/%{modulefile_subdir}/intel/%{version}

%files -n pdbsql
%defattr(-, root, root, -)
%_datadir/pdbsql
%perl_vendorlib/pdbSql

%files doc
%defattr(-, root, root, -)
%doc %{installdir}/docs

%changelog
* Mon Jan 02 2012 Josko Plazonic <plazonic@math.princeton.edu>
- adapted for puias

* Wed Dec 07 2011 Eugeny A. Rostovtsev (REAL) <real at altlinux.org> 3.17-alt1
- Version 3.17

* Wed Feb 09 2011 Eugeny A. Rostovtsev (REAL) <real at altlinux.org> 3.16-alt4
- Rebuilt for debuginfo

* Fri Oct 01 2010 Eugeny A. Rostovtsev (REAL) <real at altlinux.org> 3.16-alt3
- Fixed edgcpfe by disabling strip

* Tue Aug 31 2010 Eugeny A. Rostovtsev (REAL) <real at altlinux.org> 3.16-alt2
- Fixed for checkbashisms

* Fri Jul 16 2010 Eugeny A. Rostovtsev (REAL) <real at altlinux.org> 3.16-alt1
- Version 3.16

* Sun Aug 30 2009 Eugeny A. Rostovtsev (REAL) <real at altlinux.org> 3.14.1-alt5
- Added shared library

* Sun Jun 14 2009 Eugeny A. Rostovtsev (REAL) <real at altlinux.org> 3.14.1-alt4
- Rebuild with PIC

* Tue Jun 09 2009 Eugeny A. Rostovtsev (REAL) <real at altlinux.org> 3.14.1-alt3
- Rename tau_instrumentor -> tau_instrumentor_pdt

* Wed May 13 2009 Eugeny A. Rostovtsev (REAL) <real at altlinux.org> 3.14.1-alt2
- Rebuild with gcc 4.4

* Mon Apr 06 2009 Eugeny A. Rostovtsev (REAL) <real at altlinux.org> 3.14.1-alt1
- Initial build for Sisyphus


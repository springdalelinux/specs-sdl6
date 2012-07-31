%global snaprel %{nil}

# compiler for which we are doing this
%define compiler intel
%define openmpiversion 1.5.4
%define compilermajor 12
%define compilerminor 1

# do we want gpfs to be on, commentout for not
#define with_gpfs 1

# modules defaults
%define modulefile_path_top /usr/local/share/Modules/modulefiles/hdf5

%ifarch %{ix86}
%define bits 32
%else
%define bits 64
%endif

# deployment plan:
# top dir /usr/local/hdf5
#                        /gcc/1.8.8
#			 /gcc/openmpi-1.5.4/1.8.8
#                        /intel-12.1/1.8.8
#                        /intel-12.1/openmpi-1.5.4/1.8.8

# now, depending on the compiler we need different things - place them all here for eacy access/changing
#
# GCC Compiler
%if "%{compiler}" == "gcc"
%define compilerruntime BuildRequires: gcc-gfortran openmpi-gcc-devel >= %{openmpiversion}
%define compilerruntimeopenmpi Requires: openmpi-gcc >= %{openmpiversion}
%define compilerdevel Requires: gcc-gfortran
%define compilerdevelopenmpi Requires: gcc-gfortran \
Requires: openmpi-gcc-devel >= %{openmpiversion}
%define localdir /usr/local/hdf5/gcc/%{version}
%define localdiropenmpi /usr/local/hdf5/gcc/openmpi-%{openmpiversion}/%{version}
# do nothing special for gcc for build prep
%define compilerbuildprep echo Nothing to do for gcc prep
# no alias
%define modulefile_compiler_alias %{nil}
%define compilershort gcc
%define compilerlong gcc
%define compilerversionnum 446
%define optflags -O0 -pipe -Wall
%endif
#
# Intel compiler
%if "%{compiler}" == "intel"
# these two are used to decide which version of intel we will be using to build it all
# and which version we will be providing
%define intelminrelease 6
%define compilerversion %{compilermajor}.%{compilerminor}
%define compilerversionnum %{compilermajor}%{compilerminor}
%define compilerruntime BuildRequires: openmpi-intel%{compilerversionnum}-devel >= %{openmpiversion}
%define compilerruntimeopenmpi Requires: openmpi-intel%{compilerversionnum} >= %{openmpiversion}
%define compilerdevel Requires: intel-compiler%{compilermajor}-%{bits}-default-modules-devel >= %{compilerversion}-%{intelminrelease}
%define compilerdevelopenmpi Requires: openmpi-intel%{compilerversionnum}-devel >= %{openmpiversion}
%define localdir /usr/local/hdf5/intel-12.1/%{version}
%define localdiropenmpi /usr/local/hdf5/intel-12.1/openmpi-%{openmpiversion}/%{version}
# for intel we need to just specify our compilers
%define compilerbuildprep export CC=icc CXX=icpc F9X=ifort LDFLAGS="-Wl,--build-id" FFLAGS="-O3"; module load intel
# the following is used in above
%define compilershort intel-%{compilermajor}
%define compilerlong intel-%{compilerversion}
%define optflags -O3
%endif

# where modules really go
%define modulefile_path %{modulefile_path_top}/%{compilerlong}
# alias to make sure that module load hdf5/gcc does not load hdf5/gcc/openmpi
# also it makes sure that module load hdf5/intel and hdf5/intel-12 work
%define modulefile_compiler_alias %{modulefile_path_top}/.modulerc-%{compiler}-%{bits}-%{compilerversionnum}

# NOTE:  Try not to realease new versions to released versions of Fedora
# You need to recompile all users of HDF5 for each version change
Name: hdf5-%{?with_gpfs:gpfs-}%{compiler}
Version: 1.8.8
Release: 6.4%{?dist}
Summary: A general purpose library and file format for storing scientific data
License: BSD
Group: System Environment/Libraries
URL: http://www.hdfgroup.org/HDF5/
Source0: http://www.hdfgroup.org/ftp/HDF5/current/src/hdf5-%{version}%{?snaprel}.tar.bz2
Source1: h5comp
Patch0: hdf5-LD_LIBRARY_PATH.patch
Patch1: hdf5-1.8.8-tstlite.patch
Patch10: hdf5-fixpic.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: krb5-devel, openssl-devel, zlib-devel, gcc-gfortran, time
BuildRequires: szip-devel
%if 0%{?with_gpfs}
BuildRequires: gpfs.base
%define gpfs_description This build is made against gpfs and it cannot be mixed with non gpfs build.
%else
%define gpfs_description %{nil}
%endif
Requires: environment-modules
%{compilerruntime}

%global with_mpich2 0
%global with_openmpi 1

%if %{with_mpich2}
%global mpi_list mpich2
%endif
%if %{with_openmpi}
%global mpi_list %{?mpi_list} openmpi
%endif

%description
HDF5 is a general purpose library and file format for storing scientific data.
HDF5 can store two primary objects: datasets and groups. A dataset is
essentially a multidimensional array of data elements, and a group is a
structure for organizing objects in an HDF5 file. Using these two basic
objects, one can create and store almost any kind of scientific data
structure, such as images, arrays of vectors, and structured and unstructured
grids. You can also mix and match them in HDF5 files according to your needs.

%{gpfs_description}

%package devel
Summary: HDF5 development files
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: zlib-devel szip-devel
%{compilerdevel}

%description devel
HDF5 development headers and libraries.

%{gpfs_description}

%package static
Summary: HDF5 static libraries
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
HDF5 static libraries.


%if %{with_mpich2}
%package mpich2
Summary: HDF5 mpich2 libraries
Group: Development/Libraries
Requires: mpich2
Requires: environment-modules
BuildRequires: mpich2-devel

%description mpich2
HDF5 parallel mpich2 libraries

%{gpfs_description}

%package mpich2-devel
Summary: HDF5 mpich2 development files
Group: Development/Libraries
Requires: %{name}-mpich2%{?_isa} = %{version}-%{release}
Requires: mpich2

%description mpich2-devel
HDF5 parallel mpich2 development files

%{gpfs_description}

%package mpich2-static
Summary: HDF5 mpich2 static libraries
Group: Development/Libraries
Requires: %{name}-mpich2-devel%{?_isa} = %{version}-%{release}

%description mpich2-static
HDF5 parallel mpich2 static libraries
%endif


%if %{with_openmpi}
%package openmpi
Summary: HDF5 openmpi libraries
Group: Development/Libraries
Requires: environment-modules
%{compilerruntimeopenmpi}

%description openmpi
HDF5 parallel openmpi libraries

%{gpfs_description}

%package openmpi-devel
Summary: HDF5 openmpi development files
Group: Development/Libraries
Requires: %{name}-openmpi%{_isa} = %{version}-%{release}
%{compilerdevelopenmpi}

%description openmpi-devel
HDF5 parallel openmpi development files

%{gpfs_description}

%package openmpi-static
Summary: HDF5 openmpi static libraries
Group: Development/Libraries
Requires: %{name}-openmpi-devel%{?_isa} = %{version}-%{release}

%description openmpi-static
HDF5 parallel openmpi static libraries
%endif


%prep
%setup -q -n hdf5-%{version}%{?snaprel}
%patch0 -p1 -b .LD_LIBRARY_PATH
%ifarch ppc64 s390x x86_64
# the tstlite test fails with "stack smashing detected" on these arches
%patch1 -p1 -b .tstlite
%endif
#This should be fixed in 1.8.7
find \( -name '*.[ch]*' -o -name '*.f90' -o -name '*.txt' \) -exec chmod -x {} +
%if "%{compiler}" == "intel"
%patch10 -p1 -b .fixpic
%endif

%build
#Do out of tree builds
%global _configure ../configure
#Common configure options
%global configure_opts \\\
  --disable-dependency-tracking \\\
  --enable-fortran \\\
  --enable-fortran2003 \\\
  --enable-hl \\\
  --enable-shared \\\
  --enable-szlib \\\
  --disable-silent-rules \\\
  --disable-silent-rules \\\
  %{?with_gpfs:--enable-gpfs} \\\
%{nil}
# --enable-cxx and --enable-parallel flags are incompatible
# --with-mpe=DIR          Use MPE instrumentation [default=no]
# --enable-cxx/fortran/parallel and --enable-threadsafe flags are incompatible

# setup modules here first, even if may not need them - will not hurt
. /etc/profile.d/modules.sh

#Serial build
export CC=gcc
export CXX=g++
export F9X=gfortran
%{compilerbuildprep}
mkdir build
pushd build
ln -s ../configure .
%configure \
  %{configure_opts} \
  --libdir=%{localdir}/%{_lib} \
  --bindir=%{localdir}/bin \
  --sbindir=%{localdir}/sbin \
  --includedir=%{localdir}/include \
  --datadir=%{localdir}/share \
  --datarootdir=%{localdir}/share \
  --mandir=%{localdir}/share/man \
  --exec-prefix=%{localdir} \
  --enable-cxx
make
module purge
popd

#MPI builds
export CC=mpicc
export CXX=mpicxx
export F9X=mpif90
mkdir openmpi
pushd openmpi
  module load openmpi/%{compiler}
  ln -s ../configure .
  %configure \
    %{configure_opts} \
    --enable-parallel \
    --libdir=%{localdiropenmpi}/%{_lib} \
    --bindir=%{localdiropenmpi}/bin \
    --sbindir=%{localdiropenmpi}/sbin \
    --includedir=%{localdiropenmpi}/include \
    --datadir=%{localdiropenmpi}/share \
    --datarootdir=%{localdiropenmpi}/share \
    --mandir=%{localdiropenmpi}/share/man \
    --exec-prefix=%{localdiropenmpi} \
    --enable-gpfs
  make
  module purge
popd


%install
rm -rf $RPM_BUILD_ROOT

# setup modules here first, even if may not need them - will not hurt
. /etc/profile.d/modules.sh

#Serial build
export CC=gcc
export CXX=g++
export F9X=gfortran
%{compilerbuildprep}
make -C build install DESTDIR=${RPM_BUILD_ROOT}
rm $RPM_BUILD_ROOT/%{localdir}/%{_lib}/*.la
  module purge
  module load openmpi/%{compiler}
  make -C openmpi install DESTDIR=${RPM_BUILD_ROOT}
  rm $RPM_BUILD_ROOT/%{localdiropenmpi}/%{_lib}/*.la
  module purge

#Fortran modules
#mkdir -p ${RPM_BUILD_ROOT}%{_fmoddir}
#mv ${RPM_BUILD_ROOT}%{_includedir}/*.mod ${RPM_BUILD_ROOT}%{_fmoddir}
#Fixup example permissions
find ${RPM_BUILD_ROOT}%{localdir}/share ${RPM_BUILD_ROOT}%{localdiropenmpi}/share \( -name '*.[ch]*' -o -name '*.f90' \) -exec chmod -x {} +

#Fixup headers and scripts for multiarch
#%ifarch x86_64 ppc64 ia64 s390x sparc64 alpha
#sed -i -e s/H5pubconf.h/H5pubconf-64.h/ ${RPM_BUILD_ROOT}%{_includedir}/H5public.h
#mv ${RPM_BUILD_ROOT}%{_includedir}/H5pubconf.h \
#   ${RPM_BUILD_ROOT}%{_includedir}/H5pubconf-64.h
#for x in h5c++ h5cc h5fc
#do
#  mv ${RPM_BUILD_ROOT}%{_bindir}/${x} \
#     ${RPM_BUILD_ROOT}%{_bindir}/${x}-64
#  install -m 0755 %SOURCE1 ${RPM_BUILD_ROOT}%{_bindir}/${x}
#done
#%else
#sed -i -e s/H5pubconf.h/H5pubconf-32.h/ ${RPM_BUILD_ROOT}%{_includedir}/H5public.h
#mv ${RPM_BUILD_ROOT}%{_includedir}/H5pubconf.h \
#   ${RPM_BUILD_ROOT}%{_includedir}/H5pubconf-32.h
#for x in h5c++ h5cc h5fc
#do
#  mv ${RPM_BUILD_ROOT}%{_bindir}/${x} \
#     ${RPM_BUILD_ROOT}%{_bindir}/${x}-32
#  install -m 0755 %SOURCE1 ${RPM_BUILD_ROOT}%{_bindir}/${x}
#done
#%endif

# hack to make gfortran work transparently, still to see what it does for intel
for i in $RPM_BUILD_ROOT/%{localdir}/%{_lib} $RPM_BUILD_ROOT/%{localdiropenmpi}/%{_lib}; do
	pushd $i
	ln -s ../include finclude
	popd
done

mkdir -p ${RPM_BUILD_ROOT}%{modulefile_path}
# first the alias
cat <<ENDMODULEFILETRICK >$RPM_BUILD_ROOT/%{modulefile_compiler_alias}
#%Module
module-alias hdf5/%{compilerlong} hdf5/%{compilerlong}/%{version}
ENDMODULEFILETRICK
%if "%{compiler}" != "%{compilershort}"
echo "module-alias hdf5/%{compilershort} hdf5/%{compilerlong}/%{version}" >> $RPM_BUILD_ROOT/%{modulefile_compiler_alias}
echo "module-alias hdf5/%{compilershort}/%{version} hdf5/%{compilerlong}/%{version}" >> $RPM_BUILD_ROOT/%{modulefile_compiler_alias}
%endif
%if "%{compiler}" != "%{compilerlong}"
echo "module-alias hdf5/%{compiler} hdf5/%{compilerlong}/%{version}" >> $RPM_BUILD_ROOT/%{modulefile_compiler_alias}
echo "module-alias hdf5/%{compiler}/%{version} hdf5/%{compilerlong}/%{version}" >> $RPM_BUILD_ROOT/%{modulefile_compiler_alias}
%endif
cat <<ENDCOREMODULE > ${RPM_BUILD_ROOT}%{modulefile_path}/%{version}
#%Module

# NOTE: This is an automatically-generated file!  (generated by the
# hdf5 rpm).  Any changes made here will be lost a) if the RPM is
# uninstalled, or b) if the RPM is upgraded or uninstalled.

proc ModulesHelp { } {
   puts stderr "This module adds hdf5 %{version} for %{compilerlong} to various paths"
}   
    
module-whatis   "Sets up hdf5 {version} for %{compilerlong} in your environment"

prepend-path PATH "%{localdir}/bin"
prepend-path LD_LIBRARY_PATH "%{localdir}/%{_lib}"
prepend-path LIBRARY_PATH "%{localdir}/%{_lib}"
prepend-path MANPATH "%{localdir}/share/man"
setenv HDF5DIR "%{localdir}"
append-path -d { } LDFLAGS "-L%{localdir}/%{_lib}"
append-path -d { } INCLUDE "-I%{localdir}/include"
append-path CPATH "%{localdir}/include"
append-path -d { } FFLAGS "-I%{localdir}/include"
append-path -d { } LOCAL_LDFLAGS "-L%{localdir}/%{_lib}"
append-path -d { } LOCAL_INCLUDE "-I%{localdir}/include"
append-path -d { } LOCAL_CFLAGS "-I%{localdir}/include"
append-path -d { } LOCAL_FFLAGS "-I%{localdir}/include"
append-path -d { } LOCAL_CXXFLAGS "-I%{localdir}/include"
ENDCOREMODULE

%if %{with_openmpi}
mkdir -p ${RPM_BUILD_ROOT}%{modulefile_path}/openmpi-%{openmpiversion}
cat <<ENDMODULEMPITRICK > ${RPM_BUILD_ROOT}%{modulefile_path}/.modulerc-openmpi-%{openmpiversion}
#%Module
module-alias hdf5/%{compiler}/openmpi hdf5/%{compilerlong}/openmpi-%{openmpiversion}
ENDMODULEMPITRICK
%if "%{compiler}" != "%{compilershort}"
echo "module-alias hdf5/%{compilershort}/openmpi hdf5/%{compilerlong}/openmpi-%{openmpiversion}" >> ${RPM_BUILD_ROOT}%{modulefile_path}/.modulerc-openmpi-%{openmpiversion}
%endif
%if "%{compiler}" != "%{compilerlong}"
echo "module-alias hdf5/%{compilerlong}/openmpi hdf5/%{compilerlong}/openmpi-%{openmpiversion}" >> ${RPM_BUILD_ROOT}%{modulefile_path}/.modulerc-openmpi-%{openmpiversion}
%endif
%endif
cat <<ENDOPENMPIMODULE > ${RPM_BUILD_ROOT}%{modulefile_path}/openmpi-%{openmpiversion}/%{version}
#%Module

# NOTE: This is an automatically-generated file!  (generated by the
# hdf5 rpm).  Any changes made here will be lost a) if the RPM is
# uninstalled, or b) if the RPM is upgraded or uninstalled.

proc ModulesHelp { } {
   puts stderr "This module adds hdf5 %{version} for %{compilerlong} openmpi-%{openmpiversion} to various paths"
}   
    
module-whatis   "Sets up hdf5 {version} for %{compilerlong} openmpi-%{openmpiversion} in your environment"

prepend-path PATH "%{localdiropenmpi}/bin"
prepend-path LD_LIBRARY_PATH "%{localdiropenmpi}/%{_lib}"
prepend-path LIBRARY_PATH "%{localdiropenmpi}/%{_lib}"
prepend-path MANPATH "%{localdiropenmpi}/share/man"
setenv HDF5DIR "%{localdiropenmpi}"
append-path -d { } LDFLAGS "-L%{localdiropenmpi}/%{_lib}"
append-path -d { } INCLUDE "-I%{localdiropenmpi}/include"
append-path CPATH "%{localdiropenmpi}/include"
append-path -d { } FFLAGS "-I%{localdiropenmpi}/include"
append-path -d { } LOCAL_LDFLAGS "-L%{localdiropenmpi}/%{_lib}"
append-path -d { } LOCAL_INCLUDE "-I%{localdiropenmpi}/include"
append-path -d { } LOCAL_CFLAGS "-I%{localdiropenmpi}/include"
append-path -d { } LOCAL_FFLAGS "-I%{localdiropenmpi}/include"
append-path -d { } LOCAL_CXXFLAGS "-I%{localdiropenmpi}/include"
ENDOPENMPIMODULE

%check
#Serial build
export CC=gcc
export CXX=g++
export F9X=gfortran
%{compilerbuildprep}
make -C build check
#These really don't work on builders
#for mpi in mpich2 openmpi
#do
#  module load $mpi-%{_arch}
#  make -C $mpi check
#  module purge
#done


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING MANIFEST README.txt release_docs/RELEASE.txt
%doc release_docs/HISTORY*.txt
%{localdir}/bin/gif2h5
%{localdir}/bin/h52gif
%{localdir}/bin/h5copy
%{localdir}/bin/h5debug
%{localdir}/bin/h5diff
%{localdir}/bin/h5dump
%{localdir}/bin/h5import
%{localdir}/bin/h5jam
%{localdir}/bin/h5ls
%{localdir}/bin/h5mkgrp
%{localdir}/bin/h5perf_serial
%{localdir}/bin/h5repack
%{localdir}/bin/h5repart
%{localdir}/bin/h5stat
%{localdir}/bin/h5unjam
%{localdir}/%{_lib}/*.so.*
%dir %{modulefile_path_top}
%dir %{modulefile_path}
%{modulefile_path}/%{version}
%{modulefile_compiler_alias}

%files devel
%defattr(-,root,root,-)
%{localdir}/bin/h5c++*
%{localdir}/bin/h5cc*
%{localdir}/bin/h5fc*
%{localdir}/bin/h5redeploy
%{localdir}/include/*.h
%{localdir}/%{_lib}/*.so
%{localdir}/%{_lib}/*.settings
%{localdir}/%{_lib}/finclude
%{localdir}/include/*.mod
%{localdir}/share/hdf5_examples/

%files static
%defattr(-,root,root,-)
%{localdir}/%{_lib}/*.a

%if %{with_mpich2}
%files mpich2
%defattr(-,root,root,-)
%doc COPYING MANIFEST README.txt release_docs/RELEASE.txt
%doc release_docs/HISTORY*.txt
%{_libdir}/mpich2/bin/gif2h5
%{_libdir}/mpich2/bin/h52gif
%{_libdir}/mpich2/bin/h5copy
%{_libdir}/mpich2/bin/h5debug
%{_libdir}/mpich2/bin/h5diff
%{_libdir}/mpich2/bin/h5dump
%{_libdir}/mpich2/bin/h5import
%{_libdir}/mpich2/bin/h5jam
%{_libdir}/mpich2/bin/h5ls
%{_libdir}/mpich2/bin/h5mkgrp
%{_libdir}/mpich2/bin/h5redeploy
%{_libdir}/mpich2/bin/h5repack
%{_libdir}/mpich2/bin/h5perf
%{_libdir}/mpich2/bin/h5perf_serial
%{_libdir}/mpich2/bin/h5repart
%{_libdir}/mpich2/bin/h5stat
%{_libdir}/mpich2/bin/h5unjam
%{_libdir}/mpich2/bin/ph5diff
%{_libdir}/mpich2/%{_lib}/*.so.*

%files mpich2-devel
%defattr(-,root,root,-)
%{_includedir}/mpich2-%{_arch}
%{_libdir}/mpich2/bin/h5pcc
%{_libdir}/mpich2/bin/h5pfc
%{_libdir}/mpich2/%{_lib}/lib*.so
#{_libdir}/mpich2/lib/lib*.settings

%files mpich2-static
%defattr(-,root,root,-)
%{_libdir}/mpich2/lib/*.a
%endif

%if %{with_openmpi}
%files openmpi
%defattr(-,root,root,-)
%doc COPYING MANIFEST README.txt release_docs/RELEASE.txt
%doc release_docs/HISTORY*.txt
%{localdiropenmpi}/bin/gif2h5
%{localdiropenmpi}/bin/h52gif
%{localdiropenmpi}/bin/h5copy
%{localdiropenmpi}/bin/h5debug
%{localdiropenmpi}/bin/h5diff
%{localdiropenmpi}/bin/h5dump
%{localdiropenmpi}/bin/h5import
%{localdiropenmpi}/bin/h5jam
%{localdiropenmpi}/bin/h5ls
%{localdiropenmpi}/bin/h5mkgrp
%{localdiropenmpi}/bin/h5perf
%{localdiropenmpi}/bin/h5perf_serial
%{localdiropenmpi}/bin/h5redeploy
%{localdiropenmpi}/bin/h5repack
%{localdiropenmpi}/bin/h5repart
%{localdiropenmpi}/bin/h5stat
%{localdiropenmpi}/bin/h5unjam
%{localdiropenmpi}/bin/ph5diff
%{localdiropenmpi}/%{_lib}/*.so.*
%dir %{modulefile_path_top}
%dir %{modulefile_path}
%dir %{modulefile_path}/openmpi-%{openmpiversion}
%{modulefile_path}/.modulerc-openmpi-%{openmpiversion}
%{modulefile_path}/openmpi-%{openmpiversion}/%{version}

%files openmpi-devel
%defattr(-,root,root,-)
%{localdiropenmpi}/include
%{localdiropenmpi}/bin/h5pcc
%{localdiropenmpi}/bin/h5pfc
%{localdiropenmpi}/%{_lib}/lib*.so
%{localdiropenmpi}/%{_lib}/lib*.settings
%{localdiropenmpi}/%{_lib}/finclude
%{localdiropenmpi}/share/hdf5_examples/

%files openmpi-static
%defattr(-,root,root,-)
%{localdiropenmpi}/%{_lib}/lib*.a
%endif


%changelog
* Sat Jan 14 2012 Josko Plazonic <plazonic@math.princeton.edu>
- modify the build to use multiple compilers and env modules
  for loading
- patch configure to fix intel mpi builds and ld flag to fix
  build-id issues when using intel
- added gpfs support

* Sat Jan 7 2012 Orion Poplawski <orion@cora.nwra.com> 1.8.8-6
- Enable Fortran 2003 support (bug 772387)

* Wed Dec 21 2011 Dan Horák <dan[at]danny.cz> 1.8.8-5
- reintroduce the tstlite patch for ppc64 and s390x

* Thu Dec 01 2011 Caolán McNamara <caolanm@redhat.com> 1.8.8-4
- Related: rhbz#758334 hdf5 doesn't build on ppc64

* Fri Nov 25 2011 Orion Poplawski <orion@cora.nwra.com> 1.8.8-3
- Enable static MPI builds

* Wed Nov 16 2011 Orion Poplawski <orion@cora.nwra.com> 1.8.8-2
- Add rpm macro %%{_hdf5_version} for convenience

* Tue Nov 15 2011 Orion Poplawski <orion@cora.nwra.com> 1.8.8-1
- Update to 1.8.8
- Drop tstlite patch
- Add patch to avoid setting LD_LIBRARY_PATH

* Wed Jun 01 2011 Karsten Hopp <karsten@redhat.com> 1.8.7-2
- drop ppc64 longdouble patch, not required anymore

* Tue May 17 2011 Orion Poplawski <orion@cora.nwra.com> 1.8.7-1
- Update to 1.8.7

* Tue Mar 29 2011 Deji Akingunola <dakingun@gmail.com> - 1.8.6-2
- Rebuild for mpich2 soname bump

* Fri Feb 18 2011 Orion Poplawski <orion@cora.nwra.com> 1.8.6-1
- Update to 1.8.6-1
- Update tstlite patch - not fixed yet

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.5.patch1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Feb 6 2011 Orion Poplawski <orion@cora.nwra.com> 1.8.5.patch1-7
- Add Requires: zlib-devel to hdf5-devel

* Sun Dec 12 2010 Dan Horák <dan[at]danny.cz> 1.8.5.patch1-6
- fully conditionalize MPI support

* Wed Dec 8 2010 Orion Poplawski <orion@cora.nwra.com> 1.8.5.patch1-5
- Add EL6 compatibility - no mpich2 on ppc64

* Wed Oct 27 2010 Orion Poplawski <orion@cora.nwra.com> 1.8.5.patch1-4
- Really fixup all permissions

* Wed Oct 27 2010 Orion Poplawski <orion@cora.nwra.com> 1.8.5.patch1-3
- Add docs to the mpi packages
- Fixup example source file permissions

* Tue Oct 26 2010 Orion Poplawski <orion@cora.nwra.com> 1.8.5.patch1-2
- Build parallel hdf5 packages for mpich2 and openmpi
- Rework multiarch support and drop multiarch patch

* Tue Sep 7 2010 Orion Poplawski <orion@cora.nwra.com> 1.8.5.patch1-1
- Update to 1.8.5-patch1

* Wed Jun 23 2010 Orion Poplawski <orion@cora.nwra.com> 1.8.5-4
- Re-add rebased tstlite patch - not fixed yet

* Wed Jun 23 2010 Orion Poplawski <orion@cora.nwra.com> 1.8.5-3
- Update longdouble patch for 1.8.5

* Wed Jun 23 2010 Orion Poplawski <orion@cora.nwra.com> 1.8.5-2
- Re-add longdouble patch on ppc64 for EPEL builds

* Mon Jun 21 2010 Orion Poplawski <orion@cora.nwra.com> 1.8.5-1
- Update to 1.8.5
- Drop patches fixed upstream

* Mon Mar 1 2010 Orion Poplawski <orion@cora.nwra.com> 1.8.4.patch1-1
- Update to 1.8.4-patch1

* Wed Jan 6 2010 Orion Poplawski <orion@cora.nwra.com> 1.8.4-1
- Update to 1.8.4
- Must compile with -O0 due to gcc-4.4 incompatability
- No longer need -fno-strict-aliasing

* Thu Oct 1 2009 Orion Poplawski <orion@cora.nwra.com> 1.8.3-3.snap12
- Update to 1.8.3-snap12
- Update signal patch
- Drop detect and filter-as-option patch fixed upstream
- Drop ppc only patch
- Add patch to skip tstlite test for now, problem reported upstream
- Fixup some source file permissions

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 2 2009 Orion Poplawski <orion@cora.nwra.com> 1.8.3-1
- Update to 1.8.3
- Update signal and detect patches
- Drop open patch fixed upstream

* Sat Apr 18 2009 Karsten Hopp <karsten@redhat.com> 1.8.2-1.1
- fix s390x builds, s390x is 64bit, s390 is 32bit

* Mon Feb 23 2009 Orion Poplawski <orion@cora.nwra.com> 1.8.2-1
- Update to 1.8.2
- Add patch to compile H5detect without optimization - make detection
  of datatype characteristics more robust - esp. long double
- Update signal patch
- Drop destdir patch fixed upstream
- Drop scaleoffset patch
- Re-add -fno-strict-aliasing
- Keep settings file needed for -showconfig (bug #481032)
- Wrapper script needs to pass arguments (bug #481032)

* Wed Oct 8 2008 Orion Poplawski <orion@cora.nwra.com> 1.8.1-3
- Add sparc64 to 64-bit conditionals

* Fri Sep 26 2008 Orion Poplawski <orion@cora.nwra.com> 1.8.1-2
- Add patch to filter -little as option used on sh arch (#464052)

* Thu Jun 5 2008 Orion Poplawski <orion@cora.nwra.com> 1.8.1-1
- Update to 1.8.1

* Tue May 27 2008 Orion Poplawski <orion@cora.nwra.com> 1.8.1-0.rc1.1
- Update to 1.8.1-rc1

* Tue May 13 2008 Orion Poplawski <orion@cora.nwra.com> 1.8.0.snap5-2
- Use new %%{_fmoddir} macro
- Re-enable ppc64, disable failing tests.  Failing tests are for
  experimental long double support.

* Mon May 5 2008 Orion Poplawski <orion@cora.nwra.com> 1.8.0.snap5-1
- Update to 1.8.0-snap5
- Remove --enable-threadsafe, incompatible with --enable-cxx and
  --enable-fortran
- ExcludeArch ppc64 until we can get it to build (bug #445423)

* Tue Mar 4 2008 Orion Poplawski <orion@cora.nwra.com> 1.8.0-2
- Remove failing test for now

* Fri Feb 29 2008 Orion Poplawski <orion@cora.nwra.com> 1.8.0-1
- Update to 1.8.0, drop upstreamed patches
- Update signal patch
- Move static libraries into -static sub-package
- Make -devel multiarch (bug #341501)

* Wed Feb  6 2008 Orion Poplawski <orion@cora.nwra.com> 1.6.6-7
- Add patch to fix strict-aliasing
- Disable production mode to enable debuginfo

* Tue Feb  5 2008 Orion Poplawski <orion@cora.nwra.com> 1.6.6-6
- Add patch to fix calling free() in H5PropList.cpp

* Tue Feb  5 2008 Orion Poplawski <orion@cora.nwra.com> 1.6.6-5
- Add patch to support s390 (bug #431510)

* Mon Jan  7 2008 Orion Poplawski <orion@cora.nwra.com> 1.6.6-4
- Add patches to support sparc (bug #427651)

* Tue Dec  4 2007 Orion Poplawski <orion@cora.nwra.com> 1.6.6-3
- Rebuild against new openssl

* Fri Nov 23 2007 Orion Poplawski <orion@cora.nwra.com> 1.6.6-2
- Add patch to build on alpha (bug #396391)

* Wed Oct 17 2007 Orion Poplawski <orion@cora.nwra.com> 1.6.6-1
- Update to 1.6.6, drop upstreamed patches
- Explicitly set compilers

* Fri Aug 24 2007 Orion Poplawski <orion@cora.nwra.com> 1.6.5-9
- Update license tag to BSD
- Rebuild for BuildID

* Wed Aug  8 2007 Orion Poplawski <orion@cora.nwra.com> 1.6.5-8
- Fix memset typo
- Pass mode to open with O_CREAT

* Mon Feb 12 2007 Orion Poplawski <orion@cora.nwra.com> 1.6.5-7
- New project URL
- Add patch to use POSIX sort key option
- Remove useless and multilib conflicting Makefiles from html docs
  (bug #228365)
- Make hdf5-devel own %%{_docdir}/%%{name}

* Tue Aug 29 2006 Orion Poplawski <orion@cora.nwra.com> 1.6.5-6
- Rebuild for FC6

* Wed Mar 15 2006 Orion Poplawski <orion@cora.nwra.com> 1.6.5-5
- Change rpath patch to not need autoconf
- Add patch for libtool on x86_64
- Fix shared lib permissions

* Mon Mar 13 2006 Orion Poplawski <orion@cora.nwra.com> 1.6.5-4
- Add patch to avoid HDF setting the compiler flags

* Mon Feb 13 2006 Orion Poplawski <orion@cora.nwra.com> 1.6.5-3
- Rebuild for gcc/glibc changes

* Wed Dec 21 2005 Orion Poplawski <orion@cora.nwra.com> 1.6.5-2
- Don't ship h5perf with missing library

* Wed Dec 21 2005 Orion Poplawski <orion@cora.nwra.com> 1.6.5-1
- Update to 1.6.5

* Wed Dec 21 2005 Orion Poplawski <orion@cora.nwra.com> 1.6.4-9
- Rebuild

* Wed Nov 30 2005 Orion Poplawski <orion@cora.nwra.com> 1.6.4-8
- Package fortran files properly
- Move compiler wrappers to devel

* Fri Nov 18 2005 Orion Poplawski <orion@cora.nwra.com> 1.6.4-7
- Add patch for fortran compilation on ppc

* Wed Nov 16 2005 Orion Poplawski <orion@cora.nwra.com> 1.6.4-6
- Bump for new openssl

* Tue Sep 20 2005 Orion Poplawski <orion@cora.nwra.com> 1.6.4-5
- Enable fortran since the gcc bug is now fixed

* Tue Jul 05 2005 Orion Poplawski <orion@cora.nwra.com> 1.6.4-4
- Make example scripts executable

* Wed Jul 01 2005 Orion Poplawski <orion@cora.nwra.com> 1.6.4-3
- Add --enable-threads --with-pthreads to configure
- Add %%check
- Add some %%docs
- Use %%makeinstall
- Add patch to fix test for h5repack
- Add patch to fix h5diff_attr.c

* Mon Jun 27 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.6.4-2
- remove szip from spec, since szip license doesn't meet Fedora standards

* Sun Apr 3 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.6.4-1
- inital package for Fedora Extras

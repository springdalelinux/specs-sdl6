# compiler for which we are doing this
%define compiler intel
%define compilermajor 12
%define compilerminor 1

# we only do it for 64 bit
%define bits 64

# modules defaults
%define modulefile_path_top /usr/share/Modules/modulefiles/mpt

# deployment plan:
# top dir /usr/share/Modules/modulefiles/mpt
#                        2.05 (provided by SGI rpm)
#                        /intel-12.1/2.05

#
# Intel compiler
%if "%{compiler}" == "intel"
# these two are used to decide which version of intel we will be using to build it all
# and which version we will be providing
%define intelminrelease 6
%define compilerversion %{compilermajor}.%{compilerminor}
%define compilerversionnum %{compilermajor}%{compilerminor}
%define compilerruntime Requires: intel-compiler%{compilermajor}-%{bits}-default-modules >= %{compilerversion}-%{intelminrelease}
%define compilerdevel Requires: intel-compiler%{compilermajor}-%{bits}-default-modules-devel >= %{compilerversion}-%{intelminrelease}
# the following is used in above
%define compilershort intel-%{compilermajor}
%define compilerlong intel-%{compilerversion}
# and how do we invoke them
%define compilerc icc
%define compilercxx icpc
%define compilerf ifort
%endif

# where modules really go
%define modulefile_path %{modulefile_path_top}/%{compilerlong}
# also it makes sure that module load mpt/intel and mpt/intel-12 work
%define modulefile_compiler_alias %{modulefile_path_top}/.modulerc-%{compiler}-%{bits}-%{compilerversionnum}

Name: sgi-mpt-%{compiler}%{compilerversionnum}
Version: 2.05
Release: 1.1%{?dist}
Summary: Wrapper for SGI MPT and %{compiler} %{compilerversion} compiler
License: BSD
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: environment-modules
Requires: sgi-mpt = %{version}
%{compilerruntime}

%description
This rpm provides environment modules for using SGI's MPT with 
%{compiler} %{compilerversion} compiler

%package devel
Summary: Development wrapper for SGI MPT and %{compiler} %{compilerversion} compiler
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
%{compilerdevel}

%description devel
An empty rpm used just for requirements

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p ${RPM_BUILD_ROOT}%{modulefile_path}
# first the alias
cat <<ENDMODULEFILETRICK >$RPM_BUILD_ROOT/%{modulefile_compiler_alias}
#%Module
module-alias mpt/%{compilerlong} mpt/%{compilerlong}/%{version}
ENDMODULEFILETRICK
%if "%{compiler}" != "%{compilershort}"
echo "module-alias mpt/%{compilershort} mpt/%{compilerlong}/%{version}" >> $RPM_BUILD_ROOT/%{modulefile_compiler_alias}
echo "module-alias mpt/%{compilershort}/%{version} mpt/%{compilerlong}/%{version}" >> $RPM_BUILD_ROOT/%{modulefile_compiler_alias}
# we also need it in %{compilershort} subdir
mkdir -p $RPM_BUILD_ROOT/%{modulefile_path_top}/%{compilershort}
pushd $RPM_BUILD_ROOT/%{modulefile_path_top}/%{compilershort}
ln -s ../.modulerc-%{compiler}* .
popd
%endif
%if "%{compiler}" != "%{compilerlong}"
echo "module-alias mpt/%{compiler} mpt/%{compilerlong}/%{version}" >> $RPM_BUILD_ROOT/%{modulefile_compiler_alias}
echo "module-alias mpt/%{compiler}/%{version} mpt/%{compilerlong}/%{version}" >> $RPM_BUILD_ROOT/%{modulefile_compiler_alias}
# we also need it in %{compiler} subdir
mkdir -p $RPM_BUILD_ROOT/%{modulefile_path_top}/%{compiler}
pushd $RPM_BUILD_ROOT/%{modulefile_path_top}/%{compiler}
ln -s ../.modulerc-%{compiler}* .
popd
%endif
# finally, make the pure mpt default
echo "module-alias mpt mpt/%{version}" >> $RPM_BUILD_ROOT/%{modulefile_compiler_alias}

# and now the wrapper module
cat <<ENDCOREMODULE > ${RPM_BUILD_ROOT}%{modulefile_path}/%{version}
#%Module1.0#####################################################################
##
## mpt %{version} %{compiler} %{compilerversion} wrapper module
##
proc ModulesHelp { } {
        global version

        puts stderr "\tThis module sets appropriate paths for using SGI MPT %{version} with the %{compiler} %{compilerversion} compiler"
}

module-whatis   "Loads settings for the SGI MPT %{version} with %{compiler} %{compilerversion} compiler"
module load %{compiler}/%{compilerversion}
module load mpt/%{version}
setenv MPIF90_F90 "%{compilerf}"
setenv MPICC_CC "%{compilerc}"
setenv MPICXX_CXX "%{compilercxx}"

set     version      "3.2.3"
ENDCOREMODULE

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir %{modulefile_path_top}
%dir %{modulefile_path}
%{modulefile_path}/%{version}
%{modulefile_compiler_alias}
%if "%{compiler}" != "%{compilershort}"
%dir %{modulefile_path_top}/%{compilershort}
%{modulefile_path_top}/%{compilershort}/.modulerc-%{compiler}*
%endif
%if "%{compiler}" != "%{compilerlong}"
%dir %{modulefile_path_top}/%{compiler}
%{modulefile_path_top}/%{compiler}/.modulerc-%{compiler}*
%endif

%files devel
%defattr(-,root,root,-)

%changelog
* Thu Feb 02 2012 Josko Plazonic <plazonic@math.princeton.edu>
- initial build, partially based on the hdf5-188-compiler spec
  file

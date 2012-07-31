# The following defines the version of compiler suite we are doing this
# that we can do this easily as new versions come out, directly when
# rebuilding this src.rpm
# should be 9.1, 9.0 and so on
%{!?intelversion:%define intelversion 10.1}

# does it obsolete anything, not by default
%define intelobsoletes %{nil}

# The rest should be figured out automatically just from the above two things
%{!?intelshortversion:%define intelshortversion %(echo %{intelversion} | cut -d. -f1-2)}
%{!?intelshortshortversion:%define intelshortshortversion %(echo %{intelversion} | cut -d. -f1)}
%if "%{intelshortversion}" == "9.1" || "%{intelshortshortversion}" == "10"
%define intelnumversion %(echo %{intelshortversion} | tr -d \.)
%endif
%if "%{intelshortversion}" == "9.0"
%define intelnumversion 9
%endif
%if "%{intelshortversion}" == "8.1"
%define intelnumversion 8
%endif

%if "%{intelshortversion}" == "10.1"
%define intelobsoletes Obsoletes: intel-compiler100-%{intelbits}-default-modules
%endif

ExclusiveArch: i386 i686 x86_64
%ifarch i386 i686
%define intelbits 32
Requires: intel-icc%{intelnumversion}-modules 
Requires: intel-ifort%{intelnumversion}-modules
Requires: intel-iidb%{intelnumversion}-modules
%else
%define intelbits 64
Requires: intel-icce%{intelnumversion}-modules 
Requires: intel-iforte%{intelnumversion}-modules
Requires: intel-iidbe%{intelnumversion}-modules
%endif

# in most cases it is a compiler, will override for iidb
%define inteltype compiler

# The destination location for modules files
%define modulesdestination /opt/share/Modules/modulefiles

Summary: Common/Default Modules configuration files for intel %{intelshortversion} compilers
Name: intel-compiler%{intelnumversion}-%{intelbits}-default-modules
Version: %{intelshortversion}
Release: 19%{?dist}
License: Other
Group: Development/Languages
BuildRoot: %{_tmppath}/%{name}-%{version}-root
# In any case, require intel-license
Requires: intel-license
Provides: intel-compiler-default-modules = %{intelshortversion}
%if "%{intelshortshortversion}" == "10"
Provides: intel-compiler%{intelshortshortversion}-%{intelbits}-default-modules = %{intelshortversion}
%endif
Provides: intel-compiler-default-modules = %{intelshortversion}
Provides: intel-compiler-%{intelbits}-default-modules = %{intelshortversion}
Requires: environment-modules >= 3.2.3
%{intelobsoletes}

%description
This rpm contains modules configuration files for the default setup
of intel %{intelshortversion} compilers.  It will try load C, Fortran and
Iidb for this version if you do not specify otherwise.

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{modulesdestination}/intel/%{intelshortversion}/%{intelbits}/%{compiler}
cat > $RPM_BUILD_ROOT%{modulesdestination}/intel/%{intelshortversion}/%{intelbits}/default <<ENDDEFAULT
#%Module1.0#####################################################################
##
## default modulefile
##
proc ModulesHelp { } {
        global version

        puts stderr "\tThis module gets loaded by default if you do"
        puts stderr "\t\tmodule load intel/%{intelshortversion}/%{intelbits}"
        puts stderr "\tand it attempts configure both intel C and Fortran compilers"
        puts stderr "\tas well as the Intel idb debugger for Intel Compilers version %{intelshortversion}"
        puts stderr "\t"
        puts stderr "\n\tVersion \$version\n"
}

module-whatis   "Loads Intel C and Fortran Compilers and the debugger for %{intelshortversion} %{intelbits} bit"
module load intel/%{intelshortversion}/%{intelbits}/C
module load intel/%{intelshortversion}/%{intelbits}/Fortran
module load intel/%{intelshortversion}/%{intelbits}/Iidb
append-path LD_LIBRARY_PATH /usr/local/intel/%{_lib}
append-path -d { } LOCAL_LDFLAGS "-L/usr/local/intel/%{_lib}"
append-path -d { } LOCAL_CFLAGS "-I/usr/local/intel/include"
append-path -d { } LOCAL_CXXFLAGS "-I/usr/local/intel/include"
append-path -d { } LOCAL_FFLAGS "-I/usr/local/intel/include"

set     version      "3.2.3"
ENDDEFAULT
%if "%{intelshortshortversion}" == "10"
cat > $RPM_BUILD_ROOT%{modulesdestination}/intel/.modulerc-intel-%{intelnumversion}-%{intelbits} <<ENDGENERIC
#%Module
module-alias intel/%{intelshortshortversion} intel/%{intelshortversion}
ENDGENERIC
mkdir $RPM_BUILD_ROOT%{modulesdestination}/intel/%{intelshortshortversion}
cat > $RPM_BUILD_ROOT%{modulesdestination}/intel/%{intelshortshortversion}/.modulerc-intel-%{intelnumversion}-%{intelbits} <<ENDMOREGENERIC
#%Module
module-alias intel/%{intelshortshortversion}/%{intelbits} intel/%{intelshortversion}/%{intelbits}
ENDMOREGENERIC
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{modulesdestination}/intel
%dir %{modulesdestination}/intel/%{intelshortversion}
%dir %{modulesdestination}/intel/%{intelshortversion}/%{intelbits}
%{modulesdestination}/intel/%{intelshortversion}/%{intelbits}/default
%if "%{intelshortshortversion}" == "10"
%{modulesdestination}/intel/.modulerc-intel-%{intelnumversion}-%{intelbits}
%dir %{modulesdestination}/intel/%{intelshortshortversion}
%{modulesdestination}/intel/%{intelshortshortversion}/.modulerc-intel-%{intelnumversion}-%{intelbits}
%endif

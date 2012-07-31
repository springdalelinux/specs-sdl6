%undefine _missing_build_ids_terminate_build
%define __os_install_post %{nil}
%global __debug_package %{nil}

Version:	4.2.9
%define cudamajor %(echo %{version} | cut -d. -f1,2 | )
%define cudanumver %(echo %{version} | tr -d .)
%define destdir /usr/local/cudatoolkit/%{version}
Name:		gpucomputingsdk%{cudanumver}
Release:	4%{?dist}
Summary:	NVIDIA GPU computing SKD
Group:		Development/Libraries
License:	NVIDIA
URL:		http://developer.nvidia.com/cuda-toolkit-%(echo %{version}|cut -d. -f1,2| tr -d .)
Source0:	http://developer.download.nvidia.com/compute/cuda/%(echo %{version}|cut -d. -f1,2| tr . _)/rel/sdk/gpucomputingsdk_%{version}_linux.run
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	cudatoolkit%{cudanumver} = %{version}
BuildRequires:	freeglut-devel libX11-devel libXmu-devel libXi-devel mesa-libGL-devel mesa-libGLU-devel mesa-libGLw-devel xorg-x11-drv-nvidia-devel
Requires:	cudatoolkit%{cudanumver} = %{version}
Requires:	freeglut-devel libX11-devel libXmu-devel libXi-devel mesa-libGL-devel mesa-libGLU-devel mesa-libGLw-devel xorg-x11-drv-nvidia-devel
Provides:	gpucomputingsdk = %{version}
AutoReqProv:	0

%description
%{summary}

%prep
%setup -T -c
sh %{SOURCE0} -- --prefix=`pwd`/sdk --cudaprefix=%{destdir}
cp -ar sdk sdk-original

%build
cd sdk
. /etc/profile.d/modules.sh
module load cudatoolkit
make
cd ..
mkdir -p sdk-original/C/bin/linux/release
mv sdk/C/bin/linux/release/* sdk-original/C/bin/linux/release/
rm -rf sdk
mv sdk-original sdk

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{destdir}
mv sdk $RPM_BUILD_ROOT%{destdir}
strip $RPM_BUILD_ROOT%{destdir}/sdk/C/bin/linux/release/*

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{destdir}/sdk


%changelog
* Mon Mar 12 2012 Josko Plazonic <plazonic@math.princeton.edu>
- move to versioned build so that we can allow multiple versions

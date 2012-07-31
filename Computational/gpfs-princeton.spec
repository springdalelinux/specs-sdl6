%define kmod_name gpfs

# as our release is 128 or higher we stop at 99 below:
%define gpfskernelversion 2063299

# minor gpfs version
%define subversion 13
# we need this
%define mrelease %{subversion}.13%{?dist}

Name:		gpfs-princeton
Summary:	The kernel module for GPFS
Version:	3.4.0
Release:        %{mrelease}
License:	LGPL/GPL
Group: 		System Environment/Base
URL: 		http://www.pvfs.org/pvfs2/
Source10:	gpfs.filelist
Source100:	gpfs-kernel-setup.init
Buildroot:	%{_tmppath}/%{name}-buildroot
ExclusiveArch:  x86_64
BuildRequires:	imake ksh
Requires:	gpfs.base = %{version}-%{subversion}
Requires:	openssl097a
BuildRequires:	gpfs.base = %{version}-%{subversion}
BuildRequires:	gpfs.gpl = %{version}-%{subversion}
BuildRequires:  %kernel_module_package_buildreqs
%kernel_module_package -n %{kmod_name} -f %{SOURCE10}

%description
The kernel module for GPFS

%prep
%setup -n %{name}-%{version}-%{subversion} -c -T

echo "%defattr(644,root,root,755)" > %{_builddir}/filelist
echo "/lib/modules/%kverrel${flavor%default}/extra/*ko" >> %{_builddir}/filelist
echo "/usr/lpp/mmfs/bin/*-2.6*" >> %{_builddir}/filelist

mkdir kernel
cd kernel
mkdir usr
# copy but ignore errors
cp -ar /usr/lpp usr/ || :
pushd usr/lpp/mmfs/src/
# before beginning make symlinks for various include files that the installation
# expects to be in /usr/include so build will not be able to find
cd gpl-linux
ln -s ../../include/*.h .
cd ..
# begin with local configs
cp config/env.mcr.sample config/env.mcr
%ifarch x86_64
        perl -pi -e 's|^#define GPFS_ARCH_.*|#define GPFS_ARCH_X86_64|' config/env.mcr
%endif
        perl -pi -e 's|^LINUX_DISTRIBUTION = .*|LINUX_DISTRIBUTION = REDHAT_AS_LINUX|' config/env.mcr
        perl -pi -e 's|^#define LINUX_KERNEL_VERSION .*|#define LINUX_KERNEL_VERSION %{gpfskernelversion}|' config/env.mcr
popd
cd ..
for flavor in %flavors_to_build ; do
    cp -a kernel _kmod_build_${flavor}
        perl -pi -e "s|^KERNEL_BUILD_DIR =.*|KERNEL_BUILD_DIR = %{kernel_source $flavor}|" _kmod_build_${flavor}/usr/lpp/mmfs/src/config/env.mcr
done

%build
for flavor in %flavors_to_build ; do
    pushd _kmod_build_$flavor/usr/lpp/mmfs/src
    make World
    popd
done

%install
# install modules
for flavor in %flavors_to_build ; do
	pushd _kmod_build_$flavor/usr/lpp/mmfs/src
	mkdir 		 -p $RPM_BUILD_ROOT/lib/modules/%kverrel${flavor%default}/extra/gpfs/
	for i in tracedev.ko mmfslinux.ko mmfs26.ko; do
                install -m 644 gpl-linux/$i $RPM_BUILD_ROOT/lib/modules/%kverrel${flavor%default}/extra/gpfs/
        done
	mkdir 		 -p $RPM_BUILD_ROOT/usr/lpp/mmfs/bin
	install -m 755 bin/*%kverrel${flavor%default} $RPM_BUILD_ROOT/usr/lpp/mmfs/bin/
	popd
done
# install the rest
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
install -m 755 %{SOURCE100} $RPM_BUILD_ROOT%{_initrddir}/gpfs-kernel-setup

# Temporarily executable for stripping, fixed later in %%files.
chmod u+x $RPM_BUILD_ROOT/lib/modules/*/extra/*

%clean
rm -rf $RPM_BUILD_ROOT

%post 
/sbin/chkconfig --add gpfs-kernel-setup

%postun -p /sbin/ldconfig

%preun
if [ "$1" -eq 0 ]; then
	/sbin/chkconfig --del gpfs-kernel-setup
fi

%files
%defattr(-,root,root,-)
%{_initrddir}/gpfs-kernel-setup
#/usr/lpp/mmfs/bin/lxtrace
#/usr/lpp/mmfs/bin/dumpconv

%changelog
* Fri Aug 14 2009 Josko Plazonic <plazonic@math.princeton.edu>
- new gpfs version

* Mon Mar 30 2009 Josko Plazonic <plazonic@math.princeton.edu>
- initial build for rhel5

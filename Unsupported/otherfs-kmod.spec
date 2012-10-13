%define kmod_name otherfs

%define fsmods hfs hfsplus ufs reiserfs
%define fsdefines CONFIG_HFS_FS=m CONFIG_HFSPLUS_FS=m CONFIG_UFS_FS=m CONFIG_REISERFS_FS=m REISERFS_FS_XATTR=y REISERFS_FS_POSIX_ACL=y REISERFS_FS_SECURITY=n

Name:       %{kmod_name}-kmod
Version:    2.6.32
Release:    0.3%{?dist}
Summary:    Other file systems not included in stock RHEL6 kernel

License:    Distributable
Group:      System Environment/Kernel
URL:        http://www.kerneldrivers.org/

#Source is created from these files:
Source0:        other-fs-kmod/other-fs-2.6.32-279.5.2.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	%kernel_module_package_buildreqs
%kernel_module_package -n %{kmod_name}

%description 
We need a few more file systems then the ones included in stock rhel6.  This 
rpm contains them.

%prep
%setup -q -c -n %{kmod_name}-kmod-%{version}
mkdir source
mv fs/* source/
mkdir obj

%build
export EXTRA_CFLAGS='-DVERSION=\"%version\"'
for flavor in %flavors_to_build ; do
	echo Building for $flavor and target cpu %{_target_cpu} and kverrel = %kverrel
	rm -rf obj/$flavor
	cp -r source obj/$flavor
	for fs in %{fsmods}; do
		make -C %{kernel_source $flavor} M=$PWD/obj/$flavor/$fs %{fsdefines} modules
	done
done

%install
export INSTALL_MOD_PATH=$RPM_BUILD_ROOT
export INSTALL_MOD_DIR=extra/%{kmod_name}
for flavor in %flavors_to_build ; do
	for fs in %{fsmods}; do
		make -C %{kernel_source $flavor} modules_install M=$PWD/obj/$flavor/$fs SUBDIRS=$PWD/obj/$flavor/$fs
	done
done
# remove spurious modules files
find $RPM_BUILD_ROOT/lib/modules/ -type f -not -name \*.ko | xargs rm -f

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Sep 24 2012 Josko Plazonic <plazonic@math.princeton.edu>
- add reiserfs for rescue purpose

* Mon Dec 12 2011 Josko Plazonic <plazonic@math.princeton.edu>
- rebuild due to changed abi

* Fri Jul 09 2010 Josko Plazonic <plazonic@math.princeton.edu>
- initial build


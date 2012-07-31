%define kmod_name rdac

Name:       %{kmod_name}-kmod
Version:    09.03.0C05.0504
Release:    1%{?dist}
Summary:    LSI rdac engenio kernel modules
License:    Other
Group:      System Environment/Kernel
URL:        http://www.kerneldrivers.org/
Source0:        rdac-LINUX-%{version}-source.tar.gz
Patch1:		fixredhat.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	%kernel_module_package_buildreqs
%kernel_module_package -n %{kmod_name}

%description 
LSI rdac engenio kernel modules

%package -n rdac
Summary: RDAC
Group: System Environment/Base

%description -n rdac
RDAC programs and man pages

%prep
%setup -q -c -n %{kmod_name}-kmod-%{version}
mv linuxrdac-%{version} source
%patch1 -p0 -b .fixredhat
perl -pi -e 's|install -o root -g root|install|' source/Makefile
 
%build
export EXTRA_CFLAGS='-DVERSION=\"%version\"'
for flavor in %flavors_to_build ; do
	echo Building for $flavor and target cpu %{_target_cpu} and kverrel = %kverrel
	cp -r source $flavor
	make -C %{kernel_source $flavor} M=$PWD/$flavor modules
	make -C $flavor genuniqueid mppUtil
done

%install
export INSTALL_MOD_PATH=$RPM_BUILD_ROOT
export INSTALL_MOD_DIR=extra/%{kmod_name}
mkdir -p $RPM_BUILD_ROOT{/opt/mpp,%{_sbindir},%{_datadir}/man}
for flavor in %flavors_to_build ; do
	make -C %{kernel_source $flavor} modules_install M=$PWD/$flavor SUBDIRS=$PWD/$flavor
	make -C $flavor DEST_DIR=$RPM_BUILD_ROOT copyfiles
	make -C $flavor DEST_DIR=$RPM_BUILD_ROOT copyrpmfiles
done
# remove spurious modules files
find $RPM_BUILD_ROOT/lib/modules/ -type f -not -name \*.ko | xargs rm -f

%clean
rm -rf $RPM_BUILD_ROOT

%files -n rdac
/etc/mpp.conf
%dir /opt/mpp
/opt/mpp/.mppLnx_rpm_helpers
/opt/mpp/genuniqueid
/opt/mpp/lsvdev
/opt/mpp/mppMkInitrdHelper
/opt/mpp/mppSupport
/opt/mpp/mppiscsi_umountall
%{_sbindir}/mpp*
%{_datadir}/man/man1/mpp*
%{_datadir}/man/man9/RDAC*

%changelog
* Mon Dec 12 2011 Josko Plazonic <plazonic@math.princeton.edu>
- rebuild due to changed abi

* Fri Jul 09 2010 Josko Plazonic <plazonic@math.princeton.edu>
- initial build


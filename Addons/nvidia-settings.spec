# We use the driver version as a snapshot internal number
# The real version of the package remains 1.0
# This will prevent missunderstanding and versioning changes on the nvidia driver
%global nversion 260.19.12
#Possible replacement/complement:
#http://willem.engen.nl/projects/disper/

Name:           nvidia-settings
Version:        1.0
Release:        8%{?dist}
Summary:        Configure the NVIDIA graphics driver

Group:          Applications/System
License:        GPLv2+
URL:            ftp://download.nvidia.com/XFree86/nvidia-settings/
Source0:        ftp://download.nvidia.com/XFree86/nvidia-settings/nvidia-settings-%{nversion}.tar.bz2
Patch0:         nvidia-settings-256.35-validate.patch
Patch1:         03_do_not_exit_on_no_scanout.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{?fedora} > 11 || 0%{?rhel} > 5
ExclusiveArch: i686 x86_64
%else 0%{?fedora} == 11
ExclusiveArch: i586 x86_64
%else
ExclusiveArch: i386 x86_64
%endif

BuildRequires:  desktop-file-utils

BuildRequires:  gtk2-devel
#BuildRequires:  libXNVCtrl-devel
BuildRequires:  libXxf86vm-devel
BuildRequires:  libXext-devel
BuildRequires:  libXv-devel
#Needed for FBConfig table
#BuildRequires:  xorg-x11-drv-nvidia-devel
BuildRequires:   mesa-libGL-devel

Provides: %{name}-nversion = %{nversion}



%description
The nvidia-settings utility is a tool for configuring the NVIDIA graphics
driver.  It operates by communicating with the NVIDIA X driver, querying
and updating state as appropriate.

This communication is done with the NV-CONTROL X extension.
nvidia-settings is compatible with driver up to %{nversion}.

%prep
%setup -q -n nvidia-settings-%{nversion}
%patch0 -p1 -b .validate
%patch1 -p1 -b .noscanout
rm -rf src/libXNVCtrl/libXNVCtrl.a

sed -i -e 's|/usr/local|$(DESTDIR)/%{_prefix}|g' utils.mk
sed -i -e 's|-lXxf86vm|-lXxf86vm -ldl -lm|g' Makefile

%build
# no job control
pushd src/libXNVCtrl
  make
popd
make  \
  NVDEBUG=1 \
  NV_VERBOSE=1 \
  X_LDFLAGS="-L%{_libdir}" \
  CC_ONLY_CFLAGS="$RPM_OPT_FLAGS"


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications

# Desktop entry for nvidia-settings
desktop-file-install --vendor "" \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications/ \
    doc/nvidia-settings.desktop


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc doc/*.txt
%{_bindir}/nvidia-settings
%{_datadir}/applications/*nvidia-settings.desktop
%{_mandir}/man1/nvidia-settings.1.gz


%changelog
* Thu Oct 14 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.0-8
- Update internal to 260.19.12

* Sun Oct 10 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.0-7
- Update internal to 260.19.06
- Restore noscanout patch

* Mon Sep 06 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.0-6
- Update internal to 256.53

* Sat Jul 10 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.0-5
- Update internal to 256.35
- Use upstream desktop file (completed)
- Provides %%{name}-nversion internal

* Wed Apr 28 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.0-4
- Update internal to 195.36.24
- Avoid failure on NV_CTRL_NO_SCANOUT when not supported in legacy drivers. 

* Sun Feb 28 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.0-3.4
- Update internal version to 195.36.08
- Add patch for -lm

* Wed Oct 21 2009 kwizart < kwizart at gmail.com > - 1.0-3.1
- Update internal to 190.42

* Thu Jul 15 2009 kwizart < kwizart at gmail.com > - 1.0-3
- Update internal to 185.18.14

* Tue Mar  3 2009 kwizart < kwizart at gmail.com > - 1.0-2.1
- Update internal to 180.35

* Tue Jun 17 2008 kwizart < kwizart at gmail.com > - 1.0-2
- Update to 173.14.09
- Remove the locale patch

* Wed May 28 2008 kwizart < kwizart at gmail.com > - 1.0-1
- First Package for Fedora.


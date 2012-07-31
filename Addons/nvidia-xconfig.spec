%global nversion         260.19.06

Name:           nvidia-xconfig
Version:        1.0
Release:        5%{?dist}
Summary:        NVIDIA X configuration file editor

Group:          Applications/System
License:        GPLv2+
URL:            http://cgit.freedesktop.org/~aplattner/nvidia-xconfig/
Source0:        http://cgit.freedesktop.org/~aplattner/nvidia-xconfig/snapshot/nvidia-xconfig-%{nversion}.tar.bz2
Patch0:         nvidia-xconfig-1.0-default.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{?fedora} > 11 || 0%{?rhel} > 5
ExclusiveArch: i686 x86_64
%else 0%{?fedora} == 11
ExclusiveArch: i586 x86_64
%else
ExclusiveArch: i386 x86_64
%endif

BuildRequires: m4
Provides: %{name}-nversion = %{nversion}


%description
NVIDIA X configuration file editor.



%prep
%setup -q -n nvidia-xconfig-%{nversion}

sed -i -e 's|/usr/local|$(DESTDIR)/%{_prefix}|g' utils.mk


%build
make  \
  NVDEBUG=1 \
  NV_VERBOSE=1 \
  X_LDFLAGS="-L%{_libdir}" \
  CC_ONLY_CFLAGS="$RPM_OPT_FLAGS"


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

#We usually have it in sbin
mv $RPM_BUILD_ROOT%{_bindir}/nvidia-xconfig \
  $RPM_BUILD_ROOT%{_sbindir}
rmdir $RPM_BUILD_ROOT%{_bindir}



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING
%{_sbindir}/nvidia-xconfig
%{_mandir}/man1/nvidia-xconfig.1.*

%changelog
* Sun Oct 10 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.0-5
- Update internal version to 260.19.06

* Mon Sep 06 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.0-4
- Update internal version to 256.53

* Sat Jul 10 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.0-3
- Update internal version to 256.35
- Provides %%{name}-nversion

* Sun Feb 28 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.0-2
- Update internal version to 195.36.08

* Mon Oct 26 2009 kwizart < kwizart at gmail.com > - 1.0-1
- Update internal version to 190.42

* Wed May 28 2008 kwizart < kwizart at gmail.com > - 1.0-1.1
- First Package for Fedora.


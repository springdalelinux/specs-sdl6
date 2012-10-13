%{!?repo:%define repo core}

Summary: yum %{repo} repository configuration file
Name: puias-%{repo}
Version: 6
Release: 1.puias6.5
Group: System Environment/Base 
License: GPL
BuildRoot: %{_tmppath}/%{name}-root
BuildArch: noarch
Requires: yum puias-release /etc/pki/rpm-gpg/RPM-GPG-KEY-puias
%if "%{repo}" != "core"
Requires: puias-core
%if "%{repo}" != "addons"
Requires: puias-addons
%endif
%endif

%description
This rpm contains yum %{repo} repository configuration file.

%prep

%build

%install
mkdir -p $RPM_BUILD_ROOT/etc/yum.repos.d/

echo repo = %{repo}
%if "%{repo}" == "core"
cat > $RPM_BUILD_ROOT/etc/yum.repos.d/puias-%{version}-%{repo}.repo <<ENDCORECONFIG
[PUIAS_%{version}_%{repo}_Base]
name=PUIAS %{repo} Base \$releasever - \$basearch
mirrorlist=http://www.puias.princeton.edu/data/puias/\$releasever/\$basearch/os/mirrorlist
#baseurl=http://www.puias.princeton.edu/data/puias/\$releasever/\$basearch/os
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-puias

[PUIAS_%{version}_%{repo}_Updates]
name=PUIAS %{repo} Updates \$releasever - \$basearch
mirrorlist=http://www.puias.princeton.edu/data/puias/updates/\$releasever/en/os/mirrorlist
#baseurl=http://www.puias.princeton.edu/data/puias/updates/\$releasever/en/os/\$basearch
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-puias
ENDCORECONFIG

cat > $RPM_BUILD_ROOT/etc/yum.repos.d/puias-%{version}-%{repo}-debug.repo <<ENDCOREDEBUGCONFIG
[PUIAS_%{version}_%{repo}_Base_Debug]
name=PUIAS %{repo} Base \$releasever Debuginfo - \$basearch
mirrorlist=http://www.puias.princeton.edu/data/puias/\$releasever/\$basearch/debug/os/mirrorlist
#baseurl=http://www.puias.princeton.edu/data/puias/\$releasever/\$basearch/debug/os
gpgcheck=1
enabled=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-puias

[PUIAS_%{version}_%{repo}_Updates_Debug]
name=PUIAS %{repo} Updates \$releasever Debuginfo - \$basearch
mirrorlist=http://www.puias.princeton.edu/data/puias/updates/\$releasever/en/os/debug/\$basearch/mirrorlist
#baseurl=http://www.puias.princeton.edu/data/puias/updates/\$releasever/en/os/debug/\$basearch
gpgcheck=1
enabled=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-puias
ENDCOREDEBUGCONFIG

cat > $RPM_BUILD_ROOT/etc/yum.repos.d/puias-%{version}-%{repo}-source.repo <<ENDCORESOURCECONFIG
[PUIAS_%{version}_%{repo}_Base_Source]
name=PUIAS %{repo} Base \$releasever SRPMS - \$basearch
mirrorlist=http://www.puias.princeton.edu/data/puias/\$releasever/source/os/mirrorlist
#baseurl=http://www.puias.princeton.edu/data/puias/\$releasever/source/os
gpgcheck=1
enabled=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-puias

[PUIAS_%{version}_%{repo}_Updates_Source]
name=PUIAS %{repo} Updates \$releasever SRPMS - \$basearch
mirrorlist=http://www.puias.princeton.edu/data/puias/updates/\$releasever/en/os/SRPMS/mirrorlist
#baseurl=http://www.puias.princeton.edu/data/puias/updates/\$releasever/en/os/SRPMS
gpgcheck=1
enabled=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-puias
ENDCORESOURCECONFIG

%else
%if "%{repo}" == "addons"
cat > $RPM_BUILD_ROOT/etc/yum.repos.d/puias-%{version}-%{repo}.repo <<ENDREPOCONFIG
[PUIAS_%{version}_%{repo}]
name=PUIAS %{repo} Base \$releasever - \$basearch
mirrorlist=http://www.puias.princeton.edu/data/puias/\$releasever/\$basearch/os/Addons/mirrorlist
#baseurl=http://www.puias.princeton.edu/data/puias/%{repo}/\$releasever/\$basearch/os/Addons
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-puias

[PUIAS_%{version}_%{repo}_Updates]
name=PUIAS %{repo} Updates \$releasever - \$basearch
mirrorlist=http://www.puias.princeton.edu/data/puias/updates/\$releasever/en/%{repo}/\$basearch/mirrorlist
#baseurl=http://www.puias.princeton.edu/data/puias/updates/\$releasever/en/%{repo}/\$basearch
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-puias
ENDREPOCONFIG

%else
cat > $RPM_BUILD_ROOT/etc/yum.repos.d/puias-%{version}-%{repo}.repo <<ENDREPOCONFIG
[PUIAS_%{version}_%{repo}]
name=PUIAS %{repo} Base \$releasever - \$basearch
mirrorlist=http://www.puias.princeton.edu/data/puias/%{repo}/\$releasever/\$basearch/mirrorlist
#baseurl=http://www.puias.princeton.edu/data/puias/%{repo}/\$releasever/\$basearch
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-puias
ENDREPOCONFIG
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
/etc/yum.repos.d/puias*

%changelog
* Mon Nov 29 2010 Thomas Uphill <uphill@ias.edu>
- adding mirrorlist for all repos

* Tue Nov 16 2010 Josko Plazonic <plazonic@math.princeton.edu>
- initial build for PUIAS 6

* Tue Jul 17 2007 Josko Plazonic <plazonic@math.princeton.edu>
- variant for unsupported repo

* Mon Mar 26 2007 Josko Plazonic <plazonic@math.princeton.edu>
- first build

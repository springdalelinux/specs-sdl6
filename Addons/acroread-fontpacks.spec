%define __os_install_post %{nil}

%define acrodir /opt

%define debug_package %{nil}

Summary: Additional Font Packs for Adobe Reader
Name: AdobeReader_enu-fontpacks
Version: 9.1
Release: 1%{?dist}
License: Commercial
Group: Applications/Publishing
Source: FontPack910_chs_i486-linux.tar.bz2
Source1: FontPack910_jpn_i486-linux.tar.bz2
Source2: FontPack910_xtd_i486-linux.tar.bz2
Source3: FontPack910_cht_i486-linux.tar.bz2
Source4: FontPack910_kor_i486-linux.tar.bz2
Requires: AdobeReader_enu >= %{version}
AutoReqProv: no
BuildRoot: /var/tmp/%{name}-root
ExclusiveArch: %{ix86}

%description
This package contains all available Adobe Reader %{version} font packs

%prep
%setup -q -c -n %{name}-%{version} -a 1 -a 2 -a 3 -a 4

%build
echo Nothing to build here

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{acrodir}
for i in */*TAR; do
	tar -C $RPM_BUILD_ROOT%{acrodir} -xvf $i
done
rm -f $RPM_BUILD_ROOT%{acrodir}/{INSTALL,LICREAD.TXT}
rm -f $RPM_BUILD_ROOT%{acrodir}/Adobe/Reader9/Reader/intellinux/lib/libicu*
rm -f $RPM_BUILD_ROOT%{acrodir}/Adobe/Reader9/Resource/CMap/Identity-{H,V}
rm -f $RPM_BUILD_ROOT%{acrodir}/Adobe/Reader9/Resource/Font/MinionPro*
rm -f $RPM_BUILD_ROOT%{acrodir}/Adobe/Reader9/Resource/Font/MyriadPro*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc CHSKIT/LICREAD.TXT
%{acrodir}/Adobe/Reader9/Reader/intellinux/lib/lib*
%{acrodir}/Adobe/Reader9/Resource/*/*

%changelog
* Mon Dec 17 2007 Josko Plazonic <plazonic@math.princeton.edu>
- initial packaging

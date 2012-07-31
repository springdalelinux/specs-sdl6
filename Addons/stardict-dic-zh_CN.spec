Name: stardict-dic-zh_CN
Summary: Simplified Chinese(zh_CN) dictionaries for StarDict
Version: 2.4.2
Release: 6%{?dist}
Group: Applications/System
License: GPL+
URL: http://stardict.sourceforge.net

# Hi. Are you adding a dictionary here? Please be sure we have a clear license for it.
# The stardict page is _NOT_ a trusted source for licensing.
# Not sure? Don't include it, or email fedora-legal@redhat.com first.

# Cannot find licensing.
# Source0: http://downloads.sourceforge.net/stardict/stardict-cdict-gb-2.4.2.tar.bz2
# CEDICT license is non-free
# Source1: http://downloads.sourceforge.net/stardict/stardict-cedict-gb-2.4.2.tar.bz2
# Cannot find licensing
# Source2: http://downloads.sourceforge.net/stardict/stardict-langdao-ce-gb-2.4.2.tar.bz2
# Source3: http://downloads.sourceforge.net/stardict/stardict-langdao-ec-gb-2.4.2.tar.bz2
# Almost certainly not used with permission.
# Source4: http://downloads.sourceforge.net/stardict/stardict-oxford-gb-2.4.2.tar.bz2
# From upstream stardict, okay.
Source5: http://downloads.sourceforge.net/stardict/stardict-stardict1.3-2.4.2.tar.bz2
# From http://ftp.cdut.edu.cn/pub/linux/system/chinese/xdict/xdict.README
# GPL+
Source6: http://downloads.sourceforge.net/stardict/stardict-xdict-ce-gb-2.4.2.tar.bz2
Source7: http://downloads.sourceforge.net/stardict/stardict-xdict-ec-gb-2.4.2.tar.bz2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArchitectures: noarch

Requires: stardict >= 2.4.2

%description
Simplified Chinese(zh_CN) dictionaries for StarDict.
These dictionaries are included currently:
stardict1.3, xdict-ce-gb, xdict-ec-gb.
You can download more at: http://stardict.sourceforge.net

%prep
%setup -c -T -n %{name}-%{version}
# %%setup -q -n %{name}-%{version} -D -T -a 0
# %%setup -q -n %{name}-%{version} -D -T -a 1
# %%setup -q -n %{name}-%{version} -D -T -a 2
# %%setup -q -n %{name}-%{version} -D -T -a 3
# %%setup -q -n %{name}-%{version} -D -T -a 4
%setup -q -n %{name}-%{version} -D -T -a 5
%setup -q -n %{name}-%{version} -D -T -a 6
%setup -q -n %{name}-%{version} -D -T -a 7

%build

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/stardict/dic
cp -rf stardict-* ${RPM_BUILD_ROOT}%{_datadir}/stardict/dic/

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%{_datadir}/stardict/dic/*

%changelog
* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.4.2-4
- fix license tag
- remove dictionaries for which the licensing is unclear (or outright forbidden)

* Wed Jun 27 2007 Hu Zheng <zhu@redhat.com> - 2.4.2-3
- Separate spec files for each language's dictionaries.

* Fri Jun 22 2007 Hu Zheng <zhu@redhat.com> - 2.4.2-2
- Small fixes according to Parag AN's suggestion.

* Thu Jun 21 2007 Hu Zheng <zhu@redhat.com> - 2.4.2-1
- Initial build for Fedora


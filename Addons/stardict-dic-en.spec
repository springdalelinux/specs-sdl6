Name: stardict-dic-en
Summary: English(en) dictionaries for StarDict
Version: 2.4.2
Release: 7%{?dist}
Group: Applications/System
License: MIT
# The WordNet dictionary lives here:
# http://wordnet.princeton.edu
# Here is the license of that dictionary (MIT)
# http://wordnet.princeton.edu/license
URL: http://stardict.sourceforge.net

Source0: http://downloads.sourceforge.net/stardict/stardict-dictd_www.dict.org_wn-2.4.2.tar.bz2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArchitectures: noarch

Requires: stardict >= 2.4.2

%description
English(en) dictionaries for StarDict.
These dictionaries are included currently:
dictd_www.dict.org_wn.
You can download more at: http://stardict.sourceforge.net

%prep
%setup -c -T -n %{name}-%{version}
%setup -q -n %{name}-%{version} -D -T -a 0

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
* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.4.2-5
- use correct license tag

* Fri Sep  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.4.2-4
- fix license tag

* Wed Jun 27 2007 Hu Zheng <zhu@redhat.com> - 2.4.2-3
- Separate spec files for each language's dictionaries.

* Fri Jun 22 2007 Hu Zheng <zhu@redhat.com> - 2.4.2-2
- Small fixes according to Parag AN's suggestion.

* Thu Jun 21 2007 Hu Zheng <zhu@redhat.com> - 2.4.2-1
- Initial build for Fedora


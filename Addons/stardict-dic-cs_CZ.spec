%define dicname stardict-english-czech
Name: stardict-dic-cs_CZ
Summary: Czech dictionaries for StarDict
Version: 20100216
Release: 1%{?dist}
Group: Applications/Text
License: GFDL

URL: http://cihar.com/software/slovnik/
Source0: ftp://dl.cihar.com/slovnik/stable/%{dicname}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{dicname}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires: stardict >= 2

%description
Czech-English and English-Czech translation dictionaries for StarDict, a
GUI-based dictionary software.

%prep
%setup -q -c -n %{dicname}-%{version}

%build

%install
rm -rf ${RPM_BUILD_ROOT}
install -m 0755 -p -d ${RPM_BUILD_ROOT}%{_datadir}/stardict/dic
install -m 0644 -p  %{dicname}-%{version}/cz* ${RPM_BUILD_ROOT}%{_datadir}/stardict/dic/
install -m 0644 -p  %{dicname}-%{version}/en* ${RPM_BUILD_ROOT}%{_datadir}/stardict/dic/

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%doc %{dicname}-%{version}/README
%{_datadir}/stardict/dic/*


%changelog
* Tue Feb 16 2010 Petr Sklenar <psklenar@redhat.com> - 20100216-1
- New version of dictionary

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20081201-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 9 2009 Petr Sklenar <psklenar@redhat.com> - 20081201-2
- editing specfile - name and description

* Mon Jan 26 2009 Petr Sklenar <psklenar@redhat.com> - 20081201-1
- Initial build for Fedora


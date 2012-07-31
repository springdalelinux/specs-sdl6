Name:           stardict-dic-hi
Version:        3.0.1
Release:        6%{?dist}
Summary:        Hindi dictionary for stardict

Group:          Applications/System
License:        GPL+
URL:            http://stardict.sourceforge.net/
# URL http://ltrc.iiit.net/downloads/shabdanjali-stardict/shabdanjali-fedora.tgz
# usage: source generate-tarball.sh <version> <org-source-tarball> <initial-name-of-new-tarball>
# usage example: source generate-tarball.sh 3.0.1 shabdanjali-fedora.tgz shabdanjali-fedora
Source0:        shabdanjali-fedora-3.0.1-nobinary.tar.gz
Source1:        generate-tarball.sh
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       stardict
BuildArch:      noarch

%description
Hindi dictionary for stardict. The actual dictionary comes from
http://www.iiit.net/ltrc/Dictionaries/gen_eng_hin_hlp.html and Sriram
Chaudhry has converted it to a form usable by stardict.


%prep
%setup -q -n shabdanjali-fedora


%build
# Empty build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/stardict/dic
cp -p -rf shabdanjali* ${RPM_BUILD_ROOT}%{_datadir}/stardict/dic/

chmod 644 README

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README
%{_datadir}/stardict/dic/*


%changelog
* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 30 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.0.1-4
- Saving timestamp with -p.

* Thu Jan 30 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.0.1-3
- Added usage details for generate script

* Thu Jan 08 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.0.1-2
- Fixed the actual source link. Removed the binary rpm of no use inside
- tarball. Fixed the URL also.

* Sat Dec 06 2008 Rakesh Pandit <rakesh@fedoraproject.org> 3.0.1-1
- Initial build

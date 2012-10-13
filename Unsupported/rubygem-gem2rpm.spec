# Generated from gem2rpm-0.5.2.gem by gem2rpm -*- rpm-spec -*-
%global gemname gem2rpm

%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%global gemdocdir %{gemdir}/doc/%{gemname}-%{version}
%global rubyabi 1.8

Summary: Generate rpm specfiles from gems
Name: rubygem-%{gemname}
Version: 0.8.1
Release: 1%{?dist}
Group: Development/Languages
License: GPLv2+
%if 0%{?rhel} <= 5
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%endif
URL: https://github.com/lutter/gem2rpm/
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem
# git clone https://github.com/lutter/gem2rpm.git && cd gem2rpm && git checkout v0.8.1
# tar czvf gem2rpm-0.8.1-tests.tgz test/
Source1: %{gemname}-%{version}-tests.tgz
Requires: ruby(abi) = %{rubyabi}
Requires: ruby(rubygems)
Requires: ruby
Requires: /usr/bin/rpmdev-packager
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires: ruby(rubygems)
BuildRequires: ruby
BuildRequires: /usr/bin/rpmdev-packager
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
Generate source rpms and rpm spec files from a Ruby Gem.  The spec file
tries to follow the gem as closely as possible, and be compliant with the
Fedora rubygem packaging guidelines


%package doc
Summary:           Documentation for %{name}
Group:             Documentation
Requires:          %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -c -T
mkdir -p .%{gemdir}
gem install --local --install-dir .%{gemdir} \
            --bindir .%{_bindir} \
            --force %{SOURCE0}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
cp -a .%{gemdir}/* \
        %{buildroot}%{gemdir}/

mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x

#%%check
#tar xzvf %{SOURCE1} -C .%{geminstdir}
#pushd .%{geminstdir}
#testrb -Itest test/
#popd

%files
%dir %{geminstdir}
%{_bindir}/gem2rpm
%{geminstdir}/bin
%{geminstdir}/lib
%{geminstdir}/templates
%doc %{geminstdir}/LICENSE
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%doc %{gemdocdir}
%doc %{geminstdir}/README
%doc %{geminstdir}/AUTHORS

%changelog
* Thu Feb 09 2012 Vít Ondruch <vondruch@redhat.com> - 0.8.1-1
- Fix template for F17 and above.
- Fix release enumeration logic.

* Mon Jan 23 2012 Vít Ondruch <vondruch@redhat.com> - 0.8.0-1
- Updated to gem2rpm 0.8.0.

* Thu Jun 30 2011 Vít Ondruch <vondruch@redhat.com> - 0.7.1-1
- Updated to the 0.7.1 version.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 28 2010 Michael Stahnke <stahnma@fedoraproject.org> - 0.6.0-5
- Breaking into a main and doc package

* Tue Nov 24 2009 David Lutterkort <lutter@redhat.com> - 0.6.0-4
- Add gemdocdir contents as doc

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Oct  6 2008 David Lutterkort <dlutter@redhat.com> - 0.6.0-1
- New version

* Tue Mar 11 2008 David Lutterkort <dlutter@redhat.com> - 0.5.3-1
- Bring in accordance with Fedora guidelines

* Thu Jan  3 2008 David Lutterkort <dlutter@redhat.com> - 0.5.2-2
- Own geminstdir
- Fix Source URL

* Mon Dec 10 2007 David Lutterkort <dlutter@redhat.com> - 0.5.1-1
- Initial package

%global ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname rspec
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary: Behaviour driven development (BDD) framework for Ruby
Name: rubygem-%{gemname}
Version: 1.3.1
Release: 1%{?dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://rspec.info
Source0: http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
Patch0:  rubygem-rspec-1.3.1-RakeFileUtils_renamed_to_FileUtilsExt.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: rubygems, ruby(abi)  = 1.8
BuildRequires: rubygems, ruby
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
RSpec is a behaviour driven development (BDD) framework for Ruby.  


%prep
%setup -q -c -T
gem install \
	-V \
	--install-dir $(pwd)%{gemdir} \
	--bindir $(pwd)%{_bindir} \
	--force \
	--rdoc \
	%{SOURCE0}


pushd .%{geminstdir}
%patch0 -p1
popd

find . -type f | xargs chmod ugo+r

%build

%install
mkdir -p %{buildroot}%{gemdir}
cp -a .%{_prefix}/* %{buildroot}%{_prefix}/

find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{_bindir}/*
%{gemdir}/gems/%{gemname}-%{version}/
%doc %{gemdir}/doc/%{gemname}-%{version}
#%doc %{geminstdir}/*.txt
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec


%changelog
* Mon Mar 09 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.3.1-1
- Update from Marek Goldmann <mgoldman@redhat.com>
  - Updated to 1.3.1
  - Patch to make it work with Rake >= 0.9.0.beta.0

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Apr 16 2010 Michael Stahnke <stahnma@fedpraproject.org> - 1.3.0-2
- Removed 404 URL in the description (bug 515042)

* Fri Apr 09 2010 Michael Stahnke <stahnma@fedpraproject.org> - 1.3.0-1
- Updated to 1.3.0

* Wed Dec 09 2009 Michael Stahnke <stahnma@fedoraproject.org> - 1.2.9-1
- New Version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Michael Stahnke <stahnma@fedoraproject.org> - 1.2.7-1
- New Version

* Fri Mar 27 2009 Michael Stahnke <stahnma@fedoraproject.org> - 1.2.2-1
- New Version 

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 08 2008 Michael Stahnke <stahnma@fedoraproject.org> - 1.1.11-1
- New Version

* Mon Nov 03 2008 Michael Stahnke <stahnma@fedoraproject.org> - 1.1.8-3
- Updating to require ruby(abi)

* Mon Oct 13 2008 Michael Stahnke <stahnma@fedoraproject.org> - 1.1.8-1
- New version

* Wed May 14 2008 Michael Stahnke <stahnma@fedoraproject.org> - 1.1.3-1
- Initial package

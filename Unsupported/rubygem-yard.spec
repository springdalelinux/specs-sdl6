%define gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define gemname yard
%define geminstdir %{gemdir}/gems/%{gemname}-%{version}

%define rubyabi 1.8 

Name: rubygem-%{gemname}
Summary: Documentation tool for consistent and usable documentation in Ruby
Version: 0.7.2
Release: 1%{?dist}
Group: Development/Languages
License: MIT and (GPLv2 or Ruby)
URL: http://yardoc.org

Source0: http://rubygems.org/gems/yard-0.7.2.gem
Requires: rubygems
Requires: ruby(abi) = %{rubyabi}
BuildRequires: rubygems
BuildRequires: rubygem(rake)
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(RedCloth)
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
YARD is a documentation generation tool for the Ruby programming language.
It enables the user to generate consistent, usable documentation that can be
exported to a number of formats very easily, and also supports extending for
custom Ruby constructs such as custom class level definitions.


%prep
%setup -q -T -c

%build

%install
mkdir -p %{buildroot}%{gemdir}
mkdir -p %{buildroot}/%{_bindir}

gem install --local --install-dir ./%{gemdir} \
            --force --rdoc %{SOURCE0}
cp -a ./%{gemdir}/* %{buildroot}/%{gemdir}/. 
mv %{buildroot}%{gemdir}/bin/* %{buildroot}/%{_bindir}
rmdir %{buildroot}%{gemdir}/bin
find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x

%check
pushd .%{geminstdir} 
rake spec || : 

%files
%{_bindir}/yardoc
%{_bindir}/yri
%{_bindir}/yard
%dir %{geminstdir} 
%{geminstdir}/bin
%{geminstdir}/lib
%{geminstdir}/templates
%{geminstdir}/.yardopts
%doc %{geminstdir}/LEGAL

%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%doc %{geminstdir}/LICENSE 
%doc %{geminstdir}/README.md
%doc %{geminstdir}/Rakefile
%doc %{geminstdir}/ChangeLog
%doc %{geminstdir}/benchmarks 
%doc %{geminstdir}/spec
%doc %{geminstdir}/docs
%doc %{gemdir}/doc/%{gemname}-%{version}


%changelog
* Mon Jul 25 2011 Mo Morsi <mmorsi@redhat.com> - 0.7.2-1
- update to latest upstream release
- fixes to conform to fedora guidelines

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 22 2010 Mohammed Morsi <mmorsi@redhat.com> - 0.5.3-3
- fixed dependencies/package issues according to guidelines

* Mon Feb 08 2010 Mohammed Morsi <mmorsi@redhat.com> - 0.5.3-2
- cleaned up macros, other package guideline compliance fixes
- corrected license, added MIT
- include all files and docs, added check/test section

* Mon Feb 08 2010 Mohammed Morsi <mmorsi@redhat.com> - 0.5.3-1
- Initial package


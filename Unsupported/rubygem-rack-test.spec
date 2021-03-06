%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname rack-test
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary:        Simple testing API built on Rack
Name:           rubygem-%{gemname}
Version:        0.5.4
Release:        1%{?dist}
Group:          Development/Languages
License:        MIT
URL:            http://gitrdoc.com/brynary/rack-test/tree/master
Source0:        http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       ruby(abi) = 1.8
Requires:       rubygems
BuildRequires:  rubygems
BuildRequires:  rubygem(rack) >= 0.9.1
BuildRequires:  rubygem(rake)
BuildRequires:  rubygem(rspec)
BuildRequires:  rubygem(sinatra)
BuildArch:      noarch
Provides:       rubygem(%{gemname}) = %{version}

%description
Rack::Test is a small, simple testing API for Rack apps. It can be used on its
own or as a reusable starting point for Web frameworks and testing libraries
to build on. Most of its initial functionality is an extraction of Merb 1.0's
request helpers feature.


%prep


%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{gemdir}
gem install --local --install-dir $RPM_BUILD_ROOT%{gemdir} \
        --force --rdoc %{SOURCE0}
sed -i -e "s|~>|>=|"  $RPM_BUILD_ROOT%{geminstdir}/spec/spec_helper.rb
rm  $RPM_BUILD_ROOT%{geminstdir}/.gitignore
rm  $RPM_BUILD_ROOT%{geminstdir}/.document

%check
(cd %{buildroot}%{geminstdir}; rake spec)

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%dir %{geminstdir}
%{geminstdir}/lib
%{geminstdir}/spec
%{geminstdir}/Rakefile
%doc %{gemdir}/doc/%{gemname}-%{version}
%doc %{geminstdir}/README.rdoc
%doc %{geminstdir}/MIT-LICENSE.txt
%doc %{geminstdir}/History.txt
%doc %{geminstdir}/Thorfile
%doc %{geminstdir}/%{gemname}.gemspec
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec


%changelog

* Wed Sep 08 2010 Michal Fojtik <mfojtik@redhat.com> - 0.5.4-1
- Update to 0.5.4

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 30 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.4.0-1
- Update to 0.4.0
- Drop useless sitelib macro

* Fri Jun 26 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.3.0-3
- Get rid of duplicate files (thanks to Mamoru Tasaka)

* Mon Jun 08 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.3.0-2
- Fix up documentation list
- Depend on ruby(abi)
- Replace defines with globals

* Fri Jun 05 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.3.0-1
- Package generated by gem2rpm
- Fix up License

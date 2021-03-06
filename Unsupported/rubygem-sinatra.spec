%global ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname sinatra
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary:        Ruby-based web application framework
Name:           rubygem-%{gemname}
Version:        1.2.6
Release:        1%{?dist}
Group:          Development/Languages
License:        MIT
URL:            http://sinatra.rubyforge.org
Source0:        http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       ruby(abi) = 1.8
Requires:       rubygems
Requires:       rubygem(rack) >= 0.9.1
Requires:       rubygem(tilt)
Requires:       rubygem(rack-test) >= 0.3.0
BuildRequires:  rubygems
BuildArch:      noarch
Provides:       rubygem(%{gemname}) = %{version}
Epoch:          1

%description
Sinatra is a DSL intended for quickly creating web-applications in Ruby
with minimal effort.


%prep


%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{gemdir}
gem install --local --install-dir $RPM_BUILD_ROOT%{gemdir} \
        --force --rdoc %{SOURCE0}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%dir %{geminstdir}
%{geminstdir}/lib
%{geminstdir}/sinatra.gemspec
%{geminstdir}/test
%{geminstdir}/Rakefile
%doc %{gemdir}/doc/%{gemname}-%{version}
%doc %{geminstdir}/README.rdoc
%doc %{geminstdir}/README.*.rdoc
%doc %{geminstdir}/LICENSE
%doc %{geminstdir}/AUTHORS
%doc %{geminstdir}/CHANGES
%doc %{geminstdir}/Gemfile
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec


%changelog
* Thu Feb 10 2011 Michal Fojtik <mfojtik@redhat.com> - 1.2.6-1
- Version bump

* Thu Feb 10 2011 Michal Fojtik <mfojtik@redhat.com> - 1.2.0-1
- Version bump

* Thu Feb 10 2011 Michal Fojtik <mfojtik@redhat.com> - 1.1.2-3
- Added tilt dependency

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 10 2011 Michal Fojtik <mfojtik@redhat.com> - 1.1.2-1
- Version bump

* Thu Mar 25 2010 Michal Fojtik <mfojtik@redhat.com> - 1.0-1
- Sinatra now uses Tilt for rendering templates
- New helper methods
- New argument to specify the address to bind to
- Speed improvement in rendering templates

* Thu Feb 15 2010 Michal Fojtik <mfojtik@redhat.com> - 0.9.4-2
- Downgrade-Release

* Thu Jan 07 2010 Michal Fojtik <mfojtik@redhat.com> - 0.10.1-1
- Version-Release
- Added jp README

* Fri Jun 26 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.9.2-3
- Get rid of duplicate files (thanks to Mamoru Tasaka)

* Mon Jun 08 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.9.2-2
- Fix up documentation list
- Bring tests back
- Depend on ruby(abi)
- Replace defines with globals

* Fri Jun 05 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.9.2-1
- Package generated by gem2rpm
- Don't ship tests
- Fix up License

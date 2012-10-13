# Generated from rest-client-1.3.1.gem by gem2rpm -*- rpm-spec -*-
%global ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname rest-client
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary: Simple REST client for Ruby
Name: rubygem-%{gemname}
Version: 1.6.1
Release: 2%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/archiloque/rest-client
Source0: http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: ruby(abi) = 1.8
Requires: rubygems
Requires: rubygem(mime-types) >= 1.16
BuildRequires: rubygems
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
A simple Simple HTTP and REST client for Ruby, inspired by the Sinatra
microframework style of specifying actions: get, put, post, delete.


%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
gem install --local --install-dir %{buildroot}%{gemdir} \
            --force --rdoc %{SOURCE0}
mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}%{gemdir}/bin/* %{buildroot}/%{_bindir}
rmdir %{buildroot}%{gemdir}/bin
find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{_bindir}/restclient
%dir %{geminstdir}
%{geminstdir}/bin
%{geminstdir}/lib
%doc %{geminstdir}/README.rdoc
%doc %{geminstdir}/Rakefile
%doc %{geminstdir}/history.md
%doc %{geminstdir}/VERSION
%doc %{geminstdir}/spec
%doc %{gemdir}/doc/%{gemname}-%{version}
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec


%changelog
* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 08 2010 Michal Fojtik <mfojtik@redhat.com> - 1.6.1-1
- New version release

* Wed Mar 03 2010 Michal Fojtik <mfojtik@redhat.com> - 1.4.0-6
- New version release

* Mon Feb 17 2010 Michal Fojtik <mfojtik@redhat.com> - 1.3.1-5
- Added %dir %{geminstdir} into spec file

* Mon Feb 17 2010 Michal Fojtik <mfojtik@redhat.com> - 1.3.1-4
- Marked README.rdoc, history.md and spec/ as %doc

* Mon Feb 16 2010 Michal Fojtik <mfojtik@redhat.com> - 1.3.1-3
- Fixed licence (MIT)
- Fixed duplicated files in spec
- Replaced %define with %global

* Mon Feb 16 2010 Michal Fojtik <mfojtik@redhat.com> - 1.3.1-2
- Fixed spec filename
- Added Ruby dependency

* Mon Feb 16 2010 Michal Fojtik <mfojtik@redhat.com> - 1.3.1-1
- Initial package



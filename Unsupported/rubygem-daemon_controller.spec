%define ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%define gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define gemname daemon_controller
%define geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary:        A library for robust daemon management
Name:           rubygem-%{gemname}
Version:        0.2.5
Release:        1%{?dist}
Group:          Development/Languages
License:        Other
URL:            http://rubygems.org/gems/daemon_controller
Source0:        http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       rubygems
Requires:	ruby(abi) = 1.8
Requires:       rubygem(rake)
BuildRequires:  rubygems
BuildRequires:  rubygem(rake)
BuildArch:      noarch
Provides:       rubygem(%{gemname}) = %{version}

%description
*daemon_controller* is a library for starting and stopping specific daemons
programmatically in a robust, race-condition-free manner.

It's not a daemon monitoring system like God or Monit. It's also not a library
for writing daemons.

%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.


%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
gem install --local --install-dir %{buildroot}%{gemdir} \
            --force --rdoc %{SOURCE0}

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc %{geminstdir}/README*
%doc %{geminstdir}/LICENSE.txt
%dir %{geminstdir}/
%{geminstdir}/lib
%{geminstdir}/daemon_controller.gemspec
%{geminstdir}/spec
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%defattr(-, root, root, -)
%{gemdir}/doc/%{gemname}-%{version}


%changelog
* Fri Jan 14 2010 Josko Plazonic <plazonic@math.princeton.edu>
- initial build

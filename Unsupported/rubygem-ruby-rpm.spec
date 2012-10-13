%global ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname ruby-rpm
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary:        Ruby bindings for RPM =  Linux package manager
Name:           rubygem-%{gemname}
Version:        1.3.0
Release:        1%{?dist}
Group:          Development/Languages/Ruby
License:        GPLv2+ or Ruby
URL:            http://gitorious.org/ruby-rpm
Source0:       	http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  ruby-devel 
BuildRequires:  rubygems
BuildRequires:  rpm-devel 
BuildRequires:  popt-devel 
BuildRequires:  db4-devel
Requires:       ruby(abi) = 1.8
Requires:       rubygems
Provides:       rubygem(%{gemname}) = %{version}

%description
Provides bindings for accessing RPM packages and databases from Ruby. It
includes the low-level C API to talk to rpm as well as Ruby classes to
model the various objects that RPM deals with (such as packages,
dependencies, and files).

%prep

%build
mkdir -p ./%{gemdir}
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
gem install \
        --local \
        --install-dir ./%{gemdir} \
        -V --force --rdoc \
        %{SOURCE0}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
mv  ./%{gemdir}/* %{buildroot}%{gemdir}/

rm -rf %{buildroot}%{geminstdir}/ext

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)

%{geminstdir}/lib
%dir %{geminstdir}
%doc %{geminstdir}/CHANGELOG.rdoc
%doc %{geminstdir}/README.rdoc
%{gemdir}/cache/%{gemname}-%{version}.gem
%doc %{gemdir}/specifications/%{gemname}-%{version}.gemspec
%doc %{gemdir}/doc/%{gemname}-%{version}

%changelog


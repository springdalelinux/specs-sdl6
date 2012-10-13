%global ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname syntax
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary:        Ruby library for performing simple syntax highlighting
Name:           rubygem-%{gemname}
Version:        1.0.0
Release:        4%{?dist}
Group:          Development/Languages
License:        Public Domain
URL:            http://syntax.rubyforge.org/
Source0:        http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
Source1:        %{gemname}-LICENSE
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       ruby(abi) = 1.8
Requires:       rubygems
BuildRequires:  rubygems
BuildArch:      noarch
Provides:       rubygem(%{gemname}) = %{version}

%description
Syntax is a lexical analysis framework. It supports pluggable syntax
modules, and comes with modules for Ruby, XML, and YAML.


%prep
install -pm 0644 %{SOURCE1} LICENSE


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
%{geminstdir}/
%doc %{gemdir}/doc/%{gemname}-%{version}
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec
%doc LICENSE


%changelog
* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 08 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 1.0.0-2
- Bring tests back
- Depend on ruby(abi)
- Replace defines with globals

* Fri Jul 05 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 1.0.0-1
- Package generated by gem2rpm
- Don't ship tests
- Fix up License
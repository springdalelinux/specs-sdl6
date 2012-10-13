# Generated from activesupport-1.4.4.gem by gem2rpm -*- rpm-spec -*-
%define ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%define gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define gemname activemodel
%define geminstdir %{gemdir}/gems/%{gemname}-%{version}

%define rubyabi 1.8

Summary: A toolkit for building modeling frameworks like Active Record and Active Resource
Name: rubygem-%{gemname}
Epoch: 1
Version: 3.0.3
Release: 2%{?dist}
Group: Development/Languages
License: MIT
URL: http://rubygems.org/gems/activemodel

Source0: http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: rubygems
Requires: ruby(abi) = %{rubyabi}
BuildRequires: rubygems
BuildRequires(check): rubygem(rake)
BuildRequires(check): rubygem(mocha)
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
A toolkit for building modeling frameworks like Active Record and Active 
Resource. Rich support for attributes, callbacks, validations, observers, 
serialization, internationalization, and testing.

%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
gem install --local --install-dir %{buildroot}%{gemdir} \
            --force --rdoc %{SOURCE0}

# Fix anything executable that does not have a shebang
for file in `find %{buildroot}/%{geminstdir} -type f -perm /a+x`; do
    [ -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 644 $file
done

# Find files with a shebang that do not have executable permissions
for file in `find %{buildroot}/%{geminstdir} -type f ! -perm /a+x -name "*.rb"`; do
    [ ! -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 755 $file
done

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%dir %{geminstdir}
%doc %{geminstdir}/CHANGELOG
%doc %{geminstdir}/MIT-LICENSE
%doc %{geminstdir}/README.rdoc
%{geminstdir}/lib
%doc %{gemdir}/doc/%{gemname}-%{version}
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec


%changelog
* Tue Jan 25 2011 Josko Plazonic <plazonic@math.princeton.edu>
- initial build

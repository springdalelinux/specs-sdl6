%define ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%define gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define gemname mocha
%define geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary:        Mocking and stubbing library
Name:           rubygem-%{gemname}
Version:        0.9.8
Release:        1%{?dist}
Group:          Development/Languages
License:        MIT and Ruby
URL:            http://mocha.rubyforge.org
Source0:        http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       rubygems
Requires:	ruby(abi) = 1.8
Requires:       rubygem(rake)
BuildRequires:  rubygems
BuildRequires:  rubygem(rake)
BuildRequires:  zip
BuildArch:      noarch
Provides:       rubygem(%{gemname}) = %{version}

%description
Mocking and stubbing library with JMock/SchMock syntax, which allows mocking
and stubbing of methods on real (non-mock) classes.

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

%check 
cd %{buildroot}%{geminstdir}
rake test

%files
%defattr(-, root, root, -)
%doc %{geminstdir}/COPYING
%doc %{geminstdir}/README
%doc %{geminstdir}/MIT-LICENSE
%doc %{geminstdir}/RELEASE
%dir %{geminstdir}/
%{geminstdir}/lib
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%defattr(-, root, root, -)
%{gemdir}/doc/%{gemname}-%{version}
%{geminstdir}/Rakefile
%{geminstdir}/examples
%{geminstdir}/test


%changelog
* Sun Aug 29 2010 Michael Stahnke <stahnma@fedoraproject.org> - 0.9.8-1
- Fixed odd naming in BR
- Updating to 0.9.8
- Breaking into -doc package as well
- Adding tests

* Thu Jul 23 2009 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.9.7-1
- New upstream version

* Mon Apr 27 2009 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.9.5-1
- New upstream version

* Sun Feb 01 2009 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.9.1-4
- Mark files as %%doc

* Thu Oct 30 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.9.1-3
- Use gem instead of tgz

* Sat Oct 25 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.9.1-2
- Fix license

* Sat Oct 25 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.9.1-1
- New upstream version
- Fix license not being marked as %%doc

* Mon Sep 08 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.9.0-2
- Add ruby(abi) = 1.8 requirement

* Sat Aug 23 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.9.0-1
- New upstream version
- Initial package for review

* Sun Jul 13 2008 root <root@oss1-repo.usersys.redhat.com> - 0.5.6-1
- Initial package

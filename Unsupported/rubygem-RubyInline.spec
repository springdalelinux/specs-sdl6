# Generated from RubyInline-3.8.3.gem by gem2rpm -*- rpm-spec -*-
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname RubyInline
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

%global rubyabi 1.8

Summary: Write foreign code within your ruby code
Name: rubygem-%{gemname}
Version: 3.8.4
Release: 3%{?dist}
Group: Development/Languages
License: MIT
URL: http://www.zenspider.com/ZSS/Products/RubyInline/
Source0: http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: rubygem(ZenTest)
Requires: gcc, ruby-devel
Requires: ruby(rubygems)
Requires: ruby(abi) = %{rubyabi}
BuildRequires: ruby(rubygems)
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires: rubygem(ZenTest)
BuildRequires: ruby-devel
BuildRequires: rubygem(rake)
BuildRequires: rubygem(hoe)
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
Inline allows you to write foreign code within your ruby code. It
automatically determines if the code in question has changed and
builds it only when necessary. The extensions are then automatically
loaded into the class/module that defines it.

%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%prep
%setup -q -c -T

%build
mkdir -p .%{gemdir}
gem install -V \
  --local \
  --install-dir $(pwd)/%{gemdir} \
  --force --rdoc \
  %{SOURCE0}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
cp -a .%{gemdir}/* %{buildroot}%{gemdir}/

# These are all over the map - some executable that shouldn't be, needless
# shebangs, etc. Drop all the shebangs and set a standard permission.
find %{buildroot}%{geminstdir} -type f | \
  xargs -n 1 sed -i  -e '/^#!\/usr\/.*\/ruby.*/d'
# Ships with extremely tight permissions, bring them inline with other gems
find %{buildroot}%{geminstdir} -type f | \
  xargs chmod 0644

%clean
rm -rf %{buildroot}

%check
pushd .%{geminstdir}
rake test

%files
%defattr(-,root,root,-)
%doc %{geminstdir}/History.txt
%doc %{geminstdir}/Manifest.txt
%doc %{geminstdir}/README.txt
%dir %{geminstdir}
%{geminstdir}/lib
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%defattr(-,root,root,-)
%{geminstdir}/Rakefile
%{geminstdir}/test
%{geminstdir}/demo
%{geminstdir}/example2.rb
%{geminstdir}/example.rb
%{geminstdir}/tutorial
%{gemdir}/doc/%{gemname}-%{version}

%changelog
* Mon Aug 08 2011 Mo Morsi <mmorsi@redhat.com> - 3.8.4-3
- replace BR(check) with BR

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 24 2010 Matthew Kent <mkent@magoazul.com> - 3.8.4-1
- New upstream version.

* Thu Nov 26 2009 Matthew Kent <mkent@magoazul.com> - 3.8.3-4
- Add Requires for gcc and ruby-devel, library useless without them.

* Thu Nov 26 2009 Matthew Kent <mkent@magoazul.com> - 3.8.3-3
- Drop redundant BR for gcc (#540791)
- Leave examples as upstream intended (#540791)

* Mon Nov 23 2009 Matthew Kent <mkent@magoazul.com> - 3.8.3-2
- Remove unused ruby_sitelib macro

* Mon Nov 16 2009 Matthew Kent <mkent@magoazul.com> - 3.8.3-1
- Initial package

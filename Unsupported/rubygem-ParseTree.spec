# Generated from ParseTree-3.0.4.gem by gem2rpm -*- rpm-spec -*-
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname ParseTree
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

%global rubyabi 1.8

Summary: Extracts the parse tree for a class/method and returns an s-expression
Name: rubygem-%{gemname}
Version: 3.0.5
Release: 3%{?dist}
Group: Development/Languages
License: MIT
URL: http://parsetree.rubyforge.org/
Source0: http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Reported upstrea via
# http://rubyforge.org/tracker/?func=detail&aid=27491&group_id=439&atid=1780
Patch0: rubygem-ParseTree-3.0.4-minitest.patch
Requires: rubygem(RubyInline)
Requires: rubygem(sexp_processor)
Requires: ruby(rubygems)
Requires: ruby(abi) = %{rubyabi}
BuildRequires: ruby(rubygems)
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires: rubygem(rake)
BuildRequires: rubygem(hoe)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(RubyInline)
BuildRequires: rubygem(sexp_processor)
BuildRequires: rubygem(ruby2ruby)
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
ParseTree is a C extension (using RubyInline) that extracts the parse
tree for an entire class or a specific method and returns it as a
s-expression (aka sexp) using ruby's arrays, strings, symbols, and
integers.

%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%prep
%setup -q -c -T

mkdir -p .%{gemdir}
gem install -V \
  --local \
  --install-dir $(pwd)/%{gemdir} \
  --force --rdoc \
  %{SOURCE0}

pushd .%{geminstdir}
%patch0 -p0

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
cp -a .%{gemdir}/* %{buildroot}%{gemdir}/

mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}%{gemdir}/bin/* %{buildroot}/%{_bindir}
rmdir %{buildroot}%{gemdir}/bin
find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x

rm -f %{buildroot}%{geminstdir}/.require_paths

# Drop the standalone mode for tests - won't run that way due to missing 
# rubygems require anyway. Some shebangs in libraries as well.
find %{buildroot}%{geminstdir}/{test,lib} -type f | \
  xargs -n 1 sed -i  -e '/^#!\/usr\/.*\/ruby.*/d'
find %{buildroot}%{geminstdir}/{bin,demo} -type f | \
  xargs -n 1 sed -i -e 's"^#!/usr/local/bin/ruby"#!/usr/bin/ruby"'
# Ships with extremely tight permissions, bring them inline with other gems
find %{buildroot}%{geminstdir} -type f | \
  xargs chmod 0644
find %{buildroot}%{geminstdir}/{bin,demo,validate.sh} -type f | \
  xargs chmod 0755

%clean
rm -rf %{buildroot}

%check
pushd .%{geminstdir}
# Don't muck within home directories, also reported upstream
sed -i 's^"~/.ruby_inline"^"inline_tmp"^' Rakefile test/test_parse_tree.rb
# Builds in home by default
export INLINEDIR=inline_tmp
rake test

%files
%defattr(-,root,root,-)
%{_bindir}/parse_tree_abc
%{_bindir}/parse_tree_audit
%{_bindir}/parse_tree_deps
%{_bindir}/parse_tree_show
%doc %{geminstdir}/History.txt
%doc %{geminstdir}/Manifest.txt
%doc %{geminstdir}/README.txt
%dir %{geminstdir}
%{geminstdir}/bin
%{geminstdir}/lib
# Script creates a circular dependency and is primarily for development
# Included, but it's dependencies aren't met.
#%{geminstdir}/lib/gauntlet_parsetree.rb
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec
# Ignore development related files shipped in gem
%exclude %{geminstdir}/validate.sh

%files doc
%defattr(-,root,root,-)
%{geminstdir}/Rakefile
%{geminstdir}/test
%{geminstdir}/.autotest
# Ignore non functioning demo
%exclude %{geminstdir}/demo
%{gemdir}/doc/%{gemname}-%{version}

%changelog
* Mon Aug 08 2011 Mo Morsi <mmorsi@redhat.com> - 3.0.5-3
- Replace BR(check) with BR
- Fix missing files

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue May 4 2010 Matthew Kent <mkent@magoazul.com> - 3.0.5-1
- New upstream version - minor bugfix for NODE_METHOD.

* Thu Dec 3 2009 Matthew Kent <mkent@magoazul.com> - 3.0.4-4
- Drop needless versions from Requires (#541807).
- Exclude demo/ for now as it's non functional (#541807).

* Mon Nov 30 2009 Matthew Kent <mkent@magoazul.com> - 3.0.4-3
- Remove exclude for gauntlet_parsetree.rb, let user deal with dependencies if
  they need it.

* Sun Nov 29 2009 Matthew Kent <mkent@magoazul.com> - 3.0.4-2
- Exclude gauntlet_parsetree.rb as it introduces a circular dependency.

* Mon Nov 16 2009 Matthew Kent <mkent@magoazul.com> - 3.0.4-1
- Initial package

# Generated from haml-2.2.14.gem by gem2rpm -*- rpm-spec -*-
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname haml
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary: An elegant, structured XHTML/XML templating engine
Name: rubygem-%{gemname}
Version: 3.1.2
Release: 2%{?dist}
Group: Development/Languages
License: MIT and WTFPL
URL: http://haml-lang.com/
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem

# interim fix for https://github.com/nex3/haml/issues/403
Patch0: haml-issue-403-bugfix.patch

Requires: rubygems
Requires: ruby(abi) = 1.8
# for html2haml
Requires: rubygem(hpricot)
Requires: rubygem(yard) >= 0.5.3
Requires: rubygem(maruku) >= 0.5.9
Requires: rubygem(fssm)
Requires: rubygem(sass)

BuildRequires: rubygems
BuildRequires: ruby
BuildRequires: rubygem(rails)
BuildRequires: rubygem(hpricot)
BuildRequires: rubygem(erubis)
BuildRequires: rubygem(ruby_parser)

BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
Haml (HTML Abstraction Markup Language) is a layer on top of XHTML or XML
that's designed to express the structure of XHTML or XML documents in a
non-repetitive, elegant, easy way, using indentation rather than closing
tags and allowing Ruby to be embedded with ease.
It was originally envisioned as a plugin for Ruby on Rails, but it can
function as a stand-alone templating engine.


%prep
%setup -q -c -T
%{__mkdir_p} .%{gemdir}
gem install --local --install-dir .%{gemdir} --force -V --rdoc %{SOURCE0}

pushd .%{geminstdir}
%patch0
popd

%build

#check
#pushd %{buildroot}%{geminstdir}
## The following -path list is from Rakefile
#find * \
# -path 'test/*/*_test.rb' \
# -not -path 'test/rails/*' \
# -not -path 'test/plugins/*' \
# -not -path 'test/haml/spec/*' | \
#while read f
#do
#  ruby $f
#done
#popd

%install
mkdir -p %{buildroot}%{gemdir}
mv .%{gemdir}/* %{buildroot}%{gemdir}

mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}%{gemdir}/bin/* %{buildroot}/%{_bindir}
rmdir %{buildroot}%{gemdir}/bin
find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x

rm %{buildroot}%{geminstdir}/.yardopts

# Fix anything executable that does not have a shebang
for file in `find %{buildroot}/%{geminstdir} -type f -perm /a+x`; do
    [ -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 644 $file
done

# Find files with a shebang that do not have executable permissions
for file in `find %{buildroot}/%{geminstdir} -type f ! -perm /a+x -name "*.rb"`; do
    [ ! -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 755 $file
done

# Find files that have non-standard-executable-perm
find %{buildroot}/%{geminstdir} -type f -perm /g+wx -exec chmod -v g-w {} \;

# Find files that are not readable
find %{buildroot}/%{geminstdir} -type f ! -perm /go+r -exec chmod -v go+r {} \;

# Don't search env - use the expected ruby
find %{buildroot}%{geminstdir}/bin -type f | \
  xargs -n 1 sed -i -e 's"^#!/usr/bin/env ruby"#!/usr/bin/ruby"'

%files
%{_bindir}/haml
%{_bindir}/html2haml
%dir %{geminstdir}
%{geminstdir}/Rakefile
%{geminstdir}/bin
%{geminstdir}/extra
%{geminstdir}/init.rb
%{geminstdir}/lib
%{geminstdir}/rails
%{geminstdir}/test
%{geminstdir}/VERSION
%{geminstdir}/VERSION_NAME
# No vendored libraries thanks
%exclude %{geminstdir}/vendor
%doc %{gemdir}/doc/%{gemname}-%{version}
%doc %{geminstdir}/MIT-LICENSE
%doc %{geminstdir}/README.md
%doc %{geminstdir}/REVISION
%doc %{geminstdir}/CONTRIBUTING
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec


%changelog
* Fri Jul 22 2011 Chris Lalancette <clalance@redhat.com> - 3.1.2-2
- Fix up the sass includes

* Mon Jul 11 2011 Mo Morsi <mmorsi@redhat.com> - 3.1.2-1
- updated to latest upstream release

* Tue Mar 29 2011 Mo Morsi <mmorsi@redhat.com> - 3.0.25-1
- updated to latest upstream release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Aug 26 2010 Matthew Kent <mkent@magoazul.com> - 3.0.17-1
- New upstream version.
- Include VERSION and VERSION_NAME in main package (#627454).
- Exclude vendored copy of fssm.

* Thu Aug 12 2010 Matthew Kent <mkent@magoazul.com> - 3.0.15-2
- New BR on rubygem-erubis and ruby_parser.

* Wed Jul 28 2010 Matthew Kent <mkent@magoazul.com> - 3.0.15-1
- New upstream version.
- New dependencies on yard/maruku.

* Tue May 4 2010 Matthew Kent <mkent@magoazul.com> - 2.2.24-1
- New upstream version - minor bugfixes and improvements.
- Drop unused sitelib macro.
- No backup files to cleanup now.

* Mon Jan 04 2010 Michal Babej <mbabej@redhat.com> - 2.2.20-1
- update to new upstream release

* Mon Jan 04 2010 Michal Babej <mbabej@redhat.com> - 2.2.16-1
- update to new upstream release
- get rid of test_files macro
- add shebang/permission handling from Jeroen van Meeuwen

* Fri Dec 04 2009 Michal Babej <mbabej@redhat.com> - 2.2.15-2
- change %%define to %%global
- change license to "MIT and WTFPL" (test/haml/spec/README.md)
- add Requires on hpricot for html2haml
- change %%gemdir to %%geminstdir where appropriate

* Wed Dec 02 2009 Michal Babej <mbabej@redhat.com> - 2.2.15-1
- Update to new upstream release
- URL changed by upstream

* Wed Dec 02 2009 Michal Babej <mbabej@redhat.com> - 2.2.14-1
- Initial package

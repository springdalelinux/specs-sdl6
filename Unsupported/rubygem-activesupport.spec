# Generated from activesupport-1.4.4.gem by gem2rpm -*- rpm-spec -*-
%define ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%define gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define gemname activesupport
%define geminstdir %{gemdir}/gems/%{gemname}-%{version}

%define rubyabi 1.8

Summary: Support and utility classes used by the Rails framework
Name: rubygem-%{gemname}
Epoch: 1
Version: 2.3.8
Release: 2%{?dist}
Group: Development/Languages
License: MIT
URL: http://www.rubyonrails.org

Source0: http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem

# For some reason the activesupport doesn't ship with the upstream Rakefile
Source1: http://github.com/rails/rails/raw/2-3-stable/activesupport/Rakefile

# Also the activesupport gem doesn't ship with the test suite like the other
# Rails rpms, you may check it out like so
# git clone http://github.com/rails/rails.git -b 2-3-stable
# cd rails/activesupport/
# git reset --hard 9da7ff8842e5e6407872  # revisions after this correspond to 
#                                        # rails 2.3.9 and break test suite 
#                                        # when run against stock 2.3.8 gem
# tar czvf activesupport-23-tests.tgz test/
Source2: activesupport-23-tests.tgz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: rubygems
Requires: ruby(abi) = %{rubyabi}
BuildRequires: rubygems
BuildRequires(check): rubygem(rake)
BuildRequires(check): rubygem(mocha)
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
Utility library which carries commonly used classes and
goodies from the Rails framework

%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
gem install --local --install-dir %{buildroot}%{gemdir} \
            --force --rdoc %{SOURCE0}

# move the rakefile in place
cp %{SOURCE1} %{buildroot}%{geminstdir}

# move the tests into place
tar xzvf %{SOURCE2} -C %{buildroot}%{geminstdir}

# Remove bad shebangs
for file in %{buildroot}%{geminstdir}/lib/active_support/vendor/builder-2.1.2/builder.rb \
         %{buildroot}%{geminstdir}/lib/active_support/vendor/builder-2.1.2/blankslate.rb \
         %{buildroot}%{geminstdir}/lib/active_support/vendor/builder-2.1.2/builder/* ; do
    sed -i -e '1s/^\#!.*$//' $file
done

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

%check
pushd %{buildroot}%{geminstdir} 
rake test

%files
%defattr(-, root, root, -)
%dir %{geminstdir}
%doc %{geminstdir}/CHANGELOG
%{geminstdir}/Rakefile
%{geminstdir}/lib
%doc %{geminstdir}/README
%doc %{gemdir}/doc/%{gemname}-%{version}
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec
%{geminstdir}/test


%changelog
* Wed Aug 25 2010 Mohammed Morsi <mmorsi@redhat.com> - 1:2.3.8-2
- bumped version

* Wed Aug 04 2010 Mohammed Morsi <mmorsi@redhat.com> - 1:2.3.8-1
- Update to 2.3.8
- Added check section with rubygem-mocha dependency
- Added upsteam Rakefile and test suite to run tests

* Thu Jan 28 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:2.3.5-1
- Update to 2.3.5

* Wed Oct  7 2009 David Lutterkort <lutter@redhat.com> - 1:2.3.4-2
- Bump Epoch to ensure upgrade path from F-11

* Mon Sep 7 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.3.4-1
- Update to 2.3.4 (bug 520843, CVE-2009-3009)

* Sun Jul 26 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 2.3.3-1
- New upstream version

* Mon Mar 16 2009 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 2.3.2-1
- New upstream version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 24 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 2.2.2-1
- New upstream version

* Tue Sep 16 2008 David Lutterkort <dlutter@redhat.com> - 2.1.1-1
- New version (fixes CVE-2008-4094)

* Thu Jul 31 2008 Michael Stahnke <stahnma@fedoraproject.org> - 2.1.0-1
- New Upstream

* Mon Apr 07 2008 David Lutterkort <dlutter@redhat.com> - 2.0.2-1
- New version

* Mon Dec 10 2007 David Lutterkort <dlutter@redhat.com> - 2.0.1-1
- New version

* Wed Nov 28 2007 David Lutterkort <dlutter@redhat.com> - 1.4.4-3
- Fix buildroot

* Tue Nov 14 2007 David Lutterkort <dlutter@redhat.com> - 1.4.4-2
- Install README and CHANGELOG in _docdir

* Tue Oct 30 2007 David Lutterkort <dlutter@redhat.com> - 1.4.4-1
- Initial package

# Generated from activerecord-1.15.5.gem by gem2rpm -*- rpm-spec -*-
%define ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%define gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define gemname activerecord
%define geminstdir %{gemdir}/gems/%{gemname}-%{version}

%define rubyabi 1.8

Summary: Implements the ActiveRecord pattern for ORM
Name: rubygem-%{gemname}
Epoch: 1
Version: 2.3.8
Release: 4%{?dist}
Group: Development/Languages
License: MIT
URL: http://www.rubyonrails.org
Source0: http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem

# patch0 needed to make ar tests compatable w/ current sqlite3 version in fedora
Patch0:  activerecord-2.3.8-sqlite3-compat.patch

# patch1 https://rails.lighthouseapp.com/projects/8994/tickets/3210-rails-postgres-issue
Patch1:  activerecord-2.3.8-postgres-fix.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: ruby(abi) = %{rubyabi}
Requires: rubygems
Requires: rubygem(activesupport) = %{version}
BuildRequires: rubygems
BuildRequires(check): rubygem(rake)
BuildRequires(check): rubygem(activesupport) = %{version}
BuildRequires(check): rubygem(sqlite3-ruby)
BuildRequires(check): rubygem(mocha)
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
Implements the ActiveRecord pattern (Fowler, PoEAA) for ORM. It ties database
tables and classes together for business objects, like Customer or
Subscription, that can find, save, and destroy themselves without resorting to
manual SQL.

%prep
%setup -q -c -T

# rake test creates debug.log under %%{geminstdir},
# so let's install gem file under %%{_builddir} first

mkdir -p ./%{gemdir}
gem install --local --install-dir ./%{gemdir} \
            --force --rdoc %{SOURCE0}

pushd ./%{geminstdir}
%patch0 -p1
%patch1 -p1
popd

# Remove backup files
find ./%{geminstdir} -type f -name "*~" -delete

# Delete zero-length files
# No! These are needed for rake test
# find ./%{geminstdir} -type f -size 0c -exec rm -rvf {} \;

# Fix anything executable that does not have a shebang
for file in `find ./%{geminstdir} -type f -perm /a+x`; do
    [ -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 644 $file
done

# Find files with a shebang that do not have executable permissions
for file in `find ./%{geminstdir} -type f ! -perm /a+x -name "*.rb"`; do
    [ ! -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 755 $file
done

# this file is being marked as a doc, need to remove ruby executable path
# and mark as non-executable
sed -i -e 's/^#!\/usr\/bin\/env ruby//' ./%{geminstdir}/examples/performance.rb
chmod 0644 ./%{geminstdir}/examples/performance.rb

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
cp -a .%{gemdir}/* %{buildroot}%{gemdir}

%clean
rm -rf %{buildroot}

%check
# Only test sqlite3 backend
pushd .%{geminstdir}
rake test_sqlite3 --trace

%files
%defattr(-, root, root, -)
%dir %{geminstdir}
%doc %{geminstdir}/CHANGELOG
%doc %{geminstdir}/examples
%{geminstdir}/install.rb
%{geminstdir}/lib
%{geminstdir}/Rakefile
%doc %{geminstdir}/README
%doc %{geminstdir}/RUNNING_UNIT_TESTS
%{geminstdir}/test

%doc %{gemdir}/doc/%{gemname}-%{version}
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%changelog
* Wed Sep 08 2010 Mohammed Morsi <mmorsi@redhat.com> - 1:2.3.8-4
- Updated postgres fix to resolve security issue

* Mon Aug 16 2010 Mohammed Morsi <mmorsi@redhat.com> - 1:2.3.8-3
- Included postgres fix (patch also pushed upstream, see rails issue tracker)

* Thu Aug 12 2010 Mohammed Morsi <mmorsi@redhat.com> - 1:2.3.8-2
- Updated patch0 to correctly parse sqlite3 version

* Wed Aug 04 2010 Mohammed Morsi <mmorsi@redhat.com> - 1:2.3.8-1
- Update to 2.3.8

* Thu Jan 28 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:2.3.5-1
- Update to 2.3.5

* Wed Oct  7 2009 David Lutterkort <lutter@redhat.com> - 1:2.3.4-2
- Bump Epoch to ensure upgrade path from F-11

* Fri Sep 18 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.3.4-1
- Update to 2.3.4
- Enable check

* Sun Jul 26 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 2.3.3-1
- New upstream version

* Mon Mar 16 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 2.3.2-1
- New upstream version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 24 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 2.2.2-1
- New upstream version
- Fixed rpmlint errors zero-length files and script-without-shebang

* Thu Nov 20 2008 David Lutterkort <lutter@redhat.com> - 2.1.1-2
- Do not mark lib/ as doc

* Tue Sep 16 2008 David Lutterkort <dlutter@redhat.com> - 2.1.1-1
- New version (fixes CVE-2008-4094)

* Thu Jul 31 2008 Michael Stahnke <stahnma@fedoraproject.org> - 2.1.0-1
- New Upstream

* Tue Apr  8 2008 David Lutterkort <dlutter@redhat.com> - 2.0.2-2
- Fix dependency

* Mon Apr 07 2008 David Lutterkort <dlutter@redhat.com> - 2.0.2-1
- New version

* Mon Dec 10 2007 David Lutterkort <dlutter@redhat.com> - 2.0.1-1
- New version

* Thu Nov 29 2007 David Lutterkort <dlutter@redhat.com> - 1.15.6-1
- New version

* Tue Nov 14 2007 David Lutterkort <dlutter@redhat.com> - 1.15.5-2
- Fix buildroot
- Properly mark docs in geminstdir

* Tue Oct 30 2007 David Lutterkort <dlutter@redhat.com> - 1.15.5-1
- Initial package

# Generated from rails-1.2.5.gem by gem2rpm -*- rpm-spec -*-
%define ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%define gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define gemname rails
%define geminstdir %{gemdir}/gems/%{gemname}-%{version}

%define rubyabi 1.8

Summary: Web-application framework
Name: rubygem-%{gemname}
Epoch: 1
Version: 2.3.8
Release: 1%{?dist}
Group: Development/Languages
License: MIT
URL: http://www.rubyonrails.org
Source0: http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: ruby(rubygems) >= 1.3.4
Requires: rubygem(rake) >= 0.8.3
Requires: rubygem(activesupport) = %{version}
Requires: rubygem(activerecord) = %{version}
Requires: rubygem(actionpack) = %{version}
Requires: rubygem(actionmailer) = %{version}
Requires: rubygem(activeresource) = %{version}
Requires: ruby(abi) = %{rubyabi}

BuildRequires: rubygems

BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
Rails is a framework for building web-application using CGI, FCGI, mod_ruby,
or WEBrick on top of either MySQL, PostgreSQL, SQLite, DB2, SQL Server, or
Oracle with eRuby- or Builder-based templates.


%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
gem install --local --install-dir %{buildroot}%{gemdir} \
            -V \
            --force %{SOURCE0}

mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}%{gemdir}/bin/* %{buildroot}/%{_bindir}
rmdir %{buildroot}%{gemdir}/bin
find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x

# Cleanup some upstream packaging oddities, mostly to make rpmlint happy
sed -i '1i#!/usr/bin/ruby\n' %{buildroot}%{geminstdir}/bin/rails

# ref: bug 496480
for file in `find %{buildroot}/%{geminstdir}/ -type f -perm /a+x`; do
  sed -i -e '1s|%{_bindir}/env ruby|%{_bindir}/ruby|' $file
  chmod 755 $file
done

# Remove backup files
find %{buildroot}/%{geminstdir} -type f -name "*~" -delete

# Don't delete zero-length files (bug 496480)
#find %{buildroot}/%{geminstdir} -type f -size 0c -exec rm -rvf {} \;

# Fix anything executable that does not have a shebang
for file in `find %{buildroot}/%{geminstdir} -type f -perm /a+x`; do
    [ -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 644 $file
done

# For sure...
find %{buildroot} -name \*.gem | xargs chmod 0644

# Find files with a shebang that do not have executable permissions
for file in `find %{buildroot}/%{geminstdir} -type f ! -perm /a+x -name "*.rb"`; do
    [ ! -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 755 $file
done

# Find files that have non-standard-executable-perm
find %{buildroot}/%{geminstdir} -type f -perm /g+wx -exec chmod -v g-w {} \;

# Find files that are not readable
find %{buildroot}/%{geminstdir} -type f ! -perm /go+r -exec chmod -v go+r {} \;

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%dir %{geminstdir}
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%{geminstdir}/bin
%{geminstdir}/builtin
%doc %{geminstdir}/CHANGELOG
%{geminstdir}/configs
%{geminstdir}/dispatches
%{geminstdir}/doc
%{geminstdir}/environments
%{geminstdir}/fresh_rakefile
%{geminstdir}/guides
%{geminstdir}/helpers
%{geminstdir}/html
%{geminstdir}/lib
%doc %{geminstdir}/MIT-LICENSE
%{geminstdir}/Rakefile
%{geminstdir}/README
%{_bindir}/rails

%changelog
* Mon Aug 09 2010 Mohammed Morsi <mmorsi@redhat.com> - 1:2.3.8-1
- Update to 2.3.8

* Thu Jan 28 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:2.3.5-1
- Update to 2.3.5

* Wed Oct  7 2009 David Lutterkort <lutter@redhat.com> - 1:2.3.4-2
- Bump Epoch to ensure upgrade path from F-11

* Sun Sep 20 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.3.4-1
- Update to 2.3.4

* Fri Jul 31 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.3.3-2
- Restore some changes

* Sun Jul 26 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 2.3.3-1
- New upstream version

* Wed Jul 24 2009 Scott Seago <sseago@redhat.com> - 2.3.2-3
- Remove the 'delete zero length files' bit, as some of these are needed.

* Wed May  6 2009 David Lutterkort <lutter@redhat.com> - 2.3.2-2
- Fix replacement of shebang lines; broke scripts/generate (bz 496480)

* Mon Mar 16 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 2.3.2-1
- New upstream version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 23 2008 David Lutterkort <lutter@redhat.com> - 2.2.2-1
- New version

* Tue Sep 16 2008 David Lutterkort <dlutter@redhat.com> - 2.1.1-2
- require rubygems >= 1.1.1; the rails code checks that at runtime

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
- No dependency on actionwebservce anymore, depend on activeresource instead

* Thu Nov 29 2007 David Lutterkort <dlutter@redhat.com> - 1.2.6-1
- Don't copy files into _docdir, mark them as doc in the geminstdir

* Tue Nov 13 2007 David Lutterkort <dlutter@redhat.com> - 1.2.5-2
- Fix buildroot

* Tue Oct 30 2007 David Lutterkort <dlutter@redhat.com> - 1.2.5-1
- Initial package

# Generated from activeresource-2.0.1.gem by gem2rpm -*- rpm-spec -*-
%define ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%define gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define gemname activeresource
%define geminstdir %{gemdir}/gems/%{gemname}-%{version}

%define rubyabi 1.8

Summary: Active Record for web resources
Name: rubygem-%{gemname}
Epoch: 1
Version: 2.3.8
Release: 1%{?dist}
Group: Development/Languages
License: MIT
URL: http://www.rubyonrails.org
Source0: http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: rubygems
Requires: rubygem(activesupport) = %{version}
Requires: ruby(abi) = %{rubyabi}
BuildRequires: rubygems
BuildRequires(check): rubygem(rake)
BuildRequires(check): rubygem(mocha)
BuildRequires(check): rubygem(activesupport) = %{version}
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
Wraps web resources in model classes that can be manipulated through XML over
REST.


%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
gem install --local --install-dir %{buildroot}%{gemdir} \
            --force --rdoc %{SOURCE0}

# Remove backup files
find %{buildroot}/%{geminstdir} -type f -name "*~" -delete

# Delete zero-length files
find %{buildroot}/%{geminstdir} -type f -size 0c -exec rm -rvf {} \;

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
rake test --trace

%files
%defattr(-, root, root, -)
%dir %{geminstdir}
%doc %{geminstdir}/CHANGELOG
%{geminstdir}/lib
%doc %{geminstdir}/README
%{geminstdir}/Rakefile
%{geminstdir}/test
%doc %{gemdir}/doc/%{gemname}-%{version}
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec


%changelog
* Mon Aug 09 2010 Mohammed Morsi <mmorsi@redhat.com> - 1:2.3.8-1
- Update to 2.3.8

* Thu Jan 28 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:2.3.5-1
- Update to 2.3.5

* Wed Oct  7 2009 David Lutterkort <lutter@redhat.com> - 1:2.3.4-2
- Bump Epoch to ensure upgrade path from F-11

* Fri Sep 18 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.3.4-1
- Update to 2.3.4
- Enable test

* Sun Jul 26 2009 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 2.3.3-1
- New upstream version

* Mon Mar 16 2009 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 2.3.2-1
- New upstream version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 23 2008 David Lutterkort <lutter@redhat.com> - 2.2.2-1
- New version

* Tue Sep 16 2008 David Lutterkort <dlutter@redhat.com> - 2.1.1-1
- New version (fixes CVE-2008-4094)

* Thu Jul 31 2008 Michael Stahnke <stahnma@fedoraproject.org> - 2.1.0-1
- New Upstream

* Tue Apr  8 2008 David Lutterkort <dlutter@redhat.com> - 2.0.2-2
- Fix dependency

* Mon Apr 07 2008 David Lutterkort <dlutter@redhat.com> - 2.0.2-1
- New version

* Mon Dec 10 2007 David Lutterkort <dlutter@redhat.com> - 2.0.1-1
- Initial package

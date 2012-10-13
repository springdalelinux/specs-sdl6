# Generated from actionmailer-1.3.6.gem by gem2rpm -*- rpm-spec -*-
%define ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%define gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define gemname actionmailer
%define geminstdir %{gemdir}/gems/%{gemname}-%{version}

%define rubyabi 1.8

Summary: Service layer for easy email delivery and testing
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
Requires: rubygem(actionpack) = %{version}
Requires: ruby(abi) = %{rubyabi}
BuildRequires: rubygems
BuildRequires(check): rubygem(rake)
BuildRequires(check): rubygem(actionpack) = %{version}
BuildRequires(check): rubygem(mocha)
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
Makes it trivial to test and deliver emails sent from a single service layer.


%prep
%setup -q -c -T
mkdir -p .%{gemdir}
gem install --local --install-dir .%{gemdir} \
            -V \
            --force --rdoc %{SOURCE0}

# Remove backup files
find ./%{geminstdir} -type f -name "*~" -delete

# Fix anything executable that does not have a shebang
for file in `find ./%{geminstdir} -type f -perm /a+x`; do
    [ -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 644 $file
done

# Find files with a shebang that do not have executable permissions
for file in `find ./%{geminstdir} -type f ! -perm /a+x -name "*.rb"`; do
    [ ! -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 755 $file
done


%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
cp -a .%{gemdir}/* %{buildroot}%{gemdir}/

%clean
rm -rf %{buildroot}

%check
export GEM_PATH=$(pwd)/%{gemdir}
pushd .%{geminstdir}

rake test --trace

%files
%defattr(-, root, root, -)
%dir %{geminstdir}
%doc %{geminstdir}/CHANGELOG
%{geminstdir}/install.rb
%{geminstdir}/Rakefile
%{geminstdir}/test
%{geminstdir}/lib
%doc %{geminstdir}/MIT-LICENSE
%doc %{geminstdir}/README
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

* Mon Sep 7 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.3.4-1
- Update to 2.3.4

* Thu Aug 02 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 2.3.3-2
- Disable test

* Sun Aug  2 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.3.3-1
- 2.3.3
- Enable test

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 16 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 2.3.2-1
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
- New version

* Thu Nov 29 2007 David Lutterkort <dlutter@redhat.com> - 1.3.6-1
- New version

* Tue Nov 14 2007 David Lutterkort <dlutter@redhat.com> - 1.3.5-2
- Fix buildroot
- Mark various things in geminstdir as doc

* Tue Oct 30 2007 David Lutterkort <dlutter@redhat.com> - 1.3.5-1
- Initial package

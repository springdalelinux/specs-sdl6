%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname hoe
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary:    	Hoe is a simple rake/rubygems helper for project Rakefiles
Name:       	rubygem-%{gemname}
Version:    	2.9.4
Release:    	1%{?dist}
Group:      	Development/Languages
License:    	MIT
URL:        	http://rubyforge.org/projects/seattlerb/
Source0:    	http://rubygems.org/gems/%{gemname}-%{version}.gem
# Rescue Hoe.spec task when Manifest.txt
Patch0:		hoe-2.6.2-rescue-missing-Manifest.patch
# Fix test order due to glob order issue
Patch1:		rubygem-hoe-2.9.4-test-glob-order.patch
# Fix place to include Rake::DSL (for newer rake)
Patch2:		rubygem-hoe-2.9.4-rake-dsl-include.patch
Requires:   	ruby(abi) = 1.8
Requires:   	rubygems >= 1.3.6
Requires:   	rubygem(rubyforge) >= 2.0.4
Requires:   	rubygem(rake)      >= 0.8.7
#Requires:       rubygem(minitest)  >= 1.7.0
BuildRequires:  rubygems >= 1.3.6
# %%check
BuildRequires:	rubygem(minitest)
BuildRequires:	rubygem(rake)
BuildRequires:	rubygem(rubyforge)
BuildArch:  	noarch
Provides:   	rubygem(%{gemname}) = %{version}

%description
Hoe is a rake/rubygems helper for project Rakefiles. It helps generate
rubygems and includes a dynamic plug-in system allowing for easy
extensibility. Hoe ships with plug-ins for all your usual project
tasks including rdoc generation, testing, packaging, and deployment.
Plug-ins Provided:
* Hoe::Clean
* Hoe::Debug
* Hoe::Deps
* Hoe::Flay
* Hoe::Flog
* Hoe::Inline
* Hoe::Package
* Hoe::Publish
* Hoe::RCov
* Hoe::Signing
* Hoe::Test
See class rdoc for help. Hint: ri Hoe

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description	doc
This package contains documentation for %{name}.

%prep
%setup -q -c -T
mkdir -p .%{gemdir}
gem install \
	--local \
	-V \
	--install-dir .%{gemdir} \
	--force \
	--rdoc \
	%{SOURCE0}

pushd .%{geminstdir}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build

%install
mkdir -p %{buildroot}%{gemdir}
cp -a .%{gemdir}/* \
	%{buildroot}%{gemdir}/

chmod 0644 %{buildroot}%{gemdir}/cache/*gem

mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}%{gemdir}/bin/* %{buildroot}/%{_bindir}
rmdir %{buildroot}/%{gemdir}/bin
find %{buildroot}/%{geminstdir}/bin -type f | xargs chmod 0755

chmod 0755 %{buildroot}/%{geminstdir}/template/bin/file_name.erb
# Don't remove template files
#rm -f %{buildroot}/%{geminstdir}/template/.autotest.erb

%check
pushd .%{geminstdir}

# Make sure that hoe currently building are loaded
export RUBYLIB=$(pwd)/lib

rake test -v --trace
popd

%files
%defattr(-, root, root, -)
%{_bindir}/sow
%dir %{geminstdir}/
%{geminstdir}/bin/
%{geminstdir}/lib/
%{geminstdir}/template/
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%doc %{geminstdir}/[A-Z]*

%files	doc
%defattr(-,root,root,-)
%{geminstdir}/.autotest
%{geminstdir}/.gemtest
%{geminstdir}/test/
%{gemdir}/doc/%{gemname}-%{version}

%changelog
* Sun Apr  3 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.9.4-1
- 2.9.4

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb  7 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.9.1-1
- 2.9.1

* Wed Feb  2 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.9.0-1
- 2.9.0

* Fri Dec 10 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.8.0-1
- 2.8.0

* Sat Nov 20 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.7.0-2
- 2.7.0

* Fri Sep 17 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.6.2-3
- Rescue Hoe.spec task when Manifest.txt is missing

* Sat Sep  4 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.6.2-2
- Kill unneeded patch

* Fri Sep  3 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.6.2-1
- 2.6.2
- Drop development dependency
- Split documentation files

* Sat Jun  5 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.6.1-1
- 2.6.1

* Thu Jun  3 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.6.0-3
- Use upstreamed patch for rubyforge-without-account.patch
- Fix test failure related to glob
  (build failed with Matt's mass build, also failed on koji)

* Wed Apr 28 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.6.0-1
- 2.6.0
- gemcutter dependency dropped

* Thu Mar  4 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.5.0-3
- Enable test
- Some cleanups

* Mon Feb 15 2010 Darryl L. Pierce <dpierce@redhat.com> 2.5.0-2
- Updated the dependency on rubygem-rubyforge to >= 2.0.3.

* Mon Feb 15 2010 Darryl L. Pierce <dpierce@redhat.com> 2.5.0-1
- Added dependency on rubygem-gemcutter >= 0.2.1.
- Added dependency on rubygem-minitest >= 1.4.2.
- Release 2.5.0 of Hoe.

* Sat Aug  8 2009 Darryl L. Pierce <dpierce@redhat.com> - 2.3.3-1
- Release 2.3.3 of Hoe.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul  1 2009 Darryl L. Pierce <dpierce@redhat.com> - 2.3.2-1
- Release 2.3.2 of Hoe.

* Fri Jun 26 2009 Darryl L. Pierce <dpierce@redhat.com> - 2.3.1-1
- Release 2.3.1 of Hoe.

* Thu Jun 18 2009 Darryl L. Pierce <dpierce@redhat.com> - 2.2.0-1
- Release 2.2.0 of Hoe.

* Mon Jun 15 2009 Darryl L. Pierce <dpierce@redhat.com> - 2.1.0-1
- Release 2.1.0 of Hoe.

* Wed Jun  3 2009 Darryl L. Pierce <dpierce@redhat.com> - 2.0.0-1
- Release 2.0.0 of Hoe.

* Fri Apr 17 2009 Darryl L. Pierce <dpierce@redhat.com> - 1.12.2-1
- Release 1.12.2 of Hoe.

* Wed Apr  1 2009 Darryl L. Pierce <dpierce@redhat.com> - 1.12.1-1
- Release 1.12.1 of Hoe.

* Tue Mar 17 2009 Darryl L. Pierce <dpierce@redhat.com> - 1.11.0-1
- Release 1.11.0 of Hoe.

* Tue Mar 10 2009 Darryl L. Pierce <dpierce@redhat.com> - 1.10.0-1
- Release 1.10.0 of Hoe.

* Fri Feb 27 2009 Darryl L. Pierce <dpierce@redhat.com> - 1.9.0-1
- Release 1.9.0 of Hoe.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 21 2009 Darryl L. Pierce <dpierce@redhat.com> - 1.8.3-1
- Release 1.8.3 of Hoe.

* Mon Oct 27 2008 Darryl L. Pierce <dpierce@redhat.com> - 1.8.2-1
- Release 1.8.2 of Hoe.

* Thu Oct 23 2008 Darryl L. Pierce <dpierce@redhat.com> - 1.8.1-2
- Last build failed.

* Thu Oct 23 2008 Darryl L. Pierce <dpierce@redhat.com> - 1.8.1-1
- Release 1.8.1 of the gem.

* Mon Oct 13 2008 Darryl L. Pierce <dpierce@redhat.com> - 1.8.0-1
- Release 1.8.0 of the gem.

* Tue Jul 01 2008 Darryl L. Pierce <dpierce@redhat.com> - 1.7.0-1
- Release 1.7.0 of the gem.

* Wed Jun 18 2008 Darryl L. Pierce <dpierce@redhat.com> - 1.6.0-1
- Release 1.6.0 of the gem.

* Mon Jun 09 2008 Darryl L. Pierce <dpierce@redhat.com> - 1.5.3-2
- Fixed the dependency for the newer version of rubygem-rubyforge.

* Tue Jun 03 2008 Darryl L. Pierce <dpierce@redhat.com> - 1.5.3-1
- New release of Hoe.

* Wed May 14 2008 Darryl L. Pierce <dpierce@redhat.com> - 1.5.1-6
- Fixed the build, which failed only on devel.

* Wed May 14 2008 Darryl L. Pierce <dpierce@redhat.com> - 1.5.1-5
- First official build.

* Mon May 12 2008 Darryl L. Pierce <dpierce@redhat.com> - 1.5.1-4
- Update for Fedora 8 and 9.

* Tue Apr 29 2008 Darryl L. Pierce <dpierce@redhat.com> - 1.5.1-3
- Fixed the license to read MIT.

* Mon Apr 28 2008 Darryl L. Pierce <dpierce@redhat.com> - 1.5.1-2
- Updated the spec to comply with Ruby packaging guidelines.

* Fri Apr 18 2008 Darryl L. Pierce <dpierce@redhat.com> - 1.5.1-1
- Initial package

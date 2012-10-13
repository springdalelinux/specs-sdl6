# Generated from rubyforge-0.4.4.gem by gem2rpm -*- rpm-spec -*-
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname rubyforge
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

# Depency loop here. Kill test when resolving dependency loop
# is needed
%global enable_test 1

Summary:       A script which automates a limited set of rubyforge operations
Name:          rubygem-%{gemname}
Version:       2.0.4
Release:       3%{?dist}
Group:         Development/Languages
License:       MIT
URL:           http://rubyforge.org/projects/codeforpeople
Source0:       http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:      ruby(abi) = 1.8
Requires:      rubygems
Requires:      rubygem(json) >= 1.1.7
BuildRequires: rubygems
%if %{enable_test}
# For %%check
BuildRequires: rubygem(rake)
BuildRequires: rubygem(json)
# The following line causes dependency loop
BuildRequires: rubygem(hoe)
%endif
BuildArch:     noarch
Provides:      rubygem(%{gemname}) = %{version}

%description
A script which automates a limited set of rubyforge operations.

%package        doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description    doc
This package contains documentation for %{name}.

%prep
%setup -q -c -T

mkdir -p ./%{gemdir}
gem install \
	--local \
	--install-dir ./%{gemdir} \
	--force \
	--rdoc \
	%{SOURCE0}

# json_pure -> json
find . -name Rakefile -or -name \*.gemspec | \
	xargs sed -i -e 's|json_pure|json|g'

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
cp -a .%{gemdir}/* %{buildroot}/%{gemdir}/

mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}%{gemdir}/bin/* %{buildroot}/%{_bindir}
rmdir %{buildroot}%{gemdir}/bin

find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x
chmod 0755 %{buildroot}%{geminstdir}/lib/rubyforge.rb
chmod 0755 %{buildroot}%{geminstdir}/bin/rubyforge

%clean
rm -rf %{buildroot}

%check
%if ! %{enable_test}
exit 0
%endif

pushd .%{gemdir}
# Hoe needs rubyforge, so make it sure that system-widely installed
# Hoe looks for rubyforge just trying to install now first, not
# system-widely installed rubyforge
export GEM_PATH=$(pwd)
popd

pushd .%{geminstdir}
rake test
popd

%files
%defattr(-, root, root, -)
%{_bindir}/rubyforge
%dir %{geminstdir}
%{geminstdir}/lib/
%{geminstdir}/bin/
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec
%doc %{geminstdir}/History.txt
%doc %{geminstdir}/Manifest.txt
%doc %{geminstdir}/README.txt

%files doc
%defattr(-,root,root,-)
%{gemdir}/doc/%{gemname}-%{version}
%{geminstdir}/Rakefile
%{geminstdir}/test/


%changelog
* Mon Feb 14 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.4-3
- F-15 mass rebuild

* Thu Sep 16 2010 Mamotu Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.4-2
- Split out document files

* Thu Mar  4 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.4-1
- Update to 2.0.4
- Replace json_pure to json (bug 570252)

* Mon Feb 15 2010 Darryl L. Pierce <dpierce@redhat.com> - 2.0.3-1
- Added new dependency on rubygem-json >= 1.1.7.
- Release 2.0.3 of RubyForge.

* Tue Sep 15 2009 Darryl L. Pierce <dpierce@redhat.com> - 1.0.5-1
- Release 1.0.5 of RubyForge.

* Sat Aug  8 2009 Darryl L. Pierce <dpierce@redhat.com> - 1.0.4-1
- Release 1.0.4 of RubyForge.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Feb 27 2009 Darryl Pierce <dpierce@redhat.com> - 1.0.3-1
- Release 1.0.3 of RubyForge.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 06 2009 Darryl Pierce <dpierce@redhat.com> - 1.0.2-2
- Provided the wrong gem as source.

* Tue Jan 06 2009 Darryl Pierce <dpierce@redhat.com> - 1.0.2-1
- Release 1.0.2 of Rubyforge.

* Thu Oct 23 2008 Darryl Pierce <dpierce@redhat.com> - 1.0.1-1
- Release 1.0.1 of Rubyforge.

* Mon Jun 09 2008 Darryl Pierce <dpierce@redhat.com> - 1.0.0-1
- New version of RubyForge released.

* Wed May 14 2008 Darryl Pierce <dpierce@redhat.com> - 0.4.5-2
- Figured out how to do a proper build.

* Mon May 12 2008 Darryl Pierce <dpierce@redhat.com> - 0.4.5-1
- New version of the gem released.

* Tue Apr 29 2008 Darryl Pierce <dpierce@redhat.com> - 0.4.4-3
- Fixed the executable attribute for rubyforge.rb.

* Mon Apr 28 2008 Darryl Pierce <dpierce@redhat.com> - 0.4.4-2
- Updated the spec to comply with Ruby packaging guidelines.

* Fri Apr 18 2008 Darryl Pierce <dpierce@redhat.com> - 0.4.4-1
- Initial package

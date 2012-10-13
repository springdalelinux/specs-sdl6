%define gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define gemname rack
%define geminstdir %{gemdir}/gems/%{gemname}-%{version}

Name:           rubygem-%{gemname}
Summary:        Common API for connecting web frameworks, web servers and layers of software
# Introduce Epoch (related to bug 552972)
Epoch:          1
Version:        1.3.0
Release:        1%{?dist}
Group:          Development/Languages
License:        MIT
URL:            http://rubyforge.org/projects/%{gemname}/
Source0:        http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       rubygems
Requires:       ruby(abi) = 1.8
BuildRequires:  rubygems
BuildRequires:  rubygem(bacon)
BuildArch:      noarch
Provides:       rubygem(%{gemname}) = %{version}

%description
Rack provides a common API for connecting web frameworks,
web servers and layers of software in between

%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
gem install --local --install-dir %{buildroot}/%{gemdir} \
            --force %{SOURCE0}

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

# Find files that have non-standard-executable-perm
find %{buildroot}/%{geminstdir} -type f -perm /g+wx -exec chmod -v g-w {} \;

# Find files that are not readable
find %{buildroot}/%{geminstdir} -type f ! -perm /go+r -exec chmod -v go+r {} \;

# Move %{gemdir}/bin/rackup to %{_bindir}
mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}/%{gemdir}/bin/rackup %{buildroot}/%{_bindir}
rm -rf %{buildroot}/%{gemdir}/bin/

%clean
rm -rf %{buildroot}

%check
pushd %{buildroot}%{geminstdir}
bacon --automatic --quiet
popd

%files
%defattr(-, root, root, -)
%dir %{geminstdir}
%doc %{gemdir}/doc/%{gemname}-%{version}
%doc %{geminstdir}/COPYING
%doc %{geminstdir}/Rakefile
%doc %{geminstdir}/README
%doc %{geminstdir}/KNOWN-ISSUES
%doc %{geminstdir}/SPEC
%doc %{geminstdir}/example
%doc %{geminstdir}/test
%doc %{geminstdir}/contrib
%{geminstdir}/%{gemname}.gemspec
%{geminstdir}/lib
%{geminstdir}/bin
%{_bindir}/rackup
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%changelog
* Tue Jun 28 2011 Vít Ondruch <vondruch@redhat.com> - 1:1.3.0-1
- Updated to Rack 1.3.
- Fixed FTBFS.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Mar 11 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:1.1.0-2
- Epoch 1 for keeping upgrade path from F-12 (related to bug 552972)
- Enable %%check

* Mon Jan  4 2010 Jeroen van Meeuwen <kanarip@kanarip.com> - 1.1.0-1
- New upstream version

* Sun Oct 25 2009 Jeroen van Meeuwen <kanarip@kanarip.com> - 1.0.1-1
- New upstream version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 26 2009 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 1.0.0-1
- New upstream version

* Mon Mar 16 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.9.1-1
- New upstream version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 09 2008 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.4.0-2
- Remove unused macro (#470694)
- Add ruby(abi) = 1.8 as required by package guidelines (#470694)
- Move %%{gemdir}/bin/rackup to %%{_bindir} (#470694)

* Sat Nov 08 2008 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.4.0-1
- Initial package

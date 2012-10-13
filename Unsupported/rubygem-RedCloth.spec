# Generated from RedCloth-4.1.9.gem by gem2rpm -*- rpm-spec -*-
%global ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%global ruby_sitearch %(ruby -rrbconfig -e "puts Config::CONFIG['sitearchdir']")
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname RedCloth
%global gemlibname redcloth_scan.so
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%global installroot %{buildroot}%{geminstdir}
%global extensionddir %{installroot}/ext/redcloth_scan/

Summary:       Textile parser for Ruby
Name:          rubygem-%{gemname}
Version:       4.2.3
Release:       2%{?dist}
Group:         Development/Languages
License:       MIT
URL:           http://redcloth.org
Source0:       http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:      ruby(abi) = 1.8
Requires:      rubygems
BuildRequires: rubygems
BuildRequires: ruby-devel >= 1.8
Provides:      rubygem(%{gemname}) = %{version}

%description
Textile parser for Ruby.


%prep
%setup -q -c -T
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
gem install --local --install-dir .%{gemdir} \
          --force -V --rdoc %{SOURCE0}

# To create debuginfo file corretly (workaround for
# "#line" directive)
pushd .%{geminstdir}/ext/redcloth_scan
mkdir ext
ln -sf .. ext/redcloth_scan
popd

%build

%install
rm -rf %{buildroot}

install -d -m0755 %{buildroot}%{gemdir}
install -d -m0755 %{buildroot}%{ruby_sitelib}
install -d -m0755 %{buildroot}%{ruby_sitearch}

cp -a .%{gemdir}/* %{buildroot}%{gemdir}

mkdir -p %{buildroot}/%{_bindir}

cp -a %{buildroot}%{gemdir}/bin/* %{buildroot}/%{_bindir}
mv %{extensionddir}%{gemlibname} %{buildroot}%{ruby_sitearch}/%{gemlibname}
rm -rf %{extensionddir}

rm %{installroot}/lib/%{gemlibname}
cp %{installroot}/lib/redcloth.rb %{buildroot}%{ruby_sitelib}/redcloth.rb
rm -rf %{buildroot}%{gemdir}/bin
find %{installroot}/bin -type f | xargs chmod a+x
find %{installroot} -name "*.rb" | xargs chmod a+x

find %{installroot} -type f -name \*.rb | xargs chmod 0644

# 4.2.2-1 No files have the prologue to run as executables.
#find %%{installroot} -type f -name "\*.rb" | \
#  xargs grep -l "^#!l%%{_bindir}/env" $file | xargs chmod 0755

rm -f %{installroot}/.require_paths
rm -f %{installroot}/Manifest
rm -f %{installroot}/RedCloth.gemspec
%clean
rm -rf %{buildroot}

%check 
# Requires echoe -- not in Fedora yet
cd %{buildroot}%{geminstdir}

%files
%defattr(-, root, root, -)
%{_bindir}/redcloth
%dir %{geminstdir}
%{geminstdir}/bin
%{geminstdir}/lib
%{ruby_sitelib}/redcloth.rb
%{ruby_sitearch}/%{gemlibname}
%doc %{gemdir}/doc/%{gemname}-%{version}
%doc %{geminstdir}/spec
%doc %{geminstdir}/README
%doc %{geminstdir}/Rakefile
%doc %{geminstdir}/CHANGELOG
%doc %{geminstdir}/COPYING
%doc %{geminstdir}/setup.rb
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec


%changelog
* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Sep 03 2010 Michael Stahnke <stahnma@fedoraproject.org> - 4.2.3-1
- Version update 

* Mon Feb 15 2010 Darryl L. Pierce <dpierce@redhat.com> - 4.2.2-1
- Commented out the piece of set the executable status on files.
- Release 4.2.2 of RedCloth.

* Thu Jul 30 2009 Darryl L. Pierce <dpierce@redhat.com> - 4.1.9-7
- Resolves: rhbz#505589 - rubygem-RedCloth-debuginfo created from stripped binaries

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Darryl L. Pierce <dpierce@redhat.com> - 4.1.9-5
- Resolves: rhbz#505589 - rubygem-RedCloth-debuginfo created from stripped binaries

* Fri May  1 2009 Darryl L. Pierce <dpierce@redhat.com> - 4.1.9-4
- First official build for Fedora.

* Thu Apr 30 2009 Darryl L. Pierce <dpierce@redhat.com> - 4.1.9-3
- Changed mv to cp for binaries.
- Removed redundant %%doc entries.

* Thu Apr 30 2009 Darryl L. Pierce <dpierce@redhat.com> - 4.1.9-2
- Added BuildRequires: ruby-devel to fix koji issues.

* Thu Apr 23 2009 Darryl L. Pierce <dpierce@redhat.com> - 4.1.9-1
- Initial package

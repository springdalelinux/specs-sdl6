%define gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define gemname maruku
%define geminstdir %{gemdir}/gems/%{gemname}-%{version}

%define rubyabi 1.8 

Name: rubygem-%{gemname}
Summary: Maruku is a Markdown-superset interpreter written in Ruby
Version: 0.6.0
Release: 5%{?dist}
Group: Development/Languages
License: GPLv2+
URL: http://maruku.rubyforge.org

Source0: http://gemcutter.org/downloads/%{gemname}-%{version}.gem
Patch0:  remove_deprecated_method.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: rubygems
Requires: rubygem(syntax) >= 1.0.0
Requires: ruby(abi) = %{rubyabi}
BuildRequires: rubygems
BuildRequires: rubygem(rake)
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
Maruku is a Markdown interpreter in Ruby. It features native export to HTML
and PDF (via Latex). The output is really beautiful!


%prep
%setup -q -c -T
mkdir -p ./%{gemdir}
gem install \
  --local \
  --install-dir $(pwd)/%{gemdir} \
  --force --no-ri --rdoc \
  %{SOURCE0}

pushd .%{geminstdir}
%patch0 -p0

# fixes rpmlint warning about file-not-utf8
# http://fedoraproject.org/wiki/Common_Rpmlint_issues#file-not-utf8
iconv -f iso8859-1 -t utf-8 tests/unittest/lists10.md > list10.md.conv && mv -f list10.md.conv tests/unittest/lists10.md

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
mkdir -p %{buildroot}/%{_bindir}

cp -a ./%{gemdir}/* %{buildroot}/%{gemdir}/. 
mv %{buildroot}%{gemdir}/bin/* %{buildroot}/%{_bindir}
rmdir %{buildroot}%{gemdir}/bin
find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x

%check
pushd .%{geminstdir} 
rake test || : 

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{_bindir}/maruku
%{_bindir}/marutex
%dir %{geminstdir} 
%{geminstdir}/bin
%{geminstdir}/lib

%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%doc %{geminstdir}/docs
%doc %{geminstdir}/tests
%doc %{geminstdir}/Rakefile
%doc %{geminstdir}/maruku_gem.rb
%doc %{geminstdir}/*.sh
%doc %{gemdir}/doc/%{gemname}-%{version}



%changelog
* Mon Aug 08 2011 Mo Morsi <mmorsi@redhat.com> - 0.6.0-5
- Replace BR(check) with BR

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 23 2010 Mohammed Morsi <mmorsi@redhat.com> - 0.6.0-3
- added geminstdir to file list
- added rubygem(rake) dependency
- other fixes to conform to package guidelines

* Mon Feb 08 2010 Mohammed Morsi <mmorsi@redhat.com> - 0.6.0-2
- cleaned up macros, other package guideline compliance fixes
- corrected license
- include all files and docs, added check/test section

* Mon Feb 08 2010 Mohammed Morsi <mmorsi@redhat.com> - 0.6.0-1
- Initial package

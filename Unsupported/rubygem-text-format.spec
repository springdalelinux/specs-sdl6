# Generated from text-format-1.0.0.gem by gem2rpm -*- rpm-spec -*-
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname text-format
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary: Text::Format formats fixed-width text nicely
Name: rubygem-%{gemname}
Version: 1.0.0
Release: 5%{?dist}
Group: Development/Languages
License: Ruby
URL: http://rubyforge.org/projects/text-format
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem

# text-hyphen currently has an ugly license situation
# (not necessarily unacceptable for Fedora, but needs
#  looking into, remove dependency for now)
Patch0: remove-text-hyphen-dep.patch

Requires: rubygems
BuildRequires: rubygems
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
Text::Format is provides the ability to nicely format fixed-width text with
knowledge of the writeable space (number of columns), margins, and indentation
settings. Text::Format can work with either TeX::Hyphen or Text::Hyphen to
hyphenate words when formatting.


%prep
%setup -q -c -T
mkdir -p .%{gemdir}
gem install --local --install-dir .%{gemdir} \
            -V \
            --force --rdoc %{SOURCE0}

pushd .%{gemdir}
%patch0 -p0

%build

%install
mkdir -p %{buildroot}%{gemdir}
cp -a .%{gemdir}/* %{buildroot}%{gemdir}

# remove installer as its not needed
pushd %{buildroot}%{geminstdir}
rm pre-setup.rb setup.rb metaconfig

# remove dos end of line encoding
tr -d '\r' < Rakefile > Rakefile.new
mv Rakefile.new Rakefile

iconv -f iso8859-1 -t utf-8 README > README.conv && mv -f README.conv README
pushd %{buildroot}%{gemdir}
rm -f specifications/%{gemname}-%{version}.gemspec.orig
popd

%check
pushd %{buildroot}%{geminstdir} 
ruby tests/tc_*

%files
%defattr(-, root, root, -)
%dir %{geminstdir}
%{geminstdir}/lib
%doc %{gemdir}/doc/%{gemname}-%{version}
%doc %{geminstdir}/README
%doc %{geminstdir}/Changelog
%doc %{geminstdir}/Install
%doc %{geminstdir}/Rakefile
%doc %{geminstdir}/ToDo
%doc %{geminstdir}/tests
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec


%changelog
* Thu Mar 22 2012 Steve Linabery <slinaber@redhat.com> - 1.0.0-5
- remove {gemdir}/specifications/{gemname}-{version}.gemspec.orig file as part of install

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 02 2011 Mo Morsi <mmorsi@redhat.com> - 1.0.0-3
- remove 'file-not-utf8' rpmlint error

* Tue Feb 01 2011 Mo Morsi <mmorsi@redhat.com> - 1.0.0-2
- Updates based on review feedback

* Tue Jan 11 2011 Mo Morsi <mmorsi@redhat.com> - 1.0.0-1
- Initial package

%define gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define gemname hawler
%define geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary:        Hawler, the ruby HTTP crawler
Name:           rubygem-%{gemname}
Version:        0.3
Release:        5%{?dist}
Group:          Development/Languages
License:        BSD
URL:            http://spoofed.org/files
Source0:        http://spoofed.org/files/hawler/gems/%{gemname}-%{version}.gem
# From http://spoofed.org/files/hawler/src/COPYING
Source1:        rubygem-hawler.COPYING
Patch0:         rubygem-hawler-0.3.4-fix-tests.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       ruby(abi) = 1.8
Requires:       rubygems
Requires:       rubygem(hpricot)
BuildRequires:  rubygems
BuildRequires:  rubygem(hpricot)
BuildArch:      noarch
Provides:       rubygem(%{gemname}) = %{version}

%description
Hawler, the Ruby HTTP crawler. Written to ease satisfying
curiousities about the way the web is woven.

%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
gem install --local --install-dir %{buildroot}%{gemdir} \
            --force --rdoc %{SOURCE0}

pushd %{buildroot}/%{geminstdir}
patch -p0 < %{PATCH0}
popd

install -p -m644 %{SOURCE1} %{buildroot}/%{geminstdir}/COPYING

# Remove backup files
find %{buildroot}/%{geminstdir} -type f -name "*~" -delete

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

# Remove these hidden files
rm -rf %{buildroot}/%{geminstdir}/.project
rm -rf %{buildroot}/%{geminstdir}/.loadpath

%check
pushd %{buildroot}/%{geminstdir}
ruby test/ts_hawlee.rb || :
ruby test/ts_hawlerhelper.rb || :
ruby test/ts_hawler.rb || :
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc %{gemdir}/doc/%{gemname}-%{version}
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec
%dir %{geminstdir}
%doc %{geminstdir}/README
%doc %{geminstdir}/COPYING
%{geminstdir}/lib/
%{geminstdir}/test/

%changelog
* Sun Nov  1 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.3-5
- Fix tests (mtasaka, #530204)
- Add requirement for rubygem-hpricot

* Sun Oct 25 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.3-4
- License is BSD
- Included License file
- Updated description
- Enabled tests

* Wed Oct 21 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.3-2
- The license is actually unknown to me

* Sat Oct 17 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.3-1
- First package

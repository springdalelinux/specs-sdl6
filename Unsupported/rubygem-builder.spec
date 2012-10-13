%define ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%define gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define gemname builder
%define geminstdir %{gemdir}/gems/%{gemname}-%{version}

Name:		rubygem-%{gemname}
Summary: 	Builders for MarkUp
Version: 	2.1.2
Release: 	5%{?dist}
Group: 		Development/Languages
License: 	GPLv2+ or Ruby
URL: 		http://onestepback.org
# Source pulled from http://www.freshports.org/devel/rubygem-builder/, there's more listed
Source0:	http://rubyforge.rubyuser.de/%{gemname}/%{gemname}-%{version}.gem
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: 	rubygems
BuildRequires: 	rubygems
BuildArch: 	noarch
Provides: 	rubygem(%{gemname}) = %{version}

%description
Builder provides a number of builder objects that make creating structured
data simple to do.  Currently the following builder objects are supported:  *
XML Markup * XML Events

%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
gem install --local --install-dir %{buildroot}%{gemdir} \
            --force --rdoc %{SOURCE0}

for file in `find %{buildroot}/%{geminstdir} -name "*.rb"`; do
    [ ! -z "`head -n 1 $file | grep \"^#!\"`" ] && chmod +x $file
done

# Convert README to utf8
strings %{buildroot}/%{geminstdir}/README > %{buildroot}/%{geminstdir}/README.strings

mv -f %{buildroot}/%{geminstdir}/README.strings %{buildroot}/%{geminstdir}/README

# Remove zero-length file
rm -rf %{buildroot}/%{geminstdir}/%{gemname}-%{version}.gem

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{gemdir}/gems/%{gemname}-%{version}/
%doc %{gemdir}/doc/%{gemname}-%{version}
%doc %{geminstdir}/CHANGES
%doc %{geminstdir}/Rakefile
%doc %{geminstdir}/README
%doc %{geminstdir}/doc/releases/builder-1.2.4.rdoc
%doc %{geminstdir}/doc/releases/builder-2.0.0.rdoc
%doc %{geminstdir}/doc/releases/builder-2.1.1.rdoc
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec


%changelog
* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 29 2008 Jeroen van Meeuwen <kanarip@kanarip.com> - 2.1.2-2
- Rebuild for review

* Sun Jul 13 2008 root <root@oss1-repo.usersys.redhat.com> - 2.1.2-1
- Initial package

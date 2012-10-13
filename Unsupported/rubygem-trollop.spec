%global	gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global	gemname trollop
%global	geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary:	A command-line option parsing library for ruby
Name:		rubygem-%{gemname}
Version:	1.16.2
Release:	1%{?dist}
Group:		Applications/Productivity
License:	GPLv2
URL:		http://trollop.rubyforge.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	rubygems
Requires:	ruby(abi) = 1.8
BuildRequires:	rubygem(hoe)
BuildRequires:	rubygems
BuildArch:	noarch
Provides:	rubygem(%{gemname}) = %{version}
Source0:	http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem

%description
A command-line option parsing library for ruby. Trollop is designed to
provide the maximal amount of GNU-style argument processing in the minimum
number of lines of code (for you, the programmer).

%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
gem install --local --install-dir %{buildroot}%{gemdir} \
	--force --rdoc %{SOURCE0}

%check
cd %{buildroot}/%{geminstdir}
ruby -Ilib/ test/test_trollop.rb

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%dir %{geminstdir}
%{geminstdir}/lib
%{geminstdir}/test
%doc %{geminstdir}/*.txt
%doc %{gemdir}/doc/%{gemname}-%{version}
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%changelog
* Thu Mar 10 2011 Jan Klepek <jan.klepek at, gmail.com> - 1.16.2-1
- updated to 1.16.2

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct 3 2009 Jan Klepek <jan.klepekat, gmail.com> - 1.15-1
- update of trollop to 1.15

* Thu Sep 24 2009 Jan Klepek <jan.klepekat, gmail.com> - 1.14-1
- directory ownership fix, license changed to GPLv2, redundant macro removed

* Sun Sep 20 2009 Jan Klepek <jan.klepekat, gmail.com> - 1.14-0
- Version update,

* Sat Jan 24 2009 Kyle McMartin <kyle@redhat.com> - 1.10.2-1
- Initial release of trollop.

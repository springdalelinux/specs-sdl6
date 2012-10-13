%global	gemname	rake-compiler
%global	gemdir		%(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global	geminstdir	%{gemdir}/gems/%{gemname}-%{version}

%global	rubyabi	1.8

Summary:	Rake-based Ruby C Extension task generator
Name:		rubygem-%{gemname}
Version:	0.7.1
Release:	1%{?dist}
Group:		Development/Languages
License:	MIT
URL:		http://rake-compiler.rubyforge.org/
Source0:	http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem

BuildRequires:	ruby(abi) = %{rubyabi}
BuildRequires:	ruby(rubygems) >= 1.3.5
BuildRequires:	rubygem(rake)
Requires:	ruby(abi) = %{rubyabi}
Requires:	ruby(rubygems) >= 1.3.5
Requires:	rubygem(rake) >= 0.8.3
BuildArch:	noarch
Provides:	rubygem(%{gemname}) = %{version}-%{release}

%description
rake-compiler aims to help Gem developers while dealing with
Ruby C extensions, simplifiying the code and reducing the duplication.

It follows *convention over configuration* and set an standarized
structure to build and package C extensions in your gems.

This is the result of expriences dealing with several Gems 
that required native extensions across platforms and different 
user configurations where details like portability and 
clarity of code were lacking. 

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
	--install-dir $(pwd)%{gemdir} \
	--force \
	--rdoc \
	-V \
	%{SOURCE0}

# rpmlint cosmetic
pushd .%{geminstdir}
sed -i -e 's|\r||' README.rdoc
find ./lib/rake -name \*.rb | xargs sed -i -e '\@/usr/bin/env@d'
popd

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{gemdir}
cp -a .%{gemdir}/* %{buildroot}%{gemdir}/

# Move files under %%_bindir
mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}%{gemdir}/bin/* %{buildroot}/%{_bindir}

rmdir %{buildroot}%{gemdir}/bin

%check
pushd .%{geminstdir}
rake spec

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/rake-compiler
%dir %{geminstdir}
%doc %{geminstdir}/README.rdoc
%doc %{geminstdir}/LICENSE.txt
%doc %{geminstdir}/History.txt
%{geminstdir}/Rakefile
%{geminstdir}/cucumber.yml
%{geminstdir}/[a-z]*/
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%defattr(-,root,root,-)
%{gemdir}/doc/%{gemname}-%{version}


%changelog
* Wed Aug 11 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.7.1-1
- 0.7.1

* Thu Dec 10 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.7.0-1
- 0.7.0

* Wed Jul 29 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.6.0-1
- 0.6.0

* Sat Jul 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.5.0-2
- F-12: Mass rebuild

* Thu Jul  2 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.5.0-2
- Restore files under %%{geminstdir}/bin

* Thu Jun 11 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.5.0-1
- Initial package

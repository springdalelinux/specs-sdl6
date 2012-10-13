%global	gemdir		%(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global	majorver	2.6.0
#%%global	preminorver	.rc6
%global	rpmminorver	.%(echo %preminorver | sed -e 's|^\\.\\.*||')
%global	fullver	%{majorver}%{?preminorver}

%global	fedorarel	1

%global	gemname	rspec-mocks
%global	geminstdir	%{gemdir}/gems/%{gemname}-%{fullver}

%global	rubyabi	1.8

# %%check section needs rspec-core, however rspec-core depends on rspec-mocks
# runtime part of rspec-mocks does not depend on rspec-core
%global	need_bootstrap_set	1
%if 0%{?fedora} >= 15
%global	need_bootstrap_set	0
%endif

%{!?need_bootstrap:	%global	need_bootstrap	%{need_bootstrap_set}}

Summary:	Rspec-2 doubles (mocks and stubs)
Name:		rubygem-%{gemname}
Version:	%{majorver}
Release:	%{?preminorver:0.}%{fedorarel}%{?preminorver:%{rpmminorver}}%{?dist}

Group:		Development/Languages
License:	MIT
URL:		http://github.com/rspec/rspec-mocks
Source0:	http://rubygems.org/gems/%{gemname}-%{fullver}.gem

BuildRequires:	ruby(abi) = %{rubyabi}
BuildRequires:	rubygems
%if 0%{?need_bootstrap} < 1
BuildRequires:	rubygem(rspec-core)
%endif
Requires:	ruby(abi) = %{rubyabi}
Requires:	rubygems
Provides:	rubygem(%{gemname}) = %{version}-%{release}
BuildArch:	noarch

%description
rspec-mocks provides a test-double framework for rspec including support
for method stubs, fakes, and message expectations.

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
	-V \
	--local \
	--install-dir .%{gemdir} \
	--force \
	--rdoc \
	%{SOURCE0}

chmod 0644 .%{gemdir}/cache/%{gemname}-%{fullver}.gem

%build

%install
mkdir -p %{buildroot}%{gemdir}
cp -a .%{gemdir}/* %{buildroot}%{gemdir}/

# cleanups
rm -f %{buildroot}%{geminstdir}/{.document,.gitignore,.travis.yml}

%if 0%{?need_bootstrap} < 1
%check
pushd .%{geminstdir}
ruby -rubygems -Ilib/ -S rspec spec/
%endif

%files
%defattr(-,root,root,-)
%dir	%{geminstdir}

%doc	%{geminstdir}/License.txt
%doc	%{geminstdir}/*.md
%{geminstdir}/lib/

%{gemdir}/cache/%{gemname}-%{fullver}.gem
%{gemdir}/specifications/%{gemname}-%{fullver}.gemspec


%files	doc
%defattr(-,root,root,-)
%{gemdir}/doc/%{gemname}-%{fullver}
%{geminstdir}/.autotest
%{geminstdir}/Gemfile
%{geminstdir}/Guardfile
%{geminstdir}/Rakefile
%{geminstdir}/cucumber.yml
%{geminstdir}/%{gemname}.gemspec
%{geminstdir}/specs.watchr
%{geminstdir}/autotest/
%{geminstdir}/features/
%{geminstdir}/spec/

%changelog
* Mon May 16 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.6.0-1
- 2.6.0

* Tue May 10 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.6.0-0.3.rc6
- 2.6.0 rc6

* Tue May  3 2011 Mamoru Tasaka <mtasaka@fedoraproject.org>
- And enable check on rawhide

* Tue May  3 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.6.0-0.1.rc4
- 2.6.0 rc4

* Sat Feb 26 2011 Mamoru Tasaka <mtasaka@fedoraproject.org>
- And enable check on rawhide

* Sat Feb 26 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.5.0-2
- Cleanups

* Thu Feb 17 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.5.0-1
- 2.5.0

* Fri Nov 05 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.1-1
- Initial package

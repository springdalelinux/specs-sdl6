%global gem_name redcarpet
%global rubyabi 1.8

%global gem_dir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gem_cache %{gem_dir}/cache/%{gem_name}-%{version}.gem
%global gem_docdir %{gem_dir}/doc/%{gem_name}-%{version}
%global gem_instdir %{gem_dir}/gems/%{gem_name}-%{version}
%global gem_libdir %{gem_instdir}/lib
%global gem_spec %{gem_dir}/specifications/%{gem_name}-%{version}.gemspec

%{!?ruby_sitearch: %global ruby_sitearch %(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"] ')}
%global gem_extinstdir %{ruby_sitearch}


Summary: A fast, safe and extensible Markdown to (X)HTML parser
Name: rubygem-%{gem_name}
Version: 2.1.1
Release: 5%{?dist}
Group: Development/Languages
License: ISC
URL: http://github.com/tanoku/redcarpet
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(abi) = %{rubyabi}

BuildRequires: rubygems
BuildRequires: ruby-devel
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(rake)
BuildRequires: rubygem(nokogiri)

Provides: rubygem(%{gem_name}) = %{version}



%description
A fast, safe and extensible Markdown to (X)HTML parser


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}

%description doc
Documentation for %{name}

%prep

%build
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"

# gem install compiles any C extensions and installs into a directory
# We set that to be a local directory so that we can move it into the
# buildroot in the install section
gem install -V \
        --local \
        --install-dir ./%{gem_dir} \
        --bindir ./%{_bindir} \
        --force \
        --rdoc \
        %{SOURCE0}

# Fix permissions
chmod 644 ./%{gem_dir}/gems/%{gem_name}-%{version}/COPYING
chmod 644 ./%{gem_dir}/gems/%{gem_name}-%{version}/ext/redcarpet/*

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -a ./%{_bindir}/* %{buildroot}%{_bindir}
chmod 755 %{buildroot}%{_bindir}/redcarpet

mkdir -p %{buildroot}%{gem_extinstdir}
mv %{buildroot}%{gem_instdir}/lib/redcarpet.so %{buildroot}%{gem_extinstdir}

# Clean up ext artifacts
rm %{buildroot}%{gem_instdir}/ext/redcarpet/*.o
rm %{buildroot}%{gem_instdir}/ext/redcarpet/*.so

%check
pushd .%{gem_instdir}
ruby -rubygems -Ilib test/redcarpet_test.rb
popd

%files
%dir %{gem_instdir}
%{_bindir}/redcarpet
%{gem_instdir}/bin
%{gem_instdir}/ext
%{gem_libdir}
%{gem_extinstdir}
%{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/COPYING
%doc %{gem_instdir}/README.markdown

%files doc
%{gem_instdir}/Rakefile
%{gem_instdir}/test
%{gem_instdir}/%{gem_name}.gemspec
%doc %{gem_docdir}


%changelog
* Mon May 21 2012 Matt Hicks <mhicks@redhat.com> - 2.1.1-5
- Making architecture specific to workaround rpmdiff issue

* Mon May 21 2012 Matt Hicks <mhicks@redhat.com> - 2.1.1-4
- Removing conditionals

* Mon May 21 2012 Matt Hicks <mhicks@redhat.com> - 2.1.1-3
- Adding newer rdoc build requires to fix rpmdiff issue

* Fri May 18 2012 Matt Hicks <mhicks@redhat.com> - 2.1.1-2
- Cleaning up spec to remove patch and rake testing dependency

* Thu Apr 26 2012 Matt Hicks <mhicks@redhat.com> - 2.1.1-1
- Initial package

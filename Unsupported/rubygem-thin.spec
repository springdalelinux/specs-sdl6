%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname thin
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%global ruby_sitearch %(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"] ')
%global ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%global rubyabi 1.8

Summary: A thin and fast web server
Name: rubygem-%{gemname}
Version: 1.2.11
Release: 3%{?dist}
Group: Development/Languages
License: (GPLv2 or Ruby) and BSD and MIT
URL: http://code.macournoyer.com/thin/
Source0: http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
Patch1: rubygem-thin-fix-parser-load-path.patch
Requires: ruby(abi) = %{rubyabi}
Requires: rubygems
Requires: rubygem(rack) >= 1.0.0
Requires: rubygem(eventmachine) >= 0.12.6
Requires: rubygem(daemons) >= 1.0.9
Requires: curl
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires: ruby-devel
BuildRequires: ruby(rubygems)
BuildRequires: curl
BuildRequires: libcurl-devel
BuildRequires: rubygem(rake-compiler)
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(rspec-core)
BuildRequires: rubygem(eventmachine) >= 0.12.6
BuildRequires: rubygem(daemons) >= 1.0.9
BuildRequires: rubygem(rack) >= 1.0.0
Provides: rubygem(%{gemname}) = %{version}

%description
Thin is a Ruby web server that glues together three of the best Ruby
libraries in web history.
The Mongrel parser, the root of Mongrel speed and security,
Event Machine, a network I/O library with extremely high scalability and
Rack, a minimal interface between webservers and Ruby frameworks.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires:%{name} = %{version}-%{release}

%description doc
Documentation for %{name}

%prep
%setup -q -c -T
mkdir -p ./%{gemdir}
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
gem install --local --install-dir ./%{gemdir} -V --force %{SOURCE0}

pushd .%{geminstdir}
%patch1

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{ruby_sitearch}/%{gemname}
mkdir -p %{buildroot}%{gemdir}
mkdir -p %{buildroot}%{_prefix}
cp -a ./%{gemdir}/* %{buildroot}%{gemdir}
mv -f %{buildroot}%{geminstdir}/lib/*.so %{buildroot}%{ruby_sitearch}/
mv -f %{buildroot}%{gemdir}/bin %{buildroot}%{_prefix}
for f in $(find %{buildroot}%{geminstdir} -name \*.rb); do
  sed -i -e '/^#!/d' $f
  chmod 0644 $f
done
find %{buildroot}%{geminstdir} -type f -exec sed -i 's/^#!\/usr\/local\/bin\/ruby/#!\/usr\/bin\/ruby/g' {} \;
chmod +x %{buildroot}%{geminstdir}/lib/thin/controllers/service.sh.erb
rm -rf %{buildroot}%{geminstdir}/{ext,tmp}/
rm -f %{buildroot}%{geminstdir}/{.autotest,.require_paths}

%check
# https://bugzilla.redhat.com/show_bug.cgi?id=566401
%ifarch ppc64
exit 0
%endif
pushd ./%{geminstdir}
SPECS=
RUBYOPT="rubygems I%{buildroot}%{geminstdir}/lib I%{buildroot}%{ruby_sitearch} Ispec Ibenchmark_unit" spec -b `echo "
PERF_SPECS = Dir['spec/perf/*_spec.rb'] + [ 'spec/server/pipelining_spec.rb' ]
WIN_SPECS = %w(
spec/backends/unix_server_spec.rb
spec/controllers/service_spec.rb
spec/daemonizing_spec.rb
spec/server/unix_socket_spec.rb
spec/server/swiftiply_spec.rb
)
SPECS2     = %w(spec/server/threaded_spec.rb spec/server/tcp_spec.rb)
puts Dir['spec/**/*_spec.rb'] - PERF_SPECS - WIN_SPECS - SPECS2
" | ruby`
popd

%files
%{_bindir}/%{gemname}
%{ruby_sitearch}/thin_parser.so
%dir %{geminstdir}/
%{geminstdir}/bin/
%dir %{geminstdir}/lib
%{geminstdir}/lib/thin.rb
%{geminstdir}/lib/rack/
%dir %{geminstdir}/lib/thin/
%{geminstdir}/lib/thin/*.rb
%{geminstdir}/lib/thin/backends/
%{geminstdir}/lib/thin/controllers/
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec
# BSD
%{geminstdir}/lib/thin/stats.html.erb

%files doc
%{gemdir}/doc/%{gemname}-%{version}
%{geminstdir}/benchmark/
%{geminstdir}/tasks/
%{geminstdir}/example/
%{geminstdir}/CHANGELOG
%{geminstdir}/README
%{geminstdir}/Rakefile
%dir %{geminstdir}/spec/
%{geminstdir}/spec/backends/
%{geminstdir}/spec/*.rb
%{geminstdir}/spec/configs/
%{geminstdir}/spec/controllers/
%{geminstdir}/spec/perf/
%{geminstdir}/spec/rack/
%{geminstdir}/spec/request/
%{geminstdir}/spec/server/
%dir %{geminstdir}/spec/rails_app/
%{geminstdir}/spec/rails_app/app/
%{geminstdir}/spec/rails_app/config/
%{geminstdir}/spec/rails_app/script/
# MIT
%doc %{geminstdir}/COPYING
%{geminstdir}/spec/rails_app/public/

%changelog
* Mon Jul 25 2011 Chris Lalancette <clalance@redhat.com> - 1.2.11-3
- Move stats.html.erb to the main package (it is a runtime requirement)

* Fri Jul 22 2011 Chris Lalancette <clalance@redhat.com> - 1.2.11-2
- Fix the load path for thin_parser

* Tue Mar 01 2011 Michal Fojtik <mfojtik@redhat.com> - 1.2.11-1
- Version bump

* Tue Mar 01 2011 Michal Fojtik <mfojtik@redhat.com> - 1.2.8-3
- Removed Rake dependency completely

* Tue Mar 01 2011 Michal Fojtik <mfojtik@redhat.com> - 1.2.8-2
- Fixed RSpec tests

* Tue Mar 01 2011 Michal Fojtik <mfojtik@redhat.com> - 1.2.8-1
- Updated to upstream version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 08 2010 Michal Fojtik <mfojtik@redhat.com> - 1.2.7-1
- Updated to upstream version

* Tue Feb 04 2010 Michal Fojtik <mfojtik@redhat.com> - 1.2.5-5
- Excluded ppc64 in tests (566401)
- Fixed Licensing

* Tue Feb 03 2010 Michal Fojtik <mfojtik@redhat.com> - 1.2.5-4
- Added rspec tests
- Fixed unwanted recompilation
- Fixed licensing

* Tue Feb 02 2010 Michal Fojtik <mfojtik@redhat.com> - 1.2.5-3
- Fixed description

* Tue Feb 02 2010 Michal Fojtik <mfojtik@redhat.com> - 1.2.5-2
- Build fixed
- Licence corrected
- Added missing requires
- Marked relevant files as documentation

* Tue Feb 02 2010 Michal Fojtik <mfojtik@redhat.com> - 1.2.5-1
- Initial package



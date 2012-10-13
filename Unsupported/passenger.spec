# RPM Spec file for Phusion Passenger
#
# The latest version of this file (as well as supporting files,
# documentation, and scripts to help build it) can be found here:
#
# http://github.com/erikogan/rubygem-passenger
#
# (If you fork this project feel free to add your repo below, but please
# do not remove the URL above.)

%define gemname passenger
%define passenger_version 3.0.2
%define passenger_release 1%{?dist}
%define passenger_epoch 1

%define httpd_confdir	%{_sysconfdir}/httpd/conf.d

# Macros on the command-line overrides these defaults. You should also
# make sure these match the binaries found in your PATH
%{?!ruby: %define ruby /usr/bin/ruby}

# Debug packages are currently broken. So don't even build them
%define debug_package %nil

%define ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")

%define gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define geminstdir %{gemdir}/gems/%{gemname}-%{passenger_version}

%define perldir %(perl -MConfig -e 'print $Config{installvendorarch}')

Summary: Easy and robust Ruby web application deployment
Name: rubygem-%{gemname}
Version: %{passenger_version}
Release: %{passenger_release}
Group: System Environment/Daemons
License: Modified BSD
URL: http://www.modrails.com/
Source0: %{gemname}-%{passenger_version}.tar.gz
Source100: apache-passenger.conf.in
Source200: rubygem-passenger.te
Patch0: passenger-force-native.patch
BuildRoot: %{_tmppath}/%{name}-%{passenger_version}-%{passenger_release}-root-%(%{__id_u} -n)
Requires: rubygems
Requires: rubygem(rake) >= 0.8.1
Requires: rubygem(fastthread) >= 1.0.1
Requires: rubygem(daemon_controller) >= 0.2.5
Requires: rubygem(file-tail)
Requires: rubygem(rack)
BuildRequires: ruby-devel
BuildRequires: httpd-devel
BuildRequires: rubygems
BuildRequires: rubygem(rake) >= 0.8.1
BuildRequires: rubygem(rack)
BuildRequires: rubygem(fastthread) >= 1.0.1
BuildRequires: libcurl-devel
BuildRequires: source-highlight
BuildRequires: doxygen
BuildRequires: asciidoc
BuildRequires: graphviz
# standaline build deps
BuildRequires: libev-devel
BuildRequires: rubygem(daemon_controller) >= 0.2.5
BuildRequires: rubygem(file-tail)
# native build deps
BuildRequires: selinux-policy
BuildRequires: zlib-devel
# Can't have a noarch package with an arch'd subpackage
#BuildArch: noarch
Provides: rubygem(%{gemname}) = %{passenger_version}
Epoch: %{passenger_epoch}

%description
Phusion Passenger™ — a.k.a. mod_rails or mod_rack — makes deployment
of Ruby web applications, such as those built on the revolutionary
Ruby on Rails web framework, a breeze. It follows the usual Ruby on
Rails conventions, such as “Don’t-Repeat-Yourself”.


%package doc
Summary: Phusion Passenger Server Docs
Group: System Environment/Daemons
Requires: %{name} = %{passenger_epoch}:%{passenger_version}-%{passenger_release}
Requires: libev
Epoch: %{passenger_epoch}

%description doc
Phusion Passenger docs.

%package -n mod_passenger
Summary: Apache Module for Phusion Passenger
Group: System Environment/Daemons
Requires: %{name} = %{passenger_epoch}:%{passenger_version}-%{passenger_release}
#BuildArch: %_target_arch
Requires: libev
Obsoletes: rubygem-passenger-apache
Epoch: %{passenger_epoch}
%description -n mod_passenger
Phusion Passenger™ — a.k.a. mod_rails or mod_rack — makes deployment
of Ruby web applications, such as those built on the revolutionary
Ruby on Rails web framework, a breeze. It follows the usual Ruby on
Rails conventions, such as “Don’t-Repeat-Yourself”.

This package contains the pluggable Apache server module for Passenger.

%define perlfileckinner $SIG{__WARN__} = sub {die @_};
%define perlfileck BEGIN { %perlfileckinner } ;

%prep
%setup -q -n %{gemname}-%{passenger_version}
%patch0 -p1

# Rather than hard-coding the path into the patch, change it here so
# that it's consistent with the %{ruby} macro, which might be defined on
# the command-line (4 %'s = 2)
perl -pi -e '%{perlfileck} s{%%%%GEM_INSTALL_DIR%%%%}{%{geminstdir}};s{%%%%APACHE_INSTALLED_MOD%%%%}{%{_libdir}/httpd/modules/mod_passenger.so}' lib/phusion_passenger.rb ext/common/ResourceLocator.h

# Fix the preferred version
perl -pi -e "s{(PREFERRED_NGINX_VERSION\s*=\s*(['\"]))[\d\.]+\2}{\${1}%{nginx_version}\$2}" lib/phusion_passenger.rb

# RPM finds these in shebangs and assumes they're requirements. Clean them up here rather than in the install-dir.
find test -type f -print0 | xargs -0 perl -pi -e '%{perlfileck} s{#!(/opt/ruby.*|/usr/bin/ruby1.8)}{/usr/bin/ruby}g'


%build
export USE_VENDORED_LIBEV=false
# This isn't honored
# export CFLAGS='%optflags -I/usr/include/libev'
export LIBEV_CFLAGS='-I/usr/include/libev'
export LIBEV_LIBS='-lev'

  rake package
  rake apache2

  ### SELINUX
  rm -rf selinux
  mkdir selinux
  cd selinux
  cp %{SOURCE200} .
  echo '%{geminstdir}/agents/(apache2/)?Passenger.*	system_u:object_r:httpd_exec_t:s0' > rubygem-passenger.fc
  echo '%{_var}/log/passenger-analytics	system_u:object_r:httpd_log_t:s0' >> rubygem-passenger.fc
  touch rubygem-passenger.if
  #make -f %{_datadir}/selinux/devel/Makefile
  cd ..

%install
export USE_VENDORED_LIBEV=false
# This isn't honored
# export CFLAGS='%optflags -I/usr/include/libev'
export LIBEV_CFLAGS='-I/usr/include/libev'
export LIBEV_LIBS='-lev'

rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}

gem install --local --install-dir %{buildroot}%{gemdir} \
               --force --rdoc pkg/%{gemname}-%{passenger_version}.gem
mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}%{gemdir}/bin/* %{buildroot}/%{_bindir}
rm -f %{buildroot}/%{_bindir}/passenger-install-nginx-module
rmdir %{buildroot}%{gemdir}/bin
# Nothing there
# find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x

mkdir -p %{buildroot}/%{_libdir}/httpd/modules
install -m 0644 ext/apache2/mod_passenger.so %{buildroot}/%{_libdir}/httpd/modules

mkdir -p %{buildroot}/%{httpd_confdir}
mkdir -p %{buildroot}/%{_var}/log/passenger-analytics

# I should probably figure out how to get these into the gem
cp -ra agents %{buildroot}/%{geminstdir}

# SELINUX
#install -p -m 644 -D selinux/%{name}.pp %{buildroot}%{_datadir}/selinux/packages/%{name}/%{name}.pp

##### NATIVE LIBS INSTALL
mkdir -p %{buildroot}/%{geminstdir}/ext/ruby/native
cp -ra ext/ruby/*-linux/* %{buildroot}/%{geminstdir}/ext/ruby/native

#### Clean up everything we don't care about
rm -f %{buildroot}%{perldir}/{auto/nginx/.packlist,perllocal.pod}
# RHEL distinguishes these dirs
rm -f %{buildroot}%(perl -MConfig -e 'print $Config{installarchlib}')/perllocal.pod

#install -m 0644 %{SOURCE100} %{buildroot}/%{httpd_confdir}/passenger.conf
perl -pe 's{%%ROOT}{%geminstdir}g;s{%%RUBY}{%ruby}g' %{SOURCE100} > %{buildroot}/%{httpd_confdir}/passenger.conf

# REMOVE THIS TO FORCE 'native-packaged' (it's still in doc)
rm %{buildroot}/%{geminstdir}/DEVELOPERS.TXT

%define base_files base-package-files

### BUILD FILE LIST (To remove files from the base package that will be installed by subpackages)
cat <<EOF > %{base_files}
%defattr(-, root, root, -)
%doc %{gemdir}/doc/%{gemname}-%{passenger_version}
%doc README
%doc DEVELOPERS.TXT
%{_bindir}/passenger
%{_bindir}/passenger-install-apache2-module
%{_bindir}/passenger-config
%{_bindir}/passenger-status
%{_bindir}/passenger-memory-stats
%{_bindir}/passenger-make-enterprisey
%{gemdir}/cache/%{gemname}-%{passenger_version}.gem
%{gemdir}/specifications/%{gemname}-%{passenger_version}.gemspec
EOF

# This feels wrong (reordering arch & os) but if it helps....
# ...Going one step further and also stripping all the installed *.o files
# Move the file find here to catch the byte-compiled Python files
#define __spec_install_post \
#   %{?__debug_package:%{__debug_install_post}} \
#   %{__os_install_post} \
#   find %{buildroot}/%{geminstdir} \\( -type d -name native \\) -prune -o \\( -type f -print \\) | perl -pe 's{^%{buildroot}}{};s{^//}{/};s/([?|*'\\''\"])/\\\\$1/g;s{(^|\\n$)}{\"$&}g' >> %{base_files} \
#   %{__arch_install_post}

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc README
%doc DEVELOPERS.TXT
%{_bindir}/passenger
%{_bindir}/passenger-install-apache2-module
%{_bindir}/passenger-config
%{_bindir}/passenger-status
%{_bindir}/passenger-memory-stats
%{_bindir}/passenger-make-enterprisey
%{gemdir}/cache/%{gemname}-%{passenger_version}.gem
%{gemdir}/specifications/%{gemname}-%{passenger_version}.gemspec
%{geminstdir}/LICENSE
%{geminstdir}/Rakefile
%{geminstdir}/agents
%{geminstdir}/b*
%{geminstdir}/debian
%{geminstdir}/dev
%{geminstdir}/ext
%{geminstdir}/helper*
%{geminstdir}/lib
%{geminstdir}/man
%{geminstdir}/resources*

%files doc
%defattr(-, root, root, -)
%doc %{gemdir}/doc/%{gemname}-%{passenger_version}
%{geminstdir}/doc
%{geminstdir}/test
%{geminstdir}/LICENSE
%{geminstdir}/PACKAGING*
%{geminstdir}/README
%{geminstdir}/INSTALL
%{geminstdir}/NEWS

%files -n mod_passenger
%doc doc/Users\ guide\ Apache.html
%doc doc/Users\ guide\ Apache.txt
%doc selinux
%{_libdir}/httpd/modules/mod_passenger.so
%config %{httpd_confdir}/passenger.conf
%{_var}/log/passenger-analytics
#{_datadir}/selinux/packages/%{name}/%{name}.pp

%changelog
* Thu Dec 16 2010 Erik Ogan <erik@stealthymonkeys.com> - 3.0.2-1
- Bump to 3.0.2

* Mon Dec 13 2010 Erik Ogan <erik@stealthymonkeys.com> - 3.0.1-4
- rename rubygem-passenger-standalone to passenger-standalone
- Add graphviz to the build requirements (for /usr/bin/dot)

* Thu Dec  2 2010 Erik Ogan <erik@stealthymonkeys.com> - 3.0.1-3
- Stop double-packaging files from -native & -native-libs in the base package

* Tue Nov 30 2010 Erik Ogan <erik@stealthymonkeys.com> - 3.0.1-2
- Remove (most of) the kludges to remove %%{builddir} from installed files.
- Blessed natively-packaged patch from Hong Li
- Migration to the more static directory structure

* Mon Nov 29 2010 Erik Ogan <erik@stealthymonkeys.com> - 3.0.1-1
- Integration into passenger source
- Bump to 3.0.1

* Mon Nov 15 2010 Erik Ogan <erik@stealthymonkeys.com> - 3.0.0-11
- Fix passenger-standalone

* Fri Nov 12 2010 Erik Ogan <erik@stealthymonkeys.com> - 3.0.0-10
- Bump nginx to version 0.8.53 and build it by hand based on the newer
  nginx specfile

* Sun Nov  7 2010 Erik Ogan <erik@stealthymonkeys.com> - 3.0.0-9
- Add passenger-analytics directory, so the server doesn't try to create
  it. (SELinux violation)

* Sun Oct 31 2010 Erik Ogan <erik@stealthymonkeys.com> - 3.0.0-8
- Fix embedded Perl module

* Fri Oct 29 2010 Erik Ogan <erik@stealthymonkeys.com> - 3.0.0-7
- Add back all the missing directives from nginx.spec (Perl is
  untested and may be broken)

* Fri Oct 29 2010 Erik Ogan <erik@stealthymonkeys.com> - 3.0.0-6
- Add upstream-fair load-balancer back to nginx
- Add the original CFLAGS back to nginx (with -Wno-unused kludge for RHEL5)

* Sat Oct 23 2010 Erik Ogan <erik@cloudshield.com> - 3.0.0-5
- RHEL/CentOS Ruby is too old to support RUBY_PATCHLEVEL

* Sat Oct 23 2010 Erik Ogan <erik@stealthymonkeys.com> - 3.0.0-4
- --define 'only_native_libs 1' to rebuild native_support.so for a
  different ruby engine.
- make sure native-libs release includes passenger release and ruby patch level
- remove the macros that rely on %%{_builddir} already being unpacked

* Fri Oct 22 2010 Erik Ogan <erik@stealthymonkeys.com> - 3.0.0-3
- Break the passenger_native_support.so into its own package

* Thu Oct 21 2010 Erik Ogan <erik@stealthymonkeys.com> - 3.0.0-2
- rename rubygem-passenger-apache => mod_passenger

* Thu Oct 21 2010 Erik Ogan <erik@stealthymonkeys.com> - 3.0.0-1
- Version bump to 3.0.0

* Wed Oct 18 2010 Erik Ogan <erik@stealthymonkeys.com> - 3.0.0.pre4-2
- use nginx-alternatives

* Sun Oct 17 2010 Erik Ogan <erik@stealthymonkeys.com> - 3.0.0.pre4-1
- Nginx suport

* Mon Oct 11 2010 Erik Ogan <erik@stealthymonkeys.com> - 3.0.0.pre4-0
- Test for Gem::Version issues with the version and work around it.
- Initial Spec File

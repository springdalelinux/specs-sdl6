%global ruby_sitearch %(ruby -rrbconfig -e "puts Config::CONFIG['sitearchdir']")
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname eventmachine
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary:    Ruby/EventMachine library
Name:       rubygem-%{gemname}
Version:    0.12.10
Release:    4%{?dist}
Group:      Development/Languages
License:    GPLv2 or Ruby
URL:        http://rubyeventmachine.com
Source0:    http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
Requires:   rubygems
Requires:   ruby(abi) = 1.8
Provides:   rubygem(%{gemname}) = %{version}
BuildRequires: rubygems, ruby-devel, openssl-devel, rubygem(rake), net-tools

%description
EventMachine implements a fast, single-threaded engine for arbitrary network
communications. It's extremely easy to use in Ruby. EventMachine wraps all
interactions with IP sockets, allowing programs to concentrate on the
implementation of network protocols. It can be used to create both network
servers and clients. To create a server or client, a Ruby program only needs
to specify the IP address and port, and provide a Module that implements the
communications protocol. Implementations of several standard network protocols
are provided with the package, primarily to serve as examples. The real goal
of EventMachine is to enable programs to easily interface with other programs
using TCP/IP, especially if custom protocols are required.

%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.


%prep
%setup -q -T -c

%build
mkdir -p .%{gemdir}
gem install -V \
    --local \
    --install-dir $(pwd)/%{gemdir} \
    --force --rdoc \
    %{SOURCE0}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
mkdir -p %{buildroot}%{ruby_sitearch}
cp -a ./%{gemdir}/* %{buildroot}/%{gemdir}/

rm -rf %{buildroot}%{geminstdir}/{ext,java,.gitignore,setup.rb,%{gemname}.gemspec}
mv %{buildroot}%{geminstdir}/lib/*.so %{buildroot}%{ruby_sitearch}

%clean
rm -rf %{buildroot}

#check
#pushd .%{geminstdir}
## no kqueue support on Linux
#rm -f tests/test_process_watch.rb
#rake test || :

%files
%defattr(-, root, root, -)
%doc %{geminstdir}/README
%dir %{geminstdir}/
%{geminstdir}/lib
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec
%{ruby_sitearch}/rubyeventmachine.so
%{ruby_sitearch}/fastfilereaderext.so

%files doc
%defattr(-, root, root, -)
%{gemdir}/doc/%{gemname}-%{version}
%{geminstdir}/Rakefile
%{geminstdir}/docs
%{geminstdir}/examples
%{geminstdir}/tasks
%{geminstdir}/tests
%{geminstdir}/web

%changelog
* Tue Sep 28 2010 Michael Stahnke <stahnma@fedoraproject.org> - 0.12.10-4
- Doc package can't be noarch, due to rpmdiff oddity 

* Sun Jan 31 2010 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.12.10-3
- More review fixes

* Sun Jan 31 2010 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.12.10-2
- Review fixes (#556433)

* Mon Jan 18 2010 Ruben Kerkhof <ruben@rubenkerkhof.com> - 0.12.10-1
- Initial package

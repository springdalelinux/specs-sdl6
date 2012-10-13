%{!?ruby_sitelib: %define ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")}
%{!?ruby_sitearch: %define ruby_sitearch %(ruby -rrbconfig -e "puts Config::CONFIG['sitearchdir']")}

Name:           ruby-file-tail
Version:        1.0.5
Release:        1%{?dist}
Summary:        Ruby utility to allow tail in ruby
Group:          Development/Languages

License:        GPLv2+
URL:            http://flori.github.com/file-tail/
Source0:        http://www.ping.de/~flori/file-tail-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:	noarch

BuildRequires:  ruby ruby-devel rubygem(rake)
BuildRequires:  pkgconfig
Requires:       ruby(abi) = 1.8
Provides:       ruby(file-tail) = %{version}
Provides:	rubygem(file-tail) = %{version}

%description
This Library is similar to Perl's File::Tail. It can be used to extend Ruby's 
File-objects, as mixin for own File-derived classes, or by using the included
simple File::Tail::Logfile class. 

%prep
%setup -q -n file-tail-%{version}

%build
rake doc

%install
rm -rf %{buildroot}
install -d -m0755 %{buildroot}%{ruby_sitelib}/file/tail
install -p -m0644 lib/file/tail.rb %{buildroot}%{ruby_sitelib}/file/
install -p -m0644 lib/file/tail/version.rb %{buildroot}%{ruby_sitelib}/file/tail/

install -d -m0755 %{buildroot}%{_bindir}
install -p -m0755 bin/rtail %{buildroot}%{_bindir}/

%clean
rm -rf $RPM_BUILD_ROOT

%check
rake test

%files
%defattr(-,root,root,-)
%doc COPYING CHANGES README examples doc/*
%dir %{ruby_sitelib}/file
%dir %{ruby_sitelib}/file/tail
%{ruby_sitelib}/file/tail.rb
%{ruby_sitelib}/file/tail/version.rb
%{_bindir}/rtail

%changelog
* Fri Jan 14 2011 Josko Plazonic <plazonic@math.princeton.edu>
- initial build

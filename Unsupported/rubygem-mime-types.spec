# Generated from mime-types-1.16.gem by gem2rpm -*- rpm-spec -*-
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname mime-types
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

%global rubyabi 1.8

Summary: Return the MIME Content-Type for a given filename
Name: rubygem-%{gemname}
Version: 1.16
Release: 3%{?dist}
Group: Development/Languages
License: GPL+ or Ruby or Artistic
URL: http://mime-types.rubyforge.org/
Source0: http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
# Currently produces a "RCov is not available" warning and fails with newer rcov
# installed. Reported upstream via
# http://rubyforge.org/tracker/?func=detail&aid=27623&group_id=293&atid=1191
Patch0: mime-types-1.16-no_rcov.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: ruby(rubygems)
Requires: ruby(abi) = %{rubyabi}
BuildRequires: ruby(rubygems)
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires(check): rubygem(hoe)
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
MIME::Types for Ruby manages a MIME Content-Type database that will return the
Content-Type for a given filename.

MIME::Types was originally based on and synchronized with MIME::Types for
Perl by Mark Overmeer, copyright 2001 - 2009. As of version 1.15, the data
format for the MIME::Type list has changed and the synchronization will no
longer happen.

%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%prep
%setup -q -c -T

mkdir -p .%{gemdir}
gem install -V \
  --local \
  --install-dir $(pwd)/%{gemdir} \
  --force --rdoc \
  %{SOURCE0}

pushd .%{geminstdir}
%patch0 -p1

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
cp -a .%{gemdir}/* %{buildroot}%{gemdir}/

# These aren't executables
find %{buildroot}%{geminstdir}/{Rakefile,test} -type f | \
  xargs -n 1 sed -i  -e '/^#! \/usr\/bin\/env .*/d'

%clean
rm -rf %{buildroot}

%check
pushd .%{geminstdir}
rake test

%files
%defattr(-,root,root,-)
%doc %{geminstdir}/History.txt
%doc %{geminstdir}/Install.txt
%doc %{geminstdir}/Licence.txt
%doc %{geminstdir}/README.txt
%dir %{geminstdir}
%{geminstdir}/lib
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%defattr(-,root,root,-)
%{geminstdir}/Rakefile
%{geminstdir}/setup.rb
%{geminstdir}/mime-types.gemspec
%{geminstdir}/Manifest.txt
%{geminstdir}/test
%{gemdir}/doc/%{gemname}-%{version}

%changelog
* Wed Dec 30 2009 Matthew Kent <mkent@magoazul.com> - 1.16-3
- Remove needless rcov task in Rakefile causing issue (#544964).

* Sun Dec 27 2009 Matthew Kent <mkent@magoazul.com> - 1.16-2
- Fix license (#544964).
- Add note about rcov warning in test phase (#544964).

* Sun Dec 06 2009 Matthew Kent <mkent@magoazul.com> - 1.16-1
- Initial package

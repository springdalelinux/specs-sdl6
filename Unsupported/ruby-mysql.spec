%{!?ruby_sitearch: %define ruby_sitearch %(/usr/bin/ruby -rrbconfig -e "puts Config::CONFIG['sitearch']")}
%{!?ruby_sitearchdir: %define ruby_sitearchdir %(/usr/bin/ruby -rrbconfig -e "puts Config::CONFIG['sitearchdir']")}

Name:           ruby-mysql
Version:        2.8.2
Release:        1%{?dist}
Summary:        A Ruby interface to MySQL

Group:          Development/Languages
License:        Ruby
URL:            http://www.tmtm.org/en/mysql/ruby/

Source0:        http://tmtm.org/downloads/mysql/ruby/mysql-ruby-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  ruby ruby-devel mysql-devel

%description
This is the MySQL API module for Ruby. It provides the same functions for
Ruby programs that the MySQL C API provides for C programs.

%prep
%setup -q -n mysql-ruby-%{version}

%build
ruby extconf.rb --with-mysql-config
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
env DESTDIR=$RPM_BUILD_ROOT make install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README.html README_ja.html tommy.css COPYING COPYING.ja 
%{ruby_sitearchdir}/mysql.so

%changelog
* Thu Jul 8 2010 Orion Poplawski <orion@cora.nwra.com> - 2.8.2-1
- Update to 2.8.2

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.8-4
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 23 2009 Orion Poplawski <orion@cora.nwra.com> - 2.8-1
- Update to 2.8

* Fri Mar  7 2008 Orion Poplawski <orion@cora.nwra.com> - 2.7.5-1
- Update to 2.7.5

* Sat Feb  9 2008 Orion Poplawski <orion@cora.nwra.com> - 2.7.4-1
- Update to 2.7.4

* Wed Dec  5 2007 Orion Poplawski <orion@cora.nwra.com> - 2.7.3-3
- Rebuild for new openssl

* Thu Aug 23 2007 Orion Poplawski <orion@cora.nwra.com> - 2.7.3-2
- Update license tag to Ruby
- Rebuild for BuildID

* Thu May 17 2007 Orion Poplawski <orion@cora.nwra.com> - 2.7.3-1
- Update to 2.7.3

* Wed Oct  3 2006 Orion Poplawski <orion@cora.nwra.com> - 2.7.1-2
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 Orion Poplawski <orion@cora.nwra.com> - 2.7.1-1
- Update to 2.7.1

* Tue Feb 28 2006 Oliver Andrich <oliver.andrich@gmail.com> - 2.7-8
- changed the license to Distributable based on Bug #179933

* Fri Feb 04 2006 Oliver Andrich <oliver.andrich@gmail.com> - 2.7-6
- fixed the build problems in x86_64

* Fri Feb 03 2006 Oliver Andrich <oliver.andrich@gmail.com> - 2.7-5
- included the license documents COPYING and COPYING.ja
- fixed the license: Distributable -> GPL

* Sun Jan 22 2006 Oliver Andrich <oliver.andrich@gmail.com> - 2.7-4
- fixed changelog (next try)
- moved the package to the suggested group Development/Languages
- added %{?_smp_mflags} to the make call in the build phase
- the summary duplication in the description was removed 

* Sun Jan 22 2006 Oliver Andrich <oliver.andrich@gmail.com> - 2.7-3
- added documentation
- fixed changelog 

* Sun Jan 22 2006 Oliver Andrich <oliver.andrich@gmail.com> - 2.7-1
- First build

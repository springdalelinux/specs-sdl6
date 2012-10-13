%{!?ruby_sitelib: %define ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")}
%{!?ruby_sitearch: %define ruby_sitearch %(ruby -rrbconfig -e "puts Config::CONFIG['sitearchdir']")}

Name:           ruby-ldap
Version:        0.9.7 
Release:        10%{?dist}
Summary:        Ruby LDAP libraries
Group:          Development/Languages
License:        BSD 
URL:            http://%{name}.sourceforge.net/   
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Filed in upstream bugtracker at:
# https://sourceforge.net/tracker/?func=detail&aid=2775056&group_id=66444&atid=514521
Patch0:         %{name}-0.9.7-openldap.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ruby ruby-devel openldap-devel openssl-devel 
Requires:       ruby(abi) = 1.8 
Provides:       ruby(ldap) = %{version}-%{release}


%description
Ruby/LDAP is an extension library for Ruby. It provides the interface to
some LDAP libraries (e.g. OpenLDAP, UMich LDAP, Netscape SDK,
ActiveDirectory). The common API for application development
is described in RFC1823 and is supported by Ruby/LDAP.


%prep
%setup -q
%patch0 -p1
find example/ -type f | xargs %{__chmod} 0644


%build
export CFLAGS="$RPM_OPT_FLAGS"
ruby extconf.rb
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p" install
 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc TODO README ChangeLog example FAQ
# For noarch packages: ruby_sitelib
%{ruby_sitelib}/ldap 
# For arch-specific packages: ruby_sitearch
%{ruby_sitearch}/ldap.so


%changelog
* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.9.7-10
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 19 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 0.9.7-8
- Fix FTBFS: Added ruby-ldap-0.9.7-openldap.patch

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.9.7-6
- rebuild with new openssl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.7-5
- Autorebuild for GCC 4.3

* Wed Dec 05 2007 Michael Stahnke <mastahnke@gmail.com> - 0.9.7-4
- Bump for rebuild because of openldap bump

* Mon Oct 29 2007 Michael Stahnke <mastahnke@gmail.com> - 0.9.7-3
- More modifications from bug 346241

* Sun Oct 28 2007 Michael Stahnke <mastahnke@gmail.com> - 0.9.7-2
- Package modifications from bug 346241

* Mon Oct 22 2007 Michael Stahnke <mastahnke@gmail.com> - 0.9.7-1
- Initial Package for Fedora 

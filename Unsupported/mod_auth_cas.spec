Name:           mod_auth_cas
Version:        1.0.9.1
Release:        4%{?dist}
Summary:        Apache 2.0/2.2 compliant module that supports the CASv1 and CASv2 protocols

Group:          System Environment/Daemons
License:        GPLv3+ with exceptions
URL:            http://www.ja-sig.org/wiki/display/CASC/mod_auth_cas
# The source for this package was pulled from the upstream's vcs. Their 
# releases are stored in SVN instead of exported to a tar.gz, I used the 
# following commands to do so:
#  svn export https://source.jasig.org/cas-clients/mod_auth_cas/tags/mod_auth_cas-1.0.9.1 mod_auth_cas-1.0.9.1

#  tar -czvf mod_auth_cas-1.0.9.1.tar.gz mod_auth_cas-1.0.9.1/
Source0:        mod_auth_cas-1.0.9.1.tar.bz2
Source1:        auth_cas.conf
Patch1:		sslfix.patch

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  openssl-devel
BuildRequires:  httpd-devel
BuildRequires:	libcurl-devel

Requires:       httpd

%description
mod_auth_cas is an Apache 2.0/2.2 compliant module that supports the CASv1
and CASv2 protocols

%prep
%setup -q
%patch1 -p1 -b .sslfix


%build
%configure --with-apxs=%{_sbindir}/apxs
make %{?_smp_mflags}



%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

mkdir -p %{buildroot}/%{_sysconfdir}/httpd/conf.d
install -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/auth_cas.conf


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README
%{_libdir}/httpd/modules/*.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf

%changelog
* Tue Oct 18 2011 Adam Miller <maxamillion@fedoraproject.org> - 1.0.8.1-3
- Fixed auth_cas.conf as per BZ# 708550 (Thanks to Jimmy Ngo) for the patch

* Tue Jun 29 2010 Adam Miller <maxamillion@fedoraproject.org> - 1.0.8.1-2
- Fixed svn export link, upstream changed canonical URL names.

* Wed Apr 28 2010 Adam Miller <maxamillion@fedoraproject.org> - 1.0.8.1-1
- added requires of httpd 
- fixed mixed use of macros
- updated to latest version

* Fri Aug 07 2009 Adam Miller <maxamillion@fedoraproject.org> - 1.0.8-1
- First attempt to package mod_auth_cas for Fedora


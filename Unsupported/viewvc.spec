%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           viewvc
Version:        1.1.13
Release:        1%{?dist}
Summary:        Browser interface for CVS and SVN version control repositories

Group:          Development/Tools
License:        BSD
URL:            http://www.viewvc.org/
Source0:        http://www.viewvc.org/%{name}-%{version}.tar.gz
Source1:        viewvc.conf
Source2:        README.httpd
Source3:        viewvc-lexer-mimetypes.py
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Obsoletes:      %{name}-selinux < 1.0.3-13
Conflicts:      selinux-policy < 2.5.10-2

BuildArch:      noarch
BuildRequires:  python-devel >= 2.0, python-pygments
Requires:       rcs, diffutils
Requires:       subversion >= 1.2
Requires:       cvsgraph
Requires:       python-pygments

%description
ViewVC is a browser interface for CVS and Subversion version control
repositories. It generates templatized HTML to present navigable directory,
revision, and change log listings. It can display specific versions of files
as well as diffs between those versions. Basically, ViewVC provides the bulk
of the report-like functionality you expect out of your version control tool,
but much more prettily than the average textual command-line program output.

%package httpd
Summary:        ViewVC configuration for Apache/mod_python
Group:          Development/Tools
Requires:       httpd, %{name} = %{version}-%{release}, mod_python

%description httpd
ViewVC configuration for Apache/mod_python. This package should provide ViewVC
with decent performance when run under Apache.

%prep
%setup -q

%build

%install
%{__rm} -rf %{buildroot}
%{__python} viewvc-install --destdir="%{buildroot}" --prefix="%{python_sitelib}/viewvc"

# Remove unneeded files
%{__rm} -f %{buildroot}%{python_sitelib}/viewvc/bin/mod_python/.htaccess

# Move non-python to /usr/share
%{__mkdir} -p %{buildroot}%{_datadir}/viewvc
%{__mv} %{buildroot}%{python_sitelib}/viewvc/templates %{buildroot}%{_datadir}/viewvc

# Fix python files shebang and CONF_PATHNAME
%{__perl} -pi \
  -e 's|/usr/local/bin/python|%{_bindir}/python|g;' \
  -e 's|\s*/usr/bin/env python|%{_bindir}/python|g;' \
  -e 's|CONF_PATHNAME =.*|CONF_PATHNAME = r"%{_sysconfdir}/viewvc/viewvc.conf"|g;' \
  $(find %{buildroot}%{python_sitelib}/viewvc/ -type f)

# Set mode 755 on executable scripts
%{__grep} -rl '^#!' %{buildroot}%{python_sitelib}/viewvc | xargs %{__chmod} 0755

# Fix paths in configuration
%{__perl} -pi \
  -e 's|^#* *template_dir = .*|template_dir = %{_datadir}/viewvc/templates|g;' \
  -e 's|^#* *docroot = .*|docroot = /viewvc-static|;' \
  -e 's|^#* *cvsgraph_conf = .*|cvsgraph_conf = %{_sysconfdir}/viewvc/cvsgraph.conf|;' \
  -e 's|^#* *use_cvsgraph = .*|use_cvsgraph = 1|;' \
  %{buildroot}%{python_sitelib}/viewvc/viewvc.conf

# Install config to sysconf directory
%{__install} -Dp -m0644 %{buildroot}%{python_sitelib}/viewvc/viewvc.conf %{buildroot}%{_sysconfdir}/viewvc/viewvc.conf
%{__rm} -f %{buildroot}%{python_sitelib}/viewvc/viewvc.conf
%{__install} -Dp -m0644 %{buildroot}%{python_sitelib}/viewvc/cvsgraph.conf %{buildroot}%{_sysconfdir}/viewvc/cvsgraph.conf
%{__rm} -f %{buildroot}%{python_sitelib}/viewvc/cvsgraph.conf
%{__install} -Dp -m0644 %{buildroot}%{python_sitelib}/viewvc/mimetypes.conf %{buildroot}%{_sysconfdir}/viewvc/mimetypes.conf
%{__rm} -f %{buildroot}%{python_sitelib}/viewvc/mimetypes.conf

%{SOURCE3} >> %{buildroot}%{_sysconfdir}/viewvc/mimetypes.conf

# Install Apache configuration and README
%{__sed} -e s,__datadir__,%{_datadir}, \
         -e s,__python_sitelib__,%{python_sitelib}, %{SOURCE1} > viewvc.conf
%{__install} -Dp -m0644 viewvc.conf %{buildroot}/etc/httpd/conf.d/viewvc.conf
%{__cp} %{SOURCE2} README.httpd

# mod_python files mustn't be executable since they don't have shebang
# make rpmlint happy!
%{__chmod} 0644 %{buildroot}%{python_sitelib}/viewvc/bin/mod_python/*.py

# Rename viewvc.py to viewvc-mp.py for mod_python to avoid import cycle errors
%{__mv} %{buildroot}%{python_sitelib}/viewvc/bin/mod_python/viewvc.py \
        %{buildroot}%{python_sitelib}/viewvc/bin/mod_python/viewvc-mp.py

# Make spool directory for temp files
%{__mkdir} -p %{buildroot}%{_localstatedir}/spool/viewvc

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc CHANGES README README.httpd INSTALL COMMITTERS LICENSE.html docs
%config(noreplace) %{_sysconfdir}/viewvc
%{python_sitelib}/*
%{_datadir}/*

%files httpd
%defattr(-, root, root, -)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/viewvc.conf
%attr(0700,apache,apache) %{_localstatedir}/spool/viewvc

%changelog
* Tue Jan 24 2012 Bojan Smojver <bojan@rexursive.com> - 1.1.13-1
- bump up to 1.1.13

* Fri Nov  4 2011 Bojan Smojver <bojan@rexursive.com> - 1.1.12-1
- bump up to 1.1.12

* Wed Jun  1 2011 Bojan Smojver <bojan@rexursive.com> - 1.1.11-2
- in response to bug #708721:
-   remove webserver dependency, can run standalone
-   require httpd for httpd package
-   move spool directory to httpd package

* Wed May 18 2011 Bojan Smojver <bojan@rexursive.com> - 1.1.11-1
- bump up to 1.1.11

* Wed Mar 16 2011 Bojan Smojver <bojan@rexursive.com> - 1.1.10-1
- bump up to 1.1.10

* Mon Feb 21 2011 Bojan Smojver <bojan@rexursive.com> - 1.1.9-1
- bump up to 1.1.9

* Tue Dec  7 2010 Bojan Smojver <bojan@rexursive.com> - 1.1.8-1
- bump up to 1.1.8

* Thu Jun  3 2010 Bojan Smojver <bojan@rexursive.com> - 1.1.6-1
- bump up to 1.1.6
- drop patch for upstream issue #454

* Tue May 25 2010 Bojan Smojver <bojan@rexursive.com> - 1.1.5-2
- patch upstream issue #454

* Tue Mar 30 2010 Bojan Smojver <bojan@rexursive.com> - 1.1.5-1
- bump up to 1.1.5

* Thu Mar 11 2010 Bojan Smojver <bojan@rexursive.com> - 1.1.4-1
- bump up to 1.1.4

* Fri Jan  8 2010 Bojan Smojver <bojan@rexursive.com> - 1.1.3-2
- patch upstream issue #445

* Wed Dec 23 2009 Bojan Smojver <bojan@rexursive.com> - 1.1.3-1
- bump up to 1.1.3
- drop patch for upstream issue #427

* Wed Sep 23 2009 Bojan Smojver <bojan@rexursive.com> - 1.1.2-5
- patch upstream issue #427

* Thu Aug 13 2009 Bojan Smojver <bojan@rexursive.com> - 1.1.2-4
- try one more time

* Thu Aug 13 2009 Bojan Smojver <bojan@rexursive.com> - 1.1.2-3
- better mimetypes.conf generation script

* Wed Aug 12 2009 Bojan Smojver <bojan@rexursive.com> - 1.1.2-2
- fix replacement of various config variables

* Wed Aug 12 2009 Bojan Smojver <bojan@rexursive.com> - 1.1.2-1
- bump up to 1.1.2
- security fix: validate the 'view' parameter to avoid XSS attack
- security fix: avoid printing illegal parameter names and values

* Tue Aug 11 2009 Bojan Smojver <bojan@rexursive.com> - 1.1.1-3
- install mimetypes.conf
- populate mimetypes.conf with what pygments understands

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun  4 2009 Bojan Smojver <bojan@rexursive.com> - 1.1.1-1
- Bump up to 1.1.1

* Thu May 14 2009 Bojan Smojver <bojan@rexursive.com> - 1.1.0-1
- Final 1.1.0

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-0.beta1.1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.1.0-0.beta1.1.1
- Rebuild for Python 2.6

* Thu Nov  6 2008 Bojan Smojver <bojan@rexursive.com> - 1.1.0-0.beta1.1
- Rebase to 1.1.x

* Mon Oct 27 2008 Bojan Smojver <bojan@rexursive.com> - 1.0.7-2
- Depend on webserver to avoid pulling in Apache/mod_python (bug #457691)
- Provide viewvc-httpd package for mod_python specific configuration

* Wed Oct 15 2008 Bojan Smojver <bojan@rexursive.com> - 1.0.7-1
- Bump up to 1.0.7

* Fri Sep 19 2008 Bojan Smojver <bojan@rexursive.com> - 1.0.6-1
- Bump up to 1.0.6

* Fri Feb 29 2008 Bojan Smojver <bojan@rexursive.com> - 1.0.5-1
- Bump up to 1.0.5

* Sun Jun  3 2007 Bojan Smojver <bojan@rexursive.com> - 1.0.4-2
- Avoid import cycle errors (temporary fix)

* Tue May 15 2007 Bojan Smojver <bojan@rexursive.com> - 1.0.4-1
- Bump up to 1.0.4

* Wed Mar 28 2007 Bojan Smojver <bojan@rexursive.com> - 1.0.3-13
- Supply obsoletes/conflicts
  (suggestions by Peter Gordon, Bernard Johnson and Ville Skyttä)

* Thu Mar 22 2007 Bojan Smojver <bojan@rexursive.com> - 1.0.3-12
- Drop selinux package, required context now in official policy

* Fri Mar 09 2007 Bojan Smojver <bojan@rexursive.com> - 1.0.3-11
- Bump for tag

* Tue Mar 06 2007 Bojan Smojver <bojan@rexursive.com> - 1.0.3-10
- Enable enscript only when available

* Tue Mar 06 2007 Bojan Smojver <bojan@rexursive.com> - 1.0.3-9
- Enable cvsgraph

* Sun Mar 04 2007 Bojan Smojver <bojan@rexursive.com> - 1.0.3-8
- EPEL support patch by Bernard Johnson

* Sat Mar 03 2007 Bojan Smojver <bojan@rexursive.com> - 1.0.3-7
- Incorporate suggestions from package review process by Bernard Johnson

* Sat Mar 03 2007 Bojan Smojver <bojan@rexursive.com> - 1.0.3-6
- Use restorecon instead of chcon

* Fri Mar 02 2007 Bojan Smojver <bojan@rexursive.com> - 1.0.3-5
- SELinux integration

* Fri Mar 02 2007 Bojan Smojver <bojan@rexursive.com> - 1.0.3-4
- Incorporate suggestions from package review process by Bernard Johnson

* Fri Mar 02 2007 Bojan Smojver <bojan@rexursive.com> - 1.0.3-3
- Move non-python files out of %%{python_sitelib}

* Thu Mar 01 2007 Bojan Smojver <bojan@rexursive.com> - 1.0.3-2
- Incorporate suggestions from package review process by Bernard Johnson

* Thu Mar 01 2007 Bojan Smojver <bojan@rexursive.com> - 1.0.3-1
- Initial release, 1.0.3
- Based on package provided by Dag Wieers

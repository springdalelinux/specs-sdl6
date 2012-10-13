%global svnrev 11401

Name:           trac-spamfilter-plugin
Version:        1.0
Release:        1%{svnrev}%{?dist}
Summary:        Spam-Filter plugin for Trac
Group:          Applications/Internet
License:        BSD
URL:            http://trac.edgewall.org/wiki/SpamFilter
Source0:        plugins_%{version}_spam-filter-%{svnrev}.tar.bz2
Source1:        pull-from-svn.sh
BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       trac >= 0.12
Requires:       python-dns
Requires:       python-imaging
Requires:       python-setuptools
Requires:       spambayes

%description
TracSpamFilter is a plugin for Trac (http://trac.edgewall.com/) that provides
an infrastructure for detecting and rejecting spam (or other forms of
illegitimate/unwanted content) in submitted content.

%prep
%setup -q -n plugins

%build
cd 1.0/spam-filter
%{__python} setup.py build

%install
cd 1.0/spam-filter
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
 
%files
%doc 1.0/spam-filter/README.txt
%{python_sitelib}/TracSpamFilter-*.egg-info/
%{python_sitelib}/tracspamfilter/

%changelog
* Fri Oct 12 2012 Thomas Uphill <uphill@ias.edu> - 1.0-1
- update to 1.0

* Sun Jul 17 2011 Paul Howarth <paul@city-fan.org> - 0.4.7-0.11.20110716svn10756
- Update to current svn snapshot
  - Various Blogspam timeout fixes
  - Add links to kill spammy users (Upstream #10093)
  - Add proper check for Defensio and python < 2.6 (Upstream #10195)
  - Add cleanup code to remove obsolete captcha db entries
  - Fix issues with different SQL engines (Upstream #10227)
  - Fix wrong argument count in log message (Upstream #10264)
  - Fix possibly uninitialized value (Upstream #10261)
- No need for %%defattr

* Mon Mar 21 2011 Paul Howarth <paul@city-fan.org> - 0.4.7-0.10.20110305svn10633
- Update to current svn snapshot
  - Add BlogSpam service
  - Add Defensio service
- Update pull-from-svn script to set time of tarball to that of last commit
- Drop BuildRoot tag and explicit buildroot cleaning
- No need to define %%{python_sitelib}

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-0.9.20101210svn10366
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 13 2010 Paul Howarth <paul@city-fan.org> - 0.4.3-0.8.20101210svn10366
- Update to current svn snapshot
- Plugin requires trac >= 0.12, so drop EL4 support
- Add dependency on python-dns for DNS blacklist support
- Add dependency on python-imaging for captcha support
- Add pull-from-svn script for creation of tarball

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.2.1-0.7.20090714svn8330
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-0.6.20090714svn8330
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Paul Howarth <paul@city-fan.org> - 0.2.1-0.5.20090714svn8330
- Update to rev8330, addresses upstream tickets #6130, #7627, #8032, #8121, #8257

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-0.4.20080603svn6990
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.2.1-0.3.20080603svn6990
- Rebuild for Python 2.6

* Fri Jul 04 2008 Jesse Keating <jkeating@redhat.com> - 0.2.1-0.2.20080603svn6990
- R spambayes

* Tue Jun 03 2008 Jesse Keating <jkeating@redhat.com> - 0.2.1-0.1.20080603svn6990
- Initial packaging


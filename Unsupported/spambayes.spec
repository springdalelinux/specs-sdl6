%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%global pre a6

Name:           spambayes
Version:        1.1
Release:        0.2.%{pre}%{?dist}
Summary:        Bayesian anti-spam filter

Group:          Development/Languages
License:        Python
URL:            http://spambayes.sourceforge.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}%{pre}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel

%if 0%{?fedora} >= 8
BuildRequires:  python-setuptools-devel
%else
BuildRequires:  python-setuptools
%endif

Requires:       python-lockfile


%description
SpamBayes will attempt to classify incoming email messages as 'spam', 'ham'
(good, non-spam email) or 'unsure'. This means you can have spam or unsure
messages automatically filed away in a different mail folder, where it won't
interrupt your email reading. First SpamBayes must be trained by each user to
identify spam and ham. Essentially, you show SpamBayes a pile of email that
you like (ham) and a pile you don't like (spam). SpamBayes will then analyze
the piles for clues as to what makes the spam and ham different. For example;
different words, differences in the mailer headers and content style.  The
system then uses these clues to examine new messages.


%prep
%setup -q -n %{name}-%{version}%{pre}

# Fix rpmlint warnings
chmod -x *.txt


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} -c 'import setuptools; execfile("setup.py")' build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} -c 'import setuptools; execfile("setup.py")' install --skip-build --root $RPM_BUILD_ROOT

# Add exec permission for modules that can be run directly
for f in $RPM_BUILD_ROOT%{python_sitelib}/spambayes/*.py; do
  if head -n 1 $f | grep '^#![[:space:]]*/usr/bin/env python'; then
    chmod +x $f
  fi
done

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc *.txt
%{python_sitelib}/spambayes*
%{_bindir}/core_server.py
%{_bindir}/sb_*.py


%changelog
* Fri Dec 10 2010 Paul Howarth <paul@city-fan.org> - 1.1-0.2.a6
- Add exec permission for modules that can be run directly
- Remove references to unused patch
- Add missing dependency on python-lockfile (#661942)

* Sun Sep 12 2010 Thomas Janssen <thomasj@fedoraproject.org> 1.1-0.1.a6
- update to 1.1a6

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.0.4-10
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Sep  7 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 1.0.4-9
- Fix FTBFS: remove %%exclude of Python's byte-compiled files under %%{_bindir},
  not necessary anymore (has been fixed in brp-python-bytecompile)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0.4-6
- Rebuild for Python 2.6

* Wed Oct 17 2007 Christopher Stone <chris.stone@gmail.com> 1.0.4-5
- Providing Eggs for non-setuptools packages (bz#325041)

* Fri Apr 27 2007 Christopher Stone <chris.stone@gmail.com> 1.0.4-4
- Remove python from package name

* Thu Apr 05 2007 Christopher Stone <chris.stone@gmail.com> 1.0.4-3
- Add patch to fix python2.5 errors

* Thu Apr 05 2007 Christopher Stone <chris.stone@gmail.com> 1.0.4-2
- %%exclude pyo and pyc files from %%{_bindir}
- Add scriptlet to remove shebangs

* Sat Mar 31 2007 Christopher Stone <chris.stone@gmail.com> 1.0.4-1
- Initial Fedora release

%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define pyver %(python -c 'import sys ; print sys.version[:3]')

Name:          pyzor
Version:       0.5.0
Release:       3%{?dist}
Summary:       Pyzor collaborative spam filtering system
Group:         Applications/Internet
# COPYING is GPLv2; usage.html indicates v2+.  No statements in the code itself.
License:       GPLv2+
URL:           http://pyzor.sourceforge.net/
Source0:       http://downloads.sourceforge.net/pyzor/pyzor-%{version}.tar.bz2
Patch0:        pyzor-0.5.0-ignore-deprecation-warning.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
BuildRequires: python >= 2.2.1

%description
Pyzor is a collaborative, networked system to detect
and block spam using identifying digests of messages.
Pyzor is similar to Vipul's Razor except implemented
in python, and using fully open source servers.

Pyzor can be used either standalone, or to augment the
spam filtering ability of spamassassin.  spamassassin
is highly recommended.

%prep
%setup -q
%patch0 -p1


%build
%__python setup.py build


%install
rm -rf %{buildroot}
install -m755 -d %{buildroot}%{python_sitelib}/pyzor
install -p -m644 build/lib/pyzor/* %{buildroot}%{python_sitelib}/pyzor
install -m755 -d %{buildroot}%{_bindir}
install -p -m755 build/scripts-%{pyver}/* %{buildroot}%{_bindir}
%__python -c 'from compileall import *; compile_dir("'%{buildroot}'/%{python_sitelib}",10,"%{python_sitelib}")'
%__python -O -c 'from compileall import *; compile_dir("'%{buildroot}'/%{python_sitelib}",10,"%{python_sitelib}")'
chmod -R a+rX %{buildroot}/%{python_sitelib}/pyzor %{buildroot}%{_bindir}/pyzor*


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%dir %{python_sitelib}/pyzor
%doc docs/usage.html COPYING NEWS README THANKS UPGRADING PKG-INFO
%attr(0644,root,root) %{python_sitelib}/pyzor/client.py*
%attr(0644,root,root) %{python_sitelib}/pyzor/server.py*
%attr(0644,root,root) %{python_sitelib}/pyzor/__init__.py*
%attr(0755,root,root) %{_bindir}/pyzor
%attr(0755,root,root) %{_bindir}/pyzord


%changelog
* Thu Nov 05 2009 Warren Togami <wtogami@redhat.com> - 0.5.0-3
- -Wignore::DeprecationWarning to make it work (#531653)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 14 2009 Andreas Thienemann <andreas@bawue.net> - 0.5.0-1
- Update to new upstream release 0.5.0
- Dropped unnecessary patches

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.4.0-14
- Rebuild for Python 2.6

* Thu Aug 14 2008 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.4.0-13
- Fix failing build too.

* Thu Aug 14 2008 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.4.0-12
- Fix license tag.

* Sat Dec 23 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.4.0-11
- Rebuild with Python 2.5.

* Fri Sep 08 2006 Andreas Thienemann <andreas@bawue.net> - 0.4.0-10
- FE6 Rebuild
- Feature enhancements by including certain patches from swinog.

* Mon Feb 07 2005 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.4.0-8
- %%ghost *.pyo files.

* Sat Feb 05 2005 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.4.0-7
- Use python_sitelib macro to fix building on x86_64.
- Change byte compile argumetns so we don't encode the buildroot into the
  byte compiled python files.
- Use python-abi for Requires instead of python package.

* Sat Nov 13 2004 Warren Togami <wtogami@redhat.com> - 0.4.0-6
- bump release

* Fri May 21 2004 Warren Togami <wtogami@redhat.com> - 0.4.0-0.fdr.5
- generalize python version

* Fri Jul 11 2003 Warren Togami <warren@togami.com> - 0.4.0-0.fdr.4
- Change to __python macro

* Fri Jun 27 2003 Warren Togami <warren@togami.com> - 0.4.0-0.fdr.3
- #360 add more docs

* Sat Jun 21 2003 Warren Togami <warren@togami.com> - 0.4.0-0.fdr.2
- Fix some directory macros
- #360 Include .pyc and .pyo so package removes cleanly
- #360 install -p preserve timestamps

* Sun Jun 08 2003 Warren Togami <warren@togami.com> - 0:0.4.0-0.fdr.1
- Convert to Fedora

* Fri Jan 31 2003 Shad L. Lords <slords@mail.com>
- 0.4.0-1
- inital release

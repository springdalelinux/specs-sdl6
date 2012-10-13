Summary: A tool for monitoring the progress of data through a pipeline
Name: pv
Version: 1.3.1
Release: 3%{?dist}
License: Artistic 2.0
Group: Development/Tools
Source: http://pipeviewer.googlecode.com/files/%{name}-%{version}.tar.gz
URL: http://www.ivarch.com/programs/pv.shtml
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)


BuildRequires: gettext


%description
PV ("Pipe Viewer") is a tool for monitoring the progress of data through a
pipeline.  It can be inserted into any normal pipeline between two processes
to give a visual indication of how quickly data is passing through, how long
it has taken, how near to completion it is, and an estimate of how long it
will be until completion.


%prep
%setup -q
mv README README.iso8859
iconv -f ISO-8859-1 -t UTF-8 README.iso8859  > README
mv doc/NEWS doc/NEWS.iso8859
iconv -f ISO-8859-1 -t UTF-8 doc/NEWS.iso8859 > doc/NEWS

%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p ${RPM_BUILD_ROOT}%{_bindir}         # /usr/bin
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1    # /usr/share/man/man1

make DESTDIR=$RPM_BUILD_ROOT install
%find_lang %{name}


%check
make test


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-, root, root)
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz

%doc README doc/NEWS doc/TODO doc/COPYING


%changelog
* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 13 2008 Jakub Hrozek <jhrozek@redhat.com> - 1.1.4-1
- Bump to the latest upstream
- Convert NEWS and README to UTF8 during prep

* Mon Feb 11 2008 Jakub Hrozek <jhrozek@redhat.com> - 1.1.0-3
- Rebuild for GCC 4.3

* Sat Sep 15 2007 Jakub Hrozek <jhrozek@redhat.com> - 1.1.0-2
- Fix the license tag

* Sat Sep 15 2007 Jakub Hrozek <jhrozek@redhat.com> - 1.1.0-1
- Bump to the latest upstream

* Mon Aug 13 2007 Jakub Hrozek <jhrozek@redhat.com> - 1.0.1-1
- Bump to latest upstream

* Sun Jun 24 2007 Jakub Hrozek <jhrozek@redhat.com> - 0.9.9-1
- Initial packaging loosely based on SRPM from project's home page by 
  Andrew Wood <andrew.wood@ivarch.com>

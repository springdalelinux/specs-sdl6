Name:           xlhtml
Summary:        Excel 95/97 and PowerPoint to HTML converter
Version:        0.5
Release:        11%{?dist}

License:        GPLv2+
Group:          Applications/Text
Source0:        http://dl.sf.net/chicago/xlhtml-%{version}.tgz
URL:            http://chicago.sourceforge.net/xlhtml/
BuildRequires:  autoconf
BuildRequires:  automake
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The xlhtml program will take an Excel 95, or 97 file as input and
convert it to HTML. The output is via standard out so it can be
re-directed to files or piped to filters or used as a gateway to the
internet. pptHtml program converts PowerPoint files to HTML.


%prep
%setup -q

%build
rm -f config.{guess,sub}
aclocal
autoconf
automake -a
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf xlhtml/contrib/CVS


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc xlhtml/contrib xlhtml/{README,THANKS,TODO,ChangeLog}
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 01 2009 Robert Scheck <robert@fedoraproject.org> 0.5-10
- Solve the x86_64-redhat-linux-gnu configure target error

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.5-8
- Autorebuild for GCC 4.3

* Sun Aug 26 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.5-7
- fix license tag
- rebuild for BuildID

* Thu Aug 31 2006 Aurelien Bompard <abompard@fedoraproject.org> 0.5-6
- rebuild

* Tue Feb 21 2006 Aurelien Bompard <gauret[AT]free.fr> 0.5-5
- rebuild for FC5

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 0.5-4
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Fri Jun 25 2004 Aurelien Bompard <gauret[AT]free.fr> 0:0.5-0.fdr.2
- cleanup spec file

* Thu May 13 2004 Aurelien Bompard <gauret[AT]free.fr> 0:0.5-0.fdr.1
- initial Fedora RPM (from PLD)

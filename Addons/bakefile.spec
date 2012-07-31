Name:           bakefile
Version:        0.2.8
Release:        3%{?dist}
Summary:        A cross-platform, cross-compiler native makefiles generator
Group:          Development/Tools
License:        MIT
URL:            http://www.bakefile.org/
Source:         http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libxml2-python python-devel
Requires:       python >= 2.3.0 automake python-empy

%description
Bakefile is cross-platform, cross-compiler native makefiles generator. It takes
compiler-independent description of build tasks as input and generates native
makefile (autoconf's Makefile.in, Visual C++ project, bcc makefile etc.)

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS NEWS README THANKS
%{_bindir}/bakefil*
%{_datadir}/bakefile
%{_mandir}/man1/bakefil*
%{_libdir}/bakefile*
%exclude %{_libdir}/%{name}/empy
%exclude %{_libdir}/%{name}/py25modules
%exclude %{_libdir}/%{name}/_bkl_c.la
%{_datadir}/aclocal/*.m4

%changelog
* Tue Mar 02 2010 Filipe Rosset <rosset.filipe@gmail.com> - 0.2.8-3
- Fixed Source url
- Updated BuildRequires and Requires info
- Empy python module packaged independently
- Removed files of uuid and subprocess python modules
- Removed .la files

* Tue Dec 22 2009 Filipe Rosset <rosset.filipe@gmail.com> - 0.2.8-2
- Replaced summary information
- Updated BuildRequires and Requires information
- Replaced "{_mandir}/man1/bakefil*.gz" to "{_mandir}/man1/bakefil*"
- Correct URL and source URL
- Replaced "%%{_libdir}/*" to "%%{_libdir}/bakefile*"
- Removed useless line: "%%doc"

* Mon Dec 21 2009 Filipe Rosset <rosset.filipe@gmail.com> - 0.2.8-1
- Initial RPM release

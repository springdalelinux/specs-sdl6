Name:           libtiger
Version:        0.3.3
Release:        3%{?dist}
Summary:        Rendering library for Kate streams using Pango and Cairo

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://libtiger.googlecode.com
Source0:        http://libtiger.googlecode.com/files/libtiger-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libkate-devel >= 0.2.7
BuildRequires:  pango-devel
BuildRequires:  valgrind
BuildRequires:  doxygen


%description
Libtiger is a rendering library for Kate streams using Pango and Cairo.
More information about Kate streams may be found at 
http://wiki.xiph.org/index.php/OggKate


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pango-devel
Requires:       libkate-devel >= 0.2.7

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        doc
Summary:        Documentation for %{name}
Group:          Documentation
BuildArch:      noarch

%description    doc
The %{name}-doc package contains Documentation for %{name}.



%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT __doc
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Fix timestramps change
touch -r include/tiger/tiger.h.in $RPM_BUILD_ROOT%{_includedir}/tiger/tiger.h

# Move docdir
mv $RPM_BUILD_ROOT%{_docdir}/%{name} __doc

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/tiger/
%{_libdir}/*.so
%{_libdir}/pkgconfig/tiger.pc

%files doc
%defattr(-,root,root,-)
%doc examples __doc/html


%changelog
* Fri Feb  5 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.3.3-3
- Only pick __doc/html in the doc subpackage.

* Tue Jan 26 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.3.3-2
- Split doc subpackage

* Thu Jul  2 2009 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.3.3-1
- Update to 0.3.3

* Fri Nov 28 2008 kwizart < kwizart at gmail.com > - 0.3.2-1
- Update to 0.3.2

* Thu Sep  4 2008 kwizart < kwizart at gmail.com > - 0.1.1-1
- Initial spec file


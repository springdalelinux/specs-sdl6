Name:           snappy
Version:        1.0.4
Release:        3%{?dist}
Summary:        Fast compression and decompression library

Group:          System Environment/Libraries
License:        BSD
URL:            http://code.google.com/p/snappy/
Source0:        http://snappy.googlecode.com/files/%{name}-%{version}.tar.gz

BuildRequires:  gtest-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Snappy is a compression/decompression library. It does not aim for maximum 
compression, or compatibility with any other compression library; instead, it 
aims for very high speeds and reasonable compression. For instance, compared to 
the fastest mode of zlib, Snappy is an order of magnitude faster for most 
inputs, but the resulting compressed files are anywhere from 20% to 100% 
bigger. 


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure CXXFLAGS="%{optflags} -DNDEBUG" --disable-static
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_datadir}/doc/snappy/
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%clean
rm -rf %{buildroot}

%check
make check


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/libsnappy.so.*

%files devel
%defattr(-,root,root,-)
%doc format_description.txt
%{_includedir}/snappy*.h
%{_libdir}/libsnappy.so


%changelog
* Tue Jan 17 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.0.4-3
- Add in buildroot stuff for EL5 build

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 16 2011 Martin Gieseking <martin.gieseking@uos.de> 1.0.4-1
- updated to release 1.0.4

* Sat Jun 04 2011 Martin Gieseking <martin.gieseking@uos.de> 1.0.3-1
- updated to release 1.0.3
- added format description to devel package

* Fri Apr 29 2011 Martin Gieseking <martin.gieseking@uos.de> 1.0.2-1
- updated to release 1.0.2
- changed License to BSD
- dropped the patch as it has been applied upstream

* Thu Mar 24 2011 Martin Gieseking <martin.gieseking@uos.de> 1.0.0-3
- added file COPYING from the upstream repo

* Thu Mar 24 2011 Martin Gieseking <martin.gieseking@uos.de> 1.0.0-2
- replaced $CXXFLAGS with %%{optflags} in %%build section
- removed empty %%doc entry from %%files devel

* Thu Mar 24 2011 Martin Gieseking <martin.gieseking@uos.de> 1.0.0-1
- initial package


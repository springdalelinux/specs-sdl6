Name:           liblzf
Version:        3.6
Release:        2%{?dist}
Summary:        Small data compression library

Group:          System Environment/Libraries
License:        BSD or GPLv2+
URL:            http://oldhome.schmorp.de/marc/liblzf.html
Source0:        http://dist.schmorp.de/liblzf/liblzf-%{version}.tar.gz
# Adds autoconf and in particular support for building shared libraries.
# 7th Feb 2011 - Mail sent upstream to author. Awaiting conclusion. 
Patch0:         liblzf-%{version}-autoconf.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool

%description
LibLZF is a very small data compression library. It consists 
of only two .c and two .h files and is very easy to 
incorporate into your own programs.  The compression algorithm 
is very, very fast, yet still written in portable C.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%if 0%{?el4}%{?el5}
Requires:       pkgconfig
%endif


%description    devel
The liblzf-devel package contains libraries and header files for
developing applications that use liblzf.

%prep
%setup -q
%patch0 -p1

%build
sh ./bootstrap.sh
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
# Binary does different things depending
# on the name it is called by.
pushd %{buildroot}%{_bindir}
ln -s lzf unlzf
#Leave lzcat  out since it conflicts with xz-lzma-compat.
#If ever needed would need an alternative setting up,
#if someone ever asks I'll do it.
#ln -s lzf lzcat
popd
rm -f %{buildroot}%{_libdir}/liblzf.la

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/lzf
%{_bindir}/unlzf
%{_libdir}/liblzf.so.*
# The cs directory contains a .net implementation of lzf.
# Will happily add a .net sub package if given a patch.
%doc README Changes LICENSE cs

%files devel
%defattr(-,root,root,-)
%{_includedir}/lzf.h
%{_libdir}/liblzf.so
%{_libdir}/pkgconfig/liblzf.pc

%changelog
* Mon Feb 14 2012 Steve Traylen <steve.traylen@cern.ch> - 3.6-2
- Add a .pc file in autoconf patch as well.
- Drop lzcat since conflicts with xz-lzma-compat

* Mon Feb 7 2011 Steve Traylen <steve.traylen@cern.ch> - 3.6-1
- First version of package.

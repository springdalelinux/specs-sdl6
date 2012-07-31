Name:			mpir
Version:		1.3.1
Release:		4%{?dist}
Summary:		A library for arbitrary precision arithmetic

Group:			System Environment/Libraries
License:		LGPLv2+
URL:			http://www.mpir.org/
Source0:		http://www.mpir.org/%{name}-%{version}.tar.gz
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	autoconf automake libtool
BuildRequires:	yasm

%description
MPIR is an open source multiprecision integer library derived from
version 4.2.1 of the GMP (GNU Multi Precision) project.

%package  		devel
Summary:		Development files for %{name}
Group:			Development/Libraries
Requires:		%{name} = %{version}-%{release}

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build

# we only need to autoreconf with the new autoconfs
%if 0%{?fedora} || 0%{?rhel} > 5
autoreconf -if
%endif

CCAS="gcc -c -Wa,--noexecstack" \
CFLAGS="%{optflags}" \
LDFLAGS="%{optflags} -Wl,-z,noexecstack" \
CXXFLAGS="%{optflags}" \
./configure --build=%{_build} --host=%{_host} \
	--program-prefix=%{?_program_prefix} \
	--prefix=%{_prefix} \
	--exec-prefix=%{_exec_prefix} \
	--bindir=%{_bindir} \
	--sbindir=%{_sbindir} \
	--sysconfdir=%{_sysconfdir} \
	--datadir=%{_datadir} \
	--includedir=%{_includedir} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--localstatedir=%{_localstatedir} \
	--sharedstatedir=%{_sharedstatedir} \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--enable-mpbsd \
	--enable-cxx \
	--disable-rpath \
	--disable-strip \
	--disable-static

# Remove YASM, just use the system yasm
rm -rf yasm
mkdir yasm
ln -s %{_bindir}/yasm yasm/
cat > yasm/Makefile << EOT
all install check: 
	/bin/true
EOT

# Remove the RPATH
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool

export LD_LIBRARY_PATH=`pwd`/.libs

# Convert AUTHORS file to UTF-8
iconv --from=ISO-8859-1 --to=UTF-8 AUTHORS -o AUTHORS.conv
# Preserve the Timestamp
touch -r AUTHORS AUTHORS.conv
mv -f AUTHORS.conv AUTHORS

# Compile
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -exec rm -f {} ';'
rm -rf %{buildroot}/usr/share/info/dir
mv doc/devel doc/html

%check
export LD_LIBRARY_PATH=`pwd`/.libs
make check

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel 
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%postun devel
if [ $1 = 0 ] ; then
	/sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYING.LIB README
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/html demos
%{_includedir}/*
%{_libdir}/*.so
%{_infodir}/mpir.info*

%changelog
* Tue Mar 16 2010 Mark Chappell <tremble@fedoraproject.org> - 1.3.1-4
- Fix the RHEL build

* Fri Mar 05 2010 Mark Chappell <tremble@fedoraproject.org> - 1.3.1-3
- Include HTML documentation
- Include demos

* Thu Mar 04 2010 Mark Chappell <tremble@fedoraproject.org> - 1.3.1-2
- Ensure consistent use of macros
- Avoid multilib conflict due to modified timestamp on AUTHORS doc
- Replace perl find and replace with sed

* Wed Feb 17 2010 M D Chappell <tremble@tremble.org.uk> - 1.3.1-1
- Initial build

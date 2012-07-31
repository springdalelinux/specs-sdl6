%define kmod_name pvfs2

# we need this
%define mrelease  4%{?dist}

Name:		orangefs
Summary:	Orange File System
Version:	2.8.4
Release:        %{mrelease}
License:	LGPL/GPL
Group: 		System Environment/Base
URL: 		http://www.orangefs.net/
Source0: 	ftp://ftp.parl.clemson.edu/pub/orangefs/orangefs-%{version}.tar.gz
Patch2:		orangefs-2.8.3.filestweak.patch
Buildroot:	%{_tmppath}/%{name}-buildroot
ExclusiveArch:  i686 x86_64
BuildRequires:	db48-devel openssl-devel tetex-dvips tetex-latex latex2html ghostscript bison flex
Requires:	%{name}-libs = %{version}-%{release}
BuildRequires: libibverbs libibverbs-devel
Obsoletes:	pvfs2
Provides:	pvfs2
BuildRequires:  %kernel_module_package_buildreqs
%kernel_module_package
%description
Orange File System is a branch of the Parallel Virtual File System. Like PVFS,
Orange is a parallel file system designed for use on high end computing (HEC)
systems that provides very high performance access to disk storage for parallel
applications.

%package karma
Group:          System Environment/Base
Summary:	karma GUI for OrangeFS
Requires: %{name} = %{version}-%{release}
BuildRequires:	SDL-devel SDL_ttf-devel gtk2-devel
Provides: pvfs2-karma
Obsoletes: pvfs2-karma

%description karma
karma GUI for OrangeFS

%package libs
Group:          System Environment/Base
Summary:        OrangeFS libraries
Provides:      pvfs2-libs
Obsoletes:     pvfs2-libs

%description libs
OrangeFS libraries

%package devel
Group:          System Environment/Development
Summary:        OrangeFS development files
Requires:       %{name}-libs = %{version}-%{release}
Provides:	pvfs2-devel
Obsoletes:	pvfs2-devel

%description devel
OrangeFS development files


%prep
%setup -q -c orangefs
%patch2 -p0 -b .filestweak
mkdir kernel

%build
cd orangefs
# Kill the stack protection and fortify source stuff...it slows things down
# and orangefs hasn't been audited for it yet
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-Wp,-D_FORTIFY_SOURCE=.//' | sed -e 's/-fstack-protector//'`
#ifarch x86_64
#export CFLAGS="$RPM_OPT_FLAGS -fPIC"
#endif
# new gcc doesn't like unused variables and that causes failures with kernel configure checks, as they are done with -Werror
export CFLAGS="$RPM_OPT_FLAGS -Wno-unused-variable"
# get i686 compiled
%ifarch %{ix86}
export CFLAGS="$CFLAGS -Wno-strict-aliasing"
%endif
# we will really only do this once, easiest way to get the first param out
for flavor in %flavors_to_build; do
%configure --with-kernel=%{kernel_source $flavor} --with-openib=/usr --enable-shared
break
done
# clean first to fix a bug in building
make clean
make
make docs
make kernapps

# now build modules
cd src/kernel/linux-2.6
make clean
cd ..
for flavor in %flavors_to_build ; do
	cp -a linux-2.6 _kmod_build_${flavor}
	make -C %{kernel_source $flavor} SUBDIRS=$PWD/_kmod_build_${flavor} M=$PWD/_kmod_build_${flavor} Q=@ modules
done

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_includedir}
cd orangefs
%makeinstall
mkdir -p $RPM_BUILD_ROOT/%{_initrddir}
install -m 755 examples/pvfs2-server.rc $RPM_BUILD_ROOT/%{_initrddir}/pvfs2-server
install -m 755 examples/pvfs2-client.rc $RPM_BUILD_ROOT/%{_initrddir}/pvfs2-client
mkdir -p $RPM_BUILD_ROOT/sbin
# mount.pvfs2 should not be required for 2.6 kernels
#for i in mount.pvfs2 pvfs2-client pvfs2-client-core; do
for i in pvfs2-client pvfs2-client-core; do
	install -m 755 src/apps/kernel/linux/$i $RPM_BUILD_ROOT/sbin
done

# install modules
cd src/kernel
export INSTALL_MOD_PATH=$RPM_BUILD_ROOT
export INSTALL_MOD_DIR=extra/%{name}
for flavor in %flavors_to_build ; do
	make -C %{kernel_source $flavor} modules_install \
		           M=$PWD/_kmod_build_${flavor}
	#pushd _kmod_build_$kvariant
	#mkdir 		 -p $RPM_BUILD_ROOT/lib/modules/%{kverrel}${kvariant}/extra/%{kmod_name}
	#install -m 644 *.ko $RPM_BUILD_ROOT/lib/modules/%{kverrel}${kvariant}/extra/%{kmod_name}
	#popd
done
# remove spurious modules files
find $RPM_BUILD_ROOT/lib/modules/ -type f -not -name \*.ko | xargs rm -f

%clean
rm -rf $RPM_BUILD_ROOT

%post 
/sbin/ldconfig
/sbin/chkconfig --add pvfs2-server
/sbin/chkconfig --add pvfs2-client

%postun -p /sbin/ldconfig

%preun
if [ "$1" -eq 0 ]; then
	/sbin/chkconfig --del pvfs2-server
	/sbin/chkconfig --del pvfs2-client
fi

%files
%defattr(-,root,root,-)
%doc orangefs/doc/*.pdf orangefs/COPYING orangefs/README orangefs/ChangeLog 
%{_bindir}/pvfs*
%{_bindir}/*etmattr
%{_sbindir}/*
/sbin/*
%{_mandir}/*/*
%{_initrddir}/*

%files karma
%defattr(-,root,root,-)
%{_bindir}/karma

%files libs
%defattr(-,root,root,-)
%{_libdir}/libpv*so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/libpv*a
%{_libdir}/libpv*so

%changelog
* Mon Feb 21 2011 Josko Plazonic <plazonic@math.princeton.edu>
- convert to orangefs

* Wed May 26 2010 Josko Plazonic <plazonic@math.princeton.edu>
- build for rhel6

* Thu Jan 03 2008 Josko Plazonic <plazonic@math.princeton.edu>
- new version - 2.7.0

* Thu Sep 12 2007 Josko Plazonic <plazonic@math.princeton.edu>
- rebuild for PU_IAS 5

* Thu Jun 22 2006 Josko Plazonic <plazonic@math.princeton.edu>
- Rebuild for 2.6 kernel (2/2WS)

%define		singulardir	%{_datadir}/singular

Name:		singular
Summary:	Computer Algebra System for polynomial computations
Version:	3.1.3
Release:	3.1%{?dist}
License:	GPL
Group:		Sciences/Mathematics
Source0:	http://www.mathematik.uni-kl.de/ftp/pub/Math/Singular/SOURCES/3-1-3/Singular-3-1-3-3.tar.gz
Source1:	Singular-3-1-3-3.share.tar.gz
Source4:	fix-singular-includes.pl
Source5:	singular.hlp
Source6:	singular.idx
URL:		http://www.singular.uni-kl.de/

BuildRequires:	gmp-devel ntl-devel flex ncurses-devel readline-devel
BuildRequires:  bison-devel boost-devel
#BuildRequires:  libfac-devel factory-devel
Requires:	surf

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
SINGULAR is a Computer Algebra system for polynomial computations with
special emphasize on the needs of commutative algebra, algebraic
geometry, singularity theory and polynomial system solving. For a more
detailed overview of SINGULAR, see
     http://www.singular.uni-kl.de/Overview/

%package	devel
Group:		Development/Other
Summary:	Singular development files
Obsoletes:	%{name}-devel < 3.0.4-2
Provides:	%{name}-devel = %{version}-%{release}

%description	devel
This package contains the Singular development files.

%package	static
Group:		Development/Other
Summary:	Singular static libraries
Provides:	%{name}-static-devel = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}

%description	static
This package contains the Singular static libraries.

%prep
%setup -q -n Singular-3-1-3 -a 1

%build
find . -type d -name CVS -exec rm -fr {} \; 2> /dev/null || :

#   There is no way, other then patching all Makefiles.in by hand
# to make it respect DESTDIR ..., so build it pretending %{buildroot}
# is part of prefix, and correct the few wrong usages later.
#   It should be possible to build with proper --prefix, and use
# the install-sharedist target, but it will fail before, when trying
# to create directories in %{_prefix} during build.
export CXXFLAGS="%{optflags} -fPIC"
export CFLAGS="%{optflags} -fPIC"
#export LDFLAGS="--build-id"
export LD=gcc

#   Must use system ntl
rm -fr ntl

./configure						\
	--prefix=%{buildroot}%{_prefix}			\
	--exec-prefix=%{buildroot}%{_prefix}		\
	--includedir=%{buildroot}%{_includedir}		\
	--libdir=%{buildroot}%{_libdir}			\
	--with-malloc=system				\
	--with-apint=gmp				\
	--with-gmp=%{_prefix}				\
	--with-ntl=%{_prefix}				\
	--with-NTL					\
	--without-MP					\
	--without-lex					\
	--with-bison					\
	--with-Boost					\
	--enable-factory				\
	--enable-libfac					\
	--enable-Singular				\
	--enable-IntegerProgramming			\
	--enable-Texinfo				\
	--enable-Texi2html				\
	--enable-doc					\
	--enable-emacs

#perl -pi					\
#	-e 's|(#define\s+HAVE_BOOST)|//$1|g;'	\
#	`find . -name \*.h`

make

# need MP to build doc or will lock on failed tcp connection
#pushd doc
#    make SINGULAR=%{buildroot}%{singulardir}/%{arch}/Singular-3-1-1 all
#popd

#perl -pi					\
#	-e 's|%{buildroot}||g;'			\
#	-e 's|--with-external-config[^ ]+||g;'	\
#	-e "s|\s*--cache-file[^']+||;"		\
#	-e 's|in %{builddir}[^"]+||g;'		\
#    kernel/mod2.h				\
#    Singular/mod2.h				\
#    factory/factoryconf.h			\
#    factory/config.h

# correct compilation by default without exceptions,
# but including c++ headers that generate exceptions
# (/usr/include/boost/dynamic_bitset/dynamic_bitset.hpp)
#perl -i						\
#	-e 's|--no-exceptions|-fexceptions|g;'	\
#    `find . -name configure\*`

# these are not rebuilt after updating headers
#rm -f Singular/Singular %{buildroot}%{_prefix}/Singular-3-1-1
## run make once more to recompile anything dependent on the patched headers.
#make all libsingular

%install
#makeinstall_std install-libsingular
%makeinstall

pushd %{buildroot}%{_prefix}
  mkdir -p %{buildroot}%{singulardir}/%{_arch}
  mv -f	bin/* Singular* %{_lib}/*.o  %{_lib}/lib*.a \
	%{buildroot}%{singulardir}/%{_arch}
  rm -f LIB

  pushd %{buildroot}%{_includedir}
    [ -d %{name} ] || mkdir %{name}
    mv -f *.h templates %{name}
  popd
popd

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{singulardir}/LIB
mv Singular/LIB/* %{buildroot}%{singulardir}/LIB/
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/Singular << EOF
#!/bin/sh

SINGULARPATH=%{singulardir}/LIB %{singulardir}/%{_arch}/Singular-3-1-3 \$*
EOF
chmod +x %{buildroot}%{_bindir}/Singular
ln -sf %{_bindir}/Singular %{buildroot}%{_bindir}/singular

perl -pi -e								\
	's|(java -jar) (surfex.jar)|$1 %{singulardir}/LIB/$2|;'		\
	%{buildroot}%{singulardir}/LIB/surfex

# these headers are included by installed ones, but not installed...
mkdir -p %{buildroot}%{_includedir}/%{name}/Singular
cp -fa Singular/*.h %{buildroot}%{_includedir}/%{name}/Singular

# correct includes
perl %{SOURCE4}
perl -pi -e 's|%{buildroot}||g' %{buildroot}%{_includedir}/singular/*.h %{buildroot}%{_includedir}/singular/*/*.h

# files required during sagemath build, and/or side effect of sagemath patch
cp kernel/kInline.cc %{buildroot}%{_includedir}/%{name}
cp Singular/{attrib,grammar,ipid,ipshell,lists,subexpr,tok}.h  %{buildroot}%{_includedir}/%{name}

# installed headers are only readable by file owner...
chmod -R a+r %{buildroot}
find %{buildroot}%{_includedir} -type f -exec chmod a-x {} \;

cp Singular/3-1-3/doc/singular.idx Singular/3-1-3/info/singular.hlp %{buildroot}%{singulardir}
rm -rf Singular/3-1-3/doc Singular/3-1-3/info Singular/3-1-3/LIB
pushd %{buildroot}%{singulardir}/%{_arch}
rm -f Singular
ln -s Singular-3* Singular
popd

export QA_SKIP_BUILD_ROOT=1

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc Singular/3-1-3/*
%{_bindir}/Singular
%{_bindir}/singular
%dir %{singulardir}
%dir %{singulardir}/%{_arch}
%{singulardir}/%{_arch}/ESingular
%{singulardir}/%{_arch}/LLL
%{singulardir}/%{_arch}/Singular-3-1-3
%{singulardir}/%{_arch}/TSingular
%{singulardir}/%{_arch}/Singular
%{singulardir}/%{_arch}/change_cost
%{singulardir}/%{_arch}/gen_test
%{singulardir}/%{_arch}/libparse
%{singulardir}/%{_arch}/solve_IP
%{singulardir}/%{_arch}/surfex
%{singulardir}/%{_arch}/toric_ideal
%{singulardir}/LIB
%{singulardir}/singular.*

%files		devel
%defattr(-,root,root)
%{singulardir}/%{_arch}/*.so
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*

%files		static
%defattr(-,root,root)
%{singulardir}/%{_arch}/*.o
%{singulardir}/%{_arch}/*.a


%changelog
* Wed Jun 01 2011 Paulo Andrade <pcpa@mandriva.com.br> 3.1.1-4mdv2011.0
+ Revision: 682293
- Rebuild ensuring it does not use its local modified copy of ntl

* Tue Mar 08 2011 Paulo Andrade <pcpa@mandriva.com.br> 3.1.1-3
+ Revision: 642824
- Rebuild singular with its local/modified ntl build

* Thu Sep 23 2010 Paulo Andrade <pcpa@mandriva.com.br> 3.1.1-2mdv2011.0
+ Revision: 580795
- Update prebuilt documentation files to match singular version

* Wed Sep 22 2010 Paulo Andrade <pcpa@mandriva.com.br> 3.1.1-1mdv2011.0
+ Revision: 580442
- Update to Singular 3.1.1

* Thu Feb 11 2010 Paulo Andrade <pcpa@mandriva.com.br> 3.1.0-14mdv2010.1
+ Revision: 504285
- Update for build of sagemath 4.3.2

* Wed Feb 10 2010 Funda Wang <fwang@mandriva.org> 3.1.0-13mdv2010.1
+ Revision: 503620
- rebuild for new gmp

* Mon Jan 04 2010 Paulo Andrade <pcpa@mandriva.com.br> 3.1.0-12mdv2010.1
+ Revision: 486264
+ rebuild (emptylog)

* Wed Nov 18 2009 Paulo Andrade <pcpa@mandriva.com.br> 3.1.0-10mdv2010.1
+ Revision: 467282
+ rebuild (emptylog)

* Tue Nov 17 2009 Paulo Andrade <pcpa@mandriva.com.br> 3.1.0-9mdv2010.1
+ Revision: 467051
- Add documentation files and correct sage 4.2 crash

* Tue Nov 17 2009 Paulo Andrade <pcpa@mandriva.com.br> 3.1.0-8mdv2010.1
+ Revision: 466703
- Update for sage 4.2 build.

* Thu Sep 10 2009 Paulo Andrade <pcpa@mandriva.com.br> 3.1.0-7mdv2010.0
+ Revision: 436224
- disable build of alternate libntl

* Fri Sep 04 2009 Paulo Andrade <pcpa@mandriva.com.br> 3.1.0-6mdv2010.0
+ Revision: 431798
- Add minor patch to match sagemath doctest expected results
- add a lowercase symlink to /usr/bin/Singular

* Mon Aug 31 2009 Paulo Andrade <pcpa@mandriva.com.br> 3.1.0-5mdv2010.0
+ Revision: 423079
- Install .a libraries in the singular archdir, to avoid conflicts with ntl.

* Fri Aug 14 2009 Paulo Andrade <pcpa@mandriva.com.br> 3.1.0-4mdv2010.0
+ Revision: 416241
+ rebuild (emptylog)

* Thu Aug 13 2009 Paulo Andrade <pcpa@mandriva.com.br> 3.1.0-3mdv2010.0
+ Revision: 416218
- Correct Singular shell script to actually pass command line arguments
- Install surfex.jar and patch surfex to find it

* Wed Jul 15 2009 Paulo Andrade <pcpa@mandriva.com.br> 3.1.0-2mdv2010.0
+ Revision: 396452
+ rebuild (emptylog)

* Wed Jul 15 2009 Paulo Andrade <pcpa@mandriva.com.br> 3.1.0-1mdv2010.0
+ Revision: 396445
- Update to latest upstream release version 3.1.0, patchlevel 4.

* Fri May 29 2009 Paulo Andrade <pcpa@mandriva.com.br> 3.0.4-7mdv2010.0
+ Revision: 381167
- Correct memory corruptions problems in sagemath, that had it's root
  cause in the singular package.

* Mon May 18 2009 Paulo Andrade <pcpa@mandriva.com.br> 3.0.4-6mdv2010.0
+ Revision: 377388
+ rebuild (emptylog)

* Fri May 08 2009 Paulo Andrade <pcpa@mandriva.com.br> 3.0.4-5mdv2010.0
+ Revision: 373545
+ rebuild (emptylog)

* Thu Apr 23 2009 Paulo Andrade <pcpa@mandriva.com.br> 3.0.4-4mdv2009.1
+ Revision: 368954
- Install .lib files, as the Singular binary wants to read them.

* Thu Apr 16 2009 Paulo Andrade <pcpa@mandriva.com.br> 3.0.4-3mdv2009.1
+ Revision: 367788
- Correct include path to work from %%{_includedir}, and "manually" install
  headers that are required by the ones that are installed by %%makeinstall_std.

* Tue Apr 07 2009 Paulo Andrade <pcpa@mandriva.com.br> 3.0.4-2mdv2009.1
+ Revision: 365063
- o Compile C and C++ source with -fPIC to avoid x86_64 link problems.
  o Explicitly disable detection of libboost, as it generates link errors.
- o Renames singular-devel to libsingular-devel and add libsingular-static-devel.
  o Add missing files due to not executing 'make install-libsingular' target.

* Tue Mar 03 2009 Paulo Andrade <pcpa@mandriva.com.br> 3.0.4-1mdv2009.1
+ Revision: 348176
- Module MP wants sizeof(long) == 4. Disable build on x86_64.
- Initial import of singular, version 3.0.4.
  Singular is a Computer Algebra System for polynomial computations.
- singular


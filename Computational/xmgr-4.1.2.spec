Name: xmgr
Version: 4.1.2
Release: 12%{?dist}.2
License: distributable
Source0: ftp://plasma-gate.weizmann.ac.il/pub/xmgr4/src/xmgr-4.1.2.tar.gz
Patch0: xmgr-4.1.2.patch00
Patch1: xmgr-4.1.2.patch01
Patch2: xmgr-4.1.2.patch02
Patch3: xmgr-4.1.2.patch03
Patch4: xmgr-4.1.2.fixes.patch
BuildRoot: /tmp/xmgr-root
Packager: Henrik Seidel <seidel@mpimg-berlin-dahlem.mpg.de>
Group: Applications/Math
Summary: Numerical Data Processing and Visualization Tool (xmgr)
BuildRequires: lesstif-devel Xbae-devel byacc netcdf-devel gcc-gfortran

%description
Xmgr is a Motif application for two-dimensional data visualization.
Xmgr can transform the data using free equations, FFT, cross- and
auto-correlation, differences, integrals, histograms, and much more. The
generated figures are of high quality.  Xmgr is a very convenient tool
for data inspection, data transformation, and and for making figures for
publications.

%prep
%setup
%patch0 -p1
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p1 -b .fixes

%build
alias f77=gfortran
perl -pi -e "s|^CFLAGS=.*|CFLAGS=\"$RPM_OPT_FLAGS -Wall -pedantic -malign-double -D_ISOC99_SOURCE -D_XOPEN_SOURCE\"|" conf/ix86-linux
export CFLAGS="$RPM_OPT_FLAGS -Wall -pedantic -malign-double -D_ISOC99_SOURCE -D_XOPEN_SOURCE"
./configure --prefix=/usr --enable-acegr-home=%{_datadir}/xmgr
make
cd src
#mv xmgr xmgr.dynamic
#`make -n xmgr | grep '^gcc' | head -1 | \
# sed -e 's/\([ \t]\|^\)-lXm\b/\1-Wl,-Bstatic,-lXm,-Bdynamic/g' \
#     -e 's/\([ \t]\|^\)-lXbae\b/\1-Wl,-Bstatic,-lXbae,-Bdynamic/g'`
#mv xmgr xmgr.semistatic
cd ..

%install
if [ "x$RPM_BUILD_ROOT" != "x/" ]; then
    rm -rf $RPM_BUILD_ROOT
fi
mkdir -p $RPM_BUILD_ROOT%{_bindir}
make PREFIX=$RPM_BUILD_ROOT/usr \
     GR_HOME=$RPM_BUILD_ROOT%{_datadir}/xmgr \
     install
#ln -sf %{_datadir}/xmgr/bin/{xmgr,grconvert}
ln -sf %{_datadir}/xmgr/bin/xmgr \
     $RPM_BUILD_ROOT%{_bindir}
ln -sf %{_datadir}/xmgr/bin/xmgr \
     $RPM_BUILD_ROOT%{_bindir}/grbatch
#ln -sf %{_datadir}/xmgr/auxiliary/fdf2fit \
#     $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}
ln -sf %{_datadir}/xmgr/include/acegr_np.h \
    $RPM_BUILD_ROOT%{_includedir}/acegr_np.h
mkdir -p $RPM_BUILD_ROOT%{_libdir}
ln -sf %{_datadir}/xmgr/lib/libacegr_np.a \
    $RPM_BUILD_ROOT%{_libdir}/libacegr_np.a

%clean
if [ "x$RPM_BUILD_ROOT" != "x/" ]; then
    rm -rf $RPM_BUILD_ROOT
fi

%files 
%defattr(-,root,root)
%doc COPYRIGHT CHANGES
%doc %{_datadir}/xmgr/doc
%doc %{_datadir}/xmgr/examples
%dir %{_datadir}/xmgr
%{_datadir}/xmgr/bin
%{_datadir}/xmgr/auxiliary
%{_datadir}/xmgr/include
%{_datadir}/xmgr/lib
%{_bindir}/*
%{_libdir}/libacegr_np.a
%{_includedir}/acegr_np.h

%changelog
* Wed Feb 02 2011 Josko Plazonic <plazonic@math.princeton.edu>
- rebuild for puias6

* Fri Jan 05 2007 Josko Plazonic <plazonic@math.princeton.edu>
- drop dynamic/semistatic rpms, one rpm is good enough for me

* Thu Jun 18 1998 Henrik Seidel <seidel@mpimg-berlin-dahlem.mpg.de>

- fixed target of link /usr/X11R6/lib/X11/xmgr/bin/fdf2fit

* Wed Jun 10 1998 Henrik Seidel <seidel@mpimg-berlin-dahlem.mpg.de>

- changed the prefix to /usr/X11R6
- added wrappers to call xmgr.dynamic or xmgr.semistatic. Now there
  is no longer a need for postinstall/uninstall scripts. There was
  a problem with the links if packages were updated.

* Thu Jun  4 1998 Henrik Seidel <seidel@mpimg-berlin-dahlem.mpg.de>

- Applied patch for fixing the legend box problem (#326)

* Fri May 29 1998 Henrik Seidel <seidel@mpimg-berlin-dahlem.mpg.de>

- Fixed the bug causing segfaults if there are missing arguments to
  command line switches

* Fri May 22 1998 Henrik Seidel <seidel@mpimg-berlin-dahlem.mpg.de>

- Applied patch a patch for fixing the fft problem (#398)

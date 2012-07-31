Name:		surf
Version:	1.0.5
Summary:	Tool to visualize some real algebraic geometry
Release:	4%{?dist}
Source0:	http://downloads.sourceforge.net/project/surf/surf/surf-1.0.5/surf-1.0.5.tar.gz
URL:		http://surf.sourceforge.net/
License:	GPL
Group:		Sciences/Mathematics
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	flex automake14 autoconf texinfo bison
BuildRequires:	compat-gcc-34 compat-gcc-34-c++
BuildRequires:	gmp-devel gtk+-devel libjpeg-devel zlib-devel libtiff-devel
BuildRequires:	libXmu-devel

%description
surf is a tool to visualize some real algebraic geometry:
plane algebraic curves, algebraic surfaces and hyperplane sections of surfaces.
surf is script driven and has (optionally) a nifty GUI using the Gtk widget set.

%prep
%setup -q

%build
export LDFLAGS="-Wl,--build-id"
./configure						\
	--prefix=%{_prefix}				\
	--mandir=%{_mandir}				\
	--with-gmp=%{_prefix}				\
	--with-gtk=%{_prefix}				\
	--with-x
make CC=gcc34 CXX=g++34

%install
%makeinstall

%files
%defattr(-,root,root)
%{_bindir}/surf
%{_mandir}/man1/surf.1.*
%dir %{_datadir}/surf
%{_datadir}/surf/surf.xpm


%changelog
* Wed Dec 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.5-4mdv2011.0
+ Revision: 615041
- the mass rebuild of 2010.1 packages

* Wed Feb 10 2010 Funda Wang <fwang@mandriva.org> 1.0.5-3mdv2010.1
+ Revision: 503628
- rebuild for new gmp

* Sun Aug 23 2009 Funda Wang <fwang@mandriva.org> 1.0.5-2mdv2010.0
+ Revision: 419818
- rebuild for new libjpeg v7

* Fri Aug 14 2009 Paulo Andrade <pcpa@mandriva.com.br> 1.0.5-1mdv2010.0
+ Revision: 416247
- Import surf version 1.0.5.
  The surf program is the default singular plotting interface to sagemath.
- surf


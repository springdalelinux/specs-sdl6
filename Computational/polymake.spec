# $Project: polymake $$Id: polymake.spec 10526 2011-12-26 15:26:05Z gawrilow $

Summary: Algorithms around polytopes and polyhedra
Name: polymake
Version: 2.11
Release: 2
License: GPL
Group: Applications/Sciences/Mathematics
URL: http://www.polymake.org/
Vendor: TU Darmstadt, Algorithmic Discrete Mathematics
Packager: Ewgenij Gawrilow
Icon: as3.gif

%define topname %{name}-%{version}

%define build_perl_version %(eval "perl_`/usr/bin/perl -V:version`"; echo $perl_version)

Source: http://www.polymake.org/lib/exe/fetch.php/download/%{topname}.tar.bz2
# provides
Provides: perl(BackgroundViewer)
Provides: perl(Geomview)
Provides: perl(InteractiveViewer)
Provides: perl(JReality)
Provides: perl(JavaView)
Provides: perl(MetapostGraph)
Provides: perl(Polymake::Background)
Provides: perl(Polymake::Core::InteractiveCommands)
Provides: perl(Polymake::Core::RuleFilter)
Provides: perl(Polymake::Namespaces)
Provides: perl(Polymake::Sockets)
Provides: perl(Polymake::regex.pl)
Provides: perl(Polymake::utils.pl)
Provides: perl(SplitsTree)

Requires: gcc-c++
Requires: gmp gmp-devel 
Requires: mpfr31
Requires: java 
Requires: perl 
Requires: perl(XML::LibXML) perl(XML::SAX::Base) perl(XML::Writer) perl(XML::LibXSLT)
Requires: perl(Term::ReadLine::Gnu)
BuildRequires: gcc-c++
BuildRequires: gmp gmp-devel 
BuildRequires: mpfr31-devel 
BuildRequires: boost-devel
BuildRequires: libxml2-devel
BuildRequires: java-devel 
BuildRequires: ant
BuildRequires: perl
BuildRequires: perl(XML::LibXML) perl(XML::SAX::Base) perl(XML::Writer) perl(ExtUtils::MakeMaker)
BuildRequires: perl(XML::LibXSLT)
BuildRequires: perl(Term::ReadLine::Gnu)

Prefix: /usr

%description
Polymake is a versatile tool for the algorithmic treatment of
polytopes and polyhedra.  It offers an unified interface to a wide
variety of algorithms and free software packages from the computational
geometry field, such as convex hull computation or visualization tools.

%files
%attr(-, bin, bin) /usr/bin/polymake
%attr(-, bin, bin) /usr/bin/polymake-config
%attr(-, bin, bin) /usr/include/polymake
%attr(-, bin, bin) /usr/share/polymake
%attr(-, bin, bin) %dir /usr/%{_lib}/polymake
%attr(-, bin, bin) /usr/%{_lib}/polymake/lib
%attr(-, bin, bin) /usr/%{_lib}/polymake/perlx
%attr(-, bin, bin) /usr/%{_lib}/libpolymake.so
%attr(-, bin, bin) %config /usr/%{_lib}/polymake/conf.make
%attr(-, bin, bin) %doc /usr/share/doc/packages/polymake

%define guess_prefix : ${RPM_INSTALL_PREFIX:=%{_prefix}} ${RPM_INSTALL_PREFIX:=$RPM_INSTALL_PREFIX0} ${RPM_INSTALL_PREFIX:=/usr}

%post
%{guess_prefix}

if [ "$RPM_INSTALL_PREFIX" != /usr ]; then
   /usr/bin/perl -i -p -e 's|(PREFIX=).*|$1'$RPM_INSTALL_PREFIX'|' $RPM_INSTALL_PREFIX/%{_lib}/polymake/conf.make
fi

%prep
%setup -q -n %{topname}

%define ProjectTop %{_builddir}/%{topname}

%build

Cflags="$(perl -e '$_=q{'"$RPM_OPT_FLAGS"'}; s/(?:^|\s)-(?:g|O\d)(?=\s|$)//g; print;')"

if [ "%{_host_cpu}" = x86_64 -a "%{_target_cpu}" != x86_64 ]; then
  LDflags="LDFLAGS=-m32"
fi

./configure --prefix=/usr --libdir=/usr/%{_lib} --libexecdir=/usr/%{_lib}/polymake --docdir=/usr/share/doc/packages/%{name} \
            --build=%{_target_cpu} --without-prereq \
	    CC=gcc CXX=g++ CFLAGS="$Cflags" CXXFLAGS="$Cflags" $LDflags

make Arch=%{_target_cpu} %{?_smp_mflags}%{?!_smp_mflags:%(NCPUS=`grep -c '^processor' /proc/cpuinfo`; [ -n "$NCPUS" -a "$NCPUS" -gt 1 ] && echo -j$NCPUS )} ProcessDep=n


%install
make Arch=%{_target_cpu} PREFIX=/usr ${RPM_BUILD_ROOT:+DESTDIR=$RPM_BUILD_ROOT} install release-docs

%define __find_provides %{ProjectTop}/support/find-provides
%define __find_requires %{ProjectTop}/support/find-requires


%changelog
* Wed Mar 7 2012 Thomas Uphill <uphill@ias.edu>
- change for mpfr31 instead of mpfr-new (abandoned)
* Fri Mar 2 2012 Thomas Uphill <uphill@ias.edu>
- initial build for puias6

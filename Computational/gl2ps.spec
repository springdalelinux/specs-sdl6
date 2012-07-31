Summary:	An OpenGL to PostScript printing library
Summary(pl):	Biblioteka drukowania z OpenGL-a do PostScriptu
Name:		gl2ps
Version:	1.3.5
Release:	1%{?dist}
License:	LGPLv2+ or GL2PS
Group:		System Environment/Libraries
Source0:	http://www.geuz.org/gl2ps/src/%{name}-%{version}.tgz
Patch0:         %{name}-soversion.patch
URL:		http://www.geuz.org/gl2ps/
BuildRequires:  cmake
BuildRequires:	libGL-devel
BuildRequires:  libpng-devel
BuildRequires:  zlib-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -u -n)

%description
GL2PS is a C library providing high quality vector output for any
OpenGL application. The main difference between GL2PS and other
similar libraries is the use of sorting algorithms capable of handling
intersecting and stretched polygons, as well as non manifold objects.
GL2PS provides advanced smooth shading and text rendering, culling of
invisible primitives, mixed vector/bitmap output, and much more...

GL2PS can currently create PostScript (PS), Encapsulated PostScript
(EPS) and Portable Document Format (PDF) files, as well as LaTeX files
for the text fragments. Adding new vector output formats should be
relatively easy (and amongst the formats we would be interested in
adding, SVG is first in line). Meanwhile, you can use the excellent
pstoedit program to transform the PostScript files generated by GL2PS
into many other vector formats such as xfig, cgm, wmf, etc.

%description -l pl
GL2PS to biblioteka C zapewniająca wysokiej jakości wyjście wektorowe
dla dowolnej aplikacji OpenGL. Główna różnica między GL2PS a innymi
podobnymi bibliotekami polega na użyciu algorytmów sortujących
potrafiących obsłużyć przecinające się i rozciągnięte wielokąty, a
także obiekty nie będące rozmaitościami. GL2PS zapewnia zaawansowane
gładkie cieniowanie i renderowanie tekstu, usuwanie niewidocznych
prymitywów, mieszane wyjście wektorowo-bitmapowe i wiele więcej.

GL2PS aktualnie potrafi tworzyć pliki PostScript (PS), Encapsulated
PostScript (EPS) oraz Portable Document Format (PDF), a także pliki
LaTeXa dla fragmentów tekstowych. Dodanie nowych wyjściowych formatów
wektorowych powinno być względnie łatwe (a spośród formatów, których
dodanie zainteresowani byliby autorzy, pierwszym jest SVG). Tymczasem
można używać świetnego programu pstoedit do przekształcania plików
PostScript generowanych przez GL2PS na wiele innych formatów
wektorowych, takich jak xfig, cgm, wmf itp.

%package devel
Summary:	Header files for GL2PS library
Summary(pl):	Pliki nagłówkowe biblioteki GL2PS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libGL-devel

%description devel
Header files for GL2PS library.

%description devel -l pl
Pliki nagłówkowe biblioteki GL2PS.

%prep
%setup -q -n %{name}-%{version}-source
%patch0 -p1 -b .soversion

%build
%{cmake} .
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

if [ "x%{_lib}" != "xlib" ]; then
    mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}
fi

rm -r %{buildroot}%{_docdir}/gl2ps
rm %{buildroot}%{_libdir}/libgl2ps.a

%clean
rm -rf %{buildroot}

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING.GL2PS COPYING.LGPL README.txt
%attr(755,root,root) %{_libdir}/libgl2ps.so.*

%files devel
%defattr(644,root,root,755)
%doc gl2ps.pdf TODO.txt gl2psTest*.c
%{_libdir}/libgl2ps.so
%{_includedir}/gl2ps.h

%changelog
* Wed Jun 30 2010 Dominik Mierzejewski <rpm@greysector.net> 1.3.5-1
- updated to 1.3.5
- dropped upstreamed patches
- fixed install in libdir
- fixed missing SO version

* Sun Aug 23 2009 Dominik Mierzejewski <rpm@greysector.net> 1.3.3-1
- updated to 1.3.3
- removed calls to exit(3)
- added a simple build system (Makefile)
- dropped libtool dependency
- 1.3.3 added a new symbol, so made it versioned
- added examples to -devel docs

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jun 13 2008 Dominik Mierzejewski <rpm@greysector.net> 1.3.2-1
- adapted PLD spec r1.2
- dropped static package
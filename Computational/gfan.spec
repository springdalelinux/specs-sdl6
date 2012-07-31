Name:           gfan
Version:        0.3
Release:        8%{?dist}
Summary:        Software for Computing Gröbner Fans and Tropical Varieties
Group:          Applications/Engineering
License:        GPL+
URL:            http://www.math.tu-berlin.de/%7Ejensen/software/gfan/gfan.html
Source0:        http://www.math.tu-berlin.de/%7Ejensen/software/gfan/gfan%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Respect DESTDIR
Patch0:         gfan-0.3-respect-destdir.diff

BuildRequires:  cddlib-static cddlib-devel
BuildRequires:  gmp-devel
BuildRequires:  /usr/bin/pdflatex


%description
The software computes all marked reduced Gröbner bases of an ideal.
Their union is a universal Gröbner basis. Gfan contains algorithms for
computing this complex for general ideals and specialized algorithms
for tropical curves, tropical hypersurfaces and tropical varieties of
prime ideals. In addition to the above core functions the package
contains many tools which are useful in the study of Gröbner bases,
initial ideals and tropical geometry. Among these are an interactive
traversal program for Gröbner fans and programs for graphical renderings.



%prep
%setup -q -n %{name}%{version}
# manual is non-free
rm doc/ -rf

# Use native fedora optflags, prefix, and bindir
sed -i -e 's|^OPTFLAGS.*$||' \
  -e 's|^PREFIX.*$|PREFIX = %{_prefix}|' \
  -e 's|^BINDIR.*$|BINDIR = %{_bindir}|' Makefile

# respect DESTDIR
%patch0


%build
export OPTFLAGS="%{optflags} -DGMPRATIONAL -I/usr/include/cddlib"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/%{name}
mv $RPM_BUILD_ROOT%{_bindir}/gfan_* $RPM_BUILD_ROOT%{_libexecdir}/%{name}/
pushd $RPM_BUILD_ROOT%{_libexecdir}/%{name}/
  for symlink in gfan_*; do
    rm $symlink
#   ln -s %{_bindir}/%{name} $symlink
    ln -s ../../bin/%{name} $symlink
  done
popd


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING examples LICENSE
%{_bindir}/%{name}
%{_libexecdir}/%{name}


%changelog
* Thu Mar 18 2010 Mark Chappell <tremble@fedoraproject.org> - 0.3-8
- BuildRequire /usr/bin/pdflatex rather than texlive-latex

* Tue Dec  8 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 0.3-7
- Explicitly BR cddlib-static in accordance with the Packaging
  Guidelines (cddlib-devel is still static-only).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Conrad Meyer <konrad@tylerc.org> - 0.3-5
- Include the right place for headers (fix FTBFS).

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 30 2008 Conrad Meyer <konrad@tylerc.org> - 0.3-3
- Fix License tag.
- Fix build section.
- Remove doc/ in prep stage as it is non-free.

* Fri Dec 12 2008 Conrad Meyer <konrad@tylerc.org> - 0.3-2
- BR texlive-latex.

* Sat Dec 6 2008 Conrad Meyer <konrad@tylerc.org> - 0.3-1
- Initial package.

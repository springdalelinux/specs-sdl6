%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%global upstream_name Sphinx

Name:       python-sphinx10
Version:    1.0.4
Release:    4%{?dist}
Summary:    Python documentation generator

Group:      Development/Tools

# Unless otherwise noted, the license for code is BSD
# sphinx/util/stemmer.py Public Domain
# sphinx/pycode/pgen2 Python
# jquery (MIT or GPLv2)
License:    BSD and Public Domain and Python and (MIT or GPLv2)
URL:        http://sphinx.pocoo.org/
Source0:    http://pypi.python.org/packages/source/S/%{upstream_name}/%{upstream_name}-%{version}.tar.gz
Source1:    README.Fedora
Patch0:     Sphinx-1.0.4-localedirs.patch

BuildArch:     noarch
%if 0%{?rhel}
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%endif

BuildRequires: python2-devel >= 2.4
BuildRequires: python-setuptools
BuildRequires: python-docutils
BuildRequires: python-jinja2
# easy_install checks for runtime dependencies at install time
BuildRequires: python-pygments
BuildRequires: python-nose
Requires:      python-docutils
Requires:      python-jinja2
Requires:      python-pygments

# Require setuptools as the consumer will need pkg_resources to use this module
Requires: python-setuptools


%description
Sphinx is a tool that makes it easy to create intelligent and
beautiful documentation for Python projects (or other documents
consisting of multiple reStructuredText sources), written by Georg
Brandl. It was originally created to translate the new Python
documentation, but has now been cleaned up in the hope that it will be
useful to many other projects.

Sphinx uses reStructuredText as its markup language, and many of its
strengths come from the power and straightforwardness of
reStructuredText and its parsing and translating suite, the Docutils.

Although it is still under constant development, the following
features are already present, work fine and can be seen "in action" in
the Python docs:

    * Output formats: HTML (including Windows HTML Help) and LaTeX,
      for printable PDF versions
    * Extensive cross-references: semantic markup and automatic links
      for functions, classes, glossary terms and similar pieces of
      information
    * Hierarchical structure: easy definition of a document tree, with
      automatic links to siblings, parents and children
    * Automatic indices: general index as well as a module index
    * Code handling: automatic highlighting using the Pygments highlighter
    * Various extensions are available, e.g. for automatic testing of
      snippets and inclusion of appropriately formatted docstrings.


%package doc
Summary:    Documentation for %{name}
Group:      Documentation
License:    BSD
Requires:   %{name} = %{version}-%{release}


%description doc
Sphinx is a tool that makes it easy to create intelligent and
beautiful documentation for Python projects (or other documents
consisting of multiple reStructuredText sources), written by Georg
Brandl. It was originally created to translate the new Python
documentation, but has now been cleaned up in the hope that it will be
useful to many other projects.

This package contains documentation in reST and HTML formats.


%prep
%setup -q -n %{upstream_name}-%{version}%{?prerel}
%patch0 -p1 -b .localedirs
cp -p %{SOURCE1} .
sed '1d' -i sphinx/pycode/pgen2/token.py

%build
%{__python} setup.py bdist_egg
pushd doc
make html
%if ! 0%{?rhel}
make man
%endif
rm -rf _build/html/.buildinfo
mv _build/html ..
popd


%install
rm -rf %{buildroot}

%if 0%{?rhel}
# older versions of easy_install can't recreate path
mkdir -p %{buildroot}%{python_sitelib}
%endif

easy_install -m --prefix %{buildroot}%{_usr} dist/*.egg

# permission fix
find %{buildroot}%{python_sitelib}/Sphinx-%{version}-py*.egg -type f \
     -exec chmod a-x {} \;

# rename binaries for parallel-installability
pushd %{buildroot}%{_bindir}
for b in sphinx-*; do
  mv $b `echo $b | sed -e "s|^sphinx-|sphinx-1.0-|g"`
done
popd

%if ! 0%{?rhel}
pushd doc/_build/man
# Deliver man pages
install -d %{buildroot}%{_mandir}/man1
for manpage in sphinx-*.1; do
  mv $manpage %{buildroot}%{_mandir}/man1/`echo $manpage | sed -e "s|^sphinx-|sphinx-1.0-|g"`
done
popd
%endif

# Deliver rst files
rm -rf doc/_build
sed -i 's|python ../sphinx-build.py|/usr/bin/sphinx-1.0-build|' doc/Makefile
mv doc reST

# Move language files to /usr/share;
# patch to support this incorporated in 0.6.6
pushd %{buildroot}%{python_sitelib}/Sphinx-%{version}-py*.egg

for lang in `find sphinx/locale -maxdepth 1 -mindepth 1 -type d -printf "%f "`;
do
  install -d %{buildroot}%{_datadir}/sphinx-1.0/locale/$lang
  install -d %{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES
  mv sphinx/locale/$lang/LC_MESSAGES/sphinx.js \
     %{buildroot}%{_datadir}/sphinx-1.0/locale/$lang/
  mv sphinx/locale/$lang/LC_MESSAGES/sphinx.mo \
    %{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES/sphinx-1.0.mo
  rm -rf sphinx/locale/$lang
done
popd
%find_lang sphinx-1.0

# Language files; Since these are javascript, it's not immediately obvious to
# find_lang that they need to be marked with a language.
(cd %{buildroot} && find . -name 'sphinx.js') | sed -e 's|^.||' | sed -e \
  's:\(.*/locale/\)\([^/_]\+\)\(.*\.js$\):%lang(\2) \1\2\3:' \
  >> sphinx-1.0.lang


%if 0%{?rhel}
%clean
rm -rf %{buildroot}
%endif


%check
make test


%files -f sphinx-1.0.lang
%defattr(-,root,root,-)
%doc AUTHORS CHANGES EXAMPLES LICENSE README README.Fedora TODO
%{_bindir}/sphinx-*
%{python_sitelib}/*
%dir %{_datadir}/sphinx-1.0/
%dir %{_datadir}/sphinx-1.0/locale
%dir %{_datadir}/sphinx-1.0/locale/*
%if ! 0%{?rhel}
%{_mandir}/man1/*
%endif

%files doc
%defattr(-,root,root,-)
%doc html reST


%changelog
* Sun Mar 13 2011 Michel Salim <salimma@fedoraproject.org> - 1.0.4-4
- Build fix for EL-6: Use el5 build settings

* Tue Nov  2 2010 Michel Salim <salimma@fedoraproject.org> - 1.0.4-3
- EL-5: not generating manpages
- EL-5: re-add %%{buildroot} and %%clean
- EL-5: accomodate the older easy_install's peculiarities

* Tue Nov  2 2010 Michel Salim <salimma@fedoraproject.org> - 1.0.4-2
- Move locale files to system directories

* Mon Nov  1 2010 Michel Salim <salimma@fedoraproject.org> - 1.0.4-1
- Initial package, based on python-sphinx-1.0.4-2

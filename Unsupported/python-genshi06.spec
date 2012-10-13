Name:           python-genshi06
Version:        0.6
Release:        1%{?dist}
Summary:        Toolkit for stream-based generation of output for the web

Group:          Development/Languages
License:        BSD
URL:            http://genshi.edgewall.org/

Source0:        http://ftp.edgewall.com/pub/genshi/Genshi-%{version}.tar.gz

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel
BuildRequires:  python-setuptools-devel

Requires:       python-babel >= 0.8
Requires: python-setuptools

%description
Genshi is a Python library that provides an integrated set of
components for parsing, generating, and processing HTML, XML or other
textual content for output generation on the web. The major feature is
a template language, which is heavily inspired by Kid.

This version is a compat version for EPEL6 only. 

%prep
%setup0 -q -n Genshi-%{version}

find examples -type f | xargs chmod a-x

%build
%{__python} setup.py bdist_egg

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{python_sitelib}
easy_install -m --prefix %{buildroot}%{_usr} dist/*.egg

%check
%{__python} setup.py test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING doc examples README.txt 
%{python_sitelib}/Genshi-0.6-py2.6.egg

%changelog
* Sun Aug 22 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.6-1
- Version 0.6
- http://svn.edgewall.org/repos/genshi/tags/0.6.0/
- (Apr 22 2010, from branches/stable/0.6.x)
-
-  * Support for Python 2.3 has been dropped.
-  * Rewrite of the XPath evaluation engine for better performance and improved
-    correctness. This is the result of integrating work done by Marcin Kurczych
-    during GSoC 2008.
-  * Updated the Python AST processing for template code evaluation to use the
-    `_ast` module instead of the deprecated `compiler` package, including an
-    adapter layer for Python 2.4. This, too, is the result of integrating work
-    done by  Marcin Kurczych during GSoC 2008.
-  * Added caching in the serialization stage for improved performance in some
-    cases.
-  * Various improvements to the HTML sanitization filter.
-  * Fix problem with I18n filter that would get confused by expressions in
-    attribute values when inside an `i18n:msg` block (ticket #250).
-  * Fix problem with the transformation filter dropping events after the
-    selection (ticket #290).
-  * `for` loops in template code blocks no longer establish their own locals
-    scope, meaning you can now access variables assigned in the loop outside
-    of the loop, just as you can in regular Python code (ticket #259).
-  * Import statements inside function definitions in template code blocks no
-    longer result in an UndefinedError when the imported name is accessed
-    (ticket #276).
-  * Fixed handling of relative URLs with fragment identifiers containing colons
-    in the `HTMLSanitizer` (ticket #274).
-  * Added an option to the `HTMLFiller` to also populate password fields.
-  * Match template processing no longer produces unwanted duplicate output in
-    some cases (ticket #254).
-  * Templates instantiated without a loader now get an implicit loader based on
-    their file path, or the current directory as a fallback (ticket #320).
-  * Added documentation for the `TemplateLoader`.
-  * Enhanced documentation for internationalization.

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.5.1-8
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Sep 11 2009 Luke Macken <lmacken@redhat.com> - 0.5.1-7
- Add a patch to work around some recent Python2.6.2 behavior

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 01 2009 Luke Macken <lmacken@redhat.com> - 0.5.1-5
- Add python-babel as a requirement

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.5.1-3
- Rebuild for Python 2.6

* Thu Oct  9 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.5.1-2
- Add patch from upstream that fixes problems when using Genshi in
- conjuction with Babel.

* Tue Oct  7 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.5.1-1
- Version 0.5.1
- http://svn.edgewall.org/repos/genshi/tags/0.5.1/
- (Jul 9 2008, from branches/stable/0.5.x)
- 
-  * Fix problem with nested match templates not being applied when buffering
-    on the outer `py:match` is disabled. Thanks to Erik Bray for reporting the
-    problem and providing a test case!
-  * Fix problem in `Translator` filter that would cause the translation of
-    text nodes to fail if the translation function returned an object that was
-    not directly a string, but rather something like an instance of the
-    `LazyProxy` class in Babel (ticket #145).
-  * Fix problem with match templates incorrectly being applied multiple times.
-  * Includes from templates loaded via an absolute path now include the correct
-    file in nested directories as long if no search path has been configured
-    (ticket #240).
-  * Unbuffered match templates could result in parts of the matched content
-    being included in the output if the match template didn't actually consume
-    it via one or more calls to the `select()` function (ticket #243).

* Mon Jun  9 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.5-1
- Update to released version of Genshi.

* Thu Apr 24 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.5-0.1.svn847
- Update to snapshot of 0.5

* Tue Aug 28 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.4.4-2
- BR python-setuptools-devel

* Mon Aug 27 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.4.4-1
- Update to 0.4.4

* Mon Jul  9 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.4.2-2
- BR python-setuptools so that egg-info files get installed.  Fixes #247430.

* Thu Jun 21 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.4.2-1
- Update to 0.4.2

* Sat Jun  9 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.4.1-1
- Update to 0.4.1

* Wed Apr 18 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.4.0-1
- Update to 0.4.0

* Thu Apr 12 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.3.6-1
- First version for Fedora Extras


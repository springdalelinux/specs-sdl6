%{!?ruby_sitelib:	%global ruby_sitelib	%(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")}

%global		gemdir		%(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global		gemname		gettext
%global		geminstdir	%{gemdir}/gems/%{gemname}-%{version}

%global		rubyabi		1.8
%if 0%{?fedora} >= 11
%global		do_test		1
%else
%global		do_test		0
%endif
%global		locale_ver		2.0.5
%global		repoid			67096

Name:		rubygem-%{gemname}
Version:	2.1.0
Release:	1%{?dist}.1
Summary:	RubyGem of Localization Library and Tools for Ruby
Group:		Development/Languages

License:	Ruby
URL:		http://www.yotabanana.com/hiki/ruby-gettext.html?ruby-gettext
#Source0:	http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
Source0:	http://rubyforge.org/frs/download.php/%{repoid}/%{gemname}-%{version}.gem
Patch0:		rubygem-gettext-2.1.0-ruby186-compat.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	ruby(abi) = %{rubyabi}
BuildRequires:	ruby(rubygems)
BuildRequires:	rubygem(rake)
%if %{do_test}
BuildRequires(check):	rubygem(locale) >= %{locale_ver}
BuildRequires(check):	gettext
%endif
Requires:	ruby(abi) = %{rubyabi}
Requires:	ruby(rubygems)
Requires:	rubygem(locale) >= %{locale_ver}
Requires:	irb
Provides:	rubygem(%{gemname}) = %{version}-%{release}

BuildArch:	noarch

%description
Ruby-GetText-Package is a GNU GetText-like program for Ruby. 
The catalog file(po-file) is same format with GNU GetText. 
So you can use GNU GetText tools for maintaining.

This package provides gem for Ruby-Gettext-Package.

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description	doc
This package contains documentation for %{name}.


%package -n	ruby-gettext-package
Summary:	Localization Library and Tools for Ruby
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
Requires:	ruby(locale) >= %{locale_ver}
Provides:	ruby(gettext-package) = %{version}-%{release}

%description -n	ruby-gettext-package
Ruby-GetText-Package is a Localization(L10n) Library and Tools 
which is modeled after GNU gettext package.

The library converts the messages to localized messages properly 
using client-side locale information. And the tools for developers 
support to create, use, and modify localized message files
(message catalogs) easily.

%prep 
%setup -q -T -c

gem install \
	--local \
	--install-dir .%{gemdir} \
	--force \
	--rdoc \
	-V \
	%{SOURCE0}

pushd .%{geminstdir}
%patch0 -p0
popd

#%%{__rm} -f .%{geminstdir}/Rakefile
%{__rm} -f .%{geminstdir}/%{gemname}.gemspec
%{__rm} -f .%{geminstdir}/replace.rb
%{__rm} -rf .%{geminstdir}/po/
%{__rm} -rf .%{gemdir}/bin/
%{__chmod} 0755 .%{geminstdir}/bin/*
%{__chmod} 0644 .%{gemdir}/cache/*.gem
find .%{geminstdir}/ -name \*.po | xargs %{__chmod} 0644

# Cleanups for rpmlint
find .%{geminstdir}/lib/ -name \*.rb | while read f
do
	%{__sed} -i -e '/^#!/d' $f
done

# fix timestamps
find . -type f -print0 | xargs -0 touch -r %{SOURCE0}

%build

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{gemdir}

%{__cp} -a .%{gemdir}/* %{buildroot}%{gemdir}/
find %{buildroot}%{gemdir} -name \*.rb.patch\* -delete

# Create symlinks
##
## Note that before switching to gem %%{ruby_sitelib}/%%{gemname}
## already existed as a directory, so this cannot be replaced
## by symlink (cpio fails)
## Similarly, all directories under %%{ruby_sitelib} cannot be
## replaced by symlink
#

create_symlink_rec(){

ORIGBASEDIR=$1
TARGETBASEDIR=$2

## First calculate relative path of ORIGBASEDIR 
## from TARGETBASEDIR
TMPDIR=$TARGETBASEDIR
BACKDIR=
DOWNDIR=
num=0
nnum=0
while true
do
	num=$((num+1))
	TMPDIR=$(echo $TMPDIR | %{__sed} -e 's|/[^/][^/]*$||')
	DOWNDIR=$(echo $ORIGBASEDIR | %{__sed} -e "s|^$TMPDIR||")
	if [ x$DOWNDIR != x$ORIGBASEDIR ]
	then
		nnum=0
		while [ $nnum -lt $num ]
		do
			BACKDIR="../$BACKDIR"
			nnum=$((nnum+1))
		done
		break
	fi
done

RELBASEDIR=$( echo $BACKDIR/$DOWNDIR | %{__sed} -e 's|//*|/|g' )

## Next actually create symlink
pushd %{buildroot}/$ORIGBASEDIR
find . -type f | while read f
do
	DIRNAME=$(dirname $f)
	BACK2DIR=$(echo $DIRNAME | %{__sed} -e 's|/[^/][^/]*|/..|g')
	%{__mkdir_p} %{buildroot}${TARGETBASEDIR}/$DIRNAME
	LNNAME=$(echo $BACK2DIR/$RELBASEDIR/$f | \
		%{__sed} -e 's|^\./||' | %{__sed} -e 's|//|/|g' | \
		%{__sed} -e 's|/\./|/|' )
	%{__ln_s} -f $LNNAME %{buildroot}${TARGETBASEDIR}/$f
done
popd

}

create_symlink_rec %{geminstdir}/lib %{ruby_sitelib}
create_symlink_rec %{geminstdir}/bin %{_bindir}
create_symlink_rec %{geminstdir}/data/locale %{_datadir}/locale

# For --short-circult
%{__rm} -f *.lang

%find_lang rgettext
%{__cat} *.lang >> %{name}.lang

# modify find-lang.sh to deal with gettext .mo files under
# %%{geminstdir}/data/locale
%{__sed} -e 's|/share/locale/|/data/locale/|' \
	/usr/lib/rpm/find-lang.sh \
	> find-lang-modified.sh

sh find-lang-modified.sh %{buildroot} rgettext rgettext-gem.lang
%{__cat} *-gem.lang >> %{name}-gem.lang

# list directories under %%{geminstdir}/data/
find %{buildroot}%{geminstdir}/data -type d | while read dir
do
	echo "%%dir ${dir#%{buildroot}}" >> %{name}-gem.lang
done

%if %{do_test}
%check
pushd .%{geminstdir}
rake test
%endif

%clean
%{__rm} -rf %{buildroot}

%files	-f %{name}-gem.lang
%defattr(-,root,root,-)
%{_bindir}/rgettext
%{_bindir}/rmsgfmt
%{_bindir}/rmsgmerge

%dir %{geminstdir}/
%doc %{geminstdir}/[A-Z]*
%exclude %{geminstdir}/Rakefile
%{geminstdir}/bin/
%{geminstdir}/lib/
%{geminstdir}/src/

%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files		doc
%defattr(-,root,root,-)
%{gemdir}/doc/%{gemname}-%{version}/
%{geminstdir}/benchmark/
%{geminstdir}/samples/
%{geminstdir}/test.rb
%{geminstdir}/test/

%files -n	ruby-gettext-package	-f %{name}.lang
%defattr(-,root,root,-)
%{ruby_sitelib}/%{gemname}.rb
%{ruby_sitelib}/%{gemname}/


%changelog
* Tue Jan 12 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- gems.rubyforge.org gem file seems old, changing Source0 URL for now

* Wed Nov 18 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.0-1
- 2.1.0

* Sat Jul 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.4-2
- F-12: Mass rebuild

* Wed May 28 2009 Mamoru Tasaka <mtasaka@ios.s.u-tokyo.ac.jp> - 2.0.4-1
- 2.0.4

* Mon May 11 2009 Mamoru Tasaka <mtasaka@ios.s.u-tokyo.ac.jp> - 2.0.3-2
- 2.0.3
- Add "BR: gettext" (not to Requires) for rake test

* Fri May  1 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.1-3
- Mark LICENSE etc as %%doc

* Wed Apr 22 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.1-2
- Bump ruby-locale Requires version

* Tue Apr 21 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.1-1
- 2.0.1, drop patches already in upstream (all)

* Sat Mar 29 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.0-1
- Update to 2.0.0
- Now require rubygem(locale)
- Rescue NoMethodError on gem call on gettext.rb
- Reintroduce 4 args bindtextdomain() compatibility

* Tue Feb 24 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.93.0-8
- %%global-ize "nested" macro 

* Thu Oct 23 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.93.0-7
- Handle gettext .mo files under %%{geminstdir}/data/locale by
  modifying find-lang.sh

* Tue Oct  7 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.93.0-6
- Move sed edit section for lib/ files from %%install to %%build
  stage for cached gem file

* Tue Oct  7 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.93.0-5
- Recreate gettext .mo files (by using this itself)

* Mon Oct  6 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.93.0-3
- Some modification for spec file by Scott

* Tue Sep 23 2008 Scott Seago <sseago@redhat.com> - 1.93.0-2
- Initial package (of rubygem-gettext)
  Set at release 2 to supercede ruby-gettext-package-1.93.0-1

* Thu Sep 18 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.93.0-1
- 1.93.0

* Sat Aug  9 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.92.0-1
- 1.92.0

* Thu May 22 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.91.0-1
- 1.91.0

* Sun Feb  3 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.90.0-1
- 1.90.0
- Arch changed to noarch

* Wed Aug 29 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.10.0-1
- 1.10.0

* Wed Aug 22 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.9.0-2.dist.2
- Mass rebuild (buildID or binutils issue)

* Fri Aug  3 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.9.0-2.dist.1
- License update

* Mon May  7 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.9.0-2
- Create -doc subpackage

* Sat Apr 21 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.9.0-1
- Initial packaging

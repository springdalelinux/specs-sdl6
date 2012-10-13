# Initially generated from hpricot-0.6.164.gem by gem2rpm -*- rpm-spec -*-
%define	ruby_sitelib		%(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%define	ruby_sitearch		%(ruby -rrbconfig -e "puts Config::CONFIG['sitearchdir']")
%define	rubyabi		1.8

%define	gemdir			%(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define	gemname		hpricot
%define	geminstdir		%{gemdir}/gems/%{gemname}-%{version}

Summary:	A Fast, Enjoyable HTML Parser for Ruby
Name:		rubygem-%{gemname}
Version:	0.8.3
Release:	1%{?dist}
Group:		Development/Languages
# ext/fast_xs/FastXsService.java is licensed under ASL 2.0
License:	MIT and ASL 2.0
URL:		http://github.com/hpricot/hpricot
# Non-free file removed, see Source10
# Source0:	http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
Source0:	%{gemname}-%{version}-modified.gem
Source10:	rubygem-hpricot-create-free-gem.sh

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	ruby(abi) = %{rubyabi}
BuildRequires:	ruby(rubygems)
BuildRequires:	rubygem(rake-compiler)
BuildRequires:	ruby-devel
BuildRequires:	ragel
Requires:	ruby(abi) = %{rubyabi}
Requires:	ruby(rubygems)
Provides:	rubygem(%{gemname}) = %{version}-%{release}

%description
Hpricot is a very flexible HTML parser, based on Tanaka Akira's 
HTree and John Resig's JQuery, but with the scanner recoded in C 
(using Ragel for scanning.)

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
# Directory ownership issue
Requires:	%{name} = %{version}-%{release}
Requires:	ruby(rubygems)

%description	doc
This package contains documentation for %{name}.

%package	-n ruby-%{gemname}
Summary:	Non-Gem support package for %{gemname}
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
Provides:	ruby(%{gemname}) = %{version}-%{release}

%description	-n ruby-%{gemname}
This package provides non-Gem support for %{gemname}.

%prep
%setup -q -T -c
mkdir -p ./%{gemdir}
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
gem install \
	--local \
	--install-dir ./%{gemdir} \
	-V --force \
	%{SOURCE0}

pushd .%{geminstdir}/test
# Kill tests related to BOINGBOING, licensed under CC-BY-NC
grep -rl BOING . | \
	xargs sed -i '/BOING/s|^\([ \t][ \t]*\)\(.*\)$|\1# This test is intentionally killed\n\1return true\n\1\2|'
popd

# ??
find . -type f | xargs chmod ugo+r

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
cp -a ./%{gemdir}/* %{buildroot}%{gemdir}

mkdir -p %{buildroot}%{ruby_sitearch}
mv %{buildroot}%{geminstdir}/lib/*.so %{buildroot}%{ruby_sitearch}

# Shebang
for f in $(find %{buildroot}%{geminstdir} -name \*.rb)
do
	sed -i -e '/^#!/d' $f
	chmod 0644 $f
done

# Kill unneeded files
find %{buildroot}%{geminstdir}/ext \
	-type f \
	-not -name \*.java \
	-print0 | \
	xargs -0 rm -f
rm -f %{buildroot}%{geminstdir}/.require_paths
DIR=%{buildroot}%{geminstdir}/lib/universal-java*
[ -d $DIR ] && rmdir $DIR

# The following method is completely copied from rubygem-gettext
# spec file
#
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
	TMPDIR=$(echo $TMPDIR | sed -e 's|/[^/][^/]*$||')
	DOWNDIR=$(echo $ORIGBASEDIR | sed -e "s|^$TMPDIR||")
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

RELBASEDIR=$( echo $BACKDIR/$DOWNDIR | sed -e 's|//*|/|g' )

## Next actually create symlink
pushd %{buildroot}/$ORIGBASEDIR
find . -type f | while read f
do
	DIRNAME=$(dirname $f)
	BACK2DIR=$(echo $DIRNAME | sed -e 's|/[^/][^/]*|/..|g')
	mkdir -p %{buildroot}${TARGETBASEDIR}/$DIRNAME
	LNNAME=$(echo $BACK2DIR/$RELBASEDIR/$f | \
		sed -e 's|^\./||' | sed -e 's|//|/|g' | \
		sed -e 's|/\./|/|' )
	ln -s -f $LNNAME %{buildroot}${TARGETBASEDIR}/$f
done
popd

}

create_symlink_rec %{geminstdir}/lib %{ruby_sitelib}

# Fix permission (bug 487654)
pushd %{buildroot}
find . -type f '(' -name '[A-Z]*' -or -name '*.java' -or -name '*.rb' -or -name '*gem*' ')' \
	-print0 | xargs -0 chmod 0644
popd

%check
export GEM_PATH=$(pwd)%{gemdir}
pushd .%{geminstdir}

rake test
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root, root,-)
%{ruby_sitearch}/*.so
%dir	%{geminstdir}/
%doc	%{geminstdir}/[A-Z]*
%exclude %{geminstdir}/Rakefile
%{geminstdir}/[a-l]*/
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files	doc
%defattr(-,root,root,-)
%{geminstdir}/Rakefile
%{geminstdir}/extras/
%{geminstdir}/test/
%{gemdir}/doc/%{gemname}-%{version}/

%files	-n ruby-%{gemname}
%defattr(-,root,root,-)
%{ruby_sitelib}/%{gemname}.rb
%{ruby_sitelib}/%{gemname}/

%changelog
* Sat Nov  6 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.8.3-1
- 0.8.3

* Mon Nov  9 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.8.2-1
- 0.8.2
- Kill BOINGBOING test properly

* Sat Jul 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.8.1-3
- F-12: Mass rebuild

* Sat Jun 27 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.8.1-2
- Readd Rakefile
- Enable check

* Wed Apr  8 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.8.1-1
- 0.8.1

* Thu Mar 26 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.7-1
- 0.7

* Sat Feb 28 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.6.164-5
- Fix permission (bug 487654)

* Tue Feb 24 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.6.164-4
- F-11: Mass rebuild

* Thu Jan 15 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.6.164-3
- Fix license tag, removing non-free file (thanks to
  Michael Stahnke)

* Fri Dec 26 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.6.164-2
- Kill unneeded files more

* Sun Dec 21 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.6.164-1
- Switch to Gem

* Sat Dec 20 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.6-3
- Fix build error related to Windows constant, detected
  by Matt's mass build
  (possibly due to rubygems 1.3.1 change)

* Wed Feb 13 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.6-2
- Rebuild against gcc43
- Patch for Rakefile to skip unneeded commands call for ragel 6.0+
  (bug 432186, Thanks Jeremy Hinegardner !!)

* Tue Nov  6 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.6-1
- 0.6

* Sat Nov  3 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.5.150-2
- Use rubygem(rake) for rebuild

* Fri Jun  8 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.5.150-1
- Initial packaging

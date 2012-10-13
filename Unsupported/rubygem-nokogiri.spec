%define	ruby_sitelib		%(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%define	ruby_sitearch		%(ruby -rrbconfig -e "puts Config::CONFIG['sitearchdir']")
%define	rubyabi		1.8

%define	gemdir			%(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define	gemname		nokogiri
%define	geminstdir		%{gemdir}/gems/%{gemname}-%{version}

# Note for packager:
# Nokogiri 1.4.3.1 gem says that Nokogiri upstream will
# no longer support ruby 1.8.6 after 2010-08-01, so
# it seems that 1.4.3.1 is the last version for F-13 and below.

Summary:	An HTML, XML, SAX, and Reader parser
Name:		rubygem-%{gemname}
Version:	1.4.3.1
Release:	1%{?dist}
Group:		Development/Languages
License:	MIT
URL:		http://nokogiri.rubyforge.org/nokogiri/
Source0:	http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
Patch0:		nokogiri-1.4.2-test-xml-element-number.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	ruby(abi) = %{rubyabi}
BuildRequires:	ruby(rubygems)
BuildRequires:	rubygem(hoe)
# Not available yet
# BuildRequires:	rubygem(hoe-debugging)
BuildRequires:	rubygem(rake)
BuildRequires:	rubygem(minitest)
BuildRequires:	rubygem(rake-compiler)
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	ruby-devel
Requires:	ruby(abi) = %{rubyabi}
Requires:	ruby(rubygems)
Provides:	rubygem(%{gemname}) = %{version}-%{release}

%description
Nokogiri parses and searches XML/HTML very quickly, and also has
correctly implemented CSS3 selector support as well as XPath support.

Nokogiri also features an Hpricot compatibility layer to help ease the change
to using correct CSS and XPath.

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

pushd .%{geminstdir}
%patch0 -p1 -b .orig_fail
popd

%build
# cflags wrong (-O3 passed), recompiling
pushd ./%{geminstdir}
sed -i.flags -e 's|-O3||' ext/nokogiri/extconf.rb
find . -name \*.so -or -name \*.o -exec rm -f {} \;
rake -v compile --trace

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
cp -a ./%{gemdir}/* %{buildroot}%{gemdir}

# Remove backup file
find %{buildroot} -name \*.orig_\* | xargs rm -vf

# move arch dependent files to %%ruby_sitearch
mkdir -p %{buildroot}%{ruby_sitearch}/%{gemname}
mv %{buildroot}%{geminstdir}/lib/%{gemname}/*.so \
	%{buildroot}%{ruby_sitearch}/%{gemname}/

# move bin/ files
mkdir -p %{buildroot}%{_prefix}
mv -f %{buildroot}%{gemdir}/bin %{buildroot}%{_prefix}

# remove all shebang
for f in $(find %{buildroot}%{geminstdir} -name \*.rb)
do
	sed -i -e '/^#!/d' $f
	chmod 0644 $f
done

# cleanups
rm -rf %{buildroot}%{geminstdir}/{ext,tmp}/
rm -f %{buildroot}%{geminstdir}/{.autotest,.require_paths}

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


%clean
rm -rf %{buildroot}

%check
# test_exslt(TestXsltTransforms) [./test/test_xslt_transforms.rb:93]
# fails without TZ on sparc
export TZ="Asia/Tokyo"

pushd ./%{geminstdir}
rake test --trace
popd

%files
%defattr(-,root, root,-)
%{_bindir}/%{gemname}
%{ruby_sitearch}/%{gemname}/
%dir	%{geminstdir}/
%doc	%{geminstdir}/[A-Z]*
%exclude %{geminstdir}/Rakefile
%{geminstdir}/[a-l]*/
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files	doc
%defattr(-,root,root,-)
%{geminstdir}/Rakefile
%{geminstdir}/tasks/
%{geminstdir}/test/
%{gemdir}/doc/%{gemname}-%{version}/

%files	-n ruby-%{gemname}
%defattr(-,root,root,-)
%{ruby_sitelib}/*%{gemname}.rb
%{ruby_sitelib}/%{gemname}/
%{ruby_sitelib}/xsd/

%changelog
* Fri Jul 30 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.4.3.1-1
- 1.4.3.1

* Wed May 26 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.4.2-1
- 1.4.2

* Thu Apr 29 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.4.1-2
- Fix build failure with libxml2 >= 2.7.7

* Tue Dec 15 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.4.1-1
- 1.4.1

* Mon Nov  9 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.4.0-1
- 1.4.0

* Sat Aug 22 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.3.3-2
- Fix test failure on sparc

* Wed Jul 29 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.3.3-1
- 1.3.3

* Sat Jul 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.3.2-3
- F-12: Mass rebuild

* Thu Jul  2 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.3.2-2
- Enable test
- Recompile with -O2

* Thu Jun 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.3.2-1
- 1.3.2

* Thu Jun 11 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.3.1-1
- 1.3.1

* Thu Mar 26 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.3-1
- 1.2.3

* Thu Mar 19 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.2-1
- 1.2.2

* Thu Mar 12 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.1-1
- 1.2.1

* Tue Feb 24 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.1.1-2
- F-11: Mass rebuild

* Thu Jan 15 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.1.1-1
- 1.1.1

* Thu Dec 25 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.1.0-1
- Initial packaging


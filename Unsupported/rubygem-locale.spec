# Generated from locale-2.0.0.gem by gem2rpm -*- rpm-spec -*-
%global	ruby_sitelib	%(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")

%global	gemdir		%(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global	gemname	locale
%global	geminstdir	%{gemdir}/gems/%{gemname}-%{version}

%global	rubyabi	1.8
%global	repoid		67114

Summary:	Pure ruby library which provides basic APIs for localization
Name:		rubygem-%{gemname}
Version:	2.0.5
Release:	1%{?dist}.1
Group:		Development/Languages
License:	GPLv2 or Ruby
URL:		http://locale.rubyforge.org/
#Source0:	http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
Source0:	http://rubyforge.org/frs/download.php/%{repoid}/%{gemname}-%{version}.gem

BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	ruby(abi) = %{rubyabi}
BuildRequires:	ruby
BuildRequires:	ruby(rubygems)
BuildRequires:	rubygem(rake)
Requires:	ruby
Requires:	ruby(abi) = %{rubyabi}
Requires:	ruby(rubygems)
Provides:	rubygem(%{gemname}) = %{version}-%{release}
Conflicts:	rubygem-gettext < 2.0.0

%description
Ruby-Locale is the pure ruby library which provides basic and general purpose
APIs for localization.
It aims to support all environments which ruby works and all kind of programs
(GUI, WWW, library, etc), and becomes the hub of other i18n/l10n libs/apps to 
handle major locale ID standards. 

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

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
%setup -q -c -T
gem install \
	--local \
	--install-dir .%{gemdir} \
	--force \
	--rdoc \
	-V \
	%{SOURCE0}

# rm -f .%{geminstdir}/Rakefile
find . -name \*gem | xargs chmod 0644

# fix timestamps
find . -type f -print0 | xargs -0 touch -r %{SOURCE0}

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{gemdir}
cp -a .%{gemdir}/* %{buildroot}%{gemdir}/

# The following method is completely copied from rubygem-gettext
# spec file
#
# Create symlinks

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

%check
pushd .%{geminstdir}
rake test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %{geminstdir}/
%doc %{geminstdir}/[A-Z]*
%exclude %{geminstdir}/Rakefile
%{geminstdir}/lib/
%{geminstdir}/*.rb

%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%defattr(-,root,root,-)
%{gemdir}/doc/%{gemname}-%{version}/
%{geminstdir}/samples/
%{geminstdir}/test/

%files -n ruby-%{gemname}
%defattr(-,root,root,-)
%{ruby_sitelib}/%{gemname}.rb
%{ruby_sitelib}/%{gemname}/


%changelog
* Tue Jan 12 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- gems.rubyforge.org gem file seems old, changing Source0 URL for now

* Wed Nov 18 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.5-1
- 2.0.5
- Fix the license tag

* Sat Jul 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.4-2
- F-12: Mass rebuild

* Wed May 27 2009  Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.4-1
- 2.0.4

* Mon May 11 2009  Mamoru Tasaka <mtasaka@ios.s.u-tokyo.ac.jp> - 2.0.3-1
- 2.0.3

* Tue Apr 21 2009  Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.1-1
- 2.0.1

* Thu Mar 26 2009  Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.0-1
- Initial package

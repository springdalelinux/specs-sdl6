
Name:         drush
License:      GPLv2+
Group:        Productivity/Networking/Web/Servers
Summary:      Drush is a command line shell and scripting interface for Drupal.
Version:      5.6
Release:      2.2
URL:          http://drupal.org/project/drush
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
BuildArch:    noarch
Source0:      drush-7.x-%{version}.tar.gz
Requires:     cvs ncurses php-cli wget
Requires:     php-pear(Console_Table)

%description
Drush is a command line shell and scripting interface for Drupal, a veritable
Swiss Army knife designed to make life easier for those of us who spend some of
our working hours hacking away at the command prompt.

See http://drush.ws, the homepage for the drush project.

%prep
%setup -q -n %name

%build

%install
%{__install} -d -m 0755 %{_builddir}/drush %{buildroot}%{_datadir}/drush
%{__cp} -r %{_builddir}/drush %{buildroot}%{_datadir}

%{__mkdir} -p %{buildroot}%{_bindir}
%{__ln_s} %{_datadir}/drush/drush %{buildroot}%{_bindir}/drush

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_datadir}/drush
%{_bindir}/drush

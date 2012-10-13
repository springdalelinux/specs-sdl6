%define major_version 1.1
%define minor_version 7

Name: idm-console-framework
Version: %{major_version}.%{minor_version}
Release: 2%{?dist}
Summary: Identity Management Console Framework

Group: System Environment/Libraries
License: LGPLv2
URL: http://port389.org

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Source: http://port389.org/sources/%{name}-%{version}.tar.bz2
Requires: ldapjdk
Requires: jss >= 4.2
# Urge use of OpenJDK for runtime
Requires: java >= 1:1.6.0
BuildRequires: java-devel >= 1:1.6.0
BuildRequires: ant >= 1.6.2
BuildRequires: ldapjdk
BuildRequires: jss >=  4.2 
%if 0%{?rhel} < 6
ExcludeArch: ppc
%endif

%description
A Java Management Console framework used for remote server management.

%prep
%setup -q

%build
%{ant} \
    -Dlib.dir=%{_libdir} \
    -Dbuilt.dir=`pwd`/built \
    -Dclassdest=%{_javadir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}
install -m644 built/release/jars/idm-console-* $RPM_BUILD_ROOT%{_javadir}

# create symlinks
pushd $RPM_BUILD_ROOT%{_javadir}
ln -s idm-console-base-%{version}.jar idm-console-base-%{major_version}.jar
ln -s idm-console-base-%{version}.jar idm-console-base.jar
ln -s idm-console-mcc-%{version}.jar idm-console-mcc-%{major_version}.jar
ln -s idm-console-mcc-%{version}.jar idm-console-mcc.jar
ln -s idm-console-mcc-%{version}_en.jar idm-console-mcc-%{major_version}_en.jar
ln -s idm-console-mcc-%{version}_en.jar idm-console-mcc_en.jar
ln -s idm-console-nmclf-%{version}.jar idm-console-nmclf-%{major_version}.jar
ln -s idm-console-nmclf-%{version}.jar idm-console-nmclf.jar
ln -s idm-console-nmclf-%{version}_en.jar idm-console-nmclf-%{major_version}_en.jar
ln -s idm-console-nmclf-%{version}_en.jar idm-console-nmclf_en.jar
popd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE
%{_javadir}/idm-console-base-%{version}.jar
%{_javadir}/idm-console-base-%{major_version}.jar
%{_javadir}/idm-console-base.jar
%{_javadir}/idm-console-mcc-%{version}.jar
%{_javadir}/idm-console-mcc-%{major_version}.jar
%{_javadir}/idm-console-mcc.jar
%{_javadir}/idm-console-mcc-%{version}_en.jar
%{_javadir}/idm-console-mcc-%{major_version}_en.jar
%{_javadir}/idm-console-mcc_en.jar
%{_javadir}/idm-console-nmclf-%{version}.jar
%{_javadir}/idm-console-nmclf-%{major_version}.jar
%{_javadir}/idm-console-nmclf.jar
%{_javadir}/idm-console-nmclf-%{version}_en.jar
%{_javadir}/idm-console-nmclf-%{major_version}_en.jar
%{_javadir}/idm-console-nmclf_en.jar

%changelog
* Tue Jun 21 2011 Rich Megginson <rmeggins@redhat.com> - 1.1.7-2
- using new upstream git repo at fedorahosted.org
- git tag idm-console-framework-1.1.7
- Use DefaultTopologyPlugin if topologyplugin not found in the DS
- Bug 706472 - [console] java exception throw in UI, but user gets created
- Bug 706258 - ACI Editor dialog flickers

* Tue Mar 29 2011 Rich Megginson <rmeggins@redhat.com> - 1.1.7-1
- The 1.1.7 release
- Bug 158926 - Unable to install CA certificate when using hardware token
-             ( LunaSA )
- Bug 622436 - Removal of Security:domestic from Console
- Bug 229699 - objectclass without parent causes StringIndexOutOfBounds in console
- Bug 583652 - Console caches magic numbers instead of DNA-generated values

* Wed Feb 23 2011 Rich Megginson <rmeggins@redhat.com> - 1.1.6-1
- The 1.1.6 release
- Bug: 594939 - ACI editing dialog initial size is not big enough to display
- Bug 151705 - Need to update Console Cipher Preferences with new ciphers
- fix fourth step of cert wizard for installing cert
- Bug 668950 - Add posixGroup support to Console
- Bug 583652 - Console caches magic numbers instead of DNA-generated values

* Tue May  4 2010 Rich Megginson <rmeggins@redhat.com> - 1.1.5-1
- The 1.1.5 release - added code to deal with LDAPv3 escape sequences

* Thu Apr 15 2010 Rich Megginson <rmeggins@redhat.com> - 1.1.4-1
- The 1.1.4 release - just a few bug fixes

* Fri Dec 18 2009 Rich Megginson <rmeggins@redhat.com> - 1.1.3-3
- Excluding PPC for EPEL builds as there is not openjdk there
- change url to port389.org

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 31 2009 Rich Megginson <rmeggins@redhat.com> 1.1.3-1
- this is the 1.1.3 release
- use the epoch with the java-devel version

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  2 2008 Rich Megginson <rmeggins@redhat.com> 1.1.2-1
- numerous fixes for threading issues and help for debugging and eclipse

* Tue Apr 15 2008 Rich Megginson <rmeggins@redhat.com> 1.1.1-3
- use java > 1.5.0 for the requirements
- install jar files with mode 644

* Wed Jan  9 2008 Rich Megginson <rmeggins@redhat.com> 1.1.1-1
- fix rpmlint issues
- changed license from LGPL to LGPLv2
- added explicit requires for java-1.7.0-icedtea
- added LICENSE for doc

* Wed Dec 19 2007 Rich Megginson <rmeggins@redhat.com> 1.1.0-2
- for the fedora ds 1.1 release

* Wed Aug  1 2007 Nathan Kinder <nkinder@redhat.com> 1.1.0-1
- Initial creation (based on old fedora-idm-console package).

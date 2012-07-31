# Copyright (c) 2000-2009, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define section         non-free

%define origin          sun
%define javaver         1.6.0
%define cvsver          6
%define buildver        33
%define tzversion       1_3_34-2010o
%define priority        1600%{buildver}
%define tzupdate        0

# TODO: Think about using conditionals for version variants.
%define cvsversion      %{cvsver}u%{buildver}

%define javaws_ver      %{javaver}
%define javaws_version  %{cvsversion}

%define toplevel_dir    jdk%{javaver}_%{buildver}

%ifarch %ix86
%define target_cpu      i586
%define archname        i386
%define multi_suffix    %{nil}
%endif
%ifarch x86_64
%define target_cpu      x64
%define archname        amd64
%define multi_suffix    .x86_64
%endif

%define sdklnk          java-%{javaver}-%{origin}%{multi_suffix}
%define jrelnk          jre-%{javaver}-%{origin}%{multi_suffix}
%define sdkdir          %{name}-%{version}%{multi_suffix}
%define jredir          %{sdkdir}/jre
%define sdkbindir       %{_jvmdir}/%{sdklnk}/bin
%define sdklibdir       %{_jvmdir}/%{sdklnk}/lib
%define jrebindir       %{_jvmdir}/%{jrelnk}/bin
%define jvmjardir       %{_jvmjardir}/%{name}-%{version}%{multi_suffix}
%define policydir       %{name}%{multi_suffix}
%define javaplugin      libjavaplugin.so%{multi_suffix}
%define pluginname      %{_jvmdir}/%{jrelnk}/lib/%{archname}/libnpjp2.so

# Avoid RPM 4.2+'s internal dep generator, it may produce bogus
# Provides/Requires here.
%define _use_internal_dependency_generator 0

# This prevents aggressive stripping.
%define debug_package %{nil}
%define __strip /bin/true

# Prevent brp-java-repack-jars from being run.
# This saves a lot of time and the resulting multilib issues
# don't matter because this isn't a multilib-capable package.
%define __jar_repack 0

Name:           java-%{javaver}-%{origin}
Version:        %{javaver}.%{buildver}
Release:        1.0%{?dist}.1
Epoch:          1
Summary:        Sun Java Runtime Environment
License:        Oracle Corporation Binary Code License
Group:          Development/Languages
URL:            http://java.sun.com/javase/6
Source0:        jdk-%{cvsversion}-linux-i586.bin
Source1:	jdk-%{cvsversion}-linux-x64.bin
Source2:	jdk-6u33-linux-i586-demos.tar.gz
Source3:	jdk-6u33-linux-x64-demos.tar.gz
Source100:      tzupdater-%{tzversion}.zip
Provides:       jre-%{javaver}-%{origin} = %{epoch}:%{version}-%{release}
Provides:       jre-%{origin} = %{epoch}:%{version}-%{release}
Provides:       jre-%{javaver}, java-%{javaver}, jre = %{epoch}:%{javaver}
Provides:       java-%{origin} = %{epoch}:%{version}-%{release}
Provides:       java = %{epoch}:%{javaver}
Requires:       jpackage-utils >= 0:1.5.38
Requires(post): chkconfig
BuildArch:      i586 x86_64
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:  jpackage-utils >= 0:1.5.38, sed, %{_bindir}/perl, symlinks
BuildRequires:  desktop-file-utils
Provides:       jndi = %{epoch}:%{version}, jndi-ldap = %{epoch}:%{version}
Provides:       jndi-cos = %{epoch}:%{version}, jndi-rmi = %{epoch}:%{version}
Provides:       jndi-dns = %{epoch}:%{version}
Provides:       jaas = %{epoch}:%{version}
Provides:       jsse = %{epoch}:%{version}
Provides:       jce = %{epoch}:%{version}
Provides:       jdbc-stdext = %{epoch}:3.0, jdbc-stdext = %{epoch}:%{version}
Provides:       java-sasl = %{epoch}:%{version}
Provides:       %{name}-alsa = %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-alsa < %{epoch}:%{version}-%{release}
Provides:       %{name}-fonts = %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-fonts < %{epoch}:%{version}-%{release}
Provides:       java-fonts = %{epoch}:%{javaver}, java-%{javaver}-fonts

%description
The Java Runtime Environment (JRE) contains the software and tools
that users need to run applets and applications written using the Java
programming language.

%package        devel
Summary:        Sun Java Development Kit
Group:          Development/Languages
Provides:       java-sdk-%{javaver}-%{origin} = %{epoch}:%{version}-%{release}
Provides:       java-sdk-%{origin} = %{epoch}:%{version}-%{release}
Provides:       java-sdk-%{javaver}, java-sdk = %{epoch}:%{javaver}
Provides:       java-devel-%{origin} = %{epoch}:%{version}-%{release}
Provides:       java-%{javaver}-devel, java-devel = %{epoch}:%{javaver}
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires(post): chkconfig
Requires(postun): chkconfig

%description    devel
The Java Development Kit (JDK) contains the software and tools that
developers need to compile and debug applets and applications written
using the Java programming language.

%package        src
Summary:        Source files for Sun JDK
Group:          Development/Languages
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    src
This package contains the source code for the Sun Java class
libraries.

%package        demo
Summary:        Demonstration files for Sun JDK
Group:          Development/Languages
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    demo
This package contains demonstration files for the Sun Java Development
Kit.

%package        plugin
Summary:        Sun Java browser plugin
Group:          User Interface/Desktops
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       %{_bindir}/find, sed
Requires:       %{_libdir}/mozilla/plugins
# chkconfig needed for the various alternatives utilities
Requires(pre):  chkconfig, %{_libdir}/mozilla/plugins
Requires(post): chkconfig, %{_libdir}/mozilla/plugins
Requires(postun): chkconfig
Provides:       java-plugin = %{epoch}:%{javaver}, java-%{javaver}-plugin = %{epoch}:%{version}
Provides:       javaws = %{epoch}:%{javaws_ver}
Obsoletes:      javaws-menu

%description    plugin
This package contains the Sun Java browser plugin and Java Web Start.

%package        jdbc
Summary:        Sun Java JDBC/ODBC bridge driver
Group:          Development/Libraries
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       %{_libdir}/libodbc.so, %{_libdir}/libodbcinst.so

%description    jdbc
This package contains the Sun JDBC/ODBC bridge driver.


%prep
rm -rf $RPM_BUILD_DIR/%{toplevel_dir}
export MORE=10000
%ifarch x86_64
%define OURSOURCE %{SOURCE1}
%define DEMOSOURCE %{SOURCE3}
%else
%define OURSOURCE %{SOURCE0}
%define DEMOSOURCE %{SOURCE2}
%endif
sh %{OURSOURCE} <<EOF >/dev/null
yes
EOF
%setup -T -D -n %{toplevel_dir} -a 100
chmod -R go=u-w *
chmod -R u+w *

pushd ..
tar xvf %{DEMOSOURCE}
popd

%if %{tzupdate}
./bin/java -jar tzupdater-%(echo %{tzversion} | tr _ .)/tzupdater.jar -v -u
rm -rf jre/lib/zi.tzdata20[1-9][0-9][a-z]
%endif

# empty classes.jsa for %%ghosting so we can create it in %%post
%ifnarch x86_64
: > jre/lib/%{archname}/client/classes.jsa
%endif

# properties and XML files should not be executable
find . \( -name '*.properties' -o -name '*.xml' \) -print0 | xargs -0 chmod -x

# Avoid problematic ODBC dependencies
# The jdbc package looks for libodbc.so and libodbcinst.so sonames, but the Red Hat/Fedora
# unixODBC packages have sonames of libodbc.so.n and libodbcinst.so.n (n = 1 or 2).
# I don't know if this hack works but at least the package can install.
%global reqfilt /bin/sh -c "%{__find_requires} | %{__grep} -Evx 'libodbc(inst)?\\.so([(][)][(]64bit[)])?'"
%global __find_requires %{reqfilt}


%build
# Nope.


%install
rm -rf $RPM_BUILD_ROOT

# fix up ControlPanel APPHOME and bin locations
perl -p -i -e 's|APPHOME=.*|APPHOME=%{_jvmdir}/%{jredir}|' jre/bin/ControlPanel
perl -p -i -e 's|/usr/bin/||g' jre/bin/ControlPanel

# fix up (create new) HtmlConverter
cat > bin/HtmlConverter << EOF
#!/bin/sh

%{jrebindir}/java -jar %{sdklibdir}/htmlconverter.jar $*
EOF

%ifnarch x86_64
# fix up java-rmi.cgi PATH
perl -p -i -e 's|PATH=.*|PATH=%{jrebindir}|' bin/java-rmi.cgi
%endif

# main files
install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
cp -a bin include lib src.zip $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}

# extensions handling
install -d -m 755 $RPM_BUILD_ROOT%{jvmjardir}
pushd $RPM_BUILD_ROOT%{jvmjardir}
   # we'll make these symlinks relative later on...
   ln -s $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/jsse.jar jsse-%{version}.jar
   ln -s $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/jce.jar jce-%{version}.jar
   ln -s $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/rt.jar jndi-%{version}.jar
   ln -s $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/rt.jar jndi-ldap-%{version}.jar
   ln -s $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/rt.jar jndi-cos-%{version}.jar
   ln -s $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/rt.jar jndi-rmi-%{version}.jar
   ln -s $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/rt.jar jaas-%{version}.jar
   ln -s $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/rt.jar jdbc-stdext-%{version}.jar
   ln -s $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/rt.jar sasl-%{version}.jar
   ln -s jdbc-stdext-%{version}.jar jdbc-stdext-3.0.jar
   for jar in *-%{version}.jar ; do
      if [ x%{version} != x%{javaver} ]; then
         ln -fs ${jar} $(echo $jar | sed "s|-%{version}.jar|-%{javaver}.jar|g")
      fi
      ln -fs ${jar} $(echo $jar | sed "s|-%{version}.jar|.jar|g")
   done
popd

# rest of the jre
cp -a jre/bin jre/lib $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}
cp -a jre/javaws jre/plugin $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}
install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/endorsed

# fix up extensions symlinks
symlinks -cs $RPM_BUILD_ROOT%{jvmjardir}

# jce policy file handling
install -d -m 755 $RPM_BUILD_ROOT%{_jvmprivdir}/%{policydir}/jce/vanilla
for file in local_policy.jar US_export_policy.jar; do
  mv $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security/$file \
    $RPM_BUILD_ROOT%{_jvmprivdir}/%{policydir}/jce/vanilla
  # for ghosts
  touch $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security/$file
done

# versionless symlinks
pushd $RPM_BUILD_ROOT%{_jvmdir}
ln -s %{jredir} %{jrelnk}
ln -s %{sdkdir} %{sdklnk}
popd

pushd $RPM_BUILD_ROOT%{_jvmjardir}
ln -s %{sdkdir} %{jrelnk}
ln -s %{sdkdir} %{sdklnk}
popd

# ControlPanel freedesktop.org menu entry
perl -p -i -e 's|INSTALL_DIR/JRE_NAME_VERSION|%{_jvmdir}/%{jredir}|g' jre/plugin/desktop/sun_java.desktop
perl -p -i -e 's|Name=.*|Name=Sun Java 6 Plugin Control Panel|' jre/plugin/desktop/sun_java.desktop
perl -p -i -e 's|Icon=.*|Icon=%{name}-jcontrol.png|' jre/plugin/desktop/sun_java.desktop
perl -p -i -e 's|Exec=.*|Exec=%{_jvmdir}/%{jredir}/bin/jcontrol|' jre/plugin/desktop/sun_java.desktop
perl -p -i -e 's|Terminal=0|Terminal=false|' jre/plugin/desktop/sun_java.desktop
perl -p -i -e 's|Categories=.*|Categories=Settings;X-GNOME-NetworkSettings;X-Sun-Supported;X-Red-Hat-Base;|' \
   jre/plugin/desktop/sun_java.desktop

install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/{applications,pixmaps}
install -m 644 -p jre/lib/desktop/icons/hicolor/48x48/apps/sun-javaws.png \
   $RPM_BUILD_ROOT%{_datadir}/pixmaps/%{name}-jcontrol.png
install -m 644 -p jre/lib/desktop/icons/hicolor/48x48/apps/sun-javaws.png \
   $RPM_BUILD_ROOT%{_datadir}/pixmaps/%{name}-javaws.png

/usr/bin/desktop-file-install \
   --dir=$RPM_BUILD_ROOT%{_datadir}/applications \
   --vendor="" \
   jre/plugin/desktop/sun_java.desktop
perl -n -i -e 'print unless /^$/;' $RPM_BUILD_ROOT%{_datadir}/applications/sun_java.desktop
mv $RPM_BUILD_ROOT%{_datadir}/applications/sun_java.desktop \
   $RPM_BUILD_ROOT%{_datadir}/applications/java-1.6.0-sun-ControlPanel.desktop

# javaws freedesktop.org menu entry
cat >> %{name}-javaws.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=Sun Java 6 Web Start
Comment=Java Application Launcher
Exec=%{_jvmdir}/%{jredir}/bin/javaws
Icon=%{name}-javaws.png
Terminal=false
Type=Application
NoDisplay=true
Categories=Network;WebBrowser;X-Red-Hat-Base;
MimeType=application/x-java-jnlp-file;
EOF
/usr/bin/desktop-file-install \
   --dir=$RPM_BUILD_ROOT%{_datadir}/applications \
   --vendor="" \
   %{name}-javaws.desktop
perl -n -i -e 'print unless /^$/;' $RPM_BUILD_ROOT%{_datadir}/applications/%{name}-javaws.desktop

# man pages
install -d -m 755 $RPM_BUILD_ROOT%{_mandir}/man1
for manpage in man/man1/*; do
  install -m 644 -p $manpage $RPM_BUILD_ROOT%{_mandir}/man1/`basename $manpage .1`-%{name}.%{_arch}.1
done

# demo
install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
cp -a demo $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
# mark README.txt files as %%doc
(
find $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/demo -type d \
  | sed 's|'$RPM_BUILD_ROOT'|%dir |'
find $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/demo -type f -o -type l \
  | sed 's|'$RPM_BUILD_ROOT'||' \
  | awk '/\/README.txt$/ { printf "%%%%doc " } { print }'
) > %{name}-%{version}-demo.files

# make placeholder directory for plugin
mkdir -p $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# %%{_jvmdir}/%%{jredir}/lib/fonts was a symlink in older releases,
# and is a directory now; rpm needs some assistance dealing with this situation
[ -h %{_jvmdir}/%{jredir}/lib/fonts ] && rm -f %{_jvmdir}/%{jredir}/lib/fonts || :

%post
# Handle various manpage compression methods cleanly
ext=
[ -f %{_mandir}/man1/java-%{name}.%{_arch}.1.bz2 ] && ext=".bz2"
[ -f %{_mandir}/man1/java-%{name}.%{_arch}.1.gz ] && ext=".gz"
[ -f %{_mandir}/man1/java-%{name}.%{_arch}.1.xz ] && ext=".xz"

update-alternatives --install %{_bindir}/java java %{jrebindir}/java %{priority} \
--slave %{_jvmdir}/jre                     jre                         %{_jvmdir}/%{jrelnk} \
--slave %{_jvmjardir}/jre                  jre_exports                 %{_jvmjardir}/%{jrelnk} \
--slave %{_bindir}/jcontrol                jcontrol                    %{jrebindir}/jcontrol \
--slave %{_bindir}/keytool                 keytool                     %{jrebindir}/keytool \
--slave %{_bindir}/orbd                    orbd                        %{jrebindir}/orbd \
--slave %{_bindir}/policytool              policytool                  %{jrebindir}/policytool \
--slave %{_bindir}/rmid                    rmid                        %{jrebindir}/rmid \
--slave %{_bindir}/rmiregistry             rmiregistry                 %{jrebindir}/rmiregistry \
--slave %{_bindir}/servertool              servertool                  %{jrebindir}/servertool \
--slave %{_bindir}/tnameserv               tnameserv                   %{jrebindir}/tnameserv \
--slave %{_mandir}/man1/java.1$ext         java.1$ext                  %{_mandir}/man1/java-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/keytool.1$ext      keytool.1$ext               %{_mandir}/man1/keytool-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/orbd.1$ext         orbd.1$ext                  %{_mandir}/man1/orbd-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/policytool.1$ext   policytool.1$ext            %{_mandir}/man1/policytool-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/rmid.1$ext         rmid.1$ext                  %{_mandir}/man1/rmid-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/rmiregistry.1$ext  rmiregistry.1$ext           %{_mandir}/man1/rmiregistry-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/servertool.1$ext   servertool.1$ext            %{_mandir}/man1/servertool-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/tnameserv.1$ext    tnameserv.1$ext             %{_mandir}/man1/tnameserv-%{name}.%{_arch}.1$ext

update-alternatives --install %{_jvmdir}/jre-%{origin} jre_%{origin} %{_jvmdir}/%{jrelnk} %{priority} \
--slave %{_jvmjardir}/jre-%{origin}        jre_%{origin}_exports     %{_jvmjardir}/%{jrelnk}

update-alternatives --install %{_jvmdir}/jre-%{javaver} jre_%{javaver} %{_jvmdir}/%{jrelnk} %{priority} \
--slave %{_jvmjardir}/jre-%{javaver}       jre_%{javaver}_exports      %{_jvmjardir}/%{jrelnk}

if [ -d %{_jvmdir}/%{jrelnk}/lib/security ]; then
  # Need to remove the old jars in order to support upgrading, ugly :(
  # update-alternatives fails silently if the link targets exist as files.
  rm -f %{_jvmdir}/%{jrelnk}/lib/security/{local,US_export}_policy.jar
fi
update-alternatives \
  --install \
    %{_jvmdir}/%{jrelnk}/lib/security/local_policy.jar \
    jce_%{javaver}_%{origin}_local_policy%{multi_suffix} \
    %{_jvmprivdir}/%{policydir}/jce/vanilla/local_policy.jar \
    %{priority} \
  --slave \
    %{_jvmdir}/%{jrelnk}/lib/security/US_export_policy.jar \
    jce_%{javaver}_%{origin}_us_export_policy%{multi_suffix} \
    %{_jvmprivdir}/%{policydir}/jce/vanilla/US_export_policy.jar

# build classes.jsa
%ifnarch x86_64
cd %{_jvmdir}/%{jredir}
rm -f lib/%{archname}/client/classes.jsa
./bin/java -client -Xshare:dump > /dev/null
%endif

%post devel
# Handle various manpage compression methods cleanly
ext=
[ -f %{_mandir}/man1/javac-%{name}.%{_arch}.1.bz2 ] && ext=".bz2"
[ -f %{_mandir}/man1/javac-%{name}.%{_arch}.1.gz ] && ext=".gz"
[ -f %{_mandir}/man1/javac-%{name}.%{_arch}.1.xz ] && ext=".xz"

update-alternatives --install %{_bindir}/javac javac %{sdkbindir}/javac %{priority} \
--slave %{_jvmdir}/java                     java_sdk                    %{_jvmdir}/%{sdklnk} \
--slave %{_jvmjardir}/java                  java_sdk_exports            %{_jvmjardir}/%{sdklnk} \
--slave %{_bindir}/appletviewer             appletviewer                %{sdkbindir}/appletviewer \
--slave %{_bindir}/extcheck                 extcheck                    %{sdkbindir}/extcheck \
--slave %{_bindir}/idlj                     idlj                        %{sdkbindir}/idlj \
--slave %{_bindir}/jar                      jar                         %{sdkbindir}/jar \
--slave %{_bindir}/jarsigner                jarsigner                   %{sdkbindir}/jarsigner \
--slave %{_bindir}/javadoc                  javadoc                     %{sdkbindir}/javadoc \
--slave %{_bindir}/javah                    javah                       %{sdkbindir}/javah \
--slave %{_bindir}/javap                    javap                       %{sdkbindir}/javap \
--slave %{_bindir}/jdb                      jdb                         %{sdkbindir}/jdb \
--slave %{_bindir}/native2ascii             native2ascii                %{sdkbindir}/native2ascii \
--slave %{_bindir}/rmic                     rmic                        %{sdkbindir}/rmic \
--slave %{_bindir}/serialver                serialver                   %{sdkbindir}/serialver \
--slave %{_bindir}/jconsole                 jconsole                    %{sdkbindir}/jconsole \
--slave %{_bindir}/pack200                  pack200                     %{sdkbindir}/pack200 \
--slave %{_bindir}/unpack200                unpack200                   %{sdkbindir}/unpack200 \
--slave %{_bindir}/HtmlConverter            HtmlConverter               %{sdkbindir}/HtmlConverter \
--slave %{_bindir}/apt                      apt                         %{sdkbindir}/apt \
--slave %{_bindir}/jhat                     jhat                        %{sdkbindir}/jhat \
--slave %{_bindir}/jinfo                    jinfo                       %{sdkbindir}/jinfo \
--slave %{_bindir}/jmap                     jmap                        %{sdkbindir}/jmap \
--slave %{_bindir}/jps                      jps                         %{sdkbindir}/jps \
--slave %{_bindir}/jrunscript               jrunscript                  %{sdkbindir}/jrunscript \
--slave %{_bindir}/jsadebugd                jsadebugd                   %{sdkbindir}/jsadebugd \
--slave %{_bindir}/jstack                   jstack                      %{sdkbindir}/jstack \
--slave %{_bindir}/jvisualvm                jvisualvm                   %{sdkbindir}/jvisualvm \
--slave %{_bindir}/jstat                    jstat                       %{sdkbindir}/jstat \
--slave %{_bindir}/jstatd                   jstatd                      %{sdkbindir}/jstatd \
--slave %{_bindir}/schemagen                schemagen                   %{sdkbindir}/schemagen \
--slave %{_bindir}/wsgen                    wsgen                       %{sdkbindir}/wsgen \
--slave %{_bindir}/wsimport                 wsimport                    %{sdkbindir}/wsimport \
--slave %{_bindir}/xjc                      xjc                         %{sdkbindir}/xjc \
--slave %{_mandir}/man1/appletviewer.1$ext  appletviewer.1$ext          %{_mandir}/man1/appletviewer-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/extcheck.1$ext      extcheck.1$ext              %{_mandir}/man1/extcheck-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/idlj.1$ext          idlj.1$ext                  %{_mandir}/man1/idlj-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/jar.1$ext           jar.1$ext                   %{_mandir}/man1/jar-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/jarsigner.1$ext     jarsigner.1$ext             %{_mandir}/man1/jarsigner-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/javac.1$ext         javac.1$ext                 %{_mandir}/man1/javac-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/javadoc.1$ext       javadoc.1$ext               %{_mandir}/man1/javadoc-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/javah.1$ext         javah.1$ext                 %{_mandir}/man1/javah-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/javap.1$ext         javap.1$ext                 %{_mandir}/man1/javap-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/jdb.1$ext           jdb.1$ext                   %{_mandir}/man1/jdb-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/native2ascii.1$ext  native2ascii.1$ext          %{_mandir}/man1/native2ascii-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/rmic.1$ext          rmic.1$ext                  %{_mandir}/man1/rmic-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/serialver.1$ext     serialver.1$ext             %{_mandir}/man1/serialver-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/jconsole.1$ext      jconsole.1$ext              %{_mandir}/man1/jconsole-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/pack200.1$ext       pack200.1$ext               %{_mandir}/man1/pack200-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/unpack200.1$ext     unpack200.1$ext             %{_mandir}/man1/unpack200-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/apt.1$ext           apt.1$ext                   %{_mandir}/man1/apt-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/jhat.1$ext          jhat.1$ext                  %{_mandir}/man1/jhat-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/jinfo.1$ext         jinfo.1$ext                 %{_mandir}/man1/jinfo-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/jmap.1$ext          jmap.1$ext                  %{_mandir}/man1/jmap-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/jps.1$ext           jps.1$ext                   %{_mandir}/man1/jps-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/jrunscript.1$ext    jrunscript.1$ext            %{_mandir}/man1/jrunscript-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/jsadebugd.1$ext     jsadebugd.1$ext             %{_mandir}/man1/jsadebugd-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/jstack.1$ext        jstack.1$ext                %{_mandir}/man1/jstack-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/jvisualvm.1$ext     jvisualvm.1$ext             %{_mandir}/man1/jvisualvm-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/jstat.1$ext         jstat.1$ext                 %{_mandir}/man1/jstat-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/jstatd.1$ext        jstatd.1$ext                %{_mandir}/man1/jstatd-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/schemagen.1$ext     schemagen.1$ext             %{_mandir}/man1/schemagen-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/wsgen.1$ext         wsgen.1$ext                 %{_mandir}/man1/wsgen-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/wsimport.1$ext      wsimport.1$ext              %{_mandir}/man1/wsimport-%{name}.%{_arch}.1$ext \
--slave %{_mandir}/man1/xjc.1$ext           xjc.1$ext                   %{_mandir}/man1/xjc-%{name}.%{_arch}.1$ext

update-alternatives --install %{_jvmdir}/java-%{origin} java_sdk_%{origin} %{_jvmdir}/%{sdklnk} %{priority} \
--slave %{_jvmjardir}/java-%{origin}        java_sdk_%{origin}_exports     %{_jvmjardir}/%{sdklnk}

update-alternatives --install %{_jvmdir}/java-%{javaver} java_sdk_%{javaver} %{_jvmdir}/%{sdklnk} %{priority} \
--slave %{_jvmjardir}/java-%{javaver}       java_sdk_%{javaver}_exports      %{_jvmjardir}/%{sdklnk}


%postun
if [ $1 -eq 0 ]; then
  update-alternatives --remove java %{jrebindir}/java
  update-alternatives --remove \
    jce_%{javaver}_%{origin}_local_policy%{multi_suffix} \
    %{_jvmprivdir}/%{policydir}/jce/vanilla/local_policy.jar
  update-alternatives --remove jre_%{origin}  %{_jvmdir}/%{jrelnk}
  update-alternatives --remove jre_%{javaver} %{_jvmdir}/%{jrelnk}
fi


%postun devel
if [ $1 -eq 0 ]; then
  update-alternatives --remove javac %{sdkbindir}/javac
  update-alternatives --remove java_sdk_%{origin}  %{_jvmdir}/%{sdklnk}
  update-alternatives --remove java_sdk_%{javaver} %{_jvmdir}/%{sdklnk}
fi


%post plugin
# Register MIME type application/x-java-jnlp-file for javaws
update-desktop-database %{_datadir}/applications &>/dev/null || :

# Handle various manpage compression methods cleanly
ext=
[ -f %{_mandir}/man1/java-%{name}.%{_arch}.1.bz2 ] && ext=".bz2"
[ -f %{_mandir}/man1/java-%{name}.%{_arch}.1.gz ] && ext=".gz"
[ -f %{_mandir}/man1/java-%{name}.%{_arch}.1.xz ] && ext=".xz"

# Remove cruft left over from old packages
cruft=`alternatives --display %{javaplugin} | \
  %{__grep} -F 'jre-%{javaver}-%{origin}' | \
  %{__grep} -Fv '%{pluginname}' | \
  %{__awk} '/^\// { print $1 }'`
if [ -n "${cruft}" ]; then
  for oldplugin in `echo ${cruft}`; do
    update-alternatives --remove %{javaplugin} ${oldplugin}
  done
fi
update-alternatives --remove javaws %{jrebindir}/javaws
sed -i 's|share/javaws|bin/javaws|g' %{_localstatedir}/lib/alternatives/%{javaplugin}  2> /dev/null

# Add the current plugin, ControlPanel and javaws
update-alternatives --install %{_libdir}/mozilla/plugins/libjavaplugin.so %{javaplugin} %{pluginname} %{priority} \
--slave %{_bindir}/ControlPanel            ControlPanel                %{jrebindir}/ControlPanel \
--slave %{_bindir}/javaws                  javaws                      %{jrebindir}/javaws \
--slave %{_mandir}/man1/javaws.1$ext       javaws.1$ext                %{_mandir}/man1/javaws-%{name}.%{_arch}.1$ext

# Complete cruft removal
rm -f %{_datadir}/javaws

%postun plugin
# Unregister MIME type application/x-java-jnlp-file for javaws
update-desktop-database %{_datadir}/applications &>/dev/null || :

if [ "$1" = "0" ]; then
    update-alternatives --remove %{javaplugin} %{pluginname}
fi

%files
%defattr(-,root,root,-)
%doc jre/COPYRIGHT jre/THIRDPARTYLICENSEREADME.txt jre/README
%doc jre/Welcome.html
%dir %{_jvmdir}/%{sdkdir}/
%dir %{_jvmdir}/%{jredir}/
%dir %{_jvmdir}/%{jredir}/bin/
%{_jvmdir}/%{jredir}/bin/ControlPanel
%{_jvmdir}/%{jredir}/bin/java
%{_jvmdir}/%{jredir}/bin/java_vm
%{_jvmdir}/%{jredir}/bin/jcontrol
%{_jvmdir}/%{jredir}/bin/keytool
%{_jvmdir}/%{jredir}/bin/orbd
%{_jvmdir}/%{jredir}/bin/pack200
%{_jvmdir}/%{jredir}/bin/policytool
%{_jvmdir}/%{jredir}/bin/rmid
%{_jvmdir}/%{jredir}/bin/rmiregistry
%{_jvmdir}/%{jredir}/bin/servertool
%{_jvmdir}/%{jredir}/bin/tnameserv
%{_jvmdir}/%{jredir}/bin/unpack200
%dir %{_jvmdir}/%{jredir}/lib/
%dir %{_jvmdir}/%{jredir}/lib/%{archname}/
%ifnarch x86_64
%dir %{_jvmdir}/%{jredir}/lib/%{archname}/client/
%ghost %{_jvmdir}/%{jredir}/lib/%{archname}/client/classes.jsa
%{_jvmdir}/%{jredir}/lib/%{archname}/client/libjsig.so
%{_jvmdir}/%{jredir}/lib/%{archname}/client/libjvm.so
%{_jvmdir}/%{jredir}/lib/%{archname}/client/Xusage.txt
%endif
%{_jvmdir}/%{jredir}/lib/%{archname}/headless/
%{_jvmdir}/%{jredir}/lib/%{archname}/jli/
%{_jvmdir}/%{jredir}/lib/%{archname}/motif21/
%{_jvmdir}/%{jredir}/lib/%{archname}/native_threads/
%{_jvmdir}/%{jredir}/lib/%{archname}/server/
%{_jvmdir}/%{jredir}/lib/%{archname}/xawt/
%{_jvmdir}/%{jredir}/lib/%{archname}/jvm.cfg
%{_jvmdir}/%{jredir}/lib/%{archname}/libattach.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libawt.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libcmm.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libdcpr.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libdeploy.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libdt_socket.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libfontmanager.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libhprof.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libinstrument.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libioser12.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libj2gss.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libj2pcsc.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libj2pkcs11.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libjaas_unix.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libjava.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libjava_crw_demo.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libjawt.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libjdwp.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libjpeg.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libjsig.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libjsound.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libjsoundalsa.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libmanagement.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libmlib_image.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libnative_chmod.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libnative_chmod_g.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libnet.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libnio.so
# Not sure why this is packaged here as well as the plugin package
%{_jvmdir}/%{jredir}/lib/%{archname}/libnpjp2.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libnpt.so
%{_jvmdir}/%{jredir}/lib/%{archname}/librmi.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libsaproc.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libsplashscreen.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libunpack.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libverify.so
%{_jvmdir}/%{jredir}/lib/%{archname}/libzip.so
%{_jvmdir}/%{jredir}/lib/alt-rt.jar
%{_jvmdir}/%{jredir}/lib/alt-string.jar
%{_jvmdir}/%{jredir}/lib/applet
%{_jvmdir}/%{jredir}/lib/audio/
%{_jvmdir}/%{jredir}/lib/calendars.properties
%{_jvmdir}/%{jredir}/lib/charsets.jar
%{_jvmdir}/%{jredir}/lib/classlist
%{_jvmdir}/%{jredir}/lib/cmm/
%{_jvmdir}/%{jredir}/lib/content-types.properties
%{_jvmdir}/%{jredir}/lib/deploy/
%{_jvmdir}/%{jredir}/lib/deploy.jar
%dir %{_jvmdir}/%{jredir}/lib/desktop/
%dir %{_jvmdir}/%{jredir}/lib/desktop/applications/
%{_jvmdir}/%{jredir}/lib/desktop/applications/sun-java.desktop
%{_jvmdir}/%{jredir}/lib/desktop/applications/sun_java.desktop
%dir %{_jvmdir}/%{jredir}/lib/desktop/icons/
%dir %{_jvmdir}/%{jredir}/lib/desktop/icons/*/
%dir %{_jvmdir}/%{jredir}/lib/desktop/icons/*/*/
%dir %{_jvmdir}/%{jredir}/lib/desktop/icons/*/*/apps/
%{_jvmdir}/%{jredir}/lib/desktop/icons/*/*/apps/sun-java.png
%{_jvmdir}/%{jredir}/lib/desktop/icons/*/*/apps/sun-jcontrol.png
%{_jvmdir}/%{jredir}/lib/desktop/icons/*/*/mimetypes/
%{_jvmdir}/%{jredir}/lib/desktop/mime/
%{_jvmdir}/%{jredir}/lib/endorsed/
%{_jvmdir}/%{jredir}/lib/ext/
%{_jvmdir}/%{jredir}/lib/flavormap.properties
%{_jvmdir}/%{jredir}/lib/fontconfig.*
%{_jvmdir}/%{jredir}/lib/fonts/
%{_jvmdir}/%{jredir}/lib/im/
%{_jvmdir}/%{jredir}/lib/images/
%{_jvmdir}/%{jredir}/lib/jce.jar
%{_jvmdir}/%{jredir}/lib/jexec
%{_jvmdir}/%{jredir}/lib/jsse.jar
%{_jvmdir}/%{jredir}/lib/jvm.hprof.txt
%dir %{_jvmdir}/%{jredir}/lib/locale/
%dir %{_jvmdir}/%{jredir}/lib/locale/*/
%dir %{_jvmdir}/%{jredir}/lib/locale/*/LC_MESSAGES/
%{_jvmdir}/%{jredir}/lib/logging.properties
%{_jvmdir}/%{jredir}/lib/management/
%{_jvmdir}/%{jredir}/lib/management-agent.jar
%{_jvmdir}/%{jredir}/lib/meta-index
%{_jvmdir}/%{jredir}/lib/net.properties
%{_jvmdir}/%{jredir}/lib/oblique-fonts/
%{_jvmdir}/%{jredir}/lib/psfont.properties.ja
%{_jvmdir}/%{jredir}/lib/psfontj2d.properties
%{_jvmdir}/%{jredir}/lib/resources.jar
%{_jvmdir}/%{jredir}/lib/rt.jar
%{_jvmdir}/%{jredir}/lib/servicetag/
%{_jvmdir}/%{jredir}/lib/sound.properties
%{_jvmdir}/%{jredir}/lib/zi/
%dir %{_jvmdir}/%{jredir}/lib/security/
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/blacklist
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/cacerts
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/java.policy
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/java.security
%ghost %{_jvmdir}/%{jredir}/lib/security/local_policy.jar
%ghost %{_jvmdir}/%{jredir}/lib/security/US_export_policy.jar
%{_jvmdir}/%{jrelnk}/
%{_jvmjardir}/%{jrelnk}/
%{_jvmjardir}/%{sdkdir}/
%{_jvmprivdir}/%{policydir}/
%{_mandir}/man1/java-%{name}.%{_arch}.1*
%{_mandir}/man1/keytool-%{name}.%{_arch}.1*
%{_mandir}/man1/orbd-%{name}.%{_arch}.1*
%{_mandir}/man1/policytool-%{name}.%{_arch}.1*
%{_mandir}/man1/rmid-%{name}.%{_arch}.1*
%{_mandir}/man1/rmiregistry-%{name}.%{_arch}.1*
%{_mandir}/man1/servertool-%{name}.%{_arch}.1*
%{_mandir}/man1/tnameserv-%{name}.%{_arch}.1*

%files devel
%defattr(-,root,root,-)
%doc COPYRIGHT THIRDPARTYLICENSEREADME.txt README.html
%{_jvmdir}/%{sdkdir}/bin/
%{_jvmdir}/%{sdkdir}/include/
%{_jvmdir}/%{sdkdir}/lib/
%{_jvmdir}/%{sdklnk}
%{_jvmjardir}/%{sdklnk}
%{_mandir}/man1/appletviewer-%{name}.%{_arch}.1*
%{_mandir}/man1/extcheck-%{name}.%{_arch}.1*
%{_mandir}/man1/idlj-%{name}.%{_arch}.1*
%{_mandir}/man1/jar-%{name}.%{_arch}.1*
%{_mandir}/man1/jarsigner-%{name}.%{_arch}.1*
%{_mandir}/man1/javac-%{name}.%{_arch}.1*
%{_mandir}/man1/javadoc-%{name}.%{_arch}.1*
%{_mandir}/man1/javah-%{name}.%{_arch}.1*
%{_mandir}/man1/javap-%{name}.%{_arch}.1*
%{_mandir}/man1/jdb-%{name}.%{_arch}.1*
%{_mandir}/man1/jvisualvm-%{name}.%{_arch}.1*
%{_mandir}/man1/native2ascii-%{name}.%{_arch}.1*
%{_mandir}/man1/rmic-%{name}.%{_arch}.1*
%{_mandir}/man1/serialver-%{name}.%{_arch}.1*
%{_mandir}/man1/jconsole-%{name}.%{_arch}.1*
%{_mandir}/man1/pack200-%{name}.%{_arch}.1*
%{_mandir}/man1/unpack200-%{name}.%{_arch}.1*
%{_mandir}/man1/apt-%{name}.%{_arch}.1*
%{_mandir}/man1/jinfo-%{name}.%{_arch}.1*
%{_mandir}/man1/jmap-%{name}.%{_arch}.1*
%{_mandir}/man1/jps-%{name}.%{_arch}.1*
%{_mandir}/man1/jsadebugd-%{name}.%{_arch}.1*
%{_mandir}/man1/jstack-%{name}.%{_arch}.1*
%{_mandir}/man1/jstat-%{name}.%{_arch}.1*
%{_mandir}/man1/jstatd-%{name}.%{_arch}.1*
%{_mandir}/man1/jhat-%{name}.%{_arch}.1*
%{_mandir}/man1/jrunscript-%{name}.%{_arch}.1*
%{_mandir}/man1/schemagen-%{name}.%{_arch}.1*
%{_mandir}/man1/wsgen-%{name}.%{_arch}.1*
%{_mandir}/man1/wsimport-%{name}.%{_arch}.1*
%{_mandir}/man1/xjc-%{name}.%{_arch}.1*

%files src
%defattr(-,root,root,-)
%{_jvmdir}/%{sdkdir}/src.zip

%files -f %{name}-%{version}-demo.files demo
%defattr(-,root,root,-)

%files jdbc
%defattr(-,root,root,-)
%{_jvmdir}/%{jredir}/lib/security/trusted.libraries
%{_jvmdir}/%{jredir}/lib/%{archname}/libJdbcOdbc.so

%files plugin
%defattr(-,root,root,-)
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/javaws.policy
%{_datadir}/applications/%{name}-ControlPanel.desktop
%{_datadir}/applications/%{name}-javaws.desktop
%{_datadir}/pixmaps/%{name}-jcontrol.png
%{_datadir}/pixmaps/%{name}-javaws.png
%{_jvmdir}/%{jredir}/bin/javaws
%{_jvmdir}/%{jredir}/javaws/
%{_jvmdir}/%{jredir}/lib/%{archname}/libjavaplugin_*.so
%{_jvmdir}/%{jredir}/lib/desktop/applications/sun-javaws.desktop
%{_jvmdir}/%{jredir}/lib/desktop/icons/*/*/apps/sun-javaws.png
%{_jvmdir}/%{jredir}/lib/locale/*/LC_MESSAGES/sunw_java_plugin.mo
%{_jvmdir}/%{jredir}/lib/javaws.jar
%{_jvmdir}/%{jredir}/lib/plugin.jar
%{_jvmdir}/%{jredir}/plugin/
%{_jvmdir}/%{jrelnk}/lib/%{archname}/libnpjp2.so
%{_mandir}/man1/javaws-%{name}.%{_arch}.1*

%changelog
* Mon Dec 20 2010 Paul Howarth <paul@city-fan.org> - 1:1.6.0.23-1.0.cf
- update to 1.6.0.23

* Wed Dec  8 2010 Paul Howarth <paul@city-fan.org> - 1:1.6.0.22-2.0.cf
- update tzupdater to 1_3_34-2010o

* Fri Oct 15 2010 Paul Howarth <paul@city-fan.org> - 1:1.6.0.22-1.1.cf
- update tzupdater to 1_3_33-2010l

* Wed Oct 13 2010 Paul Howarth <paul@city-fan.org> - 1:1.6.0.22-1.0.cf
- update to 1.6.0.22

* Thu Sep  9 2010 Paul Howarth <paul@city-fan.org> - 1:1.6.0.21-1.0.cf
- bump epoch to 1 as per Red Hat EL-5 package
- add tzupdater 1_3_31-2010i
- add a null vendor option in desktop-file-install so that it works with old
  versions of desktop-file-utils such as CentOS 5
- fix URL (#495280)
- fix up some other package metadata to make it more in the Red Hat style
- added arch to man path - enables both arch installed on one machine
- add x86_64 to various directories on x86_64 to fix multilib conflicts
- add x86_64 to alternatives names on x86_64 to fix multilib conflicts
- use proper %%files lists rather than hacky script-based approach
  (except for demo package)
- drop legacy conflicts/obsoletes
- move the demo files to %%{_jvmdir}/%%{sdkdir}/demo/
- move javaws and ControlPanel to the plugin package
- move %%{_jvmdir}/%%{jredir}/lib/security/trusted.libraries to the jdbc package
- bump alternatives priority to 1600%%{buildver}
- merge alsa subpackage into main package
- merge fonts subpackage into main package
- no longer need to package %%{_datadir}/pixmaps/%%{name}.png (references
  removed from desktop files)
- drop scriptlets for messing with /etc/fonts/fonts.conf; someone who knows
  what they are doing should create a file to drop into /etc/fonts/conf.d
  instead
- don't install /var/www/cgi-bin/java-rmi.cgi
- %%ghost classes.jsa and build in %%post instead (i586 package only)
- mark README.txt files as %%doc in demo package
- remove unnecessary exec permissions on XML and properties files
- make symlinks relative rather than absolute (BR: symlinks)
- fix up desktop files to be like the Red Hat EL-5 package versions
- add support for xz-compressed manpages
- add further alternatives slaves for SDK binaries

* Sat Jul 24 2010 Paul Howarth <paul@city-fan.org> - 0:1.6.0.21-1.0.cf
- update to 1.6.0.21
- license changed to Oracle Corporation Binary Code License

* Mon Jul  5 2010 Paul Howarth <paul@city-fan.org> - 0:1.6.0.20-2.0.cf
- use libnpjp2.so as the browser plugin for all architectures since the old
  libjavaplugin_oji.so doesn't work any more, at least in Fedora 13

* Thu Apr 15 2010 Paul Howarth <paul@city-fan.org> - 0:1.6.0.20-1.0.cf
- update to 1.6.0.20

* Thu Apr  1 2010 Paul Howarth <paul@city-fan.org> - 0:1.6.0.19-1.0.cf
- update to 1.6.0.19 (thanks to Stephan Buchert for update)
- add %%{_jvmdir}/%%{jredir}/lib/security/trusted.libraries

* Tue Mar  2 2010 Paul Howarth <paul@city-fan.org> - 0:1.6.0.18-1.0.cf
- update to 1.6.0.18

* Thu Nov  9 2009 Paul Howarth <paul@city-fan.org> - 0:1.6.0.17-1.0.cf
- update to 1.6.0.17

* Mon Aug 17 2009 Paul Howarth <paul@city-fan.org> - 0:1.6.0.16-1.0.cf
- update to 1.6.0.16
- use %%{jrelnk} rather than %%{jredir} in alternatives links to make them
  work across package updates
- automatically remove old plugin alternatives

* Wed Aug  5 2009 Paul Howarth <paul@city-fan.org> - 0:1.6.0.15-1.0.cf
- update to 1.6.0.15
- add %%{_jvmdir}/%%{jredir}/lib/security/blacklist
- specifically filter out unresolvable dependencies on libodbc.so and
  libodbcinst.so (we still have dependencies on %%{_libdir}/libodbc.so and
  %%{_libdir}/libodbcinst.so so we pull in the right packages)
- make the javaws alternative a link from %%_bindir rather than %%_datadir;
  this is incompatible with JPackage but matches java-1.6.0-openjdk in F9
- if javaws is already registered as an alternatives java slave pointing from
  %%{_datadir}/javaws, fix it to point from %%{_bindir}/javaws instead;
  otherwise the alternatives install will fail; this is necessary to support
  upgrades from earlier java-1.6.0-sun packages
- drop dependency on /usr/sbin/chkfontpath in fonts subpackage, since Fedora
  9 doesn't even include it in the distribution
- add a symlink in /etc/X11/fontpath.d for the font directory instead
- change %%x11bindir and %%x11encdir directories from old XFree86 locations
  to modern X.Org locations suitable for Fedora 7 / CentOS 5 onwards
- disable apparently-broken fiddling with /etc/mailcap and /etc/mime.types
  for jnlp files in %%post; instead add the MIME type to the desktop file and
  use update-desktop-database in %%post and %%postun
- dispense with all efforts to manage plugin symlinks in versioned browser
  directories and instead use alternatives to manage a plugin link in
  %%_libdir/mozilla/plugins
- tweak desktop files to make them pass desktop-file-validate and appear in
  the menus
- don't repack jars
- add alternatives links for jcontrol and jvisualvm
- fix plugin alternatives name to be compatible with java-1.6.0-openjdk-plugin
- add dependency on %%{_libdir}/mozilla/plugins dir rather than owning it
- tweak categories in javaws desktop file as per java-1.6.0-openjdk
- don't set up alternatives for no-longer-supplied manpages kinit, klist, ktab
- use libnpjp2.so rather than libjavaplugin_jni.so for x86_64 browser plugin
- use desktop-file-install to install desktop files

* Tue Jul 21 2009 Ralph Apel <r.apel@r-apel.de> 0:1.6.0.14-1jpp
- 1.6.0.14

* Thu Jan 22 2009 Jason Corley <jason.corley@gmail.com> 0:1.6.0.11-1jpp
- update copyright to include 2009
- 1.6.0.10

* Tue Oct 21 2008 Jason Corley <jason.corley@gmail.com> 0:1.6.0.10-1jpp
- 1.6.0.10

* Mon Aug 11 2008 Jason Corley <jason.corley@gmail.com> 0:1.6.0.7-1jpp
- 1.6.0.7
- add new jvisualvm man page

* Wed May 21 2008 Jason Corley <jason.corley@gmail.com> 0:1.6.0.6-1jpp
- 1.6.0.6

* Mon Mar 10 2008 Jason Corley <jason.corley@gmail.com> 0:1.6.0.5-1jpp
- 1.6.0.5
- update copyright

* Mon Jan 14 2008 Jason Corley <jason.corley@gmail.com> 0:1.6.0.4-1jpp
- 1.6.0.4
- fix 64 bit build

* Sun Oct 07 2007 Jason Corley <jason.corley@gmail.com> 0:1.6.0.3-1jpp
- 1.6.0.3

* Wed Jul 04 2007 Jason Corley <jason.corley@gmail.com> 0:1.6.0.2-1jpp
- 1.6.0.2

* Sat Jun 23 2007 Jason Corley <jason.corley@gmail.com> 0:1.6.0.1-1jpp
- 1.6.0.1 (contributed by Lyle Dietz)
- remove redundant defines for name, version, and release
- remove vendor and distribution (should be defined in ~/.rpmmacros)
- add JPackage license

* Thu Dec 21 2006 Jason Corley <jason.corley@gmail.com> 0:1.5.0.10-2jpp
- respin, no changes

* Wed Dec 20 2006 Jason Corley <jason.corley@gmail.com> 0:1.5.0.10-1jpp
- Upgrade to 1.5.0_10

* Mon Oct  2 2006 Jason Corley <jason.corley@gmail.com> 0:1.5.0.09-1jpp
- Upgrade to 1.5.0_09... stupid Sun :-P (submitted by Henning Schmiedehausen)

* Fri Sep 29 2006 Jason Corley <jason.corley@gmail.com> 0:1.5.0.08-1jpp
- Upgrade to 1.5.0_08

* Fri Jun 8 2006 Jason Corley <jason.corley@gmail.com> 0:1.5.0.07-1jpp
- Upgrade to 1.5.0_07

* Fri Feb 3 2006 Jason Corley <jason.corley@gmail.com> 0:1.5.0.06-1jpp
- Upgrade to 1.5.0_06

* Wed Sep 28 2005 Jason Corley <jason.corley@gmail.com> 0:1.5.0.05-1jpp
- Upgrade to 1.5.0_05

* Mon Jun 27 2005 Jason Corley <jason.corley@gmail.com> 0:1.5.0.04-1jpp
- Upgrade to 1.5.0_04

* Wed May 04 2005 David Walluck <david@jpackage.org> 0:1.5.0.03-1jpp
- 1.5.0_03

* Wed Mar 16 2005 Jason Corley <jason.corley@gmail.com> 0:1.5.0.02-1jpp
- Upgrade to 1.5.0_02

* Tue Feb 08 2005 Kaj J. Niemi <kajtzu@fi.basen.net> 0:1.5.0.01-3jpp
- Support for x86_64 (amd64); no javaws, no plugins

* Wed Jan 19 2005 David Walluck <david@jpackage.org> 0:1.5.0.01-1jpp
- 1.5.0_01

* Thu Jan 06 2005 Carwyn Edwards <carwyn@carwyn.com> - 0:1.5.0.01-0.cte.1
- Updated to Upstream 1.5.0_01.
- Added long cvsversion definition.
- Rearranged defintiions that are sensitive to buildver.

* Sat Nov 13 2004 Ville Skyttä <scop at jpackage.org> - 0:1.5.0-3jpp
- Provide java-sasl.
- Fix build failure when no previous java-1.5.0 package is installed
  (%%{jvmjardir}/*.jar are dangling symlinks at build time).
- Minor spec cleanups and consistency tweaks.

* Sun Oct 17 2004 Carwyn Edwards <carwyn@carwyn.com> - 0:1.5.0-2jpp.cte.1
- Switched off rpm internal dependency generator. This fixes the bogus
  devel package provides noted in 1.5.0-0.beta2.4jpp.
- Changed auto requires/provides for all packages to be the same as
  java-1.4.2-sun (all on except jdbc due to libodbc name variability).
- AutoReq off for demo package as it still looks for libjava_crw_demo_g.so.

* Mon Oct  4 2004 Ville Skyttä <scop at jpackage.org> - 0:1.5.0-2jpp
- Update to 1.5.0, thanks to Carwyn Edwards.
- Fix alternative priority (1500 -> 1503, where "3" is Sun).

* Fri Oct 1 2004 Carwyn Edwards <carwyn@carwyn.com> - 0:1.5.0-0.cte.1
- Added missing Obsoletes for java-1.4.2-plugin.
- Modified release version to use fedora.us style 0. so jpp packages
  will override mine.

* Thu Sep 30 2004 Carwyn Edwards <carwyn@carwyn.com> - 0:1.5.0-1jpp
- Updated to 1.5.0 final.

* Thu Sep 02 2004 Carwyn Edwards <carwyn@carwyn.com> - 0:1.5.0-0.rc.1jpp
- Updated to J2SE 1.5.0 rc.
- Added alternatives slaves for new tools (and their man pages):
  apt, jinfo, jmap, jps, jsadebugd, jstack, jstat and jstatd.

* Mon Aug 02 2004 Carwyn Edwards <carwyn@carwyn.com> - 0:1.5.0-0.beta2.4jpp
- Switch off AutoReq for demo package (breaks on: libjava_crw_demo.so).
- Switch off AutoReqProv for devel package (Provides: lib.so!?).

* Thu Jul 29 2004 Carwyn Edwards <carwyn@carwyn.com> 0:1.5.0-0.beta2.3jpp
- Corrected Requires and BuildRequires for jpackage-utils (1.5.38).

* Sun Jul 25 2004 Carwyn Edwards <carwyn@carwyn.com> - 0:1.5.0-0.beta2.2jpp
- Use %%{_datadir}/xml for XSL's per FHS.
- Change plugin handling to be the same as 1.4.2.05-3jpp(sun)
  (adds firefox support).
- Remove dependency on %%{_bindir}/mozilla.
- Change manpage extension management to be the same as 1.4.2.05-3jpp(sun)
  (also supports uncompressed man pages).
- Rollback javaws alternative location to _datadir location so that concurrent
  jdk installation works again.
- Fixed freedesktop.org menu entry - Exec line was incorrect.
- Corrected the way the jconsole, pack200 and unpack200 man pages were added
  (use macros, added slave links).
- Actaully add jconsole, pack200, unpack200 and their alternatives links.

* Fri Jul 23 2004 Carwyn Edwards <carwyn@carwyn.com> 0:1.5.0-0.beta2.1jpp
- Updated to J2SE 1.5.0 Beta 2.
- Upstream filenames have changed, string replacement: "j2sdk" -> "jdk".
- Remove attempt to copy jre/.systemPrefs (it isn't there any more).
- Added man pages for jconsole, pack200 and unpack200

* Wed Feb 25 2004 David Walluck <david@anti-microsoft.org> 0:1.5.0-0.beta1.3jpp
- remove some unused code from the spec file

* Fri Feb 20 2004 David Walluck <david@anti-microsoft.org> 0:1.5.0-0.beta1.2jpp
- find man extension based on distribution
- ensure correct plugin installation
- Obsoletes: java-1.4.2-fonts
- install java-rmi.cgi
- move ControlPanel back to main so that we can use update-alternatives
- fix ControlPanel, HtmlConverter, and java-rmi.cgi bash scripts
- use included .desktop file for ControlPanel and modify included .desktop file for javaws

* Mon Feb 09 2004 David Walluck <david@anti-microsoft.org> 0:1.5.0-0.beta1.1jpp
- J2SE 1.5.0 Beta 1
- change javaws alternative to point to %%{_bindir}/javaws and only edit
  %%{_sysconfdir}/mime.types if it exists
- add javaws menu into main package (still looking for icon)
- fix installing extensions when %%{version} = %%{javaver}
- add epochs to all requires and provides
- really turn off automatic dependency generation

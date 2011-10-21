# TODO
# - ant contrib dep
#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc

%define		srcname		libbase
%include	/usr/lib/rpm/macros.java
Summary:	JFree Base Services
Name:		java-%{srcname}
Version:	1.1.3
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/jfreereport/%{srcname}-%{version}.zip
# Source0-md5:	83819f19b7338524f4292b86d686e177
Patch0:		build.patch
URL:		http://reporting.pentaho.org/
BuildRequires:	ant
#BuildRequires:	ant-contrib
BuildRequires:	ant-nodeps
BuildRequires:	java-commons-logging
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	java-commons-logging
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibBase is a library developed to provide base services like logging,
configuration and initialization to other libraries and applications.
The library is the root library for all Pentaho-Reporting projects.

%package javadoc
Summary:	Javadoc for LibBase
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
Requires:	jpackage-utils

%description javadoc
Javadoc for LibBase.

%prep
%setup -qc
%patch0 -p1

mkdir -p lib
ln -s %{_javadir}/ant lib/ant-contrib

find -name "*.jar" | xargs rm -v

%build
build-jar-repository -s -p lib commons-logging-api

%ant jar javadoc

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_javadir}
cp -p dist/%{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}
cp -a bin/javadoc/docs/api $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc ChangeLog.txt licence-LGPL.txt README.txt
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif

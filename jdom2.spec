%{?_javapackages_macros:%_javapackages_macros}
Name:          jdom2
Version:       2.0.6
Release:       1.3
Summary:       Java manipulation of XML made easy
Group:         Development/Java
License:       ASL 1.1 or BSD
URL:           https://www.jdom.org/
Source0:       https://github.com/hunterhacker/jdom/archive/JDOM-%{version}.tar.gz
# originally taken from http://repo1.maven.org/maven2/org/jdom/jdom-contrib/1.1.3/jdom-contrib-1.1.3.pom
Source1:       jdom-contrib-template.pom
Source2:       jdom-junit-template.pom
# Use system libraries
# Disable gpg signatures
# Process contrib and junit pom files
Patch0:        jdom-2.0.5-build.patch

BuildRequires: java-devel
BuildRequires: java-javadoc
BuildRequires: javapackages-local
BuildRequires: ant
BuildRequires: ant-junit
BuildRequires: bea-stax-api
BuildRequires: isorelax
BuildRequires: jaxen
BuildRequires: xalan-j2
BuildRequires: xerces-j2
BuildRequires: xml-commons-apis
# coverage deps
BuildRequires: cobertura
#BuildRequires: jakarta-oro
BuildRequires: log4j12
BuildRequires: objectweb-asm3

BuildArch:     noarch

%description
JDOM is a Java-oriented object model which models XML documents.
It provides a Java-centric means of generating and manipulating
XML documents. While JDOM inter-operates well with existing
standards such as the Simple API for XML (SAX) and the Document
Object Model (DOM), it is not an abstraction layer or
enhancement to those APIs. Rather, it seeks to provide a robust,
light-weight means of reading and writing XML data without the
complex and memory-consumptive options that current API
offerings provide.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n jdom-JDOM-%{version}
find . -name "*.class" -print -delete
find . -name "*.jar" -print -delete

%patch0 -p0
#sed -i.asm "s|%{_javadir}/objectweb-asm|%{_javadir}/objectweb-asm3|" build.xml
#sed -i.log4j "s|log4j.jar|log4j12-1.2.17.jar|" build.xml

cp -p %{SOURCE1} maven/contrib.pom
cp -p %{SOURCE2} maven/junit.pom

sed -i 's/\r//' LICENSE.txt README.txt

# Unable to run coverage: use log4j12 but switch to log4j 2.x
sed -i.coverage "s|coverage, jars|jars|" build.xml

%build

ant -Dversion=%{version} -Dj2se.apidoc=%{_javadocdir}/java maven

%install
%mvn_artifact build/maven/core/%{name}-%{version}.pom build/package/jdom-%{version}.jar
%mvn_artifact build/maven/core/%{name}-%{version}-contrib.pom build/package/jdom-%{version}-contrib.jar
%mvn_artifact build/maven/core/%{name}-%{version}-junit.pom build/package/jdom-%{version}-junit.jar
%mvn_install -J build/apidocs

%files -f .mfiles
%dir %{_javadir}/%{name}
%doc CHANGES.txt COMMITTERS.txt LICENSE.txt README.txt TODO.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Tue Oct 21 2014 gil cattaneo <puntogil@libero.it> 2.0.6-1
- update to 2.0.6 (rhbz#1118627)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.0.5-3
- Use Requires: java-headless rebuild (#1067528)

* Thu Nov 14 2013 gil cattaneo <puntogil@libero.it> 2.0.5-2
- use objectweb-asm3

* Thu Sep 12 2013 gil cattaneo <puntogil@libero.it> 2.0.5-1
- initial rpm

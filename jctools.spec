%{?scl:%scl_package jctools}
%{!?scl:%global pkg_name %{name}}

%global namedreltag %nil
%global namedversion %{version}%{?namedreltag}

Name:          %{?scl_prefix}jctools
Version:       1.2.1
Release:       4.1.bs1%{?dist}
Summary:       Java Concurrency Tools for the JVM
License:       ASL 2.0
URL:           http://jctools.github.io/JCTools/
Source0:       https://github.com/JCTools/JCTools/archive/v%{namedversion}/%{pkg_name}-%{namedversion}.tar.gz

BuildRequires: %{?scl_prefix_maven}maven-local
BuildRequires: %{?scl_prefix_maven}mvn(junit:junit)
BuildRequires: %{?scl_prefix_maven}mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires: %{?scl_prefix_maven}mvn(org.hamcrest:hamcrest-all)
BuildRequires: %{?scl_prefix_maven}mvn(org.ow2.asm:asm-all)

BuildArch:     noarch

%description
This project aims to offer some concurrent data structures
currently missing from the JDK:

° SPSC/MPSC/SPMC/MPMC Bounded lock free queues
° SPSC/MPSC Unbounded lock free queues
° Alternative interfaces for queues
° Offheap concurrent ring buffer for ITC/IPC purposes
° Single Writer Map/Set implementations
° Low contention stats counters
° Executor

%package experimental
Summary:       JCTools Experimental implementations

%description experimental
Experimental implementations for the
Java Concurrency Tools Library.

%package javadoc
Summary:       Javadoc for %{pkg_name}

%description javadoc
This package contains javadoc for %{pkg_name}.

%package parent
Summary:       JCTools Parent POM

%description parent
JCTools Parent POM.

%prep
%setup -q -n JCTools-%{namedversion}
# Cleanup
find . -name '*.class' -print -delete
find . -name '*.jar' -print -delete

%pom_xpath_set pom:project/pom:version %{namedversion}
%pom_xpath_set -r pom:parent/pom:version %{namedversion} %{pkg_name}-core %{pkg_name}-experimental

# Prevent build failure
%pom_remove_plugin :maven-enforcer-plugin

# Unavailable deps
%pom_disable_module %{pkg_name}-benchmarks

# Not available
%pom_remove_plugin :cobertura-maven-plugin %{pkg_name}-core

# Useless tasks
%pom_remove_plugin :maven-source-plugin %{pkg_name}-core
%pom_xpath_remove "pom:plugin[pom:artifactId = 'maven-javadoc-plugin']/pom:executions" %{pkg_name}-core

# Add OSGi support
for mod in core experimental; do
 %pom_xpath_set "pom:project/pom:packaging" bundle %{pkg_name}-${mod}
 %pom_add_plugin org.apache.felix:maven-bundle-plugin:2.3.7 %{pkg_name}-${mod} '
 <extensions>true</extensions>
 <executions>
   <execution>
     <id>bundle-manifest</id>
     <phase>process-classes</phase>
     <goals>
       <goal>manifest</goal>
     </goals>
   </execution>
 </executions>
 <configuration>
  <excludeDependencies>true</excludeDependencies>
 </configuration>'
done

%build

%mvn_build -s -f

%install
%mvn_install

%files -f .mfiles-%{pkg_name}-core
%doc README.md
%license LICENSE

%files experimental -f .mfiles-%{pkg_name}-experimental

%files javadoc -f .mfiles-javadoc
%license LICENSE

%files parent -f .mfiles-%{pkg_name}-parent
%license LICENSE

%changelog
* Mon Aug 07 2017 Marek Skalický <mskalick@redhat.com> - 1.2.1-4.1
- Rebuild for rh-maven35 dependency removal

* Mon Jun 26 2017 Marek Skalický <mskalick@redhat.com> - 1.2.1-3.1
- Disable tests

* Fri Jun 23 2017 Michael Simacek <msimacek@redhat.com> - 1.2.1-2.1
- Package import and sclization

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Sep 28 2016 gil cattaneo <puntogil@libero.it> 1.2.1-1
- update to 1.2.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-0.3.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-0.2.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 19 2015 gil cattaneo <puntogil@libero.it> 1.1-0.1.alpha
- initial rpm

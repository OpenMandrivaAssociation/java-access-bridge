%define gcj_support 0

%if %{_use_internal_dependency_generator}
%define __noautoreq 'devel\\((.*)\\)'
%else
%define _requires_exceptions devel.*
%endif

%define javaver 1.6.0.0
%define multilib_arches ppc64 sparc64 x86_64
%ifarch %{multilib_arches}
%define javaname        java-1.6.0-openjdk-%{javaver}.%{_arch}
%else
%define javaname        java-1.6.0-openjdk-%{javaver}
%endif

Summary:	Assistive technology for Java Swing applications
Name:		java-access-bridge
Version:	1.26.2
Release:	12
License:	LGPLv2+
Group:		Development/Java
Url:		http://www.gnome.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%name/java-access-bridge-%{version}.tar.bz2
Source100:	java-access-bridge.rpmlintrc
Patch0:		%{name}-jar_dir.patch
Patch1:		java-1.6.0-openjdk-java-access-bridge-tck.patch
Patch2:		java-1.6.0-openjdk-java-access-bridge-idlj.patch

BuildRequires:	java-1.6.0-openjdk-devel = %{javaver}
BuildRequires:	java-rpmbuild
BuildRequires:	xprop
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libbonobo-2.0)
BuildRequires:	pkgconfig(libspi-1.0)
%if %{gcj_support}
BuildRequires:	java-gcj-compat-devel
%endif

Requires: java-openjdk

%description
This package contains the Java Access Bridge for GNOME, which connects
the built-in accessibility support in Java Swing apps to the GNOME
Accessibility framework, specifically the Assistive Technology Service
Provider Interface (at-spi).

%prep
%setup -q
%apply_patches
autoreconf -ivf

%build
%configure2_5x \
	--disable-static \
	--with-java-home=%{_jvmdir}/java-openjdk
#gw disable parallel make in 1.24.0 to prevent OOM errors
make

%install
%makeinstall_std
(cd %{buildroot}%{_javadir} && mv JNav.jar jnav.jar && ln -s jnav.jar JNav.jar)
(cd %{buildroot}%{_javadir} && for jar in *.jar; do mv ${jar} `/bin/basename ${jar} .jar`-%{version}.jar; done)
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*.jar; do ln -s ${jar} `/bin/echo ${jar} | sed  "s|-%{version}||g"`; done)

mkdir -p %{buildroot}%{_jvmdir}/%{javaname}/jre/lib/ext/
ln -s %{_libdir}/libjava-access-bridge-jni.so %{buildroot}%{_jvmdir}/%{javaname}/jre/lib/ext/

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%update_gcjdb

%postun
%clean_gcjdb
%endif

%files
%doc AUTHORS ChangeLog NEWS README TODO
%attr(0755,root,root) %{_libdir}/libjava-access-bridge-jni.*
%{_jvmdir}/%{javaname}/jre/lib/ext/libjava-access-bridge-jni.so
%{_javadir}/*
%if %{gcj_support}
%{_libdir}/gcj/%{name}
%endif


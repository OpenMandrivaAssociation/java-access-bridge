%define gcj_support 0
%define _requires_exceptions devel.*
%define javaver 1.6.0.0
%define multilib_arches ppc64 sparc64 x86_64
%ifarch %{multilib_arches}
%define javaname        java-1.6.0-openjdk-%javaver.%{_arch}
%else
%define javaname        java-1.6.0-openjdk-%javaver
%endif

Name:           java-access-bridge
Version:        1.26.2
Release:        %mkrel 3
Epoch:          0
Summary:        Assistive technology for Java Swing applications
License:        LGPLv2+
Group:          Development/Java
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:            http://www.gnome.org/
Source0:        ftp://ftp.gnome.org/pub/GNOME/sources/%name/java-access-bridge-%{version}.tar.bz2
Patch0:         %{name}-jar_dir.patch
Patch1:         java-1.6.0-openjdk-java-access-bridge-tck.patch
Patch2:         java-1.6.0-openjdk-java-access-bridge-idlj.patch
BuildRequires:  at-spi-devel
BuildRequires:  java-1.6.0-openjdk-devel = %javaver
BuildRequires:  java-rpmbuild
BuildRequires:  libbonobo2_x-devel
BuildRequires:  xprop
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%endif

%description
This package contains the Java Access Bridge for GNOME, which connects
the built-in accessibility support in Java Swing apps to the GNOME
Accessibility framework, specifically the Assistive Technology Service
Provider Interface (at-spi).

%prep
%setup -q
%patch0 -p1 -b .jar_dir
%patch1 -p1 -b .tck
%patch2 -p1
%{_bindir}/autoreconf -i -v -f

%build
%configure2_5x --with-java-home=%{_jvmdir}/java-openjdk
#gw disable parallel make in 1.24.0 to prevent OOM errors
make

%install
%{__rm} -rf %{buildroot}
%{makeinstall_std}
(cd %{buildroot}%{_javadir} && %{__mv} JNav.jar jnav.jar && %{__ln_s} jnav.jar JNav.jar)
(cd %{buildroot}%{_javadir} && for jar in *.jar; do %{__mv} ${jar} `/bin/basename ${jar} .jar`-%{version}.jar; done)
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*.jar; do %{__ln_s} ${jar} `/bin/echo ${jar} | %{__sed}  "s|-%{version}||g"`; done)

rm -f %buildroot%_libdir/*.a

mkdir -p %buildroot/%_jvmdir/%javaname/jre/lib/ext/
ln -s %_libdir/libjava-access-bridge-jni.so %buildroot/%_jvmdir/%javaname/jre/lib/ext/

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc AUTHORS ChangeLog NEWS README TODO
%_libdir/libjava-access-bridge-jni.*
%_jvmdir/%javaname/jre/lib/ext/libjava-access-bridge-jni.so
%{_javadir}/*
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

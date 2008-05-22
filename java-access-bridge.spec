%define gcj_support 0

Name:           java-access-bridge
Version:        1.22.0
Release:        %mkrel 0.0.1
Epoch:          0
Summary:        Assistive technology for Java Swing applications
License:        GPL
Group:          Development/Java
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:            http://www.gnome.org/
Source0:        ftp://ftp.gnome.org/pub/GNOME/sources/java-access-bridge/1.22/java-access-bridge-%{version}.tar.bz2
Source1:        ftp://ftp.gnome.org/pub/GNOME/sources/java-access-bridge/1.22/java-access-bridge-%{version}.md5sum
Patch0:         %{name}-jar_dir.patch
BuildRequires:  at-spi-devel
BuildRequires:  java-1.6.0-openjdk-devel
BuildRequires:  java-rpmbuild
BuildRequires:  libbonobo2_x-devel
BuildRequires:  xprop
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif

%description
This package contains the Java Access Bridge for GNOME, which connects
the built-in accessibility support in Java Swing apps to the GNOME
Accessibility framework, specifically the Assistive Technology Service
Provider Interface (at-spi).

%prep
%setup -q
%patch0 -p1

%build
%{_bindir}/autoreconf -i -v -f
%{configure2_5x} --with-java-home=%{_jvmdir}/java-openjdk
%{make}

%install
%{__rm} -rf %{buildroot}
%{makeinstall_std}
(cd %{buildroot}%{_javadir} && %{__mv} JNav.jar jnav.jar && %{__ln_s} jnav.jar JNav.jar)
(cd %{buildroot}%{_javadir} && for jar in *.jar; do %{__mv} ${jar} `/bin/basename ${jar} .jar`-%{version}.jar; done)
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*.jar; do %{__ln_s} ${jar} `/bin/echo ${jar} | %{__sed}  "s|-%{version}||g"`; done)

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
%{_javadir}/*
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

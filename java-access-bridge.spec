%define gcj_support 1

Name:           java-access-bridge
Version:        1.19.1
Release:        %mkrel 0.0.1
Epoch:          0
Summary:        Assistive technology for Java Swing applications
License:        GPL
Group:          Development/Java
URL:            http://www.gnome.org/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/java-access-bridge/1.19/java-access-bridge-1.19.1.tar.bz2
Source1:        http://ftp.gnome.org/pub/GNOME/sources/java-access-bridge/1.19/java-access-bridge-1.19.1.md5sum
Patch0:         %{name}-jar_dir.patch
BuildRequires:  at-spi-devel
BuildRequires:  java-1.7.0-icedtea
BuildRequires:  jpackage-utils
BuildRequires:  libbonobo-devel
%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

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
%{configure2_5x} \
        --with-java-home=%{_jvmdir}/java-1.7.0-icedtea
%{make}

%install
%{__rm} -rf %{buildroot}
%{makeinstall_std}

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

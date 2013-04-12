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

Name:		java-access-bridge
Version:	1.26.2
Release:	8
Epoch:		0
Summary:	Assistive technology for Java Swing applications
License:	LGPLv2+
Group:		Development/Java
URL:		http://www.gnome.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%name/java-access-bridge-%{version}.tar.bz2
Source100:	java-access-bridge.rpmlintrc
Patch0:		%{name}-jar_dir.patch
Patch1:		java-1.6.0-openjdk-java-access-bridge-tck.patch
Patch2:		java-1.6.0-openjdk-java-access-bridge-idlj.patch
BuildRequires:	pkgconfig(libspi-1.0)
BuildRequires:	java-1.6.0-openjdk-devel = %{javaver}
BuildRequires:	java-rpmbuild
BuildRequires:	pkgconfig(libbonobo-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	xprop
%if %{gcj_support}
BuildRequires:	java-gcj-compat-devel
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
autoreconf -i -v -f

%build
%configure2_5x \
	--disable-static \
	--with-java-home=%{_jvmdir}/java-openjdk
#gw disable parallel make in 1.24.0 to prevent OOM errors
make

%install
%makeinstall_std
(cd %{buildroot}%{_javadir} && %{__mv} JNav.jar jnav.jar && %{__ln_s} jnav.jar JNav.jar)
(cd %{buildroot}%{_javadir} && for jar in *.jar; do %{__mv} ${jar} `/bin/basename ${jar} .jar`-%{version}.jar; done)
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*.jar; do %{__ln_s} ${jar} `/bin/echo ${jar} | %{__sed}  "s|-%{version}||g"`; done)

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
%defattr(0644,root,root,0755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(0755,root,root) %{_libdir}/libjava-access-bridge-jni.*
%{_jvmdir}/%{javaname}/jre/lib/ext/libjava-access-bridge-jni.so
%{_javadir}/*
%if %{gcj_support}
%{_libdir}/gcj/%{name}
%endif

%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0:1.26.2-4mdv2011.0
+ Revision: 665814
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.26.2-3mdv2011.0
+ Revision: 606068
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.26.2-2mdv2010.1
+ Revision: 523033
- rebuilt for 2010.1

* Tue Jun 09 2009 Götz Waschk <waschk@mandriva.org> 0:1.26.2-1mdv2010.0
+ Revision: 384338
- new version
- rediff patch 1

* Fri Jun 05 2009 Götz Waschk <waschk@mandriva.org> 0:1.26.1-1mdv2010.0
+ Revision: 382963
- update to new version 1.26.1

* Mon Mar 16 2009 Götz Waschk <waschk@mandriva.org> 0:1.26.0-1mdv2009.1
+ Revision: 355633
- new version
- rediff patch 1

* Tue Jan 20 2009 Götz Waschk <waschk@mandriva.org> 0:1.25.1-2mdv2009.1
+ Revision: 331935
- add symlink of the jni lib to the extensions dir

* Tue Jan 20 2009 Götz Waschk <waschk@mandriva.org> 0:1.25.1-1mdv2009.1
+ Revision: 331570
- new version
- rediff patch 1

* Mon Jan 12 2009 Götz Waschk <waschk@mandriva.org> 0:1.25.0-2mdv2009.1
+ Revision: 328486
- filter out devel deps

* Fri Jan 09 2009 Götz Waschk <waschk@mandriva.org> 0:1.25.0-1mdv2009.1
+ Revision: 327526
- new version
- rediff patches 0,1
- it is no longer noarch for the JNI library
- update file list
- fix source URL

* Wed Nov 12 2008 David Walluck <walluck@mandriva.org> 0:1.24.0-1.0.1mdv2009.1
+ Revision: 302579
- add java-1.6.0-openjdk-java-access-bridge-idlj.patch
- run autoreconf in %%prep, not %%build
- fix Source0 URL

* Tue Sep 09 2008 Götz Waschk <waschk@mandriva.org> 0:1.24.0-1mdv2009.0
+ Revision: 282953
- disable parallel make
- new version

* Fri Jul 04 2008 Anssi Hannula <anssi@mandriva.org> 0:1.23.0-2mdv2009.0
+ Revision: 231619
- add tck.patch from fedora

* Thu Jul 03 2008 Götz Waschk <waschk@mandriva.org> 0:1.23.0-1mdv2009.0
+ Revision: 231382
- new version

* Wed Jul 02 2008 Götz Waschk <waschk@mandriva.org> 0:1.22.2-1mdv2009.0
+ Revision: 230827
- new version
- fix license
- remove md5sum file

* Fri May 23 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:1.22.0-0.0.1mdv2009.0
+ Revision: 210154
- fix build for openjdk and disable gcj_support

* Tue Feb 26 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:1.22.0-0.0.1mdv2008.1
+ Revision: 175398
- new version
- try again to fix bonobo BR
- try again to fix the BRs
- another BR fix
- fix BRs

  + Thierry Vignaud <tv@mandriva.org>
    - fix no-buildroot-tag
    - kill re-definition of %%buildroot on Pixel's request

  + Anssi Hannula <anssi@mandriva.org>
    - buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sun Dec 09 2007 David Walluck <walluck@mandriva.org> 0:1.21.1-0.0.2mdv2008.1
+ Revision: 116640
- rebuild
- 1.21.1

* Fri Nov 30 2007 David Walluck <walluck@mandriva.org> 0:1.20.2-0.0.1mdv2008.1
+ Revision: 114131
- 1.20.2

* Fri Oct 12 2007 David Walluck <walluck@mandriva.org> 0:1.20.0-0.0.1mdv2008.1
+ Revision: 97290
- add source
- 1.20.0

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.19.2-0.0.2mdv2008.0
+ Revision: 87423
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sat Aug 18 2007 David Walluck <walluck@mandriva.org> 0:1.19.2-0.0.1mdv2008.0
+ Revision: 65402
- 1.19.2

* Mon Jul 16 2007 David Walluck <walluck@mandriva.org> 0:1.19.1-0.0.1mdv2008.0
+ Revision: 52386
- BuildRequires: xprop
- BuildRequires: java-1.7.0-icedtea-devel, not java-1.7.0-icedtea
- fix java-home setting
- fix jar naming
- define gcj_support
- Import java-access-bridge



* Sun Jul 15 2007 David Walluck <walluck@mandriva.org> 0:1.19.1-0.0.1mdv2008.0
- release

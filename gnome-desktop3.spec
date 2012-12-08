%define oname gnome-desktop

%define	api_version	3
%define api		3.0
%define major		4

%define libname		%mklibname %{oname} %{api_version} %{major}
%define develname	%mklibname -d %{oname} %{api_version}
%define girname		%mklibname %{oname}-gir %{api}

Summary:	Package containing code shared among gnome-panel, gnome-session, nautilus, etc
Name:		%{oname}3
Version:	3.6.2
Release:	1
License:	GPLv2+ and LGPLv2+
Group:		Graphical desktop/GNOME
URL:		http://www.gnome.org
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{oname}/3.6/%{oname}-%{version}.tar.xz

BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	ldetect-lst
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xkbfile)
BuildRequires:	pkgconfig(xkeyboard-config)
BuildRequires:	itstool


Requires:	ldetect-lst >= 0.1.282
Obsoletes:	%{name}-common < 2.91.92
Conflicts:	gnome-desktop-common < 2.32.1-2
%rename 	%{oname}

%description
This package contains some data files and other shared components of the
GNOME user environment.

%package -n %{libname}
Summary:	%{summary}
Group:		System/Libraries
%rename		%{_lib}%{oname}-3_2

%description -n %{libname}
This package contains an internal library
(libgnomedesktop) used to implement some portions of the GNOME
desktop.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{oname}
Group:		System/Libraries

%description -n %{girname}
GObject Introspection interface description for %{oname}.

%package -n %{develname}
Summary:	Development libraries, include files for %{oname}
Group:		Development/GNOME and GTK+
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}

%description -n %{develname}
Development libraries, include files for internal library %{oname}.

%prep
%setup -qn %{oname}-%{version}

%build
%configure2_5x \
	--disable-static \
	--with-gnome-distributor="%_vendor" \
	--disable-scrollkeeper \
	--with-pnp-ids-path=%{_datadir}/misc/pnp.ids

%make LIBS='-lrt -lgmodule-2.0'

%install
%makeinstall_std 
rm -f %{buildroot}%{_libdir}/*.la

%find_lang %{oname}-%{api}
for d in `ls -1 %{buildroot}%{_datadir}/gnome/help/`; do
  %find_lang $d --with-gnome
  cat $d.lang >> %{oname}-%{api}.lang
done

%files -f %{oname}-%{api}.lang
%doc AUTHORS COPYING ChangeLog NEWS README
%{_datadir}/gnome/gnome-version.xml
%{_datadir}/help/*

%files -n %{libname}
%{_libdir}/libgnome-desktop-%{api_version}.so.%{major}*
%{_libdir}/gnome-rr-debug

%files -n %{girname}
%{_libdir}/girepository-1.0/GnomeDesktop-%{api}.typelib

%files -n %{develname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gir-1.0/GnomeDesktop-%{api}.gir
%doc %{_datadir}/gtk-doc/html/*



%changelog
* Tue Nov 13 2012 Arkady L. Shane <ashejn@rosalab.ru> 3.6.2-1
- update to 3.6.2

* Tue Oct 30 2012 Arkady L. Shane <ashejn@rosalab.ru> 3.6.1-1
- update to 3.6.1

* Fri Oct  5 2012 Arkady L. Shane <ashejn@rosalab.ru> 3.6.0.1-1
- update to 3.6.0.1

* Fri Sep 28 2012 Arkady L. Shane <ashejn@rosalab.ru> 3.6.0-1
- update to 3.6.0

* Wed May 16 2012 Matthew Dawkins <mattydaw@mandriva.org> 3.4.2-1
+ Revision: 799250
- update to new version 3.4.2

* Thu Apr 26 2012 Matthew Dawkins <mattydaw@mandriva.org> 3.4.1-1
+ Revision: 793668
- new version 3.4.1

* Tue Mar 27 2012 Matthew Dawkins <mattydaw@mandriva.org> 3.2.1-2
+ Revision: 787820
- rebuild
- obsolete/provide gnome-desktop
- other spec clean ups

* Sat Nov 19 2011 Matthew Dawkins <mattydaw@mandriva.org> 3.2.1-1
+ Revision: 731830
- new version 3.2.1
- syncd spec with mga
- additional cleanups to spec
- splits out gir pkg
- disable static build
- removed mkrel & BuildRoot
- converts BRs to pkgconfig provides
- renamed libnamedev to develname

* Tue May 24 2011 Götz Waschk <waschk@mandriva.org> 3.0.2-1
+ Revision: 678042
- update to new version 3.0.2

* Wed Apr 27 2011 Funda Wang <fwang@mandriva.org> 3.0.1-1
+ Revision: 659521
- update to new version 3.0.1

* Tue Apr 05 2011 Funda Wang <fwang@mandriva.org> 3.0.0-1
+ Revision: 650455
- update to new version 3.0.0

* Sun Apr 03 2011 Funda Wang <fwang@mandriva.org> 2.91.93-2
+ Revision: 650066
- add conflicts with gnome-desktop 2.x

* Fri Mar 25 2011 Funda Wang <fwang@mandriva.org> 2.91.93-1
+ Revision: 648444
- new version 2.91.93

* Wed Mar 23 2011 Funda Wang <fwang@mandriva.org> 2.91.92-1
+ Revision: 648015
- New version 2.91.92 (merge common-i18n into main package)

* Wed Sep 08 2010 Götz Waschk <waschk@mandriva.org> 2.90.5-1mdv2011.0
+ Revision: 576866
- new version
- update file list

* Fri Jul 30 2010 Götz Waschk <waschk@mandriva.org> 2.90.4-1mdv2011.0
+ Revision: 563614
- gtk+3 version
- gtk3 version

* Fri Jul 30 2010 Götz Waschk <waschk@mandriva.org> 2.31.2-2mdv2011.0
+ Revision: 563553
- rebuild
- update to new version 2.31.2

* Sun Jul 11 2010 Götz Waschk <waschk@mandriva.org> 2.30.2-1mdv2011.0
+ Revision: 550681
- update to new version 2.30.2

* Wed Mar 31 2010 Götz Waschk <waschk@mandriva.org> 2.30.0-1mdv2010.1
+ Revision: 530228
- update to new version 2.30.0

* Mon Mar 08 2010 Götz Waschk <waschk@mandriva.org> 2.29.92-1mdv2010.1
+ Revision: 516391
- new version
- drop patch
- update omf file list

* Mon Feb 22 2010 Götz Waschk <waschk@mandriva.org> 2.29.91-1mdv2010.1
+ Revision: 509660
- update to new version 2.29.91

* Tue Feb 09 2010 Götz Waschk <waschk@mandriva.org> 2.29.90-1mdv2010.1
+ Revision: 502987
- update to new version 2.29.90

* Wed Jan 27 2010 Götz Waschk <waschk@mandriva.org> 2.29.6-1mdv2010.1
+ Revision: 497246
- update to new version 2.29.6

* Wed Jan 13 2010 Götz Waschk <waschk@mandriva.org> 2.29.5-1mdv2010.1
+ Revision: 490497
- new version
- new major

* Fri Jan 08 2010 Frederic Crozat <fcrozat@mandriva.com> 2.29.4-2mdv2010.1
+ Revision: 487708
- Remove pnp.ids file, use the one from ldetect-lst now

* Tue Dec 22 2009 Götz Waschk <waschk@mandriva.org> 2.29.4-1mdv2010.1
+ Revision: 481602
- update to new version 2.29.4

* Fri Dec 11 2009 Götz Waschk <waschk@mandriva.org> 2.29.3-2mdv2010.1
+ Revision: 476484
- fix crash in gnome-settings-daemon without xrandr (bug #56349)

* Wed Dec 09 2009 Götz Waschk <waschk@mandriva.org> 2.29.3-1mdv2010.1
+ Revision: 475428
- update to new version 2.29.3

* Thu Oct 22 2009 Frederic Crozat <fcrozat@mandriva.com> 2.28.1-1mdv2010.0
+ Revision: 458860
- Release 2.28.1

* Mon Sep 21 2009 Götz Waschk <waschk@mandriva.org> 2.28.0-1mdv2010.0
+ Revision: 446789
- update to new version 2.28.0

* Thu Sep 10 2009 Götz Waschk <waschk@mandriva.org> 2.27.92-1mdv2010.0
+ Revision: 437223
- update to new version 2.27.92

* Tue Aug 25 2009 Götz Waschk <waschk@mandriva.org> 2.27.91-1mdv2010.0
+ Revision: 421055
- update to new version 2.27.91

* Wed Aug 19 2009 Frederic Crozat <fcrozat@mandriva.com> 2.27.5-2mdv2010.0
+ Revision: 417962
- Remove mandriva.png from pixmaps, it is now shipped by desktop-common-data

* Tue Jul 28 2009 Götz Waschk <waschk@mandriva.org> 2.27.5-1mdv2010.0
+ Revision: 402859
- new version
- update file list
- drop gnomeui dep

* Wed Jul 15 2009 Götz Waschk <waschk@mandriva.org> 2.27.4-1mdv2010.0
+ Revision: 396379
- update to new version 2.27.4

* Tue Jun 16 2009 Götz Waschk <waschk@mandriva.org> 2.27.3-1mdv2010.0
+ Revision: 386339
- update to new version 2.27.3

* Wed May 20 2009 Götz Waschk <waschk@mandriva.org> 2.26.2-1mdv2010.0
+ Revision: 378023
- update to new version 2.26.2

* Tue Apr 14 2009 Götz Waschk <waschk@mandriva.org> 2.26.1-1mdv2009.1
+ Revision: 366928
- update to new version 2.26.1

* Mon Mar 16 2009 Götz Waschk <waschk@mandriva.org> 2.26.0-1mdv2009.1
+ Revision: 356297
- update to new version 2.26.0

* Tue Mar 03 2009 Götz Waschk <waschk@mandriva.org> 2.25.92-1mdv2009.1
+ Revision: 348015
- update to new version 2.25.92

* Tue Feb 17 2009 Götz Waschk <waschk@mandriva.org> 2.25.91-1mdv2009.1
+ Revision: 341222
- update to new version 2.25.91

* Wed Feb 04 2009 Götz Waschk <waschk@mandriva.org> 2.25.90-1mdv2009.1
+ Revision: 337266
- update to new version 2.25.90

* Tue Jan 20 2009 Götz Waschk <waschk@mandriva.org> 2.25.5-1mdv2009.1
+ Revision: 331536
- update to new version 2.25.5

* Tue Jan 06 2009 Götz Waschk <waschk@mandriva.org> 2.25.4-1mdv2009.1
+ Revision: 325312
- update to new version 2.25.4

* Thu Dec 18 2008 Götz Waschk <waschk@mandriva.org> 2.25.3-1mdv2009.1
+ Revision: 315826
- new version
- new major

* Tue Dec 02 2008 Götz Waschk <waschk@mandriva.org> 2.25.2-1mdv2009.1
+ Revision: 309076
- update deps
- update to new version 2.25.2

* Sun Nov 09 2008 Adam Williamson <awilliamson@mandriva.org> 2.25.1.1-2mdv2009.1
+ Revision: 301224
- rebuild for new xcb

* Wed Nov 05 2008 Götz Waschk <waschk@mandriva.org> 2.25.1.1-1mdv2009.1
+ Revision: 300025
- new version
- drop patch
- new major

* Wed Oct 22 2008 Götz Waschk <waschk@mandriva.org> 2.24.1-2mdv2009.1
+ Revision: 296444
- rebuild for broken build system
- update to new version 2.24.1

* Tue Sep 23 2008 Götz Waschk <waschk@mandriva.org> 2.24.0-1mdv2009.0
+ Revision: 287269
- new epiphany

* Mon Sep 08 2008 Götz Waschk <waschk@mandriva.org> 2.23.92-1mdv2009.0
+ Revision: 282802
- new version

* Tue Sep 02 2008 Götz Waschk <waschk@mandriva.org> 2.23.91-1mdv2009.0
+ Revision: 278809
- new version

* Tue Aug 19 2008 Götz Waschk <waschk@mandriva.org> 2.23.90-1mdv2009.0
+ Revision: 273604
- new version

* Tue Aug 05 2008 Götz Waschk <waschk@mandriva.org> 2.23.6-1mdv2009.0
+ Revision: 263697
- new version

* Wed Jul 23 2008 Götz Waschk <waschk@mandriva.org> 2.23.5-1mdv2009.0
+ Revision: 241858
- new version

* Thu Jul 03 2008 Götz Waschk <waschk@mandriva.org> 2.23.4-1mdv2009.0
+ Revision: 231019
- new version
- new version

* Mon Jun 30 2008 Götz Waschk <waschk@mandriva.org> 2.22.3-1mdv2009.0
+ Revision: 230187
- new version
- update license
- update buildrequires

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue May 27 2008 Götz Waschk <waschk@mandriva.org> 2.22.2-1mdv2009.0
+ Revision: 211637
- new version
- fix build

* Wed Mar 26 2008 Emmanuel Andry <eandry@mandriva.org> 2.22.0-2mdv2008.1
+ Revision: 190526
- Fix lib group

* Mon Mar 10 2008 Götz Waschk <waschk@mandriva.org> 2.22.0-1mdv2008.1
+ Revision: 183856
- new version

* Tue Feb 26 2008 Götz Waschk <waschk@mandriva.org> 2.21.92-1mdv2008.1
+ Revision: 175483
- new version

* Mon Feb 11 2008 Götz Waschk <waschk@mandriva.org> 2.21.91-1mdv2008.1
+ Revision: 165444
- fix rpmlint error
- new version

* Mon Jan 28 2008 Götz Waschk <waschk@mandriva.org> 2.21.90-1mdv2008.1
+ Revision: 159048
- new version

* Tue Jan 15 2008 Götz Waschk <waschk@mandriva.org> 2.21.5-1mdv2008.1
+ Revision: 152168
- fix buildrequires
- new version

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Tue Dec 18 2007 Götz Waschk <waschk@mandriva.org> 2.21.4-1mdv2008.1
+ Revision: 132902
- new version
- drop patch 2

* Tue Dec 18 2007 Frederic Crozat <fcrozat@mandriva.com> 2.21.2-2mdv2008.1
+ Revision: 132449
- Patch2 (Fedora): add gnome-bg API

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Nov 14 2007 Götz Waschk <waschk@mandriva.org> 2.21.2-1mdv2008.1
+ Revision: 108622
- new version

* Mon Oct 15 2007 Götz Waschk <waschk@mandriva.org> 2.20.1-1mdv2008.1
+ Revision: 98699
- new version

* Tue Sep 18 2007 Frederic Crozat <fcrozat@mandriva.com> 2.20.0-1mdv2008.0
+ Revision: 89566
- Move mo files to a new sub-package

  + Götz Waschk <waschk@mandriva.org>
    - new version

* Wed Sep 05 2007 Götz Waschk <waschk@mandriva.org> 2.19.92-1mdv2008.0
+ Revision: 79721
- new version

* Tue Aug 14 2007 Götz Waschk <waschk@mandriva.org> 2.19.90-1mdv2008.0
+ Revision: 63283
- new version
- fix buildrequires

* Wed Aug 01 2007 Götz Waschk <waschk@mandriva.org> 2.19.6-2mdv2008.0
+ Revision: 57354
- new devel name
- use scrollkeeper macros

* Mon Jul 30 2007 Götz Waschk <waschk@mandriva.org> 2.19.6-1mdv2008.0
+ Revision: 56735
- fix buildrequires
- new version

* Sun Jul 08 2007 Götz Waschk <waschk@mandriva.org> 2.19.5-1mdv2008.0
+ Revision: 49947
- new version

* Sun Jun 17 2007 Götz Waschk <waschk@mandriva.org> 2.19.4-1mdv2008.0
+ Revision: 40612
- new version
- bump deps

* Wed Jun 06 2007 Götz Waschk <waschk@mandriva.org> 2.19.3.1-1mdv2008.0
+ Revision: 36005
- new version

* Mon May 28 2007 Götz Waschk <waschk@mandriva.org> 2.18.2-1mdv2008.0
+ Revision: 32121
- new version

* Wed Apr 18 2007 Götz Waschk <waschk@mandriva.org> 2.18.1-1mdv2008.0
+ Revision: 14402
- new version


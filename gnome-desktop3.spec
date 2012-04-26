%define oname gnome-desktop

%define	api_version	3
%define api		3.0
%define major	2

%define libname		%mklibname %{oname} %{api_version} %{major}
%define develname	%mklibname -d %{oname} %{api_version}
%define girname		%mklibname %{oname}-gir %{api}

Summary:	Package containing code shared among gnome-panel, gnome-session, nautilus, etc
Name:		%{oname}3
Version:	3.4.1
Release:	1
License:	GPLv2+ and LGPLv2+
Group:		Graphical desktop/GNOME
URL:		http://www.gnome.org
Source0:	http://download.gnome.org/sources/%{oname}/3.2/%{oname}-%{version}.tar.xz

BuildRequires:	gnome-doc-utils
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	ldetect-lst
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gsettings-desktop-schemas)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xrandr)

Requires:	ldetect-lst >= 0.1.282
Obsoletes:	%{name}-common < 2.91.92
Conflicts:	gnome-desktop-common < 2.32.1-2
%rename %{oname}

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

%files -n %{libname}
%{_libdir}/libgnome-desktop-%{api_version}.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/GnomeDesktop-%{api}.typelib

%files -n %{develname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gir-1.0/GnomeDesktop-%{api}.gir
%doc %{_datadir}/gtk-doc/html/*


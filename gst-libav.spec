%define	api	1.0
%define	bname	gstreamer%{api}

Summary:	Gstreamer plugin for the libav codec
Name:		gst-libav
Version:	1.6.3
Release:	2
License:	GPLv2+
Group:		Video
Url:		http://www.gstreamer.net
Source0:	http://gstreamer.freedesktop.org/src/gst-libav/%{name}-%{version}.tar.xz
Patch1:		0001-avdeinterlace-Port-non-deprecated-AVFilter-API.patch
Patch2:		0002-libav-Remove-usage-of-deprecated-API.patch
Patch3:		0003-libav-Bitrate-field-changed-from-int-to-int64_t-fix-.patch
Patch4:		0004-avdeinterlace-Chain-up-to-parent-class-dispose.patch
%ifnarch %{arm} %{mips}
BuildRequires:	valgrind
%endif
BuildRequires:	yasm
BuildRequires:	bzip2-devel
BuildRequires:	pkgconfig(check)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gstreamer-plugins-base-%{api})
BuildRequires:	pkgconfig(orc-0.4)
BuildRequires:	ffmpeg-devel

%description
Video codec plugin for GStreamer based on the libav libraries.

%package -n %{bname}-libav
Summary:	Gstreamer plugin for the libav codec
Group:		Video

%description -n %{bname}-libav
Video codec plugin for GStreamer based on the libav libraries.

%prep
%setup -q
%apply_patches

%build
%ifarch %arm
export CC=gcc
export CXX=g++
%endif

%configure \
	--with-package-name='OpenMandriva %{name} package' \
	--with-package-origin="%{disturl}" \
	--with-libav-extra-configure='--disable-decoder=mp3 \
	--disable-decoder=mp3on4 \
	--disable-decoder=mp3adu \
	--disable-demuxer=mp3 \
	--disable-demuxer=asf' \
	--with-system-libav

%make

%install
%makeinstall_std

rm -fr %{buildroot}%{_datadir}/gtk-doc

%files -n %{bname}-libav
%doc README NEWS TODO ChangeLog AUTHORS
%{_libdir}/gstreamer-%{api}/libgstlibav.so


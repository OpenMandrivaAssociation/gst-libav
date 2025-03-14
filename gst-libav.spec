# Work around incomplete debug packages
%undefine _debugsource_packages

%define api 1.0
%define bname gstreamer%{api}

Summary:	Gstreamer plugin for the libav codec
Name:		gst-libav
Version:	1.26.0
Release:	1
License:	GPLv2+
Group:		Video
Url:		https://www.gstreamer.net
Source0:	https://gstreamer.freedesktop.org/src/gst-libav/%{name}-%{version}.tar.xz
Source1:	gst-libav.rpmlintrc
#Patch1:		gst-libav-1.24.2-ffmpeg7.patch
# remove probe which is invalid in ffmpeg7
# see https://gitlab.freedesktop.org/gstreamer/gstreamer/-/merge_requests/6505
#Patch2:		6505.diff
%ifnarch %{armx} %{mips}
BuildRequires: valgrind
%endif
BuildRequires: yasm
BuildRequires: pkgconfig(bzip2)
BuildRequires: pkgconfig(check)
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(gstreamer-plugins-base-%{api})
BuildRequires: pkgconfig(orc-0.4)
BuildRequires: ffmpeg-devel
BuildRequires: git-core
BuildRequires:  meson

%description
Video codec plugin for GStreamer based on the libav libraries.

%package -n %{bname}-libav
Summary:	Gstreamer plugin for the libav codec
Group:		Video

%description -n %{bname}-libav
Video codec plugin for GStreamer based on the libav libraries.

%prep
%autosetup -p1
# get rid of the bundled libav
rm -rf gst-libs/ext/libav
# fool configure to see a bundled libav/ffmpeg
#mkdir gst-libs/ext/libav
#ln -s /bin/true gst-libs/ext/libav/configure

%build
export CFLAGS="$CFLAGS -Wno-implicit-function-declaration -Wno-deprecated-declarations"
%meson \
       -Ddoc=disabled \
       --buildtype=release

%meson_build

%install
%meson_install

rm -fr %{buildroot}%{_datadir}/gtk-doc

%files -n %{bname}-libav
%doc README.md NEWS ChangeLog AUTHORS
%{_libdir}/gstreamer-%{api}/libgstlibav.so

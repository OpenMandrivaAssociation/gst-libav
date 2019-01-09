%define api 1.0
%define bname gstreamer%{api}

Summary:	Gstreamer plugin for the libav codec
Name:		gst-libav
Version:	1.14.4
Release:	3
License:	GPLv2+
Group:		Video
Url:		http://www.gstreamer.net
Source0:	http://gstreamer.freedesktop.org/src/gst-libav/%{name}-%{version}.tar.xz
Source1:	gst-libav.rpmlintrc
# This is essentially a backport of the current (20190109)
# master ext/libav directory
Patch0:		gst-libav-1.14.4-ffmpeg-4.1.patch
%ifnarch %{armx} %{mips}
BuildRequires:	valgrind
%endif
BuildRequires:	yasm
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	pkgconfig(check)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gstreamer-plugins-base-%{api})
BuildRequires:	pkgconfig(orc-0.4)
BuildRequires:	ffmpeg-devel
BuildRequires:	git-core
BuildRequires:	gtk-doc

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
mkdir gst-libs/ext/libav
touch gst-libs/ext/libav/configure

# (re)generate autofoo using our autotools
./autogen.sh

%build
%ifarch %arm
export CC=gcc
export CXX=g++
export CFLAGS="$CFLAGS -Wno-implicit-function-declaration -Wno-deprecated-declarations"
%endif
export CFLAGS="$CFLAGS -Wno-implicit-function-declaration -Wno-deprecated-declarations"
%configure \
	--with-package-name='OpenMandriva %{name} package' \
	--with-package-origin="%{disturl}" \
	--disable-fatal-warnings \
	--disable-decoder=mp3on4 \
	--disable-decoder=mp3adu \
	--disable-demuxer=mp3 \
	--disable-demuxer=asf' \
	--with-system-libav \
	--disable-gtk-doc \
	--disable-gtk-doc-html

%make_build

%install
%make_install

rm -fr %{buildroot}%{_datadir}/gtk-doc

%files -n %{bname}-libav
%doc README NEWS TODO ChangeLog AUTHORS
%{_libdir}/gstreamer-%{api}/libgstlibav.so


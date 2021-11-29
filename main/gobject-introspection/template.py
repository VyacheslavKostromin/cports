pkgname = "gobject-introspection"
_mver = "1.70"
pkgver = f"{_mver}.0"
pkgrel = 0
build_style = "meson"
hostmakedepends = ["meson", "pkgconf", "flex", "bison"]
makedepends = [
    "libffi-devel", "libglib-devel", "python-devel",
    "python-mako", "python-markdown"
]
depends = ["libgirepository-devel", "python-mako", "python-markdown"]
pkgdesc = "Introspection system for GObject-based libraries"
maintainer = "q66 <q66@chimera-linux.org>"
license = "GPL-2.0-or-later AND LGPL-2.1-or-later"
url = "https://wiki.gnome.org/Projects/GObjectIntrospection"
source = f"$(GNOME_SITE)/{pkgname}/{_mver}/{pkgname}-{pkgver}.tar.xz"
sha256 = "902b4906e3102d17aa2fcb6dad1c19971c70f2a82a159ddc4a94df73a3cafc4a"
# check creates a dependency cycle
# cross compiling tons of janky hackery
options = ["!check", "!cross", "lto"]

pycompile_dirs = [f"usr/lib/{pkgname}/giscanner"]

def post_install(self):
    for f in (
        self.destdir / f"usr/lib/{pkgname}/giscanner"
    ).glob("_giscanner*.so"):
        self.mv(f, f.with_name("_giscanner.so"))

@subpackage("gir-freedesktop")
def _girfdo(self):
    self.pkgdesc = "Introspection data for some freedesktop components"

    return ["usr/lib/girepository-1.0"]

@subpackage("libgirepository")
def _libgir(self):
    self.pkgdesc = "Library for handling gir data (runtime library)"

    return self.default_libs()

@subpackage("libgirepository-devel")
def _devel(self):
    self.depends += ["cairo-devel", "libffi-devel"]
    self.pkgdesc = "Library for handling gir data (development files)"

    return self.default_devel()

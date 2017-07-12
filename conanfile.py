from conans import ConanFile, CMake, tools
import os

class LibtinsConan(ConanFile):
    name = "libtins"
    version = "3.5"
    license = "BSD-2"
    url = "https://github.com/appanywhere/conan-libtins"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        self.run("git clone git@github.com:mfontanini/libtins.git")
        
    def build(self):
        cmake = CMake(self)
        shared = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else ""
        self.run("mkdir build && cd build && cmake .." % (cmake.command_line, shared))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        # self.copy("*.h", dst="include", src="hello")
        # self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["libtins"]

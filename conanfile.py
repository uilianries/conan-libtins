from conans import ConanFile, CMake, tools
import os


class LibtinsConan(ConanFile):
    name = "libtins"
    version = "3.5"
    author = "AppAnyWhere.io"
    description = "High-level, multiplatform C++ network packet sniffing and crafting library"
    license = "https://github.com/mfontanini/libtins/blob/master/LICENSE"
    url = "https://github.com/appanywhere/conan-libtins"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "enable_pcap": [True, False],
        "enable_cxx11": [True, False],
        "enable_dot11": [True, False],
        "enable_wpa2": [True, False],
        "enable_tcpip": [True, False],
        "enable_ack_tracker": [True, False],
        "enable_tcp_stream_custom_data": [True, False]
    }
    default_options = "shared=True", "enable_pcap=True", "enable_cxx11=True", "enable_dot11=True", "enable_wpa2=True", "enable_tcpip=True", "enable_ack_tracker=True", "enable_tcp_stream_custom_data=True"
    generators = "cmake"
    exports = "LICENSE"

    def requirements(self):
        if self.options.enable_wpa2:
            self.requires.add("OpenSSL/1.0.2l@conan/stable")
        if self.options.enable_ack_tracker or self.options.enable_tcp_stream_custom_data:
            self.requires.add("Boost/1.64.0@inexorgame/stable")

    def system_requirements(self):
        if self.settings.os == "Linux" and self.options.enable_pcap:
            package_tool = tools.SystemPackageTool()
            package_tool.install("libpcap-dev")

    def source(self):
        tar_name = "v%s.tar.gz" % self.version
        tools.download("https://github.com/mfontanini/libtins/archive/%s" % tar_name, tar_name)
        tools.check_md5(tar_name, "be029088c9fc8dc979022410b49a8e61")
        tools.unzip(tar_name)
        os.unlink(tar_name)

    def build(self):
        conan_magic_lines = '''PROJECT(libtins)
include(../conanbuildinfo.cmake)
CONAN_BASIC_SETUP()
'''
        libtins_dir = "%s-%s" % (self.name, self.version)
        tools.replace_in_file("%s/CMakeLists.txt" % libtins_dir,
                              "PROJECT(libtins)", conan_magic_lines)
        cmake = CMake(self)
        cmake.definitions["LIBTINS_BUILD_SHARED"] = self.options.shared
        cmake.definitions["LIBTINS_ENABLE_PCAP"] = self.options.enable_pcap
        cmake.definitions["LIBTINS_ENABLE_CXX11"] = self.options.enable_cxx11
        cmake.definitions["LIBTINS_ENABLE_DOT11"] = self.options.enable_dot11
        cmake.definitions["LIBTINS_ENABLE_WPA2"] = self.options.enable_wpa2
        cmake.definitions["LIBTINS_ENABLE_TCPIP"] = self.options.enable_tcpip
        cmake.definitions["LIBTINS_ENABLE_ACK_TRACKER"] = self.options.enable_ack_tracker
        cmake.definitions["LIBTINS_ENABLE_TCP_STREAM_CUSTOM_DATA"] = self.options.enable_tcp_stream_custom_data
        cmake.configure(source_dir=libtins_dir)
        cmake.build()

    def package(self):
        self.copy("LICENSE", dst=".", keep_path=False)
        self.copy("*.h", dst="include", src=os.path.join("libtins-%s" % self.version, "include"))
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so*", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = self.collect_libs()
        if self.settings.os == "Linux" and self.options.enable_pcap:
            self.cpp_info.libs.extend(["pcap", "pthread"])

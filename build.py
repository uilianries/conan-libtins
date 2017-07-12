from conan.packager import ConanMultiPackager


if __name__ == "__main__":
    # Boost is not built
    builder = ConanMultiPackager(args="--build missing")
    ConanMultiPackager()
    builder.add_common_builds()
    builder.run()

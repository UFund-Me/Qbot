load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "rules_python",
    sha256 = "c03246c11efd49266e8e41e12931090b613e12a59e6f55ba2efd29a7cb8b4258",
    strip_prefix = "rules_python-0.11.0",
    url = "https://github.com/bazelbuild/rules_python/archive/refs/tags/0.11.0.tar.gz",
)

load("@rules_python//python:pip.bzl", "pip_install")
load("@rules_python//python:repositories.bzl", "python_register_toolchains")

# Use a hermetic Python interpreter so that builds are reproducible
# irrespective of the Python version available on the host machine.
python_register_toolchains(
    name = "python3_10",
    python_version = "3.10",
)

load("@python3_10//:defs.bzl", "interpreter")

# Translate requirements.txt into a @third_party external repository.
pip_install(
    name = "third_party",
    python_interpreter_target = interpreter,
    requirements = "//third_party:requirements.txt",
)

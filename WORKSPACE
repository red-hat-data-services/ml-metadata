workspace(name = "ml_metadata")

load("//ml_metadata:repo.bzl", "clean_dep")
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "postgresql",
    build_file = "//ml_metadata:postgresql.BUILD",
    workspace_file_content = "//ml_metadata:postgresql.WORKSPACE",
    sha256 = "1cb8e3a59861be5175878159fc3a41240c379e9aabaabba8288e6cfd6980fff0",
    patches = ["//ml_metadata/third_party:postgresql.patch"],
    strip_prefix = "postgresql-12.17",
    urls = [
        "https://ftp.postgresql.org/pub/source/v12.17/postgresql-12.17.tar.gz",
    ],
)

# Install bazel platform version 0.0.10 (required for Bazel 6+).
http_archive(
    name = "platforms",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/platforms/releases/download/0.0.10/platforms-0.0.10.tar.gz",
        "https://github.com/bazelbuild/platforms/releases/download/0.0.10/platforms-0.0.10.tar.gz",
    ],
    sha256 = "218efe8ee736d26a3572663b374a253c012b716d8af0c07e842e82f238a0a7ee",
)

# Install version 0.9.0 of rules_foreign_cc, as default version causes an
# invalid escape sequence error to be raised, which can't be avoided with
# the --incompatible_restrict_string_escapes=false flag (flag was removed in
# Bazel 5.0).
RULES_FOREIGN_CC_VERSION = "0.9.0"
http_archive(
    name = "rules_foreign_cc",
    sha256 = "2a4d07cd64b0719b39a7c12218a3e507672b82a97b98c6a89d38565894cf7c51",
    strip_prefix = "rules_foreign_cc-%s" % RULES_FOREIGN_CC_VERSION,
    url = "https://github.com/bazelbuild/rules_foreign_cc/archive/refs/tags/%s.tar.gz" % RULES_FOREIGN_CC_VERSION,
    patch_tool = "patch",
    patches = ["//ml_metadata/third_party:rules_foreign_cc.patch",],
)

load("@rules_foreign_cc//foreign_cc:repositories.bzl", "rules_foreign_cc_dependencies")
rules_foreign_cc_dependencies()

http_archive(
    name = "com_google_absl",
    sha256 = "59d2976af9d6ecf001a81a35749a6e551a335b949d34918cfade07737b9d93c5",
    strip_prefix = "abseil-cpp-20230802.0",
    urls = [
        "https://github.com/abseil/abseil-cpp/archive/refs/tags/20230802.0.tar.gz"
    ],
)

http_archive(
    name = "boringssl",
    sha256 = "579cb415458e9f3642da0a39a72f79fdfe6dc9c1713b3a823f1e276681b9703e",
    strip_prefix = "boringssl-648cbaf033401b7fe7acdce02f275b06a88aab5c",
    urls = [
        "https://github.com/google/boringssl/archive/648cbaf033401b7fe7acdce02f275b06a88aab5c.tar.gz",
    ],
)

http_archive(
    name = "org_sqlite",
    build_file = clean_dep("//ml_metadata/third_party:sqlite.BUILD"),
    sha256 = "aa73d8748095808471deaa8e6f34aa700e37f2f787f4425744f53fdd15a89c40",
    strip_prefix = "sqlite-amalgamation-3470200",
    urls = [
        "https://www.sqlite.org/2024/sqlite-amalgamation-3470200.zip",
    ],
)

http_archive(
    name = "com_google_googletest",
    sha256 = "7b42b4d6ed48810c5362c265a17faebe90dc2373c885e5216439d37927f02926",
    strip_prefix = "googletest-1.15.2",
    urls = ["https://github.com/google/googletest/archive/refs/tags/v1.15.2.tar.gz"],
)

http_archive(
    name = "com_google_glog",
    build_file = clean_dep("//ml_metadata/third_party:glog.BUILD"),
    strip_prefix = "glog-96a2f23dca4cc7180821ca5f32e526314395d26a",
    urls = [
      "https://github.com/google/glog/archive/96a2f23dca4cc7180821ca5f32e526314395d26a.zip",
    ],
    sha256 = "6281aa4eeecb9e932d7091f99872e7b26fa6aacece49c15ce5b14af2b7ec050f",
)

http_archive(
    name = "bazel_skylib",
    sha256 = "97e70364e9249702246c0e9444bccdc4b847bed1eb03c5a3ece4f83dfe6abc44",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/bazel-skylib/releases/download/1.0.2/bazel-skylib-1.0.2.tar.gz",
        "https://github.com/bazelbuild/bazel-skylib/releases/download/1.0.2/bazel-skylib-1.0.2.tar.gz",
    ],
)

# Needed by abseil-py by zetasql.
http_archive(
    name = "six_archive",
    urls = [
        "http://mirror.bazel.build/pypi.python.org/packages/source/s/six/six-1.10.0.tar.gz",
        "https://pypi.python.org/packages/source/s/six/six-1.10.0.tar.gz",
    ],
    sha256 = "105f8d68616f8248e24bf0e9372ef04d3cc10104f1980f54d57b2ce73a5ad56a",
    strip_prefix = "six-1.10.0",
    build_file = "//ml_metadata/third_party:six.BUILD"
)

# gRPC 1.58.3 (CVE-2024-7246) with protobuf 23.4 per grpc v1.58.3 grpc_deps.bzl.
http_archive(
    name = "com_github_grpc_grpc",
    urls = ["https://github.com/grpc/grpc/archive/refs/tags/v1.58.3.tar.gz"],
    sha256 = "db820756bdb6b5f247786a0bf2df72299c8a9725fc00fe627a447a6b6482f921",
    strip_prefix = "grpc-1.58.3",
)

# Register upb before protobuf_deps() without protobuf's upb.patch, which breaks
# external upb builds (-Isrc vs -Iexternal/com_google_protobuf/src).
http_archive(
    name = "upb",
    sha256 = "c29fbd26eb19f388a1894099fae5ae599210be22926e1e1694c0ed1284f1c151",
    strip_prefix = "upb-455cfdb8ae60a1763e6d924e36851c6897a781bb",
    urls = [
        "https://github.com/protocolbuffers/upb/archive/455cfdb8ae60a1763e6d924e36851c6897a781bb.tar.gz",
    ],
)

http_archive(
    name = "com_google_protobuf",
    sha256 = "76a33e2136f23971ce46c72fd697cd94dc9f73d56ab23b753c3e16854c90ddfd",
    strip_prefix = "protobuf-2c5fa078d8e86e5f4bd34e6f4c9ea9e8d7d4d44a",
    urls = [
        "https://github.com/protocolbuffers/protobuf/archive/2c5fa078d8e86e5f4bd34e6f4c9ea9e8d7d4d44a.tar.gz",
    ],
    patches = [
        "@com_github_grpc_grpc//third_party:protobuf.patch",
    ],
    patch_args = ["-p1"],
)

load("@com_google_protobuf//:protobuf_deps.bzl", "protobuf_deps")

protobuf_deps()

# Needed by Protobuf.
http_archive(
    name = "zlib",
    build_file = "@com_google_protobuf//:third_party/zlib.BUILD",
    sha256 = "9a93b2b7dfdac77ceba5a558a580e74667dd6fede4585b91eefb60f03b72df23",
    strip_prefix = "zlib-1.3.1",
    urls = ["https://github.com/madler/zlib/releases/download/v1.3.1/zlib-1.3.1.tar.gz"],
)

http_archive(
    name = "pybind11_bazel",
    strip_prefix = "pybind11_bazel-faf56fb3df11287f26dbc66fdedf60a2fc2c6631",
    urls = ["https://github.com/pybind/pybind11_bazel/archive/faf56fb3df11287f26dbc66fdedf60a2fc2c6631.tar.gz"],
    sha256 = "a2b107b06ffe1049696e132d39987d80e24d73b131d87f1af581c2cb271232f8",
)

http_archive(
    name = "pybind11",
    urls = [
        "https://github.com/pybind/pybind11/archive/v2.10.1.tar.gz",
    ],
    strip_prefix = "pybind11-2.10.1",
    build_file = "@pybind11_bazel//:pybind11.BUILD",
)

load("@pybind11_bazel//:python_configure.bzl", "python_configure")
python_configure(name = "local_config_python")

# Needed by @com_google_protobuf.
bind(
    name = "python_headers",
    actual = "@local_config_python//:python_headers",
)

# Note - use @com_github_google_re2 instead of more canonical
#        @com_google_re2 for consistency with dependency grpc
#        which uses @com_github_google_re2.
#          (see https://github.com/google/xls/issues/234)
http_archive(
    name = "com_googlesource_code_re2",
    sha256 = "ef516fb84824a597c4d5d0d6d330daedb18363b5a99eda87d027e6bdd9cba299",
    strip_prefix = "re2-03da4fc0857c285e3a26782f6bc8931c4c950df4",
    urls = [
        "https://storage.googleapis.com/mirror.tensorflow.org/github.com/google/re2/archive/03da4fc0857c285e3a26782f6bc8931c4c950df4.tar.gz",
        "https://github.com/google/re2/archive/03da4fc0857c285e3a26782f6bc8931c4c950df4.tar.gz",
    ],
)

load("@com_github_grpc_grpc//bazel:grpc_deps.bzl", "grpc_deps")
grpc_deps()

load("@com_github_grpc_grpc//bazel:grpc_extra_deps.bzl", "grpc_extra_deps")
grpc_extra_deps()

# Needed by Protobuf.
bind(
    name = "grpc_python_plugin",
    actual = "@com_github_grpc_grpc//src/compiler:grpc_python_plugin",
)

# Needed by Protobuf.
bind(
    name = "grpc_lib",
    actual = "@com_github_grpc_grpc//:grpc++",
)

# Needed by gRPC.
http_archive(
    name = "build_bazel_rules_swift",
    sha256 = "d0833bc6dad817a367936a5f902a0c11318160b5e80a20ece35fb85a5675c886",
    strip_prefix = "rules_swift-3eeeb53cebda55b349d64c9fc144e18c5f7c0eb8",
    urls = ["https://github.com/bazelbuild/rules_swift/archive/3eeeb53cebda55b349d64c9fc144e18c5f7c0eb8.tar.gz"],
)

http_archive(
    name = "io_bazel_rules_go",
    urls = [
        "https://storage.googleapis.com/bazel-mirror/github.com/bazelbuild/rules_go/releases/download/v0.20.3/rules_go-v0.20.3.tar.gz",
        "https://github.com/bazelbuild/rules_go/releases/download/v0.20.3/rules_go-v0.20.3.tar.gz",
    ],
    sha256 = "e88471aea3a3a4f19ec1310a55ba94772d087e9ce46e41ae38ecebe17935de7b",
)

load("@io_bazel_rules_go//go:deps.bzl", "go_rules_dependencies", "go_register_toolchains")

http_archive(
    name = "bazel_gazelle",
    urls = [
        "https://storage.googleapis.com/bazel-mirror/github.com/bazelbuild/bazel-gazelle/releases/download/v0.19.1/bazel-gazelle-v0.19.1.tar.gz",
        "https://github.com/bazelbuild/bazel-gazelle/releases/download/v0.19.1/bazel-gazelle-v0.19.1.tar.gz",
    ],
    sha256 = "86c6d481b3f7aedc1d60c1c211c6f76da282ae197c3b3160f54bd3a8f847896f",
)

load("@bazel_gazelle//:deps.bzl", "go_repository", "gazelle_dependencies")

go_repository(
    name = "org_golang_x_sys",
    commit = "57f5ac02873b2752783ca8c3c763a20f911e4d89",
    importpath = "golang.org/x/sys",
)

go_repository(
    name = "com_github_google_go_cmp",
    importpath = "github.com/google/go-cmp",
    tag = "v0.2.0",
)

go_rules_dependencies()

go_register_toolchains()

gazelle_dependencies()

# For commandline flags used in gRPC server
# gflags needed by glog
http_archive(
    name = "com_github_gflags_gflags",
    strip_prefix = "gflags-a738fdf9338412f83ab3f26f31ac11ed3f3ec4bd",
    sha256 = "017e0a91531bfc45be9eaf07e4d8fed33c488b90b58509dbd2e33a33b2648ae6",
    url = "https://github.com/gflags/gflags/archive/a738fdf9338412f83ab3f26f31ac11ed3f3ec4bd.zip",
)

# UBI9-compatible ZetaSQL (protobuf 23 patch in ml_metadata/third_party/zetasql.patch)
ZETASQL_COMMIT = "f764f4e986ac1516ab5ae95e6d6ce2f4416cc6ff" # 02/03/2023
http_archive(
    name = "com_google_zetasql",
    urls = ["https://github.com/google/zetasql/archive/%s.zip" % ZETASQL_COMMIT],
    strip_prefix = "googlesql-%s" % ZETASQL_COMMIT,
    patches = ["//ml_metadata/third_party:zetasql.patch"],
    sha256 = 'afb6b1673d680e0ae7b21b6b119b0d4c8cce41b075358f87a0d7ad815c2b865d'
)

# Older UBI8/Fedora39 pin (no protobuf 23 patch):
# ZETASQL_COMMIT = "ac37cf5c0d80b5605176fc0f29e87b12f00be693" # 08/10/2022
# http_archive(
#     name = "com_google_zetasql",
#     urls = ["https://github.com/google/zetasql/archive/%s.zip" % ZETASQL_COMMIT],
#     strip_prefix = "googlesql-%s" % ZETASQL_COMMIT,
#     sha256 = '86f81591ab5ec20457a5394eb2c5c981e6f6c89f4c49c211d096c3acffec1eb1'
# )

load("@com_google_zetasql//bazel:zetasql_deps_step_1.bzl", "zetasql_deps_step_1")
zetasql_deps_step_1()
load("@com_google_zetasql//bazel:zetasql_deps_step_2.bzl", "zetasql_deps_step_2")
zetasql_deps_step_2(
    analyzer_deps = True,
    evaluator_deps = True,
    tools_deps = False,
    java_deps = False,
    testing_deps = False)

# This is part of what zetasql_deps_step_3() does.
load("@com_google_googleapis//:repository_rules.bzl", "switched_rules_by_language")
switched_rules_by_language(
    name = "com_google_googleapis_imports",
    cc = True,
)



# Please add all new ML Metadata dependencies in workspace.bzl.
load("//ml_metadata:workspace.bzl", "ml_metadata_workspace")

ml_metadata_workspace()

# Specify the minimum required bazel version.
load("@bazel_skylib//lib:versions.bzl", "versions")
versions.check("6.3.2")

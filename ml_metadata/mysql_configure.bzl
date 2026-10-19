# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Pulls mariadb-connector-c github repo and builds it.

Clients can then depend on `@libmysqlclient` to use the MYSQL C API.
"""

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

def mysql_configure():
    http_archive(
        name = "libmysqlclient",
        build_file = "//ml_metadata:libmysqlclient.BUILD",
        workspace_file = "//ml_metadata:libmysqlclient.WORKSPACE",
        urls = ["https://github.com/MariaDB/mariadb-connector-c/archive/refs/tags/v3.0.8-release.tar.gz"],
        sha256 = "6cddafd9419a338ed3d87ed7729d935ce54ce944340a1810e1cd9ba0f0e8601e",
        strip_prefix = "mariadb-connector-c-3.0.8-release",
        patches = ["//ml_metadata/third_party:libmysqlclient.patch"],
    )

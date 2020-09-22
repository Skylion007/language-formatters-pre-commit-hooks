# -*- coding: utf-8 -*-
import os
import shutil

import pytest

from language_formatters_pre_commit_hooks.pretty_format_yaml import pretty_format_yaml


@pytest.fixture(autouse=True)
def change_dir():
    working_directory = os.getcwd()
    try:
        os.chdir("test-data/pretty_format_yaml/")
        yield
    finally:
        os.chdir(working_directory)


@pytest.mark.parametrize(
    ("filename", "expected_retval"),
    (
        ("pretty-formatted.yaml", 0),
        ("not-pretty-formatted.yaml", 1),
        ("multi-doc-pretty-formatted.yaml", 0),
        ("multi-doc-not-pretty-formatted.yaml", 1),
        ("not-valid-file.yaml", 1),
        ("ansible-vault.yaml", 0),
        ("primitive.yaml", 0),
        ("empty-doc-with-separator.yaml", 1),
        ("empty-doc.yaml", 0),
        ("multi-doc-with-empty-document-inside.yaml", 0),
    ),
)
def test_pretty_format_yaml(filename, expected_retval):
    assert pretty_format_yaml([filename]) == expected_retval


@pytest.mark.parametrize(
    ("no_pretty_file_name"),
    (
        ("not-pretty-formatted.yaml"),
        ("multi-doc-not-pretty-formatted.yaml"),
    ),
)
def test_pretty_format_yaml_autofix(tmpdir, no_pretty_file_name):
    srcfile = tmpdir.join("to_be_fixed.yaml")
    shutil.copyfile(
        no_pretty_file_name,
        srcfile.strpath,
    )
    assert pretty_format_yaml(["--autofix", srcfile.strpath]) == 1

    # file was formatted (shouldn't trigger linter again)
    ret = pretty_format_yaml([srcfile.strpath])
    assert ret == 0


def test_pretty_format_yaml_preserve_quotes():
    filename = "preserve-quotes-pretty-formatted.yaml"
    assert pretty_format_yaml([filename]) == 1
    assert pretty_format_yaml(["--preserve-quotes", filename]) == 0

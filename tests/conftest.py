# -*- coding: utf-8 -*-
import os
from contextlib import contextmanager


@contextmanager
def change_dir_context(directory):
    working_directory = os.getcwd()
    try:
        os.chdir(directory)
        yield
    finally:
        os.chdir(working_directory)


@contextmanager
def undecorate_function(func):
    passed_function = func
    func = getattr(passed_function, "__wrapped__", passed_function)
    yield func
    func = passed_function

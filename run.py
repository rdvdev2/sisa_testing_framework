#!/usr/bin/env python3

import os
from pathlib import Path
import tomllib

from vunit import VUnit
from vunit.json4vhdl import encode_json

import sisa_assertions

with open("config.toml", "rb") as f:
    config = tomllib.load(f)


test_files_dir = Path(config['test_files_dir'])
source_glob = config['source_glob']

def make_post_check(test_name):
    def post_check(output_path):
        output_file = Path(output_path) / "dump.hex"
        code_file = test_files_dir / f"{test_name}.hex"
        assertions_file = test_files_dir / f"{test_name}.assertions"

        with code_file.open("r") as fread:
            code = fread.read().splitlines()

        assertions = []
        with assertions_file.open("r") as fread:
            for line in fread.read().splitlines():
                assertions.extend(sisa_assertions.Assertion.from_line(line))

        with output_file.open("r") as fread:
            memory_dump = fread.read().splitlines()

        if len(memory_dump) != 65536:
            print("Invalid dump")
            return False

        code_start = 24576
        for i in range(len(code)):
            expected = code[i]
            got = memory_dump[code_start + i]
            if expected != got:
                print(f"Code corruption @ {hex((code_start + i) * 2)} ({i}th instruction). Expected {expected}, got {got}.")
                return False

        dumps = dict(
            memory=memory_dump
        )

        for assertion in assertions:
            if not assertion.passes(dumps):
                print(assertion.describe_failure(dumps))
                return False

        return True

    return post_check


vu = VUnit.from_argv(compile_builtins=False)
vu.add_vhdl_builtins()

lib = vu.add_library("lib")
lib.add_source_files("./*.vhd")
lib.add_source_files(source_glob)

vu.add_compile_option("ghdl.a_flags", ["-fsynopsys"])
vu.set_sim_option("ghdl.elab_flags", ["-fsynopsys"])
# vu.set_generic("mem_path", "test_files/simple_io.hex")
# vu.set_generic("mem_path", "test_files/simple_io.hex")

tb = lib.get_test_benches()[0];

for test_file in os.listdir(test_files_dir):
    [test_name, ext] = os.path.splitext(test_file)
    print(test_name)

    if ext != ".hex":
        continue
    
    tb.add_config(
        test_name,
        generics = dict(mem_path = test_files_dir / test_file),
        post_check=make_post_check(test_name)
    )

vu.main()

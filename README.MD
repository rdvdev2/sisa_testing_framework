# SISA testing framework
This is a VUnit based testing framework for the SISA processor designed in the
Computer Engineering Project subject of the Computer Engineering degree of the
Facultat d'Informàtica de Barcelona, associated to the Universitat Politécnica
de Catalunya.

## Status
This project is currently in development. Please read about the shortcomings
and pitfalls of the program near the end of this README.

## Licensing
Due to the testbench being based upon the VHDL files provided by the course,
all `*.vhd` files in this repository are not covered by the license, and
pertain to their corresponding authors. Everything else is licensed under the
GPL-3.0 license.

## Software requirements
The following software is needed to run the program:
- Python >= 3.11
- Vunit
- GHDL

Please refer to the documentation of each tool for installation instructions.

## Usage

### Setup
Adjust `config.toml` to your liking. Each field should be self-explanatory. If
you are going to use this project for a CI pipeline, it is advised to include
this repository as a submodule of your repository.

### Testbench definition
Each test is composed of two files:
- `test_name.hex`: It's the code segment of the test, in the same format used
  when programming the FPGA or running the tests provided by the course.
- `test_name.assertions`: It's the memory assertions that are run after the
  completion of the program. The format is the same that is used in the project
  documentation. Beware that there isn't a fully developed parser, and as such
  whitespace IS significant.

### Test execution
Running the tests is as easy as running `./run.py`. You may check additional
VUnit flags with `-h`. It is highly recommended to parallelize the test
execution by adding the argument `-p NUMBER_OF_TESTS`.

## Shortcomings, pitfalls and future plans
- Tests can only interact with memory, no IO yet.
- There's no way to load a data segment into a test. Best you can do for now is
  to `movi` and `st` all your data at the start of the program.
- There's no timeout for tests, if a program enters an infinite loop you will
  have to kill the test runner.
- Tests have to be stored assembled. Ideally, we would like to be able to
  compile or assemble programs during test execution (with proper caching).
- The test executor is coupled to the `sisa.vhd` interface. It could very well
  happen that you need to modify `tb_sisa.vhd` before the test bench even
  compiles.

## Contributing
You can contribute by opening pull requests or issues for missing features or
bugs.

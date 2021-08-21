#!/usr/bin/env python3
"""Wrapper script for clang-tidy."""
#############################################################################
import re
import sys

from hooks.utils import ClangAnalyzerCmd


class ClangTidyCmd(ClangAnalyzerCmd):
    """Class for the clang-tidy command."""

    command = "clang-tidy"
    lookbehind = "LLVM version "

    def __init__(self, args):
        super().__init__(self.command, self.lookbehind, args)
        self.parse_args(args)
        self.edit_in_place = "-fix" in self.args or "--fix-errors" in self.args
        self.parse_ddash_args()

    def run(self):
        """Run clang-tidy"""
        for filename in self.files:
            self.run_command(filename)
            sys.stdout.buffer.write(self.stdout)
            has_errors = (b'error generated.' in self.stderr
                          or b'errors generated.' in self.stderr
                          or b'warnings treated as errors' in self.stderr)
            # Change return code if errors are generated
            if has_errors and self.returncode == 0:
                self.returncode = 1

            if self.returncode != 0:
                sys.stderr.buffer.write(self.stderr)
                sys.exit(self.returncode)
            else:
                self.stderr = b''


def main(argv=None):
    cmd = ClangTidyCmd(argv)
    cmd.run()


if __name__ == "__main__":
    main()

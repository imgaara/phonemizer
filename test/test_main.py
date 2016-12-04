# Copyright 2016 Thomas Schatz, Xuan Nga Cao, Mathieu Bernard
#
# This file is part of phonemizer: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Phonemizer is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with phonemizer. If not, see <http://www.gnu.org/licenses/>.
"""Test of the phonemizer.Phonemizer class"""

import pytest
import tempfile
import shlex

from phonemizer.main import main


class TestPhonemizerMain(object):
    def setup(self):
        pass

    def _test(self, input, output, args=''):
        with tempfile.NamedTemporaryFile('w') as finput:
            finput.write(input)
            finput.seek(0)

            with tempfile.NamedTemporaryFile('w+') as foutput:
                main(shlex.split('{} -o {} {}'.format(
                    finput.name, foutput.name, args)))
                assert foutput.read() == output + '\n'

    def test_help(self):
        with pytest.raises(SystemExit):
            main('-h'.split())

    def test_readme(self):
        self._test('hello world', 'hh-ax-l-|ow-| w-er-l-d-| ')
        self._test('hello world', 'hh-ax-l|ow w-er-l-d', '--strip')
        self._test('hello world',
                   'hh ax l ;esyll ow ;esyll ;eword w er l d ;esyll ;eword ',
                   "-p ' ' -s ';esyll ' -w ';eword '")

    def test_njobs(self):
        for njobs in range(1, 4):
            self._test(
                'hello world\ngoodbye\nthird line\nyet another',
                'hh-ax-l|ow w-er-l-d\ng-uh-d|b-ay\nth-er-d l-ay'
                '-n\ny-eh-t ax-n|ah-dh|er', '--strip -j {}'.format(njobs))
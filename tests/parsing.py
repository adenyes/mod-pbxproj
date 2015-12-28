# Copyright (c) 2015, Ignacio Calderon
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import unittest
from mod_pbxproj import XcodeProject
import openstep_parser as osp
import difflib
import sys, os, string

class Parsing(unittest.TestCase):
    def testParsingPurePython(self):
        for file in ['MusicCube', 'MetalImageProcessing', 'CollectionView', 'CloudSearch']:
            result = XcodeProject.Load('tests/samples/{0}.xcodeproj/project.pbxproj'.format(file), pure_python=True)
            control = osp.OpenStepDecoder.ParseFromFile(open('tests/samples/{0}.xcodeproj/project.pbxproj'.format(file)))
            assert result.data == control

class Saving(unittest.TestCase):
    def testSaving(self):
        for file in ['MusicCube', 'MetalImageProcessing', 'CollectionView', 'CloudSearch']:
            pbxpathin = 'tests/samples/{0}.xcodeproj/project.pbxproj'.format(file)
            pbxpathout = 'tests/samples/{0}.out.pbxproj'.format(file)
            pbx = XcodeProject.Load(pbxpathin) # TODO: pure_python=True fails when parsing "$(inherits)"
            pbx.save(pbxpathout)
            fromlines = open(pbxpathin, 'U').readlines()
            tolines = open(pbxpathout, 'U').readlines()
            diff = ''.join(difflib.unified_diff(fromlines, tolines, pbxpathin, pbxpathout,'','',1))
            os.remove(pbxpathout)
            assert not diff, "Saved unchanged project different than I read it: {0}".format(diff)

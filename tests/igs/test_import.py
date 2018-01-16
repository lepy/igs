# -*- coding: utf-8 -*-

import os
import igs.igs
modulepath = os.path.dirname(__file__)

def test_import():

    filepath = os.path.join(modulepath, "test001.iges")

    i = igs.igs.Iges(open(filepath))

if __name__ == '__main__':
    test_import()

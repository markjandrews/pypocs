import os
import unittest
import shutil


class TestRibonHandlers(unittest.TestCase):
    artefacts_dir = 'artefacts'

    def setUp(self):
        if os.path.exists(self.artefacts_dir):
            shutil.rmtree(self.artefacts_dir)

        os.makedirs(self.artefacts_dir)

    def tearDown(self):
        pass

    def testBaseHandlerImport(self):
        import ribon

        working_dir = os.path.join(self.artefacts_dir, 'project1')
        if os.path.exists(working_dir):
            shutil.rmtree(working_dir)

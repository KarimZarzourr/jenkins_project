# tests/test_deploy.py
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest import mock

import deploy


class TestDeploy(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def test_deploy_creates_release_and_current(self):
        current = deploy.deploy(self.root, "5")

        release = os.path.join(self.root, "releases", "build-5")
        self.assertTrue(os.path.isfile(os.path.join(release, "app.py")))
        self.assertTrue(os.path.isfile(os.path.join(current, "app.py")))
        with open(os.path.join(current, "VERSION.txt")) as f:
            self.assertIn("build 5", f.read())

    def test_redeploy_replaces_current(self):
        deploy.deploy(self.root, "1")
        current = deploy.deploy(self.root, "2")

        with open(os.path.join(current, "VERSION.txt")) as f:
            self.assertIn("build 2", f.read())
        self.assertEqual(
            sorted(os.listdir(os.path.join(self.root, "releases"))),
            ["build-1", "build-2"])

    def test_smoke_test_passes_on_deployed_app(self):
        current = deploy.deploy(self.root, "3")
        self.assertEqual(deploy.smoke_test(current),
                         "Hello, World from Karim Zarzour!")

    def test_smoke_test_fails_on_broken_app(self):
        with open(os.path.join(self.root, "app.py"), "w") as f:
            f.write("def greet(name):\n    return 'wrong'\n")
        with self.assertRaises(SystemExit):
            deploy.smoke_test(self.root)

    def test_main_uses_environment(self):
        env = {"DEPLOY_DIR": self.root, "BUILD_NUMBER": "9"}
        output = io.StringIO()
        with mock.patch.dict(os.environ, env), redirect_stdout(output):
            deploy.main()
        self.assertIn("Deployed build 9", output.getvalue())
        self.assertIn("Hello, World from Karim Zarzour!", output.getvalue())


if __name__ == "__main__":
    unittest.main()

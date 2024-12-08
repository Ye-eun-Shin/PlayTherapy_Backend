import unittest
from analyze.container import Container


class TestObservationRepository(unittest.TestCase):

    def setUp(self):
        self.container = Container()
        self.container.config.from_yaml("tests\config-TEST.yaml")
        self.container.wire(packages=["tests"])
        self.observation_repository = self.container.observation_repository()

    def test(self):
        results = self.observation_repository.list()
        print("\n")
        # print(results)
        self.assertTrue(len(results) > 0)


if __name__ == "__main__":
    unittest.main()

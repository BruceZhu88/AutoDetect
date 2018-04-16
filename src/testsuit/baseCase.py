
import unittest
from common.speaker import Speaker

speaker = Speaker()


class BaseCase(unittest.TestCase):

    def setUp(self):
        speaker.power_on()

    def tearDown(self):
        speaker.power_off()

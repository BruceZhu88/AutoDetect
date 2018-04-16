

from testsuit.baseCase import *


class TestBt(BaseCase):
    """Test BT function"""

    def test_BtPairing(self):
        """Test BT pairing"""
        speaker.bt_pairing()
        speaker.bt_cancel_pairing()

    def test_BtPairingTimeout(self):
        """Test BT pairing"""
        speaker.bt_pairing()
        speaker.bt_pairing_timeout()

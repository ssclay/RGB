from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..TCS34725_block import RGB
from unittest.mock import patch, MagicMock, Mock



class TestTCS34725(NIOBlockTestCase):

    def test_process_signals(self):
        """Signals pass through block unmodified."""
        #blk = TCS34725()
        #mockguy.return_value.get_raw_data.return_value = MagicMock()
        with patch('Adafruit_TCS34725.TCS34725') as mockguy:
            mockdata = [1, 2, 3, 4]
            mock_get_raw_data = mockguy.return_value.get_raw_data
            mock_get_raw_data.return_value = mockdata
            blk = RGB()
            self.configure_block(blk, {})
            blk.start()
            blk.process_signals([Signal({"hello": "n.io"})])
            blk.stop()
            self.assertTrue(mock_get_raw_data.call_count)
            self.assert_num_signals_notified(1)
            self.assertDictEqual(
                self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
                {"hello": "n.io"})

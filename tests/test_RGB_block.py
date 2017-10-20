from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..RGB_block import RGB
from unittest.mock import patch, MagicMock, Mock, ANY


class TestRGB(NIOBlockTestCase):

    def test_process_signals(self):
        """Signals pass through block unmodified."""
        with patch('Adafruit_TCS34725.TCS34725') as mockguy:
            mockdata = [1, 2, 3, 4]
            self.output = {'red': 1,
                      'green': 2,
                      'blue': 3,
                      'clear': 4,
                      'temp': ANY,
                      'lux': ANY}
            mock_get_raw_data = mockguy.return_value.get_raw_data
            mock_get_raw_data.return_value = mockdata
            blk = RGB()
            self.configure_block(blk, {})
            blk.start()
            blk.process_signals([Signal({'red': 1,
                                         'green': 2,
                                         'blue': 3,
                                         'clear': 4,
                                         'temp': 5,
                                         'lux': 6})])
            blk.stop()
            self.assertTrue(mock_get_raw_data.call_count)
            self.assert_num_signals_notified(1)
        print([DEFAULT_TERMINAL][0])
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(), self.output)

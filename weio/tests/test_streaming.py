"""
Unit tests for streaming functionality in weio
"""
import unittest
import os
import numpy as np
from weio.tests.helpers_for_test import MyDir
from weio.fast_output_file import FASTOutputFile


class TestFASTOutputFileStreaming(unittest.TestCase):
    """Test streaming functionality for FASTOutputFile"""

    def setUp(self):
        """Set up test files"""
        self.ascii_file = os.path.join(MyDir, 'FASTOut.out')
        self.binary_file = os.path.join(MyDir, 'FASTOutBin.outb')

    def test_backward_compatibility_ascii(self):
        """Test that normal mode still works for ASCII files"""
        f = FASTOutputFile(self.ascii_file)
        self.assertIsNotNone(f.data)
        self.assertGreater(len(f.data), 0)
        self.assertEqual(f.data.shape[0], 21)

    def test_backward_compatibility_binary(self):
        """Test that normal mode still works for binary files"""
        f = FASTOutputFile(self.binary_file)
        self.assertIsNotNone(f.data)
        self.assertGreater(len(f.data), 0)
        self.assertEqual(f.data.shape[0], 201)

    def test_streaming_header_only_ascii(self):
        """Test header-only reading for ASCII files"""
        with FASTOutputFile(self.ascii_file, streaming=True) as f:
            # Headers should be loaded
            self.assertIn('attribute_names', f)
            self.assertIn('attribute_units', f)
            self.assertIsNotNone(f.description)

            # Data should NOT be loaded
            self.assertIsNone(f.data)

            # Check header content
            self.assertIn('Time', f['attribute_names'])
            self.assertIn('GenSpeed', f['attribute_names'])

    def test_streaming_header_only_binary(self):
        """Test header-only reading for binary files"""
        with FASTOutputFile(self.binary_file, streaming=True) as f:
            # Headers should be loaded
            self.assertIn('attribute_names', f)
            self.assertIn('attribute_units', f)
            self.assertIsNotNone(f.description)

            # Data should NOT be loaded
            self.assertIsNone(f.data)

            # Check header content
            self.assertIn('Time', f['attribute_names'])
            self.assertIn('Wind1VelX', f['attribute_names'])

    def test_streaming_with_readAll_ascii(self):
        """Test streaming mode with readAll() for ASCII files"""
        with FASTOutputFile(self.ascii_file, streaming=True) as f:
            # Initially no data
            self.assertIsNone(f.data)

            # Call readAll()
            f.readAll()

            # Now data should be loaded
            self.assertIsNotNone(f.data)
            self.assertEqual(f.data.shape[0], 21)
            self.assertIn('Time_[s]', f.data.columns)
            self.assertIn('GenSpeed_[rpm]', f.data.columns)

    def test_streaming_with_readAll_binary(self):
        """Test streaming mode with readAll() for binary files"""
        with FASTOutputFile(self.binary_file, streaming=True) as f:
            # Initially no data
            self.assertIsNone(f.data)

            # Call readAll()
            f.readAll()

            # Now data should be loaded
            self.assertIsNotNone(f.data)
            self.assertEqual(f.data.shape[0], 201)
            self.assertIn('Time_[s]', f.data.columns)
            self.assertIn('Wind1VelX_[m/s]', f.data.columns)

    def test_streaming_data_consistency_ascii(self):
        """Test that streaming mode produces same data as normal mode (ASCII)"""
        # Normal mode
        f_normal = FASTOutputFile(self.ascii_file)
        data_normal = f_normal.data.copy()

        # Streaming mode
        with FASTOutputFile(self.ascii_file, streaming=True) as f_stream:
            f_stream.readAll()
            data_stream = f_stream.data.copy()

        # Should be identical
        np.testing.assert_array_almost_equal(data_normal.values, data_stream.values, decimal=10)
        self.assertEqual(list(data_normal.columns), list(data_stream.columns))

    def test_streaming_data_consistency_binary(self):
        """Test that streaming mode produces same data as normal mode (binary)"""
        # Normal mode
        f_normal = FASTOutputFile(self.binary_file)
        data_normal = f_normal.data.copy()

        # Streaming mode
        with FASTOutputFile(self.binary_file, streaming=True) as f_stream:
            f_stream.readAll()
            data_stream = f_stream.data.copy()

        # Should be identical
        np.testing.assert_array_almost_equal(data_normal.values, data_stream.values, decimal=5)
        self.assertEqual(list(data_normal.columns), list(data_stream.columns))

    def test_streaming_without_context_manager_fails(self):
        """Test that streaming without context manager raises error"""
        with self.assertRaises(RuntimeError) as cm:
            f = FASTOutputFile(self.ascii_file, streaming=True)
            f.read()

        self.assertIn('context manager', str(cm.exception))

    def test_readAll_without_streaming_fails(self):
        """Test that readAll() requires streaming mode"""
        f = FASTOutputFile(self.ascii_file)

        with self.assertRaises(RuntimeError) as cm:
            f.readAll()

        self.assertIn('streaming mode', str(cm.exception))

    def test_read_streaming_without_context_fails(self):
        """Test that calling read() with streaming=True fails without context manager"""
        # Creating object with streaming=True doesn't read immediately
        f = FASTOutputFile()
        f.filename = self.ascii_file
        f.streaming = True

        # Trying to read without context manager should fail
        with self.assertRaises(RuntimeError) as cm:
            f.read()

        self.assertIn('context manager', str(cm.exception))

    def test_file_handle_cleanup(self):
        """Test that file handles are properly closed"""
        # After context manager exits, file should be closed
        with FASTOutputFile(self.ascii_file, streaming=True) as f:
            f.readAll()
            self.assertIsNotNone(f._fid)

        # After exit, file handle should be None
        self.assertIsNone(f._fid)

    def test_streaming_metadata_available(self):
        """Test that all metadata is available in header-only mode"""
        with FASTOutputFile(self.binary_file, streaming=True) as f:
            # Binary-specific metadata should be available in info_binary dict
            self.assertIn('info_binary', f)
            self.assertIn('FileID', f['info_binary'])
            self.assertIn('NumOutChans', f['info_binary'])
            self.assertIn('NT', f['info_binary'])

            # Should be able to determine file properties without reading data
            num_channels = len(f['attribute_names'])
            self.assertGreater(num_channels, 0)


class TestBaseFileStreaming(unittest.TestCase):
    """Test base File class streaming functionality"""

    def test_context_manager_support(self):
        """Test that File class has context manager methods"""
        from weio.file import File

        # Check that methods exist
        self.assertTrue(hasattr(File, '__enter__'))
        self.assertTrue(hasattr(File, '__exit__'))

    def test_readAll_method_exists(self):
        """Test that readAll() method exists"""
        from weio.file import File

        self.assertTrue(hasattr(File, 'readAll'))
        self.assertTrue(hasattr(File, '_readAll'))

    def test_readChunk_method_exists(self):
        """Test that readChunk() method exists"""
        from weio.file import File

        self.assertTrue(hasattr(File, 'readChunk'))
        self.assertTrue(hasattr(File, '_readChunk'))


class TestCSVFileStreaming(unittest.TestCase):
    """Test streaming functionality for CSVFile"""

    def setUp(self):
        """Set up test files"""
        from weio.csv_file import CSVFile
        self.CSVFile = CSVFile
        self.csv_comma = os.path.join(MyDir, 'CSVComma.csv')
        self.csv_header = os.path.join(MyDir, 'CSVColInHeader.csv')
        self.csv_tab = os.path.join(MyDir, 'CSVTab.csv')

    def test_backward_compatibility_csv(self):
        """Test that normal mode still works for CSV files"""
        f = self.CSVFile(self.csv_comma)
        self.assertIsNotNone(f.data)
        self.assertGreater(len(f.data), 0)
        self.assertEqual(len(f.data.columns), 2)
        self.assertIn('ColA', f.data.columns)
        self.assertIn('ColB', f.data.columns)

    def test_streaming_header_only_csv(self):
        """Test header-only reading for CSV files"""
        with self.CSVFile(self.csv_comma, streaming=True) as f:
            # Metadata should be loaded
            self.assertIsNotNone(f.colNames)
            self.assertGreater(len(f.colNames), 0)
            self.assertIsNotNone(f.sep)

            # Data should NOT be loaded
            self.assertIsNone(f.data)

            # Check column names
            self.assertIn('ColA', f.colNames)
            self.assertIn('ColB', f.colNames)

    def test_streaming_with_readAll_csv(self):
        """Test streaming mode with readAll() for CSV files"""
        with self.CSVFile(self.csv_comma, streaming=True) as f:
            # Initially no data
            self.assertIsNone(f.data)

            # Call readAll()
            f.readAll()

            # Now data should be loaded
            self.assertIsNotNone(f.data)
            self.assertEqual(len(f.data.columns), 2)
            self.assertIn('ColA', f.data.columns)
            self.assertIn('ColB', f.data.columns)
            self.assertEqual(len(f.data), 4)

    def test_streaming_data_consistency_csv(self):
        """Test that streaming mode produces same data as normal mode (CSV)"""
        # Normal mode
        f_normal = self.CSVFile(self.csv_comma)
        data_normal = f_normal.data.copy()

        # Streaming mode
        with self.CSVFile(self.csv_comma, streaming=True) as f_stream:
            f_stream.readAll()
            data_stream = f_stream.data.copy()

        # Should be identical
        np.testing.assert_array_equal(data_normal.values, data_stream.values)
        self.assertEqual(list(data_normal.columns), list(data_stream.columns))

    def test_streaming_without_context_manager_fails_csv(self):
        """Test that streaming without context manager raises error"""
        f = self.CSVFile()
        f.filename = self.csv_comma
        f.streaming = True

        # Trying to read without context manager should fail
        with self.assertRaises(RuntimeError) as cm:
            f.read()

        self.assertIn('context manager', str(cm.exception))

    def test_readAll_without_streaming_fails_csv(self):
        """Test that readAll() requires streaming mode"""
        f = self.CSVFile(self.csv_comma)

        with self.assertRaises(RuntimeError) as cm:
            f.readAll()

        self.assertIn('streaming mode', str(cm.exception))

    def test_file_handle_cleanup_csv(self):
        """Test that file handles are properly closed"""
        # After context manager exits, file should be closed
        with self.CSVFile(self.csv_comma, streaming=True) as f:
            f.readAll()
            self.assertIsNotNone(f._fid)

        # After exit, file handle should be None
        self.assertIsNone(f._fid)

    def test_streaming_with_header_comments(self):
        """Test streaming with files containing comment headers"""
        with self.CSVFile(self.csv_header, streaming=True) as f:
            # Headers should be loaded
            self.assertIsNotNone(f.header)
            self.assertGreater(len(f.header), 0)
            self.assertIsNotNone(f.colNames)

            # Data should NOT be loaded
            self.assertIsNone(f.data)

            # Check that headers were parsed
            self.assertEqual(f.commentChar, '!')

    def test_streaming_readChunk_csv(self):
        """Test readChunk() functionality for CSV files"""
        with self.CSVFile(self.csv_comma, streaming=True) as f:
            # Read first chunk (3 lines)
            chunk1 = f.readChunk(nlines=3)
            self.assertIsNotNone(chunk1)
            self.assertEqual(len(chunk1), 3)
            self.assertIn('ColA', chunk1.columns)

            # Read second chunk (remaining 1 line)
            chunk2 = f.readChunk(nlines=3)
            # Should get the remaining line
            if chunk2 is not None:
                self.assertGreaterEqual(len(chunk2), 1)
                self.assertIn('ColA', chunk2.columns)

            # Try to read beyond EOF - should return None
            chunk3 = f.readChunk(nlines=3)
            self.assertIsNone(chunk3)


class TestHAWC2DatFileStreaming(unittest.TestCase):
    """Test streaming functionality for HAWC2DatFile"""

    def setUp(self):
        """Set up test files"""
        from weio.hawc2_dat_file import HAWC2DatFile
        self.HAWC2DatFile = HAWC2DatFile
        self.hawc2_ascii = os.path.join(MyDir, 'HAWC2_out_ascii.sel')
        self.hawc2_binary = os.path.join(MyDir, 'HAWC2_out_bin.sel')

    def test_backward_compatibility_hawc2_ascii(self):
        """Test that normal mode still works for HAWC2 ASCII files"""
        f = self.HAWC2DatFile(self.hawc2_ascii)
        self.assertIsNotNone(f.data)
        self.assertGreater(len(f.data), 0)
        self.assertIn('attribute_names', f.info)
        self.assertIn('attribute_units', f.info)

    def test_backward_compatibility_hawc2_binary(self):
        """Test that normal mode still works for HAWC2 binary files"""
        f = self.HAWC2DatFile(self.hawc2_binary)
        self.assertIsNotNone(f.data)
        self.assertGreater(len(f.data), 0)
        self.assertIn('attribute_names', f.info)

    def test_streaming_header_only_hawc2(self):
        """Test header-only reading for HAWC2 files"""
        with self.HAWC2DatFile(self.hawc2_ascii, streaming=True) as f:
            # Metadata should be loaded
            self.assertIn('attribute_names', f.info)
            self.assertIn('attribute_units', f.info)
            self.assertIn('attribute_descr', f.info)
            self.assertIn('NrSc', f.info)
            self.assertIn('NrCh', f.info)

            # Data should NOT be loaded
            self.assertIsNone(f.data)

            # Check metadata content
            self.assertGreater(len(f.info['attribute_names']), 0)
            self.assertGreater(f.info['NrSc'], 0)
            self.assertGreater(f.info['NrCh'], 0)

    def test_streaming_with_readAll_hawc2_ascii(self):
        """Test streaming mode with readAll() for HAWC2 ASCII files"""
        with self.HAWC2DatFile(self.hawc2_ascii, streaming=True) as f:
            # Initially no data
            self.assertIsNone(f.data)

            # Call readAll()
            f.readAll()

            # Now data should be loaded
            self.assertIsNotNone(f.data)
            self.assertEqual(f.data.shape[1], f.info['NrCh'])

    def test_streaming_with_readAll_hawc2_binary(self):
        """Test streaming mode with readAll() for HAWC2 binary files"""
        with self.HAWC2DatFile(self.hawc2_binary, streaming=True) as f:
            # Initially no data
            self.assertIsNone(f.data)

            # Call readAll()
            f.readAll()

            # Now data should be loaded
            self.assertIsNotNone(f.data)
            self.assertEqual(f.data.shape[1], f.info['NrCh'])

    def test_streaming_data_consistency_hawc2(self):
        """Test that streaming mode produces same data as normal mode (HAWC2)"""
        # Normal mode
        f_normal = self.HAWC2DatFile(self.hawc2_ascii)
        data_normal = f_normal.data.copy()

        # Streaming mode
        with self.HAWC2DatFile(self.hawc2_ascii, streaming=True) as f_stream:
            f_stream.readAll()
            data_stream = f_stream.data.copy()

        # Should be identical
        np.testing.assert_array_almost_equal(data_normal, data_stream, decimal=10)

    def test_streaming_without_context_manager_fails_hawc2(self):
        """Test that streaming without context manager raises error"""
        f = self.HAWC2DatFile()
        f.filename = self.hawc2_ascii
        f.streaming = True

        # Trying to read without context manager should fail
        with self.assertRaises(RuntimeError) as cm:
            f.read()

        self.assertIn('context manager', str(cm.exception))

    def test_readAll_without_streaming_fails_hawc2(self):
        """Test that readAll() requires streaming mode"""
        f = self.HAWC2DatFile(self.hawc2_ascii)

        with self.assertRaises(RuntimeError) as cm:
            f.readAll()

        self.assertIn('streaming mode', str(cm.exception))


if __name__ == '__main__':
    unittest.main()

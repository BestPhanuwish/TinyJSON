import hypothesis, icontract
from hypothesis import given, settings, strategies as st

import tinyJSON
import json
import unittest
from string import printable

# Custom strategy to generate Unicode
def unicode_strategy():
    code_digits = '0123456789abcdefABCDEF'
    sample_strategy = st.sampled_from(code_digits)
    
    def build_unicode(h1, h2, h3, h4):
        unicode_code_point = f"{h1}{h2}{h3}{h4}"
        return rf"\u{unicode_code_point}" # double backslash problem T-T
    
    unicode_build_strategy = st.builds(
        build_unicode,
        sample_strategy,
        sample_strategy,
        sample_strategy,
        sample_strategy
    )
    return unicode_build_strategy

class TestTinyJSONFunction(unittest.TestCase):
    
    # Parsing an invalid JSON string will raise an exception
    @given(st.text())
    @settings(max_examples=10)
    def test_invalid_json_parsing(self, json_str):
        with self.assertRaises((ValueError, StopIteration)):
            tinyJSON.parse_string(json_str)
        
    # Parsing null JSON should be valid
    def test_null_json_parsing(self):
        json_str = '{"name": null}'
        actual = tinyJSON.parse_string(json_str)
        expected = json.loads(json_str)
        self.assertEqual(actual, expected)
    
    # Parsing an invalid JSON null will raise an exception
    def test_invalid_null_parsing(self):
        json_str = '{"invalid_null": nb}'
        with self.assertRaises((ValueError)):
            tinyJSON.parse_string(json_str)
        
        json_str = '{"invalid_null2": nub}'
        with self.assertRaises((ValueError)):
            tinyJSON.parse_string(json_str)
            
        json_str = '{"invalid_null3": nulb}'
        with self.assertRaises((ValueError)):
            tinyJSON.parse_string(json_str)
        
    # Parsing a valid string JSON
    @st.composite
    def gen_text_json(draw):
        key = draw(st.text())
        value = draw(st.text())
        return str({key: value})
    
    @given(gen_text_json())
    def test_text_valid_json_parsing(self, json_str):
        try:
            actual = tinyJSON.parse_string(json_str)
            expected = json.loads(json_str)
            self.assertEqual(actual, expected)
        except Exception: # disregard input if it cause error while generating json
            return
    
    # Parsing an invalid JSON string will raise an exception
    def test_invalid_text_parsing(self):
        json_str = '{"invalid_string": "string"s}'
        with self.assertRaises((ValueError)):
            tinyJSON.parse_string(json_str)
        
    # Parsing a valid number JSON
    @st.composite
    def gen_number_json(draw):
        key = draw(st.integers())
        value = draw(st.integers())
        return str({key: value})
    
    @given(gen_number_json())
    def test_number_valid_json_parsing(self, json_str):
        try:
            actual = tinyJSON.parse_string(json_str)
            expected = json.loads(json_str)
            self.assertEqual(actual, expected)
        except Exception: # disregard input if it cause error while generating json
            return
    
    # Parsing an invalid JSON number will raise an exception
    def test_invalid_number_parsing(self):
        json_str = '{"invalid_num": 111a2b}'
        with self.assertRaises((ValueError)):
            tinyJSON.parse_string(json_str)
        
    # Parsing a valid float JSON
    @st.composite
    def gen_floats_json(draw):
        key = draw(st.floats())
        value = draw(st.floats())
        return str({key: value})
    
    @given(gen_floats_json())
    def test_floats_valid_json_parsing(self, json_str):
        try:
            actual = tinyJSON.parse_string(json_str)
            expected = json.loads(json_str)
            self.assertEqual(actual, expected)
        except Exception: # disregard input if it cause error while generating json
            return
    
    # Parsing an invalid JSON 0float will raise an exception
    def test_invalid_zfloat_parsing(self):
        json_str = '{"invalid_zfloat": 0.a}'
        with self.assertRaises((ValueError)):
            tinyJSON.parse_string(json_str)
            
    # Parsing an invalid JSON float will raise an exception
    def test_invalid_float_parsing(self):
        json_str = '{"invalid_float": 0.1b2}'
        with self.assertRaises((ValueError)):
            tinyJSON.parse_string(json_str)
        
    # Parsing a valid bool JSON
    @st.composite
    def gen_bool_json(draw):
        key = draw(st.booleans())
        value = draw(st.booleans())
        return str({key: value})
    
    @given(gen_bool_json())
    def test_bool_valid_json_parsing(self, json_str):
        try:
            actual = tinyJSON.parse_string(json_str)
            expected = json.loads(json_str)
            self.assertEqual(actual, expected)
        except Exception: # disregard input if it cause error while generating json
            return
        
        
    # Parsing all escape char JSON should be valid
    def test_escape_json_parsing(self):
        json_str = '{"escapes": ["\\\\", "\\b", "\\f", "\\n", "\\t", "\\r", "\\/"]}'
        actual = tinyJSON.parse_string(json_str)
        expected = json.loads(json_str)
        self.assertEqual(actual, expected)
        
    # Parsing an invalid JSON escape char will raise an exception
    def test_invalid_escape_parsing(self):
        json_str = '{"invalid_escape": "\\a"}'
        with self.assertRaises((ValueError)):
            tinyJSON.parse_string(json_str)
    
    # Parsing unicode JSON should be valid
    @given(unicode_strategy())
    def test_unicode_json_parsing(self, json_str):
        try:
            json_str = f'{{"unicode": "{json_str}"}}'
            actual = tinyJSON.parse_string(json_str)
            expected = json.loads(json_str)
            self.assertEqual(actual, expected)
        except Exception: # disregard input if it cause error while generating json
            return

    # Parsing an invalid JSON unicode will raise an exception
    def test_invalid_unicode_parsing(self):
        json_str = '{"invalid_unicode": "\\uGbcd"}'
        with self.assertRaises((ValueError)):
            tinyJSON.parse_string(json_str)
        
        json_str = '{"invalid_unicode2": "\\uaGcd"}'
        with self.assertRaises((ValueError)):
            tinyJSON.parse_string(json_str)
            
        json_str = '{"invalid_unicode3": "\\uabGd"}'
        with self.assertRaises((ValueError)):
            tinyJSON.parse_string(json_str)
            
        json_str = '{"invalid_unicode4": "\\uabcG"}'
        with self.assertRaises((ValueError)):
            tinyJSON.parse_string(json_str)
            
        json_str = '{"invalid_unicode4": "\\uG"}'
        with self.assertRaises((ValueError)):
            tinyJSON.parse_string(json_str)
    
    # Parsing JSON bool should be valid
    def test_sbool_json_parsing(self):
        json_str = '{"true": true, "false": false}'
        actual = tinyJSON.parse_string(json_str)
        expected = json.loads(json_str)
        self.assertEqual(actual, expected)
    
    # Parsing an invalid boolean will raise an exception
    def test_invalid_bool_parsing(self):
        json_str = '{"invalid_false": fb}'
        with self.assertRaises((ValueError)):
            tinyJSON.parse_string(json_str)
        
        json_str = '{"invalid_false2": fab}'
        with self.assertRaises((ValueError)):
            tinyJSON.parse_string(json_str)
            
        json_str = '{"invalid_false3": falb}'
        with self.assertRaises((ValueError)):
            tinyJSON.parse_string(json_str)
            
        json_str = '{"invalid_false4": falsb}'
        with self.assertRaises((ValueError)):
            tinyJSON.parse_string(json_str)
            
        json_str = '{"invalid_true": tb}'
        with self.assertRaises((ValueError)):
            tinyJSON.parse_string(json_str)
        
        json_str = '{"invalid_true2": trb}'
        with self.assertRaises((ValueError)):
            tinyJSON.parse_string(json_str)
            
        json_str = '{"invalid_true3": trub}'
        with self.assertRaises((ValueError)):
            tinyJSON.parse_string(json_str)
        
    # Parsing exp0 JSON should be valid
    def test_exp_json_parsing(self):
        json_str = '{"exp": 1e10, "exp2": -1E-10, "exp3": 0e10}'
        actual = tinyJSON.parse_string(json_str)
        expected = json.loads(json_str)
        self.assertEqual(actual, expected)
    
    # Parsing an invalid JSON exp will raise an exception
    def test_invalid_exp_parsing(self):
        json_str = '{"invalid_exp": 0F10}'
        with self.assertRaises((ValueError)):
            tinyJSON.parse_string(json_str)
    
    # Parsing an invalid JSON sign will raise an exception
    def test_invalid_sign_parsing(self):
        json_str = '{"invalid_sign": -a}'
        with self.assertRaises((ValueError)):
            tinyJSON.parse_string(json_str)
            
    # Parsing an invalid JSON 0exp will raise an exception
    def test_invalid_zexp_parsing(self):
        json_str = '{"invalid_zexp": 0Eb10}'
        with self.assertRaises((ValueError)):
            tinyJSON.parse_string(json_str)
    
    # Parsing an invalid JSON next exp will raise an exception
    def test_invalid_nexp_parsing(self):
        json_str = '{"invalid_nexp": 0E1a0}'
        with self.assertRaises((ValueError)):
            tinyJSON.parse_string(json_str)


if __name__ == "__main__":
    unittest.main()

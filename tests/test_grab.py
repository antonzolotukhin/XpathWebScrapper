import pytest

import pandas as pd
from datetime import datetime
import yaml
import argparse
from xpathwebscrapper.grab import scrap

"""
Poor test is better than none
"""

@pytest.mark.httpretty
def test_scrap_correct_df_data():
    df = scrap('tests/resources/test.yml')

    assert not df.empty
    assert len(df.index) == 2948
    assert df['name'][2946] == '2019–20 Persian Gulf crisis'

import pytest

import pandas as pd
from datetime import datetime
import yaml
import argparse
from xpathwebscrapper.grab import scrap
from xpathwebscrapper.utils import Config

"""
Poor test is better than none
"""

@pytest.mark.httpretty
def test_scrap_correct_df_data():
    c = Config.getInstance()

    parser = argparse.ArgumentParser()

    parser.add_argument("yml", help="site_definition.yml", type=str)
    parser.add_argument("xlsx", help="result.xlsx", type=str)
    parser.add_argument("--ssl-no-verify", default=False, help="Turn off SSL verification", type=bool)
    parser.parse_args(['tests/resources/test.yml','test.xlsx'], namespace=c.args)

    df = scrap()

    assert not df.empty
    assert len(df.index) == 2948
    assert df['name'][2946] == '2019–20 Persian Gulf crisis'

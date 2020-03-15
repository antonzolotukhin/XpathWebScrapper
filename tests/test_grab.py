import pytest
from xpathwebscrapper.grab import scrap
from xpathwebscrapper.utils import Config

"""
Poor test is better than none
"""


@pytest.mark.httpretty
def test_scrap_correct_df_data():

    c = Config.getInstance()
    c.parse_args(['tests/resources/test.yml', 'test.xlsx'])

    df = scrap()

    assert not df.empty
    assert len(df.index) == 2948
    assert df['name'][2946] == '2019–20 Persian Gulf crisis'

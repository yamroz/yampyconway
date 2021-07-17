import pytest
from yamconway.yamconway import *


@pytest.fixture
def yamconway_default():
    yc = YamConway()
    yield yc


def test_yamconway_boards_exist(yamconway_default: YamConway):
    assert yamconway_default.board1
    assert yamconway_default.board2


def test_yamconway_stats_zero(yamconway_default: YamConway):
    assert yamconway_default.stats.births == 0
    assert yamconway_default.stats.deaths == 0

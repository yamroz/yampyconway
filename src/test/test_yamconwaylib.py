import pytest
from yamconway.yamconwaylib import *


@pytest.fixture
def yamconway_default():
    yc = YamConway()
    yield yc


def test_yamconway_boards_exist(yamconway_default):
    assert yamconway_default.board1
    assert yamconway_default.board2


def test_yamconway_stats_zero(yamconway_default):
    assert yamconway_default.stats.births == 0
    assert yamconway_default.stats.deaths == 0

def test_yamconway_load_board(yamconway_default):
    yamconway_default.load_board()

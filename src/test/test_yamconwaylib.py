import pytest
from yamconway.SimulationHQ import *


@pytest.fixture
def yamconway_default():
    yc = SimulationHQ()
    yield yc


def test_yamconway_boards_exist(yamconway_default: SimulationHQ):
    assert yamconway_default.current_board
    assert yamconway_default.future_board


def test_yamconway_stats_zero(yamconway_default: SimulationHQ):
    assert yamconway_default.stats.births == 0
    assert yamconway_default.stats.deaths == 0

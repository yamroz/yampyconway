import pytest
from os import getcwd

from yamconway.ConnectedBoard import ConnectedBoard
from yamconway.ConnectedBoardFactory import ConnectedBoardFactory


@pytest.fixture
def yamconboard_default():
    yconnboard = ConnectedBoard('default')
    yield yconnboard

def test_load_board(yamconboard_default: ConnectedBoard):
    print(getcwd())
    yamconboard_default.load_from_file('src\\test\\test_data\\butterfly.yc')
    assert(yamconboard_default.count_alive_cells() == 36)
    assert(yamconboard_default.rows_no == 6)
    assert(yamconboard_default.cells_in_row == 20)

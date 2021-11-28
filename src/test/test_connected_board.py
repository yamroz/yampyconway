import pytest
from os import getcwd

from yamconway.ConnectedBoard import ConnectedBoard
from yamconway.ConnectedBoardFactory import ConnectedBoardFactory
from yamconway.yamconboardio import YamConnBoardIO

BUTTERFLY_FILE='src\\test\\test_data\\butterfly.yc'

@pytest.fixture
def yamconboard_default():
    yconnboard = ConnectedBoard('default')
    yield yconnboard

def test_load_board(yamconboard_default: ConnectedBoard):
    #yamconboard_default.load_from_file()
    YamConnBoardIO.load_from_file(yamconboard_default,BUTTERFLY_FILE)
    assert(yamconboard_default.count_alive_cells() == 36)
    assert(yamconboard_default.rows_no == 6)
    assert(yamconboard_default.cells_in_row == 20)

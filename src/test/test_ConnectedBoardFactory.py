from yamconway.ConnectedBoardFactory import ConnectedBoardFactory
from yamconway.connectedboard import ConnectedBoard


def test_getConnectedBoard():
    conBoard = ConnectedBoardFactory.getConnectedBoard()
    assert conBoard is not None
    assert type(conBoard) == ConnectedBoard

def test_loadConnectedBoardFromFile():
    conBoard = ConnectedBoardFactory.loadFromFile('src/test/test_data/butterfly.yc')
    assert conBoard is not None
    assert type(conBoard) == ConnectedBoard

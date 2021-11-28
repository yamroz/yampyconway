from yamconway.ConnectedBoard import ConnectedBoard
from yamconway.ConnBoardIO import ConnBoardIO


class ConnectedBoardFactory:
    
    def __init__(self):
        pass

    @staticmethod
    def getConnectedBoard() -> ConnectedBoard:
        return ConnectedBoard()
    
    @staticmethod
    def getCleanConnectedBoard() -> ConnectedBoard:
        return ConnectedBoard(randomize=False)

    @staticmethod
    def loadFromFile(path_to_file:str) -> ConnectedBoard:
        connBoard = ConnectedBoard()
        ConnBoardIO.load_from_file(connBoard,path_to_file)
        return connBoard

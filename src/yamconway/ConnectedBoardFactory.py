from yamconway.ConnectedBoard import ConnectedBoard
from yamconway.yamconboardio import YamConnBoardIO


class ConnectedBoardFactory:
    
    def __init__(self):
        pass

    @staticmethod
    def getConnectedBoard() -> ConnectedBoard:
        return ConnectedBoard()

    def loadFromFile(path_to_file:str) -> ConnectedBoard:
        connBoard = ConnectedBoard()
        YamConnBoardIO.load_from_file(connBoard,path_to_file)
        return connBoard

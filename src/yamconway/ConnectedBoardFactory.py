from ConnectedBoard import ConnectedBoard

class ConnectedBoardFactory:
    
    def __init__(self):
        pass

    @staticmethod
    def getConnectedBoard() -> ConnectedBoard:
        return ConnectedBoard( )

    @staticmethod
    def loadFromFile(path_to_file:str) -> ConnectedBoard:
        newBoard = ConnectedBoardFactory.getConnectedBoard()
        with open(path_to_file) as specimen:
            dead_marker = specimen.readline().rstrip()
            data = specimen.readlines()
            newBoard.rows_no = len(data)
            newBoard.cells_in_row = len(data[0].rstrip())
            newBoard._init_cells(randomize=False)
            for row_idx, row in enumerate(data):
                for char_idx, character in enumerate(row.rstrip()):
                    newBoard.cells[row_idx][char_idx].setAlive(
                        character != dead_marker)
        return newBoard
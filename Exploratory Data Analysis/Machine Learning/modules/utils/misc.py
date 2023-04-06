"""
My first perceptron class
Author: Jack Bosco
"""
def printTable(board, leftHeaders = False):
        # Print the top border
        if leftHeaders:
            print('  ' + "-"*11 * len(board[0]) + "-")
        else:
            print("-"*11 * len(board[0]) + "-")
        # Iterate through the board and print Q if we have a queen there
        for row in range(len(board)):
            if leftHeaders:
                print(row, '||', end='')
            else:
                print("| ", end="")
            for col in range(len(board[0])):
                # Print a blank space for no queen
                print("{:^8}".format(str(round(board[row][col],5))) + " | ", end="")
            print("\n" + "-"*11 * len(board[0]) + "-")
            
def progressBar(progress=1.0, size=50, message='', full = '█', empty = ' '):
    """prints a progress bar of size characters. progress is float value 0.0 to 1.0"""
    return '{4:>3}%|{0:{1}<{2}s}|{3:<{2}}'.format(full*int(progress*size), empty, size, message,  int(progress*100))

def section(name):
    return '\n{0:=^100s}'.format(name)
# DEFINE HELPER FUNCTIONS HERE IF NEEDED

# is_open: takes in the matrix for a reference, and checks if the spot at a given row and column is open
def is_open(data, row, col):
    return data[row][col] == 0

def next_move(data):
    # the input is in the form of a 9x9 matrix with the following values
    # 0 represents open squares
    # 1 represents squares already occupied by the bot
    # -1 represents squares already occupied by the user
    print(data)
    #TODO: IMPLEMENT AI STUFF HERE

    # Keep the return value of the function in this format
    return {
        "row": 1,
        "col": 1
    }

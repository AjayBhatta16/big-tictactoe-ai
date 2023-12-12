class SquareMatrix:
    def __init__(self, size):
        self.size = size
        # each value is -0b01 than what you would expect.
        # 00 corresponds to -1
        # 01 corresponds to 0
        # 10 corresponds to 1
        self.bit_array = [0b01010101010101010101010101010101] * size
        # ^ could've changed math in set_value() to take two bits and split them into furthest extremes
        # but that was more work than I was willing to do after I got this all working :)

    def set_value(self, row, col, value):
        if value < -1 or value > 1:
            raise ValueError("Value must be -1, 0, or 1, but it was " + str(value))
        if 0 <= row < self.size and 0 <= col < self.size:
            bit_position = col * 2
            # clear current bits
            mask = ~(0b11 << bit_position)
            self.bit_array[row] &= mask
            # set new value of current bits
            self.bit_array[row] |= (value + 0b01) << bit_position
        else:
            raise IndexError("Index out of range")

    def get_value(self, row, col):
        if 0 <= row < self.size and 0 <= col < self.size:
            bit_position = col * 2
            return ((self.bit_array[row] >> bit_position) & 3) - 1
        else:
            raise IndexError("Index out of range")
        
    def get_size(self):
        return self.size
    
    def get_matrix(self):
        result = []
        for i in range(self.size):
            newRow = []
            for j in range(self.size):
                newRow.append(self.get_value(i, j))    
            result.append(newRow.copy())
        return result
    
    def __str__(self):
        return str(self.get_matrix())


def test_case():
    size = 3  # Configurable size

    matrix = SquareMatrix(size)

    # Set values: -1, 0, or 1
    matrix.set_value(0, 0, 1)
    matrix.set_value(1, 1, -1)
    matrix.set_value(2, 1, 1)

    # Get values
    print(matrix.get_value(0, 0))  # Output: 1
    print(matrix.get_value(1, 1))  # Output: -1
    print("result: " + str(matrix))

    expected_result = [[1, 0, 0], [0, -1, 0], [0, 1, 0]]
    print("expected: " + str(expected_result))
    if matrix.get_matrix() == expected_result:
        print("match!")
    else: print("something went wrong")

if __name__ == '__main__':
    test_case()
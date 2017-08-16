from eaxgomoku import EaxGomoku

def test_line():
    e = EaxGomoku()

    state = [0] * 225
    assert e.get_winning_player(state) == None

    # Win somewhere in first line

    state = [0] * 225
    for i in range(5):
        state[i] = 1
    assert e.get_winning_player(state) == 1


    state = [0] * 225
    for i in range(1,6):
        state[i] = -1
    assert e.get_winning_player(state) == -1

    state = [0] * 225
    for i in range(15-5,15):
        state[i] = 1
    assert e.get_winning_player(state) == 1

    # No win because of hole

    state = [0] * 225
    for i in range(6):
        state[i] = 1
    state[2] = 0
    assert e.get_winning_player(state) == None

    state = [0] * 225
    for i in range(6):
        state[i] = -1
    state[2] = 1
    assert e.get_winning_player(state) == None

    # No win because of new line

    state = [0] * 225
    for i in range(16-5, 16):
        state[i] = 1
    assert e.get_winning_player(state) == None

def test_col():
    e = EaxGomoku()

    state = [0] * 225
    assert e.get_winning_player(state) == None

    # Win somewhere in first col

    state = [0] * 225
    for i in range(5):
        state[0+i*15] = 1
    assert e.get_winning_player(state) == 1

    state = [0] * 225
    for i in range(1,6):
        state[0+i*15] = -1
    assert e.get_winning_player(state) == -1

    state = [0] * 225
    for i in range(15-5,15):
        state[0+i*15] = 1
    assert e.get_winning_player(state) == 1

    # No win because of hole

    state = [0] * 225
    for i in range(6):
        state[0+i*15] = 1
    state[0+2*15] = 0
    assert e.get_winning_player(state) == None

    state = [0] * 225
    for i in range(6):
        state[0+i*15] = -1
    state[0+2*15] = 1
    assert e.get_winning_player(state) == None


    # No win because of new line

    state = [0] * 225
    for i in range(15-4, 15):
        state[0+i*15] = 1
    state[1+1*15] = 1
    assert e.get_winning_player(state) == None


if __name__ == '__main__':
    test_line()
    test_col()

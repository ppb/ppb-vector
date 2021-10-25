from ppb_vector import Vector


def test_match_sequence():
    match Vector(1, 2):
        case (1, 2):
            assert True
        case _:
            assert False


def test_match_dict():
    match Vector(1, 2):
        case {'x': 1, 'y': 2}:
            assert False
        case _:
            assert True


def test_match_vector_keyword():
    match Vector(1, 2):
        case Vector(x=1, y=2):
            assert True
        case _:
            assert False


def test_match_vector_sequence():
    match Vector(1, 2):
        case Vector(1, 2):
            assert True
        case _:
            assert False

def poker(hands):
    return allmax(hands, key=hand_rank)


def allmax(iter, key=None):
    result, max_value = [], None
    key = key or (lambda x: x)
    for x in iter:
        x_value = key(x)
        if not result or x_value > max_value:
            result, max_value = [x], x_value
        elif x_value == max_value:
            result.append(x)
    return result


def hand_rank(hand):
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, ranks)
    elif kind(3, ranks):
        return (3, ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else: 
        return (0, ranks)


def card_ranks(cards):
    ranks = ["--23456789TJQKA".index(r) for r, s in cards]
    ranks.sort(reverse=True)
    return [5, 4, 3, 2, 1] if (ranks == [14, 5, 3, 2]) else ranks


def straight(ranks):
    return (max(ranks) - min(ranks) == 4) and len(set(ranks)) == 5


def flush(hand):
    suits = [s for r, s in hand]
    return len(set(suits)) == 1


def two_pair(ranks):
    highest = kind(2, ranks)
    lowest = kind(2, list(reversed(ranks)))
    if highest and highest != lowest:
        return (highest, lowest)
    else:
        return None


def kind(n, ranks):
    for r in ranks:
        if ranks.count(r) == n:
            return r
    return None


def test():
    sf = "4D 5D 6D 7D 8D".split()  # straight flush
    fk = "TD TH TC TS 8D".split()  # four of a kind
    fh = "8D 8C 8H KD KC".split()  # full house
    tp = "9C 9D QH QD TC".split()  # two pair
    a_to_5_straight = "AC 2S 3D 4D 5C".split()  # A-5 straight
    a_high = "AC 2C 3D 4S 7S".split()  # A high
    fkranks = card_ranks(fk)
    tpranks = card_ranks(tp)
    assert card_ranks(sf) == [8, 7, 6, 5, 4]
    assert card_ranks(fk) == [10, 10, 10, 10, 8]
    assert card_ranks(a_to_5_straight) == [5, 4, 3, 2, 1]
    assert card_ranks(a_high) == [14, 7, 4, 3, 2]
    assert card_ranks(fh) == [8, 8, 8, 13, 13]
    assert two_pair(tpranks) == (12, 9)
    assert kind(4, fkranks) == 10
    assert poker([sf, fk, fh]) == sf
    assert poker([fk, fh]) == fk
    assert poker([fk, fk]) == fk
    assert poker([sf]) == sf
    assert poker([sf] + 20*[fh]) == sf
    assert hand_rank(sf) == (8, 8)
    assert hand_rank(fk) == (7, 10, 8)
    assert hand_rank(fh) == (6, 13, 8)
    return "test pass"

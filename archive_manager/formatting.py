grains = {
    'year':   '1',
    'month':  '2',
    'day':    '3',
    'hour':   '4',
    'minute': '5',
    'second': '6'
}

def granularity(grain, number=True):
    grain = str(grain)
    for key, value in grains.items():
        if grain == key:
            # Words
            if number:
                return value
            else:
                return grain
        elif grain == value:
            # Numbers
            if number:
                return grain
            else:
                return key
        else:
            # probably don't want anything here
            pass
    raise RuntimeError("No such granluarity: " + grain)

def date(grain, delim='.'):
    grain = int(granularity(grain))
    return delim.join(date_grain(grain))

def date_grain(grain):
    if grain >= 1:
        yield '%Y'
    if grain >= 2:
        yield '%m'
    if grain >= 3:
        yield '%d'
    if grain >= 4:
        yield '%H'
    if grain >= 5:
        yield '%M'
    if grain >= 6:
        yield '%S'

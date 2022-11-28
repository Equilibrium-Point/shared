from pprint import pprint
from functools import reduce

"""
Shorten values of a dict to a maximum length

Args:
    body (dict): the dict to be shortened
    maxlen (int): maximum length to shorten the fields to

Returns:
    dict: the dict with its values shortened
"""
shorten_all = (
    lambda body, maxlen=1024: {k: shorten_all(v) for k, v in body.items()}
    if type(body) is dict
    else list(map(shorten_all, body))
    if type(body) is list
    else f"{body[:maxlen-3]}..."
    if type(body) is str and len(body) > maxlen
    else body
)

def shprint(obj: dict, maxlen: int=1024):
    """
    Pretty-print a dict, keeping all the values shortened to a
    maximum length, so that they don't dominate the visual output

    Args:
        obj (dict): the dict to be printed
        maxlen (int): maximum character length of a dict's fields
    """
    pprint(shorten_all(obj, maxlen))

def bigprint(msg: str, margin: int=1, **kwargs):
    """
    Print a big string padded with a box :)

    Args:
        msg (str): the message to be padded and printed
        margin (int): size of the whitespace inside the box
        **kwargs: all additional kwargs are passed directly to boxpad(),
            refer to the doc for that function for additional info
    """
    print(boxpad(boxpad(msg, **{**kwargs, "char":' ', "padding":margin}), **{**kwargs, "char":'#'}))

def beeeeeegprint(msg: str, layers: int=3, **kwargs):
    """
    Print a veeeery big padded string with multiple fancy layers :D

    Args:
        msg (str): the message to be padded and printed
        layers (int): number of layers in the padding
        **kwargs: all additional kwargs are passed directly to boxpad(),
            refer to the doc for that function for additional info
    """
    print(reduce((lambda s, v: boxpad(s, **{**kwargs, 'char':' ' if v % 2 == 0 else kwargs.get('char', '#')})), range(layers), msg))

# i leave this here for patchy's amusement :p
# boxpad = lambda msg, padding=1, char='#', double_width=True: (lambda hp, wp: (lambda lines: (lambda mlen: (lambda p_str: (lambda padded_lines: (lambda core: p_str + core + p_str)('\n'.join(padded_lines) + '\n'))((f"{char*wp}{ln.ljust(mlen, ' ')}{char*wp}" for ln in lines)))((char*(wp*2 + mlen) + '\n')*hp))(max(len(m) for m in lines)))(msg.split("\n")))(padding, padding*2 if double_width else padding)[:-1]
def boxpad(msg: str, padding: int=1, char: str="#", double_width: bool=True):
    """
    Pad a string with a biiiigggg box around it to make it easier to 
    catch in the middle of a bunch of console output :p

    Args:
        msg (str): the message to pad
        padding (int): size of the box
        char (str): character to make the box out of
        double_width (bool): print the box at twice the width as the height,
            which makes the box look more square-ish with most monospaced fonts
    Returns:
        str: the newly padded string
    """
    hp, wp = padding, padding*2 if double_width else padding
    lines = msg.split("\n")
    mlen = max(len(m) for m in lines)
    p_str = (char*(wp*2 + mlen) + '\n')*hp
    padded_lines = (f"{char*wp}{ln.ljust(mlen, ' ')}{char*wp}" for ln in lines)
    core = '\n'.join(padded_lines) + '\n'
    full = p_str + core + p_str
    return full[:-1]
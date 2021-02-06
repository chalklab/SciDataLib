""" This module contains additional definitions used by the Scidata class """


def denester(q, r):
    """ denester function """
    denestered = {}

    def denest(x, y):
        """ denest function """
        denested = {}
        if type(y) is dict:
            for a, b in y.items():
                if type(b) is dict:
                    denest(a, b)
                elif type(b) is list:
                    for c in b:
                        denest(a, c)

                else:
                    if b not in ['null', None]:
                        denested.update({str(a): str(b)})

            if denested:
                denestered.update({str(x): denested})
    denest(q, r)
    return denestered

def is_number(n):
    """Function used for determining datatype"""

    try:
        float(n)
    except ValueError:
        return False
    return True


def find_sigfigs(x):
    """Function used for determining significant figures"""
    x = x.lower()
    if 'e' in x:
        mystr = x.split('e')
        return len((mystr[0])) - 1
    else:
        n = ('%.*e' % (8, abs(float(x)))).split('e')
        if '.' in x:
            s = x.replace('.', '')
            length = len(s) - len(s.rstrip('0'))
            n[0] = n[0].rstrip('0') + ''.join(['0' for num in range(length)])
        else:
            n[0] = n[0].rstrip('0')
    return find_sigfigs('e'.join(n))

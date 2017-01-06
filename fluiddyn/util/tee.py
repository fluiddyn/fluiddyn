"""MultiFile class

http://stackoverflow.com/a/16551730



"""

# bug
# from builtins import object


class MultiFile(object):
    """MultiFile

    Use for example like this::

      sys.stdout = MultiFile([sys.stdout, open('myfile.txt', 'w')])

    """
    def __init__(self, files):
        self._files = files

    def __getattr__(self, attr, *args):
        return self._wrap(attr, *args)

    def _wrap(self, attr, *args):
        def g(*a, **kw):
            for f in self._files:
                res = getattr(f, attr, *args)(*a, **kw)
            return res
        return g

class TokenVertex:

    def __init__(self, token):
        self._token = token

    def __str__(self):
        return '-({})-'.format(str(self._token))

    @property
    def token(self):
        return self._token


class DependencyEdge:

    def __init__(self, dependency, parent_vertex, child_vertex):
        self._dependency = dependency
        self._parent = parent_vertex
        self._child = child_vertex

    def __str__(self):
        return '{}-[{}]->{}'.format(str(self._parent),
                                    self._dependency,
                                    str(self._child))

    @property
    def dependency(self):
        return self._dependency

    @property
    def parent(self):
        return self._parent

    @property
    def child(self):
        return self._child

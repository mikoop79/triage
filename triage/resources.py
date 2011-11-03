class Root(object):
    def __init__(self, request):
        self.request = request
        self.projects = request.registry.settings['projects']

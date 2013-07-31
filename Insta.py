from instagram.client import InstagramAPI

client_id = ''
client_se = ''

api = InstagramAPI(client_id=client_id, client_secret=client_se)

class DuplicateMediumError(Exception):
    pass

class InstaPhotos:

    def __init__(self):
        self.media = []
        self.allowed_users = ['tidunn13', 'jadaenlynn']
        self.ids = {}

    def add(self, medium):

        if medium.id in self.ids:
            raise DuplicateMediumError('Image/video is already known')

        if medium.user.username not in self.allowed_users:
            print "user medium not allowed %s" % medium.user.username
            return

        self.media.append(medium)
        self.ids[medium.id] = True

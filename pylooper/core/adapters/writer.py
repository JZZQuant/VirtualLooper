import os
import uuid


class AudioWriter():
    def __init__(self, phrase_ids, base="../../VLoop/"):
        self.session_id = str(uuid.uuid4())
        self.folder = base + self.session_id
        for phrase_id in phrase_ids:
            os.makedirs(self.folder + "/phrase" + str(phrase_id) + "/")

class IGGAccount:
    def __init__(self, email):
        self.email = email
        self.igg_ids = []

    def add_igg_id(self, igg_id):
        self.igg_ids.append(igg_id)

    def get_enabled_characters(self):
        characters = []

        for igg_id in self.igg_ids:
            characters.extend(
                igg_id.get_enabled_characters()
            )

        return characters
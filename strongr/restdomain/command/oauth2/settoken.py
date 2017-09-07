class SetToken():
    def __init__(self, user_id, client_id, access_token, expires, scope, token_type):
        self.user_id = user_id
        self.client_id = client_id
        self.access_token = access_token
        self.expires = expires
        self.scope = scope
        self.token_type = token_type

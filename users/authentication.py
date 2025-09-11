from rest_framework.authentication import TokenAuthentication


class CustomTokenAuthentication(TokenAuthentication):
    """
    Allows both:
    - Authorization: Token <token>
    - Authorization: <token>
    """

    keyword = "Token"

    def authenticate(self, request):
        auth = request.headers.get("Authorization")

        if not auth:
            return None

        # case 1: default DRF "Token <token>"
        if auth.startswith(f"{self.keyword} "):
            return super().authenticate(request)

        # case 2: custom "<token>"
        return self.authenticate_credentials(auth.strip())

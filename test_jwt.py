from app.auth.jwt_handler import create_access_token

token = create_access_token(
    {
        "sub": "1",
        "email": "sanket@example.com"
    }
)

print(token)
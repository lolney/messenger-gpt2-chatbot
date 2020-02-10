import os
from app import create_app

if __name__ == '__main__':
    verify_token = os.getenv("VERIFY_TOKEN", None)
    access_token = os.getenv("ACCESS_TOKEN", None)

    if not verify_token:
        raise Exception("verify_token not set")
    if not access_token:
        raise Exception("access_token not set")

    env = {
        "VERIFY_TOKEN": verify_token,
        "ACCESS_TOKEN": access_token
    }

    app = create_app.create_app(env=env)
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

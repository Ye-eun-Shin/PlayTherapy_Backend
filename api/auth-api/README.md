# PlayTherapy_Backend/auth-api
회원가입, 로그인 등의 기능을 다루며, JWT 토큰을 통해 사용자가 자유롭게 서비스를 이용하도록 합니다.

## Install
```bash
pip install -r requirements.txt
```

## Run
```bash
cd api/auth-api
poetry run uvicorn main:app --reload --app-dir auth
```

## Test
```bash
cd api/auth-api
poetry run python -m unittest discover -s tests
```

## Docker Image Build
```bash
docker build --platform linux/amd64 -t 760282210016.dkr.ecr.ap-northeast-2.amazonaws.com/dsail/playtherapy/auth-api  .
```

## Docker Image Push
```bash
docker push 760282210016.dkr.ecr.ap-northeast-2.amazonaws.com/dsail/playtherapy/auth-api
```

## Docs
```bash
http://localhost:8000/docs
```
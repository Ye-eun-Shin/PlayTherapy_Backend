# PlayTherapy_Backend/core-package
모든 API에서 공통적으로 사용하는 코드를 모아둔 패키지로, MySQL을 다루는 tool code와 JWT 토큰 관련 코드가 포함되어 있습니다.

## Install Env

```bash
pip install poetry
```

## Install Dependency

```bash
cd package/core-package
poetry install --sync
```

## Test

```bash
cd package/core-package
poetry run python -m unittest discover -s tests
```
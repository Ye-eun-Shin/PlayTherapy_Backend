# PlayTherapy_Backend/analyze-api
[Langflow](https://www.langflow.org/)를 이용하여 영상에서 추출한 스크립트로 놀이치료사의 놀이치료 과정 평가 레포트를 생성해주는 API입니다.

Langflow를 이용하면 아래 그림과 같이 복잡한 일련의 프롬프트 엔지니어링 과정을 GUI를 통해 실험해 볼 수 있고, 이를 바로 API로 생성할 수 있습니다. 이때, 생성된 API를 감싸는 API가 바로 `analyze-api`입니다.

![image](https://github.com/user-attachments/assets/6063f717-fa78-4df6-bb9e-a0776a1669b2)
아래와 같은 결과를 얻어볼 수 있습니다.
```json
{

	"reports": {

		"descriptions": "놀이치료사가 아동이 놀잇감을 명명하기 전에 먼저 이름을 말하는 경우가 5번 나타났습니다.",

		"level": 2,

		"interactions": [

			{

				"C1": "(입실하며) 엄마 여기서 상담했는데 어제",

				"T1": "엄마도 여기 오셨었구나~ 지금은 아영이 시간이구",

				"check_TF": true,

				"Description": ""

			},

			{

				"C2": "(음료자판기에 동전을 넣어보고 자판기에서 계속 소리가 나자) 그런데요 제가",

				"T2": "응",

				"check_TF": false,

				"Description": ""

			}

		]

	}

}
```
## Install Env

```bash
pip install poetry
```

## Install Dependency

```bash
cd api/analyze-api
poetry install --sync
```

## Run
```bash
cd api/analyze-api
poetry run uvicorn main:app --reload --app-dir analyze
```

## Test

```bash
cd api/analyze-api
poetry run python -m unittest discover -s tests
```

## Docs
```bash
http://localhost:8000/docs
```

# UV + FastAPI 실습 가이드

uv는 Python 버전 관리(pyenv), 패키지 관리(pip/poetry), 실행 환경(pyenv-virtualenv)를 한 번에 처리해 주는 툴입니다. 이 문서는 FastAPI 프로젝트를 예시로, 초보자도 따라 할 수 있도록 **설치 → 프로젝트 생성 → Python 버전 지정 → 가상환경 운용 → 실행·테스트** 흐름을 상세히 정리했습니다.

---

## 0. 준비 개념 한눈에 보기
**왜 가상환경을 써야 할까?**
  - 프로젝트마다 필요한 패키지/버전이 다르기 때문에 전역(Global) Python에 설치하면 충돌이 납니다.
  - 가상환경(보통 `.venv/`)은 각 프로젝트가 독립적으로 패키지를 관리하도록 격리해 줍니다.
  
**uv가 해주는 일**
  - `uv python install 3.12`: pyenv 없이 원하는 버전의 Python 다운로드 및 관리
  - `uv venv --python 3.12 .venv`: 지정한 Python으로 가상환경 생성
  - `uv add fastapi`: 패키지를 `pyproject.toml`과 `uv.lock`에 기록하며 설치
  - `uv run uvicorn ...`: 가상환경을 자동 활성화한 상태로 명령 실행 (`source .venv/bin/activate` 필요 없음)

---

## 1. uv 설치 및 업데이트
1. **설치 여부 확인**
   ```bash
   uv version
   ```
   버전이 출력되면 설치 완료입니다.

2. **설치/업데이트**
- macOS / Linux
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
- Windows PowerShell (관리자 권한)
    ```powershell
    irm https://astral.sh/uv/install.ps1 | iex
    ```

3. **PATH 갱신**
- 설치 후 터미널을 새로 열고 `uv version`이 정상 출력되는지 확인합니다.
- 설치 경로를 커스터마이즈했다면 환경변수 `PATH`에 추가하세요.

---

## 2. 새 FastAPI 프로젝트 생성
```bash
# 작업 폴더 준비
mkdir fastapi-uv-demo
cd fastapi-uv-demo

# pyproject.toml 등 기본 파일 생성
uv init
```
> `uv init`은 `pyproject.toml`과 `.venv/`를 만들지 않습니다. 다음 절차에서 Python 버전을 설치하고 가상환경을 구성합니다.

---

## 3. Python 버전 설치·확인·고정
1. **설치 가능한 버전 확인**
   ```bash
   uv python list --all
   ```
   출력이 길다면 macOS/Linux에서는 `| head`, Windows PowerShell에서는 `| Select-Object -First 10`을 덧붙여 미리보기만 볼 수 있습니다.

2. **원하는 버전 설치**
   ```bash
   uv python install 3.12
   ```
   이미 설치된 버전은 다시 다운로드하지 않습니다. `uv python list`로 설치 결과를 확인하세요.

3. **가상환경 생성 및 Python 지정**
   ```bash
   uv venv --python 3.12 .venv
   ```
   - `.venv` 폴더가 생성되며, 내부 `python`은 uv가 설치한 3.12 버전을 사용합니다.
   - 다른 이름의 폴더를 쓰고 싶다면 `uv venv --python 3.12 .venv-dev`처럼 경로를 바꾸면 됩니다.

4. **프로젝트에 Python 버전 고정**
   ```bash
   uv python pin 3.12
   ```
   - `pyproject.toml`의 `requires-python` 필드가 `^3.12`처럼 업데이트되어 팀원 전원이 동일 버전을 사용하게 도와줍니다.
   - `uv python pin --unset`으로 고정을 해제할 수 있습니다.

5. **가상환경 직접 활성화 (필요할 때만)**
   ```bash
   # macOS / Linux
   source .venv/bin/activate

   # Windows PowerShell
   .\.venv\Scripts\Activate.ps1
   ```
   대부분의 명령은 `uv run ...`으로 실행하면 자동으로 `.venv`를 사용하기 때문에 수동 활성화는 IDE 연동이나 디버깅에만 필요합니다.

> 🔎 **왜 `uv run`만으로 .venv가 만들어질까?**
> - uv는 프로젝트에서 Python 버전이 고정되어 있고 `.venv/`가 없으면 자동으로 가상환경을 생성합니다.
> - `uv sync`, `uv pip install`, `uv run` 모두 `.venv/`를 기준으로 패키지를 설치·실행하므로 전역 Python을 건드리지 않습니다.

---

## 4. FastAPI & 개발 도구 설치
```bash
uv add fastapi uvicorn pytest
```
- `uv add` = `pyproject.toml`에 의존성을 추가하고, `uv.lock`에 정확한 버전을 기록합니다.
- `uv pip install fastapi`처럼 `uv pip`을 쓸 수도 있지만, `uv add`가 의존성 버전 기록과 설치를 동시에 처리해 협업에 유리합니다.
- 명령 실행 이후 `.venv/` 안에 패키지가 설치되며, `uv.tree`로 의존성 트리를 확인할 수 있습니다.

---

## 5. 프로젝트 구조 & 예제 코드
```
fastapi-uv-demo/
├─ app/
│  └─ main.py
├─ tests/
│  └─ test_app.py
├─ .venv/
├─ pyproject.toml
└─ uv.lock
```

`app/main.py`
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, uv + FastAPI!"}
```

`tests/test_app.py`
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, uv + FastAPI!"}
```

---

## 6. 애플리케이션 실행 & 문서 확인
```bash
# 자동으로 .venv를 사용합니다.
uv run uvicorn app.main:app --reload --port 8000
```
- `--reload`: 코드 수정 시 서버 자동 재시작
- `http://127.0.0.1:8000/docs`: Swagger UI (API 문서)
- `http://127.0.0.1:8000/redoc`: ReDoc 문서

서버를 중지하려면 `Ctrl + C`를 누릅니다.

---

## 7. 테스트 실행
```bash
uv run pytest
```
- 조용한 출력: `uv run pytest -q`
- 특정 테스트만 실행: `uv run pytest tests/test_app.py -k read_root`

테스트 실행 전후로 `.venv/`가 자동 사용되므로 별도의 `activate`가 필요 없습니다.

---

## 8. Python 버전 변경 & 재구성
1. **다른 버전 설치**
   ```bash
   uv python install 3.11
   ```
2. **가상환경 교체**
   ```bash
   uv venv --python 3.11 --clear .venv
   ```
   - `--clear` 옵션은 기존 `.venv`를 덮어씁니다. (밀기 전에 커밋/백업 권장)
3. **프로젝트 버전 다시 고정**
   ```bash
   uv python pin 3.11
   ```
4. **의존성 재설치**
   ```bash
   uv sync
   ```

> 📌 `uv python pin`만 변경하면 새 버전을 가리키지만, 가상환경 내부 Python을 교체하려면 `uv venv --python ...`을 반드시 실행해야 합니다.

---

## 9. 자주 쓰는 uv 명령어 & 팁
- **패키지 추가/삭제**
  ```bash
  uv add httpx
  uv remove httpx
  ```
- **의존성 동기화**: 다른 사람이 `uv.lock`을 업데이트했을 때
  ```bash
  uv sync
  ```
- **개발용/배포용 구분**: 선택한 그룹만 설치
  ```bash
  uv sync --group dev
  ```
- **패키지 최신 버전으로 올리기**
  ```bash
  uv lock --upgrade fastapi
  ```
- **의존성 확인**
  ```bash
  uv tree
  ```
- **전역 실행용 커맨드** (`fastapi` CLI 등)
  ```bash
  uv tool install fastapi
  ```
  프로젝트 밖에서도 안전하게 실행됩니다.

---

## 10. 추가 참고 자료
- FastAPI 공식 문서: <https://fastapi.tiangolo.com/>
- uv 공식 문서: <https://docs.astral.sh/uv/latest/>
- uv 도움말: `uv --help`, `uv help venv`, `uv help python`

---

궁금한 점이나 추가로 알아보고 싶은 workflow가 있다면 언제든지 질문해주세요!

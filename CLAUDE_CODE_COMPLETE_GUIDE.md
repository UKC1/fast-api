# Claude Code 완벽 가이드: 설정 관리 및 환경 이동

## 📋 목차
1. [Claude Code 기본 구조](#1-claude-code-기본-구조)
2. [Memory 시스템 설정](#2-memory-시스템-설정)
3. [MCP 서버 활용](#3-mcp-서버-활용)
4. [Hooks 설정](#4-hooks-설정)
5. [설정 백업 및 복원](#5-설정-백업-및-복원)
6. [환경 이동 가이드](#6-환경-이동-가이드)
7. [베스트 프랙티스](#7-베스트-프랙티스)

---

## 1. Claude Code 기본 구조

### 설정 파일 계층 구조
```
프로젝트/
├── .claude/                    # 프로젝트별 설정 (Git 관리)
│   ├── CLAUDE.md               # 프로젝트 메모리
│   ├── rules/                  # 모듈화된 규칙들
│   │   ├── code-style.md       # 코드 스타일 규칙
│   │   ├── testing.md          # 테스트 규칙
│   │   └── security.md         # 보안 규칙
│   ├── settings.json           # 프로젝트 설정
│   └── .mcp.json              # MCP 서버 설정
│
├── CLAUDE.md                   # 대체 위치 (루트)
└── .env                        # 환경 변수 (Git ignore)

~/                              # 사용자 홈
└── .claude/                    # 사용자 전역 설정
    ├── CLAUDE.md              # 사용자 메모리
    └── settings.json          # 사용자 설정
```

### 설정 스코프 우선순위
1. **Managed Policy** (조직 전체)
2. **Project Memory** (팀 공유)
3. **Project Rules** (모듈식 지침)
4. **User Memory** (개인 설정)
5. **Local Project Memory** (프로젝트별 개인 설정)

---

## 2. Memory 시스템 설정

### 2.1 프로젝트 메모리 설정 (.claude/CLAUDE.md)
```markdown
# Project Context

## 프로젝트 정보
- 프로젝트명: FastAPI Todo Application
- 주요 기술: FastAPI, SQLAlchemy, PostgreSQL
- Python 버전: 3.12

## 코드 컨벤션
- 들여쓰기: 4 spaces
- 문자열: double quotes 사용
- Type hints 필수
- Docstring: Google style

## 테스트 명령어
- 테스트 실행: `pytest tests/`
- 타입 체크: `mypy app/`
- 린트: `ruff check .`

## 중요 디렉토리
- API 엔드포인트: app/api/
- 데이터베이스 모델: app/models/
- 비즈니스 로직: app/services/
```

### 2.2 규칙 모듈화 (.claude/rules/)

**code-style.md**
```markdown
---
paths:
  - "**/*.py"
---
# Python 코드 스타일 규칙

- Black 포매터 규칙 준수
- 함수명: snake_case
- 클래스명: PascalCase
- 상수: UPPER_SNAKE_CASE
```

**testing.md**
```markdown
---
paths:
  - "tests/**"
---
# 테스트 작성 규칙

- 모든 새 기능에 단위 테스트 작성
- 테스트 함수명: test_<기능>_<시나리오>
- Given-When-Then 패턴 사용
```

### 2.3 메모리 파일 임포트
```markdown
# .claude/CLAUDE.md
@.claude/rules/code-style.md
@.claude/rules/testing.md
@.claude/rules/security.md

## 추가 프로젝트 컨텍스트
...
```

---

## 3. MCP 서버 활용

### 3.1 MCP 서버 설치

**GitHub 연동**
```bash
# HTTP 서버 추가 (권장)
claude mcp add --transport http github https://api.github.com/mcp

# 로컬 stdio 서버
claude mcp add --transport stdio sqlite -- npx @modelcontextprotocol/server-sqlite
```

### 3.2 프로젝트 MCP 설정 (.claude/.mcp.json)
```json
{
  "mcpServers": {
    "github": {
      "transport": "http",
      "url": "https://api.github.com/mcp",
      "auth": {
        "type": "oauth2",
        "provider": "github"
      }
    },
    "database": {
      "transport": "stdio",
      "command": "npx",
      "args": ["@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    },
    "monitoring": {
      "transport": "http",
      "url": "${MONITORING_API_URL}",
      "headers": {
        "Authorization": "Bearer ${MONITORING_API_KEY}"
      }
    }
  }
}
```

### 3.3 MCP 서버 관리 명령어
```bash
# 서버 목록 확인
claude mcp list

# 서버 상세 정보
claude mcp get github

# 서버 제거
claude mcp remove github

# 서버 새로고침
claude mcp refresh github
```

---

## 4. Hooks 설정

### 4.1 프로젝트 Hooks 설정 (.claude/settings.json)
```json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": "echo '프로젝트 시작: $(pwd)' >> .claude/session.log"
      }
    ],
    "UserPromptSubmit": [
      {
        "type": "prompt",
        "prompt": "이 프로젝트는 FastAPI를 사용합니다. 항상 async/await 패턴을 따라주세요."
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/validate-command.sh",
            "blocking": true
          }
        ]
      },
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "echo '파일 변경: ${TOOL_NAME}' >> .claude/changes.log"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "ruff format ${FILE_PATH} 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

### 4.2 보안 검증 스크립트 (scripts/validate-command.sh)
```bash
#!/bin/bash
# 위험한 명령어 차단
if echo "$CLAUDE_TOOL_PARAMS" | grep -qE "(rm -rf|dd if=|mkfs)"; then
  echo "위험한 명령어 감지됨" >&2
  exit 1
fi
exit 0
```

---

## 5. 설정 백업 및 복원

### 5.1 Git을 통한 버전 관리

**.gitignore 설정**
```gitignore
# Claude 개인 설정
.claude/local/
.claude/*.log
.claude/.cache/

# 환경 변수
.env
.env.local

# MCP 인증 정보
.claude/.mcp-auth.json
```

**설정 커밋**
```bash
# Claude 설정 추가
git add .claude/
git commit -m "feat: Claude Code 프로젝트 설정 추가"
git push origin main
```

### 5.2 설정 내보내기 스크립트
```bash
#!/bin/bash
# scripts/export-claude-config.sh

BACKUP_DIR="claude-backup-$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"

# 프로젝트 설정 복사
cp -r .claude/ "$BACKUP_DIR/"

# 사용자 설정 복사
cp -r ~/.claude/ "$BACKUP_DIR/user-claude/"

# 환경 변수 템플릿 생성
cat > "$BACKUP_DIR/.env.template" << EOF
# Database
DATABASE_URL=

# API Keys
OPENAI_API_KEY=
GITHUB_TOKEN=

# MCP Servers
MONITORING_API_URL=
MONITORING_API_KEY=
EOF

# 압축
tar -czf "$BACKUP_DIR.tar.gz" "$BACKUP_DIR"
rm -rf "$BACKUP_DIR"

echo "백업 완료: $BACKUP_DIR.tar.gz"
```

---

## 6. 환경 이동 가이드

### 6.1 새 환경 설정 (신규 PC)

**1단계: Claude Code 설치**
```bash
# Windows (PowerShell)
winget install Anthropic.ClaudeCode

# macOS
brew install claude-code

# Linux
curl -fsSL https://claude.ai/install.sh | sh
```

**2단계: 프로젝트 클론**
```bash
git clone https://github.com/username/project.git
cd project
```

**3단계: 환경 변수 설정**
```bash
# .env 파일 생성
cp .env.template .env
# 편집기로 .env 파일 열어 값 입력
```

**4단계: MCP 서버 재설치**
```bash
# 프로젝트 MCP 설정 적용
claude mcp sync

# 또는 개별 설치
claude mcp add --transport http github https://api.github.com/mcp
```

**5단계: 사용자 설정 복원**
```bash
# 사용자 Claude 설정 복사
cp -r backup/user-claude/ ~/.claude/
```

### 6.2 자동화 스크립트
```bash
#!/bin/bash
# scripts/setup-claude.sh

echo "Claude Code 환경 설정 시작..."

# 1. 의존성 확인
if ! command -v claude &> /dev/null; then
    echo "Claude Code가 설치되지 않았습니다."
    exit 1
fi

# 2. 프로젝트 설정 확인
if [ ! -d ".claude" ]; then
    echo ".claude 디렉토리가 없습니다."
    exit 1
fi

# 3. 환경 변수 설정
if [ ! -f ".env" ]; then
    cp .env.template .env
    echo ".env 파일이 생성되었습니다. 필요한 값을 입력하세요."
    exit 0
fi

# 4. MCP 서버 동기화
echo "MCP 서버 설정 중..."
claude mcp sync

# 5. Hook 스크립트 실행 권한
chmod +x scripts/*.sh

echo "Claude Code 설정 완료!"
```

---

## 7. 베스트 프랙티스

### 7.1 프로젝트 구조 표준화
```
프로젝트/
├── .claude/
│   ├── CLAUDE.md           # 메인 메모리
│   ├── rules/              # 규칙 모듈
│   ├── settings.json       # Hooks 및 설정
│   └── .mcp.json          # MCP 서버
├── scripts/
│   ├── setup-claude.sh     # 설정 스크립트
│   └── validate-*.sh       # 검증 스크립트
└── docs/
    └── CLAUDE_GUIDE.md     # 팀 가이드
```

### 7.2 팀 협업 가이드
```markdown
# docs/CLAUDE_GUIDE.md

## 팀 Claude Code 사용 가이드

### 초기 설정
1. `scripts/setup-claude.sh` 실행
2. `.env` 파일에 개인 토큰 입력
3. `claude mcp sync` 실행

### 규칙 추가 방법
1. `.claude/rules/` 디렉토리에 새 MD 파일 생성
2. YAML frontmatter로 적용 경로 지정
3. `.claude/CLAUDE.md`에서 임포트

### 커밋 전 체크리스트
- [ ] `.env` 파일이 .gitignore에 포함되었는가?
- [ ] 개인 정보가 설정 파일에 없는가?
- [ ] 새로운 MCP 서버 문서화했는가?
```

### 7.3 보안 고려사항

**민감 정보 관리**
```json
// .claude/settings.json
{
  "env": {
    "API_KEY": "${API_KEY}",  // 환경 변수 참조
    "TOKEN": "${GITHUB_TOKEN}"
  }
}
```

**권한 제한**
```json
{
  "permissions": {
    "allowedTools": ["Read", "Write", "Edit"],
    "blockedPaths": [
      "**/.env",
      "**/*secret*",
      "**/*password*"
    ]
  }
}
```

### 7.4 성능 최적화

**메모리 최적화**
- 규칙을 모듈로 분리
- 경로별 규칙 적용
- 불필요한 컨텍스트 제거

**MCP 서버 최적화**
- HTTP 서버 우선 사용
- 필요한 서버만 활성화
- 캐싱 활용

---

## 🚀 빠른 시작 체크리스트

### 새 프로젝트 설정
- [ ] `.claude/` 디렉토리 생성
- [ ] `CLAUDE.md` 작성
- [ ] 필요한 rules 파일 생성
- [ ] `settings.json` 구성
- [ ] MCP 서버 설정
- [ ] Git에 커밋

### 환경 이동 시
- [ ] 프로젝트 클론
- [ ] Claude Code 설치
- [ ] 환경 변수 설정
- [ ] MCP 서버 동기화
- [ ] Hook 스크립트 권한 설정

### 일일 사용
- [ ] `git pull`로 최신 설정 동기화
- [ ] 필요시 MCP 서버 새로고침
- [ ] 메모리 파일 업데이트
- [ ] 변경사항 커밋

---

## 📚 추가 리소스

- [Claude Code 공식 문서](https://code.claude.com/docs)
- [MCP 프로토콜 문서](https://modelcontextprotocol.io)
- [Claude Code GitHub](https://github.com/anthropics/claude-code)
- [커뮤니티 MCP 서버](https://github.com/modelcontextprotocol/servers)

---

이 가이드를 따라 Claude Code를 완벽하게 설정하고, 팀과 공유하며, 어떤 환경에서도 일관된 개발 경험을 유지할 수 있습니다.
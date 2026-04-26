# Claude Code Skills / Agents / Hooks 작성 가이드

공식 문서 기반 레퍼런스. 출처: https://code.claude.com/docs/ko/skills · /ko/sub-agents · /ko/hooks

> 이 문서는 "어떻게 만들까?"의 답을 한 파일에 모아둔 실전 치트시트입니다.
> 스킬/에이전트/훅을 이 프로젝트에 추가할 때 항상 이 파일을 먼저 확인하세요.

---

## 0. 무엇을 언제 쓰는가

| 선택지 | 쓸 때 | 쓰지 말 때 |
|---|---|---|
| **Skill** | 주 대화 컨텍스트에서 적용할 **규칙/플레이북/작업 스크립트**. `/name`으로 호출하거나 Claude가 자동 활성화 | 매 응답마다 항상 로드되어야 하는 건 CLAUDE.md에 |
| **Subagent** | **격리된 컨텍스트**에서 독립 실행이 필요한 작업(대량 탐색, 병렬 조사, 권한 제한) | 연속 왕복이 필요한 작업은 주 대화에서 |
| **Hook** | 도구 실행 전/후 같은 **라이프사이클 자동화**(검증, 린트, 로깅). Claude가 아니라 **하네스(harness)** 가 실행 | "앞으로 X할 때는 Y하세요" 같은 규칙은 메모리/CLAUDE.md에 |

핵심 차이: Skill/Agent는 **프롬프트 기반**(Claude가 지침을 읽고 판단), Hook은 **결정론적 실행**(셸/HTTP 명령이 강제됨).

---

## 1. Skills

### 1.1 위치와 우선순위

| 범위 | 경로 | 적용 대상 |
|---|---|---|
| Enterprise | 관리 설정 디렉토리 | 조직 전체 |
| Personal | `~/.claude/skills/<name>/SKILL.md` | 내 모든 프로젝트 |
| **Project** | **`.claude/skills/<name>/SKILL.md`** | 이 프로젝트만 (팀 공유 가능, 버전관리에 커밋) |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | 플러그인 활성 위치 |

같은 이름이 여러 범위에 있으면 **enterprise > personal > project** 우선. 플러그인은 `plugin-name:skill-name` 네임스페이스라 충돌 없음.

모노레포는 서브디렉토리의 `.claude/skills/`도 자동 검색 (예: `packages/frontend/.claude/skills/`).

### 1.2 디렉토리 구조

```
.claude/skills/my-skill/
├── SKILL.md           # 필수 진입점
├── reference.md       # 선택: 상세 레퍼런스 (필요 시에만 로드)
├── examples/
│   └── sample.md      # 예시 출력
└── scripts/
    └── helper.py      # 실행용 스크립트 (컨텍스트에 로드되지 않음)
```

`SKILL.md`는 **500줄 이하**로 유지. 무거운 참조 자료는 별도 파일로 분리하고 `[reference.md](reference.md)` 링크로 연결 → Claude가 필요할 때만 Read 함.

### 1.3 SKILL.md 프론트매터 전체 레퍼런스

```yaml
---
name: my-skill                      # 소문자/숫자/하이픈, 최대 64자. 생략 시 디렉토리명
description: ...                    # ★ 가장 중요. Claude가 자동 활성화할지 결정
disable-model-invocation: false     # true면 사용자만 /name으로 호출 가능 (Claude 자동 호출 차단)
user-invocable: true                # false면 / 메뉴에서 숨김 (Claude만 사용)
argument-hint: "[issue-number]"     # 자동완성 힌트
allowed-tools: Read Grep Glob       # 이 스킬 활성 시 권한 프롬프트 없이 쓸 도구 (공백/YAML 리스트)
model: sonnet                       # 이 스킬 활성 시 사용할 모델
effort: high                        # low | medium | high | max (Opus 4.6 전용)
context: fork                       # subagent 컨텍스트에서 실행
agent: Explore                      # context:fork일 때 사용할 subagent 종류
paths: "src/api/**/*.py"            # glob. 해당 파일 작업 시에만 자동 활성화
shell: bash                         # bash(기본) | powershell
hooks:                              # 이 스킬 수명 주기에 스코프된 hook
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/check.sh"
---

여기부터 본문 (markdown). Claude가 스킬 호출 시 읽는 지침.
```

**`name`, `description` 외엔 전부 선택**. `description` 하나만 잘 써도 대부분 동작함.

#### description 작성 규칙 (중요)
- **사용자가 자연스럽게 말할 키워드**를 앞에 배치
- 250자를 넘으면 스킬 목록에서 **잘려서** Claude에게 노출됨 → 핵심 먼저
- "언제 사용" 문구 포함: "Use when ...", "... 코드 리뷰가 필요할 때 사용하세요"
- 예시:
  ```yaml
  description: Explains code with visual diagrams and analogies. Use when explaining how code works, teaching about a codebase, or when the user asks "how does this work?"
  ```

### 1.4 콘텐츠 타입 2가지

**참조형(reference)** — 규칙/패턴/스타일. Claude가 현재 대화에 인라인으로 적용.
```yaml
---
name: api-conventions
description: API design patterns for this codebase
---
When writing API endpoints:
- Use RESTful naming
- Return consistent error formats
```

**작업형(task)** — 배포/커밋/코드 생성 등 단계별 지시. 대개 `disable-model-invocation: true`.
```yaml
---
name: deploy
description: Deploy to production
disable-model-invocation: true
---
1. Run tests
2. Build
3. Push to deploy target
```

### 1.5 인수 전달

| 치환자 | 의미 |
|---|---|
| `$ARGUMENTS` | 전체 인수 문자열 |
| `$ARGUMENTS[0]`, `$0` | 첫 번째 인수 (공백 분리) |
| `$1`, `$2` | 이후 인수 |
| `${CLAUDE_SESSION_ID}` | 현재 세션 ID |
| `${CLAUDE_SKILL_DIR}` | SKILL.md가 있는 디렉토리 절대경로 |

```yaml
---
name: migrate-component
description: Migrate component between frameworks
---
Migrate $0 from $1 to $2. Preserve behavior and tests.
```
`/migrate-component SearchBar React Vue` → `$0=SearchBar $1=React $2=Vue`.

`$ARGUMENTS`를 본문에 안 써도 Claude Code가 `ARGUMENTS: <value>`를 끝에 추가함.

### 1.6 동적 컨텍스트 주입: `` !`<cmd>` ``

스킬 본문의 `` !`cmd` `` 는 Claude에게 전달되기 **전에** 셸에서 실행되고 출력으로 치환됨. Claude는 명령이 아닌 결과만 봄.

```yaml
---
name: pr-summary
description: Summarize current pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---
## PR 컨텍스트
- Diff: !`gh pr diff`
- Comments: !`gh pr view --comments`
- Files: !`gh pr diff --name-only`

위 내용을 요약하세요...
```

### 1.7 Subagent에서 스킬 실행 (`context: fork`)

스킬을 **격리된 컨텍스트**에서 돌릴 때. 스킬 본문이 subagent의 프롬프트가 됨. 대화 기록 접근 불가.

```yaml
---
name: deep-research
description: Research a topic thoroughly in isolation
context: fork
agent: Explore            # 또는 Plan / general-purpose / 사용자 정의 agent
---
$ARGUMENTS 를 조사:
1. Glob/Grep으로 관련 파일 찾기
2. 코드 읽고 분석
3. 파일 경로와 함께 요약
```

⚠️ `context: fork`는 **실행 가능한 지시**가 있는 스킬에만 의미 있음. "이 규칙을 따르세요" 같은 참조형 내용만 있으면 subagent가 할 일이 없어 빈 결과 반환.

### 1.8 호출 제어 요약

| 프론트매터 | 사용자 `/name` | Claude 자동 호출 | 설명 컨텍스트 로드 |
|---|---|---|---|
| (기본) | ✅ | ✅ | 항상 |
| `disable-model-invocation: true` | ✅ | ❌ | ❌ (사용자 호출 시에만) |
| `user-invocable: false` | ❌ | ✅ | 항상 |

### 1.9 확장 사고 켜기
스킬 본문 어디든 "**ultrathink**" 단어를 포함시키면 확장 사고 활성화.

### 1.10 스킬 안에서 상세 파일 참조

```markdown
## 참고 자료
- 전체 API 명세는 [reference.md](reference.md) 참고
- 사용 예시는 [examples.md](examples.md) 참고
- 검증 스크립트: `${CLAUDE_SKILL_DIR}/scripts/validate.sh`
```

### 1.11 체크리스트 (스킬 만들 때)

- [ ] `description`에 사용 시점 키워드가 담겼는가 (250자 이내)
- [ ] `name`은 소문자·하이픈인가
- [ ] 본문 500줄 이하, 무거운 레퍼런스는 별도 파일
- [ ] 파괴적 작업인가? → `disable-model-invocation: true`
- [ ] 읽기 전용만 필요한가? → `allowed-tools: Read Grep Glob`
- [ ] 대량 탐색인가? → `context: fork`, `agent: Explore`
- [ ] 스크립트 호출 시 `${CLAUDE_SKILL_DIR}` 사용했는가 (상대경로 금지)

---

## 2. Subagents (에이전트)

### 2.1 내장 에이전트 (이미 사용 가능)

| 에이전트 | 모델 | 용도 |
|---|---|---|
| `Explore` | Haiku | 읽기 전용 코드베이스 탐색, 파일 검색 |
| `Plan` | 상속 | Plan 모드에서 컨텍스트 수집 |
| `general-purpose` | 상속 | 탐색+수정 복합 작업 |
| `statusline-setup` | Sonnet | `/statusline` 구성 |
| `Claude Code Guide` | Haiku | Claude Code 기능 질문 |

`Agent` 도구 호출 시 `subagent_type` 로 지정.

### 2.2 사용자 정의 에이전트 위치

| 경로 | 범위 | 우선순위 |
|---|---|---|
| 관리 설정 | 조직 | 1 (최고) |
| `--agents` CLI 플래그 | 세션 | 2 |
| **`.claude/agents/<name>.md`** | **프로젝트** | 3 |
| `~/.claude/agents/<name>.md` | 사용자 | 4 |
| 플러그인 `agents/` | 플러그인 | 5 |

에이전트 파일 추가 후엔 세션 재시작 또는 `/agents`로 즉시 로드.

### 2.3 에이전트 파일 형식

```markdown
---
name: code-reviewer                 # 필수
description: Expert code reviewer. Use proactively after code changes.  # 필수
tools: Read, Grep, Glob, Bash       # 생략 시 상위 도구 상속
disallowedTools: Write, Edit        # 블랙리스트
model: sonnet                       # sonnet | opus | haiku | 전체 ID | inherit
permissionMode: default             # default | acceptEdits | auto | dontAsk | bypassPermissions | plan
maxTurns: 20
skills:                             # 시작 시 스킬 콘텐츠를 시스템 프롬프트에 주입
  - api-conventions
  - error-handling-patterns
mcpServers:                         # 이 에이전트 전용 MCP
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  - github                          # 문자열은 기존 서버 참조
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
memory: project                     # user | project | local (지속 메모리 디렉토리)
background: false                   # true면 항상 백그라운드
effort: high
isolation: worktree                 # 임시 git worktree에서 실행
color: blue
initialPrompt: ""                   # --agent로 실행 시 자동 제출 프롬프트
---

당신은 시니어 코드 리뷰어입니다. 호출되면:
1. git diff로 최근 변경 확인
2. 수정된 파일에 집중
3. 즉시 리뷰 시작

리뷰 체크리스트:
- 가독성, 네이밍, 중복 제거
- 에러 핸들링, 시크릿 노출
- 입력 검증, 테스트 커버리지

우선순위별 출력:
- Critical (반드시 수정)
- Warning (수정 권장)
- Suggestion (개선 고려)
```

`tools`, `disallowedTools` 모두 지정 시 **disallowed가 먼저** 적용되고 나머지에 대해 `tools`가 해석됨.

### 2.4 호출 방법

```text
# 자연어 — Claude가 위임 여부 판단
Use the code-reviewer subagent to review the auth changes

# @-mention — 특정 에이전트 강제
@"code-reviewer (agent)" look at the auth changes

# 세션 전체를 에이전트로
claude --agent code-reviewer

# 프로젝트 기본 에이전트
# .claude/settings.json
{ "agent": "code-reviewer" }
```

### 2.5 에이전트 vs 주 대화 선택

**주 대화**: 왕복 필요, 여러 단계가 컨텍스트 공유, 작고 빠른 변경, 지연 중요.
**Subagent**: 출력 방대함, 도구 제한 적용, 자체 완결, 요약만 필요.
**Skill**: 재사용 프롬프트/워크플로우가 **주 컨텍스트**에서 실행되어야 할 때.

⚠️ Subagent는 다른 subagent를 생성할 수 없음. 중첩 위임이 필요하면 Skill 또는 순차 체이닝.

---

## 3. Hooks

Hooks는 **하네스가 실행하는 결정론적 자동화**. "~할 때 자동으로 Y하세요"를 구현하는 유일한 방법.

### 3.1 설정 위치

| 파일 | 범위 | 버전관리 |
|---|---|---|
| `~/.claude/settings.json` | 모든 프로젝트 | ✗ |
| `.claude/settings.json` | 프로젝트 | ✓ |
| `.claude/settings.local.json` | 프로젝트 (개인) | ✗ |
| 스킬/에이전트 `frontmatter.hooks` | 해당 스킬·에이전트 수명만 | ✓ (파일과 함께) |

### 3.2 이벤트 종류

| 이벤트 | 발생 시점 | Matcher 입력 |
|---|---|---|
| `SessionStart` | 세션 시작/재개 | (없음) |
| `UserPromptSubmit` | 사용자 입력 제출 | (없음) |
| `PreToolUse` | 도구 실행 **전** | 도구 이름 |
| `PostToolUse` | 도구 성공 **후** | 도구 이름 |
| `Stop` | Claude 응답 완료 | (없음) |
| `SubagentStart` / `SubagentStop` | Subagent 시작/종료 | 에이전트 이름 |
| `SessionEnd` | 세션 종료 | (없음) |
| `CwdChanged` | 작업 디렉토리 변경 | (없음) |

스킬·에이전트 frontmatter의 `Stop`은 런타임에 자동으로 `SubagentStop`으로 변환.

### 3.3 기본 구조

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/validate.sh",
            "async": false,
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### 3.4 Matcher 패턴

```json
"matcher": "Bash"           // 정확히 Bash
"matcher": "Edit|Write"     // Edit 또는 Write
"matcher": "mcp__.*__.*"    // 모든 MCP 도구 (정규식)
```

### 3.5 Hook 타입 4가지

**command** — 가장 일반적. stdin으로 JSON 수신, exit code 또는 JSON 출력으로 응답.
```bash
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if echo "$COMMAND" | grep -qE 'rm -rf|dd if='; then
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "Destructive command blocked"
    }
  }'
fi
exit 0
```

**http**
```json
{ "type": "http", "url": "http://localhost:8080/validate",
  "headers": { "Authorization": "Bearer $TOKEN" },
  "allowedEnvVars": ["TOKEN"] }
```

**prompt** — LLM 판단
```json
{ "type": "prompt",
  "prompt": "Should Claude continue? Context: $ARGUMENTS",
  "model": "claude-haiku-4-5-20251001",
  "timeout": 30 }
```
응답: `{"ok": true}` 또는 `{"ok": false, "reason": "..."}`.

**agent** — 서브에이전트에게 위임
```json
{ "type": "agent", "prompt": "Verify the changes: $ARGUMENTS" }
```

### 3.6 종료 코드 규약

| Exit code | 의미 |
|---|---|
| 0 | 성공 (통과) |
| 2 | **차단** — stderr 메시지가 Claude에게 피드백 |
| 그 외 | 실패 (비차단 에러) |

### 3.7 결정 제어 JSON 출력

**PreToolUse**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask|defer",
    "permissionDecisionReason": "...",
    "updatedInput": { "command": "npm run lint" }
  }
}
```

**Stop** (Claude 계속 여부)
```json
{ "decision": "block", "reason": "Tests must pass first" }
```

**UserPromptSubmit** (컨텍스트 주입)
```json
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "Project uses TypeScript v5"
  }
}
```

### 3.8 스킬/에이전트 안에서 Hook

```yaml
---
name: secure-task
description: Execute with security checks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "${CLAUDE_SKILL_DIR}/security-check.sh"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "${CLAUDE_SKILL_DIR}/run-linter.sh"
---
```

이 hook은 해당 스킬/에이전트가 **활성화된 동안만** 실행되고 끝나면 정리됨.

### 3.9 디버깅

- `/hooks` 메뉴에서 구성된 hook 확인
- `Ctrl+O`로 Verbose 출력 보기
- `jq`로 stdin JSON 구조 테스트
- `.claude/settings.local.json`에 시험용 hook을 두고 검증 후 공유 설정으로 이동

---

## 4. 이 프로젝트 현황

### 현재 스킬 (`.claude/skills/`)
- `fastapi-reviewer/` — FastAPI 프로덕션 코드 리뷰. 보조 레퍼런스 `project-context.md`에 이 저장소 고유 규칙(orjson·observability·UV) 분리.
- `performance-optimizer/` — FastAPI 성능 분석·최적화. 실제 벤치마크 스크립트(`tests/test_json_performance.py`, `benchmarks/`) 및 `/json/compare/{count}` 엔드포인트와 연결됨.
- `async-mentor/` — `fastapi-mastery/01-fundamentals/` 학습 전담 멘토. `paths`로 자동 활성화 제한, 읽기 전용, 정답 대신 힌트·소크라틱 질문으로 코칭.

### 스킬 간 라우팅 원칙
- 프로덕션 `app/` 코드 리뷰 → `fastapi-reviewer`
- 성능 수치·병목 분석 → `performance-optimizer`
- 학습자의 `01-fundamentals/` 코드 → `async-mentor`
- 서로의 스킬 본문에 "다른 스킬과의 관계" 섹션을 두어 교차 위임을 명시했음.

### 빠른 추가 레시피

**새 프로젝트 스킬 만들기**
```bash
mkdir -p .claude/skills/my-skill
# .claude/skills/my-skill/SKILL.md 작성 → frontmatter + 본문
# 즉시 /my-skill 로 호출 가능 (세션 재시작 불필요 — 라이브 감지)
```

**새 프로젝트 에이전트 만들기**
```bash
mkdir -p .claude/agents
# .claude/agents/my-agent.md 작성 → frontmatter + 시스템 프롬프트
# /agents 로 확인 후 @-mention 또는 자연어로 호출
```

**새 훅 추가**
```bash
mkdir -p .claude/hooks
# .claude/hooks/validate.sh 작성 (chmod +x)
# .claude/settings.json 의 "hooks" 섹션에 등록
```

---

## 5. 흔한 함정

- 🚫 **description에 일반적인 단어만 쓰기** → 자동 활성화 안 됨. 구체 키워드 필수.
- 🚫 **SKILL.md에 전부 몰아넣기** → 500줄 이상이면 잘림/컨텍스트 낭비. `reference.md`로 분리.
- 🚫 **`context: fork`를 참조형 스킬에 붙이기** → subagent가 할 일이 없어 빈 결과.
- 🚫 **훅 스크립트에서 상대경로 사용** → 작업 디렉토리 달라지면 깨짐. `$CLAUDE_PROJECT_DIR` / `${CLAUDE_SKILL_DIR}` 사용.
- 🚫 **파괴적 작업에 `disable-model-invocation` 빠뜨림** → Claude가 준비됐다고 판단해 자동 배포.
- 🚫 **에이전트가 다른 에이전트 생성 기대** → 불가능. 스킬 체이닝으로 해결.

---

## 6. 한 줄 요약

- **Skill**: 주 컨텍스트에서 쓰는 프롬프트형 플레이북. `description`이 전부.
- **Agent**: 격리된 컨텍스트에서 독립 실행. 도구/모델/권한을 좁힘.
- **Hook**: 하네스가 돌리는 결정론적 훅. 자동화·검증·차단의 유일한 수단.

**필요할 때 이 순서로 결정**: CLAUDE.md로 충분한가? → 아니면 Skill → 격리 필요하면 Agent → 강제 자동화면 Hook.

# specred

> 자연어 요구사항을 BDD 시나리오로, 시나리오를 실행 가능한 테스트 코드로. TDD의 Red 단계를 자동화합니다.

---

## 1. 프로젝트 개요

### 어떤 문제를 해결하나요?

TDD는 이상적인 개발 방법론입니다. 하지만 실무에서 TDD를 포기하게 되는 이유는 명확합니다.

- 테스트 작성에 드는 시간이 너무 많다
- 바쁘면 엣지케이스를 빠뜨린다
- 테스트를 작성했는데도 버그가 난다. 필드 존재 여부만 확인하고 값은 검증하지 않거나, 성공 케이스만 테스트하고 경계값을 빠뜨리거나, 트랜잭션 실패 시나리오를 놓치는 것처럼 — 알고 있어도 빠뜨리고, 미처 생각하지 못해서 누락된다.
- QA 팀이 없으면 테스트 전략 자체를 혼자 세워야 한다

**specred는 이 문제를 해결하는 CLI 도구입니다.**

요구사항을 포함한 문서 경로만 던져주면, AI가 유즈케이스를 생성하고, 실행 가능한 테스트 코드까지 자동으로 만들어냅니다.

이 과정에서 개발자는 **'검토'**만 합니다.

### 세 가지 철학

**TDD를 위한 BDD 프레임워크**
단순히 테스트 코드를 생성하는 것이 아닙니다. 자연어 요구사항 → 유즈케이스 → 테스트 코드로 이어지는 워크플로우 전체를 자동화합니다. 문서가 곧 테스트가 되고, 테스트가 곧 문서가 됩니다.

**QA 없이도 혼자서 가능**
QA 팀이 있어야만 촘촘한 테스트 전략을 세울 수 있다는 전제를 깹니다. AI가 산업 표준 기반으로 개발자가 놓친 엣지케이스까지 제안하고, 개발자는 의사결정만 합니다.

**TDD Red 단계까지 만들어주는 도구**
TDD의 Red 단계를 자동화합니다. 단순히 테스트 코드를 생성하는 것이 아닙니다. 테스트는 원래 검증 도구이자 문서입니다. specred가 만드는 테스트는 그 문서로서의 역할을 극대화합니다. 유즈케이스, 도메인 모델, 엣지케이스가 모두 담긴 테스트 코드는 AI가 구현을 생성할 때 가장 정확한 명세가 됩니다. 더 좋은 테스트가 더 좋은 구현을 만듭니다.

---

## 2. 기능 소개

| 기능 | 설명 |
|------|------|
| 유즈케이스 자동 생성 | 요구사항 문서를 분석해 Happy Path, 예외 케이스, 엣지케이스를 포함한 유즈케이스를 생성합니다 |
| Mermaid 다이어그램 | 생성된 유즈케이스를 `usecase.mmd` 파일로 저장합니다. 코드 기반이라 직접 수정 가능하고 GitHub/Notion에서 렌더링됩니다 |
| 검토 단계 양방향 수정 | 유즈케이스(`usecase.mmd`)와 도메인 모델(`domain.yml`) 검토 시, 파일을 직접 수정해 저장하거나 자연어로 명령하는 방식 모두 지원합니다 |
| 도메인/DTO 모델 확정 | 테스트 코드 생성 전, AI가 유즈케이스에서 도메인 모델과 DTO를 분리해 추출하고 개발자에게 확인받습니다. 이후 모든 테스트가 `domain.yml`을 single source of truth로 참조합니다 |
| 테스트 스타일 선택 | Behavior(Given-When-Then) 또는 Describe(describe/it 계층 구조) 중 선택 가능합니다 |
| 레이어별 테스트 생성 | Service, Repository, Controller, Integration 레이어 테스트를 한 번에 생성합니다. 모든 테스트는 외부 환경 없이 항상 실행 가능하도록 설계됩니다 |
| 역질문 | 룰을 적용하거나 테스트를 설계하는 도중 판단이 필요한 지점에서 자동으로 멈추고 개발자에게 질문합니다. 외부 서비스 통합이 필요한 경우 별도로 확인합니다 |
| watch 모드 | `usecase.mmd`, `domain.yml` 파일 저장을 자동으로 감지해 수정사항을 즉시 반영합니다 |
| 마크다운 리포트 | 유즈케이스별 테스트 매핑, 커버리지, 미포함 케이스를 `specred-report.md`로 생성합니다 |
| 피드백 자동 반영 | 텍스트 명령으로 변경사항을 지시하면 오케스트레이터가 영향 범위를 판단해 필요한 에이전트만 호출하고, 테스트 코드와 문서를 함께 업데이트합니다 |
| 설정 파일 재사용 | `specred.yml`로 테스트 스타일, 언어, 프레임워크, 커스텀 룰을 저장해 재사용합니다. 입력 문서는 요구사항 명세서만 필수이며, API 스펙과 도메인 모델 문서는 있으면 참고하고 없으면 AI가 추론해 생성합니다 |

---

## 3. 동작 방식

### 사용자가 할 수 있는 것

```
요구사항 문서(.md) 또는 API 스펙(.yaml) 파일 경로를 입력한다
    ↓
생성된 유즈케이스를 검토하고 OK 또는 수정한다
    ↓
도메인 모델 초안을 확인하고 확정한다
    ↓
테스트 코드를 검토한다
    ↓
텍스트로 변경사항을 지시한다
```

개발자가 하는 일은 전부 **검토와 의사결정**입니다. 작성은 AI가 합니다.

### 내부 에이전트 구조

```
사용자 입력 (파일 경로)
        │
        ▼
┌─────────────────────┐
│  Orchestrator Agent │  전체 흐름 제어, 상태 관리
└──────────┬──────────┘
           │
    ┌──────┴───────┐
    │              │
    ▼              ▼
Analyzer       UseCase Agent
요구사항 파싱   유즈케이스 + Mermaid 생성
                    │
                    ▼
         [개발자 검토 - 유즈케이스]
         파일 수정: usecase.mmd 저장 시 자동 감지
         자연어 수정: "3번 삭제하고 동시 가입 추가해줘"
                    │
                    ▼
             Domain Agent
             도메인 모델 / DTO 분리 추출
                    │
                    ▼
         [개발자 검토 - 도메인 모델]
         파일 수정: domain.yml 저장 시 자동 감지
         자연어 수정: "User에 nickname 필드 추가해줘"
                    │
                    ▼
            TestGen Agent
            테스트 코드 생성
            (룰 적용 중 판단 필요 시 역질문)
                    │
                    ▼
           DocWriter Agent
           specred-report.md 생성
                    │
                    ▼
              [개발자 검토]
              피드백 입력
                    │
                    ▼
         Orchestrator가 영향 범위 판단
         → 필요한 에이전트만 호출해 반영
```

### 해결한 핵심 문제: 도메인 모델 일관성

Kent Beck의 엄격한 TDD는 **"테스트를 먼저 작성함으로써 구현 전에 인터페이스를 강제로 고민하게 만드는 것"** 을 목표로 설계됐습니다. 테스트를 짜면서 도메인 모델이 자연스럽게 정의되는 방식입니다.

그런데 여기에는 문제가 있습니다. 테스트를 여러 개 짜다 보면 초반 테스트와 나중 테스트에서 같은 도메인 모델을 다르게 정의하는 일이 생깁니다. `User`의 비밀번호 필드가 어떤 테스트에선 `password`이고, 다른 테스트에선 `hashedPassword`인 식으로요.

AI 역시 동일한 문제를 가집니다. `UserServiceTest`와 `UserRepositoryTest`를 각각 생성하면 같은 `User` 모델을 서로 다르게 정의할 수 있습니다. 테스트끼리 일관성이 없으면 실제 구현 시 "어느 게 맞는 거지?" 혼란이 생깁니다.

specred는 이 문제를 **도메인 모델 확정 단계**로 해결합니다. 테스트 코드 생성 전에 AI가 유즈케이스에서 도메인 모델 초안을 추출하고, 개발자가 이를 확정합니다. 이후 모든 테스트 코드가 `domain.yml`을 single source of truth로 참조해서 생성되므로 일관성이 보장됩니다.

TDD의 핵심 가치인 "구현 전에 인터페이스를 고민한다"는 도메인 확정 단계에서 동일하게 달성됩니다. 순서가 바뀌었을 뿐, 고민의 깊이는 같습니다.

---

## 4. 사용자 관점 사용 흐름

### 설치

```bash
pip install specred
```

### 초기 설정

```bash
specred init
```

실행하면 다음 두 가지가 생성됩니다.

**`~/.specred/config.yml`** — API 키 저장 (최초 1회)
```yaml
anthropic_api_key: sk-ant-...

# 사용할 Claude 모델 (기본값: claude-sonnet-4-6)
# claude-opus-4-6    : 가장 정확, 복잡한 도메인에 적합
# claude-sonnet-4-6  : 균형 잡힌 성능 (권장)
# claude-haiku-4-5   : 빠르고 저렴, 간단한 요구사항에 적합
model: claude-sonnet-4-6
```

**`./specred.yml`** — 프로젝트 설정 (프로젝트마다)
```yaml
# 테스트 스타일을 선택하세요 (기본값: behavior)
# behavior: Given-When-Then 구조
# describe: describe/it 계층 구조
test:
  style: behavior

# 개발 언어 (기본값: java)
  language: java

# 테스트 프레임워크 (기본값: junit5)
# java: junit5 | kotlin: kotest | python: pytest | javascript: jest
  framework: junit5

# 커버리지 목표 (기본값: 90)
# coverage_target: 90

# 기본 룰 (항상 적용됩니다)
# - 일대다/다대다 관계는 연관된 데이터 내용까지 검증한다
# - 모든 테스트는 외부 환경 없이 항상 실행 가능해야 한다
#     DB: 인메모리 DB(@Transactional 롤백), 외부 서비스: WireMock/Stub
# - 외부 서비스 호출은 Mock 단위 테스트를 기본으로 작성하고,
#     통합 테스트는 Sandbox/Stub 서버를 가정해 설계한다
#     실제 호출 가능 여부는 생성 중 개발자에게 확인한다
# - 트랜잭션이 있는 경우 롤백 시나리오를 반드시 테스트한다
# - Null, Empty, 경계값은 항상 테스트한다
# - 룰 적용 중 판단이 필요한 지점에서는 진행을 멈추고 개발자에게 역질문한다
#
# 추가 룰이 필요하면 자연어로 작성하세요:
# rules:
#   - "페이지네이션이 있는 경우 빈 페이지와 마지막 페이지를 테스트한다"
```

### 테스트 코드 생성

```bash
# 요구사항 명세서만 있는 경우 (최소)
specred generate --requirement ./docs/signup.md

# API 스펙도 있는 경우
specred generate --requirement ./docs/signup.md --api-spec ./openapi/signup.yaml

# 도메인 모델 문서도 있는 경우 (도메인 확정 단계 생략)
specred generate --requirement ./docs/signup.md --domain ./docs/domain.md
```

`specred.yml`이 있으면 자동으로 설정을 읽어 실행합니다. 없으면 테스트 스타일 등을 질문합니다.

### 실행 흐름

```
[1/5] 요구사항 분석 중...

[2/5] 유즈케이스 생성 완료 → usecase.mmd

  유즈케이스를 확인하세요.
  파일을 수정하고 저장하면 자동으로 반영됩니다.
  자연어로 수정하려면 입력하세요. 그대로 진행하려면 [o]: o

[3/5] 도메인 모델 / DTO 초안 → domain.yml

  [domains]
  User
    - email: String
    - password: String
    - createdAt: LocalDateTime

  [dtos]
  SignupRequest
    - email: String
    - password: String
    - confirmPassword: String

  파일을 수정하고 저장하면 자동으로 반영됩니다.
  자연어로 수정하려면 입력하세요. 그대로 진행하려면 [o]: o

[4/5] 테스트 코드 생성 중...

  [역질문] 이메일 발송 서비스는 Sandbox 환경이 있나요?
  있으면 통합 테스트를 설계합니다. (y/n): y

  [역질문] 결제 서비스는 Sandbox 환경이 있나요? (y/n): n
  → Mock 기반 단위 테스트만 설계합니다.

[5/5] 완료

  생성된 파일:
    src/test/java/com/example/user/UserSignupServiceTest.java
    src/test/java/com/example/user/UserRepositoryTest.java
    src/test/java/com/example/user/UserSignupControllerTest.java
    src/test/java/com/example/user/UserSignupIntegrationTest.java
    specred-report.md
```

### 피드백 반영

```bash
specred feedback "동시 가입 테스트 추가해줘"
specred feedback "비밀번호 암호화는 Service 레이어에서 처리해"
```

테스트 코드와 `specred-report.md`가 함께 업데이트됩니다.

### CLI 명령어 전체

| 명령어 | 설명 |
|--------|------|
| `specred init` | 설정 파일 초기화 |
| `specred generate` | 테스트 코드 생성 |
| `specred review` | 유즈케이스 커버리지 요약 출력 |
| `specred review --docs` | `specred-report.md` 생성 |
| `specred feedback "..."` | 변경사항 반영 |

### 주요 플래그

| 플래그 | 설명 | 예시 |
|--------|------|------|
| `--requirement` | 요구사항 문서 경로 (필수) | `./docs/signup.md` |
| `--api-spec` | API 스펙 파일 경로 (선택) | `./openapi/signup.yaml` |
| `--domain` | 도메인 모델 문서 경로 (선택, 있으면 확정 단계 생략) | `./docs/domain.md` |
| `--model` | 모델 오버라이드 | `claude-opus-4-6` \| `claude-sonnet-4-6` \| `claude-haiku-4-5` |
| `--style` | 테스트 스타일 오버라이드 | `behavior` \| `describe` |
| `--lang` | 언어 오버라이드 | `java` \| `kotlin` \| `python` \| `javascript` |
| `--framework` | 프레임워크 오버라이드 | `junit5` \| `kotest` \| `pytest` \| `jest` |

---

## 5. 기술 스택

| 분류 | 기술 | 용도 |
|------|------|------|
| 언어 | Python 3.11+ | CLI 구현 |
| CLI 프레임워크 | Typer | 명령어 파싱, 인터랙션 |
| AI | Anthropic Claude API | 유즈케이스/테스트 코드 생성 |
| 기본 모델 | claude-sonnet-4-6 | 균형 잡힌 성능 (변경 가능) |
| 파일 감시 | watchdog | `usecase.mmd`, `domain.yml` 변경 자동 감지 |
| 설정 파싱 | PyYAML | `specred.yml`, `domain.yml` |
| 문서 생성 | Jinja2 | Mermaid, Markdown 템플릿 |
| 패키징 | pyproject.toml | `pip install specred` |

---

## 6. 프로젝트 구조

```
specred/
├── cli/
│   ├── main.py                  # 진입점
│   └── commands/
│       ├── init.py              # specred init
│       ├── generate.py          # specred generate
│       ├── review.py            # specred review
│       └── feedback.py          # specred feedback
│
├── agents/
│   ├── orchestrator.py          # 전체 흐름 제어
│   ├── analyzer.py              # 요구사항 파싱
│   ├── usecase_agent.py         # 유즈케이스 + Mermaid 생성
│   ├── domain_agent.py          # 도메인 모델 추출 및 확정
│   ├── testgen_agent.py         # 테스트 코드 생성 + 역질문 처리
│   └── docwriter_agent.py       # specred-report.md 생성
│
├── mcp/
│   ├── filesystem.py            # 파일 읽기/쓰기
│   ├── watcher.py               # 파일 변경 감지
│   └── coverage.py              # 커버리지 결과 파싱
│
├── prompts/                     # 에이전트별 프롬프트 + few-shot 예시
│   ├── usecase.py
│   ├── domain.py
│   └── testgen/
│       ├── behavior.py
│       └── describe.py
│
└── templates/                   # Mermaid, Markdown 템플릿
    ├── usecase.mmd.j2
    └── report.md.j2

~/.specred/
└── config.yml                   # API 키 (전역)

프로젝트 루트/
├── specred.yml                  # 테스트 스타일, 룰 (프로젝트별)
├── usecase.mmd                  # 생성된 유즈케이스 다이어그램
├── domain.yml                   # 확정된 도메인 모델
└── specred-report.md            # 테스트 리포트
```

---

## 학습 목표

- 에이전트 오케스트레이션
- 워크플로우를 만들어서 개발자는 검토만 하면 되는 구조를 만들기
- MCP 적용해보기

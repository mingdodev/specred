# specred — CLAUDE.md

## 프로젝트 목적

자연어 요구사항을 BDD 시나리오로, 시나리오를 실행 가능한 테스트 코드로 변환하는 CLI 도구.
TDD의 Red 단계(실패하는 테스트 작성)를 자동화해, 개발자는 검토와 의사결정만 한다.

**핵심 문제 해결:**
- 테스트 작성 시간 절감
- AI가 생성하는 다수의 테스트 파일 간 도메인 모델 일관성 보장 (`domain.yml` = single source of truth)
- QA 없이도 엣지케이스까지 커버하는 테스트 전략 수립

---

## 설계 원칙

### 1. 도메인 모델 일관성 우선
테스트 코드 생성 전 반드시 `domain.yml`을 확정한다. 모든 테스트는 이 파일만 참조해 모델을 정의한다.
`UserServiceTest`와 `UserRepositoryTest`가 `User.password`를 다르게 정의하는 문제를 방지한다.

### 2. 항상 실행 가능한 테스트
외부 환경 의존 없이 로컬에서 항상 실행 가능해야 한다.
- DB: 인메모리 DB + `@Transactional` 롤백
- 외부 서비스: WireMock / Stub
- 외부 서비스 Sandbox 여부는 생성 중 개발자에게 역질문으로 확인

### 3. 검토는 개발자, 작성은 AI
개발자는 생성된 결과를 검토하고 OK/수정만 한다.
수정 방법은 두 가지를 모두 지원한다:
- 파일 직접 수정 후 저장 → watchdog이 감지해 자동 반영
- 자연어 명령 입력 → AI가 반영

### 4. 기본 룰 (항상 적용)
- 일대다/다대다 관계: 연관 데이터 내용까지 검증
- 트랜잭션 있으면 롤백 시나리오 필수
- Null, Empty, 경계값 항상 테스트
- 외부 서비스: Mock 단위 테스트 기본, Sandbox 있으면 통합 테스트 추가
- 판단이 필요한 지점에서는 멈추고 역질문

---

## 에이전트 구조

```
사용자 입력 (파일 경로)
        │
        ▼
┌─────────────────────┐
│  Orchestrator Agent │  전체 흐름 제어, 상태 관리, 피드백 영향 범위 판단
└──────────┬──────────┘
           │
    ┌──────┴───────┐
    │              │
    ▼              ▼
Analyzer       UseCase Agent
요구사항 파싱   유즈케이스 + Mermaid 생성 → usecase.mmd
                    │
                    ▼
         [개발자 검토 - 유즈케이스]
         파일 수정 또는 자연어 명령
                    │
                    ▼
             Domain Agent
             도메인 모델 / DTO 분리 추출 → domain.yml
                    │
                    ▼
         [개발자 검토 - 도메인 모델]
         파일 수정 또는 자연어 명령
                    │
                    ▼
            TestGen Agent
            domain.yml 참조, 레이어별 테스트 생성
            (룰 적용 중 판단 필요 시 역질문)
                    │
                    ▼
           DocWriter Agent
           specred-report.md 생성
```

**피드백 흐름:** `specred feedback "..."` → Orchestrator가 영향 범위 판단 → 필요한 에이전트만 선택 호출

---

## 파일 구조

```
specred/                          # Python 패키지 루트
├── cli/
│   ├── main.py                   # Typer app 진입점, 명령어 등록
│   └── commands/
│       ├── init.py               # specred init — 전역/프로젝트 설정 파일 생성
│       ├── generate.py           # specred generate — 테스트 코드 생성 전체 플로우
│       ├── review.py             # specred review — 커버리지 요약 출력
│       └── feedback.py           # specred feedback — 변경사항 반영
│
├── agents/
│   ├── orchestrator.py           # 전체 워크플로우 제어, 상태 관리
│   ├── analyzer.py               # 요구사항 문서 파싱
│   ├── usecase_agent.py          # 유즈케이스 + Mermaid 생성
│   ├── domain_agent.py           # 도메인 모델 / DTO 추출 및 확정
│   ├── testgen_agent.py          # 테스트 코드 생성 + 역질문 처리
│   └── docwriter_agent.py        # specred-report.md 생성
│
├── mcp/
│   ├── filesystem.py             # 파일 읽기/쓰기 유틸리티
│   ├── watcher.py                # watchdog 기반 파일 변경 감지
│   └── coverage.py               # 커버리지 결과 파싱
│
├── prompts/                      # 에이전트별 시스템 프롬프트 + few-shot 예시
│   ├── usecase.py
│   ├── domain.py
│   └── testgen/
│       ├── behavior.py           # Given-When-Then 스타일
│       └── describe.py           # describe/it 스타일
│
└── templates/                    # Jinja2 템플릿
    ├── usecase.mmd.j2            # Mermaid 유즈케이스 다이어그램
    └── report.md.j2              # specred-report.md

~/.specred/config.yml             # API 키 + 모델 (전역, gitignore 대상)

프로젝트 루트/
├── specred.yml                   # 테스트 스타일, 언어, 프레임워크, 커스텀 룰
├── usecase.mmd                   # 생성된 유즈케이스 다이어그램 (검토/수정 대상)
├── domain.yml                    # 확정된 도메인 모델 (single source of truth)
└── specred-report.md             # 테스트 커버리지 리포트
```

---

## 기술 스택

| 분류 | 기술 | 용도 |
|------|------|------|
| 언어 | Python 3.11+ | CLI 구현 |
| CLI 프레임워크 | Typer | 명령어 파싱, 인터랙션 |
| AI | Anthropic Claude API | 유즈케이스/테스트 코드 생성 |
| 기본 모델 | claude-sonnet-4-6 | 균형 잡힌 성능 (변경 가능) |
| 파일 감시 | watchdog | usecase.mmd, domain.yml 변경 자동 감지 |
| 설정 파싱 | PyYAML | specred.yml, domain.yml |
| 문서 생성 | Jinja2 | Mermaid, Markdown 템플릿 |
| 패키징 | pyproject.toml | pip install specred |

---

## 개발 환경 설정

```bash
# 가상환경 활성화
source .venv/bin/activate

# 개발 모드 설치
pip install -e .

# CLI 동작 확인
specred --help
```

---

## CLI 명령어 요약

| 명령어 | 진입점 | 상태 |
|--------|--------|------|
| `specred init` | `commands/init.py` | 구현 완료 |
| `specred generate` | `commands/generate.py` | TODO |
| `specred review` | `commands/review.py` | TODO |
| `specred feedback "..."` | `commands/feedback.py` | TODO |

## 주요 플래그 (generate)

| 플래그 | 필수 | 설명 |
|--------|------|------|
| `--requirement` | 필수 | 요구사항 문서 경로 |
| `--api-spec` | 선택 | API 스펙 파일 경로 |
| `--domain` | 선택 | 도메인 모델 문서 (있으면 도메인 확정 단계 생략) |
| `--model` | 선택 | 모델 오버라이드 |
| `--style` | 선택 | 테스트 스타일 오버라이드 (behavior \| describe) |
| `--lang` | 선택 | 언어 오버라이드 |
| `--framework` | 선택 | 프레임워크 오버라이드 |

---

## 학습 목표 (프로젝트 맥락)

- 에이전트 오케스트레이션 패턴 구현
- 워크플로우 자동화 + 개발자 검토 개입점 설계
- MCP(Model Context Protocol) 적용

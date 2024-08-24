# Jammin VS Jumin

2022 재민 VS 주민 게임 개발

## 게임 모드

### 2인 플레이어 게임
두 플레이어가 서로 대결할 수 있는 원래의 게임 모드입니다.

### 1인 플레이어 게임
안재민 용사가 박주민 공주를 구출하는 새로운 싱글 플레이어 모험 모드입니다.

## 버전 기록

### 버전 1.0
#### 주요 변동 사항
- 기본 배드민턴 던지기, 상어 던지기 구현

#### 조작법
| 버전  | 캐릭터  | 이동 키                         | 던지기 공격 키 | 추가 동작 키 및 설명               |
|-------|---------|---------------------------------|----------------|------------------------------------|
| 1.0   | 주민    | W (상), A (좌), S (하), D (우)  | E              | N/A                                |
|       | 재민    | ↑ (상), ← (좌), ↓ (하), → (우)  | .              | N/A                                |

### 버전 1.1
#### 주요 변동 사항
- Ultimate Siba 모드 추가
- 사랑 발사 모드 추가

#### 조작법
| 버전  | 캐릭터  | 이동 키                         | 던지기 공격 키 | 추가 동작 키 및 설명               |
|-------|---------|---------------------------------|----------------|------------------------------------|
| 1.1   | 주민    | W (상), A (좌), S (하), D (우)  | E              | N/A                                |
|       | 재민    | [ (상), ; (좌), ' (하), Enter (우)| P             | N/A                                |

### 버전 1.2
#### 주요 변동 사항
- Ultimate Siba 모드에서 재민이 타격 시 재민이 날라가는 모션 추가
- 수행평가 요구에 맞게 좌 - 우 배치를 상 - 하 배치로 바꾸며 화면 작아짐

#### 조작법
| 버전  | 캐릭터  | 이동 키                         | 던지기 공격 키 | 추가 동작 키 및 설명               |
|-------|---------|---------------------------------|----------------|------------------------------------|
| 1.2   | 주민    | W (상), A (좌), S (하), D (우)  | E              | N/A                                |
|       | 재민    | [ (상), ; (좌), ' (하), Enter (우)| -             | = (사랑 충전), Backspace (사랑 발사) |

### 버전 2.0
- 1인 플레이어 스테이지 게임 추가
  - 안재민 용사의 박주민 공주 구출 모험
  - 다양한 스테이지와 적 캐릭터 추가
  - 새로운 게임플레이 메커닉 도입
  
#### 조작법
- 포인트 & 클릭 이동법 : 마우스로 클릭하여 목적지를 정하세요! 그 방향으로 이동합니다.
- 마우스 에임 & W 클릭 : 재민이의 슬리퍼 공격으로 장애물들을 물리치세요!

## 게임 설명을 영상으로 보고 싶다면?
[여기서 영상을 확인하세요](https://youtu.be/RG8SuWASbsY)

## 설치 방법

1. **저장소 복제**:
   ```bash
   git clone https://github.com/yourusername/Jammin-VS-Jumin.git
   cd Jammin-VS-Jumin
   ```

2. **가상 환경 생성 및 활성화 (선택사항이지만 권장)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows의 경우: .\venv\Scripts\activate
   ```

3. **필요한 패키지 설치**:
   ```bash
   pip install -r requirements.txt
   ```

4. **게임 실행**:
   ```bash
   python main.py
   ```

## 게임 모드 개요

### 2인 플레이어 게임
- 두 플레이어 간의 경쟁 게임플레이
- 배드민턴과 상어 던지기 메커닉 포함
- Ultimate Siba 및 사랑 발사 모드 제공

### 1인 플레이어 게임
- 안재민을 주인공으로 한 싱글 플레이어 모험
- 다양한 적으로부터 박주민 공주를 구출하는 미션
- 각기 다른 도전과 보스전이 있는 여러 스테이지
- 새로운 게임플레이 요소:
  - 다양한 공격 타입 (고함 발사, 슬리퍼 던지기)
  - 체력 및 속도 증가 아이템
  - 고유한 행동 패턴을 가진 다양한 적 유형

원하는 게임 모드를 선택하여 Jammin VS Jumin의 재미를 즐겨보세요!
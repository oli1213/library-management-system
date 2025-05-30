# 도서관 관리 시스템 모듈 평가 보고서

## 1. 응집도(Cohesion) 평가

### 1.1 Book 클래스 - **높은 응집도** ⭐⭐⭐⭐⭐
- **기능적 응집도(Functional Cohesion)** 달성
- 도서와 관련된 모든 기능이 한 클래스에 집중
- 대출, 반납, 상태 관리 등 도서 관련 기능만 포함
- 단일 책임 원칙(SRP) 준수

**평가 근거:**
```python
# 도서 관련 기능만 집중적으로 구현
- borrow(): 대출 기능
- return_book(): 반납 기능  
- to_dict(): 데이터 변환
```

### 1.2 Member 클래스 - **높은 응집도** ⭐⭐⭐⭐⭐
- **기능적 응집도** 달성
- 회원과 관련된 모든 기능이 응집
- 대출 한도 확인, 대출 도서 관리 등 회원 관련 기능만 포함

**평가 근거:**
```python
# 회원 관련 기능만 집중적으로 구현
- can_borrow(): 대출 가능 여부 확인
- add_borrowed_book(): 대출 도서 추가
- remove_borrowed_book(): 대출 도서 제거
```

### 1.3 Database 클래스 - **높은 응집도** ⭐⭐⭐⭐⭐
- **기능적 응집도** 달성
- 데이터베이스 관련 CRUD 기능만 집중
- 데이터 저장, 조회, 검색 기능으로 통일

### 1.4 LibraryManagementSystem 클래스 - **높은 응집도** ⭐⭐⭐⭐
- **순차적 응집도(Sequential Cohesion)** 달성
- 도서관 업무 프로세스를 순차적으로 처리
- 각 메서드가 도서관 관리라는 공통 목적을 가짐

### 1.5 UserInterface 클래스 - **높은 응집도** ⭐⭐⭐⭐⭐
- **기능적 응집도** 달성
- 사용자 인터페이스 관련 기능만 집중
- 화면 표시 및 사용자 상호작용 기능으로 통일

## 2. 결합도(Coupling) 평가

### 2.1 Book ↔ 다른 클래스 - **낮은 결합도** ⭐⭐⭐⭐⭐
- **데이터 결합도(Data Coupling)** 달성
- 다른 클래스와 독립적으로 동작
- 매개변수를 통해서만 데이터 전달

**평가 근거:**
```python
# Book 클래스는 다른 클래스에 의존하지 않음
class Book:
    def borrow(self) -> bool:  # 매개변수 없이 독립적 동작
        # 내부 상태만 변경
```

### 2.2 Member ↔ 다른 클래스 - **낮은 결합도** ⭐⭐⭐⭐⭐
- **데이터 결합도** 달성
- 독립적인 회원 관리 기능
- 외부 의존성 최소화

### 2.3 Database ↔ Book/Member - **낮은 결합도** ⭐⭐⭐⭐
- **스탬프 결합도(Stamp Coupling)** 
- 객체 자체를 매개변수로 전달하지만 필요한 부분만 사용
- 인터페이스가 명확하게 정의됨

**평가 근거:**
```python
def add_book(self, book: Book):  # 객체 전달하지만 의존성 최소
def add_member(self, member: Member):
```

### 2.4 LibraryManagementSystem ↔ 다른 클래스 - **중간 결합도** ⭐⭐⭐
- **객체 결합도(Object Coupling)**
- Database 객체에 대한 의존성 존재
- 하지만 인터페이스를 통한 상호작용으로 결합도 최소화

**개선점:**
```python
# 현재: 직접 의존
self.database = Database()

# 개선 가능: 의존성 주입
def __init__(self, database: Database):
    self.database = database
```

### 2.5 UserInterface ↔ LibraryManagementSystem - **낮은 결합도** ⭐⭐⭐⭐
- **데이터 결합도** 달성
- 의존성 주입을 통한 느슨한 결합
- 명확한 인터페이스 정의

**평가 근거:**
```python
def __init__(self, library_system: LibraryManagementSystem):
    self.library_system = library_system  # 의존성 주입
```

## 3. 전체 시스템 평가

### 3.1 장점
1. **높은 응집도**: 각 클래스가 명확한 단일 책임을 가짐
2. **낮은 결합도**: 모듈 간 독립성이 높아 유지보수가 용이
3. **확장성**: 새로운 기능 추가가 용이한 구조
4. **테스트 용이성**: 각 모듈을 독립적으로 테스트 가능

### 3.2 개선점
1. **의존성 주입**: LibraryManagementSystem의 Database 의존성을 주입 방식으로 개선
2. **인터페이스 추상화**: 추상 클래스나 인터페이스를 통한 더 나은 분리
3. **예외 처리**: 더 세밀한 예외 처리 메커니즘 추가

### 3.3 최종 평가
- **응집도**: 4.8/5.0 (거의 완벽한 기능적 응집도)
- **결합도**: 4.2/5.0 (대부분 낮은 결합도, 일부 개선 여지)
- **전체 품질**: 4.5/5.0 (우수한 모듈 설계)

## 4. 시퀀스 다이어그램과 코드의 일치성

구현된 코드는 시퀀스 다이어그램의 상호작용 패턴을 충실히 반영:

1. **검색 프로세스**: User → UI → LMS → DB → Book/Member
2. **대출 프로세스**: 회원 확인 → 도서 상태 확인 → 대출 처리
3. **반납 프로세스**: 대출 기록 확인 → 상태 업데이트

모든 상호작용이 시퀀스 다이어그램에 정의된 순서와 조건을 따름.

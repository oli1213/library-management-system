sequenceDiagram
    participant User as 사용자
    participant UI as 사용자 인터페이스
    participant LMS as 도서관관리시스템
    participant DB as 데이터베이스
    participant Book as 도서
    participant Member as 회원

    Note over User, Member: 도서 대출 프로세스
    
    User->>UI: 도서 검색 요청
    UI->>LMS: searchBook(title)
    LMS->>DB: 도서 정보 조회
    DB-->>LMS: 도서 목록 반환
    LMS-->>UI: 검색 결과
    UI-->>User: 도서 목록 표시
    
    User->>UI: 대출 요청
    UI->>LMS: borrowBook(memberId, bookId)
    LMS->>Member: 회원 정보 확인
    Member-->>LMS: 회원 상태 반환
    
    alt 회원이 유효한 경우
        LMS->>Book: 도서 상태 확인
        Book-->>LMS: 대출 가능 여부
        
        alt 도서 대출 가능
            LMS->>DB: 대출 정보 저장
            DB-->>LMS: 저장 완료
            LMS->>Book: 대출 상태로 변경
            Book-->>LMS: 상태 변경 완료
            LMS-->>UI: 대출 성공
            UI-->>User: 대출 완료 메시지
        else 도서 대출 불가능
            LMS-->>UI: 대출 실패 (도서 없음)
            UI-->>User: 오류 메시지
        end
    else 회원이 유효하지 않음
        LMS-->>UI: 대출 실패 (회원 정보 오류)
        UI-->>User: 오류 메시지
    end
    
    Note over User, Member: 도서 반납 프로세스
    
    User->>UI: 반납 요청
    UI->>LMS: returnBook(memberId, bookId)
    LMS->>DB: 대출 정보 조회
    DB-->>LMS: 대출 기록 반환
    
    alt 대출 기록이 존재하는 경우
        LMS->>Book: 반납 상태로 변경
        Book-->>LMS: 상태 변경 완료
        LMS->>DB: 반납 정보 업데이트
        DB-->>LMS: 업데이트 완료
        LMS-->>UI: 반납 성공
        UI-->>User: 반납 완료 메시지
    else 대출 기록이 없는 경우
        LMS-->>UI: 반납 실패
        UI-->>User: 오류 메시지
    end

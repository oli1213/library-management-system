# library_management_system.py
from datetime import datetime, timedelta
from typing import List, Optional, Dict
import json

class Book:
    """도서 클래스 - 높은 응집도"""
    def __init__(self, book_id: str, title: str, author: str, isbn: str):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = True
        self.borrowed_date = None
        self.due_date = None
    
    def borrow(self) -> bool:
        """도서 대출"""
        if self.is_available:
            self.is_available = False
            self.borrowed_date = datetime.now()
            self.due_date = self.borrowed_date + timedelta(days=14)
            return True
        return False
    
    def return_book(self) -> bool:
        """도서 반납"""
        if not self.is_available:
            self.is_available = True
            self.borrowed_date = None
            self.due_date = None
            return True
        return False
    
    def to_dict(self) -> Dict:
        """딕셔너리 변환"""
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'is_available': self.is_available,
            'borrowed_date': self.borrowed_date.isoformat() if self.borrowed_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None
        }

class Member:
    """회원 클래스 - 높은 응집도"""
    def __init__(self, member_id: str, name: str, email: str):
        self.member_id = member_id
        self.name = name
        self.email = email
        self.borrowed_books: List[str] = []
        self.is_active = True
    
    def can_borrow(self) -> bool:
        """대출 가능 여부 확인"""
        return self.is_active and len(self.borrowed_books) < 5
    
    def add_borrowed_book(self, book_id: str):
        """대출 도서 추가"""
        if book_id not in self.borrowed_books:
            self.borrowed_books.append(book_id)
    
    def remove_borrowed_book(self, book_id: str):
        """대출 도서 제거"""
        if book_id in self.borrowed_books:
            self.borrowed_books.remove(book_id)
    
    def to_dict(self) -> Dict:
        """딕셔너리 변환"""
        return {
            'member_id': self.member_id,
            'name': self.name,
            'email': self.email,
            'borrowed_books': self.borrowed_books,
            'is_active': self.is_active
        }

class Database:
    """데이터베이스 클래스 - 높은 응집도 (데이터 관리 기능만 담당)"""
    def __init__(self):
        self.books: Dict[str, Book] = {}
        self.members: Dict[str, Member] = {}
        self.borrow_records: List[Dict] = []
    
    def add_book(self, book: Book):
        """도서 추가"""
        self.books[book.book_id] = book
    
    def add_member(self, member: Member):
        """회원 추가"""
        self.members[member.member_id] = member
    
    def get_book(self, book_id: str) -> Optional[Book]:
        """도서 조회"""
        return self.books.get(book_id)
    
    def get_member(self, member_id: str) -> Optional[Member]:
        """회원 조회"""
        return self.members.get(member_id)
    
    def search_books(self, title: str) -> List[Book]:
        """도서 검색"""
        return [book for book in self.books.values() 
                if title.lower() in book.title.lower()]
    
    def save_borrow_record(self, member_id: str, book_id: str):
        """대출 기록 저장"""
        record = {
            'member_id': member_id,
            'book_id': book_id,
            'borrow_date': datetime.now().isoformat(),
            'return_date': None
        }
        self.borrow_records.append(record)
    
    def update_return_record(self, member_id: str, book_id: str):
        """반납 기록 업데이트"""
        for record in self.borrow_records:
            if (record['member_id'] == member_id and 
                record['book_id'] == book_id and 
                record['return_date'] is None):
                record['return_date'] = datetime.now().isoformat()
                return True
        return False

class LibraryManagementSystem:
    """도서관 관리 시스템 - 낮은 결합도로 각 모듈과 상호작용"""
    def __init__(self):
        self.database = Database()
    
    def search_book(self, title: str) -> List[Dict]:
        """도서 검색"""
        books = self.database.search_books(title)
        return [book.to_dict() for book in books]
    
    def borrow_book(self, member_id: str, book_id: str) -> Dict:
        """도서 대출"""
        member = self.database.get_member(member_id)
        if not member:
            return {'success': False, 'message': '회원 정보를 찾을 수 없습니다.'}
        
        if not member.can_borrow():
            return {'success': False, 'message': '대출 한도를 초과했거나 비활성 회원입니다.'}
        
        book = self.database.get_book(book_id)
        if not book:
            return {'success': False, 'message': '도서를 찾을 수 없습니다.'}
        
        if not book.borrow():
            return {'success': False, 'message': '이미 대출된 도서입니다.'}
        
        member.add_borrowed_book(book_id)
        self.database.save_borrow_record(member_id, book_id)
        
        return {
            'success': True, 
            'message': f'도서 "{book.title}"이 성공적으로 대출되었습니다.',
            'due_date': book.due_date.isoformat()
        }
    
    def return_book(self, member_id: str, book_id: str) -> Dict:
        """도서 반납"""
        member = self.database.get_member(member_id)
        if not member:
            return {'success': False, 'message': '회원 정보를 찾을 수 없습니다.'}
        
        book = self.database.get_book(book_id)
        if not book:
            return {'success': False, 'message': '도서를 찾을 수 없습니다.'}
        
        if book_id not in member.borrowed_books:
            return {'success': False, 'message': '해당 도서의 대출 기록이 없습니다.'}
        
        if book.return_book():
            member.remove_borrowed_book(book_id)
            self.database.update_return_record(member_id, book_id)
            return {
                'success': True, 
                'message': f'도서 "{book.title}"이 성공적으로 반납되었습니다.'
            }
        
        return {'success': False, 'message': '반납 처리 중 오류가 발생했습니다.'}

class UserInterface:
    """사용자 인터페이스 - 낮은 결합도"""
    def __init__(self, library_system: LibraryManagementSystem):
        self.library_system = library_system
    
    def display_search_results(self, results: List[Dict]):
        """검색 결과 표시"""
        if not results:
            print("검색된 도서가 없습니다.")
            return
        
        print("\n=== 검색 결과 ===")
        for book in results:
            status = "대출 가능" if book['is_available'] else "대출 중"
            print(f"ID: {book['book_id']}, 제목: {book['title']}, "
                  f"저자: {book['author']}, 상태: {status}")
    
    def display_message(self, message: str):
        """메시지 표시"""
        print(f"\n{message}")
    
    def search_book_interface(self, title: str):
        """도서 검색 인터페이스"""
        results = self.library_system.search_book(title)
        self.display_search_results(results)
    
    def borrow_book_interface(self, member_id: str, book_id: str):
        """도서 대출 인터페이스"""
        result = self.library_system.borrow_book(member_id, book_id)
        self.display_message(result['message'])
        if result['success'] and 'due_date' in result:
            print(f"반납 예정일: {result['due_date']}")
    
    def return_book_interface(self, member_id: str, book_id: str):
        """도서 반납 인터페이스"""
        result = self.library_system.return_book(member_id, book_id)
        self.display_message(result['message'])

def main():
    """메인 함수 - 시스템 초기화 및 테스트"""
    # 시스템 초기화
    library_system = LibraryManagementSystem()
    ui = UserInterface(library_system)
    
    # 샘플 데이터 추가
    book1 = Book("B001", "파이썬 프로그래밍", "김파이", "978-1234567890")
    book2 = Book("B002", "소프트웨어 공학", "이공학", "978-0987654321")
    book3 = Book("B003", "데이터베이스 시스템", "박데이", "978-1122334455")
    
    member1 = Member("M001", "홍길동", "hong@email.com")
    member2 = Member("M002", "김영희", "kim@email.com")
    
    library_system.database.add_book(book1)
    library_system.database.add_book(book2)
    library_system.database.add_book(book3)
    library_system.database.add_member(member1)
    library_system.database.add_member(member2)
    
    # 테스트 시나리오
    print("=== 도서관 관리 시스템 테스트 ===")
    
    # 1. 도서 검색
    print("\n1. 도서 검색 테스트")
    ui.search_book_interface("파이썬")
    
    # 2. 도서 대출
    print("\n2. 도서 대출 테스트")
    ui.borrow_book_interface("M001", "B001")
    
    # 3. 중복 대출 시도
    print("\n3. 중복 대출 시도")
    ui.borrow_book_interface("M002", "B001")
    
    # 4. 도서 반납
    print("\n4. 도서 반납 테스트")
    ui.return_book_interface("M001", "B001")
    
    # 5. 반납 후 재검색
    print("\n5. 반납 후 도서 상태 확인")
    ui.search_book_interface("파이썬")

if __name__ == "__main__":
    main()

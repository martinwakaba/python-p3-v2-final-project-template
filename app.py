from database.connection import db_connection
from database.setup import create_tables
from lib.models.book import Book
from lib.models.user import User
from lib.models.bookcheckout import Bookcheckout
from datetime import datetime, date

#user
def create_user(cursor):
    username = input("Enter user name: ")
    email = input("Enter email address: ")
    phone_number = input("Enter phone number: ")

    cursor.execute("SELECT id, title, genre FROM books")
    books = cursor.fetchall()

    print("Available books:")
    for book in books:
        print(f"ID: {book[0]}, Title: {book[1]}, Genre: {book[2]}")

    book_taken_id = input("Enter the ID of the book taken (or leave blank if none): ")
    book_taken_id = int(book_taken_id) if book_taken_id else None

    user = User(None, username, email, phone_number, book_taken_id)
    user.create_user(cursor)

    if book_taken_id:
        cursor.execute("""
            INSERT INTO bookscheckout (user_id, book_id, genre, checkout_date)
            VALUES (?, ?, (SELECT genre FROM books WHERE id = ?), datetime('now'))
        """, (user.id, book_taken_id, book_taken_id))

    print("User added successfully!")

def get_all_users(cursor):
    users = User.get_all_users(cursor)
    if users:
        print("All Users: ")
        for user in users:
            print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}, Book Taken ID: {user.book_taken}")
    else:
        print("No User Found")

def get_user(cursor):
    user_num = input("Enter the phone number: ")
    user = User.get_user(cursor, user_num)
    if user:
        print(f"User associated with phone number {user_num}:")
        print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}, Book Taken ID: {user.book_taken}")
    else:
        print("No match!")      

def book(self, cursor):
        cursor.execute("""
            SELECT books.id, books.title, books.publication_date, books.author, books.genre
            FROM books
            JOIN bookscheckout ON books.id = bookscheckout.book_id
            WHERE bookscheckout.user_id = ?
        """, (self._id,))
        book_data = cursor.fetchall()
        return book_data


#book

def add_book(cursor):
    book_title = input("Enter book title: ")
    publication = input("Enter publication date: ")
    author = input("Enter book's author: ")
    genre = input("Enter the genre of the book: ")
    book = Book(None, book_title, publication, author, genre)
    book.add_book(cursor)
    print("Book Added successfully!!!")

def get_all_books(cursor):
    all_books = Book.get_all_books(cursor)
    if all_books:
        print("All books")
        for book in all_books:
            print(f"ID: {book.id}, Title: {book.title}, Publication Date: {book.publication_date}, Author: {book.author}, Genre: {book.genre}")

    else:
        print(f"No Books available")

def get_book_by_genre(cursor):
    book_genre = input("Enter the book genre: ")
    books = Book.get_books_by_genre(cursor, book_genre)  
    if books:
        print(f"Books under {book_genre}: ")
        for book in books:
            print(f"ID: {book.id}, Title: {book.title}, Publication Date: {book.publication_date}, Author: {book.author}, Genre: {book.genre}")
    else:
        print(f"No match!")

def get_book_by_author(cursor):
    book_author = input("Enter the book author: ")
    books = Book.get_book_by_author(cursor, book_author)
    if books:
        print(f"Books written by {book_author}:")
        for book in books:
            print(f"ID: {book.id}, Title: {book.title}, Publication Date: {book.publication_date}, Author: {book.author}, Genre: {book.genre}")
    else:
        print(f"No match!")

#bookcheckout
def choose_book(cursor):
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    if books:
        print("Available Books:")
        for book in books:
            print(f"ID: {book[0]}, Title: {book[1]}, Publication Date: {book[2]}, Author: {book[3]}, Genre: {book[4]}")
        book_id = int(input("Enter the ID of the book you want to take: "))
        return book_id
    else:
        print("No books available.")
        return None



def main():
    
    create_tables()

    while True:
        print("\nChoose:")
        print("1. Add User")
        print("2. Show Users")
        print("3. Show User by number")
        print("4. Show Book lent to user")
        print("5. Add a book")
        print("6. Show books")
        print("7. Show Book by genre")
        print("8. Show Book by Author")

        choice = input("\nEnter A Number: ")

        if choice == "1":
            conn = db_connection()
            cursor = conn.cursor()
            create_user(cursor)
            conn.commit()
            conn.close()
        elif choice == "2":
            conn = db_connection()
            cursor = conn.cursor()
            get_all_users(cursor)
            conn.commit()
            conn.close()
        elif choice == "3":
            conn = db_connection()
            cursor = conn.cursor()
            get_user(cursor)
            conn.commit()
            conn.close()
        elif choice == "4":
            conn = db_connection()
            cursor = conn.cursor()
            book(cursor)
            conn.commit()
            conn.close()    
        elif choice == "5":
            conn = db_connection()
            cursor = conn.cursor()
            add_book(cursor)
            conn.commit()
            conn.close()
        elif choice == "6":
            conn = db_connection()
            cursor = conn.cursor()
            get_all_books(cursor)
            conn.commit()
            conn.close()
        elif choice == "7":
            conn = db_connection()
            cursor = conn.cursor()
            get_book_by_genre(cursor)
            conn.commit()
            conn.close()
        elif choice == "8":
            conn = db_connection()
            cursor = conn.cursor()
            get_book_by_author(cursor)
            conn.commit()
            conn.close()         
        else:
            print("Exiting...")
            break




if __name__ == "__main__":
    main()

#BE MINI PROJECT : STQA TESTING WEB APPLICATION 
import streamlit as st
import sqlite3

# Initialize SQLite database
def init_db():
    with sqlite3.connect('books.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS books
                     (title TEXT PRIMARY KEY, author TEXT, genre TEXT, rating INTEGER)''')
        conn.commit()

init_db()

def add_book(title, author, genre, rating):
    with sqlite3.connect('books.db') as conn:
        conn.execute("INSERT INTO books (title, author, genre, rating) VALUES (?, ?, ?, ?)", (title, author, genre, rating))
        conn.commit()

def view_all_books():
    with sqlite3.connect('books.db') as conn:
        return conn.execute("SELECT * FROM books").fetchall()

def get_book(title):
    with sqlite3.connect('books.db') as conn:
        return conn.execute("SELECT * FROM books WHERE title=?", (title,)).fetchone()

def update_rating(title, rating):
    with sqlite3.connect('books.db') as conn:
        conn.execute("UPDATE books SET rating=? WHERE title=?", (rating, title))
        conn.commit()

def delete_book(title):
    with sqlite3.connect('books.db') as conn:
        conn.execute("DELETE FROM books WHERE title=?", (title,))
        conn.commit()

def main():
    st.title("Bookshelf Manager")
    menu = ["Add Book", "View Books", "Search", "Update Rating", "Delete Book"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Book":
        st.subheader("Add a New Book")
        title = st.text_input("Title")
        author = st.text_input("Author")
        genre = st.text_input("Genre")
        rating = st.slider("Rating (out of 5)", 1, 5)
        if st.button("Add Book"):
            add_book(title, author, genre, rating)
            st.success(f"Book {title} added successfully!")

    elif choice == "View Books":
        st.subheader("View All Books")
        books = view_all_books()
        for book in books:
            st.write(f"Title: {book[0]}, Author: {book[1]}, Genre: {book[2]}, Rating: {book[3]}/5")

    elif choice == "Search":
        st.subheader("Search for a Book")
        search_term = st.text_input("Search by Title")
        book = get_book(search_term)
        if book:
            st.write(f"Title: {book[0]}, Author: {book[1]}, Genre: {book[2]}, Rating: {book[3]}/5")
        else:
            st.write(f"No book found with title {search_term}")

    elif choice == "Update Rating":
        st.subheader("Update Book Rating")
        book_title = st.text_input("Enter the title of the book")
        new_rating = st.slider("New Rating (out of 5)", 1, 5)
        if st.button("Update Rating"):
            if get_book(book_title):
                update_rating(book_title, new_rating)
                st.success(f"Rating for {book_title} updated successfully!")
            else:
                st.error(f"No book found with title {book_title}")

    elif choice == "Delete Book":
        st.subheader("Delete a Book")
        book_title = st.text_input("Enter the title of the book to delete")
        if st.button("Delete Book"):
            if get_book(book_title):
                delete_book(book_title)
                st.success(f"Book {book_title} deleted successfully!")
            else:
                st.error(f"No book found with title {book_title}")

if __name__ == "__main__":
    main()

    
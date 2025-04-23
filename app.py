import streamlit as st
import os
import json
import datetime

LIBRARY_FILE = "library.json"

def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, 'r') as file:
            return json.load(file)
    return []

def save_library(library):
    with open(LIBRARY_FILE, 'w') as file:
        json.dump(library, file)

def add_book(library, title, author, year, genre, read_status):
    book = {
        'title': title,
        'author': author,
        'year': int(year),
        'genre': genre,
        'read_status': read_status.lower() == 'yes'
    }
    library.append(book)

def remove_book(library, title):
    return [book for book in library if book['title'].lower() != title.lower()]

def search_books(library, search_type, search_value):
    if search_type == 'Title':
        return [book for book in library if search_value.lower() in book['title'].lower()]
    elif search_type == 'Author':
        return [book for book in library if search_value.lower() in book['author'].lower()]
    return []

def get_statistics(library):
    total = len(library)
    read = sum(1 for book in library if book['read_status'])
    percent = (read / total * 100) if total > 0 else 0
    return total, percent

def show_instructions():
    st.subheader("📘 How to Use the App")
    st.markdown("""
    ### 📖 Step-by-step Guide:
    1. **Add a Book**: Go to *'Add a book'* from the menu. Enter the book title, author, year, genre, and whether you've read it.
    2. **Save Automatically**: Every book you add is saved instantly to your library file.
    3. **Remove a Book**: Use the *'Remove a book'* option and type the exact title to delete a book.
    4. **Search for Books**: In *'Search for a book'*, choose whether you want to search by title or author, then type the name.
    5. **View All Books**: Check *'Display all books'* to see your full library in a neat list.
    6. **Track Progress**: Under *'Display statistics'*, see total books and percentage of books you’ve marked as read.
    """)

def main():
    st.title("📚 Personal Library Manager")
    library = load_library()

    menu = ["Add a book", "Remove a book", "Search for a book", "Display all books", "Display statistics", "How to Use the App", "Exit"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add a book":
        st.subheader("➕ Add a New Book")
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        year = st.number_input("Year", min_value=1000, max_value=2100, step=1)
        genre = st.text_input("Genre")
        read_status = st.radio("Have you read it?", ("yes", "no"))
        if st.button("Add Book"):
            if title and author and genre:
                add_book(library, title, author, year, genre, read_status)
                save_library(library)
                st.success(f"'{title}' added successfully!")
            else:
                st.error("Please fill all fields.")

    elif choice == "Remove a book":
        st.subheader("🗑️ Remove a Book")
        title = st.text_input("Enter the book title to remove")
        if st.button("Remove Book"):
            if title:
                library = remove_book(library, title)
                save_library(library)
                st.success(f"'{title}' removed successfully!")
            else:
                st.error("Please enter a title.")

    elif choice == "Search for a book":
        st.subheader("🔍 Search for a Book")
        search_type = st.radio("Search by", ["Title", "Author"])
        search_value = st.text_input(f"Enter {search_type}")
        if st.button("Search"):
            if search_value:
                results = search_books(library, search_type, search_value)
                if results:
                    for book in results:
                        st.write(f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read_status'] else 'Unread'}")
                else:
                    st.info("No matching books found.")
            else:
                st.error("Please enter a search value.")

    elif choice == "Display all books":
        st.subheader("📖 Your Library")
        if not library:
            st.info("Library is empty.")
        else:
            for i, book in enumerate(library, 1):
                st.write(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read_status'] else 'Unread'}")

    elif choice == "Display statistics":
        st.subheader("📊 Library Statistics")
        total, percent = get_statistics(library)
        st.write(f"Total Books: {total}")
        st.write(f"Books Read: {percent:.2f}%")

    elif choice == "How to Use the App":
        show_instructions()

    elif choice == "Exit":
        save_library(library)
        st.success("Library saved successfully!")

    # Footer
    current_year = datetime.datetime.now().year
    st.markdown(f"<hr><p style='text-align: center;'>&copy; {current_year} Muhammad Owais | Library Manager</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()


#Uygulamayı test etmek için rastgele isimli yazarlı kitap eklemek için kullanılabilir

path_of_csv = r"C:\Users\kuzey\OneDrive\Masaüstü"
file_name = "database"

book_names = [
    "To Kill a Mockingbird", "1984", "The Great Gatsby", "Pride and Prejudice", "The Catcher in the Rye",
    "Brave New World", "The Hobbit", "Fahrenheit 451", "The Lord of the Rings", "Animal Farm",
    "The Hunger Games", "Harry Potter and the Sorcerer's Stone", "The Da Vinci Code", "The Alchemist",
    "Gone with the Wind", "The Kite Runner", "The Hitchhiker's Guide to the Galaxy", "The Shining",
    "The Catcher in the Rye", "The Diary of a Young Girl", "The Girl with the Dragon Tattoo",
    "A Game of Thrones", "The Help", "The Road", "The Fault in Our Stars", "The Girl on the Train",
    "The Book Thief", "The Lovely Bones", "The Martian", "The Handmaid's Tale", "The Hunger Games",
    "Jurassic Park", "The Pillars of the Earth", "The Giver", "The Time Traveler's Wife",
    "The Secret Life of Bees", "The Color Purple", "The Name of the Wind", "The Goldfinch",
    "Life of Pi", "The Night Circus"
]

# List of book types
book_types = [
    "Drama", "Sci-Fi", "Mystery", "Thriller", "Romance",
    "Fantasy", "Adventure", "Horror", "Historical Fiction", "Dystopian",
    "Young Adult", "Crime", "Self-Help", "Biography", "Science",
    "Philosophy", "Humor", "Poetry", "Classic", "Non-Fiction"
]

# List of authors
authors = [
    "Harper Lee", "George Orwell", "F. Scott Fitzgerald", "Jane Austen", "J.D. Salinger",
    "Aldous Huxley", "J.R.R. Tolkien", "Ray Bradbury", "J.R.R. Tolkien", "George Orwell",
    "Suzanne Collins", "J.K. Rowling", "Dan Brown", "Paulo Coelho", "Margaret Mitchell",
    "Khaled Hosseini", "Douglas Adams", "Stephen King", "J.D. Salinger", "Anne Frank",
    "Stieg Larsson", "George R.R. Martin", "Kathryn Stockett", "Cormac McCarthy", "John Green",
    "Paula Hawkins", "Markus Zusak", "Alice Sebold", "Andy Weir", "Margaret Atwood",
    "Suzanne Collins", "Michael Crichton", "Ken Follett", "Lois Lowry", "Audrey Niffenegger",
    "Sue Monk Kidd", "Alice Walker", "Patrick Rothfuss", "Donna Tartt", "Yann Martel",
    "Erin Morgenstern"
]

# List of publishers
publishers = [
    "Penguin Random House", "HarperCollins", "Simon & Schuster", "Macmillan Publishers", "Hachette Livre",
    "Wiley", "Pearson Education", "Scholastic Corporation", "Springer Nature", "McGraw-Hill Education",
    "Houghton Mifflin Harcourt", "Cengage Learning", "Oxford University Press", "Cambridge University Press",
    "Bloomsbury Publishing", "Harvard University Press", "Elsevier", "National Geographic Society",
    "John Wiley & Sons", "Random House", "Palgrave Macmillan", "Pan Macmillan", "Abrams Books", "Disney Publishing Worldwide",
    "W.W. Norton & Company", "Usborne Publishing", "Rowman & Littlefield", "Hodder & Stoughton", "Grove Atlantic",
    "Puffin Books", "Allen & Unwin", "Tor Books", "Sage Publications", "Little, Brown and Company", "Vintage Books",
    "Houghton Mifflin", "Bloomsbury", "Viking Press", "Knopf Doubleday Publishing Group", "Faber & Faber", "Farrar, Straus and Giroux",
    "Houghton Mifflin Harcourt", "Penguin Books", "Oxford University Press"
]

# List of publication dates (from 1900 to 2023)
import random
import os
import csv
from datetime import datetime
from random import choice


def add_book(csv_name, path_for_csv, bookname, category, author, publisher, publish_date):
    csv_file_path = os.path.join(path_for_csv, f"{csv_name}.csv")

    if not os.path.exists(csv_file_path):
        return "CSV file does not exist."

    if len(publish_date) != 10 or publish_date.count('/') != 2:
        return "Invalid publish date format. Please use the format dd/mm/yyyy."

    day, month, year = publish_date.split('/')
    if not (day.isdigit() and month.isdigit() and year.isdigit()):
        return "Invalid publish date format. Please use numbers for day, month, and year."

    day = int(day)
    month = int(month)
    year = int(year)

    if not (1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= 2100):
        return "Invalid publish date. Please enter a valid date."

    with open(csv_file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        id_count = sum(1 for row in reader) + 1

    new_book = {
        'ID': id_count,
        'Kitap adi': bookname,
        'Turu': category,
        'Yazar': author,
        'Yayin evi': publisher,
        'Baski tarihi': publish_date,
        'Durumu': 'Available',
        'Kullanici ismi': '',
        'Borclunun iletisim bilgileri': '',
        'Odunc alinan zaman': ''
    }

    with open(csv_file_path, 'a', newline='') as csvfile:
        fieldnames = ['ID', 'Kitap adi', 'Turu', 'Yazar', 'Yayin evi', 'Baski tarihi', 'Durumu', 'Kullanici ismi', 'Borclunun iletisim bilgileri', 'Odunc alinan zaman']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if os.path.getsize(csv_file_path) == 0:
            writer.writeheader()

        writer.writerow(new_book)

    return True
#dd/mm/yy
for i in range(1000):  #1000 sayısını kaç tane kitap eklemek istiyorsanız o sayıyla değiştirin
    result = add_book(file_name, path_of_csv, choice(book_names), choice(book_types), choice(authors), choice(publishers), f"{random.randint(1, 31):02d}/{random.randint(1, 12):02d}/{random.randint(1900, 2024)}")

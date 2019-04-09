
class Book(object):
    def __init__(self, bookName, bookAuthor, bookIsbn, releaseYear, bookImage=None, bookDescription=None, rating_counts=None, avg_rating=None):
        self.bookName= bookName
        self.bookAuthor= bookAuthor
        self.bookIsbn= bookIsbn
        self.releaseYear= releaseYear
        self.bookImage = bookImage
        self.bookDescription= bookDescription       
        self.rating_counts = rating_counts
        self.avg_rating= avg_rating

    def getBookName(self):
        return self.bookName    

    def getBookAuthor(self):
        return self.bookAuthor

    def getBookIsbn(self):
        return self.bookIsbn      

    def getBookImage(self):
        return self.bookImage

    def getBookDescription(self):
        return self.bookDescription

    def getReleaseYear(self):
        return self.releaseYear 

    def getRating_counts(self):
        return self.rating_counts

    def getAvg_rating(self):
        return self.avg_rating    
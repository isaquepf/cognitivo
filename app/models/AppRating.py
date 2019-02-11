
class AppRating():
    def __init__(self, row):
        self.id = row["id"]
        self.name = row["track_name"]
        self.size = row["size_bytes"]
        self.currency = row["currency"]
        self.price = row["price"]
        self.rating_amount = row["rating_count_tot"]
        self.last_rating_count = row["rating_count_ver"]
        self.average_rating = row["user_rating"]
        self.last_rating_count = row["user_rating_ver"]
        self.last_version = row["ver"]
        self.parental_rating = row["cont_rating"]
        self.genre = row["prime_genre"]
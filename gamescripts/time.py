#game/time.py

class GameTime:
    def __init__(self, year=0, month=1, day=1):
        self.year = year
        self.month = month
        self.day = day

    def advance_days(self, days=1):
        for _ in range(days):
            self.day += 1
            if self.day > 30:
                self.day = 1
                self.month += 1
            if self.month > 12:
                self.month = 1
                self.year += 1
    
    def advance_years(self, years=1):
        self.year += years
    
    def __str__(self):
        return f"Year {self.year}, Month {self.month}, Day {self.day}"

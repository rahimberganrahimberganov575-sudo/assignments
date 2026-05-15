from abc import ABC, abstractmethod

class Ride(ABC):
    def __init__(self, passenger):
        self.passenger = passenger

    @abstractmethod
    def base_fare(self):
        pass

class Economy(Ride):
    def base_fare(self):
        return 15000

class Comfort(Ride):
    def base_fare(self):
        return 25000

class Business(Ride):
    def base_fare(self):
        return 60000

class Log(ABC):
    @abstractmethod
    def write(self, rides):
        pass

class TextLog(Log):
    def write(self, rides):
        for ride in rides:
            print(f"LOG: {ride.passenger} | fare={ride.base_fare()}")

class Notification(ABC):
    @abstractmethod
    def push(self, rides):
        pass

class PushNotification(Notification):
    def push(self, rides):
        for ride in rides:
            print(f"[PUSH → {ride.passenger}] Driver on the way. Fare {ride.base_fare()} ¥")

class RideManager:
    def __init__(self):
        self.rides = []

    def add(self, ride: Ride):
        self.rides.append(ride)

    def run(self, log: Log, notification: Notification):
        log.write(self.rides)
        notification.push(self.rides)

app = RideManager()
app.add(Economy("Naruto"))
app.add(Comfort("Sasuke"))
app.add(Business("Sakura"))

app.run(TextLog(), PushNotification())

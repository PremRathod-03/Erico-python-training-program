"""
Exercise 7: OOP

- Car class with make, model, year
- methods to display and update details
- ElectricCar subclass adding battery_size, overriding display_details
- __str__ for printing
- encapsulation by hiding sensitive data (VIN)
- class method to calculate the car's age
"""
from datetime import date


class Car:
    wheels = 4  # class attribute

    def __init__(self, make: str, model: str, year: int, vin: str = "UNKNOWN"):
        self.make = make
        self.model = model
        self.year = year
        self.__vin = vin          # name-mangled -> "private"

    # --- encapsulation -------------------------------------------------------
    @property
    def vin(self) -> str:
        """Only the last 4 characters are exposed."""
        return "*" * max(len(self.__vin) - 4, 0) + self.__vin[-4:]

    def verify_vin(self, candidate: str) -> bool:
        return candidate == self.__vin

    # --- behaviour -------------------------------------------------------------
    def display_details(self) -> str:
        return f"{self.year} {self.make} {self.model}"

    def update_info(self, make=None, model=None, year=None) -> None:
        if make:
            self.make = make
        if model:
            self.model = model
        if year:
            if year > date.today().year + 1:
                raise ValueError("year cannot be in the future")
            self.year = year

    @classmethod
    def calculate_age(cls, year: int, current_year: int | None = None) -> int:
        current_year = current_year or date.today().year
        return current_year - year

    def age(self) -> int:
        return Car.calculate_age(self.year)

    def __str__(self) -> str:
        return f"Car({self.display_details()}, VIN {self.vin})"


class ElectricCar(Car):
    def __init__(self, make, model, year, battery_size: float, vin: str = "UNKNOWN"):
        super().__init__(make, model, year, vin)
        self.battery_size = battery_size

    def display_details(self) -> str:   # method overriding
        return f"{super().display_details()} with a {self.battery_size} kWh battery"

    def __str__(self) -> str:
        return f"ElectricCar({self.display_details()}, VIN {self.vin})"


def main() -> None:
    car = Car("Maruti", "Swift", 2019, vin="MA3EWDE1S00123456")
    ev = ElectricCar("Tata", "Nexon EV", 2023, battery_size=40.5, vin="MAT626DZ5PL987654")

    print(car)
    print(ev)

    car.update_info(model="Swift ZXi", year=2020)
    print("Updated:", car.display_details())

    print("Hidden VIN shown as:", car.vin)
    print("Direct access raises AttributeError:", end=" ")
    try:
        print(car.__vin)  # noqa
    except AttributeError as err:
        print(err)
    print("verify_vin works:", car.verify_vin("MA3EWDE1S00123456"))

    print("Car age (class method):", Car.calculate_age(2019, current_year=2026), "years")
    print("EV age:", ev.age(), "years")


if __name__ == "__main__":
    main()

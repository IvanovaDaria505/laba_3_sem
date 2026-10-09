from abc import ABC, abstractmethod

class Pet(ABC):
    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_age(self):
        pass

    @abstractmethod
    def get_age_in_human_years(self):
        pass

    @abstractmethod
    def express(self):
        pass

class Animal(Pet):
    def __init__(self, name, age):
        self._name = name
        self._age = age

    def get_name(self):
        return self._name

    def get_age(self):
        return self._age

    def happy_birthday(self):
        self._age += 1

    @abstractmethod
    def get_age_in_human_years(self):
        pass

    @abstractmethod
    def express(self):
        pass

class Parrot(Animal):
    def get_age_in_human_years(self):
        return max(0, self.get_age()) * 5

    def express(self):
        print(f'{self.get_name()}: "Hello!"')
        print(r"""
       \
       (o>
      \\_//)
       \_/_)
        _|_
""")

class Turtle(Animal):
    def get_age_in_human_years(self):
        age = self.get_age()
        if age <= 0:
            return 0
        return 15 + (age - 1) * 2

    def express(self):
        print(r"""
   _____     ____
  /      \  |  o |
 |        |/ ___\|
 |_________/
 |_|_| |_|_
""")


class Person:
    def __init__(self, name, pet=None):
        self._name = name
        self._pet = pet

    def set_pet(self, pet):
        self._pet = pet

    def get_pet_info(self):
        print("--------------------")

        if self._pet is None:
            print(f"{self._name} has no pet yet")
            print("--------------------")
            return

        print(
            f"Pet for {self._name} is named "
            f"{self._pet.get_name()}"
        )
        print(
            f"Age: {self._pet.get_age()} year(s), "
            f"about {self._pet.get_age_in_human_years()} "
            f"human years"
        )
        print("And it expresses itself like this:")
        self._pet.express()
        print("--------------------")

def main():
    kesha = Parrot("Kesha", 2)
    zavala = Turtle("Zavala", 4)

    kesha.happy_birthday()

    jack = Person("Jack", kesha)
    john = Person("John")

    jack.get_pet_info()
    john.get_pet_info()

    john.set_pet(zavala)
    john.get_pet_info()


if __name__ == "__main__":
    main()

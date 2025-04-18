class Icecream:

    def __init__(self, name: str, flavor: str, price_per_scoop: float):
        self.__name: str = name
        self.__flavor: str = flavor
        self.__price_per_scoop: float = price_per_scoop

    @property
    def name(self):
        return self.__name

    @property
    def flavor(self):
        return self.__flavor

    @property
    def price_per_scoop(self):
        return self.__price_per_scoop


class Cone:
    def __init__(self, scoop_list: list[Icecream] = None):
        if scoop_list is None:
            self.__scoop_list = []
        self.__scoops: list[Icecream] = scoop_list

    @property
    def scoops(self):
        return self.__scoop_list


    @scoops.setter
    def scoops(self, scoop_list: list[Icecream]):
        if len(scoop_list) > 3:
            print("Zu viele Kugeln ausgewählt! Maximal 3 erlaubt.")
        else:
            self.__scoop_list = scoop_list

    def add_icecream(self, icecream: Icecream):
        if len(self.__scoop_list) < 3:
            self.__scoop_list.append(icecream)
        else:
            print("Zu viele Kugeln ausgewählt!!")


list_of_flavors = [
    Icecream("Chocolate Boom", "Chocolate", 3.99),
    Icecream("Vanilla Boom", "Vanilla", 4.99)
]

print("welcome to our ice cream shop")

print("1.Make an order")
print("2. receive invoice")
print("3.pay")
print("4.exit shop")

user_choice = int(input("what would you like to do?"))

if user_choice == 1:
    print("these are our flavors")
    for icecream in list_of_flavors:
        print(f"{icecream.name},{icecream.flavor},{icecream.price_per_scoop}")

    new_order = Cone()

    more_ice = True
    while more_ice:
        user_flavor1 = input("what ice cream flavor would you like? or do you have enough flavors type yes?")
        for flavor in list_of_flavors:
            if user_flavor1 == Icecream.flavor:
                new_order.add_icecream(icecream)
                for scoops in new_order.scoop_list:
                    print(f"{scoops.name},{scoops.flavor},{scoops.price_per_scoop}")
            if user_flavor1 == "yes":
                more_ice = False
            else:
                print("we do not have this flavor.")

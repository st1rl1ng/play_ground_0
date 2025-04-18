class Icecream:

    def __init__(self, name: str, flavor: str, price_per_scoop: float):
        self.__name: str = name
        self.__flavor: str = flavor
        self.__price_per_scoop: float = price_per_scoop
##
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
        self.__scoop_list: list[Icecream] = scoop_list if scoop_list is not None else []

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
            print("Zu viele Kugeln ausgewählt!")


list_of_flavors = [
    Icecream("Chocolate Boom", "Chocolate", 3.99),
    Icecream("Vanilla Boom", "Vanilla", 4.99)
]

print("Willkommen in unserem Eisladen!")

print("1. Bestellung aufgeben")
print("2. Rechnung erhalten")
print("3. Bezahlen")
print("4. Laden verlassen")

user_choice = int(input("Was möchten Sie tun?"))

if user_choice == 1:
    print("Das sind unsere Sorten:")
    for icecream in list_of_flavors:
        print(f"{icecream.name}, {icecream.flavor}, {icecream.price_per_scoop}€")

    new_order = Cone()
    more_ice = True

    while more_ice:
        user_flavor = input("Welche Eissorte möchten Sie? Oder geben Sie 'ja' ein, wenn Sie genug haben: ")
        
        if user_flavor.lower() == "ja":
            more_ice = False
            continue

        found = False
        for flavor in list_of_flavors:
            if user_flavor.lower() == flavor.flavor.lower():
                new_order.add_icecream(flavor)
                found = True
                print("Ihre aktuelle Bestellung:")
                for scoop in new_order.scoops:
                    print(f"- {scoop.name}, {scoop.flavor}, {scoop.price_per_scoop}€")
                break

        if not found:
            print("Diese Sorte haben wir leider nicht.")

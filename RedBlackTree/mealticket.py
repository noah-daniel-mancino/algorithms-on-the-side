'''
Provided test objects for my RB tree
'''
rom random import uniform

class MealTicket():
    """ A simple meal ticket class. """
    ID = 1

    def __init__(self, ticketName):
        """ Constructor for the meal ticket class """
        self.TicketName = ticketName
        self.ticketID = MealTicket.ID
        self.totalCost = 0
        self.items = []
        MealTicket.ID += 1

    def addItem(self, item):
        """ Adds items to the meal tickets """
        self.items.append(item)
        self.totalCost += item[1]
        self.totalCost =  round(self.totalCost, 2)
        return True

    def display(self):
        """ Displays the meal ticket nicely """
        print("=== Displaying Ticket ===")
        print("Ticket Name: ", self.TicketName)
        print("Ticket ID: ", self.ticketID)
        print("Total Cost: ", round(self.totalCost, 2))
        print("Ticket Items: ")
        for i in range(0, len(self.items)):
            print("  Item name: ", self.items[i][0], end="")
            print(" -- Item cost: ", self.items[i][1])
        print("========== End ==========\n")

def generateMealTickets(size):
    """ Generates an array of mealtickets based on the integer <size> """
    mealtickets = []
    for i in range(size):
        ticket = MealTicket("Jared's Meal " + str(i))
        ticket.addItem(("Item 1", round(uniform(0, 30), 2)))
        ticket.addItem(("Item 2", round(uniform(0, 30), 2)))
        ticket.addItem(("Item 3", round(uniform(0, 30), 2)))
        mealtickets.append(ticket)
    return mealtickets


import random

#Village of Hommlet

items = []
locations = {}
monsters = []
gold = 1000.0
health = 1000
character = None

class Character:
    def __init__(self,name):
        self.name = name
        self.gold = 1000
        self.health = 1000
        self.base_strength = 3
        self.base_armor = 1

class Monster:
    def __init__(self,name,location,health,damage,armor,alive):
        self.name = name
        self.location = location
        self.health = health
        self.damage = damage
        self.armor = armor
        self.alive = alive

class Item:
    def __init__(self,name,location,cost,):
        self.name = name
        self.location = location
        self.cost = cost
        self.is_weapon = False
        self.weapon_strength = 0
        self.is_armor = False
        self.armor_strength = 0
        self.is_shield = False

class Location:
    def __init__(self,location_number,location_name,description_str,ground_str,exits,dark_flag,dark_description_str,store_flag):
        self.location_number = location_number
        self.description_str = description_str
        self.ground_str = ground_str
        self.exits = exits
        self.dark_flag = dark_flag
        self.dark_description_str = dark_description_str
        self.store_flag = store_flag

def initialize_items():
    global items
    # open file and get items
    item_file = open("items.txt")
    for line in item_file:
        split_line = line.split(',')
        item = Item(split_line[0],int(split_line[1]),float(split_line[2]))
        if ( split_line[3] == 'True' or split_line[3] == 'true' ):
            item.is_weapon = True
            item.weapon_strength = int(split_line[4])
        if ( split_line[5] == ' True' or split_line[5] == 'true' ):
            item.is_armor = True
            item.armor_strength = int(split_line[6])
        items.append(item)

def parse_exits(exit_str):
    ret_value = {}
    exit_vals = exit_str.split(';')
    for exit_val in exit_vals:
        key,val = exit_val.split('*')
        ret_value[key] = int(val)
    return ret_value

def initialize_locations():
    """Initialize Locations"""
    #open file and read
    location_file = open("locations.txt")
    for line in location_file:
        split_line = line.split('|')
        location_name = None
        location_number = None
        description_str = None
        ground_str = None
        exits = None
        dark_flag = None
        dark_description_str = None
        store_flag = None
        for component in split_line:
            if ( ':' in component):
                name,value = component.split(":")
                if ( name == 'location_name' ):
                    location_name = value
                elif ( name == 'location_number' ):
                    location_number = int(value)
                elif ( name == 'description_str' ):
                    description_str = value
                elif ( name == 'ground_str' ):
                    ground_str = value
                elif ( name == 'exits' ):
                    exits = parse_exits(value)
                elif ( name == 'dark_flag' ):
                    if ( value == 'True' or value == 'true' ):
                        dark_flag = True
                    else:
                        dark_flag = False
                elif ( name == 'dark_str' ):
                    dark_description_str = value 
                elif ( name == 'store_flag' ):
                    if ( value == 'True' or value == 'true' ):
                        store_flag = True
                    else:
                        store_flag = False
        location = Location(location_number,location_name,description_str,ground_str,exits,dark_flag,dark_description_str,store_flag)
        locations[location_number] = location

def initialize_monsters():
    """This is where the program initializes monsters"""
#    def __init__(self,name,location,health,damage,armor,alive):
    monster_file = open("monster.txt")
    for line in monster_file:
        split_line = line.split(',')
        name = split_line[0]
        location = int(split_line[1])
        health = int(split_line[2])
        damage = int(split_line[3])
        armor = int(split_line[4])
        alive = True
        monster = Monster(name,location,health,damage,armor,alive)
        monsters.append(monster)
        

def initialize_game():
    global character
    initialize_items()
    initialize_locations()
    initialize_monsters()
    character = Character("Joe")
    print (character.name,character.health)

def print_word_with_a(name):
    if name[0] == 'a' or name[0] == 'e' or name[0] == 'i' or name[0]=='o' or name[0] == 'u':
        return "an "+name
    else:
        return "a "+name

def print_items(desc_str,location):
    global items
    items_in_location = []
    number_of_items = 0
    print_str = ""
    for item in items:
        if ( item.location == location ):
            items_in_location.append(item)
            number_of_items = number_of_items + 1
    if number_of_items == 1:
        item = items_in_location[0]
        print_str = desc_str + " is " + print_word_with_a(item.name)
    elif number_of_items == 2:
        item0 = items_in_location[0]
        item1 = items_in_location[1]
        print_str = desc_str + " are " + print_word_with_a(item0.name) + " and " + print_word_with_a(item1.name)
    elif number_of_items > 2:
        print_str =  "Lots of items"
        build_str = ""
        for i in range(number_of_items-1):
            build_str = build_str + print_word_with_a(items_in_location[i].name) + ", " 
        build_str = build_str + " and " + print_word_with_a(items_in_location[number_of_items-1].name)
        print_str = desc_str + " are " + build_str
    print (print_str)


def attack_monster(monster,character):
    print ("You attack the",monster.name)
    c_dmg = get_character_damage(character)
    dmg = random.randint(1,c_dmg)
    dmg = dmg - monster.armor
    print ("c_dmg",c_dmg,"monster.amor",monster.armor)
    if ( dmg < 0 ): dmg = 0
    print ("You do ",dmg,"damage")
    monster.health -= dmg
    print (monster.name,"has",monster.health,"health")

def get_character_damage(character):
    current_weapon_str = character.base_strength
    for i in items:
        if ( i.location == 0 and i.is_weapon ):
            if ( current_weapon_str < i.weapon_strength ):
                current_weapon_str = i.weapon_strength
    return current_weapon_str

def get_character_armor(character):
    current_armor_str = character.base_armor
    shield_bonus = 0
    for i in items:
#        print (i.name, i.location, i.is_armor,i.armor_strength)
        if ( i.location == 0 and i.is_armor ):
            if ( current_armor_str < i.armor_strength ):
                current_armor_str = i.armor_strength
#                print "********* Changing armor value"
        print ("***current armor str",current_armor_str,"armor strength",i.armor_strength)
        if ( i.location == 0 and i.is_shield ):
            shield_bonus = 1
#        print ("current armor str",current_armor_str,"armor strength",i.armor_strength)
    return current_armor_str+shield_bonus

def monster_attack(monster,character):
    print ("The",monster.name,"attacks you")
    dmg = random.randint(1,monster.damage)
    dmg = dmg - get_character_armor(character)
    print ("dmg",dmg,"character armor",get_character_armor(character))
    if ( dmg < 0 ): dmg = 0
    print ("The ",monster.name," does ",dmg,"damage")
    character.health -= dmg
    print ("You have",character.health,"health")

def fight_sequence(monster):
    global character
    if ( monster.alive == False ):
        print ("You see a dead",monster.name)
        return
    else:
        print ("You see",print_word_with_a(monster.name))
        while True:
            input = (">")
            if check_val_in_next("attack",input):
                attack_monster(monster,character)
            monster_attack(monster,character)
            if ( character.health < 0 ):
                print ("You are dead")
                exit()
            if ( monster.health < 0 ):
                print("The",monster.name,"is dead")
                monster.alive=False
                return


def print_desc(location_desc,ground_desc,location):
    print (location_desc)
    if ( ground_desc == None):
        pass
    else:
        print_items(ground_desc,location)
    for monster in monsters:
        if monster.location == location:
#            print "You see a",monster.name
            fight_sequence(monster)

def print_inventory():
    print ("Inventory:")
    print ("Gold: %f" % gold)
    for item in items:
        if ( item.location == 0 ):
            print (item.name)


def print_sale_items(location):
    print ("Items for sale include:")
    for item in items:
        if ( item.location == location.location_number * -1  ):
            print (item.name + " ("+ str(item.cost) +" gold)")

def in_inventory(name):
    for item in items:
        if ( item.location == 0 ) and ( name == item.name ):
            return True
    return False

def check_val_in_next(check_val,next):
    if ( check_val in next or check_val.capitalize() in next ):
        return True
    else:
        return False

def get_input(location_number):
    tmp_string = input("> ")
#    if "inventory" in tmp_string or "Inventory" in tmp_string:
#        print_inventory()
    if "quit" in tmp_string or "Quit" in tmp_string:
        print ("Goodbye!")
        exit()
    if check_val_in_next("get",tmp_string)  or check_val_in_next("take" ,tmp_string):
        split_str = tmp_string.split(' ')
#        print "Inside get"
        for item in items:
            if item.name in tmp_string and item.location == location_number:
                item.location = 0
                print ("You got "+ print_word_with_a(item.name))
#            elif :
#                print "You need to buy "+print_word_with_a(item.name)
    if check_val_in_next("drop",tmp_string):
#        print "You are in the drop section"
        split_str = tmp_string.split(' ')
        if ( len(split_str) > 1 ):
            if ( len(split_str) == 2 ):
                pickup_name = split_str[1]
            elif ( len(split_str) == 3 ):
                pickup_name = split_str[1]+' '+split_str[2]
            elif ( len(split_str) == 4):
                pickup_name = split_str[1]+' '+split_str[2]+' '+split_str[3]
            for item in items:
                if split_str[1] == item.name and item.location == 0:
                    item.location = location_number
                    print ("You dropped " +  print_word_with_a(item.name))
    return tmp_string

def  check_exits(next_val,exits):
    for exit_key in exits:
        if ( exit_key in next_val ):
            return exits[key]
    return 0

def check_purchase(location,next_val):
    global gold
    if ( check_val_in_next("buy",next_val) ):
        for item in items:
            if ( item.location == location.location_number*(-1) and item.name in next_val and item.cost <= gold ):
                item.location = 0
                gold = gold - item.cost
                print ("You purchased a %s for %f gold" % (item.name,item.cost))
    else:
        return
    return


def check_sale(location,next_val):
    global gold
    if ( check_val_in_next("sell",next_val) ):
        for item in items:
            if ( item.location == 0 and item.name in next_val ):
                item.location = location.location_number * -1
                print ("You just sold %s for %f gold" % (print_word_with_a(item.name),item.cost*0.8))
                gold = gold + item.cost * 0.8



#15
def lastroom():
    while True:
        print_str = "You enter a treasure room.  On top of a heap of gold, gems, jewelry, and other treasure sits a dragon."
        if in_inventory("sword") and in_inventory("armor") and in_inventory("shield"):
            print ("The dragon breathes fire upon you which you deflect with the shield.")
            print ("It then tries to rake you with its claws, but your armor deflects the claws.")
            print ("You swing at the dragon with your sword and you kill it!")
            print ("Congratulations!  You have won the game.")
            exit()
        elif in_inventory("sword") and not in_inventory("shield") and not in_inventory("armor"):
            print ("You try swinging your sword at the dragon.  Although you manage to wound it.  It breathes fire upon you.")
            print ("You die.  Perhaps if you had some protection you might have survived")
            exit()
        elif in_inventory("shield") and in_inventory("armor") and not in_inventory("sword"):
            print ("You stand in front of the dragon.  It breathes fire upon you which you shield deflects.")
            print ("It then claws at you which your armor protects you from momentarily.")
            print ("Unfortunately you have no weapon to kill the dragon.")
            print ("The dragon takes its mightly body and drops it on top of you.")
            print ("You are dead.  Perhaps if you had a weapon you would be alive.")
            exit()
        else:
            print ("The dragon kills you.  Perhaps if you had a weapon and better protection you would be alive.")
            exit()




current_location = 1



def process_location(location_no):
    if location_no in locations.keys():
        location = locations[location_no]
    else:
        print ("Sorry, the program has made a fatal error")
        print ("There is no location " , location_no)
        exit()
    while True:
#        print "Location %d  dark flag %r lamp %r dark_str %r" % ( location.location_number , location.dark_flag, in_inventory("lamp"), location.dark_description_str  )

        if ( location.dark_flag == False or in_inventory("lamp") or in_inventory("lantern") or location.dark_description_str == None ):
            print_desc(location.description_str,location.ground_str,location.location_number)
        else:
            print_desc(location.dark_description_str,None,location.location_number)
#        print "Store flag:" + str(location.store_flag)
        if (location.store_flag):
            print ("Printing sale items")
            print_sale_items(location)
        next = get_input(location_no)
        if location.exits != None:
            for exit_val in location.exits:
                if ( exit_val in next ):
                    return location.exits[exit_val]
        if (location.store_flag):
            check_purchase(location,next)
            check_sale(location,next)
        if ( check_val_in_next("inventory",next) ):
            print_inventory()


def play_game():
    #start value for goto value
    go_to_value = 1
    while True:
        go_to_value = process_location(go_to_value)


initialize_game()

play_game()

exit()




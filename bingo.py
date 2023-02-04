import random

spaces = [
    "Team quietly stands around the broken robot",
    "Drive laptop unplugged",
    "Funny meme on whiteboard",
    "Fire extinguisher on hand",
    "Jason says something on discord is innapropriate",
    "Oil on the floor",
    "Accident Counter less than 10",
    "Ramen left out on table",
    "Media pretending to be busy",
    "No quarter inch drill bits",
    "None of the batteries are charged",
    "Metal shavings all over the lathe",
    "Jukebox left on",
    "DOOR!!",
    "Fridge empty",
    "Air compressser turning on randomly",
    "3D printer spaghetti",
    "Code kids singing",
    "Couch cover is filthy",
    "CNC machine leaking",
    "Coffee stain on drawings",
    "Coffee pot full",
    "Doors are locked",
    "Being behind schedule",
]

bingoCard = [
    ["", "", "", "", ""],
    ["", "", "", "", ""],
    ["", "", "", "", ""],
    ["", "", "", "", ""],
    ["", "", "", "", ""],
]

trigger = False
random.shuffle(spaces)

for i in range(5):
    for l in range(5):
        if i == 2 and l == 2:
            bingoCard[2][2] += "Free space"
        else:
            bingoCard[i][l] += spaces[0]
            spaces.pop(0)
        if spaces == []:
            break
    if spaces == []:
        break

print("Board:")

for i in range(5):
    print(bingoCard[i])

# --------------------------------------------
# FUNCTIONS
# --------------------------------------------
def load(file_name:str):
    file = open(file_name, "r")
    sections = list()
    
    for entry in file:
        story = entry
        while not story[:3] == "\"\"\"":
            story = file.readline()
        
        story += file.readline()

        while not story.endswith("\"\"\"\n"):
            story += file.readline()
    
        story = story[3:-4]
        numChoices = int(file.readline()[:-1])
    
        jumps_str = file.readline()
        if jumps_str.endswith("\n"): jumps_str = jumps_str[:-1]
        
        if jumps_str == "":
            jumps = list()
        else:
            jumps = jumps_str.split(' ')
    
        for i in range(len(jumps)): jumps[i] = int(jumps[i])
        
        section = {
            "story": story,
            "choices": int(numChoices),
            "jumps": jumps
        }
        
        sections.append(section)
    
    file.close()
    return sections
# -------------------------------------------- END OF FUNCTION

def print_wrap(text:str, width:int, overflow_permissive:bool = False, end:str = ""):
    # split the text into lines
    word_list = text.splitlines()
    for i in range(len(word_list)):
        if word_list[i] == '': # replace blank string with new line
            word_list[i] = '\n'
        else:
            word_list[i] = word_list[i] + '\n'
    
    # split the lines into words
    word_list_copy = word_list.copy()
    word_list = list() # clear word_list
    for i in range(len(word_list_copy)):
        word_list += word_list_copy[i].split(' ')
    
    # print the words
    length = 0
    while len(word_list) != 0:
        word = word_list[0]
        word_list.pop(0)
    
        length += (len(word) + 1)
        
        if overflow_permissive: # allowed to go over the limit by 1 word
            if word.endswith("\n"):
                length = 0
                print(word, end = "")

                continue

            if length >= width:
                length = 0
                print(word, end = "")
            else:
                print(word + " ", end = "")

        else: # not allowed to go over the limit, ever
            if word.endswith("\n"):
                if length >= width:
                    print("\n" + word, end = "")
                else:
                    print(word, end = "")

                length = 0
                continue
        
            if length >= width:
                length = len(word) + 1
                print("\n" + word + " ", end = "")
            else:
                print(word + " ", end = "")
    
    print(end, end = "")
# -------------------------------------------- END OF FUNCTION

# --------------------------------------------
# GAME LOOP
# --------------------------------------------
import os

file_name = "story.txt"
sections = load(file_name)
# print(sections)

section_id = 1
section = sections[section_id - 1]
choice_text = ""

print_width = 100

divider = ""
divider = divider.zfill(print_width)
trans_table = divider.maketrans("0", "-")
divider = divider.translate(trans_table)

while True:
    story = section["story"]
    numChoices = section["choices"]
    jumps = section["jumps"]
    
    if numChoices > 1: choice_text = f"Your choice (1-{str(numChoices)}): "
    else:              choice_text = f"Your choice (1): "
    
    print(f"\n{divider}\n")
    # print(story)
    print_wrap(story, print_width, False)

    if numChoices == 0:
        Input = input("\n> Game over! Hit ENTER to restart the story!")
        os.system('cls' if os.name == 'nt' else 'clear')
        section_id = 1
    else:
        Input = input("\n" + choice_text)
    
        # handle misinputs
        while not (Input.isdecimal() and int(Input) > 0 and int(Input) <= numChoices):
            Input = input("Invalid choice. " + choice_text)

        section_id = jumps[int(Input) - 1]
        
        if section_id - 1 >= len(sections):
            Input = input("\n> This part of the story is still WIP! Hit ENTER to restart the story!")
            os.system('cls' if os.name == 'nt' else 'clear')
            section_id = 1
        
    section = sections[section_id - 1]
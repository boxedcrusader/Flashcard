from tkinter import *
import pandas
import random

data = pandas.read_csv("data/french_words.csv")
data = data.to_dict(orient="records")

stack = [] 
flip_timer = None

def next_card():
    global flip_timer, random_word
    
    if flip_timer:
        window.after_cancel(flip_timer)
        
    available = [word for word in data if word["French"] not in stack]  
    if not available:
        stack.clear()
        available = data
    
    random_word = random.choice(available)
    french_word = random_word["French"]
    stack.append(french_word)
    
    canvas.itemconfig(canvas_image, image=card_front_img)
    canvas.itemconfig(language_text, text="French", fill="black") 
    canvas.itemconfig(word_text, text=french_word, fill="black")  
    
    flip_timer = window.after(3000, flip_card)
    
def flip_card():
    global flip_timer
    english_word = random_word["English"]
    canvas.itemconfig(canvas_image, image=card_back_img)
    canvas.itemconfig(language_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=english_word, fill="white")
    
    flip_timer = window.after(3000, flip_back)
    
def flip_back():
    global flip_timer
    flip_timer = None
    french_word = random_word["French"]
    canvas.itemconfig(canvas_image, image=card_front_img)
    canvas.itemconfig(language_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=french_word, fill="black")

#------------------------------UI SETUP------------------------------#
BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.title("Flashcard App")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

# Images
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
wrong_img = PhotoImage(file="images/wrong.png")
right_img = PhotoImage(file="images/right.png")

# Card
canvas = Canvas( window, width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_image = canvas.create_image(400, 263, image=card_front_img)

language_text = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
wrong_button = Button( window, image=wrong_img, bg=BACKGROUND_COLOR, highlightthickness=0)
right_button = Button( window, image=right_img, bg=BACKGROUND_COLOR, highlightthickness=0, command=next_card)

wrong_button.grid(row=1, column=0)
right_button.grid(row=1, column=1)

next_card()

window.mainloop()
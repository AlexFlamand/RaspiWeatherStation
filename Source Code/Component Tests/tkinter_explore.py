from tkinter import *
from tkinter.ttk import Label

window = Tk()   # Creates window
window.title("Welcome to LikeGeeks app")    # Adds a title to the window
window.geometry('350x200')  # Sets the window size

lbl = Label(window, text = "Hello", font = ("Arial Bold", 50))  # Writes text to the window, with the message "Hello" with the font set to Arial Bold in 50 point size
lbl.grid(column = 0, row = 0)   # Aligns the text

txt = Entry(window, width = 10) # Creates a text box in the window with a width of 10 characters
txt.grid(column = 2, row = 0)   # Aligns the text box
txt.focus() # Has the cursor running in the text box at startup
""" txt = Entry(window, width = 10, state = 'disabled') # Greys out the text box  """

def clicked():  # Button press handler function
    lbl.configure(text = "You're pushing my buttons!")  # Changes the message of the window to "You're pushin my buttons!" when the button is clicked

def clicked2(): # Button press handler function #2
    res = "Welcome to " + txt.get() # Gets the text input from the text box at the button press
    lbl.configure(text = res)   # Writes the contents of the text box at the button press to the screen

btn = Button(window, text = "Click Me", bg = "yellow", fg = "blue", command = clicked2) # Creates a button with the label "Click Me" with the background color set to yellow and foreground color set to blue, and redirects the button press to the method clicked2()
btn.grid(column = 3, row = 0)   #Aligns the button

window.mainloop()   # Keeps the window open
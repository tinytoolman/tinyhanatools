#-------------------------------------------------------------------------------
# Name:        showme.py
# Project:     TinyTools
# version:     1.05
# Author:      Tinus Mario Brink
#
# Created:     20/07/2023
# Copyright:   (c) Schoeman and Brink LLC 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------
'''
You might be wondering, what is this piece of code for?  Well, it something
that you are more than welcome to remove, although it's just here for fun.
While I created the tool, I wanted to demo it at a management meeting and the
night before Vian Booysen told me that if it contained any bubbles he would drop
off the call.  There is some history here with bubbles by the way or Vian just
hates them, :).  So the night before, I generated this piece of code just for
Vian.  If you type bubbles as an option on the main menu screen, it displays
BUBBLES!!! EVERYWHERE!!!  You can press any key to exit
'''

import curses
import time
import random


def display_bubbles(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)  # Non-blocking getch()

    max_y, max_x = stdscr.getmaxyx()

    while True:
        stdscr.clear()

        # Generate random coordinates for the word "BUBBLES"
        y = random.randint(0, max_y - 1)
        x = random.randint(0, max_x - len("BUBBLES"))

        stdscr.addstr(y, x, "BUBBLES")

        # Generate random coordinates for bubbles
        for _ in range(10):
            bubble_y = random.randint(0, max_y - 1)
            bubble_x = random.randint(0, max_x - 1)

            # Choose random bubble character ('O' or 'o')
            bubble_char = random.choice(["O", "o"])

            stdscr.addch(bubble_y, bubble_x, bubble_char)

        stdscr.refresh()
        time.sleep(2)

        # Check if any key is pressed to interrupt the animation
        key = stdscr.getch()
        if key != curses.ERR:
            break


def main():
    curses.wrapper(display_bubbles)


if __name__ == "__main__":
    main()




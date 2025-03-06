# import sqlite3
# import numpy
import matplotlib.pyplot as plt # type: ignore

try:
    # grab data from sql db
    plt.style.use('bmh')
    title_font_size = 12
    fig,ax = plt.subplots()
    # ax.plot(...) # Fix this line
    ax.set_title('Presidential Elections of USA', fontsize=title_font_size*2)
    ax.set_xlabel('...', fontsize=title_font_size)
    ax.set_ylabel('...', fontsize=title_font_size)
    # Represent 50% of popular vote
    # Vertical Line
    # fifty_line = ax.axvline(x=50.0, color='yellow', label='50 percent')
    # Horizontal Line
    fifty_line = ax.axhline(y=50.0, color='yellow', label='50 percent')
    # Represent 51% of popular vote
    clear_winner_line = ax.axhline(x=51.00)
except:
    print('Database is not connected!')
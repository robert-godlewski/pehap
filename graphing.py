import sqlite3
# import numpy
import pandas # type: ignore
import matplotlib.pyplot as plt # type: ignore

con = sqlite3.connect('db.sqlite3')

try:
    # grab data from sql db
    # election_year_script = "SELECT * FROM election_year"
    # years_raw = pandas.read_sql_query(sql=election_year_script, con=con)
    # print(years_raw)
    # Graph data
    # Make one for the popular votes and 1 for the electoral votes
    plt.style.use('bmh')
    title_font_size = 12
    fig,ax = plt.subplots()
    # ax.plot(...) # Fix this line to make a stacked bar graph or just a plain bar graph
    ax.set_title('USA Presidential Election Popular Votes', fontsize=title_font_size*2)
    ax.set_xlabel('Election Years', fontsize=title_font_size)
    ax.set_ylabel('Percentage of Popular Vote', fontsize=title_font_size)
    # Represent 50% of popular vote
    # Vertical Line - Don't use
    # fifty_line = ax.axvline(x=50.0, color='yellow', label='50 percent')
    # Horizontal Line
    fifty_line = ax.axhline(y=50.0, color='yellow', label='50 percent')
    # Represent 51% of popular vote
    clear_winner_line = ax.axhline(y=51.0, color='green', label='51 percent')
    # ...
    ax.legend(loc='upper left', prop={'size':6})
    # plt.savefig('USA_election_results.png')
    plt.show()
except:
    print('Database is not connected!')

con.close()

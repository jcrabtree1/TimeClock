TODO List for TimeClock
=======================

 - Tweak the main application (timeclock.py) so that we have a 
   *main* function and supporting *clock_in*, *clock_out*, etc.
   funtions.

 - ~~If no timekeeper database exists, the program should create one
   and initialize it with the appropriate schema.~~

 - Fix the README.md so that it looks right

 - Create a proper testing suite:
   * Does the program work with correct inputs?
   * Does the program break with incorrect inputs?
   * If the program breaks, is the error message useful?
   * If the program breaks, are incorrect transactions rolled back?
   * Are correct transactions properly committed?
   * Is it prone to user error?

 - If you have time, try and make the date and time formatting 
   required by the user a bit more flexible.

 - Maybe allow for keyword arguments like *today* or *now*.

 - Make a branch and re-write the reporting section to do the data
   manipulation in SQL and then plot the data using gnuplot.
   Hopefully this will make life a little easier.


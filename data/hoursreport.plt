cd '.'
set datafile separator "|"
set terminal pngcairo size 900,400
set title "{} Hours Worked"
set ylabel "Hours"
set xlabel "Date"
set xdata time
set timefmt "%Y-%m-%d"
set format x "%m/%d"
set key left top
set grid
set output "{} Hours.png"
plot "hoursrpt" using 1:8 with lines lw 2 lt 3 title 'Daily Hours', \
     "hoursrpt" using 1:9 with lines lw 2 lt 4 title 'Avg Hours'
set output

set xrange [-1.5:1.5]
set yrange [-1.5:1.5]
plot "< tail -10 sensor.txt" using 2:3 w l
pause 0.1
reread

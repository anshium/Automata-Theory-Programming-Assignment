$lines = @(
    "a",
    "print b",
    "print 3.4",
    "print 3",
    "a b c",
    "if a print",
    "if a print b",
    "if a print b else print c",
    "if a + b print b else print c",
    "if a + b > c print b",
    "if a + 2 > 3 print -1",
    "if 5 + 4 > 3 print -1",
    "if 5 + 4.6 > 3 print -1",
    "print 4 if c - 4 print k",
    "print 4 if c - 4 print k else print 5 if 3 ^ 6 < 4 < print print wa else print 10.3",
    "if a * c = b / d if z = print = q print b else print",
    "if a * c = b / d if z = print = q print b else print else print o",
    "if a * c = b / d if z = print = q print b if le print 3.4 else print else print o",
    "if 1 print 2 else if 2 print 3 else print 1"
)

foreach ($line in $lines) {
    echo "$line" | python.exe .\compiler9.py # >> output.txt
}

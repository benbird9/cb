count = 0
TOTAL_BONDS = 18
with open('tradehistory.txt', 'r') as f:
    for line in f:
        words = line.split()
        count = count + float(words[5]) - float(words[2])

print count/TOTAL_BONDS
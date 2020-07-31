count = 0
TOTAL_BONDS = 18
with open('trade\\cb.trade.history.txt', 'r',encoding='gb18030', errors='ignore') as f:
    for line in f:
        words = line.split()
        count = count + float(words[5]) - float(words[2])

print(count/TOTAL_BONDS)
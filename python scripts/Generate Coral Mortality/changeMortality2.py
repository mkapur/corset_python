f1 = open(r'C:/Users/mkapur/Dropbox/_CORSET/New folder/MAR_coral_mortality_4.txt', 'r')
f2 = open(r'C:/Users/mkapur/Dropbox/_CORSET/New folder/MAR_coral_mortality_2.txt', 'w')
for line in f1:
    f2.write(line.replace('[0.05,0.15]', '[0.002,0.20]'))
f1.close()
f2.close()
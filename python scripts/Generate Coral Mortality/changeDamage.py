f1 = open(r'C:/Users/mkapur/Dropbox/_CORSET/MHI_input/user_coral_mortality_2.txt', 'r')
f2 = open(r'C:/Users/mkapur/Dropbox/_CORSET/MHI_input/MAR_coral_mortality_4.txt', 'w')
for line in f1:
    f2.write(line.replace('[0.002,0.20]','[0.05,0.15]'))
f1.close()
f2.close()
from fastparquet import ParquetFile
import matplotlib.pyplot as plt
import numpy as np
pf = ParquetFile('')
df = pf.to_pandas()

#print(df)
#print (df['grade'])

#to check the results:
# df.to_csv('')

grade_avg = df['grade'].mean()
grade_median = df['grade'].median()

print("The average grade is: ", grade_avg)
print("The median grade is: ", grade_median)


#plt.hist(df['grade'], histtype='bar', align='mid', orientation='vertical')
bin_values = np.arange(start=40, stop=110, step=10) #I can just make a loop to create this one
df['grade'].hist(bins=bin_values, figsize=[14,6])
plt.show()
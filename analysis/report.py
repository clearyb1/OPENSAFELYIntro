import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("output/input.csv")

sns.set_style('white')
sns_plot = sns.distplot(data['age'], hist=False, 
                    kde_kws={'shade':True})
fig = sns_plot.get_figure()
fig.savefig("output/descriptive.png")

sns_plot2= sns.regplot(x="age", y="bmi", data=data)
fig = sns_plot.get_figure()
fig.savefig("output/descriptive2.png")

#https://stackoverflow.com/questions/32244753/how-to-save-a-seaborn-plot-into-a-file

data = data[data.covid_vacc_third_dose_date != None]

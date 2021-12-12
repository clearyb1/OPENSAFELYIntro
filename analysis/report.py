import pandas as pd
import seaborn as sns

data = pd.read_csv("output/input.csv")

fig = data.age.plot.hist().get_figure()
fig.savefig("output/descriptive.png")

sns.set_style('white')
fig2 = sns.distplot(data['age'])
fig.savefig("output/descriptive2.png")
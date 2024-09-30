# GDP: https://data.worldbank.org/indicator/NY.GDP.MKTP.CD
# Population: https://ourworldindata.org/grapher/population
# Working age population: https://fred.stlouisfed.org

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

COUNTRIES = ["U.S.", "China", "Germany", "Japan", "U.K.", "France", "Italy", "Canada"]
COLORS = ["r", "g", "b", "c", "m", "y", "k", "#234512"]

_gdp, _pop, _wap = pd.read_csv("data/gdp.csv"), pd.read_csv("data/population.csv"), pd.read_csv("data/working_age_population.csv")
gdp, pop, wap = _gdp[["year"] + COUNTRIES], _pop[["year"] + COUNTRIES], _wap[["year"] + COUNTRIES]

print("Correlation coefficients between GDP and populations:")
for country in COUNTRIES:
    print(f"{country.rjust(max([len(w) for w in COUNTRIES]))}: {round(np.corrcoef(gdp[country], pop[country])[0][1], 3): .3f} -- {gdp['year'][0]}-{gdp['year'].iat[-1]} ({gdp['year'].iat[-1] - gdp['year'][0] + 1} years)")

print("Correlation coefficients between GDP and working age populations:")
for country in COUNTRIES:
    bound = wap[["year", country]].dropna(how='any')["year"].min()
    print(f"{country.rjust(max([len(w) for w in COUNTRIES]))}: {round(np.corrcoef(gdp[gdp['year'] >= bound][country], wap[wap['year'] >= bound][country])[0][1], 3): .3f} -- {bound}-{wap['year'].iat[-1]} ({wap['year'].iat[-1] - bound + 1} years)")

pop[COUNTRIES], wap[COUNTRIES] = pop[COUNTRIES].astype(float), wap[COUNTRIES].astype(float)

gdp.loc[:, COUNTRIES] = gdp.loc[:, COUNTRIES].apply(lambda v: v / 1e12)
pop.loc[:, COUNTRIES] = pop.loc[:, COUNTRIES].apply(lambda v: v / 1e6)
wap.loc[:, COUNTRIES] = wap.loc[:, COUNTRIES].apply(lambda v: v / 1e6)

fig = plt.figure(figsize=(16, 9))

ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)

for i, country in enumerate(COUNTRIES):
    ax1.plot(gdp["year"], gdp[country], label=country, color=COLORS[i])
    ax2.plot(pop["year"], pop[country], label=country, color=COLORS[i])
    ax2.plot(wap["year"], wap[country], "--", color=COLORS[i])

ax1.set_title("GDP")
ax1.set_xlim([gdp["year"][0], gdp["year"].iat[-1]])
ax1.set_xlabel("A.D.")
ax1.set_ylabel("Trillion USD")
ax1.grid()
ax1.legend()
ax1.set_yscale("log")

ax2.set_title("Population and Working Age Population")
ax2.set_xlim([1960, 2023])
ax2.set_xlabel("A.D.")
ax2.set_ylabel("Million people")
ax2.grid()
ax2.legend()
ax2.set_yscale("log")

fig.suptitle("Historical GDPs, Populations, and Working Age Populations of G7 and China")
fig.tight_layout()

plt.savefig("out/out.png", dpi=350)
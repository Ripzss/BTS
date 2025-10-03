#Frost APi
#Client Id 93c4a7c8-3004-4efa-97a3-753a3b2b0d46
#Client Secret 93c4a7c8-3004-4efa-97a3-753a3b2b0d46
import requests
import matplotlib.pyplot as plt
import json
import calendar

client_id = "93c4a7c8-3004-4efa-97a3-753a3b2b0d46"
url = 'https://frost.met.no/observations/v0.jsonld'

parameters = {
    'sources': 'SN50540',
    'elements': 'sum(precipitation_amount P1D)',
    'referencetime': '2020-01-01/2020-12-31'
}

r=requests.get(url, parameters, auth=(client_id, ''))
#3
data = r.json()

prec_per_month = {}
#Parse through the data. Make a dictionary of the total rain by month.
for observation in data['data']:
    # Hent måned fra referenceTime (format: YYYY-MM)
    reference_time = observation['referenceTime']
    month = reference_time[:7]  # Tar første 7 tegn (YYYY-MM)
    prec = observation['observations'][0]['value']

    if month in prec_per_month:
        prec_per_month[month] += prec
    else:
        prec_per_month[month] = prec

#sorterer måndene i riktig rekkefølge
months = sorted(prec_per_month.keys())
tot_prec = [prec_per_month[month] for month in months]

#konverter til forkortede månedsnavn
month_names = []
for month_str in months:
    month_num = int(month_str.split('-')[1])  # Hent månedsnummeret
    month_abbr = calendar.month_abbr[month_num]  # Få forkortet navn
    month_names.append(month_abbr)

#Lager Søylediagram
fig = plt.figure(figsize=(12,6))
ax = plt.axes()

#Lag Søyler med numeriske x-verdie
xticks = list(range(len(month_names)))
xtick_vals = month_names
ax.bar(xticks, tot_prec, color='steelblue', edgecolor='black')
ax.set_xticks(xticks)
ax.set_xticklabels(xtick_vals)

#X og Y Label og Tittel
ax.set_xlabel('Måned', fontsize=12)
ax.set_ylabel('Nedbør (mm)', fontsize=12)
ax.set_title('Total nedbør per måned i Bergen 2020', fontsize=14, fontweight='bold')

plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()

#viser figuren
plt.show()



#Api Request Checker
if r.status_code == 200:
    data = r.json()
    print(data)
else:
    #request failed
    print(f"Error: {r.status_code}")
    print(r.text)


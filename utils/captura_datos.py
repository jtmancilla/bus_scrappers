#!/usr/bin/env python

import scrapper
import pandas as pd


url="https://www.clickbus.com.mx/es/buscar/puebla-pue-todas-las-terminales/ciudad-de-mexico-df-%28todas-las-terminales%29/?isGroup=0&ida=2018-01-09&volta=#/step/departure"
scrapper = scrapper.Clickbus(url)

ver = scrapper.wrap_info()

df = pd.DataFrame(ver)

df.to_csv('~/Dropbox/Projects/bus_scrappers/resultados.csv',index=False,header=False,encoding="UTF8")

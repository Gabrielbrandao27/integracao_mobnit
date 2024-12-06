import pandas as pd

def merge_databases():

  df_transnit = pd.read_excel("./excel/transnit.xlsx", header=5)
  df_transoceanico = pd.read_excel("./excel/transoceanico.xlsx", header=5)

  infos_finais = pd.concat([df_transnit, df_transoceanico], ignore_index=True).fillna('')

  print(infos_finais.columns)
  print(infos_finais)

  infos_finais.to_csv('./excel/consolidado.csv', index=False)

def get_by_company(company_name):
  infos_onibus = pd.read_csv('./excel/consolidado.csv')
  return infos_onibus.loc[infos_onibus['EMPRESA'] == company_name]

def get_company_compliance(company_name):
  company_buses = get_by_company(company_name)
  print("Ônibus da empresa")
  print(company_buses)
  print("\n")
  bus_amount = len(company_buses)
  non_compliant_buses = company_buses.loc[company_buses['AR CONDICIONADO'] == 'NÃO']
  print("Ônibus da empresa sem ar condicionado")
  print(non_compliant_buses)
  print("\n")
  non_compliant_amount = len(non_compliant_buses)
  return ((bus_amount - non_compliant_amount)/bus_amount) * 100

if __name__ == '__main__':
  print(get_company_compliance('INGÁ'))
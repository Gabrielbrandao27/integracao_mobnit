# integracao_mobnit
Projeto de integração com a aplicação de mobilidade niteroiense "MobNit".

## Critérios de Avaliação:
### climatização, viagens, ônibus em circulação e quilometragem

1. Cumprimento de viagens programadas em relação às viagens realizadas
2. Produção de quilometragem realizada em relação à quilometragem programada
3. Climatização da frota
4. Quantidade de ônibus circulando em relação à quantidade de ônibus programada

# Tabela de relação Escala de Cumprimento x Subsídio a Receber

| Escala de Cumprimento(%)   | Subsídio a Receber (%) |
|:--------------------------:|:----------------------:|
|        100-95              |        100             |
|         94-90              |         95             |
|         89-85              |         85             |
|         84-80              |         70             |
|         <80                |          0             |



# Tutorial para execução:

1. `cartesi address-book` para buscar o endereço do contrato InputBox
2. `cd dapp` para entrar na pasta do dApp e `cartesi build` para buildar o dApp
3. `cartesi run` para rodar o dApp e a blockchain local utilizando Docker
4. `cd ../migrador` em um novo terminal para entrar na pasta do migrador que enviará o input para a blockchain
5. `python migrador.py` para executar o script e enviar o input
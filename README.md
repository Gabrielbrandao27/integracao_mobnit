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



# Passos para execução do projeto:

## Pré-requisitos:
* Utilizando versão python 3.7 ou superior.
- Migrador: `pip install pandas web3 python-dotenv brotli requests`
- DApp: podem ser encontrados através deste link da documentação da Cartesi: https://docs.cartesi.io/cartesi-rollups/1.5/development/installation/
- Frontend: Node.js (instalado no requisito do dApp)

## Tutorial:
1. Abrir o Docker Desktop
2. `cd dapp` para entrar na pasta do dApp e `cartesi build` para buildar o dApp
3. `cartesi run` para rodar o dApp e a blockchain local utilizando Docker
4. `cd../frontend` em um novo terminal para entrar na pasta do frontend
5. `npm install` para instalar as dependências e `npm run dev` para rodar o frontend
6. `cd ../migrador` em um novo terminal para entrar na pasta do migrador que enviará o input para a blockchain
7. `python migrador.py` para executar o script e enviar o input
8. Visualize tanto no console do terminal na aba do dapp quanto na web page os dados expostos

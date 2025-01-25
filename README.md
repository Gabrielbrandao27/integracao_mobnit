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

<br><br>
# Instruções para execução em "Self-Host Mode":

Este tutorial irá possibilitar a visualização dos logs e reports sendo gerados na Blockchain Testnet através do Inspect para o dApp quando o usuário interage com o Dashboard na web page.
Além disso, é possível visualizar os logs do método Advance quando o Migrador executa todo primeiro dia do mês e envia um input para o dApp.
<br>

## Pré-requisitos (este tutorial leva em consideração um ambiente baseado em Linux):
- Docker Desktop pode ser instalado através deste link: https://docs.docker.com/desktop/setup/install/linux/ após escolher a sua plataforma
- postgreSQL instalado com `apt install postgresql`
- imagem do postgreSQL no Docker `docker run --name some-postgres -p 15432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres`

## Tutorial:
1. `cd dapp` para entrar na pasta do dApp
2. Se estiver usando uma máquina virtual, deve adicionar o repositório "integracao_mobnit" à sua VM
 via `git clone https://github.com/Gabrielbrandao27/integracao_mobnit.git`
3. `docker run --network host --env-file 0x70aaf0ca43414eee87991f5bc3b1773d629b364f61c5d6d4fde1d3a7e0b1c09d.env -p 10000:10000  gabrielbrandao2711/integracao_mobnit_dapp_build`
 para baixar a imagem do Docker Hub, adicionar ao seu Docker local e executá-la.
4. Acesse o website via [Subsídio MobNit Dashboard](http://dashboard-subsidios.s3-website.us-east-2.amazonaws.com/)
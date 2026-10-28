# Gerador de JSONs para SCADA-LTS

Aplicação em Python para gerar arquivos JSON de configuração de usinas para o **SCADA-LTS 2.7**, a partir dos modelos disponíveis no repositório.

O programa funciona pelo terminal: você informa os dados da usina, escolhe o equipamento e responde às perguntas para gerar seus Data Sources, Data Points e, quando aplicável, Point Links.

## Requisitos

- Python 3 instalado, com o comando `python` disponível no terminal.
- Todos os arquivos e pastas deste repositório, pois os geradores utilizam os modelos JSON locais.

Os scripts utilizam apenas bibliotecas padrão do Python; não é necessário instalar pacotes com `pip`.

## Como iniciar

1. Baixe o repositório ou faça seu clone pelo GitHub.
2. Abra o terminal na pasta `Gerador-de-Json`.
3. Confira se o Python está disponível:

   ```bash
   python --version
   ```

4. Inicie a aplicação:

   ```bash
   python app.py
   ```

Execute os comandos na raiz do projeto, onde está o arquivo `app.py`, para que os scripts encontrem seus modelos.

## Como utilizar

Ao iniciar, o programa solicita:

- **Nome da usina:** nome usado na identificação dos equipamentos.
- **Prefixo da usina:** identificador usado na composição dos nomes e identificadores gerados. Utilize o mesmo prefixo em todas as gerações da mesma usina.

Em seguida, digite o **número da opção** desejada e pressione Enter:

| Opção | Geração |
| --- | --- |
| 0 | Configuração |
| 1 | Inversor |
| 2 | SmartLogger |
| 3 | ETM |
| 4 | NCU |
| 5 | Tracker |
| 6 | Nobreak |
| 7 | Multimedidor |
| 8 | Gerar tudo |
| 9 | Cálculos |
| 10 | Relé |
| 11 | Câmeras |
| 12 | Medidor |
| 13 | Trafo |
| 14 | Combiner Box |
| 15 | DJBT |
| 16 | IO Remoto |
| 17 | Parque |

As próximas perguntas variam conforme a opção escolhida. Tenha em mãos o tipo do equipamento, IP, Slave ID, quantidades e identificação do skid ou da cabine, quando solicitados.

Quando o programa pedir o **tipo**, informe a letra correspondente ao modelo do repositório, como `A`, `B` ou `C`. Por exemplo, o modelo `ETM_TIPO_A` corresponde ao tipo `A`. Confira os arquivos da pasta do equipamento para identificar os modelos disponíveis e utilize letras maiúsculas.

### Exemplo: gerar inversores

O exemplo abaixo considera uma usina com um skid e dois inversores do tipo B. Os valores são ilustrativos e devem ser substituídos pelos dados reais da instalação.

```text
Nome da usina: Usina Exemplo
Prefixo da usina: UEX
Qual Json quer gerar? 1
Quantos Skids existem? 1
Tipo do inversor ? B

--- Skid 1 ---
IP do DataSource: 192.168.1.100
Quantidade de inversores: 2
Primeiro slaveId: 1
```

Nesse caso, o arquivo é gerado em `saida/inversor1.json`. Para vários skids, o programa repete as perguntas de IP, quantidade e primeiro Slave ID para cada skid.

Nas opções individuais, a aplicação normalmente encerra após a geração. Para gerar outro equipamento da mesma usina, execute `python app.py` novamente e mantenha o mesmo nome e prefixo.

### Gerar tudo

A opção **8 — Gerar tudo** percorre as etapas de configuração e dos equipamentos, solicitando os dados de cada uma. Escolha essa opção quando precisar executar o fluxo completo; para gerar apenas determinados equipamentos, utilize as opções individuais.

Ao final, o programa pergunta:

```text
Deseja unir os arquivos em um unico arquivo? (S/N):
```

Digite `S` para gerar o arquivo consolidado `saida_final.json` na raiz do projeto.

## Onde encontrar os arquivos

Os JSONs gerados ficam na pasta `saida`, criada automaticamente pelos geradores. Exemplos de arquivos:

```text
Gerador-de-Json/
├── app.py
├── UnirJsons.py
├── saida/
│   ├── DadosConfig.json
│   ├── inversor1.json
│   ├── smartlogger1.json
│   └── ETM1.json
└── saida_final.json
```

Os nomes e a quantidade de arquivos dependem das opções utilizadas. O arquivo `saida_final.json` só é criado quando a união é executada.

## Como unir os JSONs

Também é possível consolidar os arquivos após gerar os equipamentos individualmente. Na raiz do projeto, execute:

```bash
python UnirJsons.py
```

O script lê todos os arquivos `.json` diretamente na pasta `saida` e reúne as listas `dataSources`, `dataPoints` e `pointLinks` em `saida_final.json`. Point Links individuais com `sourcePointId` e `targetPointId` também são incluídos.

Antes de unir, confira se a pasta `saida` contém apenas os arquivos que devem fazer parte daquela configuração. O script não filtra por usina nem elimina duplicidades, e uma nova união sobrescreve `saida_final.json`.

## Cuidados e problemas comuns

- **Ao iniciar uma nova usina:** guarde os resultados anteriores e esvazie a pasta `saida` para evitar misturar configurações. Alguns geradores sobrescrevem arquivos existentes; outros podem apresentar erro quando o destino já existe.
- **Python não reconhecido:** verifique a instalação e a disponibilidade do comando `python` no PATH. O `app.py` também utiliza esse comando para executar os geradores.
- **Modelo ou arquivo não encontrado:** confirme que o terminal está na raiz do projeto, que as pastas dos modelos estão presentes e que o tipo informado existe para aquele equipamento.
- **Erro ao informar quantidades:** preencha os campos numéricos com números inteiros, sem texto adicional.
- **Interromper a execução:** pressione `Ctrl+C` no terminal. Arquivos já gerados podem permanecer na pasta `saida`.

Antes de importar no SCADA-LTS, revise os arquivos gerados, incluindo prefixos, IPs, Slave IDs e referências entre os pontos. Confira também as mensagens de cada etapa: a mensagem final do fluxo completo não substitui a verificação de eventuais erros dos geradores.

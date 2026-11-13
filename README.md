# Diagnóstico Energético Residencial

## 1. Integrantes

| Integrante           | RM     |
|----------------------|--------|
| Felipe Doern         | 568798 |
| Miguel Marcelo       | 569467 |
| Victor Binot         | 571499 |

### Links do projeto

- **Repositório GitHub:** https://github.com/victorcbinot/GS_2026.02_SERS
- **Vídeo de apresentação:** PREENCHER COM O LINK DO VÍDEO

## 2. Sobre o projeto

O **Diagnóstico Energético Residencial** é um simulador desenvolvido em Python com o objetivo de auxiliar residências a compreender seu consumo de energia elétrica e avaliar alternativas para reduzir custos e impactos ambientais.

A aplicação utiliza dados tarifários disponibilizados pela Agência Nacional de Energia Elétrica (ANEEL) e permite simular dois caminhos para um consumo residencial: a adoção de medidas de eficiência energética e a instalação de um sistema de energia solar fotovoltaica.

A partir das informações fornecidas pelo usuário, o programa apresenta estimativas de custos, economia financeira, dimensionamento solar e emissões de CO₂ associadas ao consumo de eletricidade.

O projeto também conta com o **Citizen Assist AI**, um chatbot executado no terminal que apresenta o simulador, responde dúvidas sobre consumo e economia de energia, coleta os dados necessários, executa o diagnóstico energético e explica os resultados em linguagem simples. O chatbot reutiliza os mesmos cálculos e módulos do simulador original.

## 3. Problema identificado

O consumo de energia elétrica representa uma despesa recorrente para as famílias. Entretanto, nem sempre os consumidores conhecem o impacto financeiro de seus hábitos de consumo ou as alternativas disponíveis para melhorar a eficiência energética de suas residências.

Além disso, a escolha de uma solução sustentável envolve diferentes fatores, como investimento inicial, economia potencial, viabilidade financeira e impactos ambientais.

Diante desse cenário, o projeto propõe uma ferramenta simples para ajudar o consumidor residencial a visualizar e comparar alternativas energéticas.

## 4. Objetivos

- Analisar o consumo mensal de energia elétrica de uma residência.
- Consultar tarifas residenciais das distribuidoras de energia.
- Estimar o custo referente às componentes TE e TUSD.
- Simular diferentes cenários de redução do consumo.
- Estimar a potência e a geração de um sistema solar fotovoltaico.
- Comparar os resultados financeiros e ambientais das alternativas.
- Oferecer uma interação por chatbot no terminal para orientar o usuário e explicar os resultados.
- Apresentar informações que auxiliem na tomada de decisão.

## 5. Público-alvo

O projeto é direcionado a consumidores residenciais que desejam compreender melhor seus gastos com energia elétrica e conhecer alternativas para tornar o consumo mais eficiente e sustentável.

## 6. Funcionamento da aplicação

A aplicação é utilizada por meio do chatbot **Citizen Assist AI**, que funciona diretamente no terminal e reutiliza os módulos de cálculo do projeto.

### 6.1. Citizen Assist AI (chatbot)

O chatbot apresenta o seguinte menu:

1. **Fazer diagnóstico energético:** coleta distribuidora, mês de referência, consumo mensal e valor da conta, executa o diagnóstico e explica os resultados em linguagem simples.
2. **Tirar dúvidas sobre consumo e economia de energia:** responde perguntas sobre consumo, eficiência energética, energia solar, tarifas, investimento, retorno estimado e emissões de CO₂.
3. **Ver fontes de dados e limitações:** apresenta as fontes utilizadas e as principais limitações das estimativas.
4. **Encerrar a conversa:** finaliza o chatbot.

Após um diagnóstico, o usuário pode voltar ao menu para realizar uma nova simulação ou encerrar o programa. As respostas do chatbot são baseadas nos cálculos do projeto e não substituem os resultados calculados pelo próprio sistema.

### 6.2. Etapas do diagnóstico energético

Dentro da opção 1 do chatbot, o diagnóstico segue as seguintes etapas:

1. **Identificação da distribuidora:** o usuário informa sua distribuidora de energia elétrica. Caso o nome não seja encontrado, o programa apresenta uma lista numerada com as distribuidoras disponíveis.
2. **Seleção do período:** informa o mês e o ano de referência disponíveis na base tarifária. Caso o mês informado não esteja disponível, o programa apresenta uma lista numerada com os meses válidos.
3. **Informações de consumo:** informa o consumo mensal em kWh e o valor total da conta de energia em reais.
4. **Diagnóstico energético:** o programa consulta a tarifa residencial e estima o custo referente à TE e à TUSD.
5. **Eficiência energética:** apresenta cenários hipotéticos de redução de consumo de 5%, 10% e 15%.
6. **Energia solar:** estima a potência necessária, a geração mensal e anual e o investimento inicial de referência.
7. **Comparação:** apresenta os resultados financeiros e ambientais das alternativas.

## 7. Alternativas analisadas

### 7.1. Situação atual

Representa o cenário de referência, considerando o consumo informado pelo usuário e a tarifa residencial encontrada na base da ANEEL.

O custo estimado é calculado utilizando a soma das componentes TE e TUSD.

### 7.2. Eficiência energética

A eficiência energética busca reduzir o consumo de eletricidade sem necessariamente comprometer o conforto dos moradores.

O programa apresenta três cenários hipotéticos:

- Redução de 5% do consumo.
- Redução de 10% do consumo.
- Redução de 15% do consumo.

Os percentuais são utilizados como hipóteses de simulação, não como economias garantidas.

### 7.3. Energia solar fotovoltaica

A energia solar fotovoltaica utiliza painéis para converter a radiação solar em eletricidade.

O simulador estima a potência de um sistema capaz de atender ao consumo mensal informado e calcula uma referência de investimento inicial.

A alternativa é apresentada como uma possibilidade de geração de energia renovável no próprio imóvel.

## 8. Fontes de dados

O projeto utiliza fontes públicas e parâmetros de referência para realizar suas estimativas.

### 8.1. ANEEL - Tarifas de energia elétrica

**Fonte:** Agência Nacional de Energia Elétrica (ANEEL).

**Base utilizada:** Tarifas de aplicação das distribuidoras de energia elétrica.

Link: https://dadosabertos.aneel.gov.br/dataset/tarifas-distribuidoras-energia-eletrica

A base fornece informações tarifárias das distribuidoras brasileiras. O programa utiliza os registros referentes à classe residencial B1, modalidade convencional e tarifa de aplicação.

São utilizadas duas componentes:

- **TE (Tarifa de Energia):** componente relacionada à energia elétrica consumida.
- **TUSD (Tarifa de Uso do Sistema de Distribuição):** componente relacionada ao uso da infraestrutura de distribuição.

Os valores disponibilizados na base são expressos em R$/MWh e convertidos para R$/kWh por meio da divisão por 1.000.

O programa consulta os dados por meio da API pública de dados abertos da ANEEL, sem necessidade de chave de acesso, e salva os registros processados em um arquivo CSV.

**Período de referência:** são considerados os registros vigentes no momento em que a base é processada. Portanto, a disponibilidade de meses depende da vigência das tarifas encontradas.

A aplicação trabalha com meses completos dentro do período de vigência tarifária. Meses parcialmente abrangidos pela vigência não são disponibilizados para seleção.

A base não preserva automaticamente o histórico de tarifas anteriores. Por isso, meses passados que não estejam presentes nos registros processados não podem ser consultados pelo simulador.

### 8.2. EPE - Referência de custo de instalação solar

**Fonte:** Empresa de Pesquisa Energética (EPE), com dados de mercado da Greener.

Link: https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-957/RT%20-%20Microrredes%20-%20FINAL.pdf

O projeto utiliza o valor de referência de **R$ 2,66 por Wp**, correspondente ao custo médio de instalação de sistemas fotovoltaicos de pequeno e médio porte no primeiro semestre de 2024, conforme publicação da EPE.

Esse valor é utilizado exclusivamente como referência histórica para estimar o investimento inicial.

Ele não representa um orçamento atualizado de instalação em 2026. Os preços reais podem variar de acordo com equipamentos, mão de obra, localização e características do imóvel.

### 8.3. MCTI - Fator de emissão de CO₂

**Fonte:** Ministério da Ciência, Tecnologia e Inovação (MCTI).

Link: https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene/dados-e-ferramentas/fatores-de-emissao

O projeto utiliza o fator médio anual de emissão de **0,0461 tCO₂/MWh**, referente ao Sistema Interligado Nacional (SIN) em 2025.

Para utilização nos cálculos, o valor é convertido para:

**0,0461 kgCO₂/kWh.**

Esse fator permite estimar as emissões associadas ao consumo de eletricidade e calcular emissões potencialmente evitadas nos cenários de eficiência energética e geração solar.

Trata-se de um fator médio de referência, não de uma medição específica da distribuidora ou da residência.

## 9. Metodologia e cálculos

Os cálculos são realizados utilizando as informações fornecidas pelo usuário, os dados tarifários da ANEEL e os parâmetros de referência descritos anteriormente.

### 9.1. Custo estimado de energia

O custo referente às componentes TE e TUSD é calculado por:

`Custo = Consumo mensal × Tarifa total`

Onde:

- Consumo mensal: kWh.
- Tarifa total: R$/kWh.
- Custo: R$.

O resultado não representa necessariamente o valor total da conta de energia, pois não inclui todos os componentes que podem estar presentes na fatura.

O valor total da conta informado pelo usuário é utilizado apenas como referência de exibição e não entra no cálculo do custo estimado, que considera exclusivamente TE e TUSD.

### 9.2. Economia por eficiência energética

A energia economizada é calculada por:

`Energia economizada = Consumo mensal × Percentual de redução`

O novo consumo é:

`Novo consumo = Consumo mensal − Energia economizada`

A economia financeira estimada é:

`Economia = Energia economizada × Tarifa total`

Os cenários utilizam reduções de 5%, 10% e 15%.

### 9.3. Dimensionamento do sistema solar

O dimensionamento utiliza os seguintes parâmetros:

| Parâmetro | Valor adotado |
|---|---:|
| Horas de Sol Pleno (HSP) | 5 horas/dia |
| Fator de desempenho (PR) | 0,80 |
| Dias considerados no mês | 30 dias |
| Custo de referência | R$ 2,66/Wp |

A potência estimada é calculada por:

`Potência (kWp) = Consumo mensal / (HSP × Dias do mês × PR)`

A geração mensal estimada é:

`Geração mensal = Potência × HSP × Dias do mês × PR`

A geração anual é:

`Geração anual = Geração mensal × 12`

O investimento inicial é estimado por:

`Investimento = Potência (kWp) × 1.000 × Custo por Wp`

Os parâmetros de horas de sol pleno e fator de desempenho são hipóteses gerais utilizadas para a simulação. Não representam medições específicas da localização do imóvel.

### 9.4. Retorno financeiro estimado

O retorno financeiro simplificado é calculado por:

`Retorno (meses) = Investimento inicial / Economia mensal teórica`

O cálculo considera, de forma simplificada, a compensação integral do valor de TE + TUSD sobre a energia gerada pelo sistema solar.

Essa hipótese não representa necessariamente as condições reais de compensação de energia, que podem envolver cobranças, regras tarifárias, impostos e outros componentes.

Por isso, o resultado deve ser interpretado como uma estimativa teórica, e não como uma previsão garantida de retorno.

### 9.5. Impacto ambiental

A estimativa de emissões associadas ao consumo de energia elétrica utiliza o fator médio do SIN em 2025.

A fórmula aplicada é:

`Emissões (kgCO₂) = Energia (kWh) × Fator de emissão (kgCO₂/kWh)`

Para os cenários de eficiência energética, o cálculo utiliza a quantidade de energia economizada.

Para a energia solar, utiliza a geração mensal e anual estimada, considerando que essa geração possa substituir eletricidade proveniente da rede.

Os resultados representam emissões potencialmente evitadas, não uma medição direta da redução de gases de efeito estufa.

Não são contabilizadas as emissões relacionadas à fabricação, ao transporte, à instalação, à manutenção ou ao descarte dos painéis e demais equipamentos fotovoltaicos.

## 10. Tecnologias utilizadas

- **Python:** linguagem utilizada no desenvolvimento da aplicação.
- **Requests:** biblioteca utilizada para realizar requisições à API pública da ANEEL.
- **CSV:** formato utilizado para armazenar os dados tarifários processados.
- **Decimal:** utilizado para realizar operações numéricas com valores decimais, especialmente em cálculos financeiros.
- **Git e GitHub:** utilizados para versionamento e armazenamento do projeto.

## 11. Estrutura do projeto

```text
GS_2026.02_SERS/
│
├── dados/
│   └── tarifas_residenciais_processadas.csv
│
├── processar_tarifa.py
├── citizen_assist_ai.py
├── diagnostico_energetico.py
├── consultar_tarifa.py
├── eficiencia_energetica.py
├── energia_solar.py
├── comparar_alternativas.py
│
├── testes/
│   └── test_calculos.py
│
├── requirements.txt
└── README.md
```

### Responsabilidade dos arquivos

| Arquivo | Responsabilidade |
|---|---|
| `processar_tarifa.py` | Consulta e processa os dados tarifários da ANEEL. |
| `citizen_assist_ai.py` | Implementa o chatbot Citizen Assist AI, com menu, dúvidas, coleta de dados e apresentação dos resultados. |
| `diagnostico_energetico.py` | Reúne as funções de coleta e cálculo reutilizadas pelo chatbot. |
| `consultar_tarifa.py` | Consulta as tarifas e os períodos disponíveis no CSV. |
| `eficiencia_energetica.py` | Simula os cenários de redução de consumo. |
| `energia_solar.py` | Calcula o dimensionamento e o investimento solar estimado. |
| `comparar_alternativas.py` | Compara os resultados financeiros e ambientais. |
| `testes/` | Armazena os testes automatizados dos cálculos e da consulta de tarifas. |
| `dados/` | Armazena a base tarifária processada. |
| `requirements.txt` | Lista as dependências externas do projeto. |

## 12. Instalação e execução

### Pré-requisitos

- Python instalado.
- Conexão com a internet para consultar e atualizar os dados da ANEEL.

### 12.1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 12.2. Processar os dados tarifários

```bash
python processar_tarifa.py
```

Esse procedimento consulta a base pública da ANEEL e gera o arquivo CSV utilizado pelo simulador.

### 12.3. Executar o chatbot Citizen Assist AI

```bash
python citizen_assist_ai.py
```

O chatbot apresenta sua função, exibe o menu e conduz a conversa pelo terminal. Escolha a opção 1 para realizar o diagnóstico energético, a opção 2 para tirar dúvidas, a opção 3 para consultar fontes e limitações ou a opção 4 para encerrar.

## 13. Testes realizados

Durante o desenvolvimento, foram realizados testes de execução e validação das funcionalidades principais.

Os testes contemplaram:

- Entrada e identificação da distribuidora.
- Validação do mês de referência.
- Seleção de meses disponíveis na base tarifária.
- Entrada do consumo mensal em kWh.
- Entrada do valor total da conta em reais.
- Consulta das tarifas TE e TUSD.
- Cálculo do custo estimado de energia.
- Simulação dos cenários de eficiência energética.
- Dimensionamento do sistema solar.
- Estimativa de investimento e retorno financeiro.
- Cálculo das emissões estimadas e potencialmente evitadas.
- Apresentação inicial e menu do chatbot Citizen Assist AI.
- Respostas do chatbot a dúvidas sobre consumo, eficiência, energia solar, tarifas, investimento, retorno e emissões.
- Exibição das fontes de dados e das limitações das estimativas pelo chatbot.
- Execução completa do diagnóstico pelo chatbot.
- Retorno ao menu para um novo diagnóstico e encerramento da conversa.
- Execução completa do chatbot sem erros.

### Testes automatizados

O projeto inclui testes automatizados dos cálculos de energia solar, dos cenários de eficiência energética, da consulta de tarifas e da conversão de unidades.

O chatbot Citizen Assist AI foi validado por execução manual, incluindo o diagnóstico completo, as perguntas frequentes, a exibição de fontes e limitações, a repetição do diagnóstico e o encerramento da conversa.

Para executá-los:

```bash
python -m unittest discover -s testes
```

### Exemplo de teste realizado

Foi utilizado o seguinte cenário para verificar o funcionamento da aplicação:

| Informação | Valor |
|---|---:|
| Distribuidora | EDP SP |
| Mês de referência | 12/2026 |
| Consumo mensal | 1.500 kWh |
| Valor informado da conta | R$ 3.000,00 |
| Tarifa TE | R$ 0,33224/kWh |
| Tarifa TUSD | R$ 0,46944/kWh |
| Tarifa total | R$ 0,80168/kWh |

Resultados principais:

- Custo estimado de TE + TUSD: R$ 1.202,52.
- Economia mensal no cenário de 5%: R$ 60,13.
- Economia mensal no cenário de 10%: R$ 120,25.
- Economia mensal no cenário de 15%: R$ 180,38.
- Potência solar estimada: 12,50 kWp.
- Geração solar mensal estimada: 1.500 kWh.
- Investimento solar estimado: R$ 33.250,00.
- Emissões atuais estimadas: 69,15 kg de CO₂/mês.

A execução completa foi finalizada com código de saída 0, indicando que o programa foi executado sem erros nesse teste.

Os resultados são referentes a um cenário de teste e não representam dados reais de uma residência específica.

## 14. Premissas e limitações

Para interpretar corretamente os resultados, é importante considerar as seguintes limitações:

1. **Tarifas:** o simulador utiliza os valores de TE e TUSD da base processada da ANEEL. O custo calculado não corresponde necessariamente ao valor total da fatura.
2. **Histórico tarifário:** a base processada considera tarifas vigentes no momento da consulta e não mantém automaticamente o histórico de períodos anteriores.
3. **Eficiência energética:** os percentuais de redução são cenários hipotéticos, sem garantia de economia.
4. **Energia solar:** o dimensionamento utiliza parâmetros estimados e não substitui um projeto técnico de instalação.
5. **Investimento solar:** o custo por Wp é uma referência histórica de 2024 e pode não representar os preços atuais.
6. **Retorno financeiro:** o cálculo considera uma compensação simplificada de TE + TUSD e não contempla todas as cobranças e regras aplicáveis à geração distribuída.
7. **Impacto ambiental:** o fator de emissão é uma média nacional referente a 2025, não uma medição específica da residência.
8. **Ciclo de vida dos equipamentos:** não são contabilizadas as emissões da fabricação, transporte, instalação, manutenção e descarte dos equipamentos solares.

Portanto, os resultados devem ser utilizados como estimativas para comparação e conscientização sobre alternativas energéticas, não como garantias técnicas ou financeiras.

## 15. Considerações finais

O projeto demonstra como dados públicos, programação e parâmetros de referência podem ser utilizados para apoiar decisões relacionadas ao consumo residencial de energia elétrica.

Ao comparar a situação atual com cenários de eficiência energética e geração solar fotovoltaica, o simulador apresenta diferentes possibilidades para reduzir o consumo da rede, os gastos estimados e os impactos ambientais associados à eletricidade.

A proposta busca incentivar o uso consciente de energia e ampliar o conhecimento sobre alternativas mais sustentáveis para o ambiente residencial.

O Citizen Assist AI complementa o simulador ao oferecer uma interação guiada no terminal, com explicações em linguagem simples, respostas a dúvidas frequentes e acesso às fontes e limitações das estimativas. Dessa forma, o projeto mantém os mesmos cálculos do simulador original e amplia a forma de apresentação dos resultados.

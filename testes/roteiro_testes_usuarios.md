# Demonstração e Testes Funcionais

## Objetivo

Demonstrar o funcionamento do **Citizen Assist AI** e dos cálculos do projeto por meio de cenários executáveis pela própria equipe. Não é necessário envolver pessoas externas.

## Status

Cenários executados em 16/11/2026 e registrados em `testes/registro_testes_usuarios.txt`. Os dados e resultados esperados abaixo permanecem como roteiro de reprodução.

## Preparação

1. Executar o chatbot:

   ```bash
   python citizen_assist_ai.py
   ```

2. Executar os testes automatizados:

   ```bash
   python -m unittest discover -s testes
   ```

3. Usar os dados de demonstração abaixo ou outro conjunto disponível na base tarifária.
4. Registrar o resultado efetivamente observado, sem inventar saídas.
5. Marcar **aprovado** somente se o comportamento esperado for observado.
6. Se a base tarifária não possuir o mês indicado, escolher outro mês disponível e registrar essa alteração.

## Dados de demonstração

Os dados abaixo são exemplos fictícios para demonstração, não representam uma residência real.

| Informação | Valor |
|---|---:|
| Distribuidora | EDP SP |
| Mês de referência | 12/2026 |
| Consumo mensal | 1.500 kWh |
| Valor informado da conta | R$ 3.000,00 |

Os resultados esperados foram calculados com a tarifa de demonstração de R$ 0,80168/kWh. Se a base tarifária for atualizada ou outro mês for escolhido, os valores observados podem ser diferentes e devem ser registrados como foram exibidos.

## Cenário 1 - Diagnóstico energético completo

**Objetivo:** demonstrar a coleta de dados e a apresentação do diagnóstico com distribuidora, mês, consumo e valor da conta.

**Dados de entrada:**

- Distribuidora: EDP SP.
- Mês de referência: 12/2026.
- Consumo mensal: 1.500 kWh.
- Valor da conta: R$ 3.000,00.

**Passos:**

1. Escolher a opção 1 do menu.
2. Informar os dados de entrada.
3. Observar o resumo em linguagem simples.
4. Observar a comparação detalhada.
5. Verificar as recomendações finais.

**Resultado esperado:**

- O chatbot aceita os dados e conclui o diagnóstico sem encerrar inesperadamente.
- O custo estimado de TE + TUSD é de R$ 1.202,52.
- A diferença entre a conta informada e o custo estimado é de R$ 1.797,48.
- O chatbot explica que a diferença pode incluir impostos, bandeiras e outros encargos.
- As emissões atuais são estimadas em 69,15 kg de CO₂ por mês.
- O chatbot informa que não há payback numérico e apresenta as recomendações.

**Registro:**

- Resultado efetivamente observado: tarifa de R$ 0,80168/kWh; custo de TE + TUSD de R$ 1.202,52; diferença de R$ 1.797,48; emissões de 69,15 kg de CO₂/mês; resumo, comparação e recomendações exibidos sem erro.
- Situação: (X) Aprovado ( ) Reprovado
- Observações: execução local em terminal, conforme o esperado.

## Cenário 2 - Simulação de eficiência energética

**Objetivo:** demonstrar os cenários hipotéticos de redução de consumo e a economia estimada.

**Dados de entrada:** os mesmos do Cenário 1. A simulação pode ser observada no mesmo diagnóstico.

**Passos:** executar o diagnóstico do Cenário 1 e observar a seção de eficiência energética.

**Resultado esperado:**

- Cenário de 5%: novo consumo de 1.425 kWh e economia estimada de R$ 60,13 por mês.
- Cenário de 10%: novo consumo de 1.350 kWh e economia estimada de R$ 120,25 por mês.
- Cenário de 15%: novo consumo de 1.275 kWh e economia estimada de R$ 180,38 por mês.
- O chatbot informa que os percentuais são hipóteses, não economias garantidas.
- O chatbot informa que o custo das medidas de eficiência não é estimado pelo projeto.

**Registro:**

- Resultado efetivamente observado: 5% com 1.425,00 kWh e R$ 60,13/mês; 10% com 1.350,00 kWh e R$ 120,25/mês; 15% com 1.275,00 kWh e R$ 180,38/mês; avisos de hipótese e de custo não estimado exibidos.
- Situação: (X) Aprovado ( ) Reprovado
- Observações: simulação exibida no mesmo diagnóstico do Cenário 1.

## Cenário 3 - Simulação de energia solar

**Objetivo:** demonstrar a potência estimada, a geração de energia e o investimento inicial de referência.

**Dados de entrada:** os mesmos do Cenário 1. A simulação pode ser observada no mesmo diagnóstico.

**Passos:** executar o diagnóstico do Cenário 1 e observar a seção de energia solar.

**Resultado esperado:**

- Potência estimada: 12,50 kWp.
- Geração mensal estimada: 1.500 kWh.
- Geração anual estimada: 18.000 kWh.
- Investimento inicial estimado: R$ 33.250,00.
- Economia potencial máxima teórica: R$ 1.202,52 por mês.
- Emissões potencialmente evitadas: 69,15 kg de CO₂ por mês.
- O chatbot explica que a economia não é garantida e que não há payback numérico.
- O chatbot informa que o dimensionamento não substitui um projeto técnico.

**Registro:**

- Resultado efetivamente observado: 12,50 kWp; 1.500,00 kWh/mês; 18.000,00 kWh/ano; investimento de R$ 33.250,00; economia potencial de R$ 1.202,52/mês; emissões evitadas de 69,15 kg de CO₂/mês; ressalvas sobre ausência de payback e projeto técnico exibidas.
- Situação: (X) Aprovado ( ) Reprovado
- Observações: simulação exibida no mesmo diagnóstico do Cenário 1.

## Cenário 4 - Interação com o chatbot e entradas inválidas

**Objetivo:** demonstrar as respostas a dúvidas, a consulta de fontes e o tratamento de erros de entrada.

**Dúvidas sugeridas:**

- Como posso economizar energia?
- Como funciona a energia solar?
- Qual a melhor alternativa?

**Entradas inválidas sugeridas:**

- Consumo: `abc`.
- Consumo: `-10`.
- Consumo: `1.50.00`.
- Valor da conta: `abc`.

Depois das entradas inválidas, informar valores válidos, como consumo `1500` e conta `3000`.

**Passos:**

1. Escolher a opção 2 e fazer as três perguntas sugeridas.
2. Digitar `voltar` para retornar ao menu.
3. Escolher a opção 3 e observar as fontes e limitações.
4. Escolher a opção 1 e testar as entradas inválidas.
5. Informar valores válidos e concluir o diagnóstico para verificar a recuperação.

**Resultado esperado:**

- As dúvidas recebem respostas relacionadas ao tema perguntado.
- A opção 3 apresenta fontes e limitações das estimativas.
- As entradas inválidas recebem mensagem clara e o chatbot solicita novamente o valor.
- O chatbot não trava e permite corrigir os dados.
- O diagnóstico é concluído após a correção.

**Registro:**

- Resultado efetivamente observado: as três dúvidas receberam respostas adequadas; a opção 3 exibiu fontes e limitações; as entradas `abc`, `-10`, `1.50.00` e `abc` receberam mensagem de valor inválido e nova solicitação; após `1500` e `3000`, o diagnóstico foi concluído; o chatbot não travou.
- Situação: (X) Aprovado ( ) Reprovado
- Observações: recuperação após entradas inválidas confirmada.

## Critérios de aprovação

Cada cenário deve ser considerado aprovado quando:

- os passos puderem ser executados sem erro imprevisto;
- as saídas principais forem exibidas;
- as limitações e ressalvas estiverem presentes;
- o comportamento observado corresponder ao resultado esperado, ou a diferença estiver explicada nas observações.

Caso o cenário seja reprovado, registrar o que ocorreu, a mensagem exibida e a correção necessária.

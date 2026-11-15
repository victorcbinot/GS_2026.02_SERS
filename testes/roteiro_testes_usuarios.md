# Roteiro de testes com usuários

## Objetivo

Avaliar se o chatbot **Citizen Assist AI** é compreensível, útil e seguro para consumidores residenciais, sem induzir conclusões financeiras indevidas.

## Status

Testes ainda não realizados. O registro deve ser preenchido apenas com observações reais, em `testes/registro_testes_usuarios.txt`. Não inventar participantes, opiniões ou resultados.

## Participantes sugeridos

- De 3 a 5 pessoas adultas, preferencialmente responsáveis pelo pagamento da conta de energia.
- Não é necessário conhecimento técnico em energia.
- Usar identificação anônima, como `P01`, `P02` etc.
- Solicitar consentimento para registrar observações.
- Evitar expor dados pessoais ou valores reais da conta em locais públicos.

## Preparação

1. Executar o chatbot:

   ```bash
   python citizen_assist_ai.py
   ```

2. Entregar ao participante apenas a instrução do cenário.
3. Observar sem interferir. Ajudar somente se o participante ficar bloqueado.
4. Anotar dúvidas, dificuldades e sugestões no arquivo de registro.
5. Não corrigir a opinião do participante durante o teste.

## Cenário 1 - Diagnóstico completo

**Instrução ao participante:**

> Use o chatbot para fazer um diagnóstico com os dados de uma conta de energia. Escolha uma distribuidora e um mês disponíveis e informe um consumo e um valor de conta. Depois, explique o que o assistente mostrou.

**Dados sugeridos para o teste:**

- Distribuidora: EDP SP ou outra disponível.
- Mês: um mês disponível na base.
- Consumo: 1.500 kWh.
- Valor da conta: R$ 3.000,00.

**Observar:**

- O participante encontrou a opção de diagnóstico?
- Conseguiu informar distribuidora, mês, consumo e valor?
- Entendeu a diferença entre a conta informada e a estimativa de TE + TUSD?
- Entendeu que a economia de eficiência é hipotética?
- Entendeu o investimento solar e a economia potencial máxima teórica?
- Encontrou as recomendações ao final?
- Ficou claro que não há payback numérico nem garantia de retorno?
- O texto foi longo demais, confuso ou adequado?

## Cenário 2 - Dúvidas, fontes e limitações

**Instrução ao participante:**

> Faça três perguntas ao chatbot sobre economia de energia e energia solar. Depois, use a opção de fontes e limitações e diga se as informações ficaram claras.

**Perguntas sugeridas:**

- Como posso economizar energia?
- Vale a pena instalar energia solar?
- De onde vêm os dados usados pelo assistente?

**Observar:**

- As respostas foram compreensíveis?
- O participante percebeu que as estimativas têm limitações?
- A explicação sobre ausência de payback ficou clara?
- O participante encontrou as fontes e as limitações?
- Alguma resposta pareceu uma garantia de economia?

## Cenário 3 - Entrada inválida e recuperação

**Instrução ao participante:**

> Tente usar o diagnóstico com algumas informações incorretas e observe como o chatbot responde. Depois, tente corrigir e concluir o diagnóstico.

**Entradas sugeridas:**

- Consumo: `abc`.
- Consumo: vazio.
- Consumo: `-10`.
- Consumo: `1.50.00`.
- Valor da conta: `0` ou texto.

**Observar:**

- O chatbot explicou o erro de forma clara?
- O participante conseguiu tentar novamente?
- O programa travou ou encerrou inesperadamente?
- A mensagem ajudou o participante a corrigir a entrada?
- O diagnóstico foi concluído após a correção?

## Critérios de avaliação

Registrar, para cada cenário:

- Tarefa concluída: sim, não ou parcial.
- Tempo aproximado.
- Principais dificuldades.
- Trechos ou telas que geraram confusão.
- Se as recomendações foram compreendidas.
- Se o participante percebeu as limitações.
- Sugestões de melhoria.
- Ajustes que podem ser feitos no chatbot ou no README.

## Resultado esperado

Ao final, os registros devem permitir identificar:

- pontos de melhoria na linguagem do chatbot;
- tarefas que exigem instruções adicionais;
- mensagens de erro que precisam ser mais claras;
- dúvidas recorrentes sobre custos, economia, payback e emissões;
- necessidade de ajustes no roteiro de apresentação.

## Pendências

- Realizar os testes com participantes reais.
- Preencher o arquivo `testes/registro_testes_usuarios.txt`.
- Revisar o chatbot e o README com base nos resultados.
- Inserir o link do vídeo de apresentação no README.

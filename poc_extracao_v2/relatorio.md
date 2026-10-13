# Resumo (13 conversas)
- Cobertura de perguntas: 100% (15/15)
- Precisão de perguntas: 94% (16/17)
- Status correto nas perguntas achadas: 87% (13/15)
- Cobertura de promessas: 92% (11/12)
- Precisão de promessas: 100% (11/11)
- 'cumprida' correto nas promessas achadas: 100% (11/11)
- bola_com correto: 77% (10/13)
- razao_do_cliente correto: 92% (12/13)
- falha_principal_subtipo correto: 100% (13/13)
- perda_evitavel correto: 92% (12/13)

# Relatório de avaliação

## Conversa 1
  - status divergente em 'Tem algum caso parecido?': modelo=nao_respondida | gabarito=respondida_generica_ou_parcial
- Perguntas: 2 no gabarito, 2 extraídas; extras (revisar se são invenção): nenhuma
- Promessas: 1 no gabarito, 1 extraídas; extras (revisar): nenhuma
- bola_com: modelo=vendedor | gabarito=ninguem DIVERGE
- razao_do_cliente: modelo=preco_budget | gabarito=preco_budget OK
- falha_principal_subtipo: modelo=valor_roi_nao_demonstrado | gabarito=valor_roi_nao_demonstrado OK
- perda_evitavel: modelo=sim | gabarito=sim OK
- Código: categoria da falha=Descoberta e valor | alertas=['perdido_no_crm_com_pendencia_do_vendedor', 'perdido_no_crm_mas_recuperavel', 'motivo_registrado_diverge_do_diagnostico'] | confiança=media

## Conversa 2
- Perguntas: 2 no gabarito, 2 extraídas; extras (revisar se são invenção): nenhuma
- Promessas: 1 no gabarito, 1 extraídas; extras (revisar): nenhuma
- bola_com: modelo=vendedor | gabarito=ninguem DIVERGE
- razao_do_cliente: modelo=condicao_comercial_pacote_contrato | gabarito=condicao_comercial_pacote_contrato OK
- falha_principal_subtipo: modelo=oferta_inflexivel_preco_pacote | gabarito=oferta_inflexivel_preco_pacote OK
- perda_evitavel: modelo=incerto | gabarito=incerto OK
- Código: categoria da falha=Oferta e política | alertas=['perdido_no_crm_com_pendencia_do_vendedor', 'motivo_registrado_diverge_do_diagnostico'] | confiança=media

## Conversa 3
- Perguntas: 2 no gabarito, 2 extraídas; extras (revisar se são invenção): nenhuma
- Promessas: 1 no gabarito, 1 extraídas; extras (revisar): nenhuma
- bola_com: modelo=vendedor | gabarito=vendedor OK
- razao_do_cliente: modelo=sem_razao_declarada | gabarito=sem_razao_declarada OK
- falha_principal_subtipo: modelo=pendencia_do_vendedor | gabarito=pendencia_do_vendedor OK
- perda_evitavel: modelo=sim | gabarito=sim OK
- Código: categoria da falha=Retomada e follow-up | alertas=['perdido_no_crm_com_pendencia_do_vendedor', 'perdido_no_crm_mas_recuperavel', 'motivo_registrado_diverge_do_diagnostico'] | confiança=alta

## Conversa 4
- Perguntas: 0 no gabarito, 0 extraídas; extras (revisar se são invenção): nenhuma
- Promessas: 1 no gabarito, 1 extraídas; extras (revisar): nenhuma
- bola_com: modelo=vendedor | gabarito=vendedor OK
- razao_do_cliente: modelo=concorrencia_ia_gratis_ou_propria | gabarito=concorrencia_ia_gratis_ou_propria OK
- falha_principal_subtipo: modelo=abandono_sem_retomada | gabarito=abandono_sem_retomada OK
- perda_evitavel: modelo=incerto | gabarito=incerto OK
- Código: categoria da falha=Retomada e follow-up | alertas=['perdido_no_crm_com_pendencia_do_vendedor', 'perdido_no_crm_mas_recuperavel', 'motivo_registrado_diverge_do_diagnostico'] | confiança=media

## Conversa 5
- Perguntas: 2 no gabarito, 3 extraídas; extras (revisar se são invenção): nenhuma
- Promessas: 1 no gabarito, 1 extraídas; extras (revisar): nenhuma
- bola_com: modelo=vendedor | gabarito=vendedor OK
- razao_do_cliente: modelo=sem_razao_declarada | gabarito=sem_razao_declarada OK
- falha_principal_subtipo: modelo=pendencia_do_vendedor | gabarito=pendencia_do_vendedor OK
- perda_evitavel: modelo=sim | gabarito=sim OK
- Código: categoria da falha=Retomada e follow-up | alertas=['perdido_no_crm_com_pendencia_do_vendedor', 'perdido_no_crm_mas_recuperavel', 'motivo_registrado_diverge_do_diagnostico'] | confiança=alta

## Conversa 6
- Perguntas: 1 no gabarito, 1 extraídas; extras (revisar se são invenção): nenhuma
- Promessas: 1 no gabarito, 1 extraídas; extras (revisar): nenhuma
- bola_com: modelo=vendedor | gabarito=vendedor OK
- razao_do_cliente: modelo=momento_timing | gabarito=momento_timing OK
- falha_principal_subtipo: modelo=abandono_sem_retomada | gabarito=abandono_sem_retomada OK
- perda_evitavel: modelo=sim | gabarito=sim OK
- Código: categoria da falha=Retomada e follow-up | alertas=['perdido_no_crm_com_pendencia_do_vendedor', 'perdido_no_crm_mas_recuperavel', 'motivo_registrado_diverge_do_diagnostico'] | confiança=alta

## Conversa 7
- Perguntas: 1 no gabarito, 1 extraídas; extras (revisar se são invenção): nenhuma
- Promessas: 0 no gabarito, 0 extraídas; extras (revisar): nenhuma
- bola_com: modelo=vendedor | gabarito=vendedor OK
- razao_do_cliente: modelo=sem_razao_declarada | gabarito=sem_interesse_ou_lead_frio DIVERGE
- falha_principal_subtipo: modelo=lead_mal_qualificado_origem | gabarito=lead_mal_qualificado_origem OK
- perda_evitavel: modelo=incerto | gabarito=incerto OK
- Código: categoria da falha=Qualificação do lead | alertas=['perdido_no_crm_com_pendencia_do_vendedor', 'motivo_registrado_diverge_do_diagnostico'] | confiança=baixa

## Conversa 8
- Perguntas: 1 no gabarito, 1 extraídas; extras (revisar se são invenção): nenhuma
- Promessas: 0 no gabarito, 0 extraídas; extras (revisar): nenhuma
- bola_com: modelo=vendedor | gabarito=vendedor OK
- razao_do_cliente: modelo=concorrencia_ia_gratis_ou_propria | gabarito=concorrencia_ia_gratis_ou_propria OK
- falha_principal_subtipo: modelo=objecao_tratada_de_forma_generica | gabarito=objecao_tratada_de_forma_generica OK
- perda_evitavel: modelo=incerto | gabarito=incerto OK
- Código: categoria da falha=Descoberta e valor | alertas=['perdido_no_crm_com_pendencia_do_vendedor', 'perdido_no_crm_mas_recuperavel', 'motivo_registrado_diverge_do_diagnostico'] | confiança=media

## Conversa 9
- Perguntas: 0 no gabarito, 0 extraídas; extras (revisar se são invenção): nenhuma
- Promessas: 0 no gabarito, 0 extraídas; extras (revisar): nenhuma
- bola_com: modelo=ninguem | gabarito=ninguem OK
- razao_do_cliente: modelo=fora_do_icp_sem_dor | gabarito=fora_do_icp_sem_dor OK
- falha_principal_subtipo: modelo=desconto_antes_de_valor | gabarito=desconto_antes_de_valor OK
- perda_evitavel: modelo=nao | gabarito=nao OK
- Código: categoria da falha=Descoberta e valor | alertas=['motivo_registrado_diverge_do_diagnostico'] | confiança=alta

## Conversa 10
- Perguntas: 0 no gabarito, 0 extraídas; extras (revisar se são invenção): nenhuma
- Promessas: 0 no gabarito, 0 extraídas; extras (revisar): nenhuma
- bola_com: modelo=vendedor | gabarito=vendedor OK
- razao_do_cliente: modelo=sem_razao_declarada | gabarito=sem_razao_declarada OK
- falha_principal_subtipo: modelo=decisor_nao_envolvido | gabarito=decisor_nao_envolvido OK
- perda_evitavel: modelo=incerto | gabarito=incerto OK
- Código: categoria da falha=Envolvimento do decisor | alertas=['perdido_no_crm_com_pendencia_do_vendedor', 'motivo_registrado_diverge_do_diagnostico'] | confiança=baixa

## Conversa 11
  - status divergente em 'Pode mandar contrato com início em dezembro para garantir o valor? (respondido com um não)': modelo=respondida_generica_ou_parcial | gabarito=respondida
- Perguntas: 2 no gabarito, 2 extraídas; extras (revisar se são invenção): nenhuma
- Promessas: 2 no gabarito, 2 extraídas; extras (revisar): nenhuma
- bola_com: modelo=vendedor | gabarito=vendedor OK
- razao_do_cliente: modelo=condicao_comercial_pacote_contrato | gabarito=condicao_comercial_pacote_contrato OK
- falha_principal_subtipo: modelo=oferta_inflexivel_preco_pacote | gabarito=oferta_inflexivel_preco_pacote OK
- perda_evitavel: modelo=incerto | gabarito=sim DIVERGE
- Código: categoria da falha=Oferta e política | alertas=['perdido_no_crm_com_pendencia_do_vendedor', 'perdido_no_crm_mas_recuperavel', 'motivo_registrado_diverge_do_diagnostico'] | confiança=media

## Conversa 12
- Perguntas: 2 no gabarito, 2 extraídas; extras (revisar se são invenção): nenhuma
  - PROMESSA OMITIDA: Enviar contrato (enviado 03/09)
- Promessas: 3 no gabarito, 2 extraídas; extras (revisar): nenhuma
- bola_com: modelo=ninguem | gabarito=vendedor DIVERGE
- razao_do_cliente: modelo=ganho | gabarito=ganho OK
- falha_principal_subtipo: modelo=nenhuma | gabarito=nenhuma OK
- perda_evitavel: modelo=nao_se_aplica | gabarito=nao_se_aplica OK
- Código: categoria da falha=Sem falha identificada | alertas=[] | confiança=alta

## Conversa 13
- Perguntas: 0 no gabarito, 1 extraídas; extras (revisar se são invenção): ['Pediram proposta e disseram que decidiriam em até 10 dias (registro da visita)']
- Promessas: 1 no gabarito, 1 extraídas; extras (revisar): nenhuma
- bola_com: modelo=cliente | gabarito=cliente OK
- razao_do_cliente: modelo=sem_razao_declarada | gabarito=sem_razao_declarada OK
- falha_principal_subtipo: modelo=followup_sem_valor_novo | gabarito=followup_sem_valor_novo OK
- perda_evitavel: modelo=incerto | gabarito=incerto OK
- Código: categoria da falha=Retomada e follow-up | alertas=['motivo_registrado_diverge_do_diagnostico'] | confiança=baixa

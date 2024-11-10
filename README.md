# Atualização de Tag Schedule em Clusters RDS com AWS Lambda

Este projeto implementa uma função Lambda que atualiza a tag `Schedule` para clusters RDS específicos em uma conta da AWS. Ele assume uma role cross-account para acessar e modificar as tags dos clusters na conta alvo.

## Pré-requisitos

1. **Conta AWS** com permissões para criar e executar funções Lambda.
2. **Role Cross-Account** configurada na conta alvo para que a Lambda na conta principal possa acessar os clusters RDS.
3. **AWS CLI** configurado localmente (opcional para testes locais).
4. **Variáveis de Ambiente no Lambda**:
   - `ACCOUNT_ID`: ID da conta AWS de destino.
   - `REGION`: Região onde os clusters RDS estão localizados.
   - `RDS_CLUSTERS`: Lista dos IDs dos clusters RDS, separados por vírgula.
   - `DESIRED_TAG_VALUE`: Valor desejado para a tag `Schedule`.

## Estrutura do Projeto

O código Python realiza as seguintes operações:

1. Recupera variáveis de ambiente para definir `account_id`, `region`, `list_clusters_rds`, e `desired_tag_value`.
2. Assume uma role cross-account usando o `sts:AssumeRole`, permitindo acesso aos clusters na conta secundária.
3. Itera sobre cada cluster RDS, verificando e atualizando a tag `Schedule` para o valor especificado, se ela já existir.

## Como Configurar e Executar

1. ### Configuração da Role Cross-Account na Conta Alvo
   No **AWS IAM** da conta alvo, crie uma role que permite listar e modificar tags em clusters RDS:
   
   - **Trust Policy** para permitir o acesso da conta Lambda:
     ```json
     {
       "Version": "2012-10-17",
       "Statement": [
         {
           "Effect": "Allow",
           "Principal": {
             "AWS": "arn:aws:iam::<ID_CONTA_LAMBDA>:root"
           },
           "Action": "sts:AssumeRole"
         }
       ]
     }
     ```
   - **Policy** para listar e modificar tags em clusters RDS:
     ```json
     {
       "Version": "2012-10-17",
       "Statement": [
         {
           "Effect": "Allow",
           "Action": [
             "rds:AddTagsToResource",
             "rds:ListTagsForResource"
           ],
           "Resource": "arn:aws:rds:<region>:<account_id>:db:*"
         }
       ]
     }
     ```

2. ### Configuração da Função Lambda
   - Crie uma função Lambda na **conta principal** e anexe uma policy que permita ao Lambda assumir a role da conta alvo.
   - Defina as **variáveis de ambiente** mencionadas acima na configuração da função Lambda.

3. ### Executando o Script
   A função Lambda executa o código automaticamente quando acionada. Ela assume a role cross-account e atualiza a tag `Schedule` de cada cluster na lista `RDS_CLUSTERS` para o valor definido em `DESIRED_TAG_VALUE`.

## Como Contribuir
1. Fork o Repositório e clone o projeto.
2. Crie uma branch para sua contribuição (git checkout -b feature/minha-feature).
3. Implemente e teste suas mudanças.
4. Faça commit e push para a branch criada.
5. Abra um Pull Request detalhando as alterações.
6. Contribuições são bem-vindas para melhorias, como:

## Futuras features
- [ ] Suporte a novos tipos de tags ou serviços AWS.
- [ ] Melhorias na gestão de erros.
- [ ] Otimizações para reduzir custos de execução.

### Licença

Este projeto é distribuído sob a Licença MIT.

Esse README fornece uma visão geral, instruções de configuração, execução, estrutura do código e informações sobre como contribuir com o projeto.

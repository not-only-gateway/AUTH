# Referência do sistema

Este sistema tem foco a autenticação e controle de perfis pessoais e de acesso dos usuários pertencentes/cadastrados em
um servidor AD/LDAP.
___

### Modelos:

#### Session:
A Tabela sessão armazena dados do último login feito. Esses dados são utilizados para identificar e validar o token JWT. 

#### Endpoint:
Tabela que representa endpoint que será integrado com o servido. Um endpoint representa um caminho único para todos os métodos HTTP (GET, POST, PUT...)
devido a isso o Endpoint irá armazenar como chave primária uma string RegEx contendo o padrão para o endpoint em questão (Isso é necessário pois alguns frameworks como flask suportam parâmetros em suas urls e o RegEx) 

#### Access:
Relação m-m que indica quais privilégios são necessários para autorização ao uso do endpoint.


#### AccessPrivilege:
Relação m-m que indica quais privilégios estão vinculados ao usuário.


#### User:
Tabela do usurário, a inserção de dados só ocorre de forma automática no primeiro login do usuário.
Pode ser customizada com novos dados para melhor representar o usuário.

#### ActiveDirectory:
Tabela referente aos dados do servidor AD/LDAP. Contém informações de conexão e alguns metadados para identificação do servidor

___

### Endpoints:


#### active_directory:
- Métodos suportados (padrão API):
  - GET (Requer parâmetro na URL do ID)
  - POST
  - DELETE (Requer parâmetro na URL do ID)
  - PUT (Requer parâmetro na URL do ID)
- Suporte a listagem (padrão API):
  - SIM (/list/ - GET)

#### authentication:
- Métodos suportados:
  - GET - Utilizado pelos serviços externos para validar usuário.
  - POST - Utilizado para efetuar login
#### privilege:
- Métodos suportados (padrão API):
  - GET (Requer parâmetro na URL do ID)
  - POST
  - DELETE (Requer parâmetro na URL do ID)
  - PUT (Requer parâmetro na URL do ID)
- Suporte a listagem (padrão API):
  - SIM (/list/ - GET)

#### endpoint:
- Métodos suportados (padrão API):
  - GET (Requer parâmetro na URL do ID)
  - POST
  - DELETE (Requer parâmetro na URL do ID)
  - PUT (Requer parâmetro na URL do ID)
- Suporte a listagem (padrão API):
  - SIM (/list/ - GET)
  
#### access_profile:
- Métodos suportados (padrão API):
  - GET (Requer parâmetro na URL do ID)
  - POST
  - DELETE (Requer parâmetro na URL do ID)
  - PUT (Requer parâmetro na URL do ID)
- Suporte a listagem (padrão API):
  - SIM (/list/ - GET)

#### access_privilege
- Métodos suportados (padrão API):
  - POST
  - DELETE (Requer parâmetro na URL do peril de acesso e do privilégio \[ex: "/api/access_privilege/1/1"])
- Suporte a listagem (padrão API):
  - SIM (/list/ - GET)


___

### OBS:

#### Setup inicial e `env.py`:

É necessário o arquivo `env.py` configurado antes da primeira inicialização. Os dados presentes no arquivo serão
utilizados para o cadastro do primeiro servidor AD/LDAP no serviço. Esse primeiro servidor cadastrado é necessário
para o primeiro login ser efetuado e com disso fazer a manutenção dos dados necessários.

O arquivo `env.py` também é necessário para conexão com o banco de dados e para geração dos tokens jwt.

Abaixo é possível ver um exemplo do formato esperado no arquivo:

```python
AUTHORIZATION_TOKEN = "Token para criptografia/descriptografia dos JWTs"
DENOMINATION = "Nome do servidor"
DESCRIPTION = "Descrição do servidor"
SERVER = "URL SERVIDOR AD/LDAP"
BASE = 'Base AD'
FILTER = "Filtro AD"

ATTRS = "attr1, attr2, attr3"
# mapa de atributos {keyAD: keyUsuário}
MAP_ATTR = {}
DATABASE = "banco_sql_suportado_pelo_flask"
USER = "user"
PASSWORD = "senha"
HOST_NAME = "192.168.0.0"
DATABASE_NAME = "nome_banco"
```

#### Primeiro cadastro:

No momento do primeiro login será criado um perfil simples com os dados do usuário consumidos do servidor AD/LDAP em
questão. Para autenticação com o servidor AD/LDAP os dados deste perfil não precisam ser mantidos os mesmos.

#### Dependências:

- Este pacote faz uso do módulo para [APIs](https://github.com/not-only-gateway/API).
- Configuração da extensão [python-ldap](https://www.python-ldap.org/en/python-ldap-3.4.0/) é necessária.



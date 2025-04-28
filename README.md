# Rota Cultural - Backend

Sistema de gerenciamento de pontos culturais com autenticação Firebase.

## Configuração do Ambiente

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/rota_cultural_backend.git
cd rota_cultural_backend
```

2. Crie um ambiente virtual e ative-o:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
   - Copie o arquivo `.env.example` para `.env`
   - Preencha as variáveis com suas credenciais do Firebase

5. Configure o Firebase:
   - Crie um projeto no [Firebase Console](https://console.firebase.google.com/)
   - Habilite a autenticação por email/senha
   - Baixe o arquivo de credenciais do Admin SDK e salve como `firebase/serviceAccountKey.json`

## Executando o Projeto

1. Inicie o servidor:
```bash
streamlit run pages/0_login.py
```

2. Acesse o sistema no navegador:
```
http://localhost:8501
```

## Credenciais Padrão

- Email: admin@rotacultural.com
- Senha: admin123

## Estrutura do Projeto

```
rota_cultural_backend/
├── firebase/
│   ├── firebase_config.py
│   └── firebase_client.py
├── pages/
│   ├── 0_login.py
│   ├── 1_cadastrar_ponto.py
│   └── 2_listar_pontos.py
├── services/
│   ├── auth_service.py
│   └── ponto_service.py
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

## Segurança

- Todas as credenciais sensíveis devem ser mantidas no arquivo `.env`
- O arquivo `.env` está listado no `.gitignore` e não deve ser commitado
- As credenciais do Firebase devem ser mantidas seguras e não compartilhadas

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

# Guia de Contribuição

Obrigado por considerar contribuir com o Port Monitor! Este documento explica como participar do projeto.

---

## Como contribuir

### Reportar um bug

1. Verifique se o bug já foi reportado nas [Issues](https://github.com/SEU_USUARIO/port-monitor/issues)
2. Se não encontrou, abra uma nova issue usando o template **Bug Report**
3. Inclua: sistema operacional, versão do Python, passos para reproduzir e mensagem de erro

### Sugerir uma funcionalidade

1. Abra uma issue usando o template **Feature Request**
2. Descreva o problema que a funcionalidade resolveria
3. Explique como você imagina que funcionaria

### Enviar código (Pull Request)

1. Faça um **fork** do repositório
2. Crie uma branch com nome descritivo:
   ```bash
   git checkout -b feature/exportar-csv
   # ou
   git checkout -b fix/filtro-porta-udp
   ```
3. Faça suas alterações
4. Teste localmente antes de enviar
5. Abra um Pull Request descrevendo o que foi alterado e por quê

---

## Configuração do ambiente

```bash
git clone https://github.com/SEU_USUARIO/port-monitor.git
cd port-monitor
pip install psutil
python port_monitor.py
```

Não há dependências de desenvolvimento além do `psutil`.

---

## Padrões do projeto

- **Linguagem:** Python 3.10+
- **Interface:** Tkinter (sem bibliotecas externas de UI)
- **Estilo:** Siga o PEP 8. Nomes de variáveis e comentários podem ser em português ou inglês.
- **Commits:** Use mensagens claras no imperativo: `Adiciona filtro por protocolo`, `Corrige crash ao encerrar processo do sistema`

---

## Dúvidas?

Abra uma issue com a tag `question` — respondo assim que possível.

<div align="center">

<h1>⬡ Port Monitor</h1>

<p>Interface gráfica para monitorar e encerrar processos por porta — sem abrir terminal.</p>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/Licen%C3%A7a-MIT-22c55e?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/Plataforma-Windows-0078D4?style=flat-square&logo=windows&logoColor=white)](https://github.com)
[![Stars](https://img.shields.io/github/stars/Gabrielferreira1/Port_Monitor?style=flat-square&color=f59e0b)](https://github.com/Gabrielferreira1/Port_Monitor/stargazers)
[![Issues](https://img.shields.io/github/issues/Gabrielferreira1/Port_Monitor?style=flat-square&color=ef4444)](https://github.com/Gabrielferreira1/Port_Monitor/issues)

<br/>

![Port Monitor Demo](docs/demo.gif)

</div>

---

## O problema

Você tenta iniciar seu servidor e aparece:

```
Error: listen EADDRINUSE: address already in use :::3000
```

Aí começa a busca: abre o terminal, digita `netstat -ano`, filtra manualmente, pega o PID, roda `taskkill`... **3 minutos de trabalho repetitivo toda vez.**

**Port Monitor resolve isso em 1 clique.**

---

## Funcionalidades

- **Monitoramento em tempo real** de todas as portas TCP/UDP ativas
- **Auto-refresh a cada 5 segundos** (toggle para ligar/desligar)
- **Filtro instantâneo** por porta, processo, PID, caminho ou status
- **Encerramento de processos** com um clique  suporta seleção múltipla
- **Informações completas**: porta, protocolo, status, PID, nome e caminho do executável
- **Ordenação** por qualquer coluna
- **Zero dependências** na versão `.exe` — só baixar e executar

---

## Instalação

### Opção 1 — Executável (recomendado)

1. Vá em [**Releases**](https://github.com/Gabrielferreira1/Port_Monitor.git)
2. Baixe o `PortMonitor.exe`
3. Execute como **Administrador** para ver todos os processos

> **Nota:** Alguns antivírus podem alertar sobre executáveis gerados com PyInstaller. Isso é um falso positivo. O código-fonte está disponível para inspeção.

### Opção 2 — Rodar com Python

```bash
# Clone o repositório
git clone https://github.com/SEU_USUARIO/port-monitor.git
cd port-monitor

# Instale as dependências
pip install psutil

# Execute
python port_monitor.py
```

---

## Como usar

| Ação | Como fazer |
|------|-----------|
| Ver todos os processos | Abra o app (como Administrador) |
| Filtrar | Digite na caixa de busca — filtra em tempo real |
| Encerrar um processo | Clique na linha → botão **Finalizar** |
| Encerrar vários | `Shift+clique` para selecionar múltiplos → **Finalizar** |
| Ordenar | Clique no cabeçalho de qualquer coluna |
| Pausar atualização | Desmarque "Auto-refresh" |

---

## Compilar o .exe você mesmo

```bash
pip install pyinstaller psutil
pyinstaller --onefile --windowed --name "PortMonitor" port_monitor.py
```

O executável ficará em `dist/PortMonitor.exe`.

---

## Tecnologias

- **Python 3.10+**
- **Tkinter** — interface gráfica nativa
- **psutil** — leitura de processos e conexões do sistema
- **PyInstaller** — empacotamento em `.exe`

---

## Contribuindo

Contribuições são bem-vindas! Veja o [**guia de contribuição**](CONTRIBUTING.md) para começar.

Algumas ideias para quem quiser contribuir:

- [ ] Suporte a macOS e Linux
- [ ] Filtro por protocolo (TCP / UDP)
- [ ] Exportar lista para CSV
- [ ] Notificação quando uma nova porta é aberta
- [ ] Histórico de processos encerrados
- [ ] Tema claro/escuro

---

## Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE) para mais informações.

---

<div align="center">

Se este projeto te ajudou, considere deixar uma ⭐  isso ajuda outras pessoas a encontrarem.

</div>

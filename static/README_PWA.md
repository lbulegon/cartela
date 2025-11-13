# PWA - Progressive Web App

Este diretório contém todos os arquivos necessários para o PWA do Cartela.bet.

## Arquivos

- `manifest.json` - Manifesto do PWA com informações do app
- `sw.js` - Service Worker para cache offline
- `pwa-install.js` - Script para instalação do PWA
- `icons/` - Ícones do aplicativo em vários tamanhos
- `generate_icons.py` - Script para gerar ícones automaticamente

## Como usar

### Gerar ícones

Se precisar regenerar os ícones:

```bash
pip install Pillow
python static/generate_icons.py
```

### Instalação

1. Acesse o site no navegador (Chrome, Edge, Safari)
2. O navegador mostrará automaticamente um prompt para instalar
3. Ou clique no botão "📱 Instalar App" que aparece no canto inferior direito

### Funcionalidades

- ✅ Instalação como app nativo
- ✅ Funciona offline (com cache)
- ✅ Ícone na tela inicial
- ✅ Tema personalizado
- ✅ Suporte para iOS e Android

## Testando

1. Abra o DevTools (F12)
2. Vá para a aba "Application" (Chrome) ou "Application" (Firefox)
3. Verifique:
   - Service Worker está registrado
   - Manifest está carregado
   - Cache está funcionando

## Notas

- O Service Worker usa estratégia "Network First" com fallback para cache
- Os ícones são gerados automaticamente com o logo da Cartela
- O tema usa as cores do logotipo (#FFD700 e #1a1a1a)


# Instruções para Desenvolvimento Unity no Cursor

## 📚 Visão Geral

Este documento contém instruções sobre como usar o Cursor para desenvolver jogos com Unity.

## 🎮 O que é Unity?

Unity é uma engine de jogos multiplataforma amplamente usada para desenvolvimento de jogos 2D e 3D, com suporte para:
- **Desktop**: Windows, macOS, Linux
- **Mobile**: iOS, Android
- **Consoles**: PlayStation, Xbox, Nintendo Switch
- **Web**: WebGL
- **VR/AR**: Oculus, HTC Vive, ARCore, ARKit

### Características Principais
- Editor visual com drag-and-drop
- Sistema de física integrado
- Sistema de animação (Animator)
- Sistema de partículas
- Sistema de áudio
- Asset Store (biblioteca de assets prontos)
- Networking (Unity Netcode, Mirror, etc.)
- UI System (uGUI)

## 💻 Desenvolvimento Unity no Cursor

### ✅ O que funciona bem no Cursor

1. **Edição de Scripts C#**
   - O Cursor é excelente para escrever scripts Unity em C#
   - IntelliSense e autocomplete funcionam perfeitamente
   - Suporte completo para referências do Unity

2. **IntelliSense e Autocomplete**
   - Suporte completo para C# e APIs do Unity
   - Autocomplete inteligente para classes Unity
   - Navegação de código (Go to Definition)

3. **Debugging**
   - Pode depurar scripts Unity (com configuração adequada)
   - Breakpoints e inspeção de variáveis

4. **Versionamento**
   - Git integrado para controle de versão
   - Diferenças de arquivo visíveis

5. **IA Assistente**
   - Ajuda com código Unity
   - Geração de scripts
   - Resolução de problemas

### ⚠️ O que você ainda precisa

1. **Unity Editor**
   - Precisa instalar o Unity Hub e Unity Editor separadamente
   - O Unity Editor não roda dentro do Cursor
   - É necessário para visualizar cenas, testar jogos e fazer builds

2. **Fluxo de Trabalho**
   - Edite scripts no Cursor
   - Teste e visualize no Unity Editor
   - Ambos trabalham juntos

## 🚀 Configuração Recomendada

### Passo 1: Instalar Unity

1. Baixe o **Unity Hub** em: https://unity.com/download
2. Instale o Unity Hub
3. No Unity Hub, instale uma versão LTS (Long Term Support) do Unity Editor
   - Recomendado: Unity 2022.3 LTS ou mais recente
   - Versões LTS são mais estáveis para projetos de longo prazo

### Passo 2: Configurar Cursor como Editor Externo

1. Abra o Unity Editor
2. Vá em: **Edit → Preferences → External Tools**
3. Em **External Script Editor**, clique em **Browse**
4. Navegue até o executável do Cursor
   - Windows: Geralmente em `C:\Users\[SeuUsuario]\AppData\Local\Programs\cursor\Cursor.exe`
   - Ou encontre o Cursor no menu Iniciar, clique com botão direito → "Abrir localização do arquivo"
5. Selecione o executável do Cursor
6. Feche e reabra o Unity Editor

### Passo 3: Criar um Projeto Unity

1. Abra o Unity Hub
2. Clique em **New Project**
3. Escolha um template:
   - **2D**: Para jogos 2D
   - **3D**: Para jogos 3D
   - **3D (URP)**: Para jogos 3D com Universal Render Pipeline
   - **3D (HDRP)**: Para jogos 3D com High Definition Render Pipeline
4. Escolha um nome e localização para o projeto
5. Clique em **Create Project**

### Passo 4: Abrir Projeto no Cursor

1. Após criar o projeto, o Unity Editor abrirá automaticamente
2. No Cursor, vá em **File → Open Folder**
3. Navegue até a pasta do projeto Unity que você criou
4. Abra a pasta do projeto

### Estrutura de um Projeto Unity

```
MeuJogoUnity/
├── Assets/              # Assets do jogo (scripts, modelos, texturas)
│   ├── Scripts/        # Scripts C# (aqui você trabalha no Cursor)
│   ├── Scenes/         # Cenas do jogo
│   ├── Materials/      # Materiais
│   ├── Textures/       # Texturas
│   └── ...
├── Packages/            # Pacotes Unity
├── ProjectSettings/    # Configurações do projeto
└── ...
```

## 🎯 Fluxo de Trabalho Recomendado

1. **Criar/Editar Scripts no Cursor**
   - Crie scripts C# na pasta `Assets/Scripts/`
   - Use a IA do Cursor para ajudar com código
   - Aproveite o IntelliSense e autocomplete

2. **Voltar ao Unity Editor**
   - O Unity detecta automaticamente mudanças nos arquivos
   - Scripts são recompilados automaticamente
   - Teste e visualize no Unity Editor

3. **Iteração**
   - Edite no Cursor → Teste no Unity → Repita

## 💡 Vantagens de Usar Cursor com Unity

1. **IA Assistente**
   - Gere scripts Unity rapidamente
   - Resolva problemas com ajuda da IA
   - Aprenda padrões de código Unity

2. **Autocomplete Melhorado**
   - Melhor experiência de autocomplete
   - Sugestões contextuais

3. **Refatoração**
   - Renomear variáveis e classes facilmente
   - Extrair métodos
   - Reorganizar código

4. **Integração Git**
   - Controle de versão integrado
   - Commits e branches fáceis

5. **Múltiplos Arquivos**
   - Trabalhe com vários scripts simultaneamente
   - Navegação rápida entre arquivos

## ⚠️ Limitações

1. **Unity Editor Necessário**
   - Não pode visualizar cenas no Cursor
   - Não pode testar jogos no Cursor
   - Builds devem ser feitos no Unity Editor

2. **Visualização**
   - GameObjects e componentes são visíveis apenas no Unity Editor
   - Hierarquia de cenas não aparece no Cursor

3. **Testes**
   - Testes devem ser feitos no Unity Editor
   - Play Mode só funciona no Unity Editor

## 📖 Recursos de Aprendizado

### Tutoriais Oficiais
- **Unity Learn**: https://learn.unity.com/
- **Documentação Unity**: https://docs.unity3d.com/
- **Unity YouTube**: https://www.youtube.com/c/unity

### Canais Recomendados
- **Brackeys**: Tutoriais Unity (arquivo, mas ainda útil)
- **Code Monkey**: Tutoriais avançados
- **Jason Weimann**: Game development e arquitetura
- **Sebastian Lague**: Tutoriais detalhados

### Projetos para Praticar
1. **Roll-a-Ball** (Tutorial oficial Unity)
2. **2D Game Kit** (Template Unity)
3. **Microgames** (Templates Unity)

## 🔗 Integração com Cartela.bet

### Possibilidades Futuras

1. **Mini-jogos**
   - Desenvolver mini-jogos Unity para a plataforma
   - Integração via WebGL

2. **Gamificação**
   - Adicionar elementos de jogo às apostas
   - Sistema de conquistas e recompensas

3. **Visualizações Interativas**
   - Visualizações 3D de eventos esportivos
   - Animações de resultados

4. **Experiências Imersivas**
   - VR/AR para visualização de apostas
   - Experiências interativas para usuários

## 🛠️ Comandos Úteis

### No Unity Editor
- **Play**: `Ctrl + P` (Windows) / `Cmd + P` (Mac)
- **Save Scene**: `Ctrl + S`
- **Focus on Game Object**: `F`
- **Frame Selected**: `Shift + F`

### No Cursor
- **Buscar Arquivo**: `Ctrl + P`
- **Buscar Símbolo**: `Ctrl + Shift + O`
- **Terminal**: `Ctrl + `` (backtick)
- **Command Palette**: `Ctrl + Shift + P`

## 📝 Exemplo de Script Unity Básico

```csharp
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    public float speed = 5f;
    private Rigidbody rb;

    void Start()
    {
        rb = GetComponent<Rigidbody>();
    }

    void Update()
    {
        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");
        
        Vector3 movement = new Vector3(horizontal, 0f, vertical);
        rb.AddForce(movement * speed);
    }
}
```

## 🎓 Próximos Passos

1. **Instalar Unity Hub e Unity Editor**
2. **Configurar Cursor como editor externo**
3. **Criar um projeto Unity de teste**
4. **Fazer tutoriais básicos**
5. **Praticar com projetos pequenos**
6. **Explorar Asset Store**

## 📞 Suporte

- **Unity Forums**: https://forum.unity.com/
- **Unity Discord**: Comunidade ativa
- **Stack Overflow**: Tag `unity3d`
- **Reddit**: r/Unity3D

---

**Última atualização**: Janeiro 2025


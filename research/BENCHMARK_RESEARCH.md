# 📱 Benchmark Research & Design System — CineVault Mobile App
> Baseado nas diretrizes do **Appllama App Design Skill** e referências dos líderes de catálogo e streaming (Letterboxd, Apple TV, MUBI, IMDb, Reelgood).

---

## 1. Padrões de Ergonomia Mobile (Thumb Zone)
Em telas de smartphones modernos (6.1" a 6.9"), a parte superior da tela é de alcance difícil com uma única mão.
* **Ações primárias no terço inferior:** 
  - Barra de navegação inferior fixa com altura de toque mínima de 44x44pt.
  - Gatilho do Assistente de 3 etapas e Drawer de filtros acessíveis no rodapé.
  - Botão de 1-toque `[✓ Visto]` posicionado no canto direito inferior de cada card para ativação confortável com o polegar.
* **Safe Areas & Insets:**
  - Respeito obrigatório a `env(safe-area-inset-bottom)` para evitar sobreposição com o indicador de home do iOS e a barra de gestos do Android.

---

## 2. Padrões de Gavetas Móveis (Bottom Sheet Drawers)
Inspirado no comportamento nativo do iOS e implementações do Base UI / Vaul:
* **Gesto Drag-to-Dismiss:** Arrastar a barra do topo da gaveta para baixo deve fechar o modal com inércia física natural.
* **Backdrop blur:** Escurecimento sutil (`bg-black/70 backdrop-blur-md`) mantendo o contexto da lista por baixo.
* **Agrupamento de controles:** Segmented controls independentes para Formato (Tudo / Filmes / Séries) e Status, seguidos por chips compactos de Gênero, Streaming e Notas.

---

## 3. Padrões de Badges & Streaming
Inspirado no Apple TV e MUBI:
* **Badges de Streaming:** Pílulas sutis com as cores de marca de cada serviço brasileiro (Netflix `#E50914`, Max `#002BE7`, Prime Video `#00A8E1`, Disney+ `#113CCF`, Apple TV+ `#FFFFFF`, Paramount+ `#0064FF`).
* **Botão "Ver plataforma":** Link externo limpo com ícone de saída direcionando à busca do JustWatch Brasil.
* **Notas de Avaliação (IMDb & Rotten Tomatoes):** Tipografia mono nítida sem caixas pesadas ao redor:
  - IMDb: `★ 8.2` (amarelo âmbar)
  - Rotten Tomatometer (Crítica): `🍅 89%` (vermelho carmim)
  - Rotten Popcornmeter (Público): `🍿 94%` (dourado pipoca)

---

## 4. Movimento e Micro-interações a 60fps (Skecher UI)
* **Apple Mail Tabs:** Pílulas dinâmicas que expandem sua largura medindo o texto via spring animation (`stiffness: 420, damping: 36, mass: 0.8`).
* **Slide Transitions:** O fluxo do assistente corre lateralmente com aceleração cúbica natural (`ease: [0.23, 1, 0.32, 1]`).
* **Checkmark Pop:** O botão `[✓ Visto]` reage com um micro-escala (`scale: 1.15 -> 1.0`) ao ser marcado.

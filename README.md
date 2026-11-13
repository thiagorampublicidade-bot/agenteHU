# agenteHU

Base do agente que produz carrosséis institucionais (HU Brasil / campanhas de saúde) no Canva a partir de planilhas Excel.

## Como usar

1. Conecte o **Canva** em claude.ai → Configurações → Conectores.
2. Abra uma sessão do Claude Code com este repositório. As instruções do agente estão em `CLAUDE.md` e são carregadas automaticamente.
3. Coloque a planilha do briefing em `briefings/` (ou anexe na conversa) e diga quais carrosséis produzir.
4. Se houver logotipos oficiais para o projeto, coloque-os em `marcas/`.

## Estrutura

- `CLAUDE.md` — instruções permanentes do agente (direção de arte, fidelidade de texto, revisão, entrega).
- `referencias/` — referências visuais: Ciência e Cultura, Malária nas Américas, Poliomielite, Saúde Bucal (PPTX), Saúde Única (PDF) e exemplos de capa.
- `briefings/` — planilhas com o conteúdo dos carrosséis.

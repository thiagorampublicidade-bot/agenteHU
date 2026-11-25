# Montagem no Canva (conector MCP)

Caminho testado com as ferramentas do conector Canva. As ferramentas são "deferred": carregue os esquemas com `ToolSearch` (`select:mcp__Canva__create-design,mcp__Canva__read-design,mcp__Canva__edit-design,mcp__Canva__create-upload-url,mcp__Canva__list-brand-kits`) antes de chamar.

## 1. Brand Kit

`list-brand-kits` → se houver um kit do Echo, passe o `brand_kit_id` no `create-design`. Os kits podem vir sem nome; se houver mais de um e não der para saber qual é o do Echo, siga sem kit e aplique as cores de `clientes/echo-volei/marca/` manualmente.

## 2. Subir logo e fotos locais

Arquivos do repositório não têm URL pública, então use upload direto:

1. `create-upload-url` → recebe `upload_url` (uso único, expira rápido).
2. Envie os bytes crus:
   ```bash
   curl -sS -X POST "<upload_url>" -H "Content-Type: application/octet-stream" --data-binary @"clientes/echo-volei/marca/<logo>.png"
   ```
3. A resposta traz o id do recurso — guarde (ex.: em um arquivo no scratchpad) para usar em `insert_fill` / `update_fill`.

Uma URL por arquivo. Se falhar, peça outra URL; nunca reutilize.

Escolha as fotos antes de subir (olhe com Read): enquadramento compatível com a página, espaço para texto, nitidez no tamanho final. Suba só as que vai usar.

## 3. Criar o projeto

`create-design` com:
- `format`: `"Instagram Post (Portrait)"` (1080×1350). Inclua a orientação, senão sai quadrado.
- `brief`: tema, número de páginas, o sistema visual decidido e os textos das páginas na ordem.
- `references`: ids do logo e das fotos que já subiu.
- `brand_kit_id` quando houver.

Sem widget visível, consulte `get-create-design-async-job` respeitando `polling_policy.wait_seconds` até concluir. Guarde o `design_id` e o link.

O resultado é um ponto de partida gerado pelo Canva — trate como rascunho. Quase sempre será preciso reconstruir páginas para cumprir a direção de arte e o texto exato.

## 4. Editar página por página

1. `read-design` com `open_transaction: true` e `filter.fields: ["design_content", "thumbnails"]` → `transaction_id` e os `locator_id` dos elementos.
2. `edit-design` com `finalize: "keep_open"`, `page_index` e operações. As úteis:
   - `replace_text` / `find_and_replace_text` — texto exato da planilha.
   - `format_text` — tamanho, peso, cor, alinhamento, entrelinha.
   - `delete_element` — remover enfeites genéricos do rascunho.
   - `add_text` (com `width` para quebra controlada), `insert_shape` (faixas, blocos; caminho SVG só com M/L/H/V/C/S/A/Z), `insert_fill` (foto/logo pelo id), `crop_media`, `position_element`, `resize_element`, `layer_element`, `recolor_element`.
   - `add_page` (width 1080, height 1350, `background_color`) e `reorder_page` para casar com a ordem da planilha.
   - `update_title` → `Echo Vôlei — <Tema> — Carrossel — v1`.
3. Confira a miniatura devolvida após cada lote de operações. Ajuste.
4. Ao terminar todas as páginas e a revisão: `edit-design` com `finalize: "commit"` e sem operações.

Sobre salvar: o projeto é novo e foi criado a pedido do usuário para esta entrega, então salvar o rascunho revisado faz parte da tarefa. Se estiver editando um design **que já existia** (ajuste pedido em projeto anterior), mostre as miniaturas e peça confirmação antes do `commit`.

Se algo der errado no meio, `finalize: "cancel"` descarta a transação.

## 5. Revisão final

`read-design` (sem transação, versão salva) com `fields: ["thumbnails", "design_content"]` e `thumbnail_pages` de todas as páginas. Compare cada texto com a planilha. O link a entregar é o retornado pelas ferramentas.

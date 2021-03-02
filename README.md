# lexical-analyzer

Analisador Léxico desenvolvido para o MI - PROCESSADORES DE LINGUAGEM DE PROGRAMAÇÃO

## Tabela com Estrututa Léxica | Table With Lexical Structure

| Descrição | Composição |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Palavras Reservadas  | `var`, `const`, `typeDef`, `struct`, `extends`, `procedure`, `function`, `start`, `return`, `if`, `else`, `then`, `while`, `read`, `print`, `int`, `real`, `boolean`, `string`, `true`, `false`, `global`, `local` |
| Identificadores (ID) | letra(letra \| digito \| `_` )\*|
| Números| Dígito+( . Dígito+)? |
| Dígito | [0-9] |
| Letra | [a-z] \| [A-Z] |
| Operadores Aritméticos | `+` `-` `*` `/` `++` `--` |
| Operadores Relacionais | `==` `!=` `>` `>=` `<` `<=` `=` |
| Operadores Lógicos | `&&` `||` `!` |
| Delimitadores de Comentários | `//` Isto é um comentário de linha `/*` Isto é um comentário de bloco `*/`
| Delimitadores | `;` `,` `()` `[]` `{}` `.` |
| Cadeia de Caracteres (String )| "(letra \| digito \| simbolo \| `\"`)* " |
| Simbolo | ASCII de 32 a 126 (exceto ASCII 34) |


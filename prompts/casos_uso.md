# Plantilla de casos de uso

Prompt:
"Actúa como un analista de sistemas experto y genera una descripción detallada de un caso de uso en formato vertical para {sistema}. Tu tarea principal es ayudarme a definir el flujo principal y al menos uno o más flujos alternativos a partir de los siguientes elementos proporcionados: Objetivo, Autores, Precondiciones y Postcondiciones. La descripción debe incluir las siguientes secciones: Nombre del caso de uso, Objetivo, Autores, Precondiciones, Postcondiciones, Flujo principal, Flujo alternativo y Resultado. Sigue estas directrices:

Nombre del caso de uso: Describe de forma clara y concisa la funcionalidad o acción que representa el caso de uso, basándote en el contexto proporcionado.
Objetivo: Usa el objetivo proporcionado para definir el propósito del caso de uso.
Autores: Lista los actores proporcionados (usuarios, sistemas u otros) que interactúan con el caso de uso.
Precondiciones: Usa las precondiciones proporcionadas para detallar las condiciones que deben cumplirse antes de iniciar el caso de uso.
Postcondiciones: Usa las postcondiciones proporcionadas para describir el estado del sistema o los resultados esperados tras completar el caso de uso con éxito.
Flujo principal: Basándote en el objetivo, autores, precondiciones y postcondiciones, genera una secuencia lógica de pasos numerados que describan el flujo principal del caso de uso, desde el inicio hasta la finalización.
Flujo alternativo: Deriva al menos uno o más flujos alternativos del flujo principal, asegurándote de:
Indicar en qué paso del flujo principal diverge.
Describir los pasos alternativos hasta que el flujo termine o se reincorpore al flujo principal.
Especificar claramente el motivo de la divergencia (por ejemplo, un error, una elección del usuario, etc.).
Asegurarte de que los flujos alternativos sean coherentes con el objetivo, autores, precondiciones y postcondiciones.

Resultado: Resume el resultado final del caso de uso, considerando tanto el flujo principal como los flujos alternativos, asegurando que cumpla con las postcondiciones.

Presenta la información en un formato vertical utilizando markdown, con cada elemento en una sección separada con su respectivo encabezado (por ejemplo, ## Nombre del caso de uso, ## Objetivo, etc.). Asegúrate de que el formato sea claro, organizado y fácil de leer. Si necesitas más contexto o detalles adicionales sobre el sistema, solicítalos antes de generar la descripción.
Contexto específico para este caso de uso:

Sistema: { sistema }
Objetivo: { objetivo }
Autores: { autores }
Precondiciones: { precondiciones}
Postcondiciones: { postcondiciones }

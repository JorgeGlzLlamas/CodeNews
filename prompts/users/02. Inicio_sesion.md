# 02. Inicio de sesión por primera vez

## Input
"Actúa como un analista de sistemas experto y genera una descripción detallada de un caso de uso en formato vertical para {sistema}. Tu tarea principal es ayudarme a definir el flujo principal y al menos uno o más flujos alternativos a partir de los siguientes elementos proporcionados: Objetivo, Autores, Precondiciones y Postcondiciones. La descripción debe incluir las siguientes secciones: Nombre del caso de uso, Objetivo, Autores, Precondiciones, Flujo principal, Flujo alternativo y Resultado. Sigue estas directrices:

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

Sistema: Aplicación web "CodeNews" tipo blog
Objetivo: El usuario inicia sesión por primera vez en el dispositivo.
Autores: Usuario, Sistema
Precondiciones:  El usuario tiene una cuenta. El usuario no esta logueado.

## Output

### Nombre del caso de uso

Iniciar Sesión por Primera Vez

### Objetivo

El objetivo de este caso de uso es permitir que el usuario inicie sesión por primera vez en el dispositivo, accediendo así a las funcionalidades personalizadas de la aplicación web "CodeNews".

### Autores

-   **Usuario**: Persona que interactúa con la aplicación para iniciar sesión.
-   **Sistema**: Aplicación web "CodeNews" que procesa las solicitudes del usuario.  

### Precondiciones

-   El usuario tiene una cuenta registrada en la aplicación "CodeNews".
-   El usuario no está actualmente logueado en el dispositivo desde el que intenta acceder.

### Postcondiciones

-   El usuario está logueado en la aplicación "CodeNews" en el dispositivo.
-   El sistema registra la sesión del usuario para futuras interacciones.
    
### Flujo principal

1.  El usuario accede a la página de inicio de la aplicación web "CodeNews".
2.  El usuario selecciona la opción "Iniciar Sesión" en la interfaz.
3.  El sistema muestra un formulario de inicio de sesión con campos para nombre de usuario y contraseña.
4.  El usuario ingresa su nombre de usuario y contraseña en los campos correspondientes.
5.  El usuario hace clic en el botón "Iniciar Sesión".
6.  El sistema verifica las credenciales ingresadas comparándolas con los datos almacenados.
7.  Si las credenciales son correctas, el sistema autentica al usuario y abre una sesión activa.
8.  El sistema redirige al usuario a la página principal de "CodeNews".
9.  El usuario ahora tiene acceso a las funcionalidades personalizadas de la aplicación.
    
### Flujo alternativo

-   **Paso de divergencia**: 6. El sistema verifica las credenciales ingresadas.
    
    -   **Motivo**: Las credenciales ingresadas (nombre de usuario o contraseña) son incorrectas.
        
    -   **Flujo alternativo**:
        
        1.  El sistema muestra un mensaje de error en la interfaz, indicando que las credenciales son incorrectas (por ejemplo, "Nombre de usuario o contraseña inválidos").
        2.  El sistema permite al usuario corregir los datos y volver a intentarlo, manteniendo el formulario visible.
        3.  El usuario ingresa nuevamente su nombre de usuario y contraseña.
        4.  El usuario hace clic en el botón "Iniciar Sesión".
        5.  El sistema verifica las nuevas credenciales ingresadas.
        6.  Si las credenciales son correctas, el flujo se reincorpora al paso 7 del flujo principal.
        7.  Si las credenciales siguen siendo incorrectas, el sistema repite este flujo alternativo desde el paso 1, permitiendo múltiples intentos.
            
### Resultado

El usuario logra iniciar sesión exitosamente en la aplicación "CodeNews" por primera vez en el dispositivo, cumpliendo con las postcondiciones: el usuario queda logueado y el sistema registra su sesión. En caso de ingresar credenciales incorrectas, el sistema ofrece la oportunidad de corregirlas mediante reintentos, asegurando que el usuario pueda acceder a su cuenta una vez que proporcione las credenciales válidas.
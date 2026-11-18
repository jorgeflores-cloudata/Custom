# Custom

Scripts de utilidad y los comandos globales `awake` y `cursor` para PowerShell / terminal de VSCode.

| Comando  | Script               | Qué hace                                      |
|----------|----------------------|-----------------------------------------------|
| `awake`  | `keep_awake.py`      | Mantiene el equipo despierto (600 min, pantalla encendida) |
| `cursor` | `move_cursor_to.py`  | Mueve el cursor por 3 puntos, 200 repeticiones |

## Instalación

1. Clona el repo (o copia la carpeta) en una ruta fija, por ejemplo:
   `C:\Users\<usuario>\OneDrive - Stellus Rx\Custom`
2. Abre el perfil de PowerShell para todos los hosts (incluye VSCode):

   ```powershell
   New-Item -ItemType File -Force $PROFILE.CurrentUserAllHosts | Out-Null
   code $PROFILE.CurrentUserAllHosts
   ```

3. Pega estas funciones. **Ajusta la ruta** a donde esté la carpeta `Custom`:

   ```powershell
   function awake {
       python "C:\Users\<usuario>\OneDrive - Stellus Rx\Custom\keep_awake.py" --minutes 600 --display @args
   }

   function cursor {
       python "C:\Users\<usuario>\OneDrive - Stellus Rx\Custom\move_cursor_to.py" --points '[[100,100],[500,300],[900,600]]' --repeat 200 --duration 5 --pause 0.2 @args
   }
   ```

4. Guarda y abre una terminal nueva en VSCode (o ejecuta `. $PROFILE.CurrentUserAllHosts`).
5. Escribe `awake` o `cursor` desde cualquier directorio.

## Uso

- Los argumentos extra se agregan al final: `awake --minutes 120`.
- Para detener cualquiera de los dos: `Ctrl+C`.

## Solución de problemas

- **"awake" no se reconoce**: abre una terminal nueva; el perfil se carga al iniciar.
- **El perfil no carga (política de ejecución)**:
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
- **`python` no se encuentra**: verifica con `python --version` que Python esté en el PATH.

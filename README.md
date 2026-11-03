# Expedición a Roma — web con inscripción pública y panel de administrador

## Qué incluye
- Nombre de la web: **Expedición a Roma**.
- Diseño visual inspirado en una web de viajes, con fotografías de Roma.
- Los usuarios no necesitan cuenta: rellenan nombre y curso/grupo y envían la inscripción.
- El administrador entra por un acceso privado y puede consultar inscripciones, actualizar el estado del pago, anotar el número de partes, escribir notas y borrar inscripciones.
- Los datos se guardan en una base de datos SQLite.

## Probarla en tu ordenador

Necesitas Python 3.10 o posterior.

1. Descomprime el ZIP.
2. Abre una terminal dentro de la carpeta `expedicion_roma_web_profesional`.
3. Instala Flask:

   `pip install -r requirements.txt`

4. Crea un hash para tu contraseña de administrador (cambia el texto por una contraseña tuya):

   `python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('TU_CONTRASEÑA_SEGURA'))"`

   Copia el resultado.

5. Configura dos variables secretas.

   Linux/macOS:
   `export FLASK_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"`
   `export ADMIN_PASSWORD_HASH='PEGA_AQUI_EL_HASH'`

   Windows PowerShell:
   `$env:FLASK_SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"`
   `$env:ADMIN_PASSWORD_HASH = "PEGA_AQUI_EL_HASH"`

6. Ejecuta:
   `python app.py`

7. Abre `http://127.0.0.1:5000`. El acceso de administrador está en la parte superior de la página.

## Publicarla en Internet

Este ZIP todavía no es una web pública. Para que alumnos puedan entrar desde sus móviles, debes desplegarla en un hosting compatible con Flask, activar HTTPS y configurar las variables `FLASK_SECRET_KEY` y `ADMIN_PASSWORD_HASH` en el panel del hosting. Asegúrate de que el hosting tenga almacenamiento persistente para `expedicion_roma.db` o configura una base de datos gestionada.

Las fotografías se cargan desde Unsplash y las fuentes desde Google Fonts, por lo que la página necesita conexión a Internet para mostrarlas.

## Privacidad y seguridad: importante

Esta versión es una plantilla educativa inicial. No introduzcas datos personales reales de menores ni la compartas para inscripciones reales hasta que el centro educativo la autorice y una persona responsable revise el cumplimiento de protección de datos y la seguridad.

Por diseño, el formulario público solo pide nombre y curso/grupo. No pide DNI, teléfono, dirección ni fecha de nacimiento. El número de partes y el pago solo los modifica el administrador; la web no procesa ni verifica pagos. El equipo directivo debe decidir la participación conforme a las normas del centro.

Antes de publicarla para uso real, se recomienda añadir protección CSRF, limitación de intentos de acceso, copias de seguridad, gestión segura de datos, política de privacidad y revisión técnica. Usa HTTPS y una contraseña robusta y única.

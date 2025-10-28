# ObjectDetection

Proyecto Python para detección de objetos.

Archivos principales:
- `detector.py`
- `probar_indices.py`

Requisitos (ejemplo):
- Python 3.8+
- Instalar dependencias en `requirements.txt` si se agrega.

Cómo ejecutar (local):
1. Crear y activar un entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instalar dependencias (si las añades):

```powershell
pip install -r requirements.txt
```

3. Ejecutar el detector (ejemplo):

```powershell
python detector.py
```

Inicialización Git y subida a GitHub:
- Localmente ya se inicializa y hace el commit inicial (si no existe repositorio).
- Para crear el repo remoto desde la línea de comandos (si tienes `gh` instalado y autenticado):

```powershell
cd "C:\Users\USUARIO\Desktop\ObjectDetection"
gh repo create NOMBRE_DEL_REPO --public --source=. --remote=origin --push
```

- Alternativa: crea el repositorio en github.com y luego enlaza el remoto:

```powershell
git remote add origin https://github.com/USUARIO/NOMBRE_DEL_REPO.git
git push -u origin main
```

Si quieres, puedo crear el repo remoto por ti usando `gh` (necesitas autorizarlo) o puedo darte los pasos para crearlo manualmente.

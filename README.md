
# FastAPI Backend  

## Instalación  

1. Clona el repositorio:  
   ```bash
   git clone https://github.com/tu-usuario/tu-repo.git
   cd tu-repo
   ```

2. Crea un entorno virtual e instala dependencias:  
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configura las variables de entorno:  
   Crea un archivo `.env` en la raíz del proyecto con:  
   ```env
   DATABASE_URL=postgresql://user:password@localhost/dbname
   SECRET_KEY=tu-clave-secreta
   ```

4. Ejecuta el servidor:  
   ```bash
   uvicorn main:app --reload
   ```

5. Accede a la API en:  
   ```
   http://127.0.0.1:8000
   ```

## Notas  
- Requiere **Python 3.8+**.  
- Asegúrate de tener **PostgreSQL** instalado y en funcionamiento.  

# OCR API

API REST para extraer texto de documentos PDF escaneados usando OCR (Reconocimiento Óptico de Caracteres) con Tesseract.

## 📋 Descripción

Esta API permite:
- Subir archivos PDF escaneados
- Extraer texto usando OCR con soporte para múltiples idiomas
- Guardar archivos originales y texto extraído con nombres únicos (UUID)
- Configurar el idioma de reconocimiento

## 🚀 Instalación y Uso

### Opción 1: Usando Docker (Recomendado)

#### Prerrequisitos
- Docker instalado
- Docker Compose instalado

#### Pasos de instalación

1. **Clonar o descargar el proyecto**
```bash
git clone https://github.com/akuzsb/ocr-api
cd ocr-api
```

2. **Construir y levantar el contenedor**

**Para producción:**
```bash
docker-compose up --build -d
```

**Para desarrollo:**
```bash
docker-compose -f docker-compose.dev.yml up --build
```

3. **Verificar que funciona**
```bash
curl http://localhost:8000
```

#### Comandos útiles Docker

**Producción:**
```bash
# Ver logs
docker-compose logs -f

# Parar el servicio
docker-compose down

# Reconstruir sin caché
docker-compose build --no-cache
```

**Desarrollo:**
```bash
# Ver logs
docker-compose -f docker-compose.dev.yml logs -f

# Parar el servicio
docker-compose -f docker-compose.dev.yml down

# Reconstruir sin caché
docker-compose -f docker-compose.dev.yml build --no-cache
```

**General:**
```bash
# Ver contenedores activos
docker ps
```

### Opción 2: Instalación Local (Windows)

#### Prerrequisitos
- Python 3.11+
- Tesseract OCR
- Poppler

#### Instalar Tesseract OCR
1. Descargar desde: https://github.com/UB-Mannheim/tesseract/wiki
2. Instalar en `C:\Program Files\Tesseract-OCR\`
3. Agregar al PATH del sistema

#### Instalar Poppler
1. Descargar desde: https://github.com/oschwartz10612/poppler-windows/releases
2. Extraer en `C:\poppler\`
3. Agregar `C:\poppler\Library\bin` al PATH

#### Instalar dependencias Python
```bash
pip install -r requirements.txt
```

#### Ejecutar la aplicación

**Para desarrollo:**
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Para producción:**
```bash
python main.py
```

## 🔧 Entornos de Desarrollo vs Producción

### Desarrollo
- **Hot reload**: Los cambios en código se aplican automáticamente
- **Volúmenes**: El código está montado como volumen para edición en vivo
- **Sin usuario restringido**: Ejecuta como root para facilitar desarrollo
- **Dockerfile**: `Dockerfile.dev`
- **Compose**: `docker-compose.dev.yml`

### Producción
- **Sin reload**: Mayor estabilidad y performance
- **Usuario no-root**: Mayor seguridad con usuario `app`
- **Healthcheck**: Monitoreo de salud del contenedor
- **Optimizado**: Menor overhead de recursos
- **Dockerfile**: `Dockerfile`
- **Compose**: `docker-compose.yml`

## 📖 Uso de la API

### Endpoint Principal

**POST** `/extract-text/`

### Parámetros

- **file**: Archivo PDF (requerido)
- **language**: Idioma para OCR (opcional, por defecto: 'spa')

### Idiomas soportados

| Código | Idioma |
|--------|--------|
| spa    | Español |
| eng    | Inglés |

### Ejemplos de uso

#### Con curl
```bash
# Español (por defecto)
curl -X POST "http://localhost:8000/extract-text/" \
     -F "file=@documento.pdf"

# Inglés
curl -X POST "http://localhost:8000/extract-text/?language=eng" \
     -F "file=@document.pdf"
```

#### Con Python
```python
import requests

url = "http://localhost:8000/extract-text/"
files = {"file": open("documento.pdf", "rb")}
params = {"language": "spa"}

response = requests.post(url, files=files, params=params)
print(response.json())
```

### Respuesta de ejemplo
```json
{
    "message": "Texto extraído exitosamente",
    "uuid": "12345678-1234-5678-9012-123456789abc",
    "txt_filename": "12345678-1234-5678-9012-123456789abc.txt",
    "txt_file_path": "extracted_texts/12345678-1234-5678-9012-123456789abc.txt",
    "pdf_filename": "12345678-1234-5678-9012-123456789abc.pdf",
    "pdf_file_path": "original_pdfs/12345678-1234-5678-9012-123456789abc.pdf",
    "language": "spa",
    "original_filename": "mi_documento.pdf"
}
```

## 📁 Estructura del proyecto

```
ocr-api/
├── main.py                    # Aplicación principal
├── requirements.txt           # Dependencias Python
├── Dockerfile                 # Docker producción
├── Dockerfile.dev             # Docker desarrollo
├── docker-compose.yml         # Compose producción
├── docker-compose.dev.yml     # Compose desarrollo
├── .gitignore                 # Archivos excluidos
├── README.md                  # Este archivo
├── extracted_texts/           # Archivos de texto extraído
└── original_pdfs/             # PDFs originales guardados
```

## 🔍 Documentación interactiva

Una vez que la API esté ejecutándose, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🛠️ Desarrollo

### Modificar código en desarrollo
El entorno de desarrollo monta el código como volumen, por lo que los cambios se reflejan automáticamente.

### Ver logs
```bash
# Producción
docker-compose logs -f ocr-api

# Desarrollo
docker-compose -f docker-compose.dev.yml logs -f ocr-api
```

### Acceder al contenedor
```bash
# Producción
docker-compose exec ocr-api bash

# Desarrollo
docker-compose -f docker-compose.dev.yml exec ocr-api bash
```

### Construir solo las imágenes
```bash
# Producción
docker build -t ocr-api:prod .

# Desarrollo
docker build -f Dockerfile.dev -t ocr-api:dev .
```

## ⚠️ Solución de problemas

### Error de Tesseract no encontrado
```bash
# Verificar instalación en el contenedor
docker-compose exec ocr-api tesseract --version
```

### Error de Poppler no encontrado
```bash
# Verificar instalación en el contenedor
docker-compose exec ocr-api pdftoppm -h
```

### Puerto ocupado
```bash
# Cambiar puerto en docker-compose.yml
ports:
  - "8001:8000"  # Usar puerto 8001 en lugar de 8000
```

### Problemas de permisos en Windows
```bash
# Asegurar que las carpetas existan
mkdir extracted_texts original_pdfs
```

### Contenedor no responde
```bash
# Verificar estado
docker-compose ps

# Verificar logs para errores
docker-compose logs ocr-api
```

## 🚀 Despliegue

### Recomendaciones para producción
1. Usar `docker-compose.yml` (sin `.dev`)
2. Configurar variables de entorno apropiadas
3. Usar un proxy reverso (nginx) si es necesario
4. Monitorear logs y métricas
5. Configurar backups de las carpetas de salida

### Variables de entorno
```bash
# En .env file
PYTHONPATH=/app
ENV=production
```
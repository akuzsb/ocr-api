import os
import uuid
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import tempfile
import shutil

app = FastAPI(title="OCR API", description="API para extraer texto de PDFs escaneados")

def extract_text_from_scanned_pdf(pdf_path, language='spa'):
    # Verificar si el archivo existe
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"El archivo {pdf_path} no existe")
    
    pages = convert_from_path(pdf_path)
    extracted_text = ""

    for page_num, page_image in enumerate(pages):
        print(f"Procesando página {page_num + 1}...")
        page_text = pytesseract.image_to_string(
            page_image, 
            lang=language
        )
        
        extracted_text += f"\n--- Página {page_num + 1} ---\n"
        extracted_text += page_text

    return extracted_text

@app.post("/extract-text/")
async def extract_text_endpoint(
    file: UploadFile = File(...),
    language: str = Query(default='spa', description="Código de idioma para OCR (spa=español, eng=inglés, fra=francés, etc.)")
):
    # Validar que el archivo sea un PDF
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")
    
    # Generar UUID único para los nombres de archivo
    unique_id = str(uuid.uuid4())
    txt_filename = f"{unique_id}.txt"
    pdf_filename = f"{unique_id}.pdf"
    
    try:
        # Crear directorios para archivos de salida si no existen
        txt_output_dir = "extracted_texts"
        pdf_output_dir = "original_pdfs"
        os.makedirs(txt_output_dir, exist_ok=True)
        os.makedirs(pdf_output_dir, exist_ok=True)
        
        # Crear archivo temporal para el PDF subido
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            # Copiar el contenido del archivo subido al archivo temporal
            shutil.copyfileobj(file.file, temp_pdf)
            temp_pdf_path = temp_pdf.name
        
        # Guardar el PDF original con nombre UUID
        pdf_output_path = os.path.join(pdf_output_dir, pdf_filename)
        shutil.copy2(temp_pdf_path, pdf_output_path)
        
        # Extraer texto del PDF con el idioma especificado
        extracted_text = extract_text_from_scanned_pdf(temp_pdf_path, language)
        
        # Guardar el texto extraído en un archivo con nombre UUID
        txt_output_path = os.path.join(txt_output_dir, txt_filename)
        with open(txt_output_path, 'w', encoding='utf-8') as f:
            f.write(extracted_text)
        
        # Limpiar archivo temporal
        os.unlink(temp_pdf_path)
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Texto extraído exitosamente",
                "uuid": unique_id,
                "txt_filename": txt_filename,
                "txt_file_path": txt_output_path,
                "pdf_filename": pdf_filename,
                "pdf_file_path": pdf_output_path,
                "language": language,
                "original_filename": file.filename
            }
        )
        
    except Exception as e:
        # Limpiar archivo temporal en caso de error
        if 'temp_pdf_path' in locals():
            try:
                os.unlink(temp_pdf_path)
            except:
                pass
        
        raise HTTPException(status_code=500, detail=f"Error procesando el archivo: {str(e)}")

@app.get("/")
async def root():
    return {"message": "OCR API está funcionando. Use POST /extract-text/ para extraer texto de PDFs"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI, Form, Request
import uvicorn

app = FastAPI()

@app.post("/test")
async def test_form(request: Request):
    try:
        form_data = await request.form()
        return {"data_recebida": dict(form_data)}
    except Exception as e:
        return {"erro": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

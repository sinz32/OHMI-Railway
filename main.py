from fastapi import FastAPI
from ohmi_railway import get_data

app = FastAPI()
# app = FastAPI(
#     docs_url=None,       # Swagger UI 차단
#     redoc_url=None,      # ReDoc(또 다른 문서) 차단
#     openapi_url=None     # 문서의 원본 데이터가 되는 JSON 파일까지 완전 차단
# )

@app.get('/')
def get_line_data(line: str):
    return get_data(line)


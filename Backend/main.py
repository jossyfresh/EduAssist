from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer
from app.api.v1.api import api_router
from app.core.config import settings
from app.db.init_db import init_db

# Initialize database
init_db()

# Create security scheme
security = HTTPBearer()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=None,  # Disable default docs
    redoc_url=None,  # Disable default redoc
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description="EduAssist API",
        routes=app.routes,
    )
    
    # Add security scheme
    openapi_schema["components"] = {
        "securitySchemes": {
            "Bearer": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Enter your JWT token in the format: Bearer <token>"
            }
        }
    }
    
    # Add global security requirement
    openapi_schema["security"] = [{"Bearer": []}]
    
    # Add security requirements to each operation
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            if "security" not in operation:
                operation["security"] = [{"Bearer": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Custom Swagger UI
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        title=f"{settings.PROJECT_NAME} - Swagger UI",
        oauth2_redirect_url=None,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css",
        swagger_ui_parameters={
            "persistAuthorization": True,
            "displayRequestDuration": True,
            "filter": True,
            "tryItOutEnabled": True,
            "syntaxHighlight.theme": "monokai",
            "defaultModelsExpandDepth": 3,
            "defaultModelExpandDepth": 3,
            "docExpansion": "none",
            "filter": True,
            "showExtensions": True,
            "showCommonExtensions": True,
            "supportedSubmitMethods": ["get", "post", "put", "delete", "patch"],
            "validatorUrl": None,
            "deepLinking": True,
            "displayOperationId": True,
            "defaultModelRendering": "model",
            "displayRequestDuration": True,
            "docExpansion": "none",
            "filter": True,
            "operationsSorter": "alpha",
            "showExtensions": True,
            "showCommonExtensions": True,
            "tagsSorter": "alpha",
            "tryItOutEnabled": True,
            "validatorUrl": None
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True) 
from fastapi.security import HTTPBearer

# Create a single security scheme
security = HTTPBearer(auto_error=True) 
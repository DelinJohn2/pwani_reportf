from fastapi import FastAPI
from routes import routes # import your router module

app=FastAPI(
    title="Report Generation Application"

)
app.include_router(routes.router, prefix="/api", tags=["Routes"])


@app.get('/')
def root():
    return {'message':"report generation application is running"}
import uvicorn

# file allows us to run server which will handle our api
if __name__=='__main__':
    uvicorn.run('empik_api:app', port=8000,reload=True)



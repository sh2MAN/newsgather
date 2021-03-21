from fastapi import FastAPI, Query
from grabber import Lenta
from schemas import Result


app = FastAPI()


@app.get('/')
def root():
    return {'message': 'Hello World'}


@app.get('/news', response_model=Result)
def news(limit: int = Query(None, gt=0, description='Количество новостей')):
    grabber = Lenta()
    news = grabber.news(limit)
    data = []
    try:
        for i in range(len(news)):
            data.append(grabber.grub(news[i]['link']))
    except Exception:
        return {'error': 'Ошибка выполнения запроса'}
    return {'results': data}

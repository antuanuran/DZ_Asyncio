import asyncio
import httpx
import sys
from pprint import pprint
from db import engine, Session, People, Base


async def grab_by_url(client, url):
    response = await client.get(url)
    return response.json()


async def format_data(client, urls, result_key):
    if not urls:
        return ''
    else:
        names_films = []
        for url in urls:
            tasks = [grab_by_url(client, url)]
            inner_data = await asyncio.gather(*tasks)
            names_films.append(inner_data[0][result_key])

        return names_films


async def grab_star_wars_info(person_id):
    async with httpx.AsyncClient() as client:
        print('Начало загрузки данных....')
        data = await grab_by_url(client, f'https://swapi.dev/api/people/{person_id}/')

        print('Форматировние строк....')
        data['homeworld'] = (await grab_by_url(client, data['homeworld']))['name']
        data['films'] = await format_data(client, data['films'], 'title')
        data['species'] = await format_data(client, data['species'], 'name')
        data['vehicles'] = await format_data(client, data['vehicles'], 'name')
        data['starships'] = await format_data(client, data['starships'], 'name')
        print('Данные загружены....')

    return data


async def upload_to_db(data):
    pprint(data)
    print('Загрузка в Базу Данных....')

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()

    async with Session() as session:
        new_person = People(json=data)
        session.add(new_person)
        await session.commit()
        print('Завершено')


async def main(person_id):
    data = await grab_star_wars_info(person_id)
    await upload_to_db(data)


async def basic(person_id):
    tasks = [main(person_id)]
    await asyncio.gather(*tasks)


if __name__ == '__main__':

    if len(sys.argv) > 1:
        person_id = int(sys.argv[1])
    else:
        person_id = 1

    asyncio.run(basic(person_id))





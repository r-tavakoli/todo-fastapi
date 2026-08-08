from httpx import AsyncClient


async def test_get_main(client: AsyncClient):
    response = await client.get("/test")
    assert response.status_code == 200 
    assert response.json() == {"test": "everything is fine"}
import json
from http import HTTPStatus
from typing import Dict

from httpx import AsyncClient
import pytest


@pytest.mark.tweet
@pytest.mark.usefixtures("users", "posts")
class TestPosts:
    @pytest.fixture(scope="class")
    async def headers_with_content_type(self, headers: Dict) -> Dict:
        """
        Заголовок при добавлении нового поста
        """
        headers["Content-Type"] = "application/json"
        return headers

    @pytest.fixture(scope="class")
    async def resp_for_new_post(self, good_response: Dict) -> Dict:
        """
        Успешный ответ при добавлении нового поста
        """
        good_resp = good_response.copy()
        # id = 4, т.к. фикстурами уже создано 3 поста
        good_resp["post_id"] = 4
        return good_resp

    @pytest.fixture(scope="class")
    async def new_post(self) -> Dict:
        """
        Данные для добавления нового поста
        """
        return {"post_data": "Тестовый пост", "post_media_ids": []}

    @pytest.fixture(scope="class")
    async def response_post_locked(self, response_locked: Dict) -> Dict:
        response_locked["error_message"] = "The post that is being accessed is locked"
        return response_locked

    async def send_request(
        self, client: AsyncClient, headers: Dict, new_post_data: Dict = new_post
    ):
        """
        Отправка запроса на добавление нового поста
        """
        resp = await client.post(
            "/api/posts", data=json.dumps(new_post_data), headers=headers
        )

        return resp

    async def test_create_post(
        self,
        client: AsyncClient,
        new_post: Dict,
        headers_with_content_type: Dict,
        resp_for_new_post: Dict,
    ) -> None:
        """
        Тестирование добавления поста
        """
        resp = await self.send_request(
            client=client, headers=headers_with_content_type, new_post_data=new_post
        )

        assert resp
        assert resp.status_code == HTTPStatus.CREATED
        assert resp.json() == resp_for_new_post

        # Меняем id для проверки, т.к. текущий пост имеет 4 порядковый номер в БД
        resp_for_new_post["post_id"] = 5

        assert resp
        assert resp.status_code == HTTPStatus.CREATED
        assert resp.json() == resp_for_new_post

    async def test_create_invalid_post(
        self,
        client: AsyncClient,
        headers_with_content_type: Dict,
        new_post: Dict,
        bad_response: Dict,
    ) -> None:
        """
        Тестирование вывода сообщения об ошибке при публикации слишком длинного поста (> 280 символов)
        """
        new_post["post_data"] = (
            "Python — идеальный язык для новичка. "
            "Код на Python легко писать и читать, язык стабильно занимает высокие места "
            "в рейтингах популярности, а «питонисты» востребованы почти во всех сферах "
            "IT — программировании, анализе данных, системном администрировании и тестировании. "
            "YouTube, Intel, Pixar, NASA, VK, Яндекс — вот лишь немногие из известных компаний, "
            "которые используют Python в своих продуктах."
        )

        resp = await self.send_request(
            client=client, headers=headers_with_content_type, new_post_data=new_post
        )

        bad_response["error_type"] = f"{HTTPStatus.UNPROCESSABLE_ENTITY}"
        bad_response["error_message"] = (
            f"The length of the post should not exceed 280 characters. "
            f"Current value: {len(new_post['post_data'])}"
        )

        assert resp
        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert resp.json() == bad_response

    async def test_delete_post(
        self, client: AsyncClient, headers: Dict, good_response: Dict
    ) -> None:
        """
        Тестирование удаление поста
        """
        resp = await client.delete("/api/posts/1", headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert resp.json() == good_response

    async def test_delete_post_not_found(
        self, client: AsyncClient, headers: Dict, response_post_not_found: Dict
    ) -> None:
        """
        Тестирование вывода ошибки при попытке удалить несуществующий пост
        """
        resp = await client.delete("/api/posts/1000", headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert resp.json() == response_post_not_found

    async def test_delete_post_locked(
        self, client: AsyncClient, headers: Dict, response_post_locked: Dict
    ) -> None:
        """
        Тестирование вывода ошибки при попытке удалить чужой пост
        """
        resp = await client.delete("/api/posts/2", headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.LOCKED
        assert resp.json() == response_post_locked
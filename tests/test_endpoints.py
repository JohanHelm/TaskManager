import pytest


@pytest.mark.asyncio
async def test_create_task(async_client):
    data = {"name": "name_test",
            "description": "description_test",
            "status": "created",
            }
    response = await async_client.post("/task", json=data)
    assert response.status_code == 201


@pytest.mark.parametrize("false_uuid_prefix, expected_status_code, task_exist",
                         [("", 200, True,),
                          ("abrakadabra", 404, False,),]
                         )
@pytest.mark.asyncio
async def test_get_task(async_client, first_task, false_uuid_prefix, expected_status_code, task_exist):
    response = await async_client.get(f"/task/{false_uuid_prefix}{first_task['id']}")
    assert response.status_code == expected_status_code
    if task_exist:
        assert response.json() == {"description": first_task["description"],
                                   "id": first_task["id"],
                                   "name": first_task["name"],
                                   "status": first_task["status"]}
    else:
        assert response.json() == {"detail": f"Task with id {false_uuid_prefix}{first_task['id']} not found"}


@pytest.mark.parametrize("false_uuid_prefix, expected_status_code, task_exist",
                         [("", 202, True),
                          ("abrakadabra", 404, False,),]
                         )
@pytest.mark.asyncio
async def test_delete_task(async_client, first_task, false_uuid_prefix, expected_status_code, task_exist):
    response = await async_client.delete(f"/task/{false_uuid_prefix}{first_task['id']}")
    assert response.status_code == expected_status_code
    if task_exist:
        assert response.json() == {"detail": f"Task with id {first_task['id']} successfully deleted"}
    else:
        assert response.json() == {"detail": f"Task with id {false_uuid_prefix}{first_task['id']} not found"}


@pytest.mark.parametrize("false_uuid_prefix, expected_status_code, task_exist",
                         [("", 202, True),
                          ("abrakadabra", 404, False,),]
                         )
@pytest.mark.asyncio
async def test_update_task(async_client, first_task, update_data, false_uuid_prefix, expected_status_code, task_exist):
    response = await async_client.put(f"/task/{false_uuid_prefix}{first_task['id']}", json=update_data)
    assert response.status_code == expected_status_code
    if task_exist:
        assert response.json() == {"detail": f"Task with id {first_task['id']} successfully updated"}
    else:
        assert response.json() == {"detail": f"Task with id {false_uuid_prefix}{first_task['id']} not found"}

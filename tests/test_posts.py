from app import schemas


def test_get_all_post(client, test_create_post):
    res = client.get("/posts")
    print(res.json())
    assert res.status_code == 200

def test_unauthorized_create_post(client):
    res = client.post("/posts", json={"title": "Harry Potter", "content":"A story created by JK Rowling"})
    print(res.json())
    assert res.status_code == 401


def test_get_one_post(authorized_client,test_create_post):
    res = authorized_client.get("/posts/1")
    print(res.json())
    assert res.status_code == 200




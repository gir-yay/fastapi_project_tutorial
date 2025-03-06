from app import schemas


def test_unauthorized_create_post(client):
    res = client.post("/posts", json={"title": "Harry Potter", "content":"A story created by JK Rowling"})
    print(res.json())
    assert res.status_code == 401

def test_create_post(authorized_client):
    res = authorized_client.post("/posts", json={"title": "Harry Potter", "content":"A story created by JK Rowling"})
    print(res.json())
    assert res.status_code == 201



def test_get_all_post(client):
    res = client.get("/posts")
    print(res.json())
    assert res.status_code == 200
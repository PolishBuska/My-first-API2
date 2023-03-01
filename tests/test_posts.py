from typing import List
from fastapi import status
import pytest

from app import schemas
def test_get_all_posts(authorized_client,test_posts):
    res = authorized_client.get("/posts/")
    def validate(post):
        return schemas.PostOut(**post)
    posts_map = list(map(validate,res.json()))
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client,test_posts):
    res = authorized_client.get(f'/posts/888888')
    assert res.status_code == 404

def test_get_one_post(authorized_client,test_posts):
    res = authorized_client.get(f'/posts/{test_posts[0].id}')
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content

@pytest.mark.parametrize('title, content, published', [
    ("awesome",'tea',True),
    ("awesome2",'tea2',False),
    ("awesome3",'tea3',True)
])
def test_create_post(authorized_client,test_user,test_posts,title,content,published):
    res = authorized_client.post('/posts',json={"title":title,"content":content,"published":published})
    create_schema = schemas.Post(**res.json())
    assert res.status_code == 201
    assert  create_schema.title == title
    assert create_schema.content == content
    assert create_schema.published == published
    assert create_schema.owner_id == test_user["id"]

def test_create_post_default_published_true(authorized_client,test_posts,test_user):
    res = authorized_client.post('/posts', json={"title": "111", "content": "1"})
    create_schema = schemas.Post(**res.json())
    assert create_schema.published == True

def test_unauthorized_user_create_post(client, test_posts):
    res = client.post('/posts', json={"title": "111", "content": "1"})
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401

def test_delete_post_success(authorized_client,test_user,test_posts):
    res_estimate= authorized_client.get(f'/posts')
    res = authorized_client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == 204
    assert len(res_estimate.json()) == len(test_posts)

def test_delete_none_post(authorized_client,test_user,test_posts):
    res_estimate= authorized_client.get(f'/posts')
    res = authorized_client.delete(f'/posts/1000000000000')
    assert res.status_code == 404
    assert len(res_estimate.json()) == len(test_posts)

def test_delete_wrong_owner(authorized_client,test_user,test_posts,test_user_2):
    res_estimate = authorized_client.get(f'/posts')
    res = authorized_client.delete(f'/posts/{test_posts[2].id}')
    assert res.status_code == 403
    assert len(res_estimate.json()) == len(test_posts)

def test_update_post(authorized_client,test_user,test_posts):
    data = {
        "title":"update 1",
        "content":"update",
        "id":test_posts[0].id
    }
    res = authorized_client.put(f'/posts/{test_posts[0].id}',json=data)
    post_update = schemas.Post(**res.json())
    res_estimate = authorized_client.get(f'/posts')
    assert  res.status_code == status.HTTP_200_OK
    assert  post_update.title == data['title']
    assert  post_update.content == data['content']
    assert len(res_estimate.json()) == len(test_posts)

def test_update_none_post(authorized_client,test_user,test_posts):
    data = {
        "title":"update 1",
        "content":"update",
        "id":test_posts[0].id
    }
    res = authorized_client.put(f'/posts/31513513513',json=data)
    res_estimate = authorized_client.get(f'/posts')
    assert  res.status_code == status.HTTP_404_NOT_FOUND
    assert len(res_estimate.json()) == len(test_posts)

def test_unauthorized_user_update_post(client, test_posts):
    res = client.put(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401


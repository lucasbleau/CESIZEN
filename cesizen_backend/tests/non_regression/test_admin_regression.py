def test_admin_route_redirect_anonymous(client):
    r = client.get("/admin/", follow=False)
    assert r.status_code == 302

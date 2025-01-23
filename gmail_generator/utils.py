async def format_proxy(proxy: str) -> dict:
    server_port, username_password = proxy.split('@')
    server, port = server_port.split(':')
    user, password = username_password.split(':')
    proxy = {
        "server": f"http://{server}:{port}",
        "username": user,
        "password": password,
    }
    return proxy



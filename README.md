# Unix Socket Server
A single-threaded server for serving in-memory files via Unix sockets. No Requirements. just clone this repo and copy ```unix_socket_server``` module to the root of your project or install package using pip:
```bash
pip install unix-socket-server
```

## Problem
Imagine that we have a in-memory file in our Python application and we want to share this file with other apps or tools on the same host without writing it to disk.

## Solution
A lightweight solution to this problem is to use Unix socket communication for file sharing.


## Examples:

Use a context manager that automatically manages the server lifecycle:
```python
from unix_socket_server import UnixSocketServerContext

with UnixSocketServerContext(b'hello world', '/tmp/file.sock') as server:
    """
        do stuff
    """
```

Or you can create and start the server manually.
```python
server = UnixSocketServer(b'Hello World')
server.listen('/tmp/stream.socket')
```

```UnixSocketServer``` writes file to response stream by default . but if your client needs http protocol you can use http handler like example below:
```python
from unix_socket_server import UnixSocketServerContext
with open('./file-exmaple.txt', 'rb') as f:
    """
    UnixSocketServer also accepts readable io objects
    """
    with UnixSocketServerContext(f, '/tmp/file.sock', handler='http') as server:
        """
            do stuff
            dummy example:
                transport = httpx.HTTPTransport(uds=server.uri)
                client = httpx.Client(transport=transport)
                response = client.get('http://any_path/')
                assert response.status_code == 200
        """
```
import socket
from status import set_status
from temp import get_temp
import json

def read_html():
    f = open("index.html", "r")
    html = f.read()
    f.close()
    return html

def write_msg(msg):
    msgs = read_msgs()
    f = open("msgs.txt", "w")

    msg = msg.replace("%20", " ")
    msgs["items"].append(msg)

    if len(msgs["items"]) > 10:
        msgs["items"] = msgs["items"][-10:]

    f.write(json.dumps(msgs))
    f.flush()
    f.close()

def read_msgs():
    try:
        f = open("msgs.txt", "r+")
        content = f.read()
        print(content)
        f.close()
        msgs = json.loads(content)
        return msgs
    except Exception  as e:
        print(e)
        return json.loads('{"items":[]}')

def run_webserver():
    print('Starting web server...')
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]  # type: ignore
    server = socket.socket()   # type: ignore
    server.bind(addr)
    server.listen(1)
    print('Server Listener on ', addr)

    set_status(True)

    while True:
        try:
            conn, addr = server.accept()
            print('New HTTP-Request from ', addr)
            request = str(conn.recv(1024)).split('\\r\\n')
            request = request[0].split(' ')

            if len(request) > 1:
                path = request[1].lstrip('/')
                print('Request:', path)

                if path.startswith("msg:"):
                    value = path.lstrip("msg:")
                    value = value.strip()

                    if len(value) > 0:
                        write_msg(value)

            msgs = ""
            for item in read_msgs()["items"]:
                msgs = "<p>-> <b>" + item + "</b></p><hr>" + msgs

            response = read_html().replace("#MSGS#", msgs)
            response = response.replace("#TEMP#", str(get_temp()))
            conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            conn.send(response)
            conn.close()
            print('HTTP-Response handled')
        except OSError as e:
            break
        except (KeyboardInterrupt):
            break

        try: 
            conn.close()   # type: ignore
        except NameError: 
            pass

    server.close()
    print('Web server stopped')
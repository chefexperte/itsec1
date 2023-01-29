from telnetlib import Telnet
from time import sleep

host = "it-sec-challenge.urz.uni-heidelberg.de"
port = 10002
timeout = 100

col1 = bytes.fromhex("a6af943ce36f0cf4adcb12bef7f0dc1f526dd914bd3da3cafde14467ab129e640b4c41819915cb43db752155ae4b895fc71b9b0d384d06ef3118bbc643ae6384")
col2 = bytes.fromhex("a6af943ce36f0c74adcb122ef7f0dc1f526dd914bd3da3cafde14467ab129e640b4c41819915cb43db752155ae4b895fc71b9a0d384d06ef3118bbc643ae6384")

# enter your mail here
user = input("Enter your Mail: ")
wait_time = 0.2


# wait, send message, append linebreak
def send(tn: Telnet, msg: bytes):
    sleep(wait_time)
    tn.write(msg + b"\n")


# run the main script
def run():
    with Telnet(host, port, timeout) as tn:
        send(tn, user)
        send(tn, b"2")
        send(tn, b"changelog")
        send(tn, col1)
        send(tn, b"2")
        send(tn, b"top_secret")
        send(tn, col2)
        send(tn, b"4")
        send(tn, col1)
        result = tn.read_until(b"------END CONTENT------", timeout=3).decode("utf-8").split("\n")[-2]
        print(result)


if __name__ == '__main__':
    run()

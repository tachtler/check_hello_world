# check\_hello\_world.py

A basic nagios/icinga check plugin for demonstration purpose.

```
# pip install -i https://test.pypi.org/simple/ check-hello-world
```

### Aufrufbeschreibung:

```
# /usr/lib/nagios/plugins/check_hello_world -h
```

### Beispiel-Aufrufe:

 1.	```/usr/lib/nagios/plugins/check_hello_world -a 0.50 -w @0.80:0.89 -c @0.90   [OK]```
 2.	```/usr/lib/nagios/plugins/check_hello_world -a 0.85 -w @0.80:0.89 -c @0.90   [WARNING]```
 3.	```/usr/lib/nagios/plugins/check_hello_world -a 1.00 -w @0.80:0.89 -c @0.90   [CRITICAL]```

## Link

[TestPyPI - check-hello-world](https://test.pypi.org/project/check-hello-world/ "Test Python package publishing with the Test Python Package Index")

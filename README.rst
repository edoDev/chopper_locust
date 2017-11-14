Load Tests for Chopper
======================

Load tests for Chopper using locust.


Running Chopper
---------------

The easy way is to grab the container and run it, e.g.::

    docker pull tingold/sc:0.0.18
    docker run -p 8000:8000 tingold/sc:0.0.18

To check up on things, you can hit https://localhost:8000/demo

(This serves https. If you use http you might get confused. Use https.)

Now you are ready to point locust at "https://localhost:8000"
or whatever host you have this listening on.


Cert Setup
----------

Chopper's demo config ships with a self-signed certificate. For this reason,
locust is not checking certificates. You should not need to do anything about
this unless you want locust to check certificates. If you enabled checking and
it wasn't set up right, you could see this in chopper's log::

    2017/11/14 21:35:46 http: TLS handshake error from 172.17.0.1:41462: remote
    error: tls: unknown certificate authority


Dockerfile
----------

The provided dockerfile lets you run the locust tests from a docker container.
Internally it just uses `install_locust.sh` and `run_locust.sh`.

Build the image with e.g.::

    docker build -t chopper_locust .

Run it with::

    docker run -p 8089:8089 -it chopper_locust

If you want to pass a different URL to test against, use::

    URL="http://example.com"
    docker run -p 8089:8089 --env URL="$URL" -it chopper_locust



install_locust.sh
-----------------

This bash script sets up locust inside a virtualenv for you.

You shouldn't have to know anything about python and many of the recent
linux distributions will work (see the source for details).

If you do know what you're doing and you run it inside a virtualenv, it should
work in that virtualenv (subject to the limitations of what Python version that
virtualenv has).

Otherwise the script looks for a virtualenv at `~/locust_env` to use, and
creates it if need be.

If you want the script to install Python or virtualenv for you, run it with
sudo or root permissions so it can install distro packages.


run_locust.sh
-------------

If you are in an environment where `install_locust.sh` ran 
(e.g. you ran it on your laptop and you are in your laptop shell,
or you ran it in a docker container and you are in a shell in that container)
then you can use `run_locust.sh` to run the Locust server, which provides
a web interface on port 8089.

The script needs you to specify a URL to run against, passed either as the
first argument or in an environment variable named `URL`. e.g.::

    ./run_locust.sh "https://example.com"

If you are running chopper locally as pre the above instructions (not a great
way to get accurate numbers), that's::

    ./run_locust.sh "https://localhost:8000"

When Locust's web interface is running, you can access that at::

    http://127.0.0.1:8089/

If there are any obvious errors, they should show up on stdout/stderr.

If you want more detailed logging, edit run_locust.sh e.g. changing::

    LOGLEVEL=CRITICAL

to::

    LOGLEVEL=DEBUG

(That would give you apache-style lines for each outgoing request,
at the obvious performance penalty)


Headless
---------

Locust doesn't need to be run with the interface if you prefer to do it in
batch mode.

If you want to run this headless, see `locust --help`, but here's an example::

    env/bin/locust --no-web --clients=2 --hatch-rate=1


Distributed
-----------

If you want to run distributed tests, see `locust --help` and the locust manual

Here's a simple example on one host (this can be used to apply multiple
cores simply)::

    locust -f ./code/tile_tester.py --master --host "$URL" &
    locust -f ./code/tile_tester.py --slave --host "$URL" &

There is another flag if the master is on a different host

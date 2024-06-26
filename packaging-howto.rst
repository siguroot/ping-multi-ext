Documentation
*************

https://packaging.python.org/guides/distributing-packages-using-setuptools/

Update version
**************

.. code-block:: bash

    vi ping_multi_ext/__init__.py

Test pip package locally
************************

.. code-block:: bash

    export PKG_GIT_PATH=xxx/ping-multi-ext
    export REMOTE_HOST=xxx

    cd /tmp
    rm -rf ping-multi-ext-inst/
    mkdir ping-multi-ext-inst/
    python3 -m venv ping-multi-ext-inst/

    cd ping-multi-ext-inst/
    . bin/activate
    pip -qq install --upgrade pip wheel
    pip -qq install "$PKG_GIT_PATH"

    # keep the following instructions in-sync with "Test pip package from PyPi repo"

    which ping-multi | grep -q "$(pwd)/bin/" || echo ERROR
    which ping-raw-multi | grep -q "$(pwd)/bin/" || echo ERROR

    ping-multi google.com "google.com@$REMOTE_HOST" "2620:12e:1000::a00:f@$REMOTE_HOST"
    ping-raw-multi --ping google.com@local 'ping google.com' --ping google.com@remote "ssh root@$REMOTE_HOST ping google.com" --ping direct_ipv6@remote "ssh root@$REMOTE_HOST ping 2620:12e:1000::a00:f"

Upload package to PyPi
**********************

.. code-block:: bash

    . bin/activate

    pip -qq install --upgrade pip wheel twine setuptools build

    python -m build >/dev/null
    rm -r ping_multi_ext.egg-info/

    VER="$(python -c 'import ping_multi_ext; print(ping_multi_ext.version)')"
    DIST_FILES="$(find -name "ping?multi?ext-$VER*")"
    echo $VER :: $DIST_FILES

    twine check $DIST_FILES
    twine upload $DIST_FILES

    git add $DIST_FILES
    git status
    git diff ping_multi_ext/__init__.py
    git commit $DIST_FILES ping_multi_ext/__init__.py
    git push

Test pip package from PyPi repo
*******************************

.. code-block:: bash

    export REMOTE_HOST=xxx

    cd /tmp
    rm -rf ping-multi-ext-inst/
    mkdir ping-multi-ext-inst/
    python3 -m venv ping-multi-ext-inst/

    cd ping-multi-ext-inst/
    . bin/activate
    pip install --no-cache-dir ping-multi-ext

    # keep the following instructions in-sync with "Test pip package locally"

    which ping-multi | grep -q "$(pwd)/bin/" || echo ERROR
    which ping-raw-multi | grep -q "$(pwd)/bin/" || echo ERROR

    ping-multi google.com "google.com@$REMOTE_HOST" "2620:12e:1000::a00:f@$REMOTE_HOST"
    ping-raw-multi --ping google.com@local 'ping google.com' --ping google.com@remote "ssh root@$REMOTE_HOST ping google.com" --ping direct_ipv6@remote "ssh root@$REMOTE_HOST ping 2620:12e:1000::a00:f"

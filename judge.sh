docker run --rm \
  --mount type=bind,source=$(pwd)/tmp/in.txt,target=/judge/stdin,readonly \
  --mount type=bind,source=$(pwd)/tmp/out.txt,target=/judge/userout \
  --mount type=bind,source=$(pwd)/tmp/err.txt,target=/judge/usererr \
  --mount type=bind,source=$(pwd)/tmp/return.txt,target=/judge/return \
  --mount type=bind,source=$(pwd)/tmp/code.py,target=/judge/code.py,readonly \
  -m 256M --memory-swap 256M \
  judge-python

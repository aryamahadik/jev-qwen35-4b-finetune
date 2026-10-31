#!/bin/bash
# One cheap diagnostic on od-sbx1 (runs as root via sudo). Fixed literal programs only, nothing generated.
# Part 1: read the Go source rule inside the od-sbx go image. Part 2: one container with the executor's flags, same Go fixture
# (go.mod at /work, empty vendor/modules.txt, seeded GOCACHE), run with TMPDIR=/work (current) and TMPDIR=/work/.tmp (proposed).
set -u
IMG=$(python3 -I -c 'import json;print(json.load(open("/opt/od-sbx/IMAGE_MANIFEST.json"))["toolchains"]["go"]["image_id"])')
echo "go image id: $IMG"
RUN=(docker run --rm -i --runtime runsc --network none --ipc none --read-only --cap-drop ALL --security-opt no-new-privileges
     --pids-limit 256 --memory 1g --memory-swap 1g --cpus 1 --user 65534:65534 --hostname od-sbx --workdir /work --pull never
     --log-driver none --tmpfs /work:rw,exec,nosuid,nodev,size=512m,uid=65534,gid=65534,mode=0700
     --env TZ=UTC --env LANG=C.UTF-8 --env GOFLAGS=-mod=vendor --env GOPROXY=off --env GOTOOLCHAIN=local --env GOCACHE=/work/.gocache)

echo "##### PART 1: Go source, system temp root rule (modload/init.go)"
"${RUN[@]}" "$IMG" sh -c 'cd /usr/local/go/src/cmd/go/internal/modload && grep -n "system temp root" init.go; go version' </dev/null

echo "##### PART 2: same fixture, TMPDIR=/work vs TMPDIR=/work/.tmp"
"${RUN[@]}" "$IMG" sh -s <<'EOS'
set -u
printf 'module det\n\ngo 1.26\n' > go.mod
mkdir -p vendor .tmp
: > vendor/modules.txt
printf 'package det\n\nfunc Add(a, b int) int { return a + b }\n' > add.go
cat > add_test.go <<'EOT'
package det

import (
	"os"
	"path/filepath"
	"testing"
)

func TestAdd(t *testing.T) {
	if Add(1, 2) != 3 {
		t.Fatal("add")
	}
	if err := os.WriteFile(filepath.Join(t.TempDir(), "x"), []byte("x"), 0o600); err != nil {
		t.Fatal(err)
	}
}
EOT
mkdir -p cmd && printf 'package main\nimport ("fmt";"os")\nfunc main(){ fmt.Println(1+2, "ok", os.TempDir()) }\n' > cmd/m.go
mkdir -p .gocache && cp -R /opt/gocache-seed/. .gocache/
for T in /work /work/.tmp; do
  echo "=== TMPDIR=$T"
  export TMPDIR=$T
  echo "--- go env GOMOD"; go env GOMOD
  echo "--- go run ./cmd"; go run ./cmd; echo "rc=$?"
  s=$(date +%s)
  echo "--- go test -count=1 ./..."; go test -count=1 ./... ; echo "rc=$?"
  echo "elapsed_s=$(( $(date +%s) - s ))"
done
EOS
echo "##### leftover containers: $(docker ps -aq | wc -l)"

# F-GO1 skeptic, pass 2 (re-check): SOUND for code and tests, one REQUIRED fix to the rebuild notes - Sun 18 Oct 2026

FILING NOTE (builder): this file is a SUMMARY written by the builder from the coordinator's relayed message. The skeptic's own text was not available to the
builder. If the verbatim report is wanted here, paste it over this file. Nothing below goes beyond what the coordinator relayed.

Subject: the revised fix (`_reject_reserved`, 37 executor tests, executor tree hash `defbb2e49ae9589fc82b2c53d988b70ccedf7e9c0c226d7de38e47ee6eefa753`).

## Verdict
SOUND for the code and the tests: D1 and D1b are closed, the mutations are caught, S1 is unchanged, and the tree hash `defbb2e4...` was confirmed.

## One REQUIRED fix before the rebuild (IMAGE_RECIPE.md 10.5, rebuild note step 1)
`docker ps -aq --filter label=od-sbx=1 | xargs -r docker rm -f` has no `sudo`. The docker group is empty, so as the login user it removes nothing, and leftover self-test containers would be baked
into the image (ST-4.1). Use `sudo /opt/od-sbx/bin/od-sbx cleanup` or `sudo sh -c 'docker ps -aq --filter label=od-sbx=1 | xargs -r docker rm -f -v'`.
Minor: use `sudo rm -rf /home/*/sandbox /home/*/buildlogs /home/*/manifest_copy.json`, and create `/tmp/buildlogs` first.

## Resolution (builder)
Rebuild notes fixed as asked (check `sudo docker ps -aq | wc -l` prints 0), then the rebuild was ordered and done: `od-sbx-base-20261018-r2`, self-test 46/46, BUILD_RECORD.md section 8.
The cleanup found 0 leftover containers on that boot (the self-test had finished and failed on its own before it was stopped).

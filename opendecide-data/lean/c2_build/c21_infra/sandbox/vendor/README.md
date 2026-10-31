requirements.lock is created by `build/30_fetch_toolchains.sh resolve` (-> requirements.proposed.txt), reviewed by the
skeptic (who re-resolves independently and compares hashes against PyPI), then copied to requirements.lock when the
pins are FROZEN. Format: one `name==version --hash=sha256:<hex>` per line. The wheels themselves are not committed;
they are downloaded on the build VM with --require-hashes.

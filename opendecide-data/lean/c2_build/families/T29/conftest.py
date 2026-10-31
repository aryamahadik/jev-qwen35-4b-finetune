"""pytest: the _backup_* folders hold earlier iterations (their tests pin earlier text); never collect them."""
collect_ignore_glob = ["_backup*", "pilot*", "haiku"]

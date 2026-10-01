def pytest_configure(config):
    config.addinivalue_line("markers", "slow: the L4-sequence simulation (gate_4b_l4.sh vm-job1 + teacher_switch_l4.sh)")

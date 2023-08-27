import launch

if not launch.is_installed("openpyxl"):
    launch.run_pip("install openpyxl==3.1.2", "requirements for prompt rp")
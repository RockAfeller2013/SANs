- rename_mp4.py scans the directory and renames the file.mp4 based on its current directory name.
- create.py scans the current directory and then creates a simple LMS to play videos with previous and next and based on the folder names as navigation

wget --spider --recursive --no-parent https://dl.liangroup.net/ 2>&1 | grep -i 'Length:' | awk '{sum += $2} END {print sum/1024/1024 " MB"}'
wget --limit-rate=500k --wait=1 --recursive --no-parent --continue --tries=0 --timeout=30 --read-timeout=400 https://dl.liangroup.net/SANS/
wget --wait=1 --recursive --no-parent --continue --tries=0 --timeout=30 --read-timeout=400 https://dl.liangroup.net/SANS/

wget --limit-rate=500k --wait=1 --recursive --no-parent --continue --tries=0 --timeout=30 --read-timeout=30 'https://dl.liangroup.net/SANS/SANS%20-%20FOR508%20-%20Advanced%20Incident%20Response%2C%20Threat%20Hunting%2C%20and%20Digital%20Forensics/'
wget --continue ... https://dl.liangroup.net/SANS/

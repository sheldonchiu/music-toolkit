#%%
from glob import glob
from subprocess import Popen, PIPE
import shlex

root_location = "/mnt/ssd1/music/hiRes"

#%%
files = glob(f"{root_location}/**/*.flac", recursive=True)
# %%
output = []
for file in files:
    args = shlex.split(f'flac -t "{file}" ')
    cmd = Popen(args, stdout=PIPE, stderr=PIPE, shell=False)
    stdout, stderr = cmd.communicate()
    if 'ok' not in stderr.decode('utf8'):
        output.append(file)

with open('output.txt', 'w') as file:
    for text in output:
        file.write(text)
# %%

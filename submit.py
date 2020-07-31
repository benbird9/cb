import git #pip install git-python
from datetime import datetime
import os
TODAY = datetime.today().strftime('%Y-%m-%d')

repo = git.Repo('\\src\cb')
git = repo.git
#git.execute('git fetch origin master')
#git.execute('git reset --hard origin/master')

# os.chdir('\\workdir_yuqi\git_src\cb')
# os.system('python SortBySumOfPrinceAndPremium.py')
import subprocess
result = subprocess.check_output('python SortBySumOfPrinceAndPremium.py', shell=True, cwd='\\src\cb')


git.execute('git add -A')
git.execute('git commit -m "'+ TODAY  + '"')
git.execute('git push')
import git
from datetime import datetime
import os
TODAY = datetime.today().strftime('%Y-%m-%d')

repo = git.Repo('\\a_yu_workdir\project\sourcecode\cb')
git = repo.git
# git.execute('git fetch origin master')
# git.execute('git reset --hard origin/master')

os.chdir('\\a_yu_workdir\project\sourcecode\cb')
os.system('python SortBySumOfPrinceAndPremium.py')

git.execute('git add -A')
git.execute("git commit -m " + TODAY)
git.execute('git push')
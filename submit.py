import git
from datetime import datetime
import os
TODAY = datetime.today().strftime('%Y-%m-%d')

os.system('python SortBySumOfPrinceAndPremium.py')

repo = git.Repo('\\a_yu_workdir\project\sourcecode\cb')
git = repo.git
git.execute('git add -A')
git.execute("git commit -m '" + TODAY +"'")
git.execute('git push')
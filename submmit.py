import git
repo = git.Repo('./')
print repo.git.status()
# add a file
print repo.git.add( 'somefile' )
# commit
print repo.git.commit( m='my commit message' )
# now we are one commit ahead
print repo.git.status()
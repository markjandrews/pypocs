import os
import sys
import shutil
import pygit2
from pygit2.credential import AuthMethods

artefact_dir = os.path.join(os.path.dirname(__file__), 'artefacts', 'main')


def main(argv):

    if os.path.exists(artefact_dir):
        shutil.rmtree(artefact_dir)

    os.makedirs(artefact_dir)

    repo = pygit2.Repo.init(artefact_dir)
    cred = pygit2.Cred(methods=[AuthMethods.agent, AuthMethods.key])
    remote = repo.remote_create('origin', 'git@github.com:markjandrews/libgit2.git', cred)
    default_branch = remote.default_branch()

if __name__ == '__main__':
    main(sys.argv[1:])

# CFISmodulGit

Introductory module to Git and Version Control Systems 2021.

## Git cheat sheet (simplified from Carles Araguz at NanoSatLab)
Below you'll find a list of some of the most common `git` commands. Two neat and comprehensive cheat sheets can be found [here](https://www.atlassian.com/dam/jcr:8132028b-024f-4b6b-953e-e68fcce0c5fa/atlassian-git-cheatsheet.pdf) and [here](https://services.github.com/on-demand/downloads/github-git-cheat-sheet.pdf).
* `git add <file>`: add a file. Option `-v` enables verbosity.
* `git add . -u`: adds all changed files to the staging area. Files that have not been previously added to the tree are not included. The `.` is the location from which files will be looked for (recursively). Parent folders are not affected.
* `git rm <file>`: removes a file from the repo.
* `git rm <file> --cached`: removes a file from the repo and keeps a local copy.
* `git reset`: undoes staging (i.e. `add`) for all files.
* `git reset --hard`: undoes staging (i.e. `add`) for all files and overwrites all files with the ones in the previous commit.
* `git commit -m "Message"`: Creates a new commit with the given message. This records a new "snapshot" with all the previously added changes.
* `git commit -am "Message"`: Creates a new commit with the given message for all the changed files. This is equivalent to `git add . -u && git commit -m "Message"`.
* `git checkout <branch_name>`: switches to a different branch.
* `git branch <branch_name>`: creates a new branch.
* `git branch -a`: shows all branches.
* `git pull origin <branch_name>`: synchronizes a branch with its remote counterpart (does merge).
* `git pull origin <branch_name> --rebase`: synchronizes a branch with its remote counterpart (does rebase).
* `git push origin <branch_name>`: synchronizes a local branch with its remote counterpart.
* `git status`: shows current git status.
* `git log`: shows the list of commits.
* `git merge <branch_name>`: merges `<branch_name>` into the current branch.
* `git rebase <branch_name>`: rebases the current branch with the commits in `<branch_name>`.
* `git config --global alias.<alias_name> "<alias_command_expansion>"`: creates a new alias.

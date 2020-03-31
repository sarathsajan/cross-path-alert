> If you are a total noob... skip these steps and go to the [resources](#resources).

---

## Instructions to teammates

1. Fork this repository.

2. Clone local branches.<br>
`$ git clone git://your_branch.git` (use either `git://` or `https://` protocol)

3. Then, you can work locally on your branch. When you are ready to with changes, push it to your respective GitHub reporsitories.<br>
`$ git push -u origin your_branch/fork`

3. Create a pull request, with **base repository** as `sarath sajan/cross-path-alert` & **head repository** as `your fork/patch` with changes (see the sceenshot below as an example).<br><br>
![example](https://i.stack.imgur.com/qRsge.png)

4. In case you lag and want to be even with master (your's / mine) branch.<br>
`$ git pull --rebase origin master`

---

## Resources

### Must read ["Pro Git" by Scott Chacon](http://git-scm.com/book)

### 1. [The Workflow Cheat Sheet](https://towardsdatascience.com/a-simple-git-workflow-for-github-beginners-and-everyone-else-87e39b50ee08)

>Common console commands:<br>
`cd` - change directory<br>
`mkdir` - make directory<br>
`ls` - view the files/folders in directory<br>

>NOTE: Exit VIM if needed <kbd>ctrl</kbd> + <kbd>c</kbd> then type `:qa!` and push enter<br>
NOTE: If file is not in local repo, manually move the file into the correct folder (outside of console)<br><br>
>--------------------------------------------<br>
 Managing your Local Repo<br>
>--------------------------------------------<br><br>
NOTE: If you need to hard reset your local repo to match the remote master use the following commands:<br>
`$ git fetch origin`<br>
`$ git reset --hard origin/master`<br>
Undo the act of committing, leaving everything else intact:<br>
`$ git reset --soft HEAD^:`<br>
Undo the act of committing and everything you'd staged, but leave the work tree (your files intact):<br>
`$ git reset HEAD^`<br>
Completely undo it, throwing away all uncommitted changes, resetting everything to the previous commit:<br>
`$ git reset --hard HEAD^`<br><br>
>--------------------------------------------<br>
BEGIN WORKFLOW<br>
>--------------------------------------------<br><br>
>- Clone the Repo to local machine:<br>
`$ git clone https://github.com/user_name/repo_name.git`<br>
>- Make sure the local master is up-to-date:<br>
`$ git pull origin` master<br>
>- Create new branch:<br>
`$ git banch branch_name` <br>
>- Move to branch:<br>
`$ git checkout branch_name`<br>
>- Navigate file structure as needed:<br>
`$ ls`<br>
`$ cd folder_name`<br>
>- Add the files to the branch:<br>
`$ git add filename`<br>
>- Verify file:<br>
`$ git status`<br>
>- Commit the files:<br>
`$ git commit -m "comment"`<br>
>- Add branch and files to the Remote Repo:<br>
`$ git push -u origin branch_name`<br>
>- Go to the github website to manage pull request and merge.<br>
>- Switch back to local master so you can delete the local branch:<br>
`$ git checkout master`<br>
>- `Delete local branch:`<br>
`$ git branch -d branch_name`<br>
OR<br>
`$ git branch -D branch_name`<br>
>- If you don't want to go to the website, you can merge your branch to the master locally and push the new master to the remote repo:<br>
>- Switch back to master branch:<br>
`$ git checkout master`<br>
>- Merge the branch with the local master:<br>
`$ git merge branch_name -m "comment"`<br>
>- Push the local master to the remote master:<br>
`$ git push origin master`<br>
>- Delete local branch:<br>
`$ git branch -d branch_name`<br>
OR<br>
`$ git branch -D branch_name`<br>

### 2. [How to add license to an existing GitHub project](https://stackoverflow.com/questions/31639059/how-to-add-license-to-an-existing-github-project)
### 3. [How to push a new folder (containing other folders and files) to an existing git repo?](https://stackoverflow.com/questions/15612003/how-to-push-a-new-folder-containing-other-folders-and-files-to-an-existing-git)
### 4. [How do I undo the most recent local commits in Git?](https://stackoverflow.com/questions/927358/how-do-i-undo-the-most-recent-local-commits-in-git)
### 5. [Is there any Github GUI Client for Linux OS?](https://stackoverflow.com/questions/15398229/is-there-any-github-gui-client-for-linux-os)
### 6. [git error: failed to push some refs to](https://stackoverflow.com/questions/24114676/git-error-failed-to-push-some-refs-to)
### 7. [Remove file in 'changes not staged for commit`](https://stackoverflow.com/questions/13203008/remove-file-in-changes-not-staged-for-commit)
### 8. [How can I keep my fork in sync without adding a separate remote?](https://stackoverflow.com/questions/20984802/how-can-i-keep-my-fork-in-sync-without-adding-a-separate-remote/)
### 9. [Make the current Git branch a master branch](https://stackoverflow.com/questions/2763006/make-the-current-git-branch-a-master-branch)
### 10. [How to remove remote origin from Git repo](https://stackoverflow.com/questions/16330404/how-to-remove-remote-origin-from-git-repo)
### 11. [What are the git concepts of HEAD, master, origin?](https://stackoverflow.com/questions/8196544/what-are-the-git-concepts-of-head-master-origin)
### 12. [In git, what is the difference between merge --squash and rebase?](https://stackoverflow.com/questions/2427238/in-git-what-is-the-difference-between-merge-squash-and-rebase)
### 13. [How can I determine the URL that a local Git repository was originally cloned from?](https://stackoverflow.com/questions/4089430/how-can-i-determine-the-url-that-a-local-git-repository-was-originally-cloned-fr)

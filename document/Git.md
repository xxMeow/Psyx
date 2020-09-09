# Git

### Reset Author Time & Commit Time

```bash
export GIT_COMMITTER_DATE="Sun Aug 30 17:11:52 2020 +0900"
git commit --amend --no-edit --date="Sun Aug 30 17:11:52 2020 +0900"
```

- Author Time: 改次commit修改的时间，一条amend就能改
- Commit Time: 实际执行commit命令的时间，必须通过设置环境修改
- Github的小绿格是按照Author Time来的，但是项目页面的commit时间线则是按照Commit Time显示的

#### 穿越时空去修改以前的记录

- 当前工作区必须完全没有任何未保存的变动

- 从当前HEAD开始倒退12条commit

    ```bash
    $ git rebase -i HEAD~12
    ```

    但是这样的倒退最多只能修改到正数的第二条，要修改首次commit，必须使用`--root`参数来代替数字

    ```bash
    $ git rebase -i --root
    ```

- 执行倒退命令会自动打开vim，按照要求修改所有想要重写的commit前面的命令，`:wq`保存退出

- 现在就相当于回到了指定的commit刚刚提交的时间点，可以通过`git commit --amend`来修改了

- 修改好之后执行以下命令来继续

    ```bash
    git rebase --continue
    ```

    从最早的一次commit开始，每一次continue都会带你到下一个要修改的commit时间点

    之前vim里修改了几条命令，我们一共就会continue几次

- 最后一次continue会自动结束rebase
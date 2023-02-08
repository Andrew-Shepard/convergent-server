from invoke import task


@task
def db_setup(ctx):
    ctx.run("/app/files/db_init.sh")


@task
def style(ctx):
    ctx.run("black --check .")


@task
def test(ctx):
    ctx.run(f"coverage run --source convergent -m pytest tests --color=yes")


@task
def suite(ctx):
    print("**BLACK**")
    style()
    print("**DB SETUP**")
    db_setup()
    print("**TEST**")
    test()

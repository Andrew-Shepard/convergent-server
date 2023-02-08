from invoke import task


@task
def db_setup(ctx):
    ctx.run("bash /app/utility/db_init.sh")


@task
def style(ctx):
    ctx.run("black --check .")


@task
def test(ctx):
    ctx.run("pytest tests --color=yes")


@task
def suite(ctx):
    print("**BLACK**")
    style(ctx)
    print("**DB SETUP**")
    db_setup(ctx)
    print("**TEST**")
    test(ctx)

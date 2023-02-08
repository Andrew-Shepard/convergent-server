import sys
import click
import uvicorn
from convergent import settings


@click.command()
@click.option("--reload", is_flag=True)
def main(reload=False):
    kwargs = {"reload": reload}

    uvicorn.run(
        "convergent:app",
        loop="uvloop",
        host=settings.http_host,
        port=settings.http_port,
        log_level="info",
        **kwargs,
    )


if __name__ == "__main__":
    sys.exit(main())

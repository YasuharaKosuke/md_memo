from flask import Markup
from markdown import markdown
from flaskdb.service.mainService import private_dir


def share_read_md(username, file) -> str:
    with open(private_dir(username) + '/' + file + '.md', mode='r') as mdfile:
      mdcontent = mdfile.read()
      return Markup(markdown(mdcontent))


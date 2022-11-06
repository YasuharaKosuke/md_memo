from flask import Markup, session
from markdown import markdown
import os
from flaskdb.service.mainService import private_dir

class memo_MDE:
  mdfile = None
  username = None

  def __init__(self, file=None):
    self.mdfile = file
    self.username = session["username"]

  def write_md(self, data):
    with open(private_dir(self.username) + '/' + self.mdfile + '.md', mode='w') as mdfile:
      mdfile.write(data)

  def read_md(self) -> str:
    with open(private_dir(self.username) + '/' + self.mdfile + '.md', mode='r') as mdfile:
      mdcontent = mdfile.read()
      return Markup(markdown(mdcontent, extensions=['tables']))

  def read_edit_md(self) -> str:
    with open(private_dir(self.username) + '/' + self.mdfile + '.md', mode='r') as mdfile:
      mdcontent = mdfile.read()
      return mdcontent, Markup(markdown(mdcontent, extensions=['tables']))
  
  def delete_md(self):
    os.remove(private_dir(self.username) + '/' + self.mdfile + '.md')

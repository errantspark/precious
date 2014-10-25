import codecs
import datetime
import glob
import os
import re

import bottle
import bottle as app
from bottle import static_file
import misaka as m
import pystache

STATIC_PATH = os.path.abspath(
  os.path.join(os.path.abspath(__file__), '../../assets')
)
BUILD_STATIC_PATH = os.path.abspath(
  os.path.join(os.path.abspath(__file__), '../../build')
)
NOTES_PATH = os.path.abspath(
  os.path.join(os.path.abspath(__file__), '../../notes')
)
TEMPLATE_PATH = os.path.abspath(
  os.path.join(os.path.abspath(__file__),'../../html')
)

loader = pystache.loader.Loader(search_dirs=[TEMPLATE_PATH], extension='html')
renderer = pystache.renderer.Renderer(
  search_dirs=[TEMPLATE_PATH],
  file_extension='html',
  file_encoding='utf8'
)


def yield_notes_by_mtime():
  notes_match = os.path.join(NOTES_PATH, '*.md')
  notes = glob.glob(notes_match)

  cwd = os.getcwd()
  for x in notes:
    if 'conflicted copy' not in x:
      yield os.path.getmtime(os.path.abspath(os.path.join(cwd, x))), x


def get_notes_by_mtime():
  items = reversed(sorted(yield_notes_by_mtime(), key= lambda x: x[0]))

  items = [
      (datetime.datetime.fromtimestamp(int(x)).strftime('%Y-%m-%d %H:%M:%S'), y)
      for x, y in items
  ]
  for x, y in items:
    y = y.replace(NOTES_PATH, '')
    y = y.lower()
    y = y.replace('.md', '')
    y = 'http://localhost:9999/notes' + y
    yield x, y

def render(filename, template, edit=False):
  filename = filename.replace('.', '') # remove periods
  filename = filename.replace(' ', '-')
  filename = filename.replace('/', '-')
  filepath = os.path.join(NOTES_PATH, '%s.md' % (filename, ))

  if not os.path.exists(filepath):
    if edit:
      note = ''
    else:
      bottle.redirect('/edit/%s' % (filename, ))
  else:
    with codecs.open(filepath, 'r', 'utf8') as file_obj:
      note = file_obj.read()

  def replacement(match):
     match_str =  match.groups()[0]
     replace_match = match_str.replace(' ', '-')
     replace_match = match_str.replace('/', '-')

     replace_match = replace_match.replace('.', '')
     return "<a href='/notes/%s'>%s</a>" % (replace_match, match_str)

  if not edit:
   note = re.sub(
      r'\[\[([A-Z \/\.a-z0-9@]+)\]\]',
      replacement,
      m.html(note)
    )

  return pystache.render(loader.load_name(template), {
    'title': ' '.join(x.capitalize() for x in filename.split('-')),
    'filename': filename,
    'content': note
  })

@app.route('/')
def route_home():
  bottle.redirect('/notes/index')

@app.route('/assets/<path:path>')
def serve_static(path):
  return static_file(path, root=STATIC_PATH)

@app.route('/build/<path:path>')
def serve_build_static(path):
  return static_file(path, root=BUILD_STATIC_PATH)


@app.route('/api/dates')
def render_api_dates():
  return {
    'items': list(get_notes_by_mtime())
  }


@app.route('/notes/<filename>')
def render_note(filename):
  return render(filename, 'entry')


@app.route('/edit/<filename>')
def render_note(filename):
  return render(filename, 'entry-edit', edit=True)


@app.route('/edit/<filename>', method='POST')
def handle_note_post(filename):
  data = bottle.request.forms.get('string')
  #import pdb; pdb.set_trace()

  with codecs.open(os.path.join(NOTES_PATH, '%s.md' % (filename, )), 'w', 'utf8') as file_obj:
    file_obj.write(data.decode('utf8'))
  return {'success': True}


webapp = bottle.default_app()
webapp.run(host='0.0.0.0', port=8080)

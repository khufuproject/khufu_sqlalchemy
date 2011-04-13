from paste.script.templates import Template
from paste.util.template import paste_script_template_renderer


class KhufuSQLAlchemyProjectTemplate(Template):
    _template_dir = 'paster_template'
    summary = 'khufu_sqlalchemy starter project'
    template_renderer = staticmethod(paste_script_template_renderer)

from sqlalchemy.schema import CreateTable
from sqlalchemy.ext.compiler import compiles


"""This file makes it so temporary tables drop when added
https://groups.google.com/forum/#!topic/sqlalchemy/GR8T5F8g7cw
"""

# @compiles(CreateTable)
# def check_temporary(create, compiler, **kw):
#     table = create.element
#     ret = compiler.visit_create_table(create)
#     if 'TEMPORARY' in table._prefixes:
#         ret += "ON COMMIT DROP"
#     return ret
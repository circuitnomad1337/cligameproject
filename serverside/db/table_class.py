import serverside.global_vars.ret_messages as ret_mes
import serverside.global_vars.vars as vars




class Table:
    @staticmethod
    def create_table(sql_query):
        """ For sql_query var, look for /DOCS/TableCode.md, there are listed
            all formats used for table creation. Or just do it yourself."""
        
        try:
            vars.CURSOR.execute(sql_query)
            vars.CONNECTION.commit()

            print(ret_mes.SUCCESSFUL_TABLE_CREATION)
            return {"bool": True, 
                    "message": ret_mes.SUCCESSFUL_TABLE_CREATION}

        except Exception as e:
            return {"bool": False,
                    "message": e}



table = Table()
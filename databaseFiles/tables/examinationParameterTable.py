from databaseFiles.database import Database
from databaseFiles.tables.examinationTable import ExaminationTable
class ExaminationParameterTable:
    def __init__(self):
        self.database = Database()


    def add_examination_parameter(self, value, exam_id, parameter_id):
        '''Add a new examination parameter.'''
        connection = self.database.connection_utility()
        cursor = connection.cursor()

        query = "INSERT INTO examination_parameter (value, exam_id, parameter_id) VALUES (?, ?, ?)"
        cursor.execute(query, (value, exam_id, parameter_id))

        connection.commit()
        cursor.close()
        connection.close()


    def get_examination_parameters_by_exam_id(self, exam_id):
        '''Get examination parameters data for the given exam id.
        The order of returned data is: value, parameter_id.'''
        connection = self.database.connection_utility()
        cursor = connection.cursor()

        query = ("SELECT * FROM examination_parameter WHERE exam_id = ?")
        cursor.execute(query, (exam_id,))
        examination_parameter_data = cursor.fetchall()

        parameter_tuple=[]
        for parameter in examination_parameter_data:
            value = parameter[0]
            parameter_id = parameter[2]
            parameter_tuple.append((value, parameter_id))

        cursor.close()
        connection.close()

        return parameter_tuple

    def get_examination_parameters_by_parameter_id(self, parameter_id):
        '''Get examination parameters data for the given parameter id.
        The order of returned data is: value, exam_id.'''
        connection = self.database.connection_utility()
        cursor = connection.cursor()

        query = ("SELECT * FROM examination_parameter WHERE parameter_id = ?")
        cursor.execute(query, (parameter_id))
        examination_parameter_data = cursor.fetchall()

        parameter_tuple = []
        for parameter in examination_parameter_data:
            value = parameter[0]
            exam_id = parameter[1]
            parameter_tuple.append((value, exam_id))

        cursor.close()
        connection.close()

        return parameter_tuple

    def get_examination_parameters(self):
        '''Get all examination data.
        The order of returned data: value, exam_id, parameter_id.'''
        connection = self.database.connection_utility()
        cursor = connection.cursor()

        query = ("SELECT * FROM examination_parameter")
        cursor.execute(query)
        examination_parameters_data = cursor.fetchall()

        return examination_parameters_data

    def join_examination_with_examination_parameters(self, user_id, parameter_id):
        connection = self.database.connection_utility()
        cursor = connection.cursor()

        query = ("SELECT "
                 "  examination_parameter.parameter_id, "
                 "  examination_parameter.value, "
                 "  examination.date "
                 "FROM       examination_parameter "
                 "RIGHT JOIN examination "
                 "      ON examination_parameter.exam_id = examination.id "
                 "WHERE     user_id = ? "
                 "AND       parameter_id = ? "
                 "ORDER BY date(substr(examination.date, 7, 4) ||"
                 "'-' || substr(examination.date, 4, 2) ||"
                 "'-' || substr(examination.date, 1, 2))"
                 )
        cursor.execute(query, (user_id, parameter_id))
        data = cursor.fetchall()

        cursor.close()
        connection.close()

        return data

    def get_parameter_ids(self, user_id):
        connection = self.database.connection_utility()
        cursor = connection.cursor()

        query = ("SELECT DISTINCT"
                 "  examination_parameter.parameter_id "
                 "FROM       examination_parameter "
                 "RIGHT JOIN examination "
                 "      ON examination_parameter.exam_id = examination.id "
                 "WHERE     user_id = ? ")
        cursor.execute(query, (user_id,))
        data = cursor.fetchall()

        # Extracting the parameter ids and filtering out None values
        parameter_ids = [param_id[0] for param_id in data if param_id[0] is not None]

        cursor.close()
        connection.close()

        return parameter_ids


#ep = ExaminationParameterTable()
#print(ep.get_examination_parameters_by_exam_id("1"))
#print(ep.get_examination_parameters_by_parameter_id("1"))
#print(ep.get_examination_parameters())
#print(ep.join_examination_with_examination_parameters(1,1))
#print(ep.get_parameter_ids(1))
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Department, Employee 


class DepartmentObject(SQLAlchemyObjectType):
    class Meta:
        model = Department
        interfaces = (graphene.relay.Node, )


class EmployeeObject(SQLAlchemyObjectType):
    class Meta:
        model = Employee
        interfaces = (graphene.relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # Allows sorting over multiple columns, by default over the primary key
    all_employees = SQLAlchemyConnectionField(EmployeeObject)
    # Disable sorting over this field
    all_departments = SQLAlchemyConnectionField(DepartmentObject, sort=None)

class CreateEmployee(graphene.Mutation):
    class Arguments:
        name_d = graphene.String(required=True)
        name_e = graphene.String(required=True) 

    employee = graphene.Field(lambda: EmployeeObject)

    def mutate(self, info, name_d, name_e):
        department = Department.query.filter_by(name=name_d).first()
        employee = Employee(name=name_e)
        if department is not None:
            employee.department = department
        db_session.add(employee)
        db_session.commit()
        return CreateEmployee(employee=employee)

class Mutation(graphene.ObjectType):
    create_employee = CreateEmployee.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
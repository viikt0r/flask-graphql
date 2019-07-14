import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Department, Employee 


class DepartmentNode(SQLAlchemyObjectType):
    class Meta:
        model = Department
        interfaces = (relay.Node, )


class DepartmentConnection(relay.Connection):
    class Meta:
        node = DepartmentNode


class EmployeeNode(SQLAlchemyObjectType):
    class Meta:
        model = Employee
        interfaces = (relay.Node, )


class EmployeeConnection(relay.Connection):
    class Meta:
        node = EmployeeNode



class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # Allows sorting over multiple columns, by default over the primary key
    all_employees = SQLAlchemyConnectionField(EmployeeConnection)
    # Disable sorting over this field
    all_departments = SQLAlchemyConnectionField(DepartmentConnection, sort=None)

schema = graphene.Schema(query=Query)
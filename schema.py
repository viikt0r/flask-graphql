import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Department, Employee 
from graphql_relay.node.node import from_global_id


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

class CreateDepartment(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    department = graphene.Field(lambda: DepartmentObject)

    def mutate(root, info, name):
        department = Department(name=name)
        db_session.add(department)
        db_session.commit()
        return CreateDepartment(department=department)

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

class UpdateDepartment(graphene.Mutation):
    department = graphene.Field(DepartmentObject)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True) 

    def mutate(self, info, **args):
        name = args.get('name')
        id_ = args.get('id')
        # id = from_global_id(id_)
        department = db_session.query(Department).get(id_) #Department.objects.get(id==id_)
        if department:
            department.name = name
            # department.update(department)
            # record = {'id': id_, 'name': name}
            # department.update('Department', record)
            db_session.commit()
            return UpdateDepartment(department=department)

class DeleteDepartment(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    status = graphene.String()
    
    def mutate(self, info, **args):
        id_ = args.get('id')
        department = db_session.query(Department).get(id_)
        if department: 
            db_session.delete(department)
            db_session.commit()
            return DeleteDepartment(status="OK")

class Mutation(graphene.ObjectType):
    create_employee = CreateEmployee.Field()
    create_department = CreateDepartment.Field()
    update_department = UpdateDepartment.Field()
    delete_department = DeleteDepartment.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
from mysql_engine import session_scope
import models


def main():
    with session_scope() as session:
        customer = session.query(models.Customer).first()
        print(customer)


if __name__ == '__main__':
    main()

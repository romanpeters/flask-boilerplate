import time
from app import database as db
from app import account as acc

def main():
    start = time.time()
    session = db.Session()
    entries = session.query(db.Users).all()

    for u in entries:
        user = acc.User(sco=u.user_id, pwd=u.password)  # updates reservations
        if not user.login_is_valid:
            print(f"Couldn't log in {u.user_id}")
            invalid_user = session.query(db.Users).filter_by(user_id=u.user_id)
            session.delete(invalid_user)
    session.commit()
    end = time.time()
    print(f'Update completed in {round(end-start, 2)} seconds')


if __name__=="__main__":
    main()


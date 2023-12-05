import oracledb 


def dbcon():
    return oracledb.connect(user="이름", password="비번", dsn="주소")   # DB에 연결 (호스트이름 대신 IP주소 가능)

def select_area_hp(select_area):
    ret = []
    try:
        db = dbcon()
        con = db.cursor()

        con.execute("select * from hospital where HP_ADDR LIKE '%' || :select_area || '%'", select_area=select_area)
        ret = con.fetchall()
    except Exception as e:
        print('db error:',e)
    finally:
        con.close()
        db.close()
        return ret
    
def select_area_pm(select_area):
    ret = []
    try:
        db = dbcon()
        con = db.cursor()

        con.execute("select * from pharmacy where PM_ADDR LIKE '%' || :select_area || '%'", select_area=select_area)
        ret = con.fetchall()
    except Exception as e:
        print('db error:',e)
    finally:
        con.close()
        db.close()
        return ret
        
def search_hp(search):
    ret = []
    try:
        db = dbcon()
        con = db.cursor()

        con.execute("select * from hospital where HP_NAME LIKE '%' || :search || '%'", search=search)
        ret = con.fetchall()
    except Exception as e:
        print('db error:',e)
    finally:
        con.close()
        db.close()
        return ret
    
def search_pm(search):
    ret = []
    try:
        db = dbcon()
        con = db.cursor()

        con.execute("select * from pharmacy where PM_NAME LIKE '%' || :search || '%'", search=search)
        ret = con.fetchall()
    except Exception as e:
        print('db error:',e)
    finally:
        con.close()
        db.close()
        return ret

def select_all_hp():
    ret = []
    try:
        db = dbcon()
        con = db.cursor()
        con.execute("select * from hospital")
        ret = con.fetchall()
    except Exception as e:
        print('db error:',e)
    finally:
        con.close()
        db.close()
        return ret

def select_all_pm():
    ret = []
    try:
        db = dbcon()
        con = db.cursor()
        con.execute("select * from pharmacy")
        ret = con.fetchall()
    except Exception as e:
        print('db error:',e)
    finally:
        con.close()
        db.close()
        return ret

def update_ll(id, latit, longit):
    try:
        db = dbcon()
        con = db.cursor()
        #setdata = (id, name, passwd, email, address, birth)
        con.execute(f"update pharmacy set latit='{latit}',longit='{longit}' where id ='{id}'")
        db.commit()  #을 해야 db에 적용이 됩니다.. ㅎ
    except Exception as e:
        print('db error:',e)
    finally:
        con.close()
        db.close()

def select_name(idx, name):
    ret = []
    try:
        db = dbcon()
        con = db.cursor()
        #print(f"select * from user_db where id='{id}' and passwd ='{passwd}'")
        con.execute(f"select name from youth_build where idx='{idx}'")
        ret = con.fetchall()
    except Exception as e:
        print('db error:',e)
    finally:
        con.close()
        db.close()
        return ret
    
def select_hhp(idx):
    ret = []
    try:
        db = dbcon()
        con = db.cursor()
        #print(f"select * from user_db where id='{id}' and passwd ='{passwd}'")
        con.execute(f"select hp_name, hp_addr, hp_numb from hospital where id='{idx}'")
        ret = con.fetchall()
    except Exception as e:
        print('db error:',e)
    finally:
        con.close()
        db.close()
        return ret

def select_ppm(idx):
    ret = []
    try:
        db = dbcon()
        con = db.cursor()
        #print(f"select * from user_db where id='{id}' and passwd ='{passwd}'")
        con.execute(f"select pm_name, pm_addr, pm_numb from pharmacy where id='{idx}'")
        ret = con.fetchall()
    except Exception as e:
        print('db error:',e)
    finally:
        con.close()
        db.close()
        return ret
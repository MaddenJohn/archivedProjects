Select max(salary) from users where salary not in (select max(salary) from users)